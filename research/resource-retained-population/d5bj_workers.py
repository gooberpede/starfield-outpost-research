# SPDX-License-Identifier: GPL-3.0-or-later
"""Run three original worker loops on one private, preloaded pool.

SOR-P-0002 lineage: D5S export43 and D5BJ dispatch. Python owns thread start,
pool construction, memory-context TLS and bounded stop. The worker binds its
own scheduler TLS and claims and calls one native-tagged command per thread.
"""
import argparse
import ctypes as C
import json
from pathlib import Path
import shutil
import struct
import sys
import threading

sys.path.insert(0, str(Path(__file__).resolve().parent))
import d5bj_sampler as host

CODE = (0x1402b7000, 0x1428d1000, 0x1428d2000, 0x1428d3000, 0x1428d4000)
DATA = (0x143a3f000, 0x143a40000, 0x144f04000, 0x145e60000,
        0x145e9b000, 0x1461fa000, 0x1482df000)
COUNT = 3
require = host.require
address = C.addressof


def original_getter_sites(pe):
    sections = host.pe_sections(pe)
    sites = (0x1418a9009, 0x1427eeee7)
    for site in sites:
        offsets = [raw + site - start for name, start, virtual, size, raw, _ in sections
                   if name == b'.text' and start <= site and site + 7 <= start + min(virtual, size)]
        require(len(offsets) == 1, 'Getter operand outside pinned text')
        off = offsets[0]
        require(pe[off:off + 3] == b'\x48\x8d\x15'
                and site + 7 + struct.unpack_from('<i', pe, off + 3)[0] == 0x1428d1880,
                'Original JobSite constructor does not bind the common getter')


def controls(kernel, pages):
    kernel.TlsAlloc.restype = C.c_uint32
    kernel.TlsFree.argtypes = [C.c_uint32]
    kernel.TlsSetValue.argtypes = [C.c_uint32, C.c_void_p]
    kernel.TlsGetValue.argtypes = [C.c_uint32]
    kernel.TlsGetValue.restype = C.c_void_p
    memory_slot, worker_slot = kernel.TlsAlloc(), kernel.TlsAlloc()
    require(0xffffffff not in (memory_slot, worker_slot), 'Could not allocate private TLS')
    owner = C.create_string_buffer(0x340)
    pool = address(owner) + 0x140
    contexts = C.create_string_buffer(COUNT * 0xc0)
    memory_owner = C.create_string_buffer(0x488)
    memory_contexts = [C.create_string_buffer(0x420) for _ in range(COUNT)]
    queues = []
    base = address(contexts)
    C.c_uint64.from_address(pool + 0xc8).value = base
    C.c_uint32.from_address(pool + 0xe0).value = COUNT
    C.c_uint32.from_address(pool + 0xe8).value = COUNT
    stop = C.c_uint8.from_address(pool + 0xec)
    for index in range(COUNT):
        struct.pack_into('<QI', contexts, index * 0xc0 + 0x88, pool, index)
    for location in (pool, *(base + i * 0xc0 for i in range(COUNT))):
        ring, peers = C.create_string_buffer(0x40 + 8 * 8), C.create_string_buffer(COUNT * 8)
        queues.extend((ring, peers))
        struct.pack_into('<QQ', ring, 0, 8, 7)
        C.c_uint64.from_address(location + 0x48).value = address(ring)
        C.c_uint64.from_address(location + 0x60).value = address(peers)

    host.allocate_pages(kernel, pages)
    for slot, value in ((0x1461fabe8, address(owner)), (0x143a3f390, C.cast(kernel.TlsGetValue, C.c_void_p).value),
                        (0x143a3f398, C.cast(kernel.TlsSetValue, C.c_void_p).value),
                        (0x143a3f2a8, C.cast(kernel.GetCurrentThread, C.c_void_p).value)):
        C.c_uint64.from_address(slot).value = value
    C.c_uint32.from_address(0x1482dfa10).value = memory_slot
    C.c_uint32.from_address(0x145e9b174).value = worker_slot
    # Return the private memory owner. Bypass the unused static CRT TLS load
    # on the no-idle route without touching the host's TEB or CRT data.
    C.memmove(0x1402b7e60, b'\x48\xb8' + struct.pack('<Q', address(memory_owner)) + b'\xc3', 11)
    C.memmove(0x1428d3c8b, b'\x90' * 9, 9)
    C.memmove(0x1428d3c9a, b'\x31\xed\x90', 3)
    for page in pages:
        host.protect(kernel, page, 0x20 if page in CODE else 2)
    host.flush(kernel)
    require(host.callsite(0x1428d1880, 0)() == pool, 'Native shared-pool getter differs')
    invoke = C.WINFUNCTYPE(None, C.c_void_p, C.c_uint32)(0x1428d3b90)
    push = host.callsite(0x1428d2b80, 2, C.c_uint64)
    errors, trace = [], []
    released = threading.Barrier(COUNT, action=lambda: setattr(stop, 'value', 1), timeout=8)

    @C.WINFUNCTYPE(None, C.c_void_p)
    def command(payload):
        try:
            index = C.c_uint64.from_address(payload + 16).value
            require(index < COUNT and kernel.TlsGetValue(worker_slot) == base + 0xc0 * index
                    and C.c_uint64.from_address(base + 0xc0 * index + 0x88).value == pool,
                    'Callback received a wrong worker TLS or pool')
            trace.append((index, kernel.GetCurrentThreadId()))
            released.wait()
        except (ValueError, threading.BrokenBarrierError) as error:
            errors.append(str(error))
            stop.value = 1

    commands = []
    for i in range(COUNT):
        value = (C.c_uint64 * 3)(0, C.cast(command, C.c_void_p).value, i)
        commands.append(value)
        push(base + i * 0xc0, C.byref(C.c_uint64(address(value) | 1)))

    def work(index):
        if not kernel.TlsSetValue(memory_slot, address(memory_contexts[index])):
            errors.append('Worker memory TLS failed')
            stop.value = 1
            released.abort()
            return
        invoke(pool, index)
        kernel.TlsSetValue(memory_slot, None)
        kernel.TlsSetValue(worker_slot, None)

    threads = [threading.Thread(target=work, args=(i,), daemon=True) for i in range(COUNT)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(12)
    if any(thread.is_alive() for thread in threads):
        stop.value = 1
        released.abort()
        raise ValueError('Private worker failed to return before its fixture bound')
    require(not errors and sorted(i for i, _ in trace) == list(range(COUNT))
            and len({thread for _, thread in trace}) == COUNT, f'Native worker callback check failed: {errors}')
    require(C.c_uint32.from_address(pool + 0xe8).value == 0 and all(
        struct.unpack_from('<I', memory, 0x410)[0] == 0 for memory in memory_contexts),
        'Native worker shutdown counters did not drain')
    require(kernel.TlsFree(memory_slot) and kernel.TlsFree(worker_slot), 'Private TLS release failed')
    return {'live_native_worker_loops': COUNT, 'original_constructor_getter_operands': 2,
            'native_callbacks': len(trace), 'shutdown_counters_drained': True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--exe', required=True, type=Path)
    args = parser.parse_args()
    try:
        kernel, _ = host.host_preflight()
        exe = host.regular(args.exe)
        drives = {exe.anchor, Path.cwd().anchor, Path(sys.executable).anchor}
        require(all(shutil.disk_usage(drive).free >= 40_000_000_000 for drive in drives), 'Insufficient disk floor')
        pe = host.read_pinned(exe, host.EXE, 'Starfield EXE', keep=True)
        original_getter_sites(pe)
        host.cpu_check(kernel)
        result = controls(kernel, host.pe_pages(pe, CODE, DATA))
    except (OSError, ValueError, struct.error) as error:
        parser.exit(1, f'D5BJ native workers refused: {error}\n')
    print(json.dumps(dict(scope='Original worker body on fixture-started private OS threads',
                          exe=host.EXE, **result), sort_keys=True))


if __name__ == '__main__':
    main()
