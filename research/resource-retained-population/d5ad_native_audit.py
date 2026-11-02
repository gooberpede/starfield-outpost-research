# SPDX-License-Identifier: GPL-3.0-or-later
"""Pin and locate existing native evidence used by D5AD's load chronology.

Reads selected owned source-ledger rows and LOCAL-ONLY Ghidra exports. Writes
an exclusive ignored JSON receipt and sanitized locator CSV. Stdlib only; no
native execution, database edits, game/save/network/Git writes. Source lineage:
D5Z/D5AA/D5AC research under SOR-P-0002. Instruction checks corroborate cited
sites; they do not prove full control flow or actual historical execution.
"""
import csv
import importlib.util
import json
from pathlib import Path
import re
import sys
import struct

from d5ad_baseline import guard, sha

ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / 'docs/experiments/resource-retained-population'
REQUESTS = {
    '.local-work/d5z-reset/export01/native.tsv': ['141815620', '141827960', '140787830'],
    '.local-work/d5z-reset/export02/native.tsv': ['141881660', '1418278c0', '141825e00', '141827380', '141826ae0', '141826d90', '141824020'],
    '.local-work/d5aa/export01/native.tsv': ['141829ec0', '141a278a0', '1417df210', '14078c940'],
    '.local-work/d5z-visited/export02/native.tsv': ['14079d660', '14079ddf0'],
    '.local-work/d5ab/p1-export01/native.tsv': ['140982b70', '1409829b0'],
}
SITES = {
    '141881f3d': 'CMP qword ptr [0x145fd9c30],0x0',
    '141881f45': 'JNZ 0x141881f5d',
    '141881f51': 'CALL 0x140787830',
    '141815eda': 'CALL 0x14078f0b0',
    '1418162db': 'CALL 0x1418278c0',
    '141816347': 'CALL 0x141824020',
    '14181761b': 'CALL 0x141826ae0',
    '141817635': 'CALL 0x141818af0',
    '141817641': 'CALL 0x141826d90',
    '1418176de': 'CALL 0x141824020',
    '1418176f8': 'CALL 0x141826d90',
    '1418176fd': 'CALL 0x14182cab0',
    '141825f9e': 'CALL 0x141829ec0',
    '14182ab2d': 'CALL 0x14078af30',
    '14182acd8': 'CALL 0x14057fce0',
    '14182af17': 'CALL 0x14099f2c0',
}


def main():
    guard()
    out = Path(sys.argv[1]).resolve()
    if out.exists() or not out.is_relative_to(ROOT / '.local-work/d5ad'):
        raise ValueError('Fresh local output required')
    ledger_rows = []
    for name in ('d5z-sources.csv', 'd5aa-sources.csv'):
        ledger_rows.extend(csv.DictReader((DOC / name).read_text(encoding='utf-8').splitlines()))
    pinned = {r['path']: r['sha256'] for r in ledger_rows}
    pinned.update({
        '.local-work/d5z-visited/export02/native.tsv': '869f0968f70236f336f99fa938282d3737ba208758298e1dc78f006fbed169e7',
        '.local-work/d5ab/p1-export01/native.tsv': '27fe3e554236d1d03acddee2b26df26bcc0c976b1510fb60b54154fce29656a6',
    })
    rows, sites = [], {}
    for name, functions in REQUESTS.items():
        path = ROOT / name
        digest = sha(path)
        if digest != pinned[name]:
            raise ValueError('Native export pin mismatch: ' + name)
        text = path.read_text(encoding='utf-8')
        if not text.startswith('SHA256\t7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28\n'):
            raise ValueError('Wrong native image provenance')
        for match in re.finditer(r'^FUNCTION\t([^\t]+).*?^END_FUNCTION\s*$', text, re.M | re.S):
            if match[1] not in functions:
                continue
            row = dict(path=name, sha256=digest, static_va='0x' + match[1],
                       line_start=text.count('\n', 0, match.start()) + 1,
                       line_end=text.count('\n', 0, match.end()) + 1,
                       classification='LOCAL-ONLY')
            if not any(r['path'] == name and r['static_va'] == row['static_va'] for r in rows):
                rows.append(row)
            for site, expected in SITES.items():
                if re.search(r'^' + site + r'\t' + re.escape(expected) + '$', match[0], re.M):
                    sites[site] = dict(expected=expected, path=name, function=row['static_va'])
        found = {r['static_va'][2:] for r in rows if r['path'] == name}
        if set(functions) != found:
            raise ValueError('Missing cited function: ' + name)
    if set(sites) != set(SITES):
        raise ValueError('Missing instruction sites')
    exe = Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield/Starfield.exe')
    expected = '7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28'
    if sha(exe) != expected:
        raise ValueError('Installed native image mismatch')
    pe_path = ROOT / 'runtime/retained-population/build.py'
    spec = importlib.util.spec_from_file_location('owned_d5ad_pe', pe_path)
    pe = importlib.util.module_from_spec(spec); spec.loader.exec_module(pe)
    data = exe.read_bytes()
    base = 0x140000000
    pe_offset = struct.unpack_from('<I', data, 0x3c)[0]
    section_count = struct.unpack_from('<H', data, pe_offset + 6)[0]
    optional_size = struct.unpack_from('<H', data, pe_offset + 20)[0]
    section_table = pe_offset + 24 + optional_size
    singleton_rva = 0x5fd9c30
    zero_fill = None
    for index in range(section_count):
        offset = section_table + index * 40
        virtual_size, rva, raw_size = struct.unpack_from('<III', data, offset + 8)
        if rva <= singleton_rva and singleton_rva + 8 <= rva + virtual_size:
            if singleton_rva < rva + raw_size:
                raise ValueError('Singleton has unexpected file backing')
            zero_fill = dict(static_va=hex(base + singleton_rva), section_rva=hex(rva),
                             virtual_size=virtual_size, raw_size=raw_size,
                             scope='PE virtual zero-filled storage before initializers; not a runtime pointer snapshot')
    if zero_fill is None:
        raise ValueError('Singleton initial-storage domain not established')
    tables = []
    for table, name, load, link in (
            (0x144b6f0b0, '.?AVBGSResource@@', 0x1409e7900, 0x1409e8570),
            (0x144b6fd98, '.?AVBGSResourceGenerationData@@', 0x1409eed50, 0x1409efb20),
            (0x144b93b20, '.?AVTESObjectCELL@@', 0x140ae6830, 0x140ae7da0)):
        col = struct.unpack('<Q', pe.pe_read(data, table - base - 8, 8))[0]
        locator = pe.pe_read(data, col - base, 24)
        if struct.unpack_from('<I', locator, 4)[0] != 0:
            raise ValueError('Non-primary receiver table')
        descriptor = struct.unpack_from('<I', locator, 12)[0]
        actual_name = pe.pe_read(data, descriptor + 16, 180).split(b'\0')[0].decode('ascii')
        targets = {offset: struct.unpack('<Q', pe.pe_read(data, table - base + offset, 8))[0]
                   for offset in (0x88, 0xf8)}
        if actual_name != name or targets != {0x88: load, 0xf8: link}:
            raise ValueError('Typed definition dispatch mismatch')
        tables.append(dict(vtable=hex(table), col=hex(col), type_descriptor=hex(base + descriptor),
                           rtti=name, load=hex(load), postlink=hex(link)))
    if sha(exe) != expected:
        raise ValueError('Installed image changed during table audit')
    out.mkdir(parents=True)
    (out / 'native-audit.json').write_text(json.dumps(dict(rows=rows, sites=sites, definition_tables=tables,
        singleton_initial_storage=zero_fill,
        pe_reader_sha256=sha(pe_path), executable_sha256=expected,
        script_sha256=sha(__file__), scope='Pinned instruction locations; manual CFG and receiver review remains required'), indent=2) + '\n', encoding='utf-8', newline='\n')
    with (out / 'sources.csv').open('x', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)
    print(json.dumps(dict(functions=len(rows), instruction_sites=len(sites))))


if __name__ == '__main__':
    main()
