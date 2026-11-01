# SPDX-License-Identifier: GPL-3.0-or-later
"""Prepare offline protection receipts and a future B2 phase procedure.

Reads owned preservation/policy/session tools, pinned package and protected inputs.
Preflight/postflight write fresh ignored receipts and restoration COPIES only.
Lightweight checks read names/sizes and small pins, never raw events or save bytes.
No launch, deployment, process intervention, original write or network activity.
Owned prepare_native.py/common.py methods are reused under SOR-P-0002.
"""
import argparse
import ctypes as C
from ctypes import wintypes as W
import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'runtime/session-tools'))
from common import fresh, guard, regular, sha, read


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def policy_module():
    return load('p4_save_policy', 'research/resource-carinae-source-context/save_policy.py')


def verify_plan(plan):
    assert sys.flags.optimize == 0
    assert plan['schema'] == 'sor-d5ab-p4-plan/1'
    for path, digest in plan['package_pins'].items():
        assert sha(regular(path)) == digest, path
    assert {'Starfield.exe', 'sfse_loader.exe', 'sfse_1_16_244.dll',
            'Starfield.esm', 'Starfield - PlanetData.ba2'} == {
                Path(path).name for path in plan['launch_pins']}
    for path, digest in plan['launch_pins'].items():
        assert sha(regular(path)) == digest, path
    assert sha(__file__) == plan['operations_sha256']


def no_game():
    # Narrow process-name inventory, following the existing offline prepare gate.
    import subprocess
    result = subprocess.check_output(['powershell', '-NoProfile', '-Command',
        '@(Get-Process Starfield -ErrorAction SilentlyContinue).Count'], text=True)
    assert result.strip() == '0', 'Starfield must be absent for full audits'


def compare_protection(before, after):
    keys = ('save_policy_sha256', 'protected_live', 'backups', 'definitions', 'config',
            'archive_guard', 'restore_rehearsal_sha256')
    # Backup metadata is intentionally strict; active transient and Cloud metadata
    # diagnostics are not compared as scientific inputs.
    differences = [key for key in keys if before[key] != after[key]]
    assert not differences, differences
    return dict(equal=True, fields=list(keys))


def lightweight(plan, preflight):
    """Check launch/health admission without a full in-play protection scan."""
    required = {str(ROOT / name) for name in (
        'runtime/session-tools/common.py',
        'research/resource-carinae-source-context/save_policy.py',
        'research/resource-retained-population/d5ab_p4_operations.py')}
    assert set(plan['phase_pins']) == required
    for path, digest in plan['phase_pins'].items():
        assert sha(regular(path)) == digest, path
    guard()
    module = policy_module()
    policy = module.load_policy()
    previous = preflight['protection']
    assert module.policy_hash(policy) == previous['save_policy_sha256']
    expected = previous['protected_live']
    current = module.partition(module.sizes(previous['live_path'], policy), policy)
    assert not current['unclassified']
    assert current['protected'] == {name: dict(bytes=row['bytes']) for name, row in expected.items()}
    for folder, names in preflight['remote_protected_sizes'].items():
        remote = module.partition(module.sizes(folder, policy), policy)
        assert not remote['unclassified'] and remote['protected'] == names
    for path, row in previous['file_guards'].items():
        stat = regular(path).stat()
        assert (stat.st_size, stat.st_mtime_ns) == (row['bytes'], row['mtime_ns']), path
    for path, row in previous['installed'].items():
        stat = regular(path).stat()
        assert (stat.st_size, stat.st_mtime_ns) == (row['bytes'], row['mtime_ns']), path
    assert sha(regular(plan['sfse_path'])) == plan['sfse_sha256']
    deployed = regular(plan['deployed_dll'])
    assert sha(deployed) == plan['dll_sha256']
    competing = [p.name for p in deployed.parent.glob('Sor*.dll') if p != deployed]
    assert not competing, competing
    return dict(state='PASS_LIGHTWEIGHT', raw_verified=False,
                save_content_rehashed=False, transient_names=sorted(current['transient']))


def remote_sizes(protection):
    module = policy_module()
    sync = protection['sync']
    # Retain the exact namespace even when empty, so later additions are checked.
    folder = Path(sync['remote_path']) / 'Saves'
    policy = module.load_policy()
    current = module.partition(module.sizes(folder, policy), policy)
    assert not current['unclassified']
    return {str(folder): current['protected']}


def full(out):
    no_game()
    guard()
    sys.path.insert(0, str(Path(__file__).parent))
    module = load('p4_preservation', 'research/resource-retained-population/prepare_native.py')
    return module.full_preservation(out)


def preflight(plan, plan_hash, out):
    verify_plan(plan)
    protection = full(out)
    return dict(state='PASS_OFFLINE_PREFLIGHT', plan_sha256=plan_hash,
                protection=protection, remote_protected_sizes=remote_sizes(protection),
                existing_sessions=sorted(p.name for p in Path(plan['live_root']).glob('session-*')),
                cloud_current='UNKNOWN_REQUIRES_FRESH_OPERATOR_CONFIRMATION',
                authority='OFFLINE_CHECK_ONLY_NOT_B2_GO', free_bytes=guard())


def original_process_gone(identity):
    kernel = C.WinDLL('kernel32', use_last_error=True)
    kernel.OpenProcess.argtypes = [W.DWORD, W.BOOL, W.DWORD]
    kernel.OpenProcess.restype = W.HANDLE
    kernel.GetProcessTimes.argtypes = [W.HANDLE] + [C.POINTER(W.FILETIME)] * 4
    kernel.WaitForSingleObject.argtypes = [W.HANDLE, W.DWORD]
    kernel.CloseHandle.argtypes = [W.HANDLE]
    handle = kernel.OpenProcess(0x1000 | 0x100000, False, identity['pid'])
    if not handle:
        assert C.get_last_error() == 87, 'Cannot establish original process exit'
        return 'GONE'
    try:
        times = [W.FILETIME() for _ in range(4)]
        assert kernel.GetProcessTimes(handle, *(C.byref(v) for v in times))
        birth = times[0].dwLowDateTime | times[0].dwHighDateTime << 32
        if birth != identity['creation_filetime']:
            return 'ORIGINAL_GONE_PID_REUSED'
        assert kernel.WaitForSingleObject(handle, 0) == 0, 'Original process still active'
        return 'EXITED'
    finally:
        kernel.CloseHandle(handle)


def finalization(plan, preflight, session, approval):
    """Bind offline finalization to the admitted retail identity and owned STOP."""
    sys.path.insert(0, str(ROOT / 'runtime/construction-winner'))
    import p4_controller
    identity = read(session / 'identity.json')
    controller = p4_controller.RetailController.__new__(p4_controller.RetailController)
    controller.session, controller.expected, controller.plan = session, identity, plan
    controller.identity_hash = sha(session / 'identity.json')
    controller.validate_target(preflight, approval)
    assert session.name not in preflight['existing_sessions'], 'Old session'
    state = read(session / 'p4-state.json')
    assert state['identity_sha256'] == controller.identity_hash
    stop = state['stop']
    assert stop and stop['identity_sha256'] == controller.identity_hash
    assert stop['owner'] == state['owner'] and len(state['owner']) == 32
    assert len(stop['stop_nonce']) == 32
    assert (session / 'STOP').read_bytes() == (json.dumps(stop, sort_keys=True) + '\n').encode()
    terminal = read(session / 'terminal.json')
    assert all(terminal.get(key) == value for key, value in identity.items())
    assert terminal['resident_inert'] is True
    assert not state['telemetry_fault'], 'Contradictory challenged telemetry'
    return dict(identity_sha256=controller.identity_hash, owner=state['owner'],
                stop_nonce=stop['stop_nonce'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['preflight', 'postflight'])
    parser.add_argument('--plan', required=True, type=Path)
    parser.add_argument('--plan-sha256', required=True)
    parser.add_argument('--out', required=True, type=Path)
    parser.add_argument('--preflight', type=Path)
    parser.add_argument('--preflight-sha256')
    parser.add_argument('--session', type=Path)
    parser.add_argument('--approval', type=Path)
    parser.add_argument('--approval-sha256')
    args = parser.parse_args()
    out = args.out.resolve()
    assert out.is_relative_to(ROOT / '.local-work/d5ab')
    out.mkdir(parents=True, exist_ok=False)
    try:
        plan = read(args.plan, args.plan_sha256)
        if args.action == 'preflight':
            value = preflight(plan, args.plan_sha256, out)
        else:
            verify_plan(plan)
            before = read(args.preflight, args.preflight_sha256)
            assert before['plan_sha256'] == args.plan_sha256
            before['receipt_sha256'] = args.preflight_sha256
            plan['plan_sha256'] = args.plan_sha256
            approval = read(args.approval, args.approval_sha256)
            session = regular(args.session)
            assert session.parent == Path(plan['live_root'])
            identity = read(session / 'identity.json')
            process_state = original_process_gone(identity)
            errors = []
            capture_errors = []
            try:
                owned = finalization(plan, before, session, approval)
            except (AssertionError, OSError, KeyError, ValueError) as error:
                capture_errors.append(str(error))
                owned = None
            try:
                after = full(out)
                compare_protection(before['protection'], after)
                assert before['remote_protected_sizes'] == remote_sizes(after)
                assert not Path(plan['deployed_dll']).exists(), 'Disable/remove effective DLL after exit'
            except (AssertionError, OSError, ValueError) as error:
                errors.append(str(error))
            sys.path.insert(0, str(ROOT / 'runtime/construction-winner'))
            from read_capture import inspect
            result = inspect(session, plan['dll_sha256'])
            value = dict(action='postflight', process_state=process_state, session=str(session),
                         status='PARTIAL_POSTFLIGHT', protection_errors=errors,
                         capture_errors=capture_errors, owned_finalization=owned,
                         scientific=result, authority='NO_RETRY_OR_RELAUNCH',
                         plan_sha256=args.plan_sha256, preflight_sha256=args.preflight_sha256)
            # Capture integrity and scientific firstness remain separate dimensions.
            if not errors and not capture_errors and result.get('complete_session'):
                value['status'] = 'PASS_POSTFLIGHT'
    except Exception as error:
        fresh(out / 'receipt.json', dict(state='CHECK_ERROR', action=args.action, error=repr(error), authority='NO_B2_GO'))
        raise
    fresh(out / 'receipt.json', value)
    print(json.dumps(dict(out=str(out), state=value.get('state', value.get('status')))))


if __name__ == '__main__':
    main()
