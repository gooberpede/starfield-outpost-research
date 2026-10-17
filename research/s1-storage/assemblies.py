# SPDX-License-Identifier: GPL-3.0-or-later
"""Read installed ESM headers and selected PKIN cell children plus relevant ACTI.
Writes exclusive ignored assembly receipt, no database/game/save/Git effects.
Owned E3 header-walk method and strict project subrecords reader. Run CPython -B
from repository root with fresh --run NAME. Stdlib only; raw evidence local.
"""
import argparse
import json
from pathlib import Path
import struct
import sys
import zlib
from catalog import ROOT, pin, field, fields
sys.path.insert(0, str(ROOT / 'save-analysis/scripts'))
from inspect_outpost_definitions import subrecords
from inventory_historical_saves import guard


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--run', required=True)
    a = ap.parse_args()
    assert a.run.isalnum()
    guard()
    j = json.loads((ROOT / '.local-work/e2-organic/inventory02.json').read_text())
    by = {r['formid']: r for r in j['records']}
    source = Path(j['source']['path'])
    before = pin(source)
    assert before == j['source']
    packins = [r for r in by.values() if r['type'] == 'PKIN' and
               ('CargoLink' in r['edid'] or r['formid'] == 0x42dc2)]
    cells = {int.from_bytes(field(r, 'CNAM'), 'little'): r for r in packins}
    children, actis = [], []
    with source.open('rb') as f:
        end = source.stat().st_size
        stack = [(end, None)]
        pos = 0
        while pos < end:
            while pos == stack[-1][0] and len(stack) > 1:
                stack.pop()
            f.seek(pos)
            h = f.read(24)
            assert len(h) == 24
            tag = h[:4]
            n, flags, fid = struct.unpack_from('<III', h, 4)
            stop = pos + (n if tag == b'GRUP' else n + 24)
            assert pos + 24 <= stop <= stack[-1][0]
            cell = stack[-1][1]
            if tag == b'GRUP':
                if struct.unpack_from('<I', h, 12)[0] == 6:
                    cell = flags
                stack.append((stop, cell))
                pos += 24
                continue
            if tag == b'ACTI' or (tag == b'REFR' and cell in cells):
                data = f.read(n)
                if flags & 0x40000:
                    size = struct.unpack_from('<I', data)[0]
                    data = zlib.decompress(data[4:])
                    assert len(data) == size
                fs = [(k.decode(), v.hex()) for k, v in subrecords(data)]
                r = dict(formid=f'{fid:08x}', offset=pos, fields=fs)
                if tag == b'ACTI':
                    edid = next((bytes.fromhex(v).rstrip(b'\0').decode() for k, v in fs if k == 'EDID'), '')
                    if 'Outpost' in edid:
                        actis.append(dict(**r, editorid=edid))
                else:
                    children.append(dict(**r, packin=cells[cell]['edid']))
            pos = stop
    assert pin(source) == before
    out = ROOT / '.local-work/s1-storage' / (a.run + '.json')
    with out.open('x', encoding='utf8', newline='\n') as f:
        json.dump(dict(source=before, tool=pin(Path(__file__)), packins=packins,
                       children=children, actis=actis, source_unchanged=True), f, indent=2)
        f.write('\n')
    print('PASS', len(children), 'selected children;', len(actis), 'outpost ACTI')


if __name__ == '__main__':
    main()
