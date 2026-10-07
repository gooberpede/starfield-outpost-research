# SPDX-License-Identifier: GPL-3.0-or-later
"""Offline review checks; no debugger, target, save, build or deployment access.

Reads authored plan/version, prior PE receipt and optional explicit historical
disposable JSONL. Runs only the disabled historical Python CLI, never its dead
implementation. Writes one explicit create-new local JSON receipt. Reused
validator provenance: maintainer/PROVENANCE.md. Standard library only.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE/'maintainer'))
from hardware_evidence import read_rows, validate


def run(raw=None):
    checks = {}
    plan = json.loads((HERE/'next_capture_plan.json').read_text())
    version = json.loads((HERE/'tooling_version.json').read_text())
    pe = json.loads((ROOT/'.local-work/exp0002a/capture-sites.json').read_text())
    assert plan['live_enabled'] is True and plan['stage_c_enabled'] is False
    assert plan['backend'] == 'win32-hardware-rf'
    assert len(plan['sites']) == 1
    site = plan['sites'][0]
    assert site['label'] == 'REQUEST_ENTRY' and int(site['rva'], 0) == 0x183c590
    assert site['sha256'] == next(x['sha256'] for x in pe['sites'] if int(x['rva'], 0) == 0x183c590)
    assert plan['game_sha256'] == pe['game_sha256']
    assert site['mechanism'] == 'DR0_EXECUTE' and site['max_retained_hits'] == 1
    checks['one_site_matches_preserved_pe'] = True
    assert plan['setup']['operator_ui_paused_required'] is True
    assert plan['setup']['initial_attach_pause_event_required'] is False
    assert plan['setup']['watchdog_seconds'] == 300
    assert plan['setup']['armed_wait_confirmation_seconds'] == 120
    assert plan['capture']['deadline_seconds'] == 10
    assert plan['capture']['start'] == 'ACTIVE_FLUSH_ACK_BEFORE_CLICK_NOW'
    assert plan['capture']['max_requests'] == 1
    checks['separate_timing_limits_declared_not_runtime_tested'] = True
    major, minor, patch = map(int, version['observer_semver'].split('.'))
    assert (major, minor, patch) == (0, 1, 0)
    assert (major << 24) | (minor << 16) | patch == version['observer_plugin_version_integer'] == 65536
    assert version['package_filename'] == f'SorExp0002-{major}.{minor}.{patch}.zip'
    assert ((minor << 16) | (patch+1)) == 65537
    checks['reserved_version_consistent_no_package_built'] = True
    assert version['adapter_semver'] == '0.1.3'
    assert version['adapter_version_integer'] == 65539
    assert version['adapter_executable'] == 'save_request_adapter-0.1.3.exe'
    assert plan['thread_scope']['mode'] == 'S1_NONE_OR_S2_SINGLE_EXISTING'
    assert plan['thread_scope']['post_armed_create_thread'] == 'RECORD_ONLY_NO_DR0_INSTALL'
    assert plan['cleanup']['policy'] == 'CAPTURE_FIRST_DESTRUCTIVE_RECOVERY'
    assert plan['cleanup']['evidence_completeness_independent_of_cleanup'] is True
    assert plan['cleanup']['pre_capture_force_kill'] == 'FORBIDDEN_EXCEPT_INDEPENDENT_MACHINE_SAFETY'
    assert plan['launch']['stage_b'] == 'ORDINARY_STEAM_WITHOUT_SFSE'
    checks['adapter_0_1_3_scope_recovery_and_observer_reservation_distinct'] = True
    result = subprocess.run([sys.executable, '-B', str(HERE/'capture.py'), '--pid', '1', '--name', 'must-not-run', '--operator-new-slot-ready'],capture_output=True,text=True,timeout=10)
    assert result.returncode != 0 and 'DISABLED:' in result.stderr
    assert not (ROOT/'.local-work/exp0002a/must-not-run').exists()
    checks['historical_live_cli_refuses_before_target_access'] = True
    if raw:
        rows = read_rows(raw)
        verdict = validate(rows)
        assert verdict['passed'] and verdict['config']['workers'] == 8 and verdict['config']['stages'] == 1
        checks['historical_replay'] = dict(path=str(raw),sha256=hashlib.sha256(raw.read_bytes()).hexdigest(),passed=True,captures=verdict['captures'],note='Historical record replay; no new debugger trial')
        cases = {}
        altered = copy.deepcopy(rows)
        altered.remove(next(x for x in altered if x['kind']=='capture'))
        cases['missing_capture'] = not validate(altered)['passed']
        altered = copy.deepcopy(rows)
        next(x for x in altered if x['kind']=='capture')['rip'] = '0x1'
        cases['wrong_rip'] = not validate(altered)['passed']
        altered = copy.deepcopy(rows)
        next(x for x in altered if x['kind']=='context' and x['boundary']=='retired')['dr7'] = '0xff'
        cases['dirty_retirement'] = not validate(altered)['passed']
        altered = copy.deepcopy(rows)
        last = next(x for x in altered if x['kind']=='survival' and x['delay']==15)
        logs = [json.loads(x) for x in last['target_log'].splitlines()]
        next(x for x in reversed(logs) if 'heartbeat' in x)['counters'][0] = 0
        last['target_log'] = '\n'.join(json.dumps(x) for x in logs)
        cases['stalled_worker'] = not validate(altered)['passed']
        assert all(cases.values())
        checks['negative_in_memory_controls_rejected'] = cases
    return checks


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--raw',type=Path)
    parser.add_argument('--output',type=Path,required=True)
    args = parser.parse_args()
    if not args.output.resolve().is_relative_to((ROOT/'.local-work/exp0002a-adapter-0.1.3').resolve()):
        parser.error('Output must remain in ignored 0.1.3 evidence root')
    result = run(args.raw)
    with args.output.open('x',encoding='utf-8',newline='\n') as out:
        json.dump(result,out,indent=2);out.write('\n')
    print(json.dumps(result,indent=2))
