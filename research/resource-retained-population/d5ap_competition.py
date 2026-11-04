# SPDX-License-Identifier: GPL-3.0-or-later
"""Reduce authenticated D5AP histories and test unobserved claim continuations.

Reads one source-locked D5AP derivative; writes an exclusive local output tree.
Stdlib only, no target or sealed-input writes. Reuses owned D5AP extraction under
SOR-P-0002. Callback timing comparisons are observational bounds, never arbitrary
cross-thread happens-before edges. Claim fixtures instantiate native permitted
intervals; they do not execute game code or reconstruct an actual claim time.
"""
import os
import sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):
    raise RuntimeError('Use pinned Python -E -B without optimization')

import argparse
from collections import Counter, defaultdict
import csv
import json
from pathlib import Path
from d5ap_analyze import ROOT, guard, require, sha, write


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--analysis', type=Path, required=True)
    parser.add_argument('--summary-sha256', required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    guard()
    source = args.analysis.resolve()
    require(sha(source / 'summary.json') == args.summary_sha256, 'Summary binding')
    summary = json.loads((source / 'summary.json').read_bytes())
    for name, expected in summary['outputs'].items():
        require(sha(source / name) == expected, 'Derivative changed: ' + name)
    out = args.out.absolute()
    require(out.resolve().is_relative_to(ROOT / '.local-work/d5ap'), 'D5AP-local output required')
    require(not any(p.is_symlink() or p.is_junction() for p in (out, *out.parents)), 'Reparse output')
    out.mkdir(parents=True, exist_ok=False)
    load = lambda name: json.loads((source / name).read_bytes())
    cs, core, causal = load('contenders.json'), load('core.json'), load('causal.json')['events']
    scheduler, participants = load('scheduler.json')['events'], load('participants.json')
    compatible = [r for r in scheduler if r['kind'] == 1 and
                  -2 <= r['request'][0] <= 11 and -2 <= r['request'][1] <= 11]
    target_tasks = {(c['node'], c['task']) for c in cs}
    require({(r['node'], r['allocation']) for r in compatible} == target_tasks and
            len(compatible) == len(cs), 'Unexamined coordinate-compatible task')
    winner = next(c for c in cs if c['outcome'] == 'MISS')
    stage = lambda c, k: next(e for e in c['scheduler'] if e['kind'] == k)
    lookup = next(e for e in winner['core'] if e['kind'] == 4)
    store = next(e for e in winner['core'] if e['kind'] == 17)
    provider_ticks, miss_ticks = stage(winner, 9)['ticks'], lookup['ticks']
    nearest = {}
    for kind in (1, 2, 5, 3, 10, 7, 9):
        nearest[str(kind)] = [dict(task=c['task'], request=c['request'], family=c['family'],
            sequence=stage(c, kind)['sequence'], ticks=stage(c, kind)['ticks'],
            delta_from_winner=stage(c, kind)['ticks'] - stage(winner, kind)['ticks'])
            for c in sorted(cs, key=lambda c: stage(c, kind)['ticks'])[:8]]
    partitions = defaultdict(list)
    for c in cs:
        if c is winner:
            group = 'CONSTRUCTOR'
        elif stage(c, 5)['ticks'] > miss_ticks:
            group = 'READY_APPROACH_AFTER_AUTHORITY'
        elif stage(c, 9)['ticks'] > miss_ticks:
            group = 'READY_BUT_PROVIDER_AFTER_AUTHORITY'
        else:
            group = 'PROVIDER_BEFORE_AUTHORITY_EARLIER_SOURCE_WORK'
        partitions[group].append(c['task'])
    # Every potential peer is represented; positive same-thread work shows why
    # the already executing providers had not yet selected the target source.
    peers = []
    by_invocation = defaultdict(list)
    for row in core:
        by_invocation[row['invocation']].append(row)
    for c in cs:
        if c is winner or stage(c, 9)['ticks'] > miss_ticks:
            continue
        path = by_invocation[c['invocation']]
        selected = next(r for r in c['core'] if r['kind'] == 2)
        require(selected['ticks'] > store['ticks'], 'Peer target could compete before store')
        peers.append(dict(task=c['task'], request=c['request'], invocation=c['invocation'],
            all_core=path, target_selected=selected['sequence'], target_selected_ticks=selected['ticks']))
    active = []
    for part in participants:
        first, last = part['events'][0], part['events'][-1]
        if first['ticks'] <= miss_ticks and last['ticks'] >= provider_ticks:
            active.append(part)
    # Searchable owner-wide census includes explicit unknown unscoped identities.
    selections = {(r['thread'], r['invocation'], r['selection'], r['source']): r
                  for r in core if r['kind'] == 2}
    provider_index = {(r['thread'], r['core_invocation']): r for r in scheduler if r['kind'] == 9}
    with (out / 'owner-participants.csv').open('x', encoding='utf8', newline='') as stream:
        writer = csv.writer(stream, lineterminator='\n')
        writer.writerow(['type', 'lock_runtime_va', 'generation', 'thread', 'invocation', 'selection',
                         'source_runtime_va', 'task', 'request', 'events', 'ticks', 'identity_status'])
        for part in participants:
            e = part['events'][0]
            key = tuple(e[k] for k in ('thread', 'invocation', 'selection', 'source'))
            selected = selections.get(key)
            p = provider_index.get((e['thread'], e['invocation']))
            writer.writerow([part['type'], hex(e['lock']), e['generation'], e['thread'], e['invocation'],
                e['selection'], hex(e['source']), p['allocation'] if p else 'NOT-OBSERVED', e['request'],
                ' '.join(str(r['sequence']) for r in part['events']),
                ' '.join(str(r['ticks']) for r in part['events']),
                'OBSERVED_CORE_SELECTION' if selected else 'OBSERVED_OWNER_UNSCOPED_SOURCE'])
    # Compact graph: causal-channel same-thread chains are true program order.
    # Tick-sorted cross-channel diagrams would manufacture equal-tick ordering.
    threads = defaultdict(list)
    for row in causal:
        threads[str(row['thread'])].append(row['sequence'])
    graph = dict(schema='sor-d5ap-causal-graph/1',
        same_thread_causal_chains=dict(threads),
        transition_intervals=[dict(type=p['type'], sequences=[r['sequence'] for r in p['events']],
            stamps=[r['ticks'] for r in p['events']],
            semantics='REGISTRATION_AND_RELEASE_STAMPS_FOLLOW_ATOMICS; ADMITTED_STAMP_FOLLOWS_ADMISSION') for p in participants],
        winner_edges=[dict(before=2942, after=2949, semantics='SAME_THREAD_READER_RELEASE_BEFORE_PENDING_XADD'),
                      dict(before=2949, after=2950, semantics='SAME_THREAD_PENDING_BEFORE_SUCCESSFUL_OWNERSHIP'),
                      dict(before=2932, after=2950, semantics='FOREIGN_EXCLUSIVE_RELEASE_REQUIRED_BEFORE_WINNER_CAS')],
        scope='Full recorded owner generation. No cross-thread QPC edges; see exact operands and native predicates.')
    write(out / 'graph.json', graph)
    # Positive nonuniqueness witness: the claim callback stamp follows the CAS.
    # Choose two different legal times inside the actual dispatch-to-return gap;
    # every other observed event and atomic operand is fixed in both fixtures.
    dispatch = stage(winner, 3)['ticks']
    returned = stage(winner, 10)['ticks']
    queue_return = stage(winner, 12)['ticks']
    previous = max((dict(channel=channel, **r)
        for channel, rows in (('core', core), ('causal', causal), ('scheduler', scheduler))
        for r in rows if r['thread'] == winner['thread'] and r['ticks'] < returned),
        key=lambda r: r['ticks'])
    lo = max(dispatch, queue_return, previous['ticks'])
    require(lo + 3 < returned, 'No nonempty claim interval')
    choices = [lo + (returned-lo)//3, lo + 2*(returned-lo)//3]
    fixtures = [dict(successful_claim_cas_ticks=t, claim_return_ticks=returned,
        unobserved_post_claim_gap_ticks=returned-t,
        native_path='SUCCESSFUL_QUEUE_CAS_THEN_RETURN_CONTINUATION',
        observed_projection_sha256=args.summary_sha256) for t in choices]
    require(choices[0] != choices[1] and all(queue_return < t < returned for t in choices), 'Illegal claim fixtures')
    # The post-claim gap can contain ordinary native execution/preemption or
    # observer/OS cost; no unrecorded scheduler instrumentation resolves it.
    write(out / 'equivalence.json', dict(schema='sor-d5ap-claim-equivalence/1', fixtures=fixtures,
        fixed_observed_inputs=summary['outputs'], constraints=dict(dispatch=dispatch,
        enqueue_return=queue_return, last_recorded_same_thread=previous,
        claim_return=returned, callback=stage(winner, 7)['ticks']),
        proved='Two distinct candidate CAS times satisfy the checked scalar bounds; complete native scheduling equivalence is not established.',
        not_proved='A different N2 constructor, selected queue route, or retail execution probability.',
        missing='Successful selection-CAS timestamp and branch identity; interval cost attribution remains separate.'))
    # Validate observed target disqualification directly rather than treating
    # an empty exclusive-stage array as proof by itself.
    require(all(next(r for r in c['core'] if r['kind'] == 3)['a'] == (0 if c is winner else 1) for c in cs), 'Visited result mismatch')
    require(all(not any(r['kind'] in (9, 2, 3, 10, 7) for r in c['causal']) for c in cs if c is not winner), 'Unexpected target exclusive competitor')
    write(out / 'competition.json', dict(schema='sor-d5ap-competition/1', source_summary_sha256=args.summary_sha256,
        source_sha256=sha(__file__), partitions=dict(partitions), nearest_stages=nearest,
        coordinate_compatible_publications=len(compatible), unjoined_compatible_publications=0,
        provider_peers=peers, decisive_owner_participants=active,
        decisive_owner_participant_counts=dict(Counter(p['type'] for p in active)),
        decisive_coverage='Callback-envelope intersection; may include post-transition lag, not an atomic overlap assertion.',
        target_exclusive_calls=1, target_unvisited=1, target_visited_bypass=391,
        predecessor_core=[r for r in core if r['thread'] == winner['thread'] and r['invocation'] == winner['invocation']],
        outputs={p.name: sha(p) for p in out.iterdir() if p.is_file()}))
    print(json.dumps(dict(partitions={k: len(v) for k, v in partitions.items()},
                         active=dict(Counter(p['type'] for p in active)), nearest=nearest['9']), indent=2))


if __name__ == '__main__':
    main()
