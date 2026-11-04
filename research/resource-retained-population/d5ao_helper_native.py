# SPDX-License-Identifier: GPL-3.0-or-later
"""Inspect exact owned helper instructions and imported wait calls offline.

Reads one task-local DLL and installed dumpbin; writes fresh local disassembly
and a hash-bound receipt. Uses Python stdlib and the owned PE export reader.
Executes only dumpbin. No target process, game, deployment, protected input,
database, dependency installation, Git operation or network access occurs.
Unwind ranges bound each exported helper; decoded import targets distinguish
actual direct calls from a whole-DLL Sleep import used by worker/fixture code.
Indirect private fixture callbacks are recorded but not labelled wait-free.
"""
import os
import sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '0') not in ('', '0'):
    raise RuntimeError('Python optimization is forbidden; invoke with -E -B')
import argparse
import json
from pathlib import Path
import re
import struct
import subprocess
from d5am_lock_qualify import ROOT, guard, sha
from d5an_pe import inspect

TOOL = Path('C:/Program Files/Microsoft Visual Studio/18/Community/VC/Tools/MSVC/14.51.36231/bin/Hostx64/x64/dumpbin.exe')


def require(value, message):
    if not value:
        raise RuntimeError(message)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('dll', type=Path)
    parser.add_argument('out', type=Path)
    parser.add_argument('--expect-sleep', action='store_true')
    args = parser.parse_args()
    dll, out = args.dll.resolve(), args.out.resolve()
    require(all(p.is_relative_to(ROOT / '.local-work/d5ao') for p in (dll, out)), 'Task-local paths required')
    require(not out.exists(), 'Fresh output required')
    initial = guard()
    raw = dll.read_bytes()
    nt = struct.unpack_from('<I', raw, 0x3c)[0]
    optional = nt + 24
    base = struct.unpack_from('<Q', raw, optional + 24)[0]
    count = struct.unpack_from('<H', raw, nt + 6)[0]
    table = optional + struct.unpack_from('<H', raw, nt + 20)[0]
    sections = [struct.unpack_from('<4I', raw, table + i * 40 + 8) for i in range(count)]

    def read(rva, size):
        for virtual_size, virtual, stored_size, stored in sections:
            if virtual <= rva and rva + size <= virtual + stored_size:
                offset = stored + rva - virtual
                require(offset + size <= len(raw), 'PE read outside file')
                return raw[offset:offset + size]
        raise RuntimeError('RVA outside backed sections')

    def string(rva):
        value = bytearray()
        while True:
            item = read(rva + len(value), 1)
            if item == b'\0':
                return value.decode('ascii')
            value += item

    imports = {}
    import_rva, import_size = struct.unpack_from('<2I', raw, optional + 112 + 8)
    for at in range(import_rva, import_rva + import_size, 20):
        original, timestamp, forwarder, name, first = struct.unpack('<5I', read(at, 20))
        if not any((original, timestamp, forwarder, name, first)):
            break
        index = 0
        while True:
            thunk = struct.unpack('<Q', read((original or first) + index * 8, 8))[0]
            if not thunk:
                break
            if not thunk & (1 << 63):
                imports[base + first + index * 8] = string(thunk + 2)
            index += 1
    exception_rva, exception_size = struct.unpack_from('<2I', raw, optional + 112 + 3 * 8)
    functions = [struct.unpack('<3I', read(at, 12)) for at in range(exception_rva, exception_rva + exception_size, 12)]
    pe = inspect(dll)
    ranges = {}
    for name in ('D5AN_counter_next', 'D5AN_counter_leave'):
        entry = pe['exports'][name]
        matches = [(begin, end) for begin, end, unwind in functions if begin == entry]
        require(len(matches) == 1, 'Unique exported helper unwind range required')
        ranges[name] = matches[0]
    out.mkdir()
    pins = {str(dll): sha(dll), str(TOOL): sha(TOOL), str(Path(__file__)): sha(__file__)}
    run = subprocess.run([str(TOOL), '/nologo', '/disasm', str(dll)], capture_output=True)
    (out / 'observer-disassembly.txt').write_bytes(run.stdout + run.stderr)
    require(run.returncode == 0, 'Pinned disassembler failed')
    lines = run.stdout.decode('utf8', errors='replace').splitlines()
    results = {}
    waits = {'Sleep', 'SleepEx', 'SwitchToThread', 'WaitOnAddress', 'WaitForSingleObject', 'WaitForMultipleObjects'}
    for name, (begin, end) in ranges.items():
        selected, imported = [], []
        for line in lines:
            address = re.match(r'\s*([0-9A-Fa-f]{16}):', line)
            if address and base + begin <= int(address[1], 16) < base + end:
                selected.append(line.strip())
                target = re.search(r'call\s+qword ptr \[([0-9A-Fa-f]+)h\]', line)
                if target:
                    imported.append(imports.get(int(target[1], 16), 'UNKNOWN_IMPORT'))
        require(selected and sum('lock cmpxchg' in line for line in selected) == 1, 'Actual helper CAS instruction required')
        direct_waits = [item for item in imported if item in waits]
        require(direct_waits == (['Sleep'] if args.expect_sleep else []), 'Unexpected direct helper wait imports')
        require('GetLastError' in imported and 'SetLastError' in imported, 'LastError preservation calls required')
        results[name] = dict(rva=hex(begin), end_rva=hex(end), direct_import_calls=imported, direct_wait_calls=direct_waits,
                             instructions=selected, scope='Direct imported calls only; fixture-indirect calls remain explicit source-controlled seams')
    require(all(sha(path) == digest for path, digest in pins.items()), 'Inputs changed during inspection')
    receipt = dict(schema='sor-d5ao-helper-native/1', status='PASS', inputs=pins, helpers=results,
                   expected_sleep=args.expect_sleep, disassembly_sha256=sha(out / 'observer-disassembly.txt'),
                   free_before=initial, free_after=guard())
    (out / 'qualification.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf8', newline='\n')
    print(json.dumps(dict(status='PASS', helpers=len(results), expected_sleep=args.expect_sleep)))


if __name__ == '__main__':
    main()
