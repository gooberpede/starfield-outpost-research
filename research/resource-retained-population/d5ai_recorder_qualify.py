# SPDX-License-Identifier: GPL-3.0-or-later
"""Independently inspect exact native recorder outputs and adversarial readers.

Reads the specified disposable build, native host oracles and retained D5AH
geometry. Writes a new ignored qualification directory and altered byte controls.
Uses only owned readers and stdlib; no target, save, deployment, network or Git
operation. Refuses a failed native build or missing expected case. Earlier failed
builds remain untouched. This validates finite host behavior, never retail safety.
"""
from pathlib import Path
import copy
import hashlib
import importlib.util
import json
import struct
import sys

ROOT = Path(__file__).resolve().parents[2]
RUNTIME = ROOT / 'runtime/construction-winner'
sys.path.insert(0, str(RUNTIME))
from d5ai_read_geometry import decode, read_session
from d5ai_read_lifetime import read_prefix


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    build, output = (Path(p).resolve() for p in sys.argv[1:3])
    if not output.is_relative_to(ROOT / '.local-work/d5ai-recorder'):
        raise ValueError('Task-local output required')
    output.mkdir(exist_ok=False)
    receipt = json.loads((build / 'build.json').read_bytes())
    if not receipt['compilation']['pass_exit'] or not all(c['pass_exit'] for c in receipt['cases']):
        raise ValueError('Native build has failed cases')
    results = []
    sessions = {}
    status = {'d5ai-normal': [0], 'd5ai-empty': [0], 'd5ai-read-fault': [1],
              'd5ai-malformed': [2], 'd5ai-arena-full': [3], 'd5ai-overflow': [0, 0, 0, 0],
              'd5ai-retire-during': [4, 0], 'd5ai-concurrent': [0], 'd5ai-interrupted': [4],
              'd5ai-exclusive': [5], 'd5ai-stale-arm': [0], 'd5ai-held-worker': [0],
              'd5ai-consumer-partial': [7], 'd5ai-unfinished': [6], 'd5ai-stop-during': [6],
              'd5ai-last-false': [7], 'd5ai-missing-preunlock': [7],
              'd5ai-retained': [0, 0], 'd5ai-rebuilt-equal': [0, 0],
              'd5ai-rebuilt-different': [0, 0], 'd5ai-unavailable': [0, 0],
              'd5ai-native-mask0': [0], 'd5ai-native-mask3a': [0], 'd5ai-native-mask3b': [0],
              'd5ai-worker-exit': [0], 'd5ai-process-exit': [], 'd5ai-file-arm': [0],
              'd5ai-foreign-arm': []}
    status['d5ai-stop-admission'] = []
    status.update({'d5ai-context-late-zero': [0, 0], 'd5ai-context-mid-gap': [0, 4],
                   'd5ai-context-owner-change': [0, 0], 'd5ai-context-clean': [0, 0]})
    status.update({'d5ai-life-'+name:[0,0] for name in 'external-holder external-collection final partial aba mutation empty-null empty-spare stalled stop'.split()})
    status['d5ai-life-stop-admitted']=[0]
    offered = {c['case'] for c in receipt['cases']}
    if not set(status).issubset(offered):
        raise ValueError('Missing mandatory D5AI native cases')
    for case in sorted(offered):
        if not case.startswith('d5ai-'):
            continue
        session = build / case
        if not (session / 'identity.json').exists():
            continue
        result = read_session(session)
        sessions[case] = result
        (output / (case + '.json')).write_text(json.dumps(result, indent=2) + '\n', encoding='utf8', newline='\n')
        if case in status:
            actual = [s['header']['status'] for s in result['snapshots']]
            if result['errors'] or actual != status[case]:
                raise ValueError((case, result['errors'], actual, status[case]))
            results.append(dict(case=case, check='native expected snapshot status', statuses=actual, passed=True))
        elif case in ('d5ai-write-fault', 'd5ai-flush-fault', 'd5ai-receipt-fault'):
            if any(s['complete_representation'] for s in result['snapshots']) or (not result['errors'] and (result['snapshots'] or json.loads((session/'terminal.json').read_bytes()).get('failed') is not True)):
                raise ValueError('Output fault became valid geometry: ' + case)
            results.append(dict(case=case, check='unacknowledged geometry refused', passed=True))
        if case.startswith('d5ai-'):
            def worker_pairs(items):
                value = {}
                for key, item in items:
                    if key in value and not (key == 'qpc_frequency' and type(item) is int and value[key] == item):
                        raise ValueError('Duplicate new worker JSON key: ' + key)
                    value[key] = item
                return value
            for path in [session / 'identity.json', session / 'ready.json', session / 'terminal.json', *session.glob('ack-*.json')]:
                if path.exists():
                    json.loads(path.read_bytes(), object_pairs_hook=worker_pairs)
            if (session / 'flush.jsonl').exists():
                for line in (session / 'flush.jsonl').read_bytes().splitlines():
                    json.loads(line, object_pairs_hook=worker_pairs)
            results.append(dict(case=case, check='new worker JSON keys unique; identical historical QPC duplicate only', passed=True))
            terminal = session / 'terminal.json'
            if case in ('d5ai-worker-exit', 'd5ai-process-exit'):
                if terminal.exists():
                    raise ValueError('Unexpected terminal after declared exit: ' + case)
            elif not terminal.exists():
                raise ValueError('Missing expected native terminal: ' + case)
    for case in sorted(offered):
        if not case.startswith('d5ai-life-'):
            continue
        session=build/case
        terminal=json.loads((session/'terminal.json').read_bytes())
        expected_fault=case in ('d5ai-life-overflow','d5ai-life-write-fault','d5ai-life-flush-fault','d5ai-life-ack-fault') or case.startswith('d5ai-life-counter-')
        try:
            journal=read_prefix(session,terminal)
        except ValueError:
            if not expected_fault:raise
            results.append(dict(case=case,check='actual native journal fault cannot authenticate a complete prefix',passed=True))
        else:
            if expected_fault:raise ValueError('Fault became complete ending history: '+case)
            assert journal['complete'] and journal['loss']==0
            results.append(dict(case=case,check='actual native ending frames and durable coverage authenticate',records=journal['records'],passed=True))
        if case.startswith('d5ai-life-counter-'):
            assert terminal['lifetime_counter_overflow'] and terminal['lifetime_failed']
        if case=='d5ai-life-stop':
            assert terminal['lifetime_unlogged_cutoff_ticks']>terminal['lifetime_qualified_through_ticks']
        if case=='d5ai-life-stop-admitted':
            assert terminal['lifetime_enqueued']==terminal['lifetime_acknowledged']==2
    ordinary = sessions['d5ai-normal']['snapshots'][0]
    assert ordinary['holders'][0]['resources'][0]['regions'][0]['points'] == '0000803f0000004000004040000080400000a0400000c0400000e04000000041'
    held = sessions['d5ai-held-worker']['snapshots'][0]
    assert held['holders'] == ordinary['holders'] or held['holders'][0]['resources'][0]['regions'] == ordinary['holders'][0]['resources'][0]['regions']
    # Independent expected native geometry is read separately from the C++ fixture
    # input generator and the native recorder decoder.
    reference_path = ROOT / '.local-work/d5ah/geometry01/control.json'
    reference = json.loads(reference_path.read_bytes())
    for index, case in enumerate(('d5ai-native-mask0', 'd5ai-native-mask3a', 'd5ai-native-mask3b')):
        observed = sessions[case]['snapshots'][0]['holders'][0]['resources']
        actual = [(r['resource'], r['regions']) for r in observed]
        expected = [(r['resource'], r['regions']) for r in reference['runs'][index]['population']]
        assert sorted(actual) == sorted(expected), case
        results.append(dict(case=case, check='every native resource, region header and point agrees with independent retained oracle', passed=True))
    baseline = (build / 'd5ai-normal/geometry-1.bin').read_bytes()
    controls = {}

    def refuse(label, raw):
        try:
            decode(raw)
        except ValueError:
            controls[label] = True
        else:
            raise ValueError('Reader accepted adversary: ' + label)

    refuse('truncated-header', baseline[:100])
    refuse('truncated-point', baseline[:-1])
    impossible_occupancy = bytearray(baseline)
    for offset in (88, 232, 240):
        struct.pack_into('<Q', impossible_occupancy, offset, 0)
    refuse('one-holder-exceeds-zero-map-capacity', impossible_occupancy)
    # Re-signing the modeled receipt bypasses only the outer SHA check. The
    # independently decoded occupancy invariant must still reject these bytes.
    resigned = output / 'resigned-impossible-occupancy'
    resigned.mkdir()
    (resigned / 'identity.json').write_bytes((build / 'd5ai-normal/identity.json').read_bytes())
    (resigned / 'geometry-1.bin').write_bytes(impossible_occupancy)
    receipt = json.loads((build / 'd5ai-normal/geometry-1.json').read_bytes())
    receipt.update(sha256=hashlib.sha256(impossible_occupancy).hexdigest(), bytes=len(impossible_occupancy))
    (resigned / 'geometry-1.json').write_text(json.dumps(receipt) + '\n', encoding='utf8', newline='\n')
    rejected = read_session(resigned)
    assert rejected['errors'] and not any(s['complete_representation'] for s in rejected['snapshots'])
    controls['resigned-session-impossible-occupancy-refused'] = True
    for label, offset, value in [('wrong-version', 8, 3), ('false-payload-size', 16 * 8, 1),
                                 ('wrong-region-census', 14 * 8, 0), ('duplicate-holder-census', 12 * 8, 2),
                                 ('false-completion-epoch', 208 + 8, 0), ('early-consumer-iterator', 208 + 3 * 8, 0)]:
        changed = bytearray(baseline)
        struct.pack_into('<Q', changed, offset, value)
        refuse(label, changed)
    # The pre-release callback result is independently witnessed. Full iterator
    # equality cannot rescue a false last callback or missing pre-unlock event.
    for word in (0, 2, 0xffffffff):
        changed = bytearray(baseline)
        struct.pack_into('<Q', changed, 208 + 5 * 8, word)
        refuse('false-preunlock-result-' + str(word), changed)
    changed = bytearray(baseline)
    struct.pack_into('<I', changed, 324, 0)
    refuse('missing-preunlock-witness', changed)
    assert not any(s['complete_representation'] for s in sessions['d5ai-consumer-partial']['snapshots'])
    controls['actual-compiled-early-consumer-refused'] = True
    # Direct JSON mutation is not source evidence: the raw flush receipt must
    # match the exact payload, identity, request and status before decode.
    tampered = output / 'tampered-session'
    tampered.mkdir()
    for name in ('identity.json', 'geometry-1.bin', 'geometry-1.json'):
        (tampered / name).write_bytes((build / 'd5ai-normal' / name).read_bytes())
    altered = bytearray((tampered / 'geometry-1.bin').read_bytes())
    altered[-1] ^= 1
    (tampered / 'geometry-1.bin').write_bytes(altered)
    assert read_session(tampered)['errors']
    controls['raw-byte-tamper-refused-before-semantic-decode'] = True
    result = dict(schema='sor-d5ai-native-qualification/1', build_sha256=sha(build / 'build.json'),
                  reader_sha256=sha(RUNTIME / 'd5ai_read_geometry.py'), method_sha256=sha(__file__),
                  reference_sha256=sha(reference_path), native=results, reader_controls=controls,
                  scope='Actual compiled derivative observer, worker and bridge behavior in finite owned hosts; engine policies and geometry inputs supplied',
                  status='PASS')
    (output / 'qualification.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf8', newline='\n')
    print(json.dumps(dict(native_checks=len(results), reader_controls=len(controls), status='PASS')))


if __name__ == '__main__':
    main()
