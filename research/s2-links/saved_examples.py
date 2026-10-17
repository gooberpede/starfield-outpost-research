# SPDX-License-Identifier: GPL-3.0-or-later
"""Finite S2 HIST-0036 joins, not a general inventory reader.

Reads existing pinned S1/E3 receipts and their protected original through owned
readers. Rechecks the complete supported edge envelope and selected inventories,
owners and producer rows. Writes one exclusive ignored JSON; decoded scratch is
cleaned by decoded_save. CPython -B, stdlib/project only; no native execution,
save/config/database/Git mutation or network. Both-drive 40 GB guards apply.
"""
import argparse
import collections
import json
from pathlib import Path
import struct
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'research/s1-storage'))
from catalog import pin
from saved import inventory, extra_view
from inventory_historical_saves import guard
from stream_save import decoded_save
from extractor_resources import plugin_tables, saved_form
from outpost_membership import token_value
from outpost_record_framing import iter_records
from validate_mature_outposts import directory, envelopes
from workshop_inventory import reference_prefix
from research_resource_availability import audit

SELECTED = {
    'ff02a281', 'ff030376', 'ff02a29b', 'ff02a2c7',
    'ff05632f', 'ff018b62', 'ff0288d7', 'ff031075',
    'ff01aa14', 'ff01aa4d', 'ff0514e1', 'ff050aae', 'ff038416',
    'ff028cfd', 'ff028cbd', 'ff0382cf', 'ff018b64', 'ff02c339',
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--run', required=True)
    args = ap.parse_args()
    assert args.run.isalnum()
    guard()
    base = ROOT / '.local-work/s2-links'
    out = base / (args.run + '.json')
    assert not out.exists()
    prior_path = ROOT / '.local-work/e3-fabricators/saved01/HIST-0036.json'
    storage_path = ROOT / '.local-work/s1-storage/saved05.json'
    prior = json.loads(prior_path.read_text(encoding='utf8'))
    storage = json.loads(storage_path.read_text(encoding='utf8'))
    expected = {r['identity']: r for r in storage['rows']}
    selected = {'DYNAMIC:' + n for n in SELECTED}
    source = Path(prior['source']['path'])
    before = pin(source)
    assert before == prior['source'] == storage['source']
    rows = {}
    with decoded_save(source, base / 'scratch') as (data, decoded):
        d = directory(data)
        qualified = [e for e in envelopes(data, d) if e['qualifies']]
        assert len(qualified) == 1 and 'parsed' in qualified[0]
        forms = struct.unpack_from('<' + 'I' * d['reference_count'], data,
                                   d['regions']['reference_u32'][0] + 4)
        plugins = plugin_tables(data)

        def resolve(t):
            return saved_form(token_value(t, forms), plugins)

        edges = [(resolve(s), resolve(g['key']))
                 for g in qualified[0]['parsed']['groups'] for s in g['refs']]
        assert edges == [tuple(e) for e in prior['directed_edges']]
        fresh = audit(data)
        producers = collections.defaultdict(list)
        for b in fresh['beacons']:
            for g in b.get('workshop', {}).get('resource_rows', []):
                for p in g['rows']:
                    producers[p['reference_identities'][0]].append(
                        dict(owner=b['identity'], resource=g['resource_identity'], row=p))
        for r in iter_records(data, *d['regions']['region_R3'], d['words'][9]):
            identity = resolve(r['token'])
            if identity not in selected:
                continue
            old = expected[identity]
            p = reference_prefix(data, r, old['prefix']['case'])
            x = extra_view(data, r, p, resolve)
            inv = inventory(data, r, x, resolve)
            assert p == old['prefix'] and x == old['extra'] and inv == old['inventory']
            assert resolve(p['base_token']) == old['base']
            owners = [e for ex in x['extras'] if ex['type'] == '4c'
                      for e in ex['entries'] if e['keyword'] == 'starfield.esm:054ba6']
            rows[identity] = dict(base=old['base'], editorid=old['editorid'],
                                  record_offset=r['offset'], flags=r['flags'],
                                  owners=owners, inventory=inv,
                                  producer_rows=producers[identity])
    assert rows.keys() == selected
    joined = []
    for order, (s, t) in enumerate(edges):
        if s in rows and t in rows:
            so = {x['target'] for x in rows[s]['owners']}
            to = {x['target'] for x in rows[t]['owners']}
            joined.append(dict(source=s, destination=t, serialized_edge_index=order,
                               common_explicit_owners=sorted(so & to)))
    expected_pairs = {
        ('ff02a281', 'ff02a29b'), ('ff030376', 'ff02a29b'),
        ('ff02a29b', 'ff02a2c7'), ('ff05632f', 'ff018b62'),
        ('ff0288d7', 'ff031075'), ('ff01aa14', 'ff01aa4d'),
        ('ff0514e1', 'ff038416'), ('ff050aae', 'ff038416'),
        ('ff028cfd', 'ff028cbd'),
    }
    assert {(e['source'][8:], e['destination'][8:]) for e in joined} == expected_pairs
    assert all(e['common_explicit_owners'] for e in joined)
    assert pin(source) == before
    result = dict(source=before, priors=[pin(prior_path), pin(storage_path)],
                  tool=pin(Path(__file__)), decoded=decoded,
                  edge_envelope=qualified[0], all_supported_edges_equal=True,
                  edge_count=len(edges), selected_rows=rows, joined_edges=joined,
                  source_unchanged=True,
                  limits=['Historical snapshot; no movement/timing observation',
                          'Serialized order is not stable routing priority',
                          'Empty-stack-extra subset; unsupported is unknown'])
    with out.open('x', encoding='utf8', newline='\n') as f:
        json.dump(result, f, indent=2)
        f.write('\n')
    guard()
    print('PASS', len(edges), 'edges;', len(rows), 'fresh endpoint joins;', len(joined), 'selected edges')


if __name__ == '__main__':
    main()
