# SPDX-License-Identifier: GPL-3.0-or-later
"""Bounded Save52 leading ExtraBF reader, adapted from owned workshop_inventory.
Reads protected save and E2 catalog/producer receipts; temporary decoded scratch
is cleaned by existing decoder. Writes exclusive ignored JSON only. Stdlib and
project readers; no game/save/config/analysis mutations. Only six known case-5
organic producer records and their leading BF are interpreted, never byte-searched.
"""
import argparse
import json
from pathlib import Path
import struct
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from catalog import ROOT, pin
from inventory_historical_saves import guard
from stream_save import decoded_save
from extractor_resources import plugin_tables, saved_form
from outpost_membership import token_value
from outpost_record_framing import Reader, iter_records
from validate_mature_outposts import directory
from workshop_inventory import reference_prefix, linked_prefix

guard()
ap = argparse.ArgumentParser()
ap.add_argument('--run', default='selected-state01')
args = ap.parse_args()
assert args.run.replace('-', '').isalnum()
base = ROOT / '.local-work/e2-organic'
out = base / (args.run + '.json')
assert not out.exists()
receipt = json.loads((base / 'saved02.json').read_text())
catalog = json.loads((base / 'derived01.json').read_text())
by_ires = {'starfield.esm:' + r['formid'][2:]: r for r in catalog['resources']}
expected = {p['reference_identities'][0]: by_ires[g['resource']]['av']['formid']
            for g in receipt['organic_groups'] for p in g['producers']}
source = Path(receipt['source']['path'])
before = pin(source)
assert before == receipt['source']
rows = []
with decoded_save(source, base / 'scratch') as (data, metadata):
    d = directory(data)
    a, z = d['regions']['reference_u32']
    forms = struct.unpack_from('<' + 'I' * d['reference_count'], data, a + 4)
    plugins = plugin_tables(data)

    def resolve(t):
        return saved_form(token_value(t, forms), plugins)

    for r in iter_records(data, *d['regions']['region_R3'], d['words'][9]):
        identity = resolve(r['token'])
        if identity not in expected:
            continue
        assert not r['flags'] & 0x8000
        prefix = reference_prefix(data, r, 5)
        closure = linked_prefix(data, r, prefix)
        assert closure['following_extras'] == 'CLOSED'
        c = Reader(data, prefix['form_prefix_end'], r['end'])
        ri = prefix['next_reference_index']
        if r['flags'] & 0x80:
            ri += 1
            if not r['flags'] & 0xa6031f40:
                ri += 1
        if r['flags'] & 0x10:
            c.take(4)
        count = c.count()
        bf_start = c.p
        assert c.take(1) == b'\xbf'
        sections = []
        for bits in (1, 3):
            n = c.count()
            mask = c.take((bits * n + 7) // 8)
            tokens = r['refs'][ri:ri+n]
            assert len(tokens) == n
            ri += n
            values = []
            for i in range(bits * n):
                present = bool(mask[i // 8] & (1 << (i % 8)))
                offset = c.p
                value = struct.unpack('<f', c.take(4))[0] if present else None
                values.append(dict(index=i, present=present, offset=offset if present else None, value=value))
            sections.append(dict(bits=bits, count=n, mask=mask.hex(),
                                 av_identities=[resolve(t) for t in tokens], values=values))
        av = 'starfield.esm:' + expected[identity][2:]
        initial = sections[0]
        i = initial['av_identities'].index(av)
        assert initial['values'][i]['present'] and initial['values'][i]['value'] == 1.0
        rows.append(dict(identity=identity, record_offset=r['offset'], bf_offset=bf_start,
                         bf_end=c.p, sections=sections, selected_av=av, selected_value=1.0,
                         remaining_extras=closure['types'], following_extras='CLOSED'))
assert len(rows) == len(expected) == 6
assert pin(source) == before
with out.open('x', encoding='utf8', newline='\n') as f:
    json.dump(dict(source=before, tool=pin(Path(__file__)), owned_grammar=pin(ROOT/'save-analysis/scripts/workshop_inventory.py'),
                   decoded=metadata, rows=rows, status='PASS',
                   limits=['Leading BF in six known case-5 producer records only', 'Historical values, not actual loaded state']), f, indent=2)
    f.write('\n')
guard()
print('PASS six saved ExtraBF base AV values equal 1 and match producer-map resource AV')
