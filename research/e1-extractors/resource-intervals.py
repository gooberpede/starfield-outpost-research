# SPDX-License-Identifier: GPL-3.0-or-later
"""Bounded original offline E1 inventory; uses the owned strict ESM reader.
Reads pinned Starfield.esm; writes exclusive ignored
JSON only. Stdlib/CPython; repository cwd; C:/D: free-space guards. No game,
save, configuration, database, index, network or installation effects.
"""
from pathlib import Path
import argparse
import collections
import hashlib
import json
import re
import struct
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'save-analysis/scripts'))
from inspect_outpost_definitions import esm_records
from inventory_historical_saves import guard


def f32(v):
    return struct.unpack('<f', struct.pack('<f', v))[0]


def pin(p):
    with p.open('rb') as f:
        return dict(path=str(p), bytes=p.stat().st_size,
                    sha256=hashlib.file_digest(f, 'sha256').hexdigest())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--run', required=True)
    args = ap.parse_args()
    assert args.run.isalnum()
    guard()
    path = Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield/Data/Starfield.esm')
    before = pin(path)
    assert before['sha256'] == '1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7'
    counts = collections.Counter()
    records = {}
    for h, fs in esm_records(path, {b'IRES', b'AVIF', b'GLOB', b'CONT', b'COBJ', b'KYWD', b'MISC'}, repeated=True):
        counts[h['type']] += 1
        assert h['formid'] not in records
        fields = collections.defaultdict(list)
        for k, v in fs:
            fields[k.decode()].append(v)
        records[h['formid']] = dict(**h, edid=fields.get('EDID', [b''])[0].rstrip(b'\0').decode(), fields=fields)

    def single(r, k, default=b''):
        a = r['fields'].get(k, [])
        assert len(a) <= 1, (r['edid'], k)
        return a[0] if a else default

    def u32(r, k):
        b = single(r, k, b'\0'*4)
        assert len(b) == 4
        return int.from_bytes(b, 'little')

    def props(r):
        data = b''.join(r['fields'].get('PRPS', []))
        assert len(data) % 12 == 0
        result = {}
        for p in range(0, len(data), 12):
            fid, value, tail = struct.unpack_from('<IfI', data, p)
            assert fid not in result
            result[fid] = dict(value=value, tail=tail, bytes=data[p:p+12].hex())
        return result

    inorganic = [r for r in records.values() if r['type'] == 'IRES' and r['edid'].startswith('ResInorg')]
    avs = {u32(r, 'NAM1') for r in inorganic}
    assert len(avs) == len(inorganic)
    bases = []
    candidates = []
    for r in records.values():
        if r['type'] != 'CONT':
            continue
        ps = props(r)
        linked = sorted(avs & ps.keys())
        kw = single(r, 'KWDA')
        assert len(kw) % 4 == 0
        kws = list(struct.unpack('<'+'I'*(len(kw)//4), kw))
        family = [records.get(k, {}).get('edid', hex(k)) for k in kws if k in {0x299548, 0x299549, 0x29954a}]
        if linked or r['edid'].startswith('OutpostHarvester') or family or 0x8406 in kws:
            row = dict(formid=r['formid'], offset=r['offset'], edid=r['edid'],
                       family=family, resource_avs=linked, properties=ps,
                       keywords=kws, flags=r['flags'], model=single(r, 'MODL').rstrip(b'\0').decode())
            candidates.append(row)
            if linked:
                bases.append(row)
    recipes = collections.defaultdict(list)
    for r in records.values():
        if r['type'] == 'COBJ':
            recipes[u32(r, 'CNAM')].append(dict(formid=r['formid'], offset=r['offset'], edid=r['edid']))
    resources = []
    for r in inorganic:
        av = u32(r, 'NAM1'); gid = u32(r, 'NAM3'); g = records[gid]
        assert g['type'] == 'GLOB' and records[av]['type'] == 'AVIF'
        raw = single(g, 'FLTV'); assert len(raw) == 4
        seconds = f32(struct.unpack('<f', raw)[0]*3600)
        linked = [b for b in bases if av in b['resource_avs']]
        recipe = records[u32(r, 'NAM2')]
        assert recipe['type'] == 'COBJ'
        product = records[u32(recipe, 'CNAM')]
        assert product['type'] == 'MISC'
        for b in linked:
            b['construction_recipes'] = recipes[b['formid']]
            m = re.search(r'_(01|02|03)(?:_|$)', b['edid'])
            b['tier_by_edid'] = int(m[1]) if m else None
        resources.append(dict(formid=r['formid'], offset=r['offset'], edid=r['edid'],
                              resource_av=av, av_offset=records[av]['offset'],
                              interval_global=gid, global_edid=g['edid'], global_offset=g['offset'],
                              hours_bytes=raw.hex(), seconds=seconds,
                              production_recipe=u32(r, 'NAM2'), recipe_offset=recipe['offset'],
                              product=product['formid'], product_edid=product['edid'],
                              product_offset=product['offset'], extractors=linked))
    default = struct.unpack('<f', single(records[0x8407], 'NAM0'))[0]
    assert default == 1
    assert pin(path) == before
    result = dict(source=before, tool=pin(Path(__file__)), python=sys.version,
                  dependencies=[pin(ROOT/'save-analysis/scripts'/n) for n in
                                ['inspect_outpost_definitions.py', 'inventory_historical_saves.py']],
                  counts=counts, rate_av_default=default, resources=resources,
                  container_candidates=candidates,
                  excluded_ires=[dict(formid=r['formid'], edid=r['edid']) for r in records.values()
                                 if r['type'] == 'IRES' and r not in inorganic])
    out = ROOT/'.local-work/e1-intervals'/('inventory'+args.run+'.json')
    with out.open('x', encoding='utf8', newline='\n') as f:
        json.dump(result, f, indent=2); f.write('\n')
    guard()
    print('PASS pinned inventory', dict(counts), 'inorganic', len(resources), 'linked CONT', len(bases), 'candidates', len(candidates))


if __name__ == '__main__':
    main()
