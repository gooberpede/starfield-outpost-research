# SPDX-License-Identifier: GPL-3.0-or-later
"""D5AM minimal owned STOP and exact new-trial admission; SOR-P-0002 lineage.

Reads pinned controller sources, identity, plan, preflight and explicit approval;
writes only an owned session STOP/state and exclusive receipt. No launch,
deployment, target memory, save, configuration or network writes. Broad science
locks and disk/healthy-ACK checks are deliberately outside emergency STOP.
"""
import sys
import os
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):
    raise RuntimeError('Use pinned Python -E -B without PYTHONOPTIMIZE, -O or -OO')
from pathlib import Path
import d5ai_episode as original

ROOT = original.ROOT
LIVE = ROOT / '.local-work/d5am/live'
SCHEMA = 'sor-d5am-plan/1'
SCOPE = dict(processes=1, save52_loads=1, direct_travels=1, query_checkpoints=1,
             route=['Lodge', 'Feynman V Cu IL F'], new_saves=0,
             forced_regeneration=False, automatic_repeats=0, labels=['N0'])
EXTRA_RVAS = {
    'causal_sites': ([0x22cc410,0x22cc48f,0x22cc3f2,0x22cc366,0x2c45c2,0x2c45e7,
                     0x79fc85,0x79e027,0x21e0a87,0x79fcb3,0x22cc3c3,
                     0x7a51b7,0x7a5386,0x7a547c,0x982a5a,0x982a92],
                    [6,6,6,9,9,9,6,6,6,5,5,6,6,6,5,5]),
    'scheduler_sites': ([0x76cea4,0x76d07b,0x7b56c5,0x7b57eb,0x27ec100,
                        0x27e6a00,0x27e4ab0,0x27e4957,0x27e61a4,0x76d14f,
                        0x7b585f,0x28d3960,0x28d2b80], [5,5,5,5,5,5,5,8,7,5,5,5,5]),
}

def minimal_sources():
    return original.CONTROL_PATHS | {Path(__file__).resolve()}

def controller_pins(plan):
    pins = plan.get('d5am_controller_pins', {})
    original.require(len(pins) == len(minimal_sources()) and
                     {Path(p).resolve() for p in pins} == minimal_sources(),
                     'Exact D5AM minimal controller closure required')
    for path, digest in pins.items():
        original.require(original.sha(path) == digest, 'Minimal controller changed: '+path)
    original.require(Path(sys.executable).resolve() == Path(plan['python_executable']).resolve() and
                     original.sha(sys.executable) == plan['python_sha256'], 'Pinned interpreter required')

def scope(plan):
    original.require(plan.get('schema') == SCHEMA and plan.get('trial') == 'N0' and
                     original.same_structure(plan.get('scope'), SCOPE), 'Exact single N0 scope required')

def authority(plan, admission, approval, session, identity_hash):
    scope(plan)
    review = plan.get('review', {})
    original.require(review.get('state') == 'INDEPENDENTLY_REVIEWED_TECHNICAL_ACCEPT' and
                     review.get('scope') == 'D5AM_TECHNICAL_READINESS_ONLY' and
                     review.get('full_contract_disposition') == 'ESCALATE_AC01' and
                     review.get('known_deviations') == ['D5AM-AC01-subagent-cap'] and
                     review.get('prediction_sha256') == plan.get('prediction_sha256') and
                     review.get('run_card_sha256') == plan.get('run_card_sha256') and
                     isinstance(review.get('receipt_sha256'), str) and len(review['receipt_sha256']) == 64,
                     'Technical prediction/card review required; full-contract AC01 failure remains')
    disposition=approval.get('maintainer_disposition',{})
    original.require(disposition.get('deviation')=='D5AM-AC01-subagent-cap' and
                     disposition.get('decision')=='ACCEPT_EXCEPTION_FOR_SEPARATELY_AUTHORIZED_N0' and
                     disposition.get('review_receipt_sha256')==review['receipt_sha256'],
                     'Explicit maintainer disposition of known AC01 cap deviation required; technical review cannot waive it')
    original.require(admission.get('state') == 'PASS_OFFLINE_PREFLIGHT' and
                     admission.get('plan_sha256') == plan.get('plan_sha256'), 'Pinned full preflight required')
    original.require(approval.get('authority') == 'D5AM_N0_EXPLICIT_MAINTAINER_GO' and
                     approval.get('trial') == 'N0' and original.same_structure(approval.get('scope'), SCOPE),
                     'New D5AM N0 GO required; earlier episode authority is insufficient')
    original.require(approval.get('profile') == 'Starfield - SFSE' and
                     approval.get('steam_cloud') == 'DISABLED', 'Fresh profile/disabled Cloud confirmation required')
    pairs = {'plan_sha256':plan.get('plan_sha256'), 'preflight_sha256':admission.get('receipt_sha256'),
             'session':str(session), 'identity_sha256':identity_hash,
             'run_card_sha256':plan.get('run_card_sha256'), 'save52_sha256':plan.get('save52_sha256'),
             'prediction_sha256':plan.get('prediction_sha256'), 'review_receipt_sha256':review['receipt_sha256']}
    for key, value in pairs.items():
        original.require(value is not None and approval.get(key) == value, 'D5AM approval binding mismatch: '+key)

def distinct(identity, plan, identity_hash):
    prior = plan.get('prior_processes', [])
    original.require(len(prior) >= 3, 'All three original process identities required')
    for item in prior:
        original.require((identity['pid'],identity['creation_filetime']) != (item['pid'],item['creation_filetime']) and
                         identity['nonce'] != item['nonce'] and identity_hash != item['identity_sha256'],
                         'N0 needs a new birth/session distinct from every original')

def producer(expected, plan):
    original.require(expected.get('schema') == 'sor-d5x/4' and expected.get('retail') is True,
                     'Retail lifecycle identity required')
    original.require(Path(plan['process_image']).name == 'Starfield.exe', 'Wrong process image')
    for observed, pinned in [('host_sha256','game_sha256'),('sfse_sha256','sfse_sha256'),('dll_sha256','dll_sha256')]:
        original.require(expected.get(observed) == plan.get(pinned), 'Producer identity mismatch: '+observed)
    original.require(len(expected.get('sites', [])) == len(plan.get('sites', [])) == 18, 'All 18 base sites required')
    for actual, reference in zip(expected['sites'], plan['sites']):
        original.require(all(actual[k] == reference[k] for k in ('index','rva','guard_sha256')) and
                         actual['va'] == expected['module_base']+reference['rva'], 'Base site mismatch')
    original.validate_geometry_plan(expected, plan)
    original.require(expected.get('causal_bridge_admission_schema')==plan.get('causal_bridge_admission_schema')==
                     'sor-d5am-causal-bridge/1','Full native bridge admission accounting feature required')
    original.require(expected.get('scheduler_bridge_admission_schema')==plan.get('scheduler_bridge_admission_schema')==
                     'sor-d5am-scheduler-bridge/1','Full scheduler native admission required')
    original.require(expected.get('scheduler_dispatch_argument_schema')==plan.get('scheduler_dispatch_argument_schema')==
                     'r8-low-byte/1','Actual scheduler dispatch operand required')
    original.require(expected.get('scheduler_ready_serial_schema')==plan.get('scheduler_ready_serial_schema')==
                     'consumed-r9/1','Actual scheduler ready-tree serial operand required')
    for key, schema, count in [('causal','sor-d5am-causal/1',16),('scheduler','sor-d5am-scheduler/1',13)]:
        original.require(expected.get(key+'_schema') == plan.get(key+'_schema') == schema and
                         len(expected.get(key+'_sites', [])) == len(plan.get(key+'_sites', [])) == count,
                         'Full '+key+' site/schema identity required')
        for i, (actual, reference) in enumerate(zip(expected[key+'_sites'], plan[key+'_sites'])):
            original.require(actual['va'] == expected['module_base']+reference['rva'] and
                             actual['bytes'] == reference['bytes'] and
                             actual['guard_sha256'] == reference['guard_sha256'], key+' site mismatch')
            if key+'_sites' in EXTRA_RVAS:
                rvas, sizes = EXTRA_RVAS[key+'_sites']
                original.require(reference['rva'] == rvas[i] and reference['bytes'] == sizes[i], key+' site domain mismatch')
    original.require(expected.get('scheduler_event_bytes') == plan.get('scheduler_event_bytes') == 272,
                     'Scheduler event schema mismatch')
    original.require(expected.get('scheduler_vtable_guard_basis')==plan.get('scheduler_vtable_guard_basis')==
                     'preferred-image-vtable64/1','Explicit canonical DIR64 vtable guard basis required')
    original.require(len(expected.get('scheduler_targets',[]))==len(plan.get('scheduler_targets',[]))==6,
                     'Six statically pinned original target guards required')
    for actual,reference,index,rva in zip(expected['scheduler_targets'],plan['scheduler_targets'],
                                         [0,1,2,3,9,10],[0x27e5630]*4+[0x76c560,0x7b5160]):
        original.require(actual['site_index']==reference['site_index']==index and reference['rva']==rva and
                         actual['va']==expected['module_base']+rva and
                         actual['guard_sha256']==reference['guard_sha256'],'Original scheduler target mismatch')
    original.require(len(expected.get('causal_helpers',[]))==len(plan.get('causal_helpers',[]))==3,
                     'Three complete native helper body guards required')
    for actual,reference,(rva,size) in zip(expected['causal_helpers'],plan['causal_helpers'],
                                         [(0x22cc350,126),(0x22cc3d0,216),(0x2c45a0,81)]):
        original.require(reference['rva']==rva and reference['bytes']==actual['bytes']==size and
                         actual['va']==expected['module_base']+rva and
                         actual['guard_sha256']==reference['guard_sha256'],'Native helper full-body mismatch')
    original.require(len(expected.get('scheduler_vtables', [])) == len(plan.get('scheduler_vtables', [])) == 3,
                     'Three typed scheduler vtables required')
    for actual, reference, rva in zip(expected['scheduler_vtables'],plan['scheduler_vtables'],[0x4b3d0e8,0x4b3d138,0x4b406b8]):
        original.require(reference['rva'] == rva and actual['va'] == expected['module_base']+rva and
                         actual['guard_sha256'] == reference['guard_sha256'], 'Typed scheduler identity mismatch')
    reference, actual = plan['scheduler_callback'], expected['scheduler_callback']
    original.require(reference['rva'] == 0x27ec2e0 and actual['va'] == expected['module_base']+reference['rva'] and
                     actual['guard_sha256'] == reference['guard_sha256'], 'Scheduler callback mismatch')

class TrustedController(original.EpisodeController):
    def validate_target(self, admission, approval):
        controller_pins(self.plan)
        original.require(self.session.parent == LIVE == Path(self.plan['live_root']).resolve() and
                         self.session.name == 'session-'+self.expected['nonce'], 'Wrong D5AM session namespace')
        producer(self.expected,self.plan)
        distinct(self.expected,self.plan,self.identity_hash)
        authority(self.plan,admission,approval,self.session,self.identity_hash)

def main():
    import argparse
    p=argparse.ArgumentParser(description=__doc__)
    for name in ('plan','preflight','approval'):
        p.add_argument('--'+name,type=Path,required=True);p.add_argument('--'+name+'-sha256',required=True)
    p.add_argument('--session',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    p.add_argument('--reason',default='operator-directed D5AM N0 owned STOP')
    a=p.parse_args()
    original.require(a.out.resolve().is_relative_to(ROOT/'.local-work/d5am'), 'D5AM exclusive receipt required')
    plan=original.pinned_json(a.plan,a.plan_sha256);plan['plan_sha256']=a.plan_sha256
    before=original.pinned_json(a.preflight,a.preflight_sha256);before['receipt_sha256']=a.preflight_sha256
    c=TrustedController(a.session,original.strict_session_json(a.session/'identity.json'),plan,before,
                        original.pinned_json(a.approval,a.approval_sha256),'stop')
    try: original.write_new(a.out,c.request_stop(a.reason))
    finally:c.close()

if __name__=='__main__':main()
