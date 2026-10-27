# SPDX-License-Identifier: GPL-3.0-or-later
"""Exercise twelve software probes against pinned disposable Windows processes.

Reads a fresh build and owned SRO1 transport/independent decoder. Writes fresh
local journals, fsynced frames/readback ACKs and reductions. Intentionally
terminates only its sibling fixture in STOP/error cases. No retail route,
network, installs, save/configuration/analysis or Git writes.
"""
import copy
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
from build import ROOT, LOCAL, pin
from reduce import reduce


def load(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT/relative)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


transport = load('d5l_transport', 'research/resource-oracle-retail/collect.py')
decoder = load('d5l_decoder', 'research/resource-tungsten-acquisition/qualify.py')
old_qualification = load('d5l_old_qualification', 'research/resource-source-decisions/qualify.py')


def main():
    build, out = (Path(p).resolve() for p in sys.argv[1:3])
    if not build.is_relative_to(LOCAL) or not out.is_relative_to(LOCAL):
        raise ValueError('Task paths only')
    manifest = json.loads((build/'build.json').read_text())
    assert manifest['exit_code'] == 0
    for p, h in manifest['files'].items():
        assert pin(p) == h, p
    out.mkdir(exist_ok=False)
    results = []
    modes = sys.argv[3:] or ['basic', 'reuse', 'reset', 'owner-aba', 'failed', 'nested', 'concurrent', 'invalid', 'crash', 'stop', 'bad-ack', 'pre-arm-stop', 'step-stop']
    for mode in modes:
        dest = out/mode
        dest.mkdir()
        rows, receipts = [], []
        with (dest/'stderr.txt').open('xb') as stderr, (dest/'events.jsonl').open('x', encoding='utf8', newline='\n') as journal:
            process = subprocess.Popen([str(build/'sor-d5l-controller.exe'), '--synthetic-fixture',
                pin(build/'sor-d5l-fixture.exe'), mode], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=stderr, text=True)
            session = None
            for line in process.stdout:
                r = json.loads(line)
                rows.append(r)
                journal.write(json.dumps(r)+'\n');journal.flush();os.fsync(journal.fileno())
                if r['kind'] == 'SESSION':
                    session = r
                if r['kind'] in ('SAMPLE', 'ARM_BARRIER'):
                    payload = [session, dict(kind='SAMPLE', event=r), dict(kind='END', complete=r.get('read_complete', True))]
                    path = dest/f'capture-{len(receipts):05d}.bin'
                    ack = transport.persist(path, payload, synthetic=True)
                    assert decoder.independent(path) == payload
                    receipts.append(dict(path=str(path), **ack))
                    answer = 'ARM_ACK' if r['kind'] == 'ARM_BARRIER' else f'ACK {r["capture"]}'
                    if mode == 'pre-arm-stop' and r['kind'] == 'ARM_BARRIER':
                        answer = 'STOP'
                    if mode == 'stop' and r.get('capture') == 6:
                        answer += ' STOP'
                    if mode == 'bad-ack' and r['kind'] == 'SAMPLE':
                        answer = 'REJECT'
                    process.stdin.write(answer+'\n');process.stdin.flush()
            code = process.wait(timeout=15)
        reduction = reduce(rows)
        checks = {}
        checks['target_absent'] = bool(session and old_qualification.target_absent(session['pid']))
        checks['expected_exit'] = code == (2 if mode == 'bad-ack' else 0)
        if mode not in ('bad-ack', 'pre-arm-stop', 'stop', 'step-stop'):
            checks['first_chain'] = bool(reduction['chains'])
            checks['bypass_distinct'] = any(c['decision'] == 'VISITED_BYPASS' and c['qualified'] for c in reduction['decisions'])
        if mode in ('reuse', 'reset', 'owner-aba'):
            checks['two_masks'] = [c['mask'] for c in reduction['chains']] == [0, 3]
            checks['different_lifetimes'] = len({tuple(c['lifetime']) for c in reduction['chains']}) == 2
        if mode == 'failed':
            checks['incomplete_not_promoted'] = any(c['decision'] == 'MISS' and not c['qualified'] for c in reduction['decisions']) and len(reduction['chains']) == 1
        if mode == 'concurrent':
            checks['all_requests'] = len(reduction['decisions']) == 16
        if mode in ('stop', 'pre-arm-stop', 'bad-ack', 'step-stop'):
            stopped = next((i for i,r in enumerate(rows) if r['kind'] == 'STOP_COMMITTED'), None)
            checks['monotonic_stop'] = stopped is not None and not any(r['kind'] == 'SAMPLE' for r in rows[stopped+1:])
        if mode == 'invalid':
            checks['bad_read_gap'] = any(r['reason'] == 'coverage_or_read' for r in reduction['rejected'])
        if mode == 'basic':
            for label, change in [('missing', lambda r:r.pop(next(i for i,x in enumerate(r) if x.get('site') == 8))),
                                  ('sequence', lambda r:next(x for x in r if x['kind'] == 'SAMPLE').update(capture=999))]:
                changed = copy.deepcopy(rows)
                try:
                    change(changed)
                    checks['reject_'+label] = not reduce(changed)['chains']
                except StopIteration:
                    checks['reject_'+label] = False
            raw = bytearray(Path(receipts[0]['path']).read_bytes());raw[len(raw)//2] ^= 1
            path = dest/'corrupt.bin';path.write_bytes(raw)
            try:
                decoder.independent(path)
                checks['corrupt_rejected'] = False
            except (ValueError, AssertionError, RuntimeError, UnicodeError):
                checks['corrupt_rejected'] = True
        transport.write(dest/'reduction.json', reduction)
        transport.write(dest/'receipts.json', receipts)
        result = dict(mode=mode, code=code, captures=len(receipts), checks=checks, passed=all(checks.values()))
        results.append(result)
        transport.write(dest/'result.json', result)
        print(json.dumps(result), flush=True)
    transport.write(out/'results.json', results)
    return 0 if all(r['passed'] for r in results) else 1


if __name__ == '__main__':
    raise SystemExit(main())
