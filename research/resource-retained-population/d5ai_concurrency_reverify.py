# SPDX-License-Identifier: GPL-3.0-or-later
"""Requalify frozen native concurrency files using the revised pinned receiver.

Reads only preserved native raw02, its immutable run receipt and current receiver
methods. Writes fresh ignored analysis and normalized journal files. No native
producer executes again; no original bytes, clocks or counters are rewritten.
Same-thread typed phase/sequence proof may admit intra-call clock ties; target
boundary ties and active snapshot markers remain refused by the pinned receiver.
No game, process, save, deployment, network or publication action.
"""
from pathlib import Path
import json
import sys

from d5ai_concurrency_qualify import ROOT, verify_case
from common import guard, fresh, sha, inventory
from d5ai_read_lifetime import read_prefix
from d5ai_read_geometry import decode
from d5ai_operations import worker_json


def main():
    raw, out = (Path(p).resolve() for p in sys.argv[1:3])
    if raw != ROOT / '.local-work/d5ai-recorder/concurrency02' or not out.is_relative_to(ROOT / '.local-work/d5ai-recorder'):
        raise ValueError('Exact preserved raw02 and fresh task-local output required')
    guard()
    out.mkdir(exist_ok=False)
    before = inventory(raw)
    original = json.loads((raw / 'qualification.json').read_bytes())
    assert original['status'] == 'PASS' and original['actual_observer_kind'].startswith('Standalone EXE')
    methods = [Path(__file__), Path(__file__).with_name('d5ai_concurrency_qualify.py'),
               ROOT / 'runtime/construction-winner/d5ai_read_lifetime.py',
               ROOT / 'runtime/construction-winner/d5ai_read_geometry.py',
               ROOT / 'runtime/construction-winner/read_capture.py',
               Path(__file__).with_name('d5ai_operations.py'), Path(__file__).with_name('d5ai_episode.py')]
    pins = {str(path): sha(path) for path in methods}
    cases = []
    for mode in ('normal', 'short', 'held', 'overload'):
        verified = verify_case(raw / mode, accept_intra_call_ties=True)
        row = dict(mode=mode, verification=verified)
        if mode != 'overload':
            session = raw / mode / 'session'
            terminal = worker_json(session / 'terminal.json')
            journal = read_prefix(session, terminal)
            journal_path = out / (mode + '-journal.json')
            fresh(journal_path, journal)
            first = decode((session / 'geometry-1.bin').read_bytes())
            last = decode((session / 'geometry-33.bin').read_bytes())
            geometry_path = out / (mode + '-boundary-snapshots.json')
            fresh(geometry_path, dict(first=first, last=last, scope='Supplied immutable geometry; marker/transport test, no construction/frame certificate'))
            row.update(journal_path=str(journal_path), journal_sha256=sha(journal_path),
                       boundary_snapshots_path=str(geometry_path), boundary_snapshots_sha256=sha(geometry_path))
        cases.append(row)
    assert inventory(raw) == before
    assert all(sha(path) == digest for path, digest in pins.items())
    value = dict(schema='sor-d5ai-concurrency-receiver-qualification/1', status='PASS', cases=cases, method_pins=pins,
                 native_run_receipt_sha256=sha(raw / 'qualification.json'), actual_probe_executable_sha256=original['executable_sha256'],
                 source_matched_to_candidate16_sha256=original['source_matched_to_candidate16_sha256'],
                 native_executed_again=False, raw_preserved=True,
                 scope='Receiver-only qualification of actual standalone EXE native files; retained worker plus source-matched compiled producer, not executed candidate DLL16')
    fresh(out / 'qualification.json', value)
    print(json.dumps(dict(status='PASS', cases=len(cases), actual_short_ties=cases[1]['verification']['intra_call_QPC_ties'], native_executed_again=False)))


if __name__ == '__main__':
    main()
