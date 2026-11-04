# SPDX-License-Identifier: GPL-3.0-or-later
# D5AN owned derivative of d5am_n1_operations_qualify.py; exact origin pins in operations-lineage.json.
"""Qualify D5AM single N2 control against the owned native host, never retail.

Retail admission/protection discovery and the archive session-namespace
comparator are explicitly replaced by owned fixture validation. Production
ownership/challenge/arm/flush/STOP and neutral content
comparison remain real. Tests alter only new owned files or in-memory plans.
No deployment, protected originals, target memory, game or network operations.
An unsuccessful fixture gets STOP/exit signals and a bounded grace period;
if it remains alive, only this tool's own Popen handle is terminated and the
forced cleanup is recorded as failure. This is never retail owned finalization.
"""
import sys
import os
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):
    raise RuntimeError('Use pinned Python -E -B without PYTHONOPTIMIZE, -O or -OO')
import argparse
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import shutil
import time
import d5an_n2_episode as episode
import d5an_n2_operations as operations
import d5an_n2_stop as trusted
from d5ai_episode import ROOT,require,sha,strict_session_json
from common import fresh,guard,inventory

def fixture_target(c):
    trusted.controller_pins(c.plan)
    require(c.expected['retail'] is False and c.session.is_relative_to(ROOT/'.local-work/d5an'),'Owned fixture only')
    require(Path(c.plan['process_image']).name=='sor-d5x-fixture.exe' and
            sha(c.plan['process_image'])==c.expected['host_sha256']==c.plan['fixture_host_sha256'],'Owned host mismatch')
    require(sha(c.plan['dll'])==c.expected['dll_sha256']==c.plan['dll_sha256'],'Owned DLL mismatch')
    trusted.distinct(c.expected,c.plan,c.identity_hash)

class Owned(episode.N2Controller):
    def validate_target(self,admission,approval):operations.source_pins(self.plan);fixture_target(self)
    def validate_phase(self,admission):operations.source_pins(self.plan);guard()

class Fallback(trusted.TrustedController):
    def validate_target(self,admission,approval):fixture_target(self)

def protection_controls(out,plan,check,refuses):
    """Production lightweight/content methods with declared owned discovery."""
    folder=out/'owned-protected';folder.mkdir();live=folder/'Saves';live.mkdir()
    for path,data in [(live/'Save52.sfs',b'owned primary'),(folder/'backup.sfs',b'owned primary'),
                      (folder/'profile.ini',b'owned config'),(folder/'definitions.ba2',b'owned defs'),
                      (folder/'sfse.dll',b'owned sfse'),(folder/'archive.zip',b'owned index')]:path.write_bytes(data)
    restore=folder/'restore-copy.sfs';shutil.copyfile(folder/'backup.sfs',restore)
    deployed=folder/'SorConstructionWinner.dll';shutil.copyfile(plan['dll'],deployed)
    def metadata(path):return dict(bytes=path.stat().st_size,mtime_ns=path.stat().st_mtime_ns)
    def full(destination):
        require(sha(live/'Save52.sfs')==sha(folder/'backup.sfs')==sha(restore),'Owned protected copy/backup readiness')
        configs={str(folder/'profile.ini'):sha(folder/'profile.ini')};defs={str(folder/'definitions.ba2'):sha(folder/'definitions.ba2')}
        return dict(save_policy_sha256='owned-policy',live_path=str(live),protected_live={'Save52.sfs':dict(bytes=(live/'Save52.sfs').stat().st_size,sha256=sha(live/'Save52.sfs'))},
                    backups={'Save52.sfs':[dict(path=str(folder/'backup.sfs'),kind='LOOSE_BACKUP',sha256=sha(folder/'backup.sfs'),metadata=metadata(folder/'backup.sfs'))]},
                    config=configs,definitions=defs,file_guards={p:metadata(Path(p)) for p in configs|defs},
                    installed={str(folder/'sfse.dll'):dict(**metadata(folder/'sfse.dll'),sha256=sha(folder/'sfse.dll'))},
                    archive_guard={str(folder/'archive.zip'):metadata(folder/'archive.zip')},
                    archive_content_sha256={str(folder/'archive.zip'):sha(folder/'archive.zip')},restore_rehearsal_sha256=sha(restore))
    before=full(out)
    class Policy:
        def load_policy(self):return {}
        def policy_hash(self,p):return 'owned-policy'
        def sizes(self,path,p):return {x.name:dict(bytes=x.stat().st_size) for x in Path(path).iterdir() if x.is_file()}
        def partition(self,rows,p):return dict(protected={n:r for n,r in rows.items() if n=='Save52.sfs'},unclassified=[n for n in rows if n!='Save52.sfs'],transient=[])
    module=operations.legacy();module.policy_module=lambda:Policy();module.full=full;module.remote_sizes=lambda value:{}
    previous_legacy=operations.legacy;operations.legacy=lambda:module
    fixture=copy.deepcopy(plan);fixture.update(sfse_path=str(folder/'sfse.dll'),sfse_sha256=sha(folder/'sfse.dll'),deployed_dll=str(deployed))
    admission=dict(protection=before,remote_protected_sizes={})
    try:
        operations.lightweight(fixture,admission);check('owned-production-content-first-lightweight',True)
        for path in (folder/'profile.ini',folder/'definitions.ba2',folder/'sfse.dll'):
            st=path.stat();os.utime(path,ns=(st.st_atime_ns,st.st_mtime_ns+2_000_000_000))
        value=operations.lightweight(fixture,admission);check('owned-timestamp-only-content-equal',len(value['timestamp_changes'])==3)
        for name in ('profile.ini','definitions.ba2','sfse.dll'):
            path=folder/name;data=path.read_bytes();st=path.stat();path.write_bytes(b'X'+data[1:]);os.utime(path,ns=(st.st_atime_ns,st.st_mtime_ns))
            refuses('owned-same-metadata-byte-change-'+name,lambda:operations.lightweight(fixture,admission))
            path.write_bytes(data);os.utime(path,ns=(st.st_atime_ns,st.st_mtime_ns))
        rogue=live/'Unclassified.sfs';rogue.write_bytes(b'owned unclassified')
        refuses('owned-unclassified-save-refused',lambda:operations.lightweight(fixture,admission));rogue.unlink()
        rival=folder/'SorOther.dll';rival.write_bytes(b'owned rival')
        refuses('owned-competing-candidate-refused',lambda:operations.lightweight(fixture,admission));rival.unlink()
        operations.content.compare_protection(before,full(out));check('owned-full-protection-content-equal',True)
        archive=folder/'archive.zip';data=archive.read_bytes();st=archive.stat();archive.write_bytes(b'X'+data[1:]);os.utime(archive,ns=(st.st_atime_ns,st.st_mtime_ns))
        refuses('owned-full-archive-byte-change-refused',lambda:operations.content.compare_protection(before,full(out)))
        archive.write_bytes(data);os.utime(archive,ns=(st.st_atime_ns,st.st_mtime_ns))
    finally:operations.legacy=previous_legacy
    return module,before,fixture

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for name in ('build','plan','out'):p.add_argument('--'+name,type=Path,required=True)
    a=p.parse_args();build,planpath,out=(getattr(a,n).resolve() for n in ('build','plan','out'))
    require(out.is_relative_to(ROOT/'.local-work/d5an'),'Fresh D5AM output required');guard();out.mkdir(parents=True,exist_ok=False)
    plan=json.loads(planpath.read_bytes());operations.verify_plan(plan);plan['plan_sha256']=sha(planpath)
    image=build/'sor-d5x-fixture.exe';dll=build/'SorConstructionWinner.dll'
    require(sha(dll)==plan['dll_sha256'],'Qualified DLL required')
    plan.update(process_image=str(image),dll=str(dll),fixture_host_sha256=sha(image))
    checks=[];states=[];c=None;session=out/'session';result=dict(schema='sor-d5an-n2-operations-qualification/1',status='FAIL',
        dll_sha256=plan['dll_sha256'],method_sha256=sha(__file__),source_lock_sha256=plan['d5an_n2_source_lock_sha256'],
        scope='Actual owned host; explicit fixture-only admission/protection discovery seams')
    def check(name,value):checks.append(dict(name=name,passed=bool(value)));require(value,name)
    def refuses(name,fn):
        try:fn()
        except (ValueError,KeyError,AssertionError,OSError):check(name,True)
        else:check(name,False)
    for name in ('d5an_n2_stop.py','d5an_n2_episode.py','d5an_n2_content.py','d5an_n2_operations.py','d5an_readiness.py','d5an_n2_operations_qualify.py','d5an_n2_archive.py'):
        script=Path(__file__).with_name(name)
        for flag in ('-O','-OO','ENV'):
            env=dict(os.environ);command=[sys.executable,'-E','-B']
            if flag=='ENV':env['PYTHONOPTIMIZE']='1'
            else:command.append(flag)
            command.extend([str(script),'--help'])
            completed=subprocess.run(command,capture_output=True,env=env)
            check('optimization-refusal-'+name+'-'+flag,completed.returncode!=0 and any(marker in completed.stderr.lower() for marker in (b'pythonoptimize',b'optimization')))
    # Pure authority controls use an explicitly synthetic reviewed-freeze token,
    # never written into the actual draft plan or presented as maintainer GO.
    adm=dict(state='PASS_OFFLINE_PREFLIGHT',plan_sha256=sha(planpath),receipt_sha256='1'*64)
    approved=dict(authority='D5AM_N2_EXPLICIT_MAINTAINER_GO',trial='N2',scope=trusted.SCOPE,
                  plan_sha256=sha(planpath),preflight_sha256='1'*64,session=str(session),identity_sha256='2'*64,
                  run_card_sha256=plan['run_card_sha256'],save52_sha256=plan['save52_sha256'],
                  prediction_sha256=plan['prediction_sha256'],review_receipt_sha256='3'*64,
                  profile='Starfield - SFSE',steam_cloud='DISABLED')
    refuses('actual-draft-refuses-live-authority',lambda:trusted.authority(plan,adm,approved,session,'2'*64))
    reviewed=copy.deepcopy(plan);reviewed['review']=dict(state='INDEPENDENTLY_REVIEWED_N2_TECHNICAL_ACCEPT',
             scope='D5AM_N2_0.9.2_READINESS',
             prediction_sha256=plan['prediction_sha256'],run_card_sha256=plan['run_card_sha256'],receipt_sha256='3'*64)
    refuses('pending-prospective-N2-decision-refused',lambda:trusted.authority(reviewed,adm,approved,session,'2'*64))
    reviewed['prospective_trial_decision']=dict(state='RECORDED_PROSPECTIVE_MAINTAINER_DECISION',trial='N2',prediction_mode='NEW_PROSPECTIVE_FORECAST',sha256='4'*64,prediction_sha256='5'*64)
    reviewed['prediction_sha256']=reviewed['review']['prediction_sha256']=approved['prediction_sha256']='5'*64
    reviewed['review']['prospective_trial_decision_sha256']='4'*64
    approved['prospective_trial_decision_sha256']='4'*64
    refuses('technical-review-does-not-waive-known-cap-deviation',lambda:trusted.authority(reviewed,adm,approved,session,'2'*64))
    approved['maintainer_disposition']=dict(deviation='D5AM-AC01-subagent-cap',decision='ACCEPTED_HISTORICAL_EXCEPTION',disposition_sha256=plan['accepted_disposition_sha256'])
    trusted.authority(reviewed,adm,approved,session,'2'*64);check('synthetic-authority-predicate-positive-only',True)
    for key,value in [('deviation','other'),('decision','AI_ACCEPT'),('disposition_sha256','0'*64)]:
        bad=copy.deepcopy(approved);bad['maintainer_disposition'][key]=value
        refuses('known-deviation-disposition-refuse-'+key,lambda bad=bad:trusted.authority(reviewed,adm,bad,session,'2'*64))
    missing=copy.deepcopy(reviewed);missing['review']={}
    refuses('missing-independent-review-refused',lambda:trusted.authority(missing,adm,approved,session,'2'*64))
    for key,value in [('authority','D5AM_N0_EXPLICIT_MAINTAINER_GO'),('trial','B0'),('profile','wrong'),('steam_cloud','UNKNOWN')]+[(k,'0'*64) for k in ('plan_sha256','preflight_sha256','identity_sha256','run_card_sha256','prediction_sha256','review_receipt_sha256','save52_sha256')]:
        bad=dict(approved);bad[key]=value
        refuses('authority-refuse-'+key,lambda bad=bad:trusted.authority(reviewed,adm,bad,session,'2'*64))
    for key,value in [('authority','D5AM_N1_EXPLICIT_MAINTAINER_GO'),('trial','N1')]:
        bad=dict(approved,**{key:value})
        refuses('stale-N1-'+key+'-refused',lambda bad=bad:trusted.authority(reviewed,adm,bad,session,'2'*64))
    stale=copy.deepcopy(reviewed);stale['schema']='sor-d5am-n1-plan/1'
    refuses('stale-N1-plan-schema-refused',lambda:trusted.authority(stale,adm,approved,session,'2'*64))
    for old in plan['prior_processes']:
        reused=dict(pid=old['pid'],creation_filetime=old['creation_filetime'],nonce=old['nonce'])
        refuses('prior-birth-refused-'+str(old['pid']),lambda reused=reused,old=old:trusted.distinct(reused,plan,old['identity_sha256']))
    reused_pid=plan['prior_processes'][-1]
    trusted.distinct(dict(pid=reused_pid['pid'],creation_filetime=reused_pid['creation_filetime']+1,nonce='f'*64),plan,'f'*64)
    check('numeric-pid-reuse-with-new-birth-permitted',True)
    refuses('old-N0-label-refused-before-any-arm',lambda:episode.arm_once(None,'N0'))
    wrong_trial=copy.deepcopy(approved);wrong_trial['trial']='N0'
    refuses('old-N0-trial-refused',lambda:trusted.authority(reviewed,adm,wrong_trial,session,'2'*64))
    # Full producer validation oracle uses synthetic relocated site rows under
    # real source-pinned guards. It is not retail installation evidence.
    synthetic=json.loads((build/'d5ai-normal/identity.json').read_bytes());synthetic.update(retail=True,host_sha256=plan['game_sha256'],sfse_sha256=plan['sfse_sha256'])
    synthetic['scheduler_vtable_guard_basis']='preferred-image-vtable64/1'
    base=0x140000000;synthetic['module_base']=base
    for key in ('sites','geometry_sites','context_sites','lifetime_sites','causal_sites','scheduler_sites','scheduler_vtables','causal_helpers','scheduler_targets'):
        synthetic[key]=[dict(va=base+r['rva'],**r) for r in plan[key]]
    synthetic['scheduler_callback']=dict(va=base+plan['scheduler_callback']['rva'],guard_sha256=plan['scheduler_callback']['guard_sha256'])
    retailplan=copy.deepcopy(plan);retailplan['process_image']='Starfield.exe'
    trusted.producer(synthetic,retailplan);check('synthetic-full-producer-predicate-positive-only',True)
    for key,value in [('counter_helper_rva',synthetic['counter_helper_rva']+1),('counter_leave_rva',synthetic['counter_leave_rva']+1),('counter_dll_base',True)]:
        bad=dict(synthetic,**{key:value})
        refuses('counter-producer-binding-refuse-'+key,lambda bad=bad:trusted.producer(bad,retailplan))
    for key in ('sites','geometry_sites','context_sites','lifetime_sites','causal_sites','scheduler_sites','scheduler_vtables','causal_helpers','scheduler_targets'):
        bad=copy.deepcopy(synthetic);bad[key]=bad[key][:-1]
        refuses('refuse-omitted-'+key,lambda bad=bad:trusted.producer(bad,retailplan))
    for key in ('causal_sites','scheduler_sites','causal_helpers','scheduler_targets'):
        for index in range(len(synthetic[key])):
            bad=copy.deepcopy(synthetic);bad[key][index]['guard_sha256']='0'*64
            refuses('refuse-'+key+'-guard-'+str(index),lambda bad=bad:trusted.producer(bad,retailplan))
    for feature in ('causal_bridge_admission_schema','scheduler_bridge_admission_schema','scheduler_dispatch_argument_schema','scheduler_ready_serial_schema','geometry_target_guard_basis','counter_schema'):
        bad=copy.deepcopy(synthetic);bad.pop(feature,None)
        refuses('refuse-missing-'+feature,lambda bad=bad:trusted.producer(bad,retailplan))
    wrong_basis=copy.deepcopy(synthetic);wrong_basis['geometry_target_guard_basis']='original32-unmodified/1'
    refuses('refuse-stale-geometry-guard-basis',lambda:trusted.producer(wrong_basis,retailplan))
    import d5an_n2_archive
    archive_session=trusted.LIVE/('session-'+'e'*64)
    archive_post=dict(schema='sor-d5an-n2-postflight/1',trial='N2',plan_sha256=sha(planpath),session=str(archive_session))
    archive_roots=dict(capture=dict(path=str(archive_session),kind='raw-capture'))
    binding=d5an_n2_archive.association(plan,sha(planpath),archive_post,archive_roots)
    check('synthetic-archive-plan-association-positive-only',binding['plan_sha256']==sha(planpath))
    for key,value in [('schema','other'),('trial','B0'),('plan_sha256','0'*64),('session',str(out/'foreign-session'))]:
        bad=dict(archive_post,**{key:value})
        refuses('archive-refuse-postflight-'+key,lambda bad=bad:d5an_n2_archive.association(plan,sha(planpath),bad,archive_roots))
    refuses('archive-refuse-other-raw-root',lambda:d5an_n2_archive.association(plan,sha(planpath),archive_post,
        dict(capture=dict(path=str(out/'foreign-session'),kind='raw-capture'))))
    refuses('archive-refuse-extra-raw-root',lambda:d5an_n2_archive.association(plan,sha(planpath),archive_post,
        dict(archive_roots,extra=dict(path=str(out/'foreign-session'),kind='raw-capture'))))
    bad=dict(archive_post,session=str(trusted.LIVE/'session'))
    refuses('archive-production-refuses-malformed-session-name',lambda:d5an_n2_archive.association(plan,sha(planpath),bad,
        dict(capture=dict(path=bad['session'],kind='raw-capture'))))
    protected_module,protected_before,protected_plan=protection_controls(out,plan,check,refuses)
    logs=[(out/name).open('xb') for name in ('host.stdout','host.stderr')]
    child=subprocess.Popen([str(image),str(dll),str(session),'d5ai-controller-host'],stdout=logs[0],stderr=logs[1],creationflags=subprocess.CREATE_NO_WINDOW)
    def until(fn,label):
        # The existing native bootstrap can wait for transient crypto threads
        # to retire before installing private patches. This is a fixture bound,
        # not a retail timer, scientific quota or forced gameplay cutoff.
        end=time.monotonic()+180
        while True:
            value=fn()
            if value:return value
            require(child.poll() is None and time.monotonic()<end,'Finite fixture wait failed: '+label);time.sleep(.01)
    try:
        until(lambda:(session/'ready.json').exists() and (session/'fixture-controller-ready.json').exists(),'ready')
        identity=strict_session_json(session/'identity.json');c=Owned(session,identity,plan,{},{},'start')
        for label in ('A0','A1','B0','N0','N1',''):
            refuses('refuse-label-'+label,lambda label=label:episode.arm_once(c,label))
        def armed():
            value=episode.arm_once(c,'N2');states.append(value['state'])
            return value if value['state']=='GEOMETRY_ARMED' else None
        value=until(armed,'arm');check('actual-one-native-request',value['geometry_request']['arm_ack']['geometry_armed']==1)
        ack=value['geometry_request']['arm_ack']
        for key,value in [('counter_fault_schema','old'),('counter_fault_publication',1),('counter_fault_ids',2),('counter_fault_thread',1)]:
            bad=dict(ack,**{key:value})
            refuses('counter-provenance-health-refusal-'+key,lambda bad=bad:episode.recorder_health(bad))
        for fault in (1,2,3):
            bad=dict(ack,causal_native_counter_faults=fault,causal_failed=True)
            refuses('native-bridge-counter-fault-refused-'+str(fault),lambda bad=bad:episode.recorder_health(bad))
        bad=dict(ack);bad.pop('causal_bridge_active')
        refuses('missing-native-bridge-active-refused',lambda:episode.recorder_health(bad))
        pending=dict(ack,causal_bridge_active=1,scheduler_active=1,scheduler_registry_faults=2,scheduler_identity_faults=3)
        episode.recorder_health(pending);check('healthy-active-and-science-uncertainty-no-automatic-STOP',True)
        (session/'fixture-query-1').write_bytes(b'one explicitly owned synthetic query\n')
        until(lambda:(session/'geometry-request-1.json').exists(),'capture')
        value=episode.arm_once(c,'N2');check('natural-early-capture-inspected-no-rearm',value['state']=='GEOMETRY_ALREADY_CONSUMED' and value['natural_early_capture_inspected'])
        check('no-second-query-or-request',c.state['geometry_last_request']==1 and c.state['d5an_n2_arms']=={'N2':1})
        owner=c.state['owner'];c.close();c=Owned(session,identity,plan,{},{},'request')
        check('reconnect-preserves-exclusive-owner-and-single-arm',c.state['owner']==owner and c.state['d5an_n2_arms']=={'N2':1})
        for item in plan['prior_processes']:
            reused=copy.deepcopy(identity);reused['pid']=item['pid']
            trusted.distinct(reused,plan,sha(session/'identity.json'))
            check('synthetic-numeric-pid-reuse-with-new-birth-allowed-'+str(item['pid']),True)
            wrong=dict(reused,creation_filetime=item['creation_filetime'])
            refuses('prior-process-birth-refused-'+str(item['pid']),lambda wrong=wrong:trusted.distinct(wrong,plan,sha(session/'identity.json')))
        broken=copy.deepcopy(plan);broken['d5an_n2_source_lock_sha256']='0'*64
        refuses('broad-science-lock-failure',lambda:operations.source_pins(broken))
        altered_lock=json.loads(Path(plan['d5an_n2_source_lock']).read_bytes())
        altered_lock['sources'][str(Path(episode.__file__).resolve())]='0'*64
        fresh(out/'changed-source-lock.json',altered_lock)
        altered_plan=copy.deepcopy(plan);altered_plan.update(d5an_n2_source_lock=str(out/'changed-source-lock.json'),
                                                          d5an_n2_source_lock_sha256=sha(out/'changed-source-lock.json'))
        refuses('authentic-lock-with-changed-source-digest-refused',lambda:operations.source_pins(altered_plan))
        trusted.controller_pins(broken);check('minimal-stop-closure-independent-of-broad-failure',True)
        bad=copy.deepcopy(broken);bad['d5an_n2_controller_pins'][next(iter(bad['d5an_n2_controller_pins']))]='0'*64
        refuses('controller-integrity-never-waived',lambda:trusted.controller_pins(bad))
        c.close();c=Fallback(session,identity,broken,{},{},'stop')
        value=c.request_stop('finite N2 owned-host qualification; broad science lock failed')
        check('actual-authenticated-fallback-STOP',value['state']=='STOP_REQUESTED');c.close();c=None
        (session/'fixture-controller-done').write_bytes(b'finite completion\n');child.wait(timeout=30)
        check('normal-host-exit',child.returncode==0)
        from d5ai_read_geometry import read_session
        from d5ai_read_lifetime import read_prefix
        from d5am_read_causal import read as causal_read
        from d5am_read_scheduler import read as scheduler_read
        terminal=strict_session_json(session/'terminal.json');geometry=read_session(session)
        check('actual-one-flushed-geometry',not geometry['errors'] and len(geometry['snapshots'])==1 and terminal['geometry_completed']==1)
        check('actual-lifetime-complete',read_prefix(session,terminal)['complete'])
        causal=causal_read(session,plan['dll_sha256']);scheduler=scheduler_read(session,plan['dll_sha256'])
        fresh(out/'causal.json',causal);fresh(out/'scheduler.json',scheduler)
        check('actual-worker-new-sidecar-byte-accounting',causal['sidecar_accounting_complete'] and
              causal.get('native_bridge_accounting_complete') is True and scheduler['byte_accounting_complete'] and
              scheduler.get('native_bridge_accounting_complete') is True)
        check('uninstalled-fixture-sites-not-retail-proof',all(s['va']==0 for s in identity['scheduler_sites']))
        # Execute actual production postflight/readers. Only full-protection
        # discovery and retail authority/target admission are fixture seams.
        old_legacy,old_finalization=operations.legacy,operations.finalization
        operations.legacy=lambda:protected_module
        def fixture_finalization(p,b,s,approval):
            state=strict_session_json(s/'p4-state.json');stop=state['stop']
            require(state['identity_sha256']==sha(s/'identity.json') and stop['identity_sha256']==state['identity_sha256'] and
                    stop['owner']==state['owner'] and (s/'STOP').read_bytes()==(json.dumps(stop,sort_keys=True)+'\n').encode(),'Actual owned STOP mismatch')
            return dict(identity_sha256=state['identity_sha256'],owner=state['owner'],stop_nonce=stop['stop_nonce'],fixture_only=True)
        operations.finalization=fixture_finalization
        protected_plan['deployed_dll']=str(out/'absent-effective-dll')
        before=dict(protection=protected_before,remote_protected_sizes={},existing_sessions=[],receipt_sha256='1'*64)
        try:post=operations.postflight(protected_plan,before,session,{},out)
        finally:operations.legacy,operations.finalization=old_legacy,old_finalization
        fresh(out/'fixture-postflight.json',post)
        check('actual-production-postflight-new-readers-owned-protection',post['status']=='PASS_POSTFLIGHT' and
              post['scientific_completeness'].startswith('INCONCLUSIVE') and post['causal'] and post['scheduler'])
        for filename,mode in [('causal.bin','corrupt'),('scheduler.bin','corrupt'),('events.bin','partial')]:
            copied=out/(mode+'-'+filename.replace('.','-'));shutil.copytree(session,copied)
            file=copied/filename;data=file.read_bytes()
            file.write_bytes(bytes([data[0]^1])+data[1:] if mode=='corrupt' else data[:-1])
            operations.legacy=lambda:protected_module;operations.finalization=fixture_finalization
            try:adverse=operations.postflight(protected_plan,before,copied,{},out)
            finally:operations.legacy,operations.finalization=old_legacy,old_finalization
            fresh(out/(mode+'-'+filename+'.json'),adverse)
            check('actual-copy-'+mode+'-'+filename+'-postflight-partial',adverse['status']=='PARTIAL_POSTFLIGHT' and adverse['capture_errors'])
        companion=out/'companion';companion.mkdir();post['fixture_only']=True
        fresh(companion/'postflight.json',post)
        fresh(companion/'protection-before.json',protected_before)
        path=ROOT/'runtime/session-tools/archive.py';spec=importlib.util.spec_from_file_location('d5am_owned_archive_qualify',path)
        archive=importlib.util.module_from_spec(spec);spec.loader.exec_module(archive)
        roots=dict(capture=dict(path=str(session),kind='raw-capture'),companion=dict(path=str(companion),kind='private-receipt'))
        original_inventory=inventory(session)
        partial=dict(post,status='PARTIAL_POSTFLIGHT');fresh(companion/'partial-postflight.json',partial)
        refuses('partial-archive-requires-explicit-reason',lambda:archive.seal(roots,companion/'partial-postflight.json',sha(companion/'partial-postflight.json')))
        # The owned host is outside LIVE and has its original fixture name.
        # Only the exact namespace comparator is replaced here. All production
        # CLI source/plan/postflight/raw-root/archive logic remains real.
        saved_namespace=d5an_n2_archive._session_namespace;saved_argv=sys.argv
        def owned_namespace(actual,live):
            require(actual==session and live==Path(plan['live_root']).resolve(),
                    'Only the actual owned fixture namespace is substituted')
        d5an_n2_archive._session_namespace=owned_namespace
        fresh(out/'roots.json',roots)
        destination=out/'owned-host-evidence.zip'
        def archive_cli(action,input_path,output_path,extra):
            sys.argv=[str(Path(d5an_n2_archive.__file__)),action,'--plan',str(planpath),'--plan-sha256',sha(planpath),
                      '--input',str(input_path),'--sha256',sha(input_path),'--out',str(output_path),*extra]
            require(d5an_n2_archive.main()==0,'Actual archive CLI failed: '+action)
        try:
            archive_cli('seal',out/'roots.json',out/'seal.json',
                        ['--postflight',str(companion/'postflight.json'),'--postflight-sha256',sha(companion/'postflight.json')])
            seal=json.loads((out/'seal.json').read_bytes());bound=seal['d5am']
            archive_cli('create',out/'seal.json',out/'archive-create.json',['--archive',str(destination)])
            archive_cli('verify',out/'seal.json',out/'archive-verify.json',
                        ['--archive',str(destination),'--archive-sha256',sha(destination)])
        finally:
            d5an_n2_archive._session_namespace=saved_namespace;sys.argv=saved_argv
        check('actual-archive-CLI-seal-create-verify-declared-namespace-seam',bound['session']==str(session))
        check('every-native-channel-and-companion-lossless-archive',inventory(session)==original_inventory and
              archive.collect(roots)==seal['files'] and 'capture/causal.bin' in seal['files'] and 'capture/scheduler.bin' in seal['files'])
        require(sha(planpath)==plan['plan_sha256'],'Original plan changed during qualification')
        operations.verify_plan(json.loads(planpath.read_bytes()))
        check('exact-plan-card-prediction-and-source-inputs-preserved',True)
        result.update(status='PASS',identity_sha256=sha(session/'identity.json'),plan_sha256=sha(planpath),
                      limits='No retail admission or protection-discovery claim. Generic scheduler sites uninstalled in this host; native task adapter positive integration qualified separately. Byte completeness is not task/causal completeness.')
    except BaseException as error:
        result['error']=repr(error)
        raise
    finally:
        cleanup_errors=[]
        if c is not None:
            try:c.request_stop('owned-host failure closeout')
            except Exception as error:cleanup_errors.append('STOP: '+repr(error))
            try:c.close()
            except Exception as error:cleanup_errors.append('Lease close: '+repr(error))
        if child.poll() is None:
            # Disposable fixture emergency signal only, never called owned finalization.
            try:
                if not(session/'STOP').exists():(session/'STOP').write_bytes(b'owned fixture failure STOP\n')
                (session/'fixture-controller-done').touch(exist_ok=True);child.wait(timeout=90)
            except subprocess.TimeoutExpired:
                child.kill();child.wait(timeout=30)
                cleanup_errors.append('Only the spawned owned fixture handle was terminated after failed grace; not owned finalization')
            except Exception as error:cleanup_errors.append('Fixture cleanup: '+repr(error))
        for log in logs:log.close()
        if cleanup_errors:result['status']='FAIL'
        result.update(cleanup_errors=cleanup_errors,owned_fixture_pid=child.pid,owned_fixture_exit=child.poll())
        result.update(checks=checks,states=states,final_free=guard());fresh(out/'qualification.json',result)
    print(json.dumps(dict(status=result['status'],checks=len(checks))))
    require(result['status']=='PASS','Operational qualification failed')

if __name__=='__main__':main()
