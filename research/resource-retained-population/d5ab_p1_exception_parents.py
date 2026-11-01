# SPDX-License-Identifier: GPL-3.0-or-later
"""Original diagnostic: invert ten named FH4 unwind actions in pinned PE metadata.

Reads the installed executable and this method's source. Consulted the installed
Microsoft ehdata4_export.h for metadata-format facts; no Microsoft implementation
is imported, copied, or executed. This is an independent stdlib interpretation.
Adapted from the owned local P1 specialist diagnostic, SHA-256
6919baf53e2b5d8fea062b2f73281fb8c90bb1a9dee854c455fa011e185ecb31.
Writes one fresh local-only JSON receipt; does not map/execute target instructions,
open saves, edit an analysis database, or contact a network service.
"""
from pathlib import Path
import ctypes
import hashlib
import json
import struct
import sys

exe = Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield/Starfield.exe')
header = Path('C:/Program Files/Microsoft Visual Studio/18/Community/VC/Tools/MSVC/14.51.36231/include/ehdata4_export.h')
ROOT = Path(__file__).resolve().parents[2]
output = (ROOT / sys.argv[1]).resolve()
assert output.is_relative_to(ROOT / '.local-work/d5ab')
assert not output.exists()
output.parent.mkdir(parents=True, exist_ok=True)
for drive in ('C:/', 'D:/'):
    free = ctypes.c_ulonglong()
    assert ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(drive), ctypes.byref(free), None, None)
    assert free.value > 40_000_000_000
data = exe.read_bytes()
sha = hashlib.sha256(data).hexdigest()
assert sha == '7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28'
pe = struct.unpack_from('<I', data, 0x3c)[0]
optional = pe + 24
section_count = struct.unpack_from('<H', data, pe + 6)[0]
optional_size = struct.unpack_from('<H', data, pe + 20)[0]
sections = []
named_sections = []
for index in range(section_count):
    at = optional + optional_size + index * 40
    virtual_size, address, raw_size, raw = struct.unpack_from('<IIII', data, at + 8)
    sections.append((address, raw_size, raw))
    named_sections.append((data[at:at + 8].split(b'\0')[0].decode(), address, raw_size, raw))

def offset(rva):
    for address, size, raw in sections:
        if address <= rva < address + size:
            return raw + rva - address
    raise ValueError(f'unbacked RVA {rva:#x}')

def word(rva):
    return struct.unpack_from('<I', data, offset(rva))[0]

def compressed(rva):
    first = data[offset(rva)]
    prefix = 0
    while prefix < 4 and first & (1 << prefix):
        prefix += 1
    if prefix == 4:
        return word(rva + 1), rva + 5
    size = prefix + 1
    encoded = int.from_bytes(data[offset(rva):offset(rva) + size], 'little')
    return encoded >> size, rva + size

targets = (0x37bc3c0, 0x37bd170, 0x3810a30, 0x3810a50, 0x3810a90,
           0x3810af0, 0x3812b90, 0x3812da0, 0x385f220, 0x385f250)
directory, directory_size = struct.unpack_from('<II', data, optional + 112 + 24)
assert directory_size % 12 == 0
matches = []
errors = []
eligible = 0
for at in range(directory, directory + directory_size, 12):
    begin, end, unwind = struct.unpack_from('<III', data, offset(at))
    if not unwind:
        continue
    try:
        flags = data[offset(unwind)] >> 3
        if not flags & 3 or flags & 4:
            continue
        code_count = data[offset(unwind) + 2]
        handler_at = unwind + ((4 + 2 * code_count + 3) & ~3)
        if word(handler_at) != 0x3663130:
            continue
        eligible += 1
        info = word(handler_at + 4)
        cursor = info
        bits = data[offset(cursor)]
        cursor += 1
        if bits & 4:
            _, cursor = compressed(cursor)
        if not bits & 8:
            continue
        unwind_map = word(cursor)
        count, cursor = compressed(unwind_map)
        if count > 10000:
            raise ValueError('unwind entry bound')
        for state in range(count):
            entry = cursor
            encoded, cursor = compressed(cursor)
            kind = encoded & 3
            action = None
            obj = None
            if kind:
                action = word(cursor)
                cursor += 4
            if kind in (1, 2):
                obj, cursor = compressed(cursor)
            if action in targets:
                matches.append(dict(parent_begin=hex(begin), parent_end=hex(end),
                    pdata=hex(at), unwind=hex(unwind), funcinfo=hex(info),
                    unwind_map=hex(unwind_map), state=state, entry=hex(entry),
                    type=kind, object=obj, action=hex(action), action_field=hex(compressed(entry)[1]),
                    funcinfo_bytes=data[offset(info):offset(info) + 9].hex(),
                    entry_bytes=data[offset(entry):offset(cursor)].hex()))
    except Exception as exc:
        errors.append(dict(begin=hex(begin), error=str(exc)))
raw_references = []
for name, address, raw_size, raw in named_sections:
    if name != '.rdata':
        continue
    region = data[raw:raw + raw_size]
    for target in targets:
        needle = target.to_bytes(4, 'little')
        position = region.find(needle)
        while position >= 0:
            raw_references.append(dict(action=hex(target), address=hex(address + position)))
            position = region.find(needle, position + 1)
recognized = {(row['action'], row['action_field']) for row in matches}
unmapped_raw_references = [row for row in raw_references if (row['action'], row['address']) not in recognized]
receipt = dict(executable_path=str(exe), executable_sha256=sha,
    method_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    consulted_format_path=str(header),
    consulted_format_sha256=hashlib.sha256(header.read_bytes()).hexdigest(),
    metadata_scope='PE exception directory; FH4 handler RVA 0x3663130; ten explicit L17 action targets',
    exception_directory=[hex(directory), directory_size], targets=[hex(t) for t in targets],
    fh4_entries=eligible, matches=matches, errors=errors,
    raw_reference_scope='.rdata only; exact ten little-endian RVA literals',
    raw_references=raw_references, unmapped_raw_references=unmapped_raw_references)
with output.open('x', encoding='utf8', newline='\n') as stream:
    stream.write(json.dumps(receipt, indent=2) + '\n')
assert not errors
assert not unmapped_raw_references
assert len(matches) == 12
assert set(int(row['action'], 16) for row in matches) == set(targets)
print(output, len(matches), hashlib.sha256(output.read_bytes()).hexdigest())
