# SPDX-License-Identifier: GPL-3.0-or-later
"""Exercise pinned cell destructors and constructor cleanup in an owned process.

Reads the pinned installed PE through the owned retained-population PE reader.
Maps only six bounded original instruction ranges at their preferred addresses
inside this disposable Python process. A recording free callback replaces the
cell allocator thunk; it never frees an engine object. Source slots point to an
owned PAGE_NOACCESS page. Writes hashes, substitutions and oracles to a fresh
ignored output directory. No game, debugger, save, database, network or Git effect.
An unexpected native fault fails the process; no exception is suppressed.
"""
import ctypes as C
import faulthandler
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import struct
import sys

ROOT = Path(__file__).resolve().parents[2]


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    faulthandler.enable()
    out = (ROOT / sys.argv[1]).resolve()
    assert out.is_relative_to(ROOT / '.local-work/d5ab')
    out.mkdir(parents=True, exist_ok=False)
    (out/'source.py').write_bytes(Path(__file__).read_bytes())
    free = {drive: shutil.disk_usage(drive).free for drive in ('C:/', 'D:/')}
    assert min(free.values()) >= 40_000_000_000
    method = ROOT / 'runtime/retained-population/build.py'
    spec = importlib.util.spec_from_file_location('p1_owned_pe', method)
    pe = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(pe)
    executable = pe.GAME / 'Starfield.exe'
    assert sha(executable) == pe.GAME_HASH
    image = executable.read_bytes()
    kernel = C.WinDLL('kernel32', use_last_error=True)
    kernel.VirtualAlloc.argtypes = [C.c_void_p, C.c_size_t, C.c_ulong, C.c_ulong]
    kernel.VirtualAlloc.restype = C.c_void_p
    kernel.VirtualProtect.argtypes = [C.c_void_p, C.c_size_t, C.c_ulong, C.POINTER(C.c_ulong)]
    kernel.FlushInstructionCache.argtypes = [C.c_void_p, C.c_void_p, C.c_size_t]
    pages = set()

    def install(address, raw):
        page = address & ~0xffff
        assert address + len(raw) <= page + 65536
        if page not in pages:
            allocated=kernel.VirtualAlloc(page, 65536, 0x3000, 4)
            assert allocated == page, (hex(page),allocated,C.get_last_error())
            pages.add(page)
        C.memmove(address, raw, len(raw))

    ranges = [(0x982d90, 1107), (0x9858d0, 43), (0x985c20, 43), (0x986050, 43),
              (0x2b6280, 66), (0x2c5b40, 11)]
    pins = []
    for rva, size in ranges:
        raw = pe.pe_read(image, rva, size)
        install(0x140000000 + rva, raw)
        pins.append(dict(rva=hex(rva), size=size, sha256=hashlib.sha256(raw).hexdigest()))
    calls = []

    @C.WINFUNCTYPE(None, C.c_void_p, C.c_size_t, C.c_void_p)
    def record_free(pointer, size, unused):
        calls.append((pointer, size))

    thunk = 0x14365cdb0
    stub = b'\x48\xb8' + struct.pack('<Q', C.cast(record_free, C.c_void_p).value) + b'\xff\xe0'
    install(thunk, stub)
    constructor_calls=[]
    bounds_allowed=True

    @C.WINFUNCTYPE(None, C.c_void_p)
    def acquire(pointer):
        constructor_calls.append('lock')
        C.c_uint32.from_address(pointer+4).value=0x20000

    @C.WINFUNCTYPE(C.c_void_p, C.c_void_p, C.c_void_p)
    def origin(grid, output):
        C.memset(output,0,8)
        return output

    @C.WINFUNCTYPE(C.c_uint64, C.c_void_p, C.c_void_p, C.c_void_p, C.c_void_p, C.c_void_p)
    def bounds(*unused):
        constructor_calls.append('bounds')
        return int(bounds_allowed)

    callbacks={0x1422c8d10:acquire,0x1409870d0:origin,0x140982d00:bounds}
    for address,callback in callbacks.items():
        install(address,b'\x48\xb8'+struct.pack('<Q',C.cast(callback,C.c_void_p).value)+b'\xff\xe0')
    for page in pages:
        old = C.c_ulong()
        assert kernel.VirtualProtect(page, 65536, 0x20, C.byref(old))
        assert kernel.FlushInstructionCache(C.c_void_p(-1), page, 65536)
    inaccessible = kernel.VirtualAlloc(None, 4096, 0x3000, 1)
    assert inaccessible
    rows = []
    constructor=C.WINFUNCTYPE(C.c_void_p,*([C.c_void_p]*6),C.c_float,C.c_float)(0x140982d90)
    grid=C.create_string_buffer(0x70)
    source=C.create_string_buffer(0x1a0)
    array=(C.c_uint64*2)(0,C.addressof(source))
    coordinates=(C.c_int32*2)(23,-7)
    C.memmove(C.addressof(source)+0x10,coordinates,8)
    C.memmove(C.addressof(grid)+0x10,struct.pack('<IIQ',2,2,C.addressof(array)),16)
    master=C.create_string_buffer(0x50)
    descriptor=C.create_string_buffer(0x2c)
    for allowed in (False,True):
        bounds_allowed=allowed
        constructor_calls.clear()
        result=constructor(C.addressof(grid),C.addressof(master),C.addressof(coordinates),
                           C.addressof(coordinates),C.addressof(coordinates),C.addressof(descriptor),0.0,0.0)
        assert result==(C.addressof(source) if allowed else None)
        assert constructor_calls==['lock','bounds']
        assert C.c_uint32.from_buffer(grid,0x60).value==0
        assert list(array)==[0,C.addressof(source)]
        rows.append(dict(case='constructor-dedup' if allowed else 'constructor-bounds-refusal',passed=True,
                         original_instructions=True,allocation_called=False))
    for rva, size in ((0x9858d0, 0x28), (0x985c20, 0x40), (0x986050, 0x78)):
        for deleting in (0, 1):
            cell = C.create_string_buffer(size)
            address = C.addressof(cell)
            for offset in range(0x18, size - 7, 8):
                C.memmove(address + offset, struct.pack('<Q', inaccessible), 8)
            before = bytes(cell)
            start = len(calls)
            function = C.WINFUNCTYPE(C.c_void_p, C.c_void_p, C.c_uint64)(0x140000000 + rva)
            result = function(address, deleting)
            expected = [(address, size)] if deleting else []
            assert result == address and calls[start:] == expected
            assert bytes(cell)[8:] == before[8:]
            assert struct.unpack_from('<Q', cell)[0] == 0x144b67ff8
            rows.append(dict(case=f'cell-{rva:x}-{deleting}', passed=True,
                             receiver_bytes=size, free_calls=len(expected), source_page='PAGE_NOACCESS'))
    slot = C.c_uint64(inaccessible)
    restore = C.WINFUNCTYPE(None, C.c_void_p)(0x1402c5b40)
    restore(C.addressof(slot))
    assert slot.value == 0x144af7060
    rows.append(dict(case='allocator-functor-cleanup', passed=True,
                     source_page='PAGE_NOACCESS', effect='Restores only the stack object vtable.'))
    release = C.WINFUNCTYPE(None, C.c_void_p)(0x1402b6280)
    for word, expected in ((0x20000, 0), (0x10001, 0)):
        lock = (C.c_uint32 * 2)(123, word)
        holder = C.c_void_p(C.addressof(lock))
        release(C.addressof(holder))
        assert lock[1] == expected
        if word == 0x10001:
            assert lock[0] == 0
        rows.append(dict(case=f'lock-cleanup-{word:x}', passed=True))
    result = dict(schema='sor-d5ab-p1-native-controls/1', passed=True, rows=rows,
                  executable_sha256=pe.GAME_HASH, source_sha256=sha(__file__),
                  owned_pe_reader_sha256=sha(method), ranges=pins, initial_free=free,
                  substitutions=[dict(va=hex(thunk), behavior='Recording callback; no actual free.'),
                                 dict(va=hex(0x1422c8d10),behavior='Owned lock-state setup.'),
                                 dict(va=hex(0x1409870d0),behavior='Owned zero origin output.'),
                                 dict(va=hex(0x140982d00),behavior='Explicit true/false bounds oracle.')],
                  limits='Bounded original cell/helper instructions; no complete engine constructor, allocator, retail scheduling or asynchronous unwind test.')
    (out / 'receipt.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf8', newline='\n')
    print(json.dumps(dict(passed=True, tests=len(rows))))


if __name__ == '__main__':
    main()
