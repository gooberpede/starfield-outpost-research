# SPDX-License-Identifier: GPL-3.0-or-later
"""Execute original lock, destruction, lookup and dispatch controls in an owned host.

Reads only the pinned game EXE and project source. Writes exclusive ignored JSON
receipts; maps authenticated instructions only in this disposable Python host.
The two external calls are resolved to installed Windows GetCurrentThreadId and
WaitOnAddress. Controlled fixture threads release owned lock words. No retail
process, save, installed plugin, analysis project or configuration is changed.
The parent gives this finite fixture host a 20-second failure timeout; this is
not a limit on a live scientific capture. No third-party source is incorporated.
"""
import os
import sys
if sys.flags.optimize or not __debug__ or os.environ.get('PYTHONOPTIMIZE', '0') not in ('', '0'):
    raise RuntimeError('Optimization forbidden; invoke pinned Python -E -B')

import ctypes as C
import hashlib
import json
from pathlib import Path
import struct
import subprocess
import threading
import time
from d5ar_native_inventory import ROOT, EXE, PIN, disk_floor


def owned_host(destination):
    before = disk_floor()
    data = EXE.read_bytes()
    if hashlib.sha256(data).hexdigest() != PIN:
        raise ValueError('Installed PE identity mismatch')
    pe = struct.unpack_from('<I', data, 0x3c)[0]
    count = struct.unpack_from('<H', data, pe + 6)[0]
    optional = struct.unpack_from('<H', data, pe + 20)[0]
    sections = [struct.unpack_from('<IIII', data, pe + 24 + optional + 40 * n + 8) for n in range(count)]

    def original(address, length):
        rva = address - 0x140000000
        for _, section_rva, size, raw in sections:
            if section_rva <= rva and rva + length <= section_rva + size:
                return data[raw + rva - section_rva:raw + rva - section_rva + length]
        raise ValueError('File-backed range missing')

    k = C.WinDLL('kernel32', use_last_error=True)
    k.VirtualAlloc.argtypes = [C.c_void_p, C.c_size_t, C.c_ulong, C.c_ulong]
    k.VirtualAlloc.restype = C.c_void_p
    k.VirtualProtect.argtypes = [C.c_void_p, C.c_size_t, C.c_ulong, C.POINTER(C.c_ulong)]
    k.GetCurrentProcess.restype = C.c_void_p
    k.FlushInstructionCache.argtypes = [C.c_void_p, C.c_void_p, C.c_size_t]
    synchronization = C.WinDLL('kernelbase', use_last_error=True)
    synchronization.WakeByAddressSingle.argtypes = [C.c_void_p]
    reservations = []
    for base, size in ((0x1422c0000, 0x10000), (0x143a30000, 0x20000)):
        if k.VirtualAlloc(base, size, 0x3000, 4) != base:
            raise OSError(C.get_last_error(), 'Owned original-address reservation failed')
        reservations.append((base, size))
    code = original(0x1422cc350, 0x7e)
    C.memmove(0x1422cc350, code, len(code))
    C.c_void_p.from_address(0x143a3f418).value = C.cast(k.GetCurrentThreadId, C.c_void_p).value
    C.c_void_p.from_address(0x143a402d0).value = C.cast(synchronization.WaitOnAddress, C.c_void_p).value
    previous = C.c_ulong()
    if not k.VirtualProtect(0x1422cc000, 0x1000, 0x20, C.byref(previous)):
        raise OSError(C.get_last_error(), 'Owned executable protection failed')
    if not k.FlushInstructionCache(k.GetCurrentProcess(), 0x1422cc350, len(code)):
        raise OSError(C.get_last_error(), 'Instruction cache flush failed')
    acquire = C.WINFUNCTYPE(None, C.c_void_p)(0x1422cc350)
    rows = []
    word = (C.c_uint32 * 2)()
    acquire(C.addressof(word))
    if list(word) != [0, 1]:
        raise ValueError('Uncontended reader result')
    rows.append(dict(case='uncontended-reader', actual=list(word), passed=True))
    word[0], word[1] = k.GetCurrentThreadId(), 0x00400000
    acquire(C.addressof(word))
    if word[1] != 0x00400001:
        raise ValueError('Recursive exclusive result')
    rows.append(dict(case='same-thread-exclusive-admits-reader', actual=list(word), passed=True,
                     consequence='Reader admission is insufficient for coherent COMPLETE status'))
    word[0], word[1] = 0, 0x00400000
    released = threading.Event()

    def release_fixture_writer():
        time.sleep(0.05)
        word[1] = 1
        released.set()
        synchronization.WakeByAddressSingle(C.addressof(word) + 4)

    worker = threading.Thread(target=release_fixture_writer)
    worker.start()
    acquire(C.addressof(word))
    returned_before_release = not released.is_set()
    worker.join()
    if returned_before_release or not released.is_set() or word[1] != 1:
        raise ValueError('Concurrent foreign writer control')
    rows.append(dict(case='foreign-exclusive-reader-waits', actual=list(word), passed=True,
                     fixture='Owned writer releases after fixed setup interval; no engine mutator executed'))
    # The complete original destructor and original map clear run unchanged.
    # Unrelated empty cache destruction and heap release are bounded stand-ins.
    for base in (0x140790000, 0x1407a0000, 0x1402b0000):
        if k.VirtualAlloc(base, 0x10000, 0x3000, 4) != base:
            raise OSError(C.get_last_error(), 'Owned destructor reservation failed')
        reservations.append((base, 0x10000))
    destructor = original(0x14079d910, 0x16e)
    map_clear = original(0x1407aa8a0, 0x8d)
    C.memmove(0x14079d910, destructor, len(destructor))
    C.memmove(0x1407aa8a0, map_clear, len(map_clear))
    frees = []

    @C.WINFUNCTYPE(None, C.c_void_p)
    def release_backing(pointer):
        frees.append(int(pointer or 0))

    for address in (0x1407aa3c0, 0x1407a9bb0):
        C.memmove(address, b'\xc3', 1)
    jump = b'\x48\xb8' + struct.pack('<Q', C.cast(release_backing, C.c_void_p).value) + b'\xff\xe0'
    C.memmove(0x1402b7910, jump, len(jump))
    for base in (0x140790000, 0x1407a0000, 0x1402b0000):
        if not k.VirtualProtect(base, 0x10000, 0x20, C.byref(previous)):
            raise OSError(C.get_last_error(), 'Owned destructor protection failed')
        if not k.FlushInstructionCache(k.GetCurrentProcess(), base, 0x10000):
            raise OSError(C.get_last_error(), 'Destructor instruction flush failed')
    owner = C.create_string_buffer(0x160)
    slot = C.create_string_buffer(0x18)
    holder = C.create_string_buffer(0x40)
    C.c_uint32.from_buffer(holder).value = 2
    C.c_uint64.from_buffer(slot, 0x00).value = 0x12345678
    C.c_uint64.from_buffer(slot, 0x08).value = C.addressof(holder)
    C.c_uint64.from_buffer(slot, 0x10).value = 0
    C.c_uint64.from_buffer(owner, 0x20).value = C.addressof(slot)
    C.c_uint64.from_buffer(owner, 0x28).value = 1
    C.c_uint32.from_buffer(owner, 0x44).value = 1
    C.WINFUNCTYPE(None, C.c_void_p)(0x14079d910)(C.addressof(owner))
    result = dict(reader_word=C.c_uint32.from_buffer(owner, 0x44).value,
                  map_pointer=C.c_uint64.from_buffer(owner, 0x20).value,
                  map_capacity=C.c_uint64.from_buffer(owner, 0x28).value,
                  slot_holder=C.c_uint64.from_buffer(slot, 0x08).value,
                  holder_references=C.c_uint32.from_buffer(holder).value,
                  backing_release_recorded=frees == [C.addressof(slot)])
    if result != dict(reader_word=1, map_pointer=0, map_capacity=0, slot_holder=0,
                      holder_references=1, backing_release_recorded=True):
        raise ValueError(f'Destructor counterexample differs: {result}')
    rows.append(dict(case='destructor-ignores-active-reader', actual=result, passed=True,
                     consequence='ProcGen reader alone does not fence destruction',
                     bounds='Unrelated cache clears replaced with RET; backing free records only; actual destructor and holder-map clear unchanged'))
    for base, size in ((0x140c10000, 0x10000), (0x145eb0000, 0x30000)):
        if k.VirtualAlloc(base, size, 0x3000, 4) != base:
            raise OSError(C.get_last_error(), 'Owned command-table reservation failed')
        reservations.append((base, size))
    lookup_code = original(0x140c16380, 0x41)
    dispatcher_code = original(0x140c12b80, 0x264)
    C.memmove(0x140c16380, lookup_code, len(lookup_code))
    C.memmove(0x140c12b80, dispatcher_code, len(dispatcher_code))
    if not k.VirtualProtect(0x140c10000, 0x10000, 0x20, C.byref(previous)):
        raise OSError(C.get_last_error(), 'Owned command code protection failed')
    if not k.FlushInstructionCache(k.GetCurrentProcess(), 0x140c10000, 0x10000):
        raise OSError(C.get_last_error(), 'Command instruction flush failed')
    command_name = C.create_string_buffer(b'SORSnapshot')
    row_address = 0x145eb1050 + 0x49 * 0x58
    C.c_uint64.from_address(row_address).value = C.addressof(command_name)
    C.c_uint32.from_address(row_address + 0x10).value = 0x149
    calls = []

    @C.WINFUNCTYPE(C.c_bool, C.c_void_p, C.c_void_p, C.c_void_p, C.c_void_p,
                  C.c_void_p, C.c_void_p, C.POINTER(C.c_float), C.POINTER(C.c_uint32))
    def command_handler(parameters, bytecode, reference, container, script, locals_pointer, output, offset):
        calls.append(dict(bytecode=int(bytecode or 0), reference=int(reference or 0),
                          locals_pointer=int(locals_pointer or 0), offset=offset[0]))
        output[0] = 7.0
        return True

    C.c_void_p.from_address(row_address + 0x30).value = C.cast(command_handler, C.c_void_p).value
    lookup = C.WINFUNCTYPE(C.c_void_p, C.c_uint32)(0x140c16380)
    if lookup(0x149) != row_address or lookup(0x349) is not None:
        raise ValueError('Original opcode lookup bounds')
    expression = C.create_string_buffer(b'\x58\x49\x01\x00\x00')
    position = C.c_uint32()
    scalar = C.c_float()
    locals_object = C.create_string_buffer(0x40)
    dispatch = C.WINFUNCTYPE(C.c_bool, C.c_void_p, C.c_void_p, C.c_void_p,
                             C.c_void_p, C.c_void_p, C.c_void_p, C.c_void_p)(0x140c12b80)
    ok = dispatch(C.byref(scalar), C.addressof(expression), C.byref(position), None, None, None, C.addressof(locals_object))
    if not ok or scalar.value != 7.0 or position.value != 5 or len(calls) != 1:
        raise ValueError('Original expression dispatch result')
    if calls[0] != dict(bytecode=C.addressof(expression), reference=0,
                       locals_pointer=C.addressof(locals_object), offset=5):
        raise ValueError('Native handler operand mismatch')
    rows.append(dict(case='original-opcode-lookup-and-expression-dispatch', passed=True,
                     opcode='0x149', callback_count=len(calls), scalar=scalar.value, final_offset=position.value,
                     bounds='Owned table row and compiled expression; not full console parser, registration lifecycle or retail callback affinity'))
    receipt = dict(schema='sor-d5ar/native-shared-controls/1', rows=rows,
                   exe_sha256=PIN, helper_static_va='0x1422cc350', helper_sha256=hashlib.sha256(code).hexdigest(),
                   destructor_sha256=hashlib.sha256(destructor).hexdigest(), map_clear_sha256=hashlib.sha256(map_clear).hexdigest(),
                   lookup_sha256=hashlib.sha256(lookup_code).hexdigest(), expression_dispatch_sha256=hashlib.sha256(dispatcher_code).hexdigest(),
                   source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                   free_before=before, free_after=disk_floor(),
                   scope='Original lock/destructor/lookup/expression-dispatch owned controls with explicit stand-ins; no retail callback, destructor lease or snapshot qualification')
    with destination.open('x', encoding='utf8', newline='\n') as stream:
        json.dump(receipt, stream, indent=2)
        stream.write('\n')


def main():
    destination = Path(sys.argv[-1]).resolve()
    if not destination.is_relative_to(ROOT / '.local-work') or destination.exists():
        raise ValueError('Fresh ignored output required')
    if any(p.is_symlink() or p.is_junction() for p in (destination, *destination.parents)):
        raise ValueError('Reparse output refused')
    if len(sys.argv) == 3 and sys.argv[1] == '--owned-host':
        owned_host(destination)
        return
    disk_floor()
    destination.parent.mkdir(parents=True, exist_ok=True)
    completed = subprocess.run([sys.executable, '-E', '-B', str(Path(__file__).resolve()), '--owned-host', str(destination)],
                               cwd=ROOT, timeout=20, capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
    if completed.returncode:
        with destination.with_suffix('.failure.json').open('x', encoding='utf8', newline='\n') as failure:
            json.dump(dict(schema='sor-d5ar/native-host-failure/1', exit=completed.returncode,
                           stdout=completed.stdout.decode('utf8', errors='replace'),
                           stderr=completed.stderr.decode('utf8', errors='replace'),
                           source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()), failure, indent=2)
            failure.write('\n')
        raise RuntimeError(f'Owned host failed {completed.returncode}: {completed.stderr.decode("utf8", errors="replace")}')
    if not destination.is_file():
        raise RuntimeError('Owned host produced no receipt')
    print(destination)


if __name__ == '__main__':
    main()
