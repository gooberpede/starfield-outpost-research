# SPDX-License-Identifier: GPL-3.0-or-later
"""Original bounded PKIN cell-child walk; local ignored output only.
Reads E2 inventory and pinned main ESM. Uses established 24-byte ESM/group
framing and owned subrecord reader; decompresses only REFRs in six target cells.
No game/save/analysis/configuration effects, dependencies, network or Git writes.
"""
import argparse
import json
from pathlib import Path
import struct
import sys
import zlib

sys.path.insert(0, str(Path(__file__).resolve().parent))
from catalog import ROOT, pin
from inventory_historical_saves import guard
from inspect_outpost_definitions import subrecords


def main():
    guard()
    ap = argparse.ArgumentParser()
    ap.add_argument('--inventory', type=Path, default=ROOT / '.local-work/e2-organic/inventory02.json')
    ap.add_argument('--run', default='assemblies01')
    args = ap.parse_args()
    assert args.run.isalnum()
    base = ROOT / '.local-work/e2-organic'
    out = base / (args.run + '.json')
    assert not out.exists()
    j = json.loads(args.inventory.read_text())
    pk = [r for r in j['records'] if r['type'] == 'PKIN' and r['edid'].startswith('OutpostPI_BuilderOrganic')]
    cells = {int.from_bytes(bytes.fromhex(v), 'little'): r for r in pk for k, v in r['fields'] if k == 'CNAM'}
    source = Path(j['source']['path'])
    assert pin(source) == j['source']
    rows = []
    with source.open('rb') as f:
        end = source.stat().st_size
        stack = [(end, None)]
        p = 0
        while p < end:
            while p == stack[-1][0] and len(stack) > 1:
                stack.pop()
            assert p + 24 <= stack[-1][0]
            f.seek(p); h = f.read(24)
            tag = h[:4]; n, flags, fid = struct.unpack_from('<III', h, 4)
            stop = p + (n if tag == b'GRUP' else n + 24)
            assert p + 24 <= stop <= stack[-1][0]
            cell = stack[-1][1]
            if tag == b'GRUP':
                kind = struct.unpack_from('<I', h, 12)[0]
                if kind == 6:
                    cell = flags
                stack.append((stop, cell)); p += 24
                continue
            if tag == b'REFR' and cell in cells:
                assert n <= 16 * 1024 * 1024
                data = f.read(n)
                if flags & 0x40000:
                    size = struct.unpack_from('<I', data)[0]
                    assert size <= 16 * 1024 * 1024
                    d = zlib.decompressobj(); data = d.decompress(data[4:], size + 1)
                    assert len(data) == size and d.eof and not d.unused_data and not d.unconsumed_tail
                fields = list(subrecords(data))
                names = [int.from_bytes(v, 'little') for k, v in fields if k == b'NAME']
                assert len(names) == 1
                rows.append(dict(packin=cells[cell]['formid'], cell=cell, formid=fid,
                                 offset=p, base=names[0]))
            p = stop
        assert p == end and all(stop == end for stop, _ in stack)
    assert pin(source) == j['source']
    result = dict(source=j['source'], tool=pin(Path(__file__)), packins=pk, references=rows,
                  limits=['Main ESM default cell children, not loaded instance enumeration'])
    with out.open('x', encoding='utf8', newline='\n') as f:
        json.dump(result, f, indent=2); f.write('\n')
    guard()
    print(dict(packins=len(pk), child_references=len(rows)))


if __name__ == '__main__':
    main()
