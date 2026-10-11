"""SPDX-License-Identifier: GPL-3.0-or-later
Read-only interpretation of retained final-attempt receipts; no process access.
Writes a NEW ignored result matrix, with hashes and selected trace line references.
The output is a completed outcome B, never qualification of an executable.
"""
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
LOCAL = ROOT / '.local-work/thread-control'
sys.path.insert(0, str(ROOT / 'debugger/event-oracle'))
from materialize_epochs import decode


def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    cases = []
    suspend_failures = []
    queued_traps = []
    builds = {}
    for matrix in sorted(LOCAL.glob('*/matrix.json')):
        parent = matrix.parent
        builds[parent.name] = json.loads((parent / 'build.json').read_text())
        builds[parent.name]['harness_sha256'] = sha(parent / 'harness.py')
        for number, case in enumerate(json.loads(matrix.read_text())['cases']):
            run = parent / (str(number).zfill(2) + '-' + case['mode'])
            path = run.relative_to(ROOT).as_posix()
            log = run / 'adapter.log'
            failing = []
            queued = []
            rewound = 0
            trace_count = 0
            for line_no, line in enumerate(log.open(encoding='utf-8', errors='replace'), 1):
                if not line.startswith('TRACE '):
                    continue
                row = json.loads(line[6:])
                trace_count += 1
                if row.get('kind') == 'thread_api' and row.get('phase') == 'suspend' and row['result'] == 0xffffffff:
                    failing.append({'path': path + '/adapter.log', 'line': line_no, 'trace': row})
                if row.get('kind') == 'thread_api' and row.get('phase') == 'exit_query_after_failed_suspend':
                    failing.append({'path': path + '/adapter.log', 'line': line_no, 'trace': row})
                if row.get('kind') == 'exception' and row.get('pending') and row.get('matching_site') and row['code'] == 0x80000003 and row['tid'] != row['stepping']:
                    queued.append({'path': path + '/adapter.log', 'line': line_no, 'trace': row})
                rewound += row.get('kind') == 'queued_rewound'
            suspend_failures += failing
            queued_traps += queued
            rows, receipt = decode(run / 'evidence/epochs.wal')
            counts = case.get('counts', {})
            expected_exceptions = {'foreign-break': 1, 'full': 2, 'center-only': 2, 'grid-guard-failure': 2, 'writer-failure': 2, 'stop-replay': 2}.get(case['mode'], 0)
            unexpected = None if not counts else counts['exceptions'] - expected_exceptions
            timing = run / 'timing.json'
            observed_latency = None
            if timing.exists():
                profile = json.loads(timing.read_text())
                ticks = [sum(sample['ticks']) * 1000 / profile['qpc_frequency'] for sample in profile['samples']]
                observed_latency = {'samples': len(ticks), 'total_handler_ms': sum(ticks), 'max_handler_ms': max(ticks, default=0), 'meaning': 'diagnostic handler accounting includes trace overhead; concurrent experiments; NOT baseline latency comparison'}
            cases.append({
                'path': path, 'mode': case['mode'], 'adapter_exit': case['adapter_exit'], 'fixture_exit': case['fixture_exit'],
                'adapter_sha256': case['adapter_sha256'], 'fixture_sha256': case['fixture_sha256'], 'case_receipt_sha256': sha(run / 'result.json'),
                'trace_sha256': sha(log), 'trace_rows': trace_count, 'counts': counts, 'boundary_counts': case.get('boundary_counts'),
                'unexpected_breakpoint_exceptions': unexpected, 'restoration_detach_verified': case['restoration_detach_verified'],
                'postflight_limit': case.get('postflight_limit'), 'orchestration_failures': case['failures'],
                'diagnostic_expectations_met': case.get('diagnostic_expectations_met'), 'candidate_qualified': False,
                'elapsed_ms': case['elapsed_ms'], 'handler_latency': observed_latency, 'wal': receipt,
                'terminal': [row for row in rows if row.get('kind') in ('terminal', 'retired', 'target_exit')],
                'failed_suspend_trace_count': len(failing), 'queued_trap_count': len(queued), 'queued_rewinds': rewound,
            })
    api = [json.loads(line) for line in (LOCAL / 'api-probe-01/results.jsonl').read_text().splitlines() if line.strip()]
    assert len(api) == 5
    by_name = {row['name']: row for row in api}
    assert by_name['exited-full']['suspend_error'] == 5 and by_name['exited-full']['after_exit'] == 23
    assert by_name['exited-debug-minimum-rights']['suspend_error'] == 5 and by_name['exited-debug-minimum-rights']['after_error'] == 5
    assert by_name['running-existing-suspend']['suspend'] == 1 and by_name['running-existing-suspend']['resume'] == 2
    final = [case for case in cases if '/repair-trial-02/' in case['path']]
    assert len(final) == 8
    stopped = [case for case in final if case['mode'] == 'stop-queued']
    assert len(stopped) == 3 and all(case['unexpected_breakpoint_exceptions'] > 0 and case['restoration_detach_verified'] is True and case['diagnostic_expectations_met'] is False for case in stopped)
    assert suspend_failures and queued_traps
    assert len(cases) == 32, len(cases)
    original = [case for case in cases if '/original-trace-01/' in case['path']]
    assert len(original) == 6 and all(case['restoration_detach_verified'] for case in original)
    startup = json.loads((LOCAL / 'startup-014-final/results.json').read_text())
    assert len(startup['cases']) == 19 and startup['all_targets_normal_exit']
    assert 'checks=12 PASS' in (LOCAL / 'health-repeat.log').read_text()
    assert 'Ran 11 tests' in (LOCAL / 'inspector-final.log').read_text() and 'OK' in (LOCAL / 'inspector-final.log').read_text()
    offline = json.loads((LOCAL / 'offline-final.json').read_text())
    assert offline['status'] == 'PASS'
    historical_root = ROOT / '.local-work/event-instrumentation'
    original_r1 = json.loads((historical_root / 'startup-candidate-014-03/result.json').read_text())['cases']['grid-guard-failure']
    _, original_r2_wal = decode(historical_root / 'startup-candidate-014-02/full/evidence/epochs.wal')
    historical = [
        {'id': 'R1', 'path': '.local-work/event-instrumentation/startup-candidate-014-03/grid-guard-failure', 'original_result': original_r1, 'independent_postflight': 'NOT_CAPTURED', 'actual_handle_mask_and_API_pair': 'UNKNOWN'},
        {'id': 'R2', 'path': '.local-work/event-instrumentation/startup-candidate-014-02/full', 'original_wal': original_r2_wal, 'adapter_exit': 'NOT_RETAINED', 'fixture_exit': 'NOT_RETAINED', 'independent_postflight': 'NOT_CAPTURED', 'exception_address': 'NOT_CAPTURED'},
        {'id': 'prior-014-01', 'path': '.local-work/event-instrumentation/startup-candidate-014-01', 'outcome': 'source identity changed during run; NOT_QUALIFIED'},
    ]
    result = {'outcome': 'B', 'decision': 'ABANDON_EXTERNAL_DEBUGGER_PATH', 'completed_failure_analysis': True, 'candidate_issued': False,
              'historical_counterexamples': historical,
              'builds': builds, 'cases': cases, 'api_probe': api, 'suspend_failure_traces': suspend_failures, 'queued_trap_traces': queued_traps,
              'checks': {'startup_baseline_014': 19, 'health': 12, 'WAL_inspector': 11, 'offline_protected_inputs': 'PASS'},
              'limits': ['No new Starfield access or live result.', 'Original R1 handle/native state was not captured; new rights/lifetime evidence does not reconstruct it.',
                         'Diagnostic repeats cannot erase historical failures.', 'Retirement debt/TF/termination state is NOT fully qualified.',
                         'Historical collector exit0 means completed receipt collection, not control success; raw failed counts/exits retained.',
                         'Original-trace six workflows supplement retained original qualification; diagnostic harness is not the full scientific inspector suite.']}
    output = LOCAL / 'result-matrix.json'
    with output.open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(result, stream, indent=2)
        stream.write('\n')
    print(result['decision'], 'cases=', len(cases), 'API failure traces=', len(suspend_failures), 'queued traps=', len(queued_traps))


if __name__ == '__main__':
    main()
