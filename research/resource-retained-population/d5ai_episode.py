# SPDX-License-Identifier: GPL-3.0-or-later
"""Control a separately approved D5AI episode without inheriting B2 authority.

Reuses owned P4 worker/session/STOP mechanisms and geometry arm functions under
SOR-P-0002. Reads pinned plan/preflight/approval, process-query handles and small
session metadata; writes only exclusive session/controller requests and receipts.
No launch, deployment, game action, save access, process intervention or network.
D5AI Stage A does not supply the approval required by this prospective CLI.
"""
import argparse
import copy
import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
RUNTIME = ROOT / 'runtime/construction-winner'
sys.path.insert(0, str(RUNTIME))
from p4_controller import LIVE, disk_guard, sha, write_new
from d5ai_controller import arm, poll_geometry, read_json, pinned_json, validate_geometry_plan


def strict_session_json(path):
    """Parse each worker/state file once, with only the legacy QPC exception."""
    def pairs(items):
        value = {}
        for key, item in items:
            if key in value and not (key == 'qpc_frequency' and type(item) is int and
                                     type(value[key]) is int and value[key] == item):
                raise ValueError('Duplicate session JSON key: ' + key)
            value[key] = item
        return value

    def constant(text):
        raise ValueError('Nonfinite session JSON constant: ' + text)

    with Path(path).open('rb') as stream:
        data = stream.read(65537)
    if len(data) > 65536:
        raise ValueError('Bounded session JSON file required')
    return json.loads(data, object_pairs_hook=pairs, parse_constant=constant)


# Original P4 methods resolve read_json through their defining module globals.
# Give D5AI an isolated module instance, then replace its parser before exposing
# any controller. Each inherited read is parsed once and used directly; there is
# no pre-check followed by a permissive second parse. The historical module and
# its callers retain their original parser and behavior.
_p4_spec = importlib.util.spec_from_file_location('d5ai_private_owned_p4', RUNTIME / 'p4_controller.py')
_private_p4 = importlib.util.module_from_spec(_p4_spec)
_p4_spec.loader.exec_module(_private_p4)
_private_p4.read_json = strict_session_json
SessionController = _private_p4.SessionController

SCHEMA = 'sor-d5ai-plan/1'
SCOPES = {
    'A': dict(processes=1, save52_loads=1, direct_travels=3, query_checkpoints=2,
              route=['Lodge', 'Feynman V Cu IL F', 'Lodge', 'Feynman V Cu IL F'],
              new_saves=0, forced_regeneration=False, automatic_repeats=0),
    'B': dict(processes=1, save52_loads=1, direct_travels=1, query_checkpoints=1,
              route=['Lodge', 'Feynman V Cu IL F'], new_saves=0,
              forced_regeneration=False, automatic_repeats=0),
}
CONTROL_PATHS = {RUNTIME / name for name in (
    'p4_controller.py', 'controller.py', 'worker_health.py', 'read_capture.py',
    'reduce_v3.py', 'reduce_v4.py', 'd5ai_controller.py', 'd5ai_read_geometry.py', 'd5ai_read_lifetime.py')} | {Path(__file__).resolve()}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def scope_for_episode(episode):
    require(episode in SCOPES, 'Episode must be A or B')
    return copy.deepcopy(SCOPES[episode])


def same_structure(a, b):
    return json.dumps(a, sort_keys=True, allow_nan=False) == json.dumps(b, sort_keys=True, allow_nan=False)


def verify_controller_pins(plan):
    pins = plan.get('controller_pins', {})
    require(len(pins) == len(CONTROL_PATHS) and {Path(p).resolve() for p in pins} == CONTROL_PATHS,
            'Exact ten controller source pins required')
    for path, digest in pins.items():
        require(sha(path) == digest, 'Controller source identity mismatch: ' + path)


def validate_authority(plan, admission, approval, session, identity_hash):
    require(plan.get('schema') == SCHEMA, 'D5AI episode plan required')
    episode = plan.get('episode')
    expected_scope = scope_for_episode(episode)
    require(same_structure(plan.get('scope'), expected_scope), 'Frozen episode action scope mismatch')
    require(admission.get('state') == 'PASS_OFFLINE_PREFLIGHT', 'Successful full preflight required')
    require(admission.get('plan_sha256') == plan.get('plan_sha256'), 'Preflight plan identity mismatch')
    require(approval.get('authority') == f'D5AI_EPISODE_{episode}_EXPLICIT_MAINTAINER_GO',
            'Separate approval for this D5AI episode required; B2 approval is insufficient')
    require(approval.get('episode') == episode and same_structure(approval.get('scope'), expected_scope),
            'Approval episode/scope mismatch')
    require(approval.get('plan_sha256') == plan.get('plan_sha256'), 'Approval plan identity mismatch')
    require(approval.get('preflight_sha256') == admission.get('receipt_sha256'), 'Approval preflight identity mismatch')
    require(approval.get('session') == str(session), 'Approval session mismatch')
    require(approval.get('identity_sha256') == identity_hash, 'Approval process/session identity mismatch')
    require(approval.get('run_card_sha256') == plan.get('run_card_sha256') and
            isinstance(plan.get('run_card_sha256'), str) and len(plan['run_card_sha256']) == 64,
            'Approval must name this frozen episode card')
    require(approval.get('save52_sha256') == plan.get('save52_sha256') and
            isinstance(plan.get('save52_sha256'), str) and len(plan['save52_sha256']) == 64,
            'Approval must bind the protected Save52 input')


class EpisodeController(SessionController):
    """Keep P4 mechanisms with D5AI scope, strict parsing and owned STOP admission."""
    def __init__(self, session, expected, plan, admission, approval, action):
        if action != 'stop':
            super().__init__(session, expected, plan, admission, approval, action)
            return
        # Source-informed P4 STOP admission: retain target/authority, process and
        # exclusive persisted ownership checks without requiring healthy READY or
        # ACK files. No new owner is inferred from malformed controller state.
        self.session = _private_p4.clean_path(session)
        self.expected, self.plan = dict(expected), dict(plan)
        self.lock = self.lease = None
        self.identity_hash = sha(self.session / 'identity.json')
        require(strict_session_json(self.session / 'identity.json') == expected, 'STOP identity mismatch')
        self.validate_target(admission, approval)
        self.process_state = _private_p4.process_identity(expected, plan['process_image'], True)
        try:
            self.lock = (self.session / 'p4-controller.lock').open('a+b')
            self.lock.seek(0)
            _private_p4.msvcrt.locking(self.lock.fileno(), _private_p4.msvcrt.LK_NBLCK, 1)
            self.state_path = self.session / 'p4-state.json'
            self.state = strict_session_json(self.state_path)
            owner = self.state['owner']
            require(self.state['identity_sha256'] == self.identity_hash and isinstance(owner, str) and
                    len(owner) == 32 and all(c in '0123456789abcdef' for c in owner),
                    'Existing STOP ownership identity required')
        except BaseException:
            self.close()
            raise

    def validate_target(self, admission, approval):
        require(self.session.parent == LIVE == Path(self.plan['live_root']).resolve() and
                self.session.name == 'session-' + self.expected['nonce'], 'Wrong live session namespace')
        require(self.expected.get('schema') == 'sor-d5x/4' and self.expected.get('retail') is True,
                'Pinned retail lifecycle identity required')
        require(self.expected['host_sha256'] == self.plan['game_sha256'] and
                self.expected['sfse_sha256'] == self.plan['sfse_sha256'] and
                self.expected['dll_sha256'] == self.plan['dll_sha256'], 'Game/SFSE/candidate identity mismatch')
        require(Path(self.plan['process_image']).name == 'Starfield.exe', 'Wrong process image')
        require(len(self.expected['sites']) == len(self.plan['sites']) == 18, 'All base lifecycle sites required')
        for observed, pinned in zip(self.expected['sites'], self.plan['sites']):
            require(observed['index'] == pinned['index'] and observed['rva'] == pinned['rva'] and
                    observed['guard_sha256'] == pinned['guard_sha256'] and
                    observed['va'] == self.expected['module_base'] + pinned['rva'], 'Base lifecycle site mismatch')
        validate_geometry_plan(self.expected, self.plan)
        validate_authority(self.plan, admission, approval, self.session, self.identity_hash)

    def validate_phase(self, admission):
        path = ROOT / 'research/resource-retained-population/d5ai_operations.py'
        require(sha(path) == self.plan['operations_sha256'], 'Episode operations source mismatch')
        spec = importlib.util.spec_from_file_location('d5ai_bound_operations', path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        module.lightweight(self.plan, admission)


def execute(args):
    plan = pinned_json(args.plan, args.plan_sha256)
    plan['plan_sha256'] = args.plan_sha256
    verify_controller_pins(plan)
    preflight = pinned_json(args.preflight, args.preflight_sha256)
    preflight['receipt_sha256'] = args.preflight_sha256
    approval = pinned_json(args.approval, args.approval_sha256)
    if args.action != 'stop':
        disk_guard()
    identity = read_json(args.session / 'identity.json')
    action = 'start' if args.action == 'start' else 'stop' if args.action == 'stop' else 'poll' if args.action in ('poll', 'geometry-poll') else 'request'
    controller = EpisodeController(args.session, identity, plan, preflight, approval, action)
    try:
        if args.action == 'start':
            result = dict(state='BOUND_READY', raw_verified=False)
        elif args.action == 'request':
            result = controller.request()
        elif args.action == 'poll':
            result = controller.poll()
        elif args.action == 'stop':
            result = controller.request_stop(args.reason)
        elif args.action == 'arm':
            result = arm(controller, args.label)
        else:
            result = poll_geometry(controller)
        result.update(episode=plan['episode'], identity_sha256=controller.identity_hash,
                      owner=controller.state['owner'], plan_sha256=args.plan_sha256,
                      approval_sha256=args.approval_sha256)
        write_new(args.out, result)
        print(json.dumps(result))
    finally:
        controller.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['start', 'request', 'poll', 'stop', 'arm', 'geometry-poll'])
    parser.add_argument('--session', required=True, type=Path)
    for name in ('plan', 'preflight', 'approval'):
        parser.add_argument('--' + name, required=True, type=Path)
        parser.add_argument('--' + name + '-sha256', required=True)
    parser.add_argument('--label', default='')
    parser.add_argument('--reason', default='maintainer-directed D5AI STOP')
    parser.add_argument('--out', required=True, type=Path)
    args = parser.parse_args()
    try:
        execute(args)
    except BaseException as error:
        try:
            write_new(args.out, dict(state='CHECK_ERROR', action=args.action, error=repr(error), raw_verified=False))
        except OSError:
            pass
        raise


if __name__ == '__main__':
    main()
