# SPDX-License-Identifier: GPL-3.0-or-later
"""Prospective Episode A controller and source-scoped read-only checkpoint.

SOR-P-0002: integrates frozen D5AI owner/worker/arm/STOP mechanisms and D5AJ
qualification. Controller actions require separately hash-bound maintainer GO.
Checkpoint only reads evidence; it cannot issue an arm, travel or STOP. Writes
exclusive receipts and, for approved controller actions, owned session commands.
No launch, deployment, save access, attachment, forced refresh or network.
"""
import sys
if not __debug__ or sys.flags.optimize:
    raise RuntimeError('Use the pinned Python interpreter with -E -B; optimization is forbidden')

import argparse
import json
from pathlib import Path

import d5ai_episode as original
import d5ak_operations as operations
import d5aj_checkpoint as checkpoint

TARGET = '0:37536:20928:0029d20e'
OWNER_FORMID = '0005e0de'


def frozen_subject(target, owner):
    original.require(target == TARGET and owner == int(OWNER_FORMID, 16),
                     'D5AK requires the frozen Feynman target and body owner')


class EpisodeAController(original.EpisodeController):
    def validate_target(self, admission, approval):
        operations.source_pins(self.plan)
        super().validate_target(admission, approval)

    def validate_phase(self, admission):
        self.phase_result = operations.lightweight(self.plan, admission)

    def poll(self):
        value = super().poll()
        if value['state'] == 'HEALTHY_ACK':
            ack = value['ack']
            original.require(ack.get('geometry_failed') is False and
                             ack.get('geometry_no_slot') == 0 and
                             ack.get('lifetime_failed') is False and
                             ack.get('lifetime_drops') == 0 and
                             ack.get('lifetime_unlogged_cutoff_ticks') == 0,
                             'Actual geometry/lifetime recorder integrity failure')
        return value


def arm_once(controller, label):
    """Reconnect a pending arm; never arm a consumed label again."""
    original.require(label in ('A0', 'A1'), 'Only A0/A1 labels permitted')
    history = controller.state.setdefault('d5ak_arms', {})
    current = controller.state.get('geometry_request')
    if label in history:
        original.require(current and current['label'] == label and
                         current['request_id'] == history[label], 'Consumed checkpoint cannot be rearmed')
        if current['state'] not in ('ARMED', 'PUBLICATION_PENDING'):
            return dict(state='GEOMETRY_ALREADY_CONSUMED', geometry_request=current,
                        raw_verified=False, automatic_retry=False)
    elif label == 'A0':
        original.require(not history and not current, 'A0 must be the first and only baseline arm')
    else:
        original.require(set(history) == {'A0'} and controller.state.get('d5ak_departure_gate'),
                         'Qualified baseline and explicit departure check required before A1')
    result = original.arm(controller, label)
    current = controller.state.get('geometry_request')
    if current and current['label'] == label:
        history[label] = current['request_id']
        controller.save()
    return result


def departure_check(controller, certificate, plan_hash):
    """Require exact A0 identity plus a fresh current worker challenge ACK."""
    original.require(certificate.get('state') == 'BASELINE_PREFIX_QUALIFIED' and
                     certificate.get('method') == 'sor-d5aj-source-grid/1' and
                     certificate.get('plan_sha256') == plan_hash and
                     certificate.get('identity_sha256') == controller.identity_hash,
                     'A qualified source-scoped certificate for this plan/session is indispensable')
    envelope = certificate.get('envelope', {})
    original.require(envelope.get('source') == dict(key=TARGET, body_formid=OWNER_FORMID) and
                     envelope.get('frame', {}).get('owner_formid') == OWNER_FORMID and
                     certificate.get('proof', {}).get('owner_context', {}).get('owner_formid') == OWNER_FORMID,
                     'Departure certificate must qualify the exact frozen target and owner')
    arm = controller.state.get('geometry_request', {})
    receipt = arm.get('receipt', {})
    original.require(arm.get('label') == 'A0' and
                     receipt.get('snapshot_id') == certificate.get('snapshot_id') and
                     receipt.get('sha256') == certificate.get('snapshot_sha256') and
                     controller.state.get('d5ak_arms', {}).get('A0') == arm.get('request_id'),
                     'Certificate does not bind this owned completed A0 arm')
    health = controller.poll()
    if health['state'] != 'HEALTHY_ACK':
        return dict(state='HOLD_DEPARTURE', health=health, permission_to_depart=False,
                    automatic_stop=False)
    ack = health['ack']
    original.require(ack.get('geometry_failed') is False and ack.get('lifetime_failed') is False and
                     ack.get('lifetime_unlogged_cutoff_ticks') == 0 and
                     ack.get('lifetime_drops') == 0 and
                     ack.get('request_nonce') != certificate['request_nonce'] and
                     ack.get('lifetime_flushed', -1) >= certificate['lifetime']['records'] and
                     ack.get('lifetime_acknowledged') == ack.get('lifetime_flushed') and
                     ack.get('lifetime_qualified_through_ticks', -1) >= certificate['lifetime']['qualified_through_ticks'] and
                     ack.get('flushed', -1) >= certificate['acknowledged_records'],
                     'Current worker cannot support baseline departure')
    controller.state['d5ak_departure_gate'] = dict(snapshot_id=certificate['snapshot_id'],
                                                  snapshot_sha256=certificate['snapshot_sha256'],
                                                  request_nonce=ack['request_nonce'])
    controller.save()
    return dict(state='BASELINE_AND_CURRENT_HEALTH_QUALIFIED', permission_to_depart=True,
                scope='Only separately approved ordinary Lodge departure and Feynman return')


def qualify(args, plan):
    """Analyze the same captured bytes repeatedly without issuing controller work."""
    operations.source_pins(plan)
    frozen_subject(args.target, int(args.owner_formid, 16))
    result = checkpoint.inspect_prefix(args.session, plan['dll_sha256'], args.snapshot,
                                       args.nonce, args.target, int(args.owner_formid, 16))
    result.update(plan_sha256=args.plan_sha256,
                  d5ak_source_lock_sha256=plan['d5ak_source_lock_sha256'],
                  d5aj_source_lock_sha256=plan['d5aj_source_lock_sha256'],
                  method_sha256=original.sha(checkpoint.__file__))
    return result


def compare_session(args, plan):
    """Compare two stopped Episode A boundaries under the exact same lock."""
    operations.source_pins(plan)
    frozen_subject(args.target, int(args.owner_formid, 16))
    reducer = checkpoint.reducer
    report = reducer.inspect(args.session, plan['dll_sha256'], args.target, int(args.owner_formid, 16))
    def find(identifier):
        found = [row for row in report['observations'] if row['envelope']['snapshot_id'] == str(identifier)]
        original.require(len(found) == 1, 'Unique qualified comparison boundary required: ' + str(identifier))
        return found[0]
    before, after = find(args.before_snapshot), find(args.after_snapshot)
    original.require(args.before_snapshot != args.after_snapshot and
                     before['proof']['header']['completion_ticks'] < after['proof']['header']['ticks_begin'],
                     'Ordered distinct A0/A1 consumer boundaries required')
    certificate = reducer.relation(before, after, report['events'], report['events'], report['lifetime'])
    comparison = reducer.compare(before['envelope'], after['envelope'], certificate)
    return dict(state='COMPARISON_REPORTED', result=comparison, certificate=certificate,
                before=before, after=after, refused=report['refused'],
                lifecycle_raw_sha256=report['lifecycle_raw_sha256'],
                method_sha256=original.sha(reducer.__file__), plan_sha256=args.plan_sha256,
                d5ak_source_lock_sha256=plan['d5ak_source_lock_sha256'],
                d5aj_source_lock_sha256=plan['d5aj_source_lock_sha256'],
                authority='NO_EPISODE_B_OR_RETRY_AUTHORITY')


def execute(args):
    plan = original.pinned_json(args.plan, args.plan_sha256)
    plan['plan_sha256'] = args.plan_sha256
    operations.source_pins(plan)
    original.verify_controller_pins(plan)
    if args.action in ('checkpoint', 'compare'):
        original.disk_guard()
        return qualify(args, plan) if args.action == 'checkpoint' else compare_session(args, plan)
    preflight = original.pinned_json(args.preflight, args.preflight_sha256)
    preflight['receipt_sha256'] = args.preflight_sha256
    approval = original.pinned_json(args.approval, args.approval_sha256)
    if args.action != 'stop':
        original.disk_guard()
    identity = original.strict_session_json(args.session / 'identity.json')
    action = ('start' if args.action == 'start' else 'stop' if args.action == 'stop' else
              'poll' if args.action in ('poll', 'geometry-poll', 'departure-check') else 'request')
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
            result = arm_once(controller, args.label)
        elif args.action == 'departure-check':
            result = departure_check(controller, original.pinned_json(args.certificate, args.certificate_sha256), args.plan_sha256)
        else:
            result = original.poll_geometry(controller)
        result.update(episode='A', identity_sha256=controller.identity_hash,
                      owner=controller.state['owner'], plan_sha256=args.plan_sha256,
                      approval_sha256=args.approval_sha256,
                      phase_check=getattr(controller, 'phase_result', None))
        return result
    finally:
        controller.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('start', 'request', 'poll', 'stop', 'arm',
                                           'geometry-poll', 'checkpoint', 'departure-check', 'compare'))
    for name in ('plan', 'preflight', 'approval', 'certificate'):
        parser.add_argument('--' + name, type=Path, required=name == 'plan')
        parser.add_argument('--' + name + '-sha256', required=name == 'plan')
    parser.add_argument('--session', type=Path, required=True)
    parser.add_argument('--label', default='')
    parser.add_argument('--reason', default='maintainer-directed D5AK Episode A STOP')
    parser.add_argument('--snapshot', type=int, default=1)
    parser.add_argument('--before-snapshot', type=int, default=1)
    parser.add_argument('--after-snapshot', type=int, default=2)
    parser.add_argument('--nonce')
    parser.add_argument('--target', default=checkpoint.reducer.read_capture.TARGET)
    parser.add_argument('--owner-formid', default='0005e0de')
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    original.require(args.out.resolve().is_relative_to(original.ROOT / '.local-work/d5ak'),
                     'Exclusive D5AK receipt path required')
    try:
        result = execute(args)
    except operations.content.TimestampPending as error:
        result = dict(state='TIMESTAMP_CONTENT_CHECK_PENDING', diagnostic=str(error),
                      automatic_stop=False, permission_to_depart=False)
    except BaseException as error:
        # Preserve the actual cause. This receipt itself never writes STOP or
        # retires acquisition; the approved card distinguishes integrity faults
        # from scientific refusal and always holds the dependent gameplay action.
        original.write_new(args.out, dict(state='CHECK_ERROR', action=args.action,
                                          error=repr(error), permission_to_depart=False,
                                          automatic_stop=False))
        raise
    original.write_new(args.out, result)
    print(json.dumps(dict(state=result['state'], receipt=str(args.out))))


if __name__ == '__main__':
    main()
