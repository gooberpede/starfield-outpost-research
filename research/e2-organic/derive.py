# SPDX-License-Identifier: GPL-3.0-or-later
"""Derive local E2 catalog from inventory02; verify selected physical ESM fields.
Reads inventory, main ESM, existing Save52 inventory and sibling CSV. Writes one
exclusive ignored JSON. Stdlib/owned reader only; no original/save/target writes.
No live state or menu membership is inferred from these definitions.
"""
import argparse
import collections
import csv
import json
from pathlib import Path
import struct
import sys
import zlib

sys.path.insert(0, str(Path(__file__).resolve().parent))
from catalog import ROOT, pin
from inspect_outpost_definitions import subrecords


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--inventory', type=Path, default=ROOT / '.local-work/e2-organic/inventory02.json')
    ap.add_argument('--run', default='derived01')
    args = ap.parse_args()
    assert args.run.isalnum()
    base = ROOT / '.local-work/e2-organic'
    out = base / (args.run + '.json')
    assert not out.exists()
    inventory = args.inventory
    j = json.loads(inventory.read_text())
    rs = j['records']
    by = {r['formid']: r for r in rs}
    assert len(by) == len(rs)
    selected = {}

    def field(r, k):
        a = [bytes.fromhex(v) for t, v in r['fields'] if t == k]
        assert len(a) <= 1, (r['edid'], k)
        return a[0] if a else b''

    def number(r, k):
        return int.from_bytes(field(r, k), 'little')

    def identify(r):
        selected[r['formid']] = r
        return dict(formid=f"{r['formid']:08x}", edid=r['edid'], offset=r['offset'], type=r['type'])

    def inputs(r):
        data = field(r, 'FVPA')
        assert len(data) % 12 == 0
        return [dict(**identify(by[i]), quantity=q, tail=t) for i, q, t in struct.iter_unpack('<III', data)]

    bases = []
    for r in rs:
        if r['type'] != 'CONT':
            continue
        kw = field(r, 'KWDA')
        assert len(kw) % 4 == 0
        kws = [i[0] for i in struct.iter_unpack('<I', kw)]
        if not {0x2731a0, 0x2c5a95}.issubset(kws):
            continue
        ps = {i: v for i, v, tail in struct.iter_unpack('<IfI', field(r, 'PRPS'))}
        bases.append(dict(**identify(r), keywords=[identify(by[k]) for k in kws],
                          properties={f'{i:08x}': v for i, v in ps.items()},
                          resource_avs=[i for i in ps if by.get(i, {}).get('type') == 'AVIF'
                                       and by[i]['edid'].startswith('ResourceOrg')]))
    resources = []
    avset = {i for b in bases for i in b['resource_avs']}
    for r in rs:
        if r['type'] != 'IRES' or number(r, 'NAM1') not in avset:
            continue
        av, recipe, glob = [by[number(r, k)] for k in ['NAM1', 'NAM2', 'NAM3']]
        product = by[number(recipe, 'CNAM')]
        assert (av['type'], recipe['type'], glob['type'], product['type']) == ('AVIF', 'COBJ', 'GLOB', 'MISC')
        raw = field(glob, 'FLTV')
        assert len(raw) == 4
        seconds = struct.unpack('<f', struct.pack('<f', struct.unpack('<f', raw)[0] * 3600))[0]
        resources.append(dict(**identify(r), av=identify(av), recipe=identify(recipe), product=identify(product),
                              interval_global=identify(glob), seconds=seconds,
                              recipe_count=number(recipe, 'NNAM'), inputs=inputs(recipe)))
    construction = []
    for r in rs:
        if r['type'] == 'COBJ' and 'Organic' in r['edid'] and r['edid'].startswith('co_Outpost_'):
            target = by.get(number(r, 'CNAM'))
            construction.append(dict(**identify(r), created=identify(target) if target else None,
                                     inputs=inputs(r), conditions=[v for k, v in r['fields'] if k == 'CTDA']))
    # Cross-check all exported recipe signatures against canonical or both
    # fauna-specific alternatives. This does not independently recover NPC OMODs.
    resource_by_id = {r['formid']: r for r in resources}
    grouped = collections.defaultdict(list)
    for r in resources:
        grouped[r['product']['formid']].append(r)
    csvpath = Path(j['text_sources'][2]['path'])
    with csvpath.open(encoding='utf-8-sig', newline='') as f:
        rows = list(csv.DictReader(f))
    checked = 0
    for row in rows:
        if row['ResourceResolutionStatus'] != 'Resolved':
            continue
        canonical = resource_by_id[row['ResourceFormID'].lower()]
        expected = [(row[f'ResourceInput{i}FormID'].lower(), int(row[f'ResourceInput{i}Qty']))
                    for i in (1, 2) if row[f'ResourceInput{i}FormID']]
        candidates = grouped[canonical['product']['formid']]
        assert any([(x['formid'], x['quantity']) for x in r['inputs']] == expected for r in candidates), row
        checked += 1
    # Read exact selected records independently by physical offset, including
    # compressed closure and every repeated field, rather than trusting cache.
    esm = Path(j['source']['path'])
    assert pin(esm) == j['source']
    with esm.open('rb') as f:
        for r in selected.values():
            f.seek(r['offset']); h = f.read(24)
            n, flags, fid = struct.unpack_from('<III', h, 4)
            assert h[:4].decode() == r['type'] and fid == r['formid'] and flags == r['flags']
            data = f.read(n)
            if flags & 0x40000:
                size = struct.unpack_from('<I', data)[0]
                d = zlib.decompressobj(); data = d.decompress(data[4:], size + 1)
                assert len(data) == size and d.eof and not d.unused_data and not d.unconsumed_tail
            assert [[k.decode(), v.hex()] for k, v in subrecords(data)] == r['fields']
    save_inventory = ROOT / '.local-work/workshop-inventory/final05/mature-Save52.json'
    before_save = pin(save_inventory)
    saved = json.loads(save_inventory.read_text())
    roots = [{k: r[k] for k in ['instance_identity', 'owner_identity', 'construction_definition',
              'editor_name', 'record_offset', 'member_identities', 'member_offsets']}
             for r in saved['constructed_instances'] if 'BuilderOrganic' in r.get('editor_name', '')]
    del saved
    assert pin(save_inventory) == before_save
    assert pin(esm) == j['source']
    result = dict(inventory=pin(inventory), source=j['source'], tool=pin(Path(__file__)),
                  bases=bases, resources=resources, construction=construction, saved_roots=roots,
                  saved_inventory=before_save, physical_records_checked=len(selected),
                  csv_recipe_signatures_checked=checked,
                  limits=['No NPC OMOD or diet recovery in CSV cross-check', 'No actual current output/eligibility sampled',
                          'Save roots are prior supported positive subset, not full population'])
    with out.open('x', encoding='utf8', newline='\n') as f:
        json.dump(result, f, indent=2); f.write('\n')
    print(json.dumps(dict(bases=len(bases), resources=len(resources), construction=len(construction),
                         physical=len(selected), csv_checked=checked, saved_roots=len(roots))))


if __name__ == '__main__':
    main()
