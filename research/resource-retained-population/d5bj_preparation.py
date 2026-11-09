# SPDX-License-Identifier: GPL-3.0-or-later
"""Execute D5S rectangle admission, registration and traversal in private pages.

SOR-P-0002 adaptation of the D5S preparation and D5BJ page-host methods.
Uses caller-owned objects, command reservation and resident-cell recording
seams. Reads the pinned local EXE and emits JSON on stdout.
"""
import argparse
import ctypes as C
import json
from pathlib import Path
import shutil
import struct
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import d5bj_sampler as host

CODE = (
    0x140323000, 0x140362000, 0x14079c000, 0x14079d000, 0x1407b1000,
    0x1407b4000, 0x1407b5000, 0x1418aa000, 0x1422c8000, 0x1422cd000, 0x1422ce000, 0x1427e4000,
    0x1427e5000, 0x1427e6000, 0x1427e9000, 0x1427ea000, 0x1427ec000, 0x1428d1000,
    0x1428d5000, 0x1428d7000, 0x1428d8000, 0x1428d9000,
)
DATA = (
    0x143a3f000, 0x143a40000, 0x144afc000, 0x144b00000, 0x144b3f000,
    0x144d9c000, 0x144da7000, 0x1458d5000, 0x145fd9000, 0x1461e1000, 0x1461ef000, 0x1461fa000,
)
TRIPLE = (1, 2, 3)
RECTANGLE = (-16, -16, 23, 23)
require = host.require
address = C.addressof


class CommandBuffer:
    def __init__(self, site=None):
        self.site = C.create_string_buffer(0x2a0) if site is None else site
        self.segment = C.create_string_buffer(0xc0)
        self.receiver = address(self.site) + 0x40
        self.commands = self.receiver + 0x40
        host.put(self.site, 0x1d0, '<Q', address(self.segment))
        host.put(self.site, 0x1e4, '<I', 128)
        host.put(self.segment, 0x10, '<I', 128)
        struct.pack_into('<6H', self.site, 0x28a, 1, 2, 4, 8, 16, 32)
        host.put(self.site, 0x296, '<H', 9)
        self.used = 0

    def committed(self):
        return struct.unpack_from('<I', self.segment, 0xc)[0]

    def state(self):
        return struct.unpack_from('<H', self.site, 0x296)[0]

    def reserve(self, result, size):
        require(size in (32, 40) and self.used + size <= 128, 'Unexpected command reservation')
        offset = self.used
        self.used += size
        struct.pack_into('<II', self.segment, 0x40 + offset, size, 128)
        C.memmove(result, struct.pack('<QII', address(self.segment), offset, size), 16)
        return address(self.segment) + 0x48 + offset


class Preparation:
    def __init__(self, kernel, pages):
        self.receiver = CommandBuffer()
        self.manager = C.create_string_buffer(0x210)
        self.index = C.create_string_buffer(0x70)
        self.content = C.create_string_buffer(0x500)
        self.service = CommandBuffer((C.c_char * 0x2a0).from_buffer(self.content, 0x40))
        self.server_owner = C.create_string_buffer(0x450)
        self.node = C.create_string_buffer(0xe0)
        self.layer = C.create_string_buffer(0xc0)
        self.pool_owner = C.create_string_buffer(0x400)
        self.outer_result = C.create_string_buffer(0x28)
        self.cells = []
        self.callbacks = []
        self.errors = []
        self.allocated = False
        self.layer_allocated = False
        self.followups = []
        self.registrations = []
        self.republications = []
        self.released = False
        self.server = address(self.server_owner) + 0x40
        self.wake = (C.c_uint64 * 4)(0x144da7db8, address(self.service.site), 0x1428d1880, 0)
        host.put(self.service.site, 0x278, '<Q', address(self.wake))
        host.put(self.server_owner, 0x70, '<Q', self.receiver.receiver)
        host.put(self.manager, 0x80, '<I', 0x5e0de)
        host.put(self.manager, 0x120, '<Q', address(self.index))
        struct.pack_into('<3I', self.manager, 0x60, *TRIPLE)
        host.allocate_pages(kernel, pages)
        for slot, buffer in ((0x145fd9c30, self.manager), (0x145fd9c38, self.server_owner),
                             (0x1461e1d80, self.content), (0x1461fabe8, self.pool_owner)):
            C.c_void_p.from_address(slot).value = address(buffer)
        ptr, word = C.c_void_p, C.c_uint32
        self.hook(0x1427e4a30, ptr, (ptr, word), self.allocate)
        self.hook(0x1422cdf60, ptr, (ptr, ptr, word, word), self.reserve)
        self.hook(0x1427e6c00, None, (ptr,), self.followups.append)
        self.hook(0x1427e9f70, C.c_uint8, (ptr, ptr, ptr), self.register_active)
        self.hook(0x1428d8fe0, C.c_uint64, (ptr, ptr), self.publish)
        self.hook(0x1418aa1c0, None, (ptr, ptr, C.c_uint8), self.resident_cell)
        self.bind(0x143a3f418, kernel.GetCurrentThreadId)
        self.bind(0x143a40258, self.callback(C.c_int, (ptr,), self.clock))
        self.bind(0x143a402c8, self.callback(None, (ptr,), self.validate_wake))
        self.install_pump_boundary()
        layer_boundary = 0x1407b4d08
        require(C.string_at(layer_boundary, 8) == bytes.fromhex('48 8b 45 48 48 8b 48 30'),
                'Unexpected layer registration boundary')
        # Stop the layer producer after publishing its registration command,
        # before starting its dependent density-neighbor and layer work.
        C.memmove(layer_boundary, b'\xe9' + struct.pack('<i', 0x1407b513a - layer_boundary - 5) + b'\x90' * 3, 8)
        for page in pages:
            host.protect(kernel, page, 0x20 if page in CODE else 2)
        host.flush(kernel)
        self.producer = host.callsite(0x14079ce00, 2, C.c_uint8)
        self.receive = host.callsite(0x1428d8060, 1, C.c_uint8)
        self.pump = C.WINFUNCTYPE(None, ptr, C.c_float)(0x1428d89b0)
        self.layer_producer = host.callsite(0x1407b4bb0, 4, None)
        self.dispatch_registration = host.callsite(0x1427eaf50, 1, None)
        self.destroy = C.WINFUNCTYPE(ptr, ptr, word)(0x1407b19f0)

    def callback(self, result, args, operation):
        def guard(*values):
            try:
                return operation(*values)
            except (ValueError, OSError, struct.error) as error:
                self.errors.append(str(error))
                return None if result in (None, C.c_void_p) else 0
        function = C.WINFUNCTYPE(result, *args)(guard)
        self.callbacks.append(function)
        return function

    def bind(self, slot, function):
        C.c_void_p.from_address(slot).value = C.cast(function, C.c_void_p).value

    def hook(self, entry, result, args, operation):
        function = self.callback(result, args, operation)
        jump = b'\x48\xb8' + struct.pack('<Q', C.cast(function, C.c_void_p).value) + b'\xff\xe0'
        C.memmove(entry, jump, len(jump))

    def install_pump_boundary(self):
        boundary, scratch, unwind = 0x1428d8a4e, 0x1428d5000, 0x1428d8b3a
        require(C.string_at(boundary, 7) == bytes.fromhex('44 89 ab 84 02 00 00'),
                'Unexpected original instruction at receiver return')
        callback = self.callback(None, (C.c_void_p,), self.after_release)
        # The native stack is already aligned. Pass the site in RBX to the
        # Win64 callback and return via the original epilogue, stopping before
        # any additional pump iteration or normal terminal wake.
        shim = bytes.fromhex('48 83 ec 20 48 89 d9 48 b8')
        shim += struct.pack('<Q', C.cast(callback, C.c_void_p).value)
        shim += bytes.fromhex('ff d0 48 83 c4 20')
        shim += b'\xe9' + struct.pack('<i', unwind - (scratch + len(shim) + 5))
        C.memmove(scratch, shim, len(shim))
        C.memmove(boundary, b'\xe9' + struct.pack('<i', scratch - (boundary + 5)) + b'\x90\x90', 7)

    def allocate(self, context, size):
        if size == C.sizeof(self.layer):
            require(not self.layer_allocated, 'Unexpected second layer allocation')
            self.layer_allocated = True
            return address(self.layer)
        require(size == C.sizeof(self.node) and not self.allocated, 'Unexpected node allocation')
        self.allocated = True
        return address(self.node)

    def reserve(self, queue, result, size, align):
        require(align == 8, 'Unexpected command alignment')
        if queue == self.receiver.commands:
            return self.receiver.reserve(result, size)
        require(queue == self.service.commands, 'Unexpected command queue')
        return self.service.reserve(result, size)

    def clock(self, result):
        C.c_uint64.from_address(result).value = 123
        return 1

    def validate_wake(self, pointer):
        require(pointer == address(self.manager) + 0x70, 'Unexpected lock wake')

    def resident_cell(self, content, coord, flag):
        require(content == address(self.content) and flag == 1 and len(self.cells) < 1600,
                'Wrong resident-cell service operand')
        require(self.service.state() == 9 and struct.unpack_from('<I', self.service.site, 0x44)[0] == 0x10001,
                'Rectangle worker entered outside its qualified service receiver')
        self.cells.append(tuple((C.c_int32 * 2).from_address(coord)))

    def publish(self, pool, payload):
        self.republications.append((pool, payload))
        return 0

    def register_active(self, table, reader, node):
        require(table == reader == self.server + 0x38 and node in (address(self.node), address(self.layer)),
                'Unexpected server active-map insertion operands')
        self.registrations.append(node)
        return 1

    def admit(self, triple, mode, ready):
        host.put(self.manager, 0x20, '<B', mode)
        host.put(self.index, 0x60, '<B', ready)
        task = (C.c_uint32 * 7)(*triple, *RECTANGLE)
        return self.producer(task, self.outer_result)

    def readers(self):
        return struct.unpack_from('<I', self.manager, 0x28)[0]

    def after_release(self, site):
        require(site == address(self.service.site) and not self.released
                and struct.unpack_from('<II', self.service.site, 0x40) == (0, 0)
                and self.service.state() == 9, 'Wrong native post-receiver state')
        require(len(self.cells) == 1600 and self.receiver.committed() == 72,
                'Receiver released before the nonempty worker posted completion')
        self.released = True
        # Produce the original layer-preparation node. Invoke the generated
        # registration callback directly. The original server drain is outside
        # this fixture, so rectangle completion stays recorded in its queue.
        query = (C.c_int32 * 2)(-2, 11)
        self.layer_producer(query, None, None, None)
        require(self.layer_allocated and self.receiver.committed() == 104
                and struct.unpack_from('<4Q', self.receiver.segment, 0x90)
                == (0x144d9cb50, 0x1427eaf50, self.server, address(self.layer))
                and struct.unpack_from('<Q', self.layer)[0] == 0x144b40708
                and struct.unpack_from('<Q', self.layer, 0x98)[0] == site
                and self.layer.raw[0xa0] == 1
                and struct.unpack_from('<2i', self.layer, 0xb0) == (-2, 11),
                'Native layer producer emitted the wrong registration')
        self.dispatch_registration(address(self.receiver.segment) + 0x90)
        require(self.layer.raw[0xa8] == 4 and self.service.committed() == 64
                and self.service.state() == 25 and not self.republications
                and struct.unpack_from('<4Q', self.service.segment, 0x68)
                == (0x144d9cbd0, 0x1427ec2e0, address(self.layer), self.server),
                'Native layer command failed to remain pending')

    def run(self):
        for triple, mode, ready, expected in (
            ((1, 2, 4), 2, 1, 5), (TRIPLE, 3, 1, 3), (TRIPLE, 2, 0, 3),
        ):
            require(self.admit(triple, mode, ready) == expected and not self.allocated
                    and not self.receiver.committed() and not self.readers() and not self.errors,
                    'Rejected rectangle admitted a node or retained a reader')
        getter = host.callsite(0x1428d1880, 0)
        require(getter() == address(self.pool_owner) + 0x140, 'Native embedded pool getter differs')
        require(self.admit(TRIPLE, 2, 1) == 5 and self.receiver.committed() == 32
                and self.allocated and not self.errors, 'Native rectangle producer failed')
        require(struct.unpack_from('<4Q', self.receiver.segment, 0x48)
                == (0x144d9cb50, 0x1427eaf50, self.server, address(self.node)),
                'Native registration command identity mismatch')
        require(struct.unpack_from('<Q', self.node)[0] == 0x144b3f158
                and struct.unpack_from('<Q', self.node, 0x98)[0] == address(self.content) + 0x40
                and self.node.raw[0xa0] == 1 and self.node.raw[0xc0] == 1
                and struct.unpack_from('<Q', self.node, 0xb8)[0] == address(self.manager)
                and struct.unpack_from('<4i', self.node, 0xc8) == RECTANGLE and self.readers() == 1,
                'Rectangle node did not capture its bounds, scope and reader')
        require(self.receive(self.receiver.receiver) == 1 and not self.errors and not self.cells,
                f'Native registration did not defer work to ContentManager: {self.errors}')
        require(self.followups == [self.server] and self.registrations == [address(self.node)],
                'Wrong server bookkeeping operands')
        require(self.service.committed() == 32 and self.service.state() == 25 and not self.republications
                and self.node.raw[0xa8] == 4
                and struct.unpack_from('<4Q', self.service.segment, 0x48)
                == (0x144d9cbd0, 0x1427ec2e0, address(self.node), self.server),
                'Wrong native tag-1 publication or wake')
        self.pump(self.service.site, 0.)
        require(self.released and not self.errors and self.service.state() == 25,
                f'Native pump did not reach the qualified boundary: {self.errors}')
        require(self.cells == [(x, y) for x in range(-16, 24) for y in range(23, -17, -1)],
                'Native rectangle service order differs')
        require(self.receiver.committed() == 104 and struct.unpack_from('<3Q', self.receiver.segment, 0x68)
                == (0x144b00d68, 0x140362510, self.server)
                and self.receiver.segment.raw[0x80:0x8c] == self.node.raw[8:20],
                'Native completion command identity or key mismatch')
        require(self.destroy(self.node, 0) == address(self.node) and self.readers() == 0,
                'Native destructor leaked the reader')
        return dict(rectangle=RECTANGLE, cells=len(self.cells), completion_queued=True,
                    rejected=['wrong_generation', 'wrong_mode', 'unready_index'],
                    native_pool_getter=True, receiver_released_running_state=9, reader_released=True,
                    native_tag1_publication=True, native_layer_producer_pending=True,
                    observed_post_receiver_va='0x1428d8a4e', pump_fixture_stopped_at_boundary=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--exe', required=True, type=Path)
    args = parser.parse_args()
    try:
        kernel, _ = host.host_preflight()
        exe = host.regular(args.exe)
        drives = {exe.anchor, Path.cwd().anchor, Path(sys.executable).anchor}
        require(all(shutil.disk_usage(drive).free >= 40_000_000_000 for drive in drives), 'Insufficient disk floor')
        pages = host.pe_pages(host.read_pinned(exe, host.EXE, 'Starfield EXE', keep=True), CODE, DATA)
        host.cpu_check(kernel)
        result = Preparation(kernel, pages).run()
    except (OSError, ValueError, struct.error) as error:
        parser.exit(1, f'D5BJ preparation refused: {error}\n')
    print(json.dumps(dict(scope='Native rectangle admission, command, iteration and completion publication',
                          exe=host.EXE, **result), sort_keys=True))


if __name__ == '__main__':
    main()
