# SPDX-License-Identifier: GPL-3.0-or-later
"""Summarize P1 inspected saved ExtraCB adjacency without simulating allocation.
Reads only instances04..09 JSON receipts. Writes exclusive local --run JSON.
No original saves, native/game execution, third-party dependencies or Git effects.
Reuses project saved_instances.pin; unknown endpoints/representation stay explicit.
Reciprocity and components are observed serialized structure, not load authority.
"""
import argparse
import collections
import json
from pathlib import Path
from saved_instances import ROOT, pin


def analyze(j):
    nodes = {r['identity']: r for r in j['rows']}
    edges = []
    flags = {}
    for r in j['rows']:
        for e in r.get('extra_view', {}).get('extras', []):
            if e['type'] == 'cb':
                for t, v in zip(e['references'], e['words']):
                    edges.append(dict(source=r['identity'], target=t, word=v,
                                      extra_offset=e['offset'], words_offset=e['words_offset']))
            if e['type'] == '9c':
                flags[r['identity']] = dict(flags=e['flags'], offset=e['offset'])
    adjacency = collections.defaultdict(list)
    pairs = {(e['source'], e['target']) for e in edges}
    for e in edges:
        adjacency[e['source']].append(e['target'])
    components, seen = [], set()
    for start in nodes:
        if start in seen:
            continue
        todo, members = [start], []
        while todo:
            n = todo.pop()
            if n in seen:
                continue
            seen.add(n); members.append(n)
            todo.extend(t for t in adjacency[n] if t in nodes and t not in seen)
        components.append(dict(nodes=members, kinds=dict(collections.Counter(nodes[n]['kind'] for n in members)),
                               boundary_edges=[e for e in edges if e['source'] in members and e['target'] not in nodes]))
    return dict(sample=j['sample'], source=j['source'], decoded=j['decoded'], counts=j['counts'],
                candidate_count=len(nodes), extra_status=dict(collections.Counter(r.get('extra_view', {}).get('status', 'GAP') for r in nodes.values())),
                graph_edges=len(edges), words=dict(collections.Counter(str(e['word']) for e in edges)),
                reciprocal_edges=sum((e['target'], e['source']) in pairs for e in edges),
                unpaired_edges=[e for e in edges if (e['target'], e['source']) not in pairs],
                external_edges=[e for e in edges if e['target'] not in nodes],
                no_cb_target_nodes=[n for n in nodes if not adjacency[n]],
                flags_by_kind=dict(collections.Counter(f"{nodes[n]['kind']}:{v['flags']:x}" for n, v in flags.items())),
                components=components, edges=edges, flags=flags,
                record_locators={n: dict(kind=r['kind'], base=r['base'], edid=r['definition_edid'],
                                        offset=r['record_offset'], end=r['record_end'],
                                        props=r['base_props']) for n, r in nodes.items()})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--run', required=True)
    args = ap.parse_args()
    assert args.run.isalnum()
    base = ROOT / '.local-work/p1-power/saved'
    paths = [base / f'instances{i:02d}.json' for i in (4, 5, 6, 7, 8, 9)]
    rows = [analyze(json.loads(p.read_text())) for p in paths]
    out = base / (args.run + '.json')
    with out.open('x', encoding='utf8', newline='\n') as f:
        json.dump(dict(inputs=[pin(p) for p in paths], tool=pin(Path(__file__)), rows=rows,
            limits=['Components cover only positively identified candidates',
                    'Zero serialized targets is not proof of universal physical unwired state',
                    'ExtraCB adjacency interpretation requires native corroboration; no power simulation']), f, indent=2)
        f.write('\n')
    for r in rows:
        print(json.dumps({k: r[k] for k in ['sample', 'candidate_count', 'graph_edges', 'reciprocal_edges', 'words', 'extra_status', 'flags_by_kind']}))
        print(json.dumps(dict(components=len(r['components']), no_cb_targets=len(r['no_cb_target_nodes']), external_edges=len(r['external_edges']))))


if __name__ == '__main__':
    main()
