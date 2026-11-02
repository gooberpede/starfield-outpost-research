# SPDX-License-Identifier: GPL-3.0-or-later
"""Test D5AF observational discrimination and call-level arbitration controls.

Reads authenticated B2 with the owned D5AC decoder, existing owned D5AE predicate
model and fresh native queue receipts. Writes a fresh ignored D5AF directory.
Stdlib only; no game, save, database, configuration, network or Git mutation.
SOR-P-0002 lineage is explicit: D5AC decoding and D5AE SourceModel. Synthetic
schedules test implications, not retail frequency or Windows lock fairness.
Stop on identity/oracle/disk-floor failure; retain outputs and diagnostics.
"""
import json
from pathlib import Path
import sys

from d5ad_baseline import guard, sha
from d5ac_reconstruct import SESSION, decode_frames
from d5ae_controls import SourceModel, controls as inherited_controls

ROOT = Path(__file__).resolve().parents[2]


def schedules():
    rows = []
    # Both requests have passed the same native shared visited predicate. The
    # exclusive acquisition order is supplied, never derived from event stamps.
    for order in [('B', 'A'), ('A', 'B'), ('C', 'B', 'A'), ('C', 'A', 'B')]:
        model = SourceModel()
        for request in ('A', 'B', 'C'):
            model.visit(request, token=11 if request == 'C' else 10)
        for request in order:
            model.exclusive(request, pointer=101 if request == 'C' else 100,
                            token=11 if request == 'C' else 10)
        expected = next(r for r in order if r in ('A', 'B'))
        if model.holders[(1, 100)] != expected:
            raise AssertionError('Independent first-target-acquisition oracle')
        rows.append(dict(order=order, winner=expected, log=model.log,
                         scope='Synthetic call-level equivalent, successful allocation'))
    # Dependency-ready order changes eligibility before any visited test. A
    # priority value alone does not activate a still-pending request.
    for ready_order in [('A', 'B'), ('B', 'A')]:
        model = SourceModel()
        first, second = ready_order
        if model.visit(second, ready=False) != 'dependency-pending':
            raise AssertionError('Pending request admitted')
        model.visit(first)
        model.exclusive(first)
        if model.visit(second) != 'visited':
            raise AssertionError('Later-ready request regenerated retained source')
        rows.append(dict(ready_order=ready_order, rank=[0, 0], winner=first,
                         scope='Synthetic readiness predicate control'))
    # Equal readiness/rank and earlier event stamp do not constrain callback
    # completion. These two legal thread-local orders share the same recorded
    # stamps and final outcomes while assigning different callback-return times.
    observable = dict(A_stamp=0, B_stamp=10, B_lookup=60, B_store=70, A_lookup=100)
    histories = [dict(A_return=90, A_attempt=91, B_return=20, B_attempt=21),
                 dict(A_return=1, A_attempt=91, B_return=20, B_attempt=21)]
    for history in histories:
        for request in ('A', 'B'):
            if not (observable[request+'_stamp'] < history[request+'_return']
                    < history[request+'_attempt'] < observable[request+'_lookup']):
                raise AssertionError('Per-thread native order violated')
    rows.append(dict(observations=observable, hidden_histories=histories,
                     scope='Synthetic observation-equivalence witness; arbitrary units, no measured delay'))
    return rows


def main():
    if not __debug__ or sys.flags.optimize:
        raise RuntimeError('Use Python -E -B without optimization')
    out = Path(sys.argv[1]).resolve()
    if out.exists() or not out.is_relative_to(ROOT / '.local-work/d5af'):
        raise ValueError('Fresh task-local output required')
    free = guard()
    raw = SESSION / 'events.bin'
    events = decode_frames(raw.read_bytes())
    selected = {s: events[s-1] for s in (8004,8005,8006,8018,8019,8020,
                                       8091,8094,8104,8105,8106,8339)}
    a,b,miss,hit = [selected[s] for s in (8006,8020,8091,8339)]
    if not (a['ticks'] < b['ticks'] < miss['ticks'] < selected[8106]['ticks'] < hit['ticks']):
        raise AssertionError('Native QPC order')
    if len({(e['proc'],e['source'],e['epoch']) for e in (a,b,miss,hit)}) != 1:
        raise AssertionError('Contender identity')
    if (a['thread'],b['thread'],a['invocation'],b['invocation']) != (42984,44268,3837,3844):
        raise AssertionError('B2 thread/invocation provenance')
    intervening = [e for e in events if e['kind'] == 4 and e['proc'] == a['proc']
                   and a['ticks'] < e['ticks'] < hit['ticks']]
    if [e['sequence'] for e in sorted(intervening,key=lambda e:e['ticks'])] != [8054,8069,8081,8090,8091,8113,8142,8184]:
        raise AssertionError('Owner-wide competing protected decisions')
    durations = dict(A_stamp_to_lookup_ticks=hit['ticks']-a['ticks'],
                     B_stamp_to_lookup_ticks=miss['ticks']-b['ticks'],
                     stamps_separated_ticks=b['ticks']-a['ticks'],
                     qpc_hz=10_000_000, interpretation='Elapsed intervals, not lock wait times')
    # Existing negative state/failure predicates are reused as owned code, not
    # promoted to new native engine execution.
    state_cases = inherited_controls()
    queue_path = ROOT / '.local-work/d5af/incremental01.json'
    queue = json.loads(queue_path.read_bytes())
    rows = schedules()
    out.mkdir(parents=True)
    result = dict(schema='sor-d5af-controls/1', method_sha256=sha(__file__),free=free,
                  raw_sha256=sha(raw), decoder_sha256=sha(ROOT/'research/resource-retained-population/d5ac_reconstruct.py'),
                  model_sha256=sha(ROOT/'research/resource-retained-population/d5ae_controls.py'),
                  queue_sha256=sha(queue_path), queue=queue, b2=selected,
                  same_owner_intervening_lookups=intervening,elapsed=durations,
                  state_cases=state_cases,schedules=rows,
                  native_scope='Queue receipt contains actual native fixture execution; arbitration schedules are synthetic')
    (out/'controls.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf8',newline='\n')
    print(json.dumps(dict(state_cases=len(state_cases),schedule_cases=len(rows),
                          intervening_same_owner=len(intervening),elapsed=durations)))


if __name__ == '__main__':
    main()
