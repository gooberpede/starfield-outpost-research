# SPDX-License-Identifier: GPL-3.0-or-later
"""Bounded S1 follow-up calculation receipts, not an inventory extractor.
Reads four existing owned S1 saved receipts and their hash-pinned originals,
installed ESM/index and census; physically rereads selected definitions. Writes
one fresh ignored JSON plus optional authored calculation CSV. Stdlib/owned
readers only, CPython -B from repo root. No game, save/database/Git mutation.
Unknown effective inputs remain unknown; nominal predictions are explicit.
"""
import argparse
import collections
import csv
import json
from pathlib import Path
import struct
import zlib
from catalog import ROOT, pin, field, props, words
from inspect_outpost_definitions import subrecords
from inventory_historical_saves import guard


def f32(x):
    return struct.unpack('<f', struct.pack('<f', x))[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--run', required=True)
    ap.add_argument('--table', action='store_true')
    a = ap.parse_args()
    assert a.run.isalnum()
    guard()
    out = ROOT / '.local-work/s1-capacity' / (a.run + '.json')
    assert not out.exists()
    cache = ROOT / '.local-work/e2-organic/inventory02.json'
    j = json.loads(cache.read_text())
    by = {r['formid']: r for r in j['records']}
    esm = Path(j['source']['path'])
    assert pin(esm) == j['source']
    census = json.loads((ROOT / '.local-work/s1-storage/census02.json').read_text())
    bases = {int(r['formid'], 16): r for r in census['rows']}
    touched = {0x2dc: by[0x2dc]}
    selected = {'ff018b64', 'ff018b66', 'ff018b61', 'ff02c339',
                'ff01c792', 'ff01ac54', 'ff018b73', 'ff01a4fb', 'ff0294fd'}
    examples, coverage, inputs = [], [], []
    for name in ['saved03', 'saved04', 'saved05', 'saved06']:
        p = ROOT / '.local-work/s1-storage' / (name + '.json')
        s = json.loads(p.read_text())
        assert pin(s['source']['path']) == s['source']
        assert pin(s['tool']['path']) == s['tool']
        inputs.extend([pin(p), s['source']])
        counts = collections.Counter()
        constrained = []
        for r in s['rows']:
            inv = r.get('inventory', {})
            counts[inv.get('status', r.get('gap', 'UNKNOWN'))] += 1
            if inv.get('status') != 'DECODED_EMPTY_STACK_EXTRA_SUBSET':
                continue
            bid = int(r['base'].split(':')[1], 16)
            base = by[bid]
            if bid not in bases:
                continue
            touched[bid] = base
            capacity = props(base).get(0x2dc)
            occupied, items = 0., []
            supported = True
            for row in inv['rows']:
                if not row['item'].startswith('starfield.esm:'):
                    supported = False
                    break
                iid = int(row['item'].split(':')[1], 16)
                item = by.get(iid)
                if not item or item['type'] != 'MISC' or len(field(item, 'DATA')) != 8:
                    supported = False
                    break
                touched[iid] = item
                assert not item['flags'] & 4, 'MISC virtual130 excludes flag bit2'
                weight = struct.unpack_from('<f', field(item, 'DATA'), 4)[0]
                count = sum(x['count'] for x in row['stacks'])
                assert all(x['count'] >= 0 for x in row['stacks']) and count < 0x100000000
                term = f32(f32(count) * weight)
                occupied = f32(occupied + term)
                items.append(dict(form=f'{iid:08x}', editorid=item['edid'], count=count,
                                  weight=weight, term=term, esm_offset=item['offset'],
                                  keywords=[f'{v:08x}' for v in words(item, 'KWDA')]))
            if not supported or capacity is None:
                counts['WEIGHT_OR_CAPACITY_UNSUPPORTED'] += 1
                continue
            saved_av = [v for e in r['extra']['extras'] if e['type'] == 'bf'
                        for section in e['sections'] for v in section['values']
                        if v['av'] == 'starfield.esm:0002dc']
            free = f32(capacity - occupied)
            nominal_full = occupied >= capacity
            if nominal_full:
                constrained.append(r['identity'])
            if r['identity'].split(':')[1] not in selected:
                continue
            if s['sample'] != 'HIST-0036' and not (s['sample'] == 'HIST-0077' and r['identity'] == 'DYNAMIC:ff0294fd'):
                continue
            # Empty solid/cargo controls use Lithium/Caesium respectively.
            candidate = items[0] if items else dict(form='0000557f' if bid == 0x23aed9 else '000057df')
            ci = by[int(candidate['form'], 16)]
            touched[ci['formid']] = ci
            filter_ids = words(base, 'ONAM')
            if filter_ids:
                admitted = {int.from_bytes(v, 'little') for fl in filter_ids
                            for k, v in by[fl]['fields'] if k == 'LNAM'
                            for v in [bytes.fromhex(v)]}
                assert ci['formid'] in admitted or admitted.intersection(words(ci, 'KWDA'))
                for fl in filter_ids:
                    touched[fl] = by[fl]
            assert not ci['flags'] & 4
            weight = struct.unpack_from('<f', field(ci, 'DATA'), 4)[0]
            fit = max(0, int(f32(free / weight))) if weight > 0 else None
            examples.append(dict(sample=s['sample'], reference=r['identity'], base=f'{bid:08x}',
                                 base_editorid=base['edid'], base_offset=base['offset'],
                                 record_offset=r['offset'], inventory_start=inv['start'], items=items,
                                 nominal_capacity=capacity, occupied_binary32=occupied,
                                 nominal_free_binary32=free, nominal_full=nominal_full,
                                 candidate=candidate['form'], candidate_weight=weight,
                                 nominal_fit=fit, saved_carryweight_values=saved_av,
                                 effective_capacity='UNMEASURED; fallback reconstruction is conditional',
                                 extra_types=[e['type'] for e in r['extra']['extras']]))
        coverage.append(dict(sample=s['sample'], candidates=len(s['rows']), statuses=dict(counts),
                             nominal_constrained=constrained,
                             scope='Four S1 positive inline-base subsets; not exhaustive corpus'))
    with esm.open('rb') as f:
        for r in touched.values():
            f.seek(r['offset'])
            h = f.read(24)
            n, flags, fid = struct.unpack_from('<III', h, 4)
            assert h[:4].decode() == r['type'] and fid == r['formid']
            data = f.read(n)
            if flags & 0x40000:
                size = struct.unpack_from('<I', data)[0]
                data = zlib.decompress(data[4:])
                assert len(data) == size
            assert [(k.decode(), v.hex()) for k, v in subrecords(data)] == [tuple(v) for v in r['fields']]
    assert pin(esm) == j['source']
    for p in inputs:
        assert pin(p['path']) == p
    guard()
    result = dict(tool=pin(__file__), esm=j['source'], cache=pin(cache), inputs=inputs,
                  examples=examples, coverage=coverage, reread_records=len(touched),
                  definitions=[dict(form=f'{i:08x}', editorid=r['edid'], type=r['type'], offset=r['offset']) for i, r in touched.items()],
                  qualification='Ordinary positive saved counts/empty stack extras and current main ESM fallback. No actual loaded capacity/stock measurement; historical overrides after load unknown.')
    out.write_text(json.dumps(result, indent=2) + '\n', encoding='utf8', newline='\n')
    if a.table:
        with (ROOT / 'docs/experiments/storage/capacity-examples.csv').open('w', encoding='utf8', newline='') as f:
            w = csv.writer(f, lineterminator='\n')
            w.writerow(['sample', 'reference', 'base', 'record_offset', 'inventory_start', 'contents_form_count_weight', 'fallback_capacity', 'occupied_binary32', 'fallback_free_binary32', 'candidate', 'fallback_fit', 'qualification'])
            for r in examples:
                w.writerow([r['sample'], r['reference'], r['base'], r['record_offset'], r['inventory_start'], ';'.join(i['form']+' x'+str(i['count'])+' @'+str(i['weight']) for i in r['items']), r['nominal_capacity'], r['occupied_binary32'], r['nominal_free_binary32'], r['candidate'], r['nominal_fit'], result['qualification']])
    print('PASS', len(examples), 'examples;', len(touched), 'physical rereads;', [(r['sample'], len(r['nominal_constrained'])) for r in coverage])


if __name__ == '__main__':
    main()
