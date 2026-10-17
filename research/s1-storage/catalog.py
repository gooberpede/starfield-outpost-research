# SPDX-License-Identifier: GPL-3.0-or-later
"""S1 offline census. Reads pinned E2 index and installed ESM, rereads selected
records. Writes new ignored JSON and authored summary CSV. Stdlib/project only;
no game, database, save, configuration or Git mutation. Run from repository root
with CPython -B; --run must be fresh. Raw fields stay local.
"""
import argparse
import csv
import hashlib
import io
import json
from pathlib import Path
import struct
import sys
import zlib

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'save-analysis/scripts'))
from inspect_outpost_definitions import subrecords
from inventory_historical_saves import guard


def pin(p):
    p = Path(p)
    with p.open('rb') as f:
        return dict(path=str(p), bytes=p.stat().st_size,
                    sha256=hashlib.file_digest(f, 'sha256').hexdigest())


def fields(r, k):
    return [bytes.fromhex(v) for t, v in r['fields'] if t == k]


def field(r, k):
    a = fields(r, k)
    assert len(a) <= 1, (r['edid'], k)
    return a[0] if a else b''


def words(r, k):
    return [v[0] for v in struct.iter_unpack('<I', field(r, k))]


def props(r):
    return {i: v for i, v, tail in struct.iter_unpack('<IfI', field(r, 'PRPS'))}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--run', required=True)
    a = ap.parse_args()
    assert a.run.isalnum()
    guard()
    base = ROOT / '.local-work/s1-storage'
    out = base / (a.run + '.json')
    assert not out.exists()
    cache = ROOT / '.local-work/e2-organic/inventory02.json'
    j = json.loads(cache.read_text())
    source = Path(j['source']['path'])
    before = pin(source)
    assert before == j['source']
    rs = j['records']
    by = {r['formid']: r for r in rs}
    # A bounded positive census of every CONT bearing the ordinary Workshop
    # object keyword. Retain non-logistics containers as explicit exclusions.
    chest_lists = [by[i] for i in (0xb863, 0x80665, 0x80667)]
    chests = {int.from_bytes(v, 'little') for r in chest_lists for v in fields(r, 'LNAM')}
    selected = [r for r in rs if r['type'] == 'CONT' and
                (0x1f55f1 in words(r, 'KWDA') or r['formid'] in chests)]
    rows = []
    touched = {r['formid']: r for r in selected}
    for r in selected:
        p = props(r)
        filters = words(r, 'ONAM')
        for i in words(r, 'KWDA') + filters + list(p):
            if i in by:
                touched[i] = by[i]
        filter_entries = [int.from_bytes(v, 'little') for i in filters for v in fields(by[i], 'LNAM')]
        for i in filter_entries:
            touched[i] = by[i]
        rows.append(dict(formid=f"{r['formid']:08x}", editorid=r['edid'],
                         offset=r['offset'], carryweight=p.get(0x2dc),
                         build_container=p.get(0xf65a), no_in=p.get(0x2192d5),
                         no_out=p.get(0x313eb), filters=[f'{i:08x}' for i in filters],
                         filter_entries=[dict(formid=f'{i:08x}', editorid=by[i]['edid'], type=by[i]['type']) for i in filter_entries],
                         boundary_chest=r['formid'] in chests,
                         keywords=[by[i]['edid'] if i in by else f'{i:08x}' for i in words(r, 'KWDA')],
                         properties={by[i]['edid'] if i in by else f'{i:08x}': v for i, v in p.items()},
                         raw_fields=r['fields']))
    # Reread each candidate and its direct classification/configuration records
    # at exact physical offsets; no semantics inferred from hash equality.
    with source.open('rb') as f:
        for r in touched.values():
            f.seek(r['offset'])
            h = f.read(24)
            tag = h[:4].decode()
            n, flags, fid = struct.unpack_from('<III', h, 4)
            assert (tag, fid) == (r['type'], r['formid'])
            data = f.read(n)
            if flags & 0x40000:
                size = struct.unpack_from('<I', data)[0]
                data = zlib.decompress(data[4:])
                assert len(data) == size
            assert [(k.decode(), v.hex()) for k, v in subrecords(data)] == [tuple(v) for v in r['fields']]
    assert pin(source) == before
    construction = []
    for r in rs:
        if r['type'] == 'COBJ':
            product = int.from_bytes(field(r, 'CNAM'), 'little')
            if product in touched or product in (0x1f9af2, 0x1f9af4, 0x1f9af5, 0x1f9af8):
                construction.append(dict(formid=f"{r['formid']:08x}", editorid=r['edid'],
                                         product=f'{product:08x}', offset=r['offset']))
    result = dict(source=before, cache=pin(cache), tool=pin(Path(__file__)),
                  python=sys.version, rows=rows, reread_records=len(touched),
                  construction=construction,
                  source_unchanged=True, scope='All main-ESM CONT with KYWD 001f55f1; not all construction roots or overrides')
    out.write_text(json.dumps(result, indent=2) + '\n', encoding='utf8', newline='\n')
    print('PASS', len(rows), 'Workshop CONT;', len(touched), 'physical rereads;', out)


if __name__ == '__main__':
    main()
