# SPDX-License-Identifier: GPL-3.0-or-later
"""Independent packed-state oracle and N2 observer/native-delay continuations.

Reads authenticated D5AP derivatives and existing native-source text; writes a
fresh local receipt only. Original stdlib model of the documented native masks,
not copied proprietary instructions or a live native experiment. Enumerates
legal atomic operand continuations independently of the indexed writer rules.
Timing fixtures preserve observed stamps and distinguish unobserved delay sites;
they supply no uninstrumented-winner or probability claim.
"""
import os
import sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):
    raise RuntimeError('Use pinned Python -E -B without optimization')

import argparse
import json
from pathlib import Path
from d5ap_analyze import ROOT, guard, require, sha, write


def transition(state, kind, owner=False):
    """Native packed-state predicates, independently of callback ordering."""
    if kind == 'reader_register':
        return state + 1
    if kind == 'reader_admit':
        return state if not state & 0xffc00000 or owner else None
    if kind == 'reader_release':
        return state - 1 if state & 0xfff else None
    if kind == 'pending':
        return state + 0x1000
    if kind == 'acquire':
        return state + 0x400000 if not state & 0xffc00fff and state & 0x3ff000 else None
    if kind == 'recursive':
        return state + 0x400000 if owner and state & 0xffc00000 else None
    if kind == 'recursive_release':
        return state - 0x400000 if state & 0xffc00000 >= 0x800000 else None
    if kind == 'release':
        return state - 0x401000 if state & 0xffc00000 == 0x400000 else None
    raise ValueError(kind)


def exhaustive_operands(rows, initial):
    """Enumerate only operand-compatible permutations; no timestamp ordering."""
    names = {2: 'pending', 3: 'acquire', 5: 'reader_register', 6: 'reader_release', 7: 'release'}
    results = []
    def visit(state, remaining, path):
        if not remaining:
            results.append(path)
            return
        for n, row in enumerate(remaining):
            if row['old_state'] != state:
                continue
            after = transition(state, names[row['kind']])
            if after != row['new_state']:
                continue
            visit(after, remaining[:n] + remaining[n+1:], path + [row['sequence']])
    visit(initial, rows, [])
    return results


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
    for name in ('causal.json', 'core.json', 'contenders.json', 'scheduler.json', 'content.json'):
        require(sha(source / name) == summary['outputs'][name], 'Changed derivative')
    causal = json.loads((source / 'causal.json').read_bytes())['events']
    core = json.loads((source / 'core.json').read_bytes())
    by_seq = {r['sequence']: r for r in causal}
    seqs = list(range(2927, 2933)) + [2935, 2937, 2940, 2941, 2942, 2949, 2950]
    rows = [by_seq[s] for s in seqs]
    orders = exhaustive_operands(rows, 0x401000)
    expected = [2927, 2928, 2929, 2930, 2931, 2932, 2935, 2937, 2941, 2940, 2942, 2949, 2950]
    require(orders == [expected], 'Actual cohort operand order is not uniquely reconstructed')
    corrupted = [dict(r) for r in rows]
    corrupted[-1]['new_state'] += 1
    require(not exhaustive_operands(corrupted, 0x401000), 'Contradictory CAS accepted')
    missing = [r for r in rows if r['sequence'] != 2941]
    require(not exhaustive_operands(missing, 0x401000), 'Missing reader release silently completed')
    checks = dict(pending_does_not_block_reader=transition(0x1000, 'reader_admit') == 0x1000,
        exclusive_blocks_foreign_reader=transition(0x401001, 'reader_admit') is None,
        recursive_owner_can_read=transition(0x401001, 'reader_admit', True) == 0x401001,
        pending_not_ticket=transition(0x2000, 'acquire') == 0x402000,
        outstanding_reader_blocks_writer=transition(0x2001, 'acquire') is None,
        recursive_requires_owner=transition(0x401000, 'recursive') is None,
        recursive_owner_depth=transition(0x401000, 'recursive', True) == 0x801000,
        recursive_release_preserves_pending=transition(0x801000, 'recursive_release') == 0x401000,
        final_release_preserves_registered_readers=transition(0x401005, 'release') == 5,
        zero_reader_release_refused=transition(0, 'reader_release') is None)
    require(all(checks.values()), 'Native predicate control failed')
    # The actual competitor's callback-tail gap straddles winner arbitration.
    a, b = by_seq[2946], next(r for r in core if r['sequence'] == 3967)
    require(a['thread'] == b['thread'] == 56840 and a['invocation'] == b['invocation'] == 1804, 'Peer identity')
    require(a['ticks'] < by_seq[2949]['ticks'] < by_seq[2950]['ticks'] < b['ticks'], 'Gap does not straddle arbitration')
    # Check every recorded event on this thread, including other invocations.
    scheduler = json.loads((source / 'scheduler.json').read_bytes())['events']
    content = json.loads((source / 'content.json').read_bytes())
    lifetime = content['lifetime']['events']
    gap_events = [dict(channel=name, sequence=r['sequence']) for name, values in
        (('causal', causal), ('core', core), ('scheduler', scheduler)) for r in values
        if r['thread'] == a['thread'] and a['ticks'] < r['ticks'] < b['ticks']]
    require(not any(r['thread'] == a['thread'] and a['ticks'] < r['ticks'] < b['ticks'] for r in lifetime), 'Intervening lifetime event')
    require(not gap_events, 'An intervening stamp constrains the proposed delay site')
    delay = 5000
    slack = b['ticks'] - a['ticks']
    require(slack > delay + 100, 'Insufficient actual gap')
    # emit stamps before queue publication and return. Callback completion and
    # native-loop progress are unobserved; either can contain the same pause.
    retained_header = ROOT / '.local-work/d5ao/final05/candidate/runtime/construction-winner/d5am_causality.h'
    require(sha(retained_header) == 'd3900246e4f6826f520cd1d2e5617c44fd58f5fa61f054346b0b23cc63bbce3c', 'Retained 0.9.3 emitter changed')
    event_text = retained_header.read_text(encoding='utf8')
    require('e.ticks=tick()' in event_text and 'emit(event(VisitedDone' in event_text, 'Timestamp placement source changed')
    continuations = [
        dict(name='OBSERVER_TAIL_DELAY', steps=[['visited_done_stamp', a['ticks']],
             ['event_published_sequence_2946', a['ticks']+1],
             ['observer_tail_preempt', a['ticks']+2], ['observer_resume', a['ticks']+2+delay],
             ['observer_return', a['ticks']+delay+50], ['native_next_selection', b['ticks']]]),
        dict(name='NATIVE_CONTINUATION_DELAY', steps=[['visited_done_stamp', a['ticks']],
             ['event_published_sequence_2946', a['ticks']+1],
             ['observer_return', a['ticks']+50], ['native_preempt', a['ticks']+51],
             ['native_resume', a['ticks']+51+delay], ['native_next_selection', b['ticks']]])]
    for fixture in continuations:
        require(all(x[1] < y[1] for x, y in zip(fixture['steps'], fixture['steps'][1:])), 'Nonmonotone continuation')
    # Challenge upstream enumeration against the complete actual target family.
    contenders = json.loads((source / 'contenders.json').read_bytes())
    density = sorted((c for c in contenders if c['family'] == 1),
                     key=lambda c: next(e['ticks'] for e in c['scheduler'] if e['kind'] == 1))
    coordinates = [tuple(c['request']) for c in density]
    frontier = sorted(((x, y) for x in range(-2, 12) for y in range(-2, 12)),
                      key=lambda q: (q[0]-q[1], q[0]))
    require(coordinates == frontier, 'Actual target density frontier order differs')
    require(sha(ROOT / 'research/resource-retained-population/d5s_controls.py') ==
            '8441b76dbcce7eed7f1176295dc2416e9ff703d452d92e03485d04336b5e45ea', 'Native registration model changed')
    import d5s_controls
    _, native_model = d5s_controls.registration()
    modeled = [q for q in native_model if -2 <= q[0] <= 11 and -2 <= q[1] <= 11]
    require(coordinates == modeled, 'Established native recursion model disagrees on target subsequence')
    target = args.out.absolute()
    require(target.resolve().is_relative_to(ROOT / '.local-work/d5ap'), 'D5AP-local output')
    require(not any(p.is_symlink() or p.is_junction() for p in (target, *target.parents)), 'Reparse output')
    write(target, dict(schema='sor-d5ap-native-controls/1', status='PASS', checks=checks,
        actual_atomic_order=orders, equal_tick_release_witnesses=[2941, 2940],
        negative_controls=['CONTRADICTORY_CAS', 'MISSING_READER_RELEASE'],
        delay_continuations=continuations, gap_ticks=slack, gap_recorded_events=gap_events,
        lifetime_gap_clear=True, retained_emitter_sha256=sha(retained_header),
        enumeration=dict(target_density_count=len(coordinates), all196_match=True,
            actual_order=coordinates, first=coordinates[0], first_task=density[0]['task'],
            publication_threads=sorted({next(e['thread'] for e in c['scheduler'] if e['kind'] == 1) for c in density}),
            model_sha256=sha(Path(d5s_controls.__file__)),
            scope='Target subsequence agrees; actual larger root rectangle/ingress arguments are unrecorded, so full publication stream equality is not claimed.'),
        projection=dict(causal_visited_done=2946, core_next_selected=3967,
                        fixed_inputs=summary['outputs']),
        semantics='Same actual projected event/operand record, different unobserved pause site during peer delay. No changed winner asserted.',
        limits='Original semantic continuation fixtures, not executed native instructions; delay attribution and uninstrumented outcome remain unidentifiable.',
        source_sha256=sha(__file__), summary_sha256=args.summary_sha256,
        native_semantic_sources={n: sha(ROOT / n) for n in (
            'runtime/construction-winner/d5am_causality.h',
            'docs/experiments/resource-retained-population/d5af-prelock-causality.md')}))
    print('PASS: actual operand cohort, adverse controls and two delay continuations')


if __name__ == '__main__':
    main()
