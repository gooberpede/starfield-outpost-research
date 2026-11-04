# SPDX-License-Identifier: GPL-3.0-or-later
# D5AN owned derivative of d5am_n1_operations.py; exact origin pins in operations-lineage.json.
"""D5AM N2 offline pre/postflight and exact operational closure (SOR-P-0002).

Adapts owned P4 preservation and D5AL content comparison without projecting
episode authority. Reads pins/protected inputs; writes fresh receipts and owned
restoration copies only. No launch, deployment, original save or network writes.
"""
import sys
import os
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):
    raise RuntimeError('Use pinned Python -E -B without PYTHONOPTIMIZE, -O or -OO')
import argparse
import copy
import json
from pathlib import Path
import d5an_n2_stop as trusted
import d5an_n2_content as content
import d5ai_operations as original
from d5ai_episode import ROOT,require,sha,strict_session_json
from common import fresh,guard,regular

POLICY='sor-d5an-n2-operational-lock/1'

def required_sources():
    # Exact conservative closure of the reused owned preservation machinery.
    # D5AL's list supplies source filenames only, never an authority decision.
    import d5al_operations
    return (d5al_operations.required_sources() | {Path(d5al_operations.__file__).resolve()} |
            {Path(__file__).with_name(name).resolve() for name in
             ('d5an_n2_stop.py','d5an_n2_episode.py','d5an_n2_operations.py','d5an_n2_content.py',
              'd5an_readiness.py','d5an_n2_operations_qualify.py','d5an_n2_archive.py','d5am_join_causal.py','d5ad_baseline.py',
              'd5am_n1_prediction_oracle.py','d5am_n1_prediction_controls.py','d5am_scheduler_qualify.py',
              'd5am-scheduler-fixture.cpp','d5am-scheduler-fixture.asm','d5am_lock_qualify.py',
              'd5am-lock-component.cpp','d5am-lock-bridges.asm','d5am_abi_qualify.py',
              'd5am-abi-driver.cpp','d5am-abi-driver.asm','d5am_causal_controls.py',
              'd5am_scheduler_reader_controls.py','d5am_relocation_census.py','d5am_scheduler_recheck.py')} |
            {ROOT/'runtime/construction-winner'/name for name in
             ('d5am_read_causal.py','d5am_read_scheduler.py','d5am_causality.h','d5am_causality.asm',
              'd5am_scheduler.h','d5am_scheduler.asm','d5an_read_counter.py','d5an_read_causal.py')})

def source_pins(plan):
    trusted.scope(plan);trusted.controller_pins(plan)
    lock=original.pinned_json(plan['d5an_n2_source_lock'],plan['d5an_n2_source_lock_sha256'])
    require(lock.get('schema')==POLICY,'D5AM operational source lock required')
    require(Path(lock['interpreter']).resolve()==Path(sys.executable).resolve() and
            sha(sys.executable)==lock['interpreter_sha256'],'Pinned interpreter mismatch')
    expected=required_sources()|{Path(p).resolve() for p in plan['package_pins']}
    pins=lock['sources']
    require(len(pins)==len(expected) and {Path(p).resolve() for p in pins}==expected,'Exact D5AM source closure required')
    for path,digest in pins.items():require(sha(regular(path))==digest,'D5AM locked input changed: '+path)
    require(lock['dll_sha256']==plan['dll_sha256'],'D5AM producer lock mismatch')
    return lock

def legacy():return original.legacy()

def component_plan(plan):
    """Project only source-pinned, scientifically neutral preservation fields."""
    value=copy.deepcopy(plan);value['schema']='sor-d5ab-p4-plan/1'
    value['operations_sha256']=sha(original.LEGACY_PATH)
    value['phase_pins']={str(p):sha(p) for p in original.LEGACY_PHASES}
    return value

def verify_plan(plan):
    source_pins(plan)
    require(plan.get('timestamp_policy')==content.POLICY,'D5AM content-first plan required')
    legacy().verify_plan(component_plan(plan))
    for stem in ('run_card','prediction'):
        require(sha(regular(plan[stem+'_path']))==plan[stem+'_sha256'],stem+' source changed')
    require(Path(plan['live_root']).resolve()==trusted.LIVE,'Fresh D5AM live namespace required')
    require(plan.get('native_version')=='0.9.2','D5AM producer required')

def lightweight(plan,before):return content.lightweight(plan,before)

def preflight(plan,plan_hash,out):
    verify_plan(plan);module=legacy()
    value=module.preflight(component_plan(plan),plan_hash,out)
    value['protection']['archive_content_sha256']=content.archive_hashes(value['protection'])
    protected=value['protection']['protected_live']
    require(plan['save52_name'] in protected and protected[plan['save52_name']]['sha256']==plan['save52_sha256'],
            'Protected Save52 differs from frozen input')
    source_pins(plan)
    value.update(schema='sor-d5an-n2-preflight/1',trial='N2',scope=trusted.SCOPE,
                 authority='D5AM_OFFLINE_ONLY_NO_LIVE_GO',timestamp_policy=content.POLICY,
                 prediction_sha256=plan['prediction_sha256'],review=plan['review'])
    return value

def finalization(plan,before,session,approval):
    identity=strict_session_json(session/'identity.json')
    c=trusted.TrustedController.__new__(trusted.TrustedController)
    c.session,c.expected,c.plan=session,identity,plan;c.identity_hash=sha(session/'identity.json')
    c.validate_target(before,approval)
    require(session.name not in before['existing_sessions'],'Old session refused')
    state=strict_session_json(session/'p4-state.json');stop=state.get('stop')
    require(state['identity_sha256']==c.identity_hash and stop and stop['identity_sha256']==c.identity_hash and
            stop['owner']==state['owner'] and len(state['owner'])==32 and len(stop['stop_nonce'])==32,'Owned STOP required')
    require((session/'STOP').read_bytes()==(json.dumps(stop,sort_keys=True)+'\n').encode(),'Foreign STOP')
    terminal=strict_session_json(session/'terminal.json')
    require(all(terminal.get(k)==v for k,v in identity.items()) and terminal['resident_inert'] is True and
            not state['telemetry_fault'],'Invalid closed identity/state')
    return dict(identity_sha256=c.identity_hash,owner=state['owner'],stop_nonce=stop['stop_nonce'])

def postflight(plan,before,session,approval,out):
    verify_plan(plan);module=legacy();session=regular(session)
    process_state=module.original_process_gone(strict_session_json(session/'identity.json'))
    errors,capture_errors=[],[];owned=None;comparisons=[]
    try:owned=finalization(plan,before,session,approval)
    except (AssertionError,OSError,KeyError,ValueError) as e:capture_errors.append(str(e))
    try:
        after=module.full(out);after['archive_content_sha256']=content.archive_hashes(after)
        comparisons.append(content.compare_protection(before['protection'],after))
        require(before['remote_protected_sizes']==module.remote_sizes(after),'Remote protected saves changed')
        require(not Path(plan['deployed_dll']).exists(),'Disable effective candidate after exit')
    except (AssertionError,OSError,ValueError) as e:errors.append(str(e))
    from read_capture import inspect
    from d5ai_read_geometry import read_session
    from d5ai_read_lifetime import read_prefix
    scientific=geometry=lifetime=None
    try:scientific=inspect(session,plan['dll_sha256'])
    except (ValueError,OSError,KeyError) as e:capture_errors.append('Core: '+str(e))
    try:
        geometry=read_session(session);capture_errors.extend(e['error'] for e in geometry['errors'])
    except (ValueError,OSError,KeyError) as e:capture_errors.append(str(e))
    try:lifetime=read_prefix(session,strict_session_json(session/'terminal.json'))
    except (ValueError,OSError,KeyError) as e:capture_errors.append(str(e))
    causal=scheduler=joins=counter=None
    try:
        from d5an_read_counter import read as counter_read
        counter=counter_read(session,plan['dll_sha256'],plan['dll'])
        require(counter['complete'] and counter['disposition']=='NO_COUNTER_FAULT_RECORDED','Counter fault or incomplete diagnostic provenance')
    except (ValueError,OSError,KeyError) as e:capture_errors.append('Counter diagnostics: '+str(e))
    try:
        from d5an_read_causal import read as causal_read
        from d5am_read_scheduler import read as scheduler_read
        causal=causal_read(session,plan['dll_sha256'])
        require(causal['sidecar_accounting_complete'],'Causal byte accounting incomplete')
        require(causal.get('native_bridge_accounting_complete') is True,'Causal full native bridge admission incomplete')
    except (ValueError,OSError,KeyError) as e:capture_errors.append(str(e))
    try:
        from d5am_read_scheduler import read as scheduler_read
        scheduler=scheduler_read(session,plan['dll_sha256'])
        require(scheduler['byte_accounting_complete'],'Scheduler byte accounting incomplete')
        require(scheduler.get('native_bridge_accounting_complete') is True,'Scheduler full native admission incomplete')
    except (ValueError,OSError,KeyError) as e:capture_errors.append(str(e))
    try:
        import d5am_join_causal
        joins=d5am_join_causal.inspect(session,plan['dll_sha256'])
    except (ValueError,OSError,KeyError) as e:capture_errors.append('Cross-channel join integrity: '+str(e))
    status='PASS_POSTFLIGHT' if not errors and not capture_errors and scientific and scientific.get('complete_session') else 'PARTIAL_POSTFLIGHT'
    reader_paths=[ROOT/'runtime/construction-winner'/n for n in ('d5an_read_causal.py','d5am_read_scheduler.py','d5an_read_counter.py')]
    reader_paths.append(Path(__file__).with_name('d5am_join_causal.py'))
    return dict(schema='sor-d5an-n2-postflight/1',action='postflight',session=str(session),status=status,
                trial='N2',process_state=process_state,owned_finalization=owned,protection_errors=errors,
                capture_errors=capture_errors,protection_comparisons=comparisons,scientific=scientific,
                geometry=geometry,lifetime=lifetime,causal=causal,scheduler=scheduler,joins=joins,counter=counter,
                reader_sources={str(p):sha(p) for p in reader_paths},
                scientific_completeness='INCONCLUSIVE_REQUIRES_SCOPED_TARGET_CONTROL_REVIEW',plan_sha256=plan['plan_sha256'],
                preflight_sha256=before['receipt_sha256'],authority='NO_RETRY_RELAUNCH_OR_NEXT_TRIAL')

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('action',choices=('preflight','postflight'))
    for name in ('plan','preflight','approval'):
        p.add_argument('--'+name,type=Path,required=name=='plan');p.add_argument('--'+name+'-sha256',required=name=='plan')
    p.add_argument('--session',type=Path);p.add_argument('--out',type=Path,required=True)
    a=p.parse_args();out=a.out.resolve();require(out.is_relative_to(ROOT/'.local-work/d5an'),'Fresh D5AM output required')
    guard();out.mkdir(parents=True,exist_ok=False)
    try:
        plan=original.pinned_json(a.plan,a.plan_sha256);plan['plan_sha256']=a.plan_sha256
        if a.action=='preflight':value=preflight(plan,a.plan_sha256,out)
        else:
            before=original.pinned_json(a.preflight,a.preflight_sha256);before['receipt_sha256']=a.preflight_sha256
            require(before['plan_sha256']==a.plan_sha256,'Preflight plan mismatch')
            value=postflight(plan,before,a.session,original.pinned_json(a.approval,a.approval_sha256),out)
    except BaseException as e:fresh(out/'receipt.json',dict(state='CHECK_ERROR',error=repr(e),authority='NONE'));raise
    fresh(out/'receipt.json',value);print(json.dumps(dict(out=str(out),state=value.get('state',value.get('status')))))

if __name__=='__main__':main()
