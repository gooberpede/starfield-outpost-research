# SPDX-License-Identifier: GPL-3.0-or-later
"""Run the original D5AQ/D5S dispatch, queue claim and JobSite wake controls.

SOR-P-0002 adaptation of D5S native_dispatch.py and d5s_controls.registration.
Uses process-local TLS, private PE pages and five supplied worker contexts.
No worker is started. The wake experiment substitutes a publication recorder.
Input is the pinned local EXE. The disposable process writes JSON to stdout.
"""
import argparse
from collections import deque
import ctypes as C
import json
from pathlib import Path
import shutil
import struct
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import d5bj_sampler as sampler
from d5s_controls import registration

CODE = (
    0x1422c8000, 0x1422ce000, 0x1427eb000, 0x1428d2000, 0x1428d3000,
    0x1428d7000, 0x1428d8000, 0x1428d9000,
)
DATA = (
    0x143a3f000, 0x143a40000, 0x144d9c000, 0x144da7000, 0x145e60000,
    0x1458d5000, 0x145e9b000, 0x1482df000,
)
CONTEXTS = 5
DENSITY_CALLBACK = 0x1427ec2e0
PUMP_CALLBACK = 0x1428d9560
require = sampler.require


def expected_order(count):
    pending = deque()
    for index in range(count):
        if pending:
            imported = pending.popleft()
            pending.extend((index, imported))
        else:
            pending.append(index)
    return list(pending)


class DispatchHost:
    def __init__(self, kernel, pages):
        self.kernel = kernel
        self.allocations = {}
        self.errors = []
        self.publications = []
        self.completed_pumps = []
        self.pool = None
        kernel.TlsAlloc.restype = C.c_uint32
        kernel.TlsSetValue.argtypes = [C.c_uint32, C.c_void_p]
        kernel.TlsSetValue.restype = C.c_int
        kernel.TlsGetValue.argtypes = [C.c_uint32]
        kernel.TlsGetValue.restype = C.c_void_p
        kernel.TlsFree.argtypes = [C.c_uint32]
        self.tls = kernel.TlsAlloc()
        require(self.tls != 0xffffffff, 'Could not allocate disposable TLS slot')
        sampler.allocate_pages(kernel, pages)
        C.c_uint32.from_address(0x145e9b174).value = self.tls
        C.c_void_p.from_address(0x143a3f390).value = C.cast(kernel.TlsGetValue, C.c_void_p).value
        C.c_void_p.from_address(0x143a3f418).value = C.cast(kernel.GetCurrentThreadId, C.c_void_p).value
        self.allocate_callback = C.WINFUNCTYPE(C.c_void_p, C.c_void_p, C.c_uint64, C.c_uint32)(self.allocate)
        self.publish_callback = C.WINFUNCTYPE(C.c_uint64, C.c_void_p, C.c_void_p)(self.publish)
        self.pool_callback = C.WINFUNCTYPE(C.c_void_p)(self.get_pool)
        # No waiting threads are present. Record the terminal private wake.
        self.completed_callback = C.WINFUNCTYPE(None, C.c_void_p)(self.completed_pumps.append)
        C.c_void_p.from_address(0x143a402d8).value = C.cast(self.completed_callback, C.c_void_p).value
        self.stub(0x1422ce9f0, self.allocate_callback)
        for page in pages:
            sampler.protect(kernel, page, 0x20 if page in CODE else 2)
        sampler.flush(kernel)
        self.dispatch = sampler.callsite(0x1427eb6b0, 2, C.c_uint64)
        self.push = sampler.callsite(0x1428d2b80, 2, C.c_uint64)
        self.pop = C.WINFUNCTYPE(C.c_void_p, C.c_void_p, C.c_void_p,
                                 C.c_void_p, C.c_uint8, C.c_uint8)(0x1428d3960)
        self.wake = sampler.callsite(0x1428d96c0, 1, C.c_uint64)
        self.pump_publish = sampler.callsite(0x1428d8fe0, 2, C.c_uint64)

    def stub(self, address, callback):
        jump = b'\x48\xb8' + struct.pack('<Q', C.cast(callback, C.c_void_p).value) + b'\xff\xe0'
        C.memmove(address, jump, len(jump))

    def allocate(self, context, size, alignment):
        if (context, size, alignment) != (1, 32, 8) or len(self.allocations) >= 5160:
            self.errors.append('Unqualified native callback allocation')
            return None
        storage = C.create_string_buffer(size)
        address = C.addressof(storage)
        self.allocations[address] = storage
        return address

    def get_pool(self):
        return C.addressof(self.pool)

    def publish(self, site, payload):
        self.publications.append((site, C.c_uint64.from_address(payload).value))
        return 0

    def setup(self):
        self.pool = C.create_string_buffer(0x200)
        workers = C.create_string_buffer(0xc0 * CONTEXTS)
        self.queue_storage = [workers]
        pool, worker = C.addressof(self.pool), C.addressof(workers)
        sampler.put(self.pool, 0xc8, '<Q', worker)
        sampler.put(self.pool, 0xe0, '<I', CONTEXTS)
        for queue in [pool, *(worker + i * 0xc0 for i in range(CONTEXTS))]:
            ring = C.create_string_buffer(0x40 + 2048 * 8)
            peers = C.create_string_buffer(CONTEXTS * 8)
            self.queue_storage.extend((ring, peers))
            struct.pack_into('<QQ', ring, 0, 2048, 2047)
            C.c_void_p.from_address(queue + 0x48).value = C.addressof(ring)
            C.c_void_p.from_address(queue + 0x60).value = C.addressof(peers)
        for i in range(CONTEXTS):
            struct.pack_into('<QQI', workers, i * 0xc0 + 0x80, 1, pool, i)
        require(self.kernel.TlsSetValue(self.tls, worker), 'Could not bind disposable worker TLS')
        return pool, worker

    def claim(self, pool, worker, callback):
        holder = C.c_uint64()
        self.pop(pool, C.byref(holder), worker, 0, 0)
        require(holder.value in self.allocations, 'Native claim returned a missing or foreign callback')
        target, payload = struct.unpack_from('<QQ', self.allocations[holder.value], 8)
        require(target == callback, f'Native claim returned wrong callback {target:#x}')
        return payload

    def run(self, count, owner):
        pool, worker = self.setup()
        for i in range(count):
            payload = (C.c_uint64 * 2)(i + 0x10000, 0x20000)
            self.dispatch(pool, payload)
            require(not self.errors, str(self.errors))
        result = []
        for _ in range(count):
            result.append(self.claim(pool, worker if owner else worker + 0xc0, DENSITY_CALLBACK) - 0x10000)
            if owner:
                marker = (C.c_uint64 * 2)(0x40000, 0)
                self.pump_publish(pool, marker)
                require(not self.errors and self.claim(pool, worker, PUMP_CALLBACK) == 0x40000,
                        'Unexpected neutral pump callback')
        return result

    def receiver_control(self):
        # An empty command queue gives a finite native acquire, drain and release.
        # Execute it separately with the pump running, then let the empty pump
        # execute its own later running-bit clear.
        site = C.create_string_buffer(0x2a0)
        queue = C.create_string_buffer(0x80)
        sampler.put(site, 0x1d0, '<Q', C.addressof(queue))
        struct.pack_into('<6H', site, 0x28a, 1, 2, 4, 8, 16, 32)
        sampler.put(site, 0x296, '<H', 9)
        receiver = sampler.callsite(0x1428d8060, 1, C.c_uint8)
        require(receiver(C.addressof(site) + 0x40) == 0, 'Empty native receiver reported work')
        require(struct.unpack_from('<II', site, 0x40) == (0, 0)
                and struct.unpack_from('<H', site, 0x296)[0] == 9,
                'Native receiver release changed the separate pump running bit')
        pump = C.WINFUNCTYPE(None, C.c_void_p, C.c_float)(0x1428d89b0)
        pump(site, 0.)
        require(struct.unpack_from('<II', site, 0x40) == (0, 0)
                and struct.unpack_from('<H', site, 0x296)[0] == 1
                and self.completed_pumps == [C.addressof(site) + 0x296],
                'Empty native pump did not clear its running bit')
        return {'receiver_released_running_state': 9, 'completed_pump_state': 1}

    def plain_queue_controls(self, count):
        result = []
        for shared in (False, True):
            for owner in (False, True):
                pool, worker = self.setup()
                for i in range(count):
                    value = C.c_uint64(i + 0x10000)
                    self.push(pool if shared else worker, C.byref(value))
                actual = []
                for _ in range(count):
                    value = C.c_uint64()
                    self.pop(pool, C.byref(value), worker if owner else worker + 0xc0, 0, 0)
                    actual.append(value.value - 0x10000)
                expected = list(reversed(range(count))) if owner and not shared else list(range(count))
                require(actual == expected, 'Native direct or shared queue order differs')
                result.append({'shared': shared, 'owner': owner, 'full_order_equal': True})
        return result

    def populated_receiver_control(self):
        site = C.create_string_buffer(0x2a0)
        queue = C.create_string_buffer(0x80)
        sampler.put(site, 0x1d0, '<Q', C.addressof(queue))
        struct.pack_into('<6H', site, 0x28a, 1, 2, 4, 8, 16, 32)
        sampler.put(site, 0x296, '<H', 9)
        trace = []
        command_address = C.addressof(queue) + 0x48

        @C.WINFUNCTYPE(None, C.c_void_p)
        def command(address):
            if address != command_address:
                self.errors.append('Wrong private preparation command receiver')
                return
            marker, = struct.unpack_from('<Q', queue, 0x58)
            owner, lock = struct.unpack_from('<II', site, 0x40)
            state, = struct.unpack_from('<H', site, 0x296)
            trace.append((marker, owner == self.kernel.GetCurrentThreadId(), lock, state))

        def stage(marker):
            # One terminal, 32-byte private command in the native list format.
            struct.pack_into('<4I', site, 0x1d8, 0, 0, 0, 32)
            sampler.put(queue, 0xc, '<I', 32)
            struct.pack_into('<IIQQQ', queue, 0x40, 32, 32, 0,
                             C.cast(command, C.c_void_p).value, marker)

        def state():
            return struct.unpack_from('<H', site, 0x296)[0]

        receive = sampler.callsite(0x1428d8060, 1, C.c_uint8)
        stage(1)
        require(receive(C.addressof(site) + 0x40) == 1
                and trace == [(1, True, 0x10001, 9)] and not self.errors,
                'Native receiver did not execute the first command under its lock')
        require(struct.unpack_from('<II', site, 0x40) == (0, 0) and state() == 9,
                'Populated receiver did not return released while the pump was running')
        stage(2)
        self.publications.clear()
        request = (C.c_uint64 * 3)(C.addressof(site), C.cast(self.pool_callback, C.c_void_p).value, 0)
        self.wake(request)
        require(state() == 25 and len(trace) == 1 and not self.publications,
                'Second private command did not remain pending after running-site wake')
        self.completed_pumps.clear()
        pump = C.WINFUNCTYPE(None, C.c_void_p, C.c_float)(0x1428d89b0)
        pump(site, 0.)
        require(trace == [(1, True, 0x10001, 9), (2, True, 0x10001, 9)] and not self.errors
                and state() == 1 and struct.unpack_from('<II', site, 0x40) == (0, 0)
                and self.completed_pumps == [C.addressof(site) + 0x296] and not self.publications,
                'Native pump did not service the pending command then clear its running bit')
        return {'first_command_running_state': 9, 'pending_wake_state': 25,
                'extra_publications': 0, 'completed_pump_state': 1, 'ordered_private_commands': [1, 2]}

    def wake_cases(self, count):
        entry = 0x1428d8fe0
        page = entry & ~4095
        sampler.protect(self.kernel, page, 4)
        self.stub(entry, self.publish_callback)
        sampler.protect(self.kernel, page, 0x20)
        sampler.flush(self.kernel)
        site = C.create_string_buffer(0x2a0)
        struct.pack_into('<6H', site, 0x28a, 1, 2, 4, 8, 16, 32)
        payload = (C.c_uint64 * 3)(C.addressof(site), C.cast(self.pool_callback, C.c_void_p).value, 0)
        result = []
        for state, publications in ((1, 1), (9, 0), (25, 0)):
            self.publications.clear()
            sampler.put(site, 0x296, '<H', state)
            for _ in range(count):
                self.wake(payload)
            final, = struct.unpack_from('<H', site, 0x296)
            require(final == 25 and len(self.publications) == publications,
                    f'Unexpected pump publication for state {state}')
            result.append(dict(initial=state, final=final, publications=len(self.publications)))
        return result

    def close(self):
        require(self.kernel.TlsSetValue(self.tls, None) and self.kernel.TlsFree(self.tls),
                'Could not release disposable TLS')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--exe', required=True, type=Path)
    args = parser.parse_args()
    try:
        kernel, _ = sampler.host_preflight()
        exe = sampler.regular(args.exe)
        drives = {exe.anchor, Path.cwd().anchor, Path(sys.executable).anchor}
        require(all(shutil.disk_usage(drive).free >= 40_000_000_000 for drive in drives), 'Insufficient disk floor')
        pages = sampler.pe_pages(sampler.read_pinned(exe, sampler.EXE, 'Starfield EXE', keep=True), CODE, DATA)
        sys.setrecursionlimit(10000)
        coordinates, registrations = registration()
        require((len(coordinates), len(registrations)) == (1600, 1720), 'Unqualified registration model')
        support = set(sampler.GRID)
        offsets = ((-1, 1), (-1, 0), (0, 1), (1, 1))
        counterexamples = [(x, y) for x, y in sampler.GRID
                           if all((x + dx, y + dy) not in support for dx, dy in offsets)]
        require(counterexamples == [(-2, 11)], 'Wrong density-only layer exclusion counterexample')
        model = expected_order(len(registrations))
        sampler.cpu_check(kernel)
        host = DispatchHost(kernel, pages)
        try:
            owner, peer = host.run(len(model), True), host.run(len(model), False)
            require(owner == model[::-1] and peer == model, 'Native dispatch differs from separate deque model')
            receiver = host.receiver_control()
            queue_controls = host.plain_queue_controls(len(model))
            wakes = host.wake_cases(len(model))
            populated = host.populated_receiver_control()
        finally:
            host.close()
        first = []
        for name, order, expected in (('owner', owner, (58, 845, (10, 11))),
                                      ('peer', peer, (28, 874, (-2, -2)))):
            found = next((i, registration, registrations[registration]) for i, registration in enumerate(order)
                         if registrations[registration] in support)
            require(found == expected, f'Unexpected first C1 coordinate in {name} order')
            first.append(dict(route=name, preceding=found[0], registration=found[1], query=found[2], order=order))
    except (ValueError, OSError, struct.error, StopIteration) as error:
        parser.exit(1, f'D5BJ dispatch refused: {error}\n')
    print(json.dumps(dict(scope='Selected native dispatch, queue claim and wake with supplied contexts',
                          exe=sampler.EXE, root_coordinates=1600, density_registrations=1720,
                          contexts=CONTEXTS, neutral_pump_markers=1720,
                          first_c1_coordinates=first, receiver=receiver, wakes=wakes,
                          plain_queue_controls=queue_controls,
                          populated_receiver=populated,
                          density_only_exclusion_counterexamples=counterexamples), sort_keys=True))


if __name__ == '__main__':
    main()
