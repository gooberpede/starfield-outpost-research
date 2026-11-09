# SPDX-License-Identifier: GPL-3.0-or-later
"""Execute the original selected-source provider block through map lookup.

SOR-P-0002 lineage: D5S export29 and D5AR source-lifetime/map controls.
The private ABI shim starts after source selection and stops at the native
branch destinations. Reads only the pinned local EXE and emits JSON.
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

CODE = (0x1402c4000, 0x140349000, 0x14079f000, 0x1407a0000, 0x1422cc000)
DATA = (0x143a3f000, 0x143a40000, 0x144d58000, 0x144d59000)
EXITS = {0x1407a0141: 'no_biome', 0x14079ffaa: 'visited',
         0x14079fcd6: 'hit', 0x14079fd02: 'miss'}
require = host.require
address = C.addressof


class Lookup:
    def __init__(self, kernel, pages):
        host.allocate_pages(kernel, pages)
        sync = C.WinDLL('kernelbase', winmode=0x800)
        for slot, function in ((0x143a3f418, kernel.GetCurrentThreadId),
                               (0x143a402c8, sync.WakeByAddressSingle),
                               (0x143a402d0, sync.WaitOnAddress)):
            C.c_void_p.from_address(slot).value = C.cast(function, C.c_void_p).value
        self.release = host.callsite(0x1402c45a0, 1, None)
        self.names = dict(enumerate(EXITS.values(), 1))
        # Restore the private stack frame and the caller's nonvolatile registers.
        tail = bytes.fromhex('48 83 c4 68 41 5f 41 5e 41 5d 41 5c 5f 5e 5d 5b c3')
        for number, terminal in enumerate(EXITS, 1):
            stub = b'\xb8' + struct.pack('<I', number) + tail
            C.memmove(terminal, stub, len(stub))
        # Align the frame for native calls. Supply the owner, BIOM and source
        # via R13, R15, RDI and the original source local at RSP + 0x38.
        entry = bytes.fromhex(
            '53 55 56 57 41 54 41 55 41 56 41 57 48 83 ec 68 '
            '48 8d 6c 24 50 49 89 cd 49 89 d7 4c 89 c7 48 89 7c 24 38'
        ) + b'\x48\xb8' + struct.pack('<Q', 0x14079fc26) + b'\xff\xe0'
        shim = kernel.VirtualAlloc(None, host.PAGE, 0x3000, 4)
        require(shim, 'Could not allocate private provider frame')
        C.memmove(shim, entry, len(entry))
        host.protect(kernel, shim, 0x20)
        for page in pages:
            host.protect(kernel, page, 0x20 if page in CODE else 2)
        host.flush(kernel)
        self.lookup = host.callsite(shim, 3, C.c_uint32)
        self.thread = kernel.GetCurrentThreadId()

    def run(self, token, seen=(), occupied=False, other_source=False, has_biome=True):
        owner = C.create_string_buffer(0x70)
        source = C.create_string_buffer(0x70)
        foreign = C.create_string_buffer(0x70)
        biome = C.create_string_buffer(0x30)
        holder = C.create_string_buffer(16)
        slots = C.create_string_buffer(24)
        visited = (C.c_uint64 * len(seen))(*seen)
        host.put(biome, 0x28, '<I', 0x145440)
        host.put(source, 0x68, '<Q', token)
        host.put(foreign, 0x68, '<Q', token)
        struct.pack_into('<QQ', owner, 0x20, address(slots), 1)
        struct.pack_into('<I4xQ', owner, 0x48, len(seen), address(visited))
        key = address(foreign if other_source else source) if occupied else 0
        struct.pack_into('<QQI', slots, 0, key, address(holder) if occupied else 0,
                         1 if occupied else 0xffffffff)
        branch = self.names[self.lookup(owner, biome if has_biome else None, source)]
        lock = struct.unpack_from('<II', owner, 0x40)
        if branch in ('hit', 'miss'):
            require(lock == (self.thread, 0x401000), 'Native lookup did not hold the selected owner')
            self.release(address(owner) + 0x40)
            require(struct.unpack_from('<II', owner, 0x40)[1] == 0, 'Native exclusive release leaked')
        else:
            require(lock == (0, 0), 'BIOM or visited exit retained the owner lock')
        return branch

    def controls(self):
        # The discriminator is private. Distinct full tokens share the
        # reader-qualified C1 low word for the counterexample.
        token = (7 << 32) | 1003558160
        variants = [
            ('cold', {}, 'miss'),
            ('same_pointer_holder', {'occupied': True}, 'hit'),
            ('foreign_pointer_holder', {'occupied': True, 'other_source': True}, 'miss'),
            ('same_full_token', {'seen': (token,)}, 'visited'),
            ('same_low_word', {'seen': (token ^ (1 << 32),)}, 'miss'),
            ('visited_with_existing_holder', {'seen': (token,), 'occupied': True}, 'visited'),
            ('no_biome', {'has_biome': False}, 'no_biome'),
        ]
        result = {name: self.run(token, **inputs) for name, inputs, _ in variants}
        require(result == {name: expected for name, _, expected in variants},
                f'Original provider branch differs: {result}')
        return result


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
        result = Lookup(kernel, pages).controls()
    except (OSError, ValueError, KeyError, struct.error) as error:
        parser.exit(1, f'D5BJ protected lookup refused: {error}\n')
    print(json.dumps(dict(scope='Original selected-source BIOM, visited, lock and pointer-map block',
                          exe=host.EXE, branches=result), sort_keys=True))


if __name__ == '__main__':
    main()
