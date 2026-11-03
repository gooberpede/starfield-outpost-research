# SPDX-License-Identifier: GPL-3.0-or-later
"""B-only controller and read-only D5AJ checkpoint/comparison.

SOR-P-0002 adaptation of D5AK. Reads pinned operational inputs and new B evidence;
writes exclusive receipts and separately approved owned worker requests. No
launch, deployment, gameplay automation, original-save write or network action.
"""
import sys
import os
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):
    raise RuntimeError('Use pinned Python -E -B without PYTHONOPTIMIZE, -O or -OO')
import argparse
import json
from pathlib import Path
import d5ai_episode as original
import d5al_operations as operations
import d5al_stop as trusted
import d5aj_checkpoint as checkpoint
import d5al_baseline as baseline
TARGET = '0:37536:20928:0029d20e'
OWNER_FORMID = '0005e0de'


def frozen_subject(target, owner):
    original.require(target == TARGET and owner == int(OWNER_FORMID,16), 'Exact frozen target and owner required')


class EpisodeBController(trusted.TrustedController):
    def validate_target(self, admission, approval):
        operations.source_pins(self.plan)
        super().validate_target(admission, approval)

    def validate_phase(self, admission):
        self.phase_result = operations.lightweight(self.plan, admission)

    def poll(self):
        value = super().poll()
        if value['state'] == 'HEALTHY_ACK':
            ack = value['ack']
            original.require(ack.get('geometry_failed') is False and ack.get('geometry_no_slot') == 0 and
                             ack.get('lifetime_failed') is False and ack.get('lifetime_drops') == 0 and
                             ack.get('lifetime_unlogged_cutoff_ticks') == 0, 'Actual recorder integrity failure')
        return value


def arm_once(controller, label):
    original.require(label == 'B0', 'Only the single B0 label is permitted')
    history = controller.state.setdefault('d5al_arms', {})
    current = controller.state.get('geometry_request')
    if history:
        original.require(set(history) == {'B0'} and current and current['label'] == label and
                         current['request_id'] == history[label], 'No second B request')
        if (controller.session / f"geometry-request-{current['request_id']}.json").exists():
            captured = original.poll_geometry(controller)
            return dict(state='GEOMETRY_ALREADY_CONSUMED', geometry_request=captured['geometry_request'],
                        natural_early_capture_inspected=True, automatic_retry=False)
        if current['state'] not in ('ARMED','PUBLICATION_PENDING'):
            return dict(state='GEOMETRY_ALREADY_CONSUMED',geometry_request=current,automatic_retry=False)
    else:
        original.require(not current and not controller.state.get('geometry_last_request'), 'B0 must be the first arm')
    value = original.arm(controller,label)
    current = controller.state.get('geometry_request')
    if current:
        history['B0'] = current['request_id']
        original.require(current['request_id'] == 1, 'Only native request 1 is permitted')
        controller.save()
    return value


def qualify(args, plan):
    operations.source_pins(plan)
    frozen_subject(args.target,int(args.owner_formid,16))
    identity = original.strict_session_json(args.session / 'identity.json')
    trusted.distinct(identity,plan,original.sha(args.session / 'identity.json'))
    original.require(args.snapshot == 1, 'Only initial B0 snapshot 1 permitted')
    result = checkpoint.inspect_prefix(args.session,plan['dll_sha256'],1,args.nonce,args.target,int(args.owner_formid,16))
    result.update(plan_sha256=args.plan_sha256,d5al_source_lock_sha256=plan['d5al_source_lock_sha256'],
                  d5aj_source_lock_sha256=plan['d5aj_source_lock_sha256'],automatic_stop=False)
    return result


def compare_session(args,plan):
    operations.source_pins(plan)
    frozen_subject(args.target, int(args.owner_formid, 16))
    return baseline.compare(args,plan)


def execute(args):
    plan = original.pinned_json(args.plan,args.plan_sha256)
    plan['plan_sha256'] = args.plan_sha256
    operations.source_pins(plan)
    original.verify_controller_pins(plan)
    if args.action in ('checkpoint','compare'):
        original.disk_guard()
        return qualify(args,plan) if args.action == 'checkpoint' else compare_session(args,plan)
    before = original.pinned_json(args.preflight,args.preflight_sha256)
    before['receipt_sha256'] = args.preflight_sha256
    approval = original.pinned_json(args.approval,args.approval_sha256)
    if args.action != 'stop': original.disk_guard()
    action = 'poll' if args.action in ('poll','geometry-poll') else 'start' if args.action == 'start' else 'stop' if args.action == 'stop' else 'request'
    controller = EpisodeBController(args.session, original.strict_session_json(args.session/'identity.json'),plan,before,approval,action)
    try:
        if args.action == 'start': result = dict(state='BOUND_READY',raw_verified=False)
        elif args.action == 'arm': result = arm_once(controller,args.label)
        elif args.action == 'geometry-poll': result = original.poll_geometry(controller)
        elif args.action == 'stop': result = controller.request_stop(args.reason)
        else: result = getattr(controller,args.action)()
        result.update(episode='B',identity_sha256=controller.identity_hash,plan_sha256=args.plan_sha256,
                      approval_sha256=args.approval_sha256,phase_check=getattr(controller,'phase_result',None))
        return result
    finally: controller.close()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('action',choices=('start','request','poll','arm','geometry-poll','checkpoint','compare','stop'))
    for name in ('plan','preflight','approval','postflight'):
        p.add_argument('--'+name,type=Path,required=name=='plan')
        p.add_argument('--'+name+'-sha256',required=name=='plan')
    p.add_argument('--session',type=Path,required=True)
    p.add_argument('--label',default='B0')
    p.add_argument('--reason',default='operator-directed D5AL B STOP')
    p.add_argument('--snapshot',type=int,default=1)
    p.add_argument('--before-snapshot',type=int,default=1)
    p.add_argument('--after-snapshot',type=int,default=1)
    p.add_argument('--nonce')
    p.add_argument('--target',default=TARGET)
    p.add_argument('--owner-formid',default=OWNER_FORMID)
    p.add_argument('--out',type=Path,required=True)
    args=p.parse_args()
    original.require(args.out.resolve().is_relative_to(original.ROOT/'.local-work/d5al'),'Exclusive D5AL receipt required')
    try: result=execute(args)
    except operations.content.TimestampPending as error:
        result=dict(state='TIMESTAMP_CONTENT_CHECK_PENDING',diagnostic=str(error),automatic_stop=False)
    except BaseException as error:
        original.write_new(args.out,dict(state='CHECK_ERROR',action=args.action,error=repr(error),automatic_stop=False))
        raise
    original.write_new(args.out,result)
    print(json.dumps(dict(state=result['state'],receipt=str(args.out))))

if __name__ == '__main__': main()
