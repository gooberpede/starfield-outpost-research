# SPDX-License-Identifier: GPL-3.0-or-later
"""Authenticate completed D5O receipts and assert exit-race coverage operands.

Reads frozen qualification journals and owned independent binders. Writes fresh
ignored checks and deliberately damaged evidence copies through check_hybrid.
No target execution, original changes, dependencies, network or Git writes.
This post-capture verifier is pinned separately from the compiled build.
"""
import json
from collections import Counter
from pathlib import Path
import sys
import check_hybrid
from qualify_coverage_hybrid import MODES, validate


def lifecycle(folder):
    def rows(name):
        return [json.loads(s) for s in (folder/name).read_text(encoding='utf8').splitlines()]
    control, events = rows('control.jsonl'), rows('events.jsonl')
    resets = [r for r in events if r['kind']=='SAMPLE' and r.get('site')==7]
    assert len(resets)==32
    # Auxiliary Windows threads may also appear. The fixture's 96 waiters share
    # one entry address and precede the final Reset; two later callers use it too.
    registered = [r for r in control if r['action']=='THREAD_REGISTER']
    last_reset = max(r['debug_event_sequence'] for r in control if r['action']=='TRAP_CONTEXT' and r['site']==7)
    before_reset = [r for r in registered if r['debug_event_sequence']<last_reset]
    starts = Counter(r['start'] for r in before_reset)
    worker_start, count = starts.most_common(1)[0]
    assert count==96 and sum(r['start']==worker_start for r in registered)==98
    worker_lifetimes = {r['thread_lifetime'] for r in before_reset if r['start']==worker_start}
    assert len(worker_lifetimes)==96
    exited = {r['thread_lifetime'] for r in events if r['kind']=='THREAD_EXIT'}
    assert worker_lifetimes <= exited
    denied = [r for r in control if r['action']=='PEER_SUSPEND_RESULT' and r['error']==5]
    assert denied
    for row in denied:
        assert row['peer_lifetime'] in worker_lifetimes and row['prior_count']==0xffffffff
        state = next(r for r in control if r['sequence']==row['sequence']+1)
        assert state['action']=='PEER_STATE' and state['phase']=='suspend'
        assert state['peer_lifetime']==row['peer_lifetime'] and state['wait']==258 and state['error']==0
        event = row['debug_event_sequence']
        batch = [r for r in control if r['debug_event_sequence']==event]
        assert any(r['action']=='TRAP_CONTEXT' and r['site']==7 for r in batch)
        assert any(r['kind']=='DEFERRED_TRAP' and r['tid']==row['tid'] for r in events)
        assert not any(r['action'] in ('PATCH_INTENT','SITES_VERIFIED','STEP_PREPARED') for r in batch)
        assert any(r['action']=='EVENT_RECEIVED' and r['event']==4 and
                   r['thread_lifetime']==row['peer_lifetime'] and r['sequence']>row['sequence'] for r in control)
    assert not any(r['action'] in ('CONTROLLER_FATAL','COVERAGE_EXITED') for r in control)
    assert json.loads((folder/'reduction.json').read_text())['chains']
    return dict(reset_samples=32,exited_worker_lifetimes=96,actual_denied_suspend=len(denied),passed=True)


def main():
    folder, output = map(Path, sys.argv[1:])
    results = json.loads((folder/'results.json').read_text())
    assert {r['mode'] for r in results}==set(MODES) and len(results)==len(MODES)
    assert all(r['passed'] for r in results)
    fields = [validate(folder/mode) for mode in MODES]
    race = lifecycle(folder/'coverage-exit-race')
    exit_control = [json.loads(s) for s in (folder/'coverage-exit/control.jsonl').read_text().splitlines()]
    codes = [r for r in exit_control if r['action']=='PEER_EXIT_CODE']
    assert {0,259} <= {r['exit_code'] for r in codes if r['ok'] and r['error']==0}
    check_hybrid.main()
    (output/'coverage-checks.json').write_text(json.dumps(dict(fields=fields,exit_race=race,
        actual_exit_codes=sorted({r['exit_code'] for r in codes}),passed=True),indent=2)+'\n',encoding='utf8',newline='\n')
    print('Exact coverage operands, exit race and all receipt/ACK controls PASS')


if __name__ == '__main__':
    main()
