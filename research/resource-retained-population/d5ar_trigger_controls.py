# SPDX-License-Identifier: GPL-3.0-or-later
"""Qualify one nonblocking reader attempt against pinned native lock code.

Uses the owned D5AR PE range mapping method under SOR-P-0002. Executes original
lock operations on fixture words in a disposable process. Reads the pinned EXE
and writes a fresh ignored receipt. No retail process, saves or game state.
"""
import os
import sys

if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '0') not in ('', '0'):
    raise RuntimeError('Use pinned Python -E -B without optimization')

import ctypes as C
import hashlib
import json
from pathlib import Path
import struct
import subprocess
import threading

from d5ar_native_inventory import EXE, PIN, ROOT, disk_floor


def need(condition, reason):
    if not condition:
        raise ValueError(reason)


def owned():
    image = EXE.read_bytes()
    need(hashlib.sha256(image).hexdigest() == PIN, 'Installed executable hash differs')
    pe, = struct.unpack_from('<I', image, 0x3c)
    count, = struct.unpack_from('<H', image, pe + 6)
    optional, = struct.unpack_from('<H', image, pe + 20)
    sections = [struct.unpack_from('<IIII', image, pe + 24 + optional + n * 40 + 8) for n in range(count)]

    def native(address, size):
        rva = address - 0x140000000
        for _, start, length, raw in sections:
            if start <= rva and rva + size <= start + length:
                return image[raw + rva - start:raw + rva - start + size]
        raise ValueError('Original byte range is not file-backed')

    kernel = C.WinDLL('kernel32', use_last_error=True)
    api = C.WinDLL('kernelbase', use_last_error=True)
    kernel.VirtualAlloc.argtypes = [C.c_void_p, C.c_size_t, C.c_ulong, C.c_ulong]
    kernel.VirtualAlloc.restype = C.c_void_p
    kernel.VirtualProtect.argtypes = [C.c_void_p, C.c_size_t, C.c_ulong, C.POINTER(C.c_ulong)]
    kernel.GetCurrentProcess.restype = C.c_void_p
    kernel.FlushInstructionCache.argtypes = [C.c_void_p, C.c_void_p, C.c_size_t]
    api.WaitOnAddress.argtypes = [C.c_void_p, C.c_void_p, C.c_size_t, C.c_uint32]
    api.WaitOnAddress.restype = C.c_int
    api.WakeByAddressSingle.argtypes = api.WakeByAddressAll.argtypes = [C.c_void_p]
    code_pages = (0x1422cc000, 0x1402c4000, 0x1421e0000)
    blocks = {page & ~0xffff for page in (*code_pages, 0x143a3f000, 0x143a40000)}
    for block in sorted(blocks):
        need(kernel.VirtualAlloc(block, 0x10000, 0x3000, 4) == block, f'Cannot reserve owned block {block:#x}')
    ranges = {0x1422cc350: 0x7e, 0x1422cc3d0: 0xd8, 0x1402c45a0: 0x51, 0x1421e0a82: 0x23}
    pins = {}
    for address, size in ranges.items():
        code = native(address, size)
        C.memmove(address, code, size)
        pins[hex(address)] = dict(bytes=size, sha256=hashlib.sha256(code).hexdigest())

    waiting = threading.Event()
    wakes = []

    @C.WINFUNCTYPE(C.c_int, C.c_void_p, C.c_void_p, C.c_size_t, C.c_uint32)
    def wait(address, value, size, timeout):
        waiting.set()
        return api.WaitOnAddress(address, value, size, timeout)

    @C.WINFUNCTYPE(None, C.c_void_p)
    def wake(address):
        wakes.append(address)
        api.WakeByAddressSingle(address)

    imports = {0x143a3f418: kernel.GetCurrentThreadId, 0x143a402d0: wait,
               0x143a402c8: wake, 0x143a402d8: api.WakeByAddressAll}
    for slot, target in imports.items():
        C.c_void_p.from_address(slot).value = C.cast(target, C.c_void_p).value

    # Owned shim supplies the normal shadow space for the native wake CALL.
    shim = 0x1421e0800
    jump = b'\x48\x83\xec\x28\xe9' + struct.pack('<i', 0x1421e0a82 - (shim + 9))
    C.memmove(shim, jump, len(jump))
    C.memmove(0x1421e0aa5, b'\x48\x83\xc4\x28\xc3', 5)
    # The owned primitive changes only the counter, from idle 0 to one reader.
    cas = bytes.fromhex('31 c0 ba 01 00 00 00 f0 0f b1 11 0f 94 c0 0f b6 c0 c3')
    C.memmove(shim + 0x20, cas, len(cas))
    for page in code_pages:
        old = C.c_ulong()
        need(kernel.VirtualProtect(page, 0x1000, 0x20, C.byref(old)), 'Cannot protect owned code')
        need(kernel.FlushInstructionCache(kernel.GetCurrentProcess(), page, 0x1000), 'Instruction flush failed')
    call = C.WINFUNCTYPE(None, C.c_void_p)
    original_reader, writer, unlock_writer, unlock_reader = map(call, (0x1422cc350, 0x1422cc3d0, 0x1402c45a0, shim))
    try_reader = C.WINFUNCTYPE(C.c_int, C.c_void_p)(shim + 0x20)
    lock = (C.c_uint32 * 2)()
    addr = C.addressof(lock)
    word = addr + 4
    cases = []

    original_reader(addr)
    need(list(lock) == [0, 1], 'Original idle reader did not yield [0,1]')
    unlock_reader(word)
    need(list(lock) == [0, 0], 'Original read release failed')
    need(try_reader(word) == 1 and list(lock) == [0, 1], 'Owned idle reader differs from original')
    unlock_reader(word)
    need(list(lock) == [0, 0] and not wakes, 'Idle release altered lock or signalled wake')
    cases.append('idle reader matches original and releases without wake')

    for state in (1, 0xfff, 0x1000, 0x1001, 0x400000, 0x401000, 0x800000, 0xffffffff):
        lock[0], lock[1] = kernel.GetCurrentThreadId() if state & 0xffc00000 else 0, state
        previous = list(lock)
        need(try_reader(word) == 0 and list(lock) == previous, f'Nonidle refusal modified state {state:#x}')
        cases.append(f'nonidle {state:#x} refuses without mutation')

    lock[0], lock[1] = 0, 0
    need(try_reader(word) == 1, 'Owned reader did not enter')
    original_reader(addr)
    need(lock[1] == 2, 'An original reader cannot coexist with the owned reader')
    unlock_reader(word)
    need(lock[1] == 1, 'Concurrent reader release changed the owned count')
    unlock_reader(word)
    need(list(lock) == [0, 0], 'Coexisting reader count leaked')
    cases.append('original reader joins and both counts release')

    acquired = threading.Event()
    allow_release = threading.Event()
    held = []

    def native_writer():
        writer(addr)
        held.extend(lock)
        acquired.set()
        allow_release.wait(5)
        unlock_writer(addr)

    need(try_reader(word) == 1, 'Owned reader did not enter writer-race control')
    thread = threading.Thread(target=native_writer, daemon=True)
    thread.start()
    need(waiting.wait(5) and lock[1] == 0x1001 and not acquired.is_set(), 'Original writer did not wait behind reader')
    need(try_reader(word) == 0 and lock[1] == 0x1001, 'Contender changed the queued writer state')
    unlock_reader(word)
    need(acquired.wait(5) and len(held) == 2 and held[0] and held[1] == 0x401000, 'Original writer did not resume on reader release')
    need(wakes == [word], 'Original reader release did not wake exactly one queued writer')
    need(try_reader(word) == 0 and list(lock) == held, 'Owned CAS changed an admitted writer')
    allow_release.set()
    thread.join(5)
    need(not thread.is_alive() and list(lock) == [0, 0], 'Original writer release did not clear the lock')
    cases.append('original writer queues behind the CAS reader, wakes, acquires and releases')
    return dict(exe_sha256=PIN, original_ranges=pins, cases=cases, owned_cas_sha256=hashlib.sha256(cas).hexdigest(),
                scope='Synthetic lock-word compatibility only. No retail lifetime, command, map copy or output verified.')


def main():
    if sys.argv[1:] == ['--owned']:
        print(json.dumps(owned()))
        return
    output = Path(sys.argv[1]).absolute()
    need(output.resolve().is_relative_to(ROOT/'.local-work/d5ar') and output.parent.is_dir() and not output.exists(),
         'Fresh ignored output required')
    need(not any(p.is_symlink() or p.is_junction() for p in (output, *output.parents)), 'Non-plain output path')
    before = disk_floor()
    method = Path(__file__).read_bytes()
    run = subprocess.run([sys.executable, '-E', '-B', str(Path(__file__).resolve()), '--owned'],
                         capture_output=True, timeout=20, creationflags=subprocess.CREATE_NO_WINDOW)
    value = json.loads(run.stdout) if run.returncode == 0 else dict(stderr=run.stderr.decode(errors='replace'))
    value.update(exit=run.returncode, method_sha256=hashlib.sha256(method).hexdigest(), free_before=before, free_after=disk_floor())
    need(Path(__file__).read_bytes() == method, 'Control method changed during execution')
    with output.open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(value, stream, indent=2)
        stream.write('\n')
    need(run.returncode == 0, 'Owned fixture failed. See receipt.')
    print(json.dumps(dict(status='PASS', cases=len(value['cases']))))


if __name__ == '__main__':
    main()
