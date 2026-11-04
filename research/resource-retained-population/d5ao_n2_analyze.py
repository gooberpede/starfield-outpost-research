# SPDX-License-Identifier: GPL-3.0-or-later
"""Index a stopped, separately reviewed N2 postflight for focused evidence.

Reads the exact supplied receipt and raw core using owned decoder under
SOR-P-0002; writes one fresh local JSON. Stdlib only. No target, protected-file,
deployment or network actions. Does not authenticate qualification facts,
establish a universal cohort, evaluate a forecast or totally order atomics.
All-history pairwise witnesses remain explicitly UNCOMPUTED.
"""
import os
import sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):
    raise RuntimeError('Use pinned Python -E -B without optimization')

import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import d5ao_n2_operations as operations


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--postflight', type=Path, required=True)
    parser.add_argument('--sha256', required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    operations.guard()
    post = operations.original.pinned_json(args.postflight, args.sha256)
    operations.require(post['trial'] == 'N2' and post['process_state'] == 'EXITED', 'Stopped N2 required')
    operations.require(post['status'] == 'PASS_POSTFLIGHT', 'Separate partial analysis required on failure')
    import read_capture as core
    session = Path(post['session'])
    raw = (session / 'events.bin').read_bytes()
    operations.require(hashlib.sha256(raw).hexdigest() == post['scientific']['raw_sha256'], 'Core changed')
    events = [core.decode(raw[i + 16:i + 328]) for i in range(0, len(raw), 328)]
    births = {}
    target = []
    for row in events:
        if row['kind'] == 14:
            births[row['source']] = row
        elif row['source'] in births and core.source_key(births[row['source']]) == core.TARGET:
            target.append((births[row['source']]['selection'], row))
    constructors = [row for row in post['joins']['observations'] if row['source_key'] == core.TARGET]
    operations.require(len(constructors) == 1, 'Single target construction assumption refused')
    constructor = constructors[0]
    allocation = constructor['source_allocation']
    rows = [row for birth, row in target if birth == allocation]
    selected = [row for row in rows if row['kind'] == 2]
    invocations = {row['invocation'] for row in selected}
    scheduler = post['scheduler']['events']
    providers = [row for row in scheduler if row['kind'] == 9 and row['core_invocation'] in invocations]
    provider_index = defaultdict(list)
    for row in providers:
        provider_index[row['core_invocation']].append(row)
    operations.require(all(len(provider_index[i]) == 1 for i in invocations), 'Ambiguous target provider')
    keys = {(row['node'], row['allocation']) for row in providers}
    task_index = defaultdict(list)
    for row in scheduler:
        key = (row['node'], row['allocation'])
        if key in keys:
            task_index[key].append(row)
    missing = [dict(node=key[0], allocation=key[1], missing=sorted(set(range(1, 13)) - {row['kind'] for row in values}))
               for key, values in task_index.items() if set(range(1, 13)) - {row['kind'] for row in values}]
    winner = [row for row in providers if row['core_invocation'] == constructor['invocation']]
    operations.require(len(winner) == 1, 'Ambiguous winner task')
    winner_key = (winner[0]['node'], winner[0]['allocation'])
    causal = post['causal']['events']
    focus = [row for row in causal if row['invocation'] == constructor['invocation'] and row['selection'] == constructor['selection']]
    operations.require(bool(focus), 'Missing constructor causal scope')
    result = dict(schema='sor-d5ao-n2-focused-analysis/1', postflight_sha256=args.sha256,
        method_sha256=digest(__file__), core_sha256=hashlib.sha256(raw).hexdigest(),
        constructor=constructor, target_core_kinds=dict(Counter(row['kind'] for row in rows)),
        target_selections=len(selected), provider_count=len(providers), task_allocations=len(keys),
        family_counts=dict(Counter(row['family'] for row in providers)), missing_task_stages=missing,
        target_task_history_issues=[h for h in post['scheduler']['histories'] if (h['node'], h['allocation']) in keys and h['issues']],
        winner_task=task_index[winner_key], constructor_causal=focus,
        local_owner_evidence=[row for row in causal if 2910 <= row['sequence'] <= 2965],
        owner_kind_counts=dict(Counter(row['kind'] for row in causal)),
        source_lifetime_target_chains=[dict(allocation=birth, sequence=row['sequence'], kind=row['kind'])
            for birth, row in target if row['kind'] in (4, 7, 17)],
        limit='Recorded stage census and focused operands only; all-history pairwise witnesses UNCOMPUTED. Separate native/source/participant review required.')
    out = args.out.resolve()
    operations.require(out.is_relative_to(operations.ROOT / '.local-work/d5ao'), 'Local fresh output required')
    operations.require(not any(p.is_symlink() or p.is_junction() for p in (out, *out.parents)), 'No reparse output')
    operations.fresh(out, result)
    print(json.dumps({k: result[k] for k in ('target_selections', 'provider_count', 'task_allocations', 'family_counts', 'missing_task_stages')}))


if __name__ == '__main__':
    main()
