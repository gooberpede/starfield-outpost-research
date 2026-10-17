# SPDX-License-Identifier: GPL-3.0-or-later
"""Bounded offline order/state follow-up; project-owned stdlib readers only.

Reads pinned P1 receipts and their protected original saves. Reframes full R3,
checks selected records against prior evidence, and emits exclusive local JSON.
Decoded scratch is guarded and removed by decoded_save. No game, database,
network, original writes, power calculation or Git effects. Replay consumes
actual saved word-3 forests with explicitly conditional runtime predicates.
Run from repository: CPython -B research/p1-power/followup.py --run NAME.
"""
import argparse
import collections
import json
from pathlib import Path
import struct

from saved_instances import (ROOT, pin, guard, decoded_save, directory,
                             plugin_tables, saved_form, token_value,
                             iter_records, reference_prefix, extra_view)


def generation_walk(adj, root, recursive=False):
    """Only direct admitted edges: recursive forward vs deque front promotion."""
    seen, order, pending = set(), [], [root]
    if recursive:
        def visit(n):
            if n in seen:
                return
            seen.add(n); order.append(n)
            for t in adj[n]:
                visit(t)
        visit(root)
    else:
        while pending:
            n = pending.pop(0)
            assert n not in seen
            seen.add(n); order.append(n)
            for t in adj[n]:
                if t in seen:
                    continue
                if t in pending:
                    pending.remove(t)
                pending.insert(0, t)
    return order


def assessment_walk(adj, seeds, excluded=(), terminals=()):
    """Allocator vector index walk; no demand/supply/result simulation."""
    vector, seen, order = list(seeds), set(), []
    i = 0
    while i < len(vector):
        n = vector[i]; i += 1
        if n in seen:
            continue
        seen.add(n)
        if n in excluded:
            continue
        order.append(n)
        if n not in terminals:
            vector.extend(t for t in adj[n] if t not in seen)
    return order


def inspect(path, outbase):
    old = json.loads(path.read_text())
    source = Path(old['source']['path'])
    before = pin(source)
    assert before == old['source']
    expected = {r['record_offset']: r for r in old['rows']}
    rows = []
    guard()
    with decoded_save(source, outbase / 'scratch') as (data, decoded):
        d = directory(data)
        a, _ = d['regions']['reference_u32']
        forms = struct.unpack_from('<'+'I'*d['reference_count'], data, a+4)
        plugins = plugin_tables(data)
        def resolve(t):
            return saved_form(token_value(t, forms), plugins)
        for r in iter_records(data, *d['regions']['region_R3'], d['words'][9]):
            if r['offset'] not in expected:
                continue
            prior = expected[r['offset']]
            p = reference_prefix(data, r, prior['prefix']['case'])
            assert resolve(r['token']) == prior['identity']
            assert r['flags'] == prior['change_flags']
            assert r['end'] == prior['record_end'] and p == prior['prefix']
            e = extra_view(data, r, p, resolve)
            assert e == prior['extra_view']
            rows.append(dict(identity=prior['identity'], base=prior['base'],
                kind=prior['kind'], offset=r['offset'], end=r['end'],
                change_flags=r['flags'], open_difference=bool(r['flags'] & 0x800000),
                default_difference=bool(r['flags'] & 0x400000),
                extras=e, props=prior['base_props']))
    assert len(rows) == len(expected) and pin(source) == before
    guard()
    return dict(sample=old['sample'], source=before, prior=pin(path),
                decoded=decoded, source_unchanged=True, rows=rows)


def replay(sample):
    nodes = {r['identity']: r for r in sample['rows']}
    adj = {}
    for n, r in nodes.items():
        es = [e for e in r['extras'].get('extras', []) if e['type'] == 'cb']
        if r['extras']['status'] != 'COUNT_CLOSED' or len(es) != 1:
            continue
        e = es[0]
        if all(w == 3 and t in nodes for t, w in zip(e['references'], e['words'])):
            adj[n] = e['references']
    # Choose a complete actual connected component with multiple generators.
    choices, seen = [], set()
    for root in sorted(adj):
        if root in seen:
            continue
        todo, members = [root], set()
        while todo:
            n = todo.pop()
            if n in members:
                continue
            members.add(n)
            todo.extend(adj.get(n, []))
        seen |= members
        if not members <= adj.keys():
            continue
        gens = sorted(n for n in members if nodes[n]['kind'] == 'GENERATOR')
        if len(gens) > 1:
            choices.append((len(members), sorted(members), gens))
    assert choices
    _, members, gens = sorted(choices)[0]
    assert sum(len(adj[n]) for n in members) == 2*(len(members)-1)
    # Chosen ordinary fixture: connector generators/switches, wired receiver
    # lamps and leaf consumers. Current matching AV/category state is assumed.
    terminals = []
    for n in members:
        r = nodes[n]
        if r['kind'] in ('GENERATOR', 'SWITCH'):
            assert r['props'].get('0002d0', 0) != 0
        elif r['kind'] == 'LAMP':
            assert r['props'].get('0003a2', 0) != 0  # receiver, word 3 expands
        else:
            assert r['kind'] == 'CONSUMER' and len(adj[n]) == 1
            terminals.append(n)
    modes = []
    for root in gens:
        for recursive in (False, True):
            walk = generation_walk(adj, root, recursive)
            seeds = [n for n in walk if n in gens]
            sequence = assessment_walk(adj, seeds, terminals=terminals)
            assert set(sequence) == set(members)
            modes.append(dict(root=root, recursive=recursive, generation_visit=walk,
                              generator_seeds=seeds, assessment=sequence))
    switches = [n for n in members if nodes[n]['kind'] == 'SWITCH']
    blocked = []
    if switches:
        # Conditional state change, not an assertion that this switch was open.
        blocked = assessment_walk(adj, modes[0]['generator_seeds'], [switches[0]], terminals)
    return dict(sample=sample['sample'], members=members,
        ordered_adjacency={n: adj[n] for n in members}, modes=modes,
        terminal_consumers=terminals,
        conditional_excluded_switch=switches[0] if switches else None,
        assessment_with_exclusion=blocked,
        limits=['Assume all saved direct word-3 targets resolve with unchanged order',
                'Assume each generator eligible and all nodes otherwise valid',
                'No spline, word-1 partition, cell fallback or demand calculation',
                'Roots chosen as explicit parameters, not reconstructed events',
                'Not validation of historical or loaded assessment/powered state'])


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--run', required=True)
    args = ap.parse_args(); assert args.run.isalnum()
    base = ROOT / '.local-work/p1-order/saved'; base.mkdir(parents=True, exist_ok=True)
    out = base / (args.run+'.json'); assert not out.exists()
    samples = [inspect(ROOT / f'.local-work/p1-power/saved/instances{i:02}.json', base)
               for i in (4, 5)]
    fixtures = [replay(s) for s in samples]
    # Independent small counterexample for duplicate-pending front promotion.
    cycle = dict(a=['b', 'c', 'd'], b=['a', 'd'], c=['a'], d=['a', 'b'])
    assert generation_walk(cycle, 'a') == ['a', 'd', 'b', 'c']
    assert generation_walk(cycle, 'a', True) == ['a', 'b', 'd', 'c']
    j = dict(tool=pin(Path(__file__)), samples=samples, fixtures=fixtures,
             limits=['No paired toggle ground truth or live animation/script sampling'])
    with out.open('x', encoding='utf8', newline='\n') as f:
        json.dump(j, f, indent=2); f.write('\n')
    for s, f in zip(samples, fixtures):
        print(s['sample'], len(s['rows']), 'fixture', len(f['members']),
              'orders', len({tuple(m['assessment']) for m in f['modes']}),
              'switch differences', dict(collections.Counter(
                  (r['open_difference'], r['default_difference'])
                  for r in s['rows'] if r['kind'] == 'SWITCH')))


if __name__ == '__main__':
    main()
