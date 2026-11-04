# SPDX-License-Identifier: GPL-3.0-or-later
# D5AN owned derivative of d5am_n1_episode.py; exact origin pins in operations-lineage.json.
"""Single N2 controller, source-informed D5AL/D5AI owned mechanisms (SOR-P-0002).

Reads exact pinned approval/protection and native metadata; writes only owned
worker requests, one immutable geometry arm and exclusive receipts. No game
launch, query automation, deployment, memory, save or network actions.
"""
import sys
import os
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):
    raise RuntimeError('Use pinned Python -E -B without PYTHONOPTIMIZE, -O or -OO')
import argparse
import json
from pathlib import Path
import d5an_n2_stop as trusted
import d5ai_episode as original

def recorder_health(ack):
    original.require(ack.get('counter_fault_schema')=='sor-d5an-counter/1', 'Missing D5AN fault schema')
    for key in ('publication','ids','id','producer','class','value','thread','address','return_va','enabled','scheduler_bits','causal_bits'):
        value=ack.get('counter_fault_'+key)
        original.require(type(value) is int and value==0, 'Counter fault or incomplete diagnostic: '+key)
    for key in ('geometry_failed','lifetime_failed','causal_failed','scheduler_failed',
                'causal_counter_overflow','scheduler_counter_overflow','scheduler_counter_contention'):
        original.require(ack.get(key) is False, 'Recorder failure or missing metric: '+key)
    for key in ('geometry_no_slot','lifetime_drops','lifetime_unlogged_cutoff_ticks',
                'causal_drops','causal_reentrant','causal_native_counter_faults','scheduler_drops','scheduler_reentrant'):
        original.require(type(ack.get(key)) is int and ack[key] == 0, 'Recorder loss or missing metric: '+key)
    for channel in ('causal','scheduler'):
        written,enqueued=ack.get(channel+'_written'),ack.get(channel+'_enqueued')
        original.require(type(written) is int and type(enqueued) is int and
                         0 <= written <= enqueued < 2**64, 'Invalid flushed channel counters')
    for key in ('causal_bridge_active','causal_active','scheduler_active','scheduler_bridge_active',
                'scheduler_registry_faults','scheduler_identity_faults'):
        original.require(type(ack.get(key)) is int and 0<=ack[key]<2**64,
                         'Missing or invalid native accounting: '+key)
    # Open producers and registry/identity science uncertainty do not turn an
    # otherwise flushed worker ACK into a claim of complete task coverage.

class N2Controller(trusted.TrustedController):
    def validate_target(self,admission,approval):
        import d5an_n2_operations as operations
        operations.source_pins(self.plan)
        super().validate_target(admission,approval)
    def validate_phase(self,admission):
        import d5an_n2_operations as operations
        self.phase_result=operations.lightweight(self.plan,admission)
    def poll(self):
        value=super().poll()
        if value['state']=='HEALTHY_ACK':recorder_health(value['ack'])
        return value

def arm_once(controller,label):
    original.require(label=='N2','Only the single N2 label is permitted')
    history=controller.state.setdefault('d5an_n2_arms',{})
    current=controller.state.get('geometry_request')
    if history:
        original.require(history=={'N2':1} and current and current['label']=='N2' and
                         current['request_id']==1, 'No second N2 request or retry')
        if (controller.session/'geometry-request-1.json').exists():
            captured=original.poll_geometry(controller)
            return dict(state='GEOMETRY_ALREADY_CONSUMED',geometry_request=captured['geometry_request'],
                        natural_early_capture_inspected=True,automatic_retry=False)
        if current['state'] not in ('ARMED','PUBLICATION_PENDING'):
            return dict(state='GEOMETRY_ALREADY_CONSUMED',geometry_request=current,automatic_retry=False)
    else:original.require(not current and not controller.state.get('geometry_last_request'),'N2 must be first and only arm')
    value=original.arm(controller,label)
    current=controller.state.get('geometry_request')
    if current:
        original.require(current['request_id']==1,'Only native request 1 permitted')
        history['N2']=1;controller.save()
    return value

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('action',choices=('start','request','poll','arm','geometry-poll','stop'))
    for name in ('plan','preflight','approval'):
        p.add_argument('--'+name,type=Path,required=True);p.add_argument('--'+name+'-sha256',required=True)
    p.add_argument('--session',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    p.add_argument('--label',default='N2');p.add_argument('--reason',default='operator-directed D5AM N2 STOP')
    a=p.parse_args();original.require(a.out.resolve().is_relative_to(trusted.ROOT/'.local-work/d5an'),'D5AM receipt required')
    plan=original.pinned_json(a.plan,a.plan_sha256);plan['plan_sha256']=a.plan_sha256
    before=original.pinned_json(a.preflight,a.preflight_sha256);before['receipt_sha256']=a.preflight_sha256
    cls=trusted.TrustedController if a.action=='stop' else N2Controller
    c=cls(a.session,original.strict_session_json(a.session/'identity.json'),plan,before,
          original.pinned_json(a.approval,a.approval_sha256),'start' if a.action=='start' else
          'stop' if a.action=='stop' else 'poll' if a.action in ('poll','geometry-poll') else 'request')
    try:
        if a.action=='start':value=dict(state='BOUND_READY',raw_verified=False)
        elif a.action=='arm':value=arm_once(c,a.label)
        elif a.action=='geometry-poll':value=original.poll_geometry(c)
        elif a.action=='stop':value=c.request_stop(a.reason)
        else:value=getattr(c,a.action)()
        value.update(trial='N2',identity_sha256=c.identity_hash,plan_sha256=a.plan_sha256,
                     phase_check=getattr(c,'phase_result',None))
        original.write_new(a.out,value)
    finally:c.close()
    print(json.dumps(dict(state=value['state'],receipt=str(a.out))))

if __name__=='__main__':main()
