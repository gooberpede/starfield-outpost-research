# SPDX-License-Identifier: GPL-3.0-or-later
"""Run one B-shaped capture against the existing owned native fixture host.

Reads source-locked plan and unchanged 0.7.0 DLL/owned host, launches only that
host (never Starfield), writes fresh ignored evidence. Fixture-only admission
replaces retail image/site checks; actual ownership, worker challenge, one-shot
arm, raw transport, source-Grid qualification and authenticated STOP remain real.
Protection full-audit discovery is replaced by independent owned file copies;
content comparison, wrapper routing and archive member verification remain real.
No protected-original writes, deployment, network, dependency or native rebuild.
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
import shutil
import subprocess
import time
from types import SimpleNamespace
import d5al_episode as episode
import d5al_operations as operations
from d5ai_episode import ROOT,require,sha,read_json,poll_geometry
from d5ai_read_lifetime import validate_identity,read_prefix
from d5ai_read_geometry import read_session
from d5ai_operations import worker_json
from worker_health import disk_guard


class OwnedController(episode.EpisodeBController):
    def validate_target(self,admission,approval):
        operations.source_pins(self.plan)
        require(self.expected['retail'] is False and self.session.is_relative_to(ROOT/'.local-work/d5al'),'Owned fixture only')
        require(Path(self.plan['process_image']).name=='sor-d5x-fixture.exe' and sha(self.plan['process_image'])==self.expected['host_sha256'],'Owned host mismatch')
        require(sha(self.plan['dll'])==self.expected['dll_sha256']==self.plan['dll_sha256'],'Fixture DLL mismatch')
        episode.trusted.distinct(self.expected,self.plan,self.identity_hash)
        validate_identity(self.expected)
    def validate_phase(self,admission):
        operations.source_pins(self.plan)
        disk_guard()


class OwnedFallback(episode.trusted.TrustedController):
    def validate_target(self,admission,approval):
        episode.original.verify_controller_pins(self.plan)
        require(sha(episode.trusted.__file__)==self.plan['trusted_stop_sha256'],'Trusted STOP mismatch')
        require(self.expected['retail'] is False and self.session.is_relative_to(ROOT/'.local-work/d5al'),'Owned fallback fixture only')
        require(Path(self.plan['process_image']).name=='sor-d5x-fixture.exe' and sha(self.plan['process_image'])==self.expected['host_sha256'],'Owned fallback identity mismatch')
        episode.trusted.distinct(self.expected,self.plan,self.identity_hash)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('build',type=Path);p.add_argument('plan',type=Path);p.add_argument('out',type=Path)
    a=p.parse_args();build,plan_path,out=(v.resolve() for v in (a.build,a.plan,a.out))
    require(out.is_relative_to(ROOT/'.local-work/d5al'),'New task-local output required')
    disk_guard();out.mkdir(parents=True,exist_ok=False)
    plan=read_json(plan_path);operations.source_pins(plan);plan_hash=sha(plan_path)
    image=build/'package-runtime/sor-d5x-fixture.exe';dll=build/'package-runtime/SorConstructionWinner.dll'
    require(sha(image)=='3f39eafc7a1ed4c5d76df7368b55a8053846f5f125f36fc00c980e4e2696e34a' and sha(dll)==plan['dll_sha256'],'Frozen owned fixture input mismatch')
    plan.update(process_image=str(image),dll=str(dll),plan_sha256=plan_hash)
    session=out/'session';checks=[];states=[]
    def check(name,value):
        checks.append(dict(name=name,passed=bool(value)));require(value,name)
    def refuses(name,fn):
        try:fn()
        except (ValueError,KeyError,AssertionError,OSError):check(name,True)
        else:check(name,False)
    logs=[(out/name).open('xb') for name in ('host.stdout','host.stderr')]
    child=subprocess.Popen([str(image),str(dll),str(session),'d5ai-controller-host'],stdout=logs[0],stderr=logs[1],creationflags=subprocess.CREATE_NO_WINDOW)
    controller=None;result=dict(status='FAIL',scope='Actual native B-shaped one-shot; fixture-only retail admission and owned-copy preservation discovery')
    def wait_file(name):
        while not (session/name).exists():
            require(child.poll() is None,'Owned host exited before '+name);time.sleep(.01)
    def health():
        controller.request()
        while True:
            value=controller.poll()
            if value['state']=='HEALTHY_ACK':return value
            require(value['state']=='ALIVE_ACK_PENDING','Unexpected worker health '+value['state']);time.sleep(.01)
    try:
        wait_file('ready.json');wait_file('fixture-controller-ready.json')
        identity=read_json(session/'identity.json')
        controller=OwnedController(session,identity,plan,{},{},'start')
        for label in ('A0','A1','B1',''):
            refuses('refuse-label-'+label,lambda label=label:episode.arm_once(controller,label))
        while True:
            value=episode.arm_once(controller,'B0');states.append(value['state'])
            if value['state']=='GEOMETRY_ARMED':break
            require(child.poll() is None,'Owned host ended during arm');time.sleep(.02)
        check('exact-native-arm-1',value['geometry_request']['arm_ack']['geometry_armed']==1)
        (session/'fixture-query-1').write_bytes(b'one permitted owned query\n')
        wait_file('geometry-request-1.json')
        early=episode.arm_once(controller,'B0')
        check('completed-natural-capture-inspected-before-any-new-arm-or-query',early['state']=='GEOMETRY_ALREADY_CONSUMED' and early['natural_early_capture_inspected'] and controller.state['geometry_last_request']==1)
        check('capture-receipt',poll_geometry(controller)['state']=='GEOMETRY_CAPTURE_RECEIPT')
        check('no-second-query',episode.arm_once(controller,'B0')['state']=='GEOMETRY_ALREADY_CONSUMED' and controller.state['geometry_last_request']==1)
        nonce=health()['ack']['request_nonce']
        args=SimpleNamespace(session=session,snapshot=1,nonce=nonce,target=episode.TARGET,owner_formid=episode.OWNER_FORMID,plan_sha256=plan_hash)
        cert=episode.qualify(args,plan);check('actual-preterminal-source-grid-B0',cert['state']=='BASELINE_PREFIX_QUALIFIED' and not(session/'terminal.json').exists())
        operations.fresh(out/'B0-certificate.json',cert)
        check('repeat-read-only-same-capture',episode.qualify(args,plan)==cert)
        for field,wrong in (('snapshot',2),('target','foreign'),('owner_formid','00000001')):
            bad=copy.copy(args);setattr(bad,field,wrong)
            refuses('checkpoint-reject-'+field,lambda bad=bad:episode.qualify(bad,plan))
        owner=controller.state['owner'];controller.close()
        controller=OwnedController(session,identity,plan,{},{},'request')
        check('reconnect-preserves-owner-and-single-arm',controller.state['owner']==owner and controller.state['d5al_arms']=={'B0':1})
        admission=dict(state='PASS_OFFLINE_PREFLIGHT',plan_sha256=plan_hash,receipt_sha256='1'*64)
        approval=dict(authority='D5AL_EPISODE_B_EXPLICIT_MAINTAINER_GO',episode='B',scope=plan['scope'],plan_sha256=plan_hash,preflight_sha256='1'*64,session=str(session),identity_sha256=sha(session/'identity.json'),run_card_sha256=plan['run_card_sha256'],save52_sha256=plan['save52_sha256'], profile='Starfield - SFSE', steam_cloud='DISABLED')
        episode.trusted.authority(plan,admission,approval,session,sha(session/'identity.json'))
        check('new-B-authority-exact-binding',True)
        for field,wrong in (('authority','D5AI_EPISODE_B_EXPLICIT_MAINTAINER_GO'),('authority','D5AI_EPISODE_A_EXPLICIT_MAINTAINER_GO'),('identity_sha256','0'*64),('plan_sha256','0'*64),('run_card_sha256','0'*64),('preflight_sha256','0'*64),('save52_sha256','0'*64),('profile','wrong profile'),('steam_cloud','UNKNOWN')):
            bad=dict(approval);bad[field]=wrong
            refuses('refuse-stale-authority-'+field+'-'+wrong[:8],lambda bad=bad:episode.trusted.authority(plan,admission,bad,session,sha(session/'identity.json')))
        bad=copy.deepcopy(plan);bad['d5ak_a_process']={'creation_filetime':identity['creation_filetime'],'nonce':identity['nonce'],'identity_sha256':sha(session/'identity.json')}
        refuses('same-process-session-refused',lambda:episode.trusted.distinct(identity,bad,sha(session/'identity.json')))
        broken=copy.deepcopy(plan);broken['d5aj_source_lock_sha256']='0'*64
        refuses('broad-source-lock-refuses',lambda:operations.source_pins(broken))
        episode.original.verify_controller_pins(broken)
        altered=copy.deepcopy(broken);altered['controller_pins'][next(iter(altered['controller_pins']))]='0'*64
        refuses('fallback-controller-integrity-not-waived',lambda:episode.original.verify_controller_pins(altered))
        controller.close();controller=OwnedFallback(session,identity,broken,{},{},'stop')
        result['stop']=controller.request_stop('finite owned B0 qualification complete; trusted fallback after scientific lock refusal')
        check('authenticated-fallback-STOP',result['stop']['state']=='STOP_REQUESTED')
        controller.close();controller=None
        (session/'fixture-controller-done').write_bytes(b'finite owned one-query done\n');child.wait()
        check('normal-host-exit',child.returncode==0)
        terminal=worker_json(session/'terminal.json');raw=read_session(session);life=read_prefix(session,terminal)
        check('one-complete-native-snapshot',not raw['errors'] and len(raw['snapshots'])==1 and terminal['geometry_completed']==1 and life['complete'] and terminal['lifetime_drops']==0)
        stopped=episode.checkpoint.reducer.inspect(session,plan['dll_sha256'],episode.TARGET,int(episode.OWNER_FORMID,16))
        check('stopped-source-grid-qualified',len(stopped['observations'])==1 and not stopped['refused'])
        operations.fresh(out/'stopped.json',stopped)
        # Mutations affect only disposable copies of actual new fixture bytes.
        def tamper(path):
            data=bytearray(path.read_bytes());data[0]^=1;path.write_bytes(data)
        def edit(folder,name,key,value):
            path=folder/name;row=episode.original.strict_session_json(path);row[key]=value;path.write_text(json.dumps(row)+'\n',encoding='utf8',newline='\n')
        cases=(('missing-geometry',lambda f:(f/'geometry-1.bin').unlink()),('partial-geometry',lambda f:edit(f,'geometry-1.json','flushed',False)),('bad-core',lambda f:tamper(f/'events.bin')),('bad-lifetime',lambda f:tamper(f/'lifetimes.bin')),('bad-geometry',lambda f:tamper(f/'geometry-1.bin')),('lifetime-loss',lambda f:edit(f,'ack-'+nonce+'.json','lifetime_drops',1)),('core-loss',lambda f:edit(f,'ack-'+nonce+'.json','drops',1)))
        for name,mutation in cases:
            folder=out/name;shutil.copytree(session,folder);mutation(folder);bad=copy.copy(args);bad.session=folder
            refuses('actual-native-copied-'+name,lambda bad=bad:episode.qualify(bad,plan))
        result.update(status='PASS',snapshots=1,plan_sha256=plan_hash,identity_sha256=sha(session/'identity.json'),limits='Retail process/site admission replaced by owned host checks; source-Grid data actual native fixture. Future retail prediction NOT TESTED. Full preservation and archive qualified separately.')
    except BaseException as error:
        result['error']=repr(error);raise
    finally:
        if controller is not None:
            try:controller.request_stop('owned fixture failure closeout')
            finally:controller.close()
        if session.exists() and child.poll() is None:
            if not(session/'STOP').exists():(session/'STOP').write_bytes(b'owned failed fixture STOP\n')
            (session/'fixture-controller-done').touch(exist_ok=True);child.wait()
        for log in logs:log.close()
        result.update(checks=checks,states=states,final_free=disk_guard())
        operations.fresh(out/'qualification.json',result)
    print(json.dumps(dict(status=result['status'],checks=len(checks),snapshots=result['snapshots'])))

if __name__=='__main__':main()
