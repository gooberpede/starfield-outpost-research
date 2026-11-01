# SPDX-License-Identifier: GPL-3.0-or-later
"""Compare compiled P3 host actions with capture records and consumer verdicts.

Reads completed disposable build captures, the host's independently recorded
actions/state and exact packaged consumers. Writes a fresh ignored receipt and
source snapshot only. Uses stdlib; no process, game, save, network or Git effect.
Host geometry is emulated and never inferred from a sampled mask. Adapted from
the maintainer-owned P1 qualification receipt/consumer-loading method.
"""
import collections
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[2]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    build, out = ((ROOT / p).resolve() for p in sys.argv[1:3])
    assert build.is_relative_to(ROOT / '.local-work/d5x')
    assert out.is_relative_to(ROOT / '.local-work/d5ab')
    assert min(shutil.disk_usage(p).free for p in ('C:/', 'D:/')) >= 40_000_000_000
    out.mkdir(parents=True, exist_ok=False)
    (out / 'source.py').write_bytes(Path(__file__).read_bytes())
    source = build / 'package-runtime'
    spec = importlib.util.spec_from_file_location('p3_native_reader', source / 'read_capture.py')
    reader = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(reader)
    manifest = json.loads((build / 'build.json').read_bytes())
    development = '--development' in sys.argv[3:]
    assert manifest['compilation']['pass_exit'] and (manifest['source_unchanged'] or development)
    assert all(sha(build / p) == digest for p, digest in manifest['outputs'].items())
    inputs = {str(source / name): sha(source / name) for name in
              ('SorConstructionWinner.dll', 'read_capture.py', 'reduce_v3.py', 'reduce_v4.py', 'controller.py')}
    rows = []

    def record(case, passed, **details):
        row = dict(case=case, passed=bool(passed), **details)
        rows.append(row)
        with (out / 'progress.jsonl').open('a', encoding='utf8', newline='\n') as stream:
            stream.write(json.dumps(row) + '\n')
            stream.flush()

    # This table specifies expected native outcomes before examining capture data.
    expected_chains = {
        'p3-positive-no-bypass': 1, 'p3-positive-bypass': 1,
        'p3-empty-output': 1, 'p3-partial-output': 1,
        'p3-generator-throw': 0, 'p3-reserve-throw': 0,
        'p3-reserve-fail': 0, 'p3-skipped-store': 0,
        'p3-retire-before-store': 0, 'p3-reset-before-generate': 0,
        'p3-prerequisite-failure': 0, 'p3-map-hit': 0,
        'p3-density-reuse': 0, 'p3-real-reuse': 1,
        'p3-competing-map': 0, 'p3-detached-retirement': 0,
        'p3-loss-recovery': 0, 'p3-loss-after-reset': 0, 'p3-loss-unknown-bounds': 0,
        'p3-token-collision': 0, 'p3-same-geography-other-owner': 1,
        'p3-owner-replacement-selected': 0,
    }
    required_cases = set(expected_chains) | {'p3-unwind-probe', 'p3-store-access-fault'}
    assert required_cases <= {row['case'] for row in manifest['cases']}
    probe = build / 'p3-unwind-probe/unwind-probe.json'
    assert probe.is_file()
    if probe.exists():
        unwind = json.loads(probe.read_bytes())
        cases = collections.Counter(row['case'] for row in unwind)
        expected = {'original-provider': 1, 'selected-bridge': 1, 'visited-bridge': 1,
                    'birth-bridge': 1, 'published-bridge': 1, 'stored-bridge': 1,
                    'bridge-instruction-boundary': 214, 'erase-trampoline-boundary': 6}
        record('unwind-all-declared-boundaries', cases == expected and len(unwind) == 226 and
               all(row['correct'] and row['actual_RtlVirtualUnwind'] for row in unwind),
               boundaries=len(unwind), receipt_sha256=sha(probe))
    fault = build / 'p3-store-access-fault'
    assert (fault / 'host-oracle-before-store.jsonl').is_file()
    if fault.exists():
        independent = [json.loads(line) for line in (fault / 'host-oracle-before-store.jsonl').read_text().splitlines()]
        raw = (fault / 'events.bin').read_bytes()
        events = [reader.decode(raw[i+16:i+328]) for i in range(0, len(raw), 328)]
        result = reader.inspect(fault, inputs[str(source / 'SorConstructionWinner.dll')])
        native = next(row for row in manifest['cases'] if row['case'] == 'p3-store-access-fault')
        record('actual-native-store-access-fault', native['actual'] == native['expected'] == 0xc0000005 and
               any(row['operation'] == 'store-destination-inaccessible' for row in independent) and
               any(e['kind'] == 16 and e['a'] != 0xffffffff for e in events) and
               not any(e['kind'] == 17 for e in events) and not result['complete_session'] and not result['chains'],
               scope='Unhandled MOV access violation in disposable host; admitted pre-store prefix survives.',
               admitted_records=result['durable_records'])
    for name, expected in expected_chains.items():
        session = build / name
        actions = [json.loads(line) for line in (session / 'host-oracle.jsonl').read_text().splitlines()]
        state = json.loads((session / 'host-state.json').read_bytes())
        counts = collections.Counter(row['operation'] for row in actions)
        raw = (session / 'events.bin').read_bytes()
        assert len(raw) % 328 == 0
        events = [reader.decode(raw[i+16:i+328]) for i in range(0, len(raw), 328)]
        kinds = collections.Counter(e['kind'] for e in events)
        correspondence = {
            1: counts['provider-begin'], 9: counts['provider-begin'],
            2: counts['selected-native'], 3: counts['visited-native'],
            5: counts['descriptor-consumed'],
            12: counts['native-empty-reset'],
            14: counts['constructor-begin'], 15: counts['publication-store'],
            4: counts['protected-map'], 6: counts['generator-begin'],
            7: counts['ordinary-sample'],
            8: counts['generator-output'] + counts['generator-throw'],
            16: counts['reserve-success'] + counts['reserve-failed'] + counts['reserve-throw'],
            17: counts['visited-store'],
        }
        record(name + '-native-boundaries', all(kinds[k] == n for k, n in correspondence.items()),
               expected=correspondence, actual={k: kinds[k] for k in correspondence},
               oracle_sha256=sha(session / 'host-oracle.jsonl'))
        for action, kind in (('publication-store', 15), ('visited-store', 17), ('protected-map', 4),
                             ('selected-native', 2), ('visited-native', 3),
                             ('descriptor-consumed', 5), ('generator-begin', 6),
                             ('ordinary-sample', 7), ('native-empty-reset', 12)):
            host = [row for row in actions if row['operation'] == action]
            observed = [e for e in events if e['kind'] == kind]
            def key(row, native=False):
                result = (row['thread'],) if kind == 12 else (row['source'], row['thread'])
                if kind == 12:
                    result += (row['proc'],)
                elif kind != 15:
                    result += (row['proc'], tuple(row['request'] if native else row['query']))
                if kind == 17:
                    result += (row['a'], row['b'])
                if kind == 4:
                    result += (row['a'],)
                if kind == 3:
                    result += (row['a'], row['b'])
                if kind == 5:
                    result += (row['b'] if native else row['a'], row['c'] if native else row['b'])
                if kind == 6:
                    result += tuple(row[field] for field in ('a', 'b', 'c', 'd'))
                if kind == 7:
                    result += (row['a'], row['c'] if native else row['b'])
                if kind == 12:
                    result += (row['a'], row['b'])
                return result
            record(name + '-' + action + '-operands',
                   sorted(key(row) for row in host) == sorted(key(row, True) for row in observed))
        result = reader.inspect(session, inputs[str(source / 'SorConstructionWinner.dll')])
        record(name + '-reducer', len(result['chains']) == expected and result['complete_session'],
               expected_chains=expected, actual_chains=len(result['chains']),
               diagnostics=result['diagnostics'], state=state,
               source_qualified_identities=len(result['identities']))
        if name == 'p3-positive-bypass':
            record(name + '-membership', counts['visited-membership'] == 1 and
                   any(e['kind'] == 3 and e['a'] == 1 for e in events) and
                   bool(result['chains']) and result['chains'][0]['later_bypass'])
        if name == 'p3-density-reuse':
            record(name + '-no-provider', counts['density-aggregate-reuse-without-provider'] == 1 and
                   all(kinds[kind] == 0 for kind in (1, 2, 3, 4, 6, 7, 17)))
        if name == 'p3-owner-replacement-selected':
            replacement = [row for row in actions if row['operation'] == 'owner-component-replacement']
            record(name + '-installed-owner-readback', len(replacement) == 1 and
                   replacement[0]['a'] != replacement[0]['b'] and
                   state['installed_owner'] == replacement[0]['a'] and
                   all(e['proc'] == replacement[0]['b'] for e in events if e['kind'] == 1) and
                   any(e['kind'] == 4 and e['status'] & 8 for e in events) and not result['chains'],
                   scope='Actual host manager slot replacement; old request object retained; engine routine emulated.')
        if name in ('p3-empty-output', 'p3-partial-output'):
            geometry = 0 if name == 'p3-empty-output' else 1
            record(name + '-geometry-distinction', state['geometry_units'] == geometry and
                   kinds[7] == 1 and kinds[17] == 1,
                   scope='Emulated host output; sample/store alone does not establish retail geometry.')
        if name in ('p3-generator-throw', 'p3-reserve-throw'):
            record(name + '-unwind', counts['exception-caught'] == counts['unwind-state-restored'] == 1 and
                   any(e['kind'] == 9 and e['status'] & 16 for e in events) and kinds[17] == 0)
        if name == 'p3-competing-map':
            outcomes = [row['a'] for row in actions if row['operation'] == 'protected-map']
            record(name + '-winner-waiting-hits', outcomes.count(8) == 1 and outcomes.count(2) == 3 and
                   kinds[3] == 4 and len({tuple(row['query']) for row in actions if row['operation'] == 'provider-begin'}) == 4)
        if name == 'p3-real-reuse':
            freed = [row for row in actions if row['operation'] == 'allocation-free']
            reused = [row for row in actions if row['operation'] == 'allocation-reused']
            record(name + '-real-allocation', len(freed) == len(reused) == 1 and
                   freed[0]['source'] == reused[0]['source'] and
                   freed[0]['host_allocation'] != reused[0]['host_allocation'])
        if name == 'p3-detached-retirement':
            record(name + '-retired-before-map', counts['allocation-free'] == 1 and
                   next(row['ticks'] for row in actions if row['operation'] == 'allocation-free') <
                   next(row['ticks'] for row in actions if row['operation'] == 'protected-map') and
                   any(e['kind'] == 4 and e['status'] & 8 for e in events))
        if name.startswith('p3-loss-'):
            expected_candidates = 1 if name == 'p3-loss-recovery' else 0
            record(name + '-loss-accounting', counts['forced-retry-loss'] == 1 and
                   result['terminal']['drops'] == result['terminal']['contention_exhausted'] == 1 and
                   len(result['candidate_chains']) == expected_candidates and
                   len(result['reset_scoped_chains']) == expected_candidates and not result['chains'] and
                   result['scientific_firstness_qualified'] is False,
                   expected_candidates=expected_candidates, actual_candidates=len(result['candidate_chains']),
                   recovered_scoped_chains=len(result['reset_scoped_chains']),
                   unknown_bounds=result['terminal']['loss_bounds_uncertain'])
    receipt = dict(schema='sor-d5ab-p3-native-controls/1', build=str(build), development=development,
                   build_sha256=sha(build / 'build.json'), inputs=inputs,
                   script_sha256=sha(__file__), rows=rows,
                   failures=[row['case'] for row in rows if not row['passed']],
                   scope='Actual compiled producer/bridges with emulated engine host and independent host-state oracle.')
    (out / 'receipt.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf8', newline='\n')
    print(json.dumps(dict(out=str(out), checks=len(rows), failures=receipt['failures'])))
    return bool(receipt['failures'])


if __name__ == '__main__':
    raise SystemExit(main())
