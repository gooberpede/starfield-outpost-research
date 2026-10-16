# SPDX-License-Identifier: GPL-3.0-or-later
"""Verify existing owned E1 SWF derivatives against current installed archive.
Reads pinned Interface.ba2, E1 SWF/ABC and owned local instruction decoder;
writes exclusive ignored E2 receipt only. CPython/stdlib. No Flash execution,
external dependency, game/save/analysis effects. Local helper dependency is
explicitly pinned in the receipt; raw UI remains private.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import sys
import zlib

sys.path.insert(0, str(Path(__file__).resolve().parent))
from catalog import ROOT, pin
from inventory_historical_saves import guard

guard()
ap = argparse.ArgumentParser()
ap.add_argument('--run', default='ui-verification01')
args = ap.parse_args()
assert args.run.replace('-', '').isalnum()
base = ROOT / '.local-work/e2-organic'
out = base / (args.run + '.json')
assert not out.exists()
old = ROOT / '.local-work/e1-arithmetic'
archive = Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield/Data/Starfield - Interface.ba2')
inputs = [archive, old/'ui-disasm.py', old/'ui-assets/workshopbuildermenu.swf',
          old/'ui-assets/workshopbuildermenu.uncompressed.swf',
          old/'ui-assets/workshopbuildermenu.uncompressed.abc.json']
before = [pin(p) for p in inputs]
with archive.open('rb') as f:
    h = f.read(32)
    magic, version, kind, count, names = struct.unpack('<4sI4sIQ', h[:24])
    assert (magic, version, kind) == (b'BTDX', 2, b'GNRL')
    records = [f.read(36) for _ in range(count)]
    f.seek(names)
    found = []
    for i in range(count):
        n = int.from_bytes(f.read(2), 'little')
        name = f.read(n).decode()
        if name.lower() == 'interface/workshopbuildermenu.swf':
            found.append((i, name))
    assert len(found) == 1
    i, name = found[0]
    offset, packed, unpacked = struct.unpack_from('<QII', records[i], 16)
    assert offset + (packed or unpacked) <= names
    f.seek(offset); raw = f.read(packed or unpacked)
    data = zlib.decompress(raw) if packed else raw
    assert len(data) == unpacked and data == inputs[2].read_bytes()
    assert data[:3] in (b'FWS', b'CWS')
    swf = data if data[:3] == b'FWS' else b'FWS' + data[3:8] + zlib.decompress(data[8:])
    assert len(swf) == int.from_bytes(data[4:8], 'little') and swf == inputs[3].read_bytes()
spec = importlib.util.spec_from_file_location('owned_ui_decoder', inputs[1])
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
methods = []
for block in json.loads(inputs[4].read_text()):
    for body in block['bodies']:
        code = bytes.fromhex(body['code_hex'])
        offset_in_swf = block['swf_abc_offset'] + body['abc_code_offset']
        assert swf[offset_in_swf:offset_in_swf+len(code)] == code
        ins = module.decode(block, body)
        if body['method'] in {344, 373, 374, 589, 840, 842, 843, 844}:
            methods.append(dict(method=body['method'], aliases=body['aliases'],
                                offset_in_swf=offset_in_swf,
                                code_sha256=hashlib.sha256(code).hexdigest(), instructions=ins))
assert len(methods) == 8
assert [pin(p) for p in inputs] == before
with out.open('x', encoding='utf8', newline='\n') as f:
    json.dump(dict(inputs=before, tool=pin(Path(__file__)), archive_member=name,
                   member_index=i, methods=methods, status='PASS',
                   limits=['Instruction decoding/branch inspection only; no UI execution']), f, indent=2)
    f.write('\n')
print('PASS archive identity, full SWF equality, every ABC method byte span, eight selected methods')
