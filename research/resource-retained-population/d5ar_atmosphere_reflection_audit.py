# SPDX-License-Identifier: GPL-3.0-or-later
"""Reconstruct one pinned child ATMO field path from original reader evidence.

Reads exact file-audit operands, selected native exports, original PE vtables
and the owned zero-list control. Writes one fresh ignored receipt. This is a
bounded read-only evidence method, not a generic reflection or save importer.
No third-party exporter implementation/heuristic is used.
"""
import os
import sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):
    raise RuntimeError('Use pinned Python -E -B')
import hashlib
import json
from pathlib import Path
import struct
from d5ad_baseline import ROOT, guard, sha
from d5ar_native_inventory import EXE, PIN


def need(condition, message):
    if not condition:
        raise ValueError(message)


def read_tables():
    data = EXE.read_bytes()
    need(hashlib.sha256(data).hexdigest() == PIN, 'Installed executable changed')
    pe = struct.unpack_from('<I', data, 0x3c)[0]
    optional = struct.unpack_from('<H', data, pe + 20)[0]
    sections = [struct.unpack_from('<IIII', data, pe + 24 + optional + 40*i + 8)
                for i in range(struct.unpack_from('<H', data, pe + 6)[0])]
    def file_bytes(va, count):
        rva = va - 0x140000000
        for _, start, length, offset in sections:
            if start <= rva and rva + count <= start + length:
                at = offset + rva - start
                return data[at:at + count]
        raise ValueError('Expected original operand is not file-backed')
    expected = {0x144b6d6f0: 0x140852f20, 0x144b6d738: 0x1405df980,
                0x144b6d740: 0x1405dfa40, 0x144b6d760: 0x140853520,
                0x144b6d9a0: 0x1409dcf70, 0x144d9afb8: 0x1427be8e0,
                0x145975240: 0x144b5ad88, 0x144b5add8: 0x1408e2df0}
    need(all(struct.unpack('<Q', file_bytes(a, 8))[0] == b for a, b in expected.items()), 'Original dispatch slot changed')
    names = {0x144b55fc8: 'BGSAtmosphere', 0x144b55f60: 'Settings',
             0x144b567c0: 'BGSAtmosphere::AtmosphereSettings', 0x144b5676c: 'Misc',
             0x144b56978: 'BGSAtmosphere::MiscSettings', 0x144b569a8: 'InorganicResources'}
    need(all(file_bytes(a, len(name) + 1) == name.encode('ascii') + b'\0' for a, name in names.items()),
         'Original reflected metadata name changed')
    return {hex(a): hex(b) for a, b in expected.items()}, {hex(a): name for a, name in names.items()}


def examine_child(raw, parent):
    need(struct.unpack_from('<4sIII', raw) == (b'BETH', 8, 4, 15), 'Child reflected header changed')
    chunks = []
    cursor = 16
    while cursor < len(raw):
        need(cursor + 8 <= len(raw), 'Short reflected chunk header')
        tag, size = struct.unpack_from('<4sI', raw, cursor)
        end = cursor + 8 + size
        need(end <= len(raw), 'Short reflected chunk')
        chunks.append((tag, cursor, raw[cursor + 8:end]))
        cursor = end
    need([x[0] for x in chunks] == [b'STRT', b'TYPE'] + [b'CLAS']*10 + [b'DIFF', b'LIST'],
         'Child reflected chunk sequence changed')
    strings = chunks[0][2]
    need(chunks[1][2] == struct.pack('<I', 10), 'Child type count changed')
    def string(offset):
        need(offset < len(strings) and (not offset or strings[offset-1] == 0), 'Invalid reflected name offset')
        end = strings.index(0, offset)
        return strings[offset:end].decode('ascii')
    classes = {}
    for _, _, data in chunks[2:12]:
        class_id, base_id, flags, count = struct.unpack_from('<IIHH', data)
        need(len(data) == 12 + 12*count and class_id not in classes, 'Invalid bounded CLAS framing')
        fields = [(string(name), kind, offset, size) for name, kind, offset, size
                  in struct.iter_unpack('<IIHH', data[12:])]
        classes[class_id] = dict(name=string(class_id), flags=flags, base_id=base_id, fields=fields)
    diff = chunks[12][2]
    cursor = 0
    def take(kind):
        nonlocal cursor
        result = struct.unpack_from(kind, diff, cursor)[0]
        cursor += struct.calcsize(kind)
        return result
    path = []
    def select(class_id, class_name, field_name):
        row = classes[class_id]
        need(row['name'] == class_name and row['flags'] == 0, 'Unsupported reflected class path')
        index = take('<H')
        name, kind, offset, size = row['fields'][index]
        need(name == field_name, 'Original selected field changed')
        path.append(dict(class_name=class_name, field_index=index, field=name, wire_kind=hex(kind),
                         serialized_byte_offset=offset, serialized_byte_size=size))
        return kind
    root = take('<I')
    settings = select(root, 'BGSAtmosphere', 'Settings')
    settings_name = 'BGSAtmosphere::AtmosphereSettings'
    misc_name = 'BGSAtmosphere::MiscSettings'
    need(select(settings, settings_name, 'pParent') == 0xffffff05, 'Parent field kind changed')
    need(take('<I') == 0xffffff0d and take('<I') == parent, 'Child parent reference changed')
    misc = select(settings, settings_name, 'Misc')
    need(select(misc, misc_name, 'AtmosphereType') == 0xffffff02, 'Atmosphere enum kind changed')
    count = take('<H')
    need(diff[cursor:cursor + count] == b'AT_TYPE_CARBON_DIOXIDE\0', 'Child enum operand changed')
    cursor += count
    need(select(misc, misc_name, 'InorganicResources') == 0xffffff03, 'Resource array kind changed')
    need([take('<H') for _ in range(3)] == [0xffff]*3 and cursor == len(diff), 'Unclosed child DIFF path')
    kind, list_count = struct.unpack('<II', chunks[13][2])
    need((kind, list_count) == (0xffffff01, 0), 'Child requested array count changed')
    return dict(path=path, diff_offset=chunks[12][1], diff_bytes=len(diff), list_offset=chunks[13][1],
                requested_list_count=list_count, list_element_kind=hex(kind), native_parent_candidate=hex(parent))


def main():
    out = Path(sys.argv[1]).resolve()
    before = guard()
    need(out.is_relative_to(ROOT / '.local-work/d5ar') and not out.exists() and
         not any(p.is_symlink() or p.is_junction() for p in (out, *out.parents)), 'Fresh ignored output required')
    local = ROOT / '.local-work/d5ar'
    inputs = {}
    audit = local / 'atmosphere-definition01.json'
    need(sha(audit) == 'c882b36c68c3cdbc0c475e5d77c5e5e28f2d5b2366bfb3bf13d2e2b2bff76330', 'File audit changed')
    inputs[str(audit.relative_to(ROOT))] = sha(audit)
    rows = json.loads(audit.read_bytes())['records']
    need([r['header']['formid'] for r in rows] == [0xc19b, 0xec29f, 0x20cdd4], 'ATMO chain changed')
    fields = {r['tag']: bytes.fromhex(r['raw_hex']) for r in rows[0]['fields']}
    child = examine_child(fields['RDIF'], struct.unpack('<I', fields['RFDP'])[0])
    checks = {
        'reflected-class-resolver01': ('1427d38de\tMOV dword ptr [RSI + 0x18],EAX',
            '1427d38fe\tCALL 0x1427ba230', '1427d393b\tLEA R14,[RBX + 0xc]',
            '1427d3b20\tMOVZX EDX,byte ptr [RAX]', '1427d3b58\tADD R14,0xc'),
        'reflected-field-dispatch01': ('1427c3aa5\tMOVZX EDI,word ptr [RAX]', '1427c3af8\tCALL 0x1427c5a40'),
        'reflected-value-dispatch01': ('1427c3c8e\tCMP R8D,0xffffff03', '1427c3d20\tJMP 0x1427c2f90',
            '1427c5a7d\tMOV R10D,dword ptr [RAX + 0x10]'),
        'reflected-list-scalar01': ('1427c3042\tMOV R15D,dword ptr [RBP + 0x54]',
            '1427c3062\tCALL qword ptr [RAX + 0x50]'),
        'reflected-pending-diff01': ('1408536a5\tCALL 0x1405e10b0', '140853774\tCALL 0x1427bcaf0',
            '1408537e5\tCALL 0x1427bd510', '140853845\tCALL RDI', '140853b6f\tCALL qword ptr [RAX + 0x338]'),
        'reflected-schema-reader01': ('1427bdc61\tLEA RAX,[0x144d9afb8]', '1427be0f4\tCALL 0x1427bce70'),
        'reflected-diff-reader-factory01': ('1427bd58a\tCALL 0x1427bdbd0',),
        'reflected-enum-reader01': ('1427c5c9d\tMOVZX ECX,word ptr [RAX]', '1427c5ee1\tSUB ECX,EBP'),
        'atmosphere-list-type01': ('1408e2e0d\tMOV dword ptr [RCX],0x0',),
        'atmosphere-root-type01': ('1408bb7d3\tLEA RDX,[0x144b55f60]', '1408bb7eb\tMOV dword ptr [RSP + 0x70],0x38'),
        'atmosphere-settings-type01': ('1408bfaee\tLEA RDX,[0x144b5676c]', '1408bfb06\tMOV dword ptr [RSP + 0x60],0x90'),
        'atmosphere-property-type01': ('1408bdaa5\tMOV R9D,0x8', '1408bdb5f\tCALL 0x1427c8420',
            '1408bdb64\tLEA RDX,[0x144b569a8]', '1408bdb73\tLEA RCX,[0x145975240]',
            '1408bdb82\tMOV dword ptr [RSP + 0x108],R9D'),
        'atmosphere-resource-fixup01': ('1409dd3fa\tMOV EAX,dword ptr [RBX + 0xd0]', '1409dd408\tMOV RBX,qword ptr [RBX + 0xd8]'),
        'save-unit6-typed-bodies01': ('1427c8420\tMOV R8,RCX', '1427c8485\tRET'),
    }
    for name, anchors in checks.items():
        path = local / name / 'native.tsv'
        lines = path.read_text(encoding='utf8').splitlines()
        need(lines[0] == 'SHA256\t' + PIN and lines[-1] == 'END' and all(a in lines for a in anchors),
             'Original reader anchor changed: ' + name)
        if name == 'save-unit6-typed-bodies01':
            begin = next(i for i, line in enumerate(lines) if line.startswith('FUNCTION\t1427c8420\t'))
            end = next(i for i in range(begin + 1, len(lines)) if lines[i].startswith('XREF\t'))
            need(not any('R9' in line or '\tCALL ' in line or '\tJMP ' in line for line in lines[begin+1:end]),
                 'Original property metadata mover no longer preserves R9')
        inputs[str(path.relative_to(ROOT))] = sha(path)
    control = local / 'atmosphere-list-native02.json'
    evidence = json.loads(control.read_bytes())
    need(evidence['status'] == 'PASS_ORIGINAL_ZERO_LIST_ARRAY_CONTRACT' and len(evidence['rows']) == 3 and
         evidence['source_sha256'] == sha(Path(__file__).with_name('d5ar_atmosphere_list_controls.py')),
         'Original zero-list control changed')
    inputs[str(control.relative_to(ROOT))] = sha(control)
    slots, names = read_tables()
    result = dict(status='PASS_SCOPED_C19B_DEFINITION_ROUTE_CLEAR', child=child, original_vtable_slots=slots,
                  native_reflected_names=names,
                  inputs=inputs, method_sha256=sha(__file__), floors_before=before, floors_after=guard(),
                  scope='Normal pinned C19B definition parent/copy then native DIFF/LIST clear; no output geometry inference.',
                  limits=['Does not observe A0 runtime AtmosphereModifier or PerBiomeData',
                          'Assumes healthy initialized native type registry and resolved main-file definition route',
                          'No generic reflection grammar or whole-save/persistence closure'])
    with out.open('x', encoding='utf8', newline='\n') as stream:
        stream.write(json.dumps(result, indent=2) + '\n')
    print(json.dumps(dict(status=result['status'], selected_fields=len(child['path']), list_count=child['requested_list_count'])))


if __name__ == '__main__':
    main()
