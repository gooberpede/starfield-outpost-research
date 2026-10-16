# SPDX-License-Identifier: GPL-3.0-or-later
"""Read-only E2 Save52 producer audit using existing owned decoder/Workshop reader.
Reads pinned original save, prior receipt, derived catalog. Writes exclusive local
JSON and disposable decoded scratch through existing cleanup context. Stdlib and
project readers only; C:/D: guards; no game, restoration or source-save writes.
"""
import argparse
import collections
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from catalog import ROOT, pin
from inventory_historical_saves import guard
from research_resource_availability import audit
from stream_save import decoded_save
from extractor_resources import plugin_tables, saved_form
from outpost_membership import token_value
from validate_mature_outposts import directory, envelopes
import struct


def main():
    guard()
    ap = argparse.ArgumentParser()
    ap.add_argument('--run', required=True)
    args = ap.parse_args()
    assert args.run.isalnum()
    base = ROOT / '.local-work/e2-organic'
    out = base / (args.run + '.json')
    assert not out.exists()
    prior = ROOT / '.local-work/resource-availability/saves01/mature-Save52.json'
    old = json.loads(prior.read_text())
    source = Path(old['source']['path'])
    before = pin(source)
    assert before['sha256'] == old['source']['sha256']
    assert before['bytes'] == old['source']['size']
    definitions = json.loads((base / 'derived01.json').read_text())
    ids = {'starfield.esm:' + r['formid'][2:]: r for r in definitions['resources']}
    with decoded_save(source, base / 'scratch') as (data, metadata):
        fresh = audit(data)
        d = directory(data)
        es = [e for e in envelopes(data, d) if e['qualifies']]
        assert len(es) == 1 and 'parsed' in es[0]
        a, z = d['regions']['reference_u32']
        forms = struct.unpack_from('<' + 'I' * d['reference_count'], data, a + 4)
        plugins = plugin_tables(data)

        def resolve(token):
            return saved_form(token_value(token, forms), plugins)

        edges = [(resolve(s), resolve(g['key'])) for g in es[0]['parsed']['groups'] for s in g['refs']]
    rows = []
    for beacon in fresh['beacons']:
        for group in beacon.get('workshop', {}).get('resource_rows', []):
            if group['resource_identity'] in ids:
                rows.append(dict(owner=beacon['identity'], resource=group['resource_identity'],
                                 resource_edid=ids[group['resource_identity']]['edid'],
                                 count_offset=group['count_offset'], producers=group['rows']))
    producers = collections.defaultdict(list)
    for beacon in fresh['beacons']:
        for group in beacon.get('workshop', {}).get('resource_rows', []):
            for row in group['rows']:
                producers[row['reference_identities'][0]].append(group['resource_identity'])
    incoming = collections.defaultdict(list)
    for s, t in edges:
        incoming[t].append(s)
    traces = []
    for group in rows:
        for producer in group['producers']:
            start = producer['reference_identities'][0]
            visited = {start}
            queue = collections.deque([[start]])
            paths, terminals = [], []
            while queue:
                path = queue.popleft()
                node = path[-1]
                if node != start and 'starfield.esm:0083ec' in producers[node]:
                    paths.append(path)
                if not incoming[node]:
                    terminals.append(dict(identity=node, path=path, resource_rows=producers[node],
                                          semantics='NO_FURTHER_SAVED_INCOMING_EDGE; endpoint type unresolved'))
                for nxt in incoming[node]:
                    if nxt not in visited:
                        visited.add(nxt); queue.append(path + [nxt])
            traces.append(dict(producer=start, water_producer_paths=paths, terminals=terminals,
                               visited=len(visited), result='LOCAL_SAVED_WATER_PRODUCER_REACHED' if paths else
                               'NO_SAVED_WATER_PRODUCER_PATH_IDENTIFIED; terminal provenance unresolved'))
    assert fresh == old['data']
    assert pin(source) == before
    result = dict(source=before, prior=pin(prior), tool=pin(Path(__file__)),
                  decoded=metadata, exact_prior_audit_equal=True, organic_groups=rows,
                  link_envelope=es[0], directed_edges=edges, upstream_water_traces=traces,
                  limits=['Ordinary inline-base beacon subset only', 'Saved scheduling/configuration, not current eligibility/output'])
    with out.open('x', encoding='utf8', newline='\n') as f:
        json.dump(result, f, indent=2); f.write('\n')
    guard()
    print(json.dumps(dict(groups=len(rows), producers=sum(len(r['producers']) for r in rows),
                         exact_prior_audit_equal=True)))


if __name__ == '__main__':
    main()
