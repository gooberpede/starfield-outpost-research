# SPDX-License-Identifier: GPL-3.0-or-later
"""Control only approved Episode A using separately qualified timestamp guards.

Reuses frozen D5AI identity/worker/ownership/arm/STOP methods under SOR-P-0002.
Reads hash-bound authority/plan/preflight and small session metadata plus selected
content guards; writes exclusive controller requests and receipts only. No game
launch, gameplay, deployment, memory access, save access or process intervention.
The user controls launch/load/travel/exit. Use Python -E -B; do not optimize.
"""
import sys
if not __debug__ or sys.flags.optimize:
    raise RuntimeError('Use Python -E -B')

import argparse
import json
from pathlib import Path

import d5ai_episode as original
import d5ai_a_operations as operations


class EpisodeAController(original.EpisodeController):
    def validate_target(self, admission, approval):
        operations.adapter_pins(self.plan)
        super().validate_target(admission, approval)

    def validate_phase(self, admission):
        self.phase_result = operations.lightweight(self.plan, admission)


def execute(args):
    plan = original.pinned_json(args.plan, args.plan_sha256)
    plan['plan_sha256'] = args.plan_sha256
    operations.adapter_pins(plan)
    original.verify_controller_pins(plan)
    preflight = original.pinned_json(args.preflight, args.preflight_sha256)
    preflight['receipt_sha256'] = args.preflight_sha256
    approval = original.pinned_json(args.approval, args.approval_sha256)
    if args.action != 'stop':
        original.disk_guard()
    identity = original.strict_session_json(args.session / 'identity.json')
    action = 'start' if args.action == 'start' else 'stop' if args.action == 'stop' else 'poll' if args.action in ('poll', 'geometry-poll') else 'request'
    controller = EpisodeAController(args.session, identity, plan, preflight, approval, action)
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
            original.require(args.label in ('A0', 'A1'), 'Only A0/A1 labels permitted')
            result = original.arm(controller, args.label)
        else:
            result = original.poll_geometry(controller)
        result.update(episode='A', identity_sha256=controller.identity_hash,
                      owner=controller.state['owner'], plan_sha256=args.plan_sha256,
                      approval_sha256=args.approval_sha256,
                      phase_check=getattr(controller, 'phase_result', None))
        original.write_new(args.out, result)
        print(json.dumps(dict(state=result['state'], receipt=str(args.out))))
    finally:
        controller.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['start', 'request', 'poll', 'stop', 'arm', 'geometry-poll'])
    for name in ('plan', 'preflight', 'approval'):
        parser.add_argument('--' + name, type=Path, required=True)
        parser.add_argument('--' + name + '-sha256', required=True)
    parser.add_argument('--session', type=Path, required=True)
    parser.add_argument('--label', default='')
    parser.add_argument('--reason', default='maintainer-directed Episode A STOP')
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    try:
        execute(args)
    except operations.TimestampPending as error:
        original.write_new(args.out, dict(state='TIMESTAMP_CONTENT_CHECK_PENDING',
                                         action=args.action, diagnostic=str(error),
                                         automatic_abort=False, raw_verified=False))
        print(json.dumps(dict(state='TIMESTAMP_CONTENT_CHECK_PENDING', receipt=str(args.out))))
    except BaseException as error:
        try:
            original.write_new(args.out, dict(state='CHECK_ERROR', action=args.action, error=repr(error)))
        except OSError:
            pass
        raise


if __name__ == '__main__':
    main()
