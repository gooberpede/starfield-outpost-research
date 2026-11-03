# SPDX-License-Identifier: GPL-3.0-or-later
"""Exercise public B comparison using two real owned native fixture sessions.

Reads stopped fixtures and preserves their bytes. Temporarily substitutes only
baseline selection, retail identity/approval admission and input-inventory lookup
inside this disposable Python process; production CLI has no fixture switches.
The actual B reducer, separate-process relation, normalization, full byte oracle
and failure classifications remain unchanged. No launch, raw write or network.
"""
import sys
import os
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):
    raise RuntimeError('Use pinned Python -E -B without PYTHONOPTIMIZE, -O or -OO')
import argparse
import copy
import json
import shutil
from pathlib import Path
from types import SimpleNamespace
import d5al_baseline as baseline
import d5al_operations as operations
import d5al_stop as trusted
from common import fresh,inventory


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('plan',type=Path);p.add_argument('session',type=Path);p.add_argument('out',type=Path);a=p.parse_args()
    out=a.out.resolve();operations.require(out.is_relative_to(baseline.ROOT/'.local-work/d5al'),'New task-local output required');operations.guard();out.mkdir(parents=True,exist_ok=False)
    plan=baseline.canonical.load(a.plan);plan['plan_sha256']=operations.sha(a.plan)
    first=baseline.ROOT/'.local-work/d5ak/integration-final02/session';second=a.session.resolve()
    originals={str(p):inventory(p) for p in (first,second)}
    a_report=baseline.reducer.inspect(first,plan['dll_sha256'],baseline.TARGET,0x5e0de)
    before=next(o for o in a_report['observations'] if o['envelope']['snapshot_id']=='1')
    rawidentity=baseline.canonical.load(second/'identity.json')
    operations.require(rawidentity['retail'] is False,'Owned B fixture required')
    plan['game_sha256']=rawidentity['host_sha256']
    protected=dict(definitions={'owned.definition':'1'*64},config={'owned.profile':'2'*64},installed={'owned.image':dict(sha256='3'*64)},save52='owned.Save52',protected_live={'owned.Save52':dict(bytes=42,sha256='4'*64)})
    preflight=dict(state='PASS_OFFLINE_PREFLIGHT',plan_sha256=plan['plan_sha256'],protection=protected)
    prepath=out/'preflight.json';fresh(prepath,preflight)
    approval=dict(authority='D5AL_EPISODE_B_EXPLICIT_MAINTAINER_GO',episode='B',scope=plan['scope'],plan_sha256=plan['plan_sha256'],preflight_sha256=operations.sha(prepath),session=str(second),identity_sha256=operations.sha(second/'identity.json'),run_card_sha256=plan['run_card_sha256'],save52_sha256=plan['save52_sha256'],profile='Starfield - SFSE',steam_cloud='DISABLED')
    appath=out/'approval.fixture-only.json';fresh(appath,approval)
    postflight=dict(schema='sor-d5ai-postflight/1',episode='B',session=str(second),plan_sha256=plan['plan_sha256'],preflight_sha256=operations.sha(prepath),process_state='EXITED',status='PASS_POSTFLIGHT',protection_errors=[],capture_errors=[],owned_finalization=dict(identity_sha256=operations.sha(second/'identity.json')),fixture_only=True,scope='SYNTHETIC postflight eligibility premise; actual owned fixture PARTIAL receipt remains unchanged')
    postpath=out/'postflight.synthetic-premise.json';fresh(postpath,postflight)
    args=SimpleNamespace(postflight=postpath,postflight_sha256=operations.sha(postpath),session=second,before_snapshot=1,after_snapshot=1,preflight=prepath,preflight_sha256=operations.sha(prepath),approval=appath,approval_sha256=operations.sha(appath))
    tests=[]
    def check(name,value):tests.append(dict(name=name,passed=bool(value)));operations.require(value,name)
    def refuses(name,fn):
        try:fn()
        except (ValueError,KeyError,OSError,TypeError):check(name,True)
        else:check(name,False)
    saved_auth,saved_load,saved_approval,saved_producer=baseline.authenticate,baseline.canonical.load,trusted.authority,baseline.validate_producer
    baseline.authenticate=lambda value:dict(observation=before)
    try:
        # New B authority still validates without retail process admission.
        refuses('production-compare-refuses-native-nonretail-fixture',lambda:baseline.compare(args,plan))
        def load(path):
            path=Path(path)
            if path.resolve()==(baseline.NOTES/'preflight01/receipt.json').resolve():return dict(protection=copy.deepcopy(protected))
            return saved_load(path)
        baseline.canonical.load=load
        def fixture_producer(identity, value, session):
            operations.require(identity==rawidentity and Path(session)==second and identity['retail'] is False and identity['dll_sha256']==value['dll_sha256'], 'Exact owned fixture producer required')
        baseline.validate_producer=fixture_producer
        # Authority itself remains actual and fully hash-bound; only retail
        # identity lookup is modeled above, not process/query provenance.
        result=baseline.compare(args,plan)
        check('public-compare-actual-B-reducer-relation-and-bytes',result['result']['prediction']=='CONFIRMED' and result['result']['observation']=='REBUILT_IDENTICAL')
        fresh(out/'public-comparison.fixture-only.json',result)
        for name, mutate in (('wrong-label',lambda v:v['geometry_request'].__setitem__('label','A1')), ('wrong-arm-map',lambda v:v.__setitem__('d5al_arms',{'B1':1})), ('second-request',lambda v:v.__setitem__('geometry_last_request',2)), ('wrong-record-owner',lambda v:v['geometry_request'].__setitem__('owner','0'*32)), ('wrong-record-receipt',lambda v:v['geometry_request']['receipt'].__setitem__('sha256','0'*64))):
            folder=out/('binding-'+name);shutil.copytree(second,folder);state_path=folder/'p4-state.json';state=baseline.original.strict_session_json(state_path);mutate(state);state_path.write_text(json.dumps(state)+'\n',encoding='utf8',newline='\n')
            refuses('actual-owned-binding-'+name,lambda folder=folder:baseline.validate_capture_binding(folder,operations.sha(folder/'identity.json'),result['after']))
        for before_id,after_id in ((2,1),(1,2)):
            bad=copy.copy(args);bad.before_snapshot=before_id;bad.after_snapshot=after_id
            refuses('public-comparator-reject-snapshot-'+str((before_id,after_id)),lambda bad=bad:baseline.compare(bad,plan))
        bad=copy.copy(args);bad.approval=None
        refuses('public-compare-missing-approval',lambda:baseline.compare(bad,plan))
        changed=dict(approval);changed['authority']='D5AI_EPISODE_B_EXPLICIT_MAINTAINER_GO'
        changedpath=out/'historical-approval.fixture-only.json';fresh(changedpath,changed)
        bad=copy.copy(args);bad.approval=changedpath;bad.approval_sha256=operations.sha(changedpath)
        refuses('public-compare-stale-approval',lambda:baseline.compare(bad,plan))
        for name, mutate in (('definitions', lambda v:v['definitions'].__setitem__('owned.definition','0'*64)), ('configuration',lambda v:v['config'].__setitem__('owned.profile','0'*64)), ('Save52',lambda v:v['protected_live']['owned.Save52'].__setitem__('sha256','0'*64))):
            altered=copy.deepcopy(preflight);mutate(altered['protection']);pp=out/('changed-'+name+'-preflight.json');fresh(pp,altered)
            aa=dict(approval);aa['preflight_sha256']=operations.sha(pp);ap=out/('changed-'+name+'-approval.fixture-only.json');fresh(ap,aa)
            bad=copy.copy(args);bad.preflight=pp;bad.preflight_sha256=operations.sha(pp);bad.approval=ap;bad.approval_sha256=operations.sha(ap)
            post=copy.deepcopy(postflight);post['preflight_sha256']=operations.sha(pp);po=out/('changed-'+name+'-postflight.synthetic-premise.json');fresh(po,post);bad.postflight=po;bad.postflight_sha256=operations.sha(po)
            changed_result=baseline.compare(bad,plan)
            check('public-compare-changed-'+name+'-inconclusive',changed_result['result']['prediction']=='INCONCLUSIVE' and bool(changed_result['input_equivalence_mismatches']))
        for name,wrong in (('profile','different profile'),('steam_cloud','UNKNOWN')):
            aa=dict(approval);aa[name]=wrong;ap=out/('wrong-'+name+'-approval.fixture-only.json');fresh(ap,aa)
            bad=copy.copy(args);bad.approval=ap;bad.approval_sha256=operations.sha(ap)
            refuses('public-compare-wrong-'+name,lambda bad=bad:baseline.compare(bad,plan))
        for name, mutate in (('failed-protection',lambda v:v['protection_errors'].append('owned synthetic content difference')),('partial',lambda v:v.__setitem__('status','PARTIAL_POSTFLIGHT')),('wrong-identity',lambda v:v['owned_finalization'].__setitem__('identity_sha256','0'*64))):
            post=copy.deepcopy(postflight);mutate(post);po=out/('failed-'+name+'-postflight.synthetic-premise.json');fresh(po,post);bad=copy.copy(args);bad.postflight=po;bad.postflight_sha256=operations.sha(po)
            failed=baseline.compare(bad,plan)
            check('public-compare-'+name+'-postflight-inconclusive',failed['result']['prediction']=='INCONCLUSIVE' and 'full-protected-postflight' in failed['input_equivalence_mismatches'])
        check('original-fixture-identities-and-all-raw-files-preserved',all(inventory(Path(path))==value for path,value in originals.items()))
    finally:
        baseline.authenticate=saved_auth;baseline.canonical.load=saved_load;trusted.authority=saved_approval;baseline.validate_producer=saved_producer
    fresh(out/'qualification.json',dict(status='PASS',tests=tests,plan_sha256=operations.sha(a.plan),actual_A_fixture=str(first),actual_B_fixture=str(second),substitutions=['baseline authenticate returns qualified actual owned A0 fixture','pure retail producer namespace/site admission replaced by exact owned fixture producer validation','canonical A preflight lookup uses equal owned-fixture input inventory','explicitly synthetic successful postflight eligibility premise (actual fixture receipt remains PARTIAL)'],unmodified=['D5AL authority checks','actual native B reducer inspect','separate-process relation','full normalized byte equality and frozen assess','actual owned B0 arm/request1/capture binding'],limits='Fixture classification only. Production operator CLI has no seam and rejects nonretail fixture. Actual D5AI-PRED-01 remains NOT TESTED.'))
    print({'status':'PASS','checks':len(tests)})

if __name__=='__main__':main()
