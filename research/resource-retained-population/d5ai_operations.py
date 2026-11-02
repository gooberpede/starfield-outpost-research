# SPDX-License-Identifier: GPL-3.0-or-later
"""Prepare protected pre/postflight for separately approved D5AI episodes.

Adapts owned P4 preservation, archive and phase mechanisms under SOR-P-0002.
Reads pinned sources/package, installed/protected inputs and session evidence;
writes only fresh ignored receipts and restoration COPIES. No game launch,
deployment, original save writes/restoration, process intervention or network.
The adapter grants no Episode A/B approval and never invents B2 authorization.
"""
import argparse
import copy
import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).parent))
from d5ai_episode import EpisodeController, SCHEMA, require, scope_for_episode, verify_controller_pins, same_structure, strict_session_json
from d5ai_episode import RUNTIME, sha, pinned_json, read_json
sys.path.insert(0, str(ROOT / 'runtime/session-tools'))
from common import fresh, guard, regular

LEGACY_PATH = ROOT / 'research/resource-retained-population/d5ab_p4_operations.py'
LEGACY_PHASES = {ROOT / name for name in (
    'runtime/session-tools/common.py', 'research/resource-carinae-source-context/save_policy.py',
    'research/resource-retained-population/d5ab_p4_operations.py')}
PHASES = LEGACY_PHASES | {Path(__file__).resolve()}


def legacy():
    spec = importlib.util.spec_from_file_location('d5ai_owned_p4_operations', LEGACY_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def phase_pins(plan):
    pins = plan.get('phase_pins', {})
    require(len(pins) == len(PHASES) and {Path(p).resolve() for p in pins} == PHASES, 'Exact four phase-helper pins required')
    require(plan.get('operations_sha256') == sha(__file__), 'D5AI operations source identity mismatch')
    for path, digest in pins.items():
        require(sha(regular(path)) == digest, 'Phase helper identity mismatch: ' + path)


def legacy_plan(plan):
    """Project already verified component fields; authority is never projected."""
    value = copy.deepcopy(plan)
    value['schema'] = 'sor-d5ab-p4-plan/1'
    value['operations_sha256'] = sha(LEGACY_PATH)
    value['phase_pins'] = {p: digest for p, digest in plan['phase_pins'].items()
                           if Path(p).resolve() in LEGACY_PHASES}
    return value


def verify_plan(plan):
    require(plan.get('schema') == SCHEMA, 'D5AI episode plan required')
    require(same_structure(plan.get('scope'), scope_for_episode(plan.get('episode'))), 'Frozen episode action scope mismatch')
    phase_pins(plan)
    verify_controller_pins(plan)
    # This checks the original package/launch/loader/content identity gates with
    # their actual pinned component source, after checking the new wrapper too.
    legacy().verify_plan(legacy_plan(plan))
    require(sha(regular(plan['run_card_path'])) == plan['run_card_sha256'], 'Episode card identity mismatch')


def lightweight(plan, preflight):
    phase_pins(plan)
    value = legacy().lightweight(legacy_plan(plan), preflight)
    value.update(episode=plan['episode'], operations_schema='sor-d5ai-operations/1')
    return value


def preflight(plan, plan_hash, out):
    verify_plan(plan)
    module = legacy()
    value = module.preflight(legacy_plan(plan), plan_hash, out)
    module.no_game()
    protected = value['protection']['protected_live']
    require(plan['save52_name'] in protected and protected[plan['save52_name']]['sha256'] == plan['save52_sha256'],
            'This protected Save52 must match the episode plan')
    value.update(schema='sor-d5ai-preflight/1', episode=plan['episode'], scope=plan['scope'],
                 authority='OFFLINE_CHECK_ONLY_NO_D5AI_EPISODE_GO')
    return value


def worker_json(path):
    """Use the same bounded single-parse worker/state policy as the controller."""
    return strict_session_json(path)


def finalization(plan, preflight_receipt, session, approval):
    """Bind a closed retail episode to its own authority and unchanged owned STOP."""
    session = Path(session).resolve()
    identity = read_json(session / 'identity.json')
    controller = EpisodeController.__new__(EpisodeController)
    controller.session, controller.expected, controller.plan = session, identity, plan
    controller.identity_hash = sha(session / 'identity.json')
    controller.validate_target(preflight_receipt, approval)
    require(session.name not in preflight_receipt['existing_sessions'], 'Old session cannot become a new episode')
    state = read_json(session / 'p4-state.json')
    require(state['identity_sha256'] == controller.identity_hash, 'Controller identity mismatch')
    stop = state.get('stop')
    require(stop and stop['identity_sha256'] == controller.identity_hash and stop['owner'] == state['owner'] and
            len(state['owner']) == 32 and len(stop['stop_nonce']) == 32, 'Owned STOP identity required')
    require((session / 'STOP').read_bytes() == (json.dumps(stop, sort_keys=True) + '\n').encode(), 'Foreign STOP')
    terminal = worker_json(session / 'terminal.json')
    require(all(terminal.get(k) == v for k, v in identity.items()) and terminal['resident_inert'] is True,
            'Terminal identity/residency mismatch')
    require(not state['telemetry_fault'], 'Contradictory challenged telemetry')
    return dict(episode=plan['episode'], identity_sha256=controller.identity_hash, owner=state['owner'],
                stop_nonce=stop['stop_nonce'])


def postflight(plan, before, session, approval, out):
    verify_plan(plan)
    module = legacy()
    session = regular(session)
    identity = read_json(session / 'identity.json')
    process_state = module.original_process_gone(identity)
    errors, capture_errors = [], []
    try:
        owned = finalization(plan, before, session, approval)
    except (AssertionError, OSError, KeyError, ValueError) as error:
        owned = None
        capture_errors.append(str(error))
    try:
        after = module.full(out)
        module.compare_protection(before['protection'], after)
        require(before['remote_protected_sizes'] == module.remote_sizes(after), 'Remote protected saves changed')
        require(not Path(plan['deployed_dll']).exists(), 'Disable/remove the effective candidate after exit')
    except (AssertionError, OSError, ValueError) as error:
        errors.append(str(error))
    sys.path.insert(0, str(RUNTIME))
    from read_capture import inspect
    from d5ai_read_geometry import read_session
    from d5ai_read_lifetime import read_prefix
    scientific = inspect(session, plan['dll_sha256'])
    try:
        geometry = read_session(session)
        capture_errors.extend(e['error'] for e in geometry['errors'])
    except (ValueError, OSError) as error:
        geometry = None
        capture_errors.append(str(error))
    try:
        lifetime=read_prefix(session,worker_json(session/'terminal.json'))
    except (ValueError,OSError,KeyError) as error:
        lifetime=None
        capture_errors.append(str(error))
    value = dict(schema='sor-d5ai-postflight/1' , action='postflight', episode=plan['episode'],
                 process_state=process_state, session=str(session), status='PARTIAL_POSTFLIGHT',
                 protection_errors=errors, capture_errors=capture_errors, owned_finalization=owned,
                 scientific=scientific, geometry=geometry, lifetime=lifetime, plan_sha256=plan['plan_sha256'],
                 preflight_sha256=before['receipt_sha256'], authority='NO_RETRY_OR_RELAUNCH_OR_NEXT_EPISODE')
    if not errors and not capture_errors and scientific.get('complete_session'):
        value['status'] = 'PASS_POSTFLIGHT'
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['preflight', 'postflight'])
    parser.add_argument('--plan', required=True, type=Path)
    parser.add_argument('--plan-sha256', required=True)
    parser.add_argument('--out', required=True, type=Path)
    for name in ('preflight', 'approval'):
        parser.add_argument('--' + name, type=Path)
        parser.add_argument('--' + name + '-sha256')
    parser.add_argument('--session', type=Path)
    args = parser.parse_args()
    out = args.out.resolve()
    require(out.is_relative_to(ROOT / '.local-work/d5ai'), 'Fresh task-local operation output required')
    out.mkdir(parents=True, exist_ok=False)
    try:
        plan = pinned_json(args.plan, args.plan_sha256)
        if args.action == 'preflight':
            value = preflight(plan, args.plan_sha256, out)
        else:
            before = pinned_json(args.preflight, args.preflight_sha256)
            require(before['plan_sha256'] == args.plan_sha256, 'Preflight plan mismatch')
            before['receipt_sha256'] = args.preflight_sha256
            plan['plan_sha256'] = args.plan_sha256
            approval = pinned_json(args.approval, args.approval_sha256)
            value = postflight(plan, before, args.session, approval, out)
    except BaseException as error:
        fresh(out / 'receipt.json', dict(state='CHECK_ERROR', action=args.action, error=repr(error), authority='NO_D5AI_EPISODE_GO'))
        raise
    fresh(out / 'receipt.json', value)
    print(json.dumps(dict(out=str(out), state=value.get('state', value.get('status')))))


if __name__ == '__main__':
    main()
