# SPDX-License-Identifier: GPL-3.0-or-later
"""Execute finite BiomeMapDB entry-state controls in a disposable Python process.

Reads pinned installed EXE and owned PE reader; copies one original helper into
private executable memory and supplies six synthetic, uncontended entry states.
No running/pending-other-loader state is admitted, so external wait/recovery
calls are never reached. Writes fresh local receipts, frees the private page.
No game, save, database, configuration, deployment, network or Git operation.
Adapted from this repository's d5z_append_control.py (owned fixture method).
This tests state acquisition only, not file decoding or real concurrency.
The risk is an instruction/ABI fault in this disposable process; it cannot
modify the game process. Identity, disk-query, disk-floor or oracle failure
stops the run. Each result is flushed before checking; normal cleanup releases
the private page, and process exit releases it after an unhandled fault.
"""
import ctypes as C
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
EXE = Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield/Starfield.exe')
EXPECTED = '7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28'


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def sha(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        while block := stream.read(8 * 1024 * 1024):
            digest.update(block)
    return digest.hexdigest()


def main():
    require(os.name == 'nt' and C.sizeof(C.c_void_p) == 8, 'Windows x64 required')
    out = Path(sys.argv[1]).resolve()
    require(out.is_relative_to(ROOT / '.local-work') and not out.exists(),
            'Fresh local output required')
    kernel = C.WinDLL('kernel32', use_last_error=True)
    kernel.GetDiskFreeSpaceExW.argtypes = [C.c_wchar_p, C.POINTER(C.c_ulonglong),
                                         C.c_void_p, C.c_void_p]
    free = {}
    for drive in ('C:/', 'D:/'):
        value = C.c_ulonglong()
        require(kernel.GetDiskFreeSpaceExW(drive, C.byref(value), None, None),
                'Disk query failed')
        require(value.value >= 40_000_000_000, 'Free-space floor failed')
        free[drive] = value.value
    require(sha(EXE) == EXPECTED, 'EXE identity mismatch')
    method = ROOT / 'runtime/retained-population/build.py'
    spec = importlib.util.spec_from_file_location('owned_d5ad_pe', method)
    reader = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(reader)
    code = reader.pe_read(EXE.read_bytes(), 0x27d4be0, 0x116)
    require(len(code) == 0x116 and code[0xb3] == 0xc3,
            'Helper framing mismatch')
    kernel.VirtualAlloc.argtypes = [C.c_void_p, C.c_size_t, C.c_ulong, C.c_ulong]
    kernel.VirtualAlloc.restype = C.c_void_p
    kernel.VirtualProtect.argtypes = [C.c_void_p, C.c_size_t, C.c_ulong,
                                     C.POINTER(C.c_ulong)]
    kernel.VirtualFree.argtypes = [C.c_void_p, C.c_size_t, C.c_ulong]
    kernel.GetCurrentProcess.restype = C.c_void_p
    kernel.FlushInstructionCache.argtypes = [C.c_void_p, C.c_void_p, C.c_size_t]
    page = kernel.VirtualAlloc(None, 4096, 0x3000, 0x04)
    require(page, 'Private allocation failed')
    out.mkdir(parents=True)
    records = []
    try:
        C.memmove(page, code, len(code))
        old = C.c_ulong()
        require(kernel.VirtualProtect(page, 4096, 0x20, C.byref(old)),
                'Private RX protection failed')
        require(kernel.FlushInstructionCache(kernel.GetCurrentProcess(), page, len(code)),
                'Instruction-cache flush failed')
        acquire = C.WINFUNCTYPE(C.c_uint64, C.c_void_p, C.c_uint8)(page)
        # Independent state/return oracles from the documented state masks.
        # Only uncontended acquisition/ready classes are admitted to execution.
        cases = [(1, 0, 6, 0xa0000001), (1, 1, 1, 1),
                 (0x20000002, 0, 6, 0xa0000002),
                 (0x50000002, 0, 6, 0xa0000002),
                 (0x30000001, 0, 0, 0x30000001),
                 (0x40000002, 0, 0, 0x40000002)]
        with (out / 'cases.jsonl').open('x', encoding='utf8', newline='\n') as stream:
            for before, flag, expected, after in cases:
                entry = (C.c_uint32 * 10)()
                entry[5] = before
                result = acquire(C.addressof(entry), flag)
                record = dict(before=before, flag=flag, returned=result,
                              after=entry[5], expected_return=expected,
                              expected_after=after)
                stream.write(json.dumps(record) + '\n')
                stream.flush()
                os.fsync(stream.fileno())
                require(result == expected and entry[5] == after,
                        'Native state transition disagrees with oracle')
                require(all(entry[n] == 0 for n in range(10) if n != 5),
                        'Unexpected synthetic entry write')
                records.append(record)
    finally:
        require(kernel.VirtualFree(page, 0, 0x8000), 'Private cleanup failed')
    require(sha(EXE) == EXPECTED, 'EXE changed')
    receipt = dict(schema='sor-d5ad-readiness-control/1', passed=True,
                   game_process=False, executable_sha256=EXPECTED,
                   static_va='0x1427d4be0', code_bytes=len(code),
                   code_sha256=hashlib.sha256(code).hexdigest(),
                   script_sha256=sha(__file__), pe_reader_sha256=sha(method),
                   free=free, cases=records,
                   scope='Uncontended state acquisition and ready return only; '
                         'no stream decoder, waiting, competing loader or retail ordering.')
    (out / 'control.json').write_text(json.dumps(receipt, indent=2) + '\n',
                                      encoding='utf8', newline='\n')
    print(json.dumps(dict(passed=True, cases=len(records), receipt=str(out / 'control.json'))))


if __name__ == '__main__':
    main()
