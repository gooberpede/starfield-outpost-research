# SPDX-License-Identifier: GPL-3.0-or-later
"""Independent bounded exhaustive oracles for the offline D5AP index.

Reads synthetic in-memory histories and optionally an existing authenticated
postflight JSON. Writes only an exclusive new D5AP-local receipt. Stdlib only;
no network, process, game, deployment, protected-save or original-evidence writes.
The postflight option checks analysis agreement, not raw-record authentication.
Invoke pinned installed CPython with -E -B. Original D5AM semantics are reused
under SOR-P-0002; the exhaustive implementation is independent of the index.
"""
import os
import sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):
    raise RuntimeError('Use pinned Python -E -B without optimization')

import argparse
from collections import Counter
import ctypes
import hashlib
import importlib.util
import json
from pathlib import Path
import random
import time
import tracemalloc

from d5ap_windows import HistoryIndex


def require(condition, message):
    if not condition:
        raise ValueError(message)


def exhaustive(rows, issues=()):
    """Small independent oracle: scan backward for each acquire, then all rows.

    This deliberately performs the expensive lifecycle scan for every pair.
    It neither invokes HistoryIndex nor shares any of its extraction helpers.
    """
    if 'MISSING_OR_DUPLICATE_REGISTRATION' in issues or 'UNKNOWN_INITIAL_HOLDERS' in issues:
        return []
    contexts = []
    for row in rows:
        identity = (row['thread'], row['invocation'], row['selection'], row['source'])
        if identity not in contexts:
            contexts.append(identity)
    calls = []
    for identity in contexts:
        local = [r for r in rows if tuple(r[k] for k in ('thread', 'invocation', 'selection', 'source')) == identity]
        for end, row in enumerate(local):
            if row['kind'] != 3:
                continue
            pending = approach = None
            for prior in reversed(local[:end]):
                if prior['kind'] == 3:
                    break
                if prior['kind'] == 2 and pending is None:
                    pending = prior
                if prior['kind'] == 9:
                    approach = prior
                    break
            if pending is not None:
                calls.append((approach, pending, row))
    result = []
    for a in calls:
        for b in calls:
            if a[2]['thread'] == b[2]['thread'] or a[2]['ticks'] >= b[2]['ticks']:
                continue
            values = [r for r in (*a, *b) if r is not None]
            lower, upper = min(r['ticks'] for r in values), max(r['ticks'] for r in values)
            uncertainty = any(r['status'] != 0 or r['hazards'] != 0 for r in values)
            for r in rows:
                if r['kind'] in (12, 13, 14) and lower <= r['ticks'] <= upper:
                    uncertainty = True
            code, edges = 'OVERLAPPING_INTERVALS_UNKNOWN', []
            if uncertainty:
                code = 'RELEVANT_LIFECYCLE_OR_CONTEXT_UNCERTAINTY'
            elif b[0] is not None and a[2]['ticks'] < b[0]['ticks']:
                code = 'EARLIER_ACQUISITION_BEFORE_OTHER_HELPER_ENTRY'
                edges = [a[2]['sequence'], b[0]['sequence']]
            elif a[0] is not None and b[1]['ticks'] < a[0]['ticks']:
                code = 'PRIOR_PENDING_WRITER_OVERTAKEN'
                edges = [b[1]['sequence'], a[0]['sequence'], a[2]['sequence']]
            result.append((a[2]['sequence'], b[2]['sequence'], code, edges))
    return result


def compact(index):
    return [(w['earlier_acquisition'], w['later_acquisition'], w['interpretation'],
             w['disjoint_callback_boundaries']) for w in index.iter_legacy()]


def row(sequence, kind, thread, ticks, invocation=None, source=None, **extra):
    result = dict(sequence=sequence, kind=kind, thread=thread, ticks=ticks,
                  lock=4096, generation=1, invocation=thread if invocation is None else invocation,
                  selection=thread, source=thread * 256 if source is None else source,
                  epoch=1, hazards=0, old_state=0, new_state=0, status=0, site=0, request=[0, 0])
    result.update(extra)
    return result


def synthetic():
    checks = []
    schedules = {
        'disjoint': [(9, 1, 10), (2, 1, 11), (3, 1, 12), (9, 2, 20), (2, 2, 21), (3, 2, 22)],
        'overlap': [(9, 1, 10), (2, 1, 11), (9, 2, 12), (2, 2, 13), (3, 1, 20), (3, 2, 22)],
        'overtaken': [(9, 2, 10), (2, 2, 11), (9, 1, 12), (2, 1, 13), (3, 1, 20), (3, 2, 22)],
        'equal_ticks': [(9, 1, 10), (2, 1, 11), (9, 2, 10), (2, 2, 11), (3, 1, 20), (3, 2, 20)],
        'missing_approach': [(2, 1, 11), (3, 1, 12), (2, 2, 21), (3, 2, 22)],
        'missing_pending': [(9, 1, 10), (3, 1, 12), (9, 2, 20), (2, 2, 21), (3, 2, 22)],
        'approach_cancels_pending': [(2, 1, 9), (9, 1, 10), (3, 1, 12), (9, 2, 20), (2, 2, 21), (3, 2, 22)],
        'recursive_and_readers': [(5, 3, 1), (15, 3, 2), (9, 1, 10), (2, 1, 11), (6, 3, 12),
                                  (3, 1, 13), (4, 1, 14), (8, 1, 15), (7, 1, 16),
                                  (9, 2, 20), (2, 2, 21), (3, 2, 22)],
        'reset': [(9, 1, 10), (2, 1, 11), (3, 1, 12), (12, 3, 15), (13, 3, 16),
                  (9, 2, 20), (2, 2, 21), (3, 2, 22)],
        'retirement': [(9, 1, 10), (2, 1, 11), (3, 1, 12), (14, 3, 15),
                       (9, 2, 20), (2, 2, 21), (3, 2, 22)],
        'same_thread_repeated_context': [(9, 1, 10), (2, 1, 11), (3, 1, 12),
                                         (9, 1, 20), (2, 1, 21), (3, 1, 22)],
    }
    for name, schedule in schedules.items():
        rows = [row(i + 1, *data) for i, data in enumerate(schedule)]
        index = HistoryIndex(rows, qualified=True)
        require(compact(index) == exhaustive(rows), name + ': oracle mismatch')
        require(len(index.export()['event_sequences']) == len(rows), name + ': missing retained event')
        for a in index.calls:
            for b in index.calls:
                value = index.pair(a['acquired']['sequence'], b['acquired']['sequence'])
                require(value['relationship'] in ('DEFINITELY_PRECEDES', 'DEFINITELY_FOLLOWS', 'NOT_COMPARABLE',
                    'OVERLAPS_OR_INDETERMINATE', 'OUTSIDE_QUALIFIED_COVERAGE'), name + ': bad relationship')
        checks.append(name)
    base = [row(i + 1, *data) for i, data in enumerate(schedules['disjoint'])]
    require(HistoryIndex(base, qualified=True).pair(3, 6)['relationship'] == 'DEFINITELY_PRECEDES', 'Disjoint edge lost')
    equal = [row(i + 1, *data) for i, data in enumerate(schedules['equal_ticks'])]
    require(HistoryIndex(equal, qualified=True).pair(5, 6)['relationship'] == 'OVERLAPS_OR_INDETERMINATE', 'Equal ticks ordered')
    require(HistoryIndex(base).pair(3, 6)['relationship'] == 'OUTSIDE_QUALIFIED_COVERAGE', 'Default coverage promoted')
    require(HistoryIndex(base, qualified=True).event_pair(3, 6)['relationship'] == 'NOT_COMPARABLE', 'Cross-thread stamps became HB')
    require(HistoryIndex(base, qualified=True).event_pair(1, 3)['relationship'] == 'DEFINITELY_PRECEDES', 'Program order lost')
    for issue in ('MISSING_OR_DUPLICATE_REGISTRATION', 'UNKNOWN_INITIAL_HOLDERS', 'RECORDER_LOSS_OR_FAILURE',
                  'NO_TERMINAL_ACCOUNTING', 'COUNTER_OVERFLOW', 'INCOMPLETE_PREFIX', 'REGISTRY_GENERATION_UNCERTAINTY'):
        index = HistoryIndex(base, [issue], qualified=True)
        require(compact(index) == exhaustive(base, [issue]), issue + ': legacy drift')
        require(index.pair(3, 6)['relationship'] == 'OUTSIDE_QUALIFIED_COVERAGE', issue + ': unsafe coverage')
        checks.append(issue)
    for field in ('status', 'hazards'):
        changed = [dict(r) for r in base]
        changed[1][field] = 1
        index = HistoryIndex(changed, qualified=True)
        require(compact(index) == exhaustive(changed), field + ': mismatch')
        require(index.pair(3, 6)['relationship'] == 'OUTSIDE_QUALIFIED_COVERAGE', field + ': unsafe coverage')
        checks.append(field)
    # Equal runtime pointers cannot merge distinct observer owner generations.
    for field in ('generation', 'lock'):
        mixed = [dict(r) for r in base]
        mixed[-1][field] += 1
        try:
            HistoryIndex(mixed, qualified=True)
        except ValueError:
            checks.append('reject_mixed_' + field)
        else:
            raise ValueError('Mixed owner identity accepted')
    unrelated = [dict(r, source=999 if r['thread'] == 2 else r['source']) for r in base]
    require(compact(HistoryIndex(unrelated, qualified=True)) == exhaustive(unrelated), 'Other-source writer lost')
    checks.append('unrelated_source_same_lock')
    # Seeded small histories exercise repeated contexts, missing events and ties.
    rng = random.Random(20261104)
    for number in range(150):
        rows = []
        for n in range(rng.randrange(3, 25)):
            rows.append(row(n + 1, rng.choice((2, 3, 4, 5, 6, 7, 8, 9, 12, 13, 14, 15)),
                            rng.randrange(1, 5), rng.randrange(1, 25), status=int(rng.random() < .03)))
        require(compact(HistoryIndex(rows)) == exhaustive(rows), 'Seeded oracle mismatch ' + str(number))
    checks.append('150_seeded_bounded_histories')
    return checks


def actual(path):
    raw = path.read_bytes()
    post = json.loads(raw)
    rows = post['causal']['events']
    legacy_path = Path(__file__).resolve().parents[2] / 'runtime/construction-winner/d5am_read_causal.py'
    spec = importlib.util.spec_from_file_location('d5ap_bounded_legacy_reference', legacy_path)
    legacy = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(legacy)
    groups = {}
    for r in rows:
        groups.setdefault((r['lock'], r['generation']), []).append(r)
    results = []
    for owner, values in groups.items():
        histories = [h for h in post['causal']['histories'] if (h['lock'], h['generation']) == owner]
        require(len(histories) == 1, 'Ambiguous owner history')
        issues = histories[0]['issues']
        tracemalloc.start()
        start = time.perf_counter()
        index = HistoryIndex(values, issues)
        build_seconds = time.perf_counter() - start
        start = time.perf_counter()
        counts = Counter()
        stream = hashlib.sha256()
        total = 0
        for witness in index.iter_legacy():
            counts[witness['interpretation']] += 1
            total += 1
            stream.update(json.dumps(witness, sort_keys=True, separators=(',', ':')).encode('utf8') + b'\n')
        query_seconds = time.perf_counter() - start
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        ordered = sorted(index.calls, key=lambda c: c['acquired']['sequence'])
        # Deterministic small focus includes the accepted target anchor where present.
        anchor = next((n for n, c in enumerate(ordered) if c['acquired']['sequence'] == 2950), len(ordered) // 2)
        selected = ordered[max(0, anchor - 3):anchor + 4]
        contexts = {c['key'] for c in selected}
        focused = [r for r in values if r['kind'] in (12, 13, 14) or
                   tuple(r[k] for k in ('thread', 'invocation', 'selection', 'source')) in contexts]
        require(compact(HistoryIndex(focused, issues)) == exhaustive(focused, issues), 'Actual focused oracle mismatch')
        require(list(HistoryIndex(focused, issues).iter_legacy()) == legacy.registration_windows(focused, issues),
                'Actual original-reader focused mismatch')
        results.append(dict(owner=list(owner), events=len(values), calls=len(index.calls),
                            all_conditional_pairs=total, interpretations=dict(counts),
                            pair_stream_sha256=stream.hexdigest(), build_seconds=build_seconds,
                            all_pair_seconds=query_seconds, traced_peak_bytes=peak,
                            focused_event_count=len(focused), focused_acquisitions=[c['acquired']['sequence'] for c in selected],
                            focused_exhaustive_agreement=True, focused_original_reader_agreement=True))
    return dict(postflight=str(path.resolve()), postflight_sha256=hashlib.sha256(raw).hexdigest(), groups=results,
                original_reader_sha256=hashlib.sha256(legacy_path.read_bytes()).hexdigest(),
                qualification='Analysis agreement only; original raw/authentication checks are separate prerequisites.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--postflight', type=Path)
    parser.add_argument('--out', type=Path)
    args = parser.parse_args()
    result = dict(schema='sor-d5ap-window-controls/1', python=sys.executable, version=sys.version,
                  controls=synthetic(), source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  index_sha256=hashlib.sha256(Path(__file__).with_name('d5ap_windows.py').read_bytes()).hexdigest())
    if args.postflight:
        result['actual'] = actual(args.postflight)
    result['status'] = 'PASS'
    if args.out:
        target = args.out.resolve()
        root = Path(__file__).resolve().parents[2] / '.local-work/d5ap'
        require(target.is_relative_to(root), 'Output must be D5AP-local')
        require(not any(p.is_symlink() or p.is_junction() for p in (target, *target.parents)), 'Reparse output refused')
        for drive in ('C:/', 'D:/'):
            available = ctypes.c_ulonglong()
            require(ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(drive), ctypes.byref(available), None, None)
                    and available.value >= 40_000_000_000, 'Both caller-available disk floors must hold')
        with target.open('x', encoding='utf8', newline='\n') as handle:
            json.dump(result, handle, indent=2)
            handle.write('\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
