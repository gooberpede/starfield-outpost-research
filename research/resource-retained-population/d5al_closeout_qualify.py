# SPDX-License-Identifier: GPL-3.0-or-later
"""D5AL fixture closeout, owned-copy protection and lossless archive controls.

Reads a stopped native B fixture and final plan; creates fresh task-local copies,
full-file hashes, restoration-copy rehearsal and archive. The platform-specific
retail inventory discovery/finalization admission is explicitly substituted by
owned-copy discovery/native fixture ownership; production postflight, protection
comparison, process-exit query, core/geometry/lifetime and archive code execute.
No retail process, protected-original write, deployment, restore or network.
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
import d5al_operations as operations
import d5al_episode as episode
from d5ai_episode import ROOT,require,sha,read_json
from common import fresh,inventory


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('build',type=Path);p.add_argument('plan',type=Path);p.add_argument('session',type=Path);p.add_argument('out',type=Path)
    a=p.parse_args();build,planpath,source,out=(x.resolve() for x in (a.build,a.plan,a.session,a.out))
    require(out.is_relative_to(ROOT/'.local-work/d5al') and not out.is_relative_to(source),'New nonnested local fixture output required')
    operations.guard();out.mkdir(parents=True,exist_ok=False)
    plan=read_json(planpath);operations.source_pins(plan);plan['plan_sha256']=sha(planpath)
    checks=[]
    def check(name,condition):checks.append(dict(name=name,passed=bool(condition)));require(condition,name)
    def refuses(name,fn):
        try:fn()
        except (ValueError,AssertionError,OSError):check(name,True)
        else:check(name,False)
    files=out/'owned-protected';files.mkdir()
    for name,data in (('Save52.sfs',b'owned protected primary input'),('Save52.backup',b'owned protected primary input'),('game.exe',b'owned image'),('profile.ini',b'owned configuration'),('definitions.ba2',b'owned definition'),('archive.zip',b'owned archive/index')):
        (files/name).write_bytes(data)
    restore=out/'restoration-copy.sfs';shutil.copyfile(files/'Save52.backup',restore)
    pin={str(p):sha(p) for p in files.iterdir()}
    def full(destination):
        # Full content hash audit of every independent fixture input/copy.
        require(sha(files/'Save52.sfs')==sha(files/'Save52.backup')==sha(restore),'Independent fixture backup/restoration readiness failed')
        def metadata(path):return dict(bytes=path.stat().st_size,mtime_ns=path.stat().st_mtime_ns)
        return dict(save_policy_sha256='owned-fixture-policy',protected_live={'Save52.sfs':dict(bytes=(files/'Save52.sfs').stat().st_size,sha256=sha(files/'Save52.sfs'))},backups={'Save52.sfs':[dict(path=str(files/'Save52.backup'),kind='LOOSE_BACKUP',sha256=sha(files/'Save52.backup'),metadata=metadata(files/'Save52.backup'))]},definitions={str(files/'definitions.ba2'):sha(files/'definitions.ba2')},config={str(files/'profile.ini'):sha(files/'profile.ini')},file_guards={str(files/name):metadata(files/name) for name in ('profile.ini','definitions.ba2')},installed={str(files/'game.exe'):dict(**metadata(files/'game.exe'),sha256=sha(files/'game.exe'))},archive_guard={str(files/'archive.zip'):metadata(files/'archive.zip')},archive_content_sha256={str(files/'archive.zip'):sha(files/'archive.zip')},restore_rehearsal_sha256=sha(restore))
    before=full(out)
    check('actual-owned-save-backup-independent-restore-bytes',sha(files/'Save52.sfs')==sha(files/'Save52.backup')==sha(restore))
    operations.content.compare_protection(before,full(out));check('full-owned-content-audits-equal',True)
    for path in files.iterdir():
        st=path.stat();os.utime(path,ns=(st.st_atime_ns,st.st_mtime_ns+2_000_000_000))
    diagnostics=operations.content.compare_protection(before,full(out))
    check('all-owned-timestamp-only-positive-content-acceptance',len(diagnostics['timestamp_changes'])>=5)
    for name in ('profile.ini','definitions.ba2','game.exe','archive.zip'):
        path=files/name;data=path.read_bytes();st=path.stat();path.write_bytes(b'X'+data[1:]);os.utime(path,ns=(st.st_atime_ns,st.st_mtime_ns))
        refuses('full-owned-same-metadata-byte-change-'+name,lambda:operations.content.compare_protection(before,full(out)))
        path.write_bytes(data);os.utime(path,ns=(st.st_atime_ns,st.st_mtime_ns))
    identity=read_json(source/'identity.json');check('native-fixture-only',identity['retail'] is False)
    native_state=read_json(source/'p4-state.json');stop=native_state['stop']
    check('actual-native-owned-stop',native_state['identity_sha256']==sha(source/'identity.json') and stop['identity_sha256']==native_state['identity_sha256'] and stop['owner']==native_state['owner'] and (source/'STOP').read_bytes()==(json.dumps(stop,sort_keys=True)+'\n').encode())
    original=operations.original
    legacy=original.legacy()
    check('actual-native-original-process-exited',legacy.original_process_gone(identity) in ('GONE','EXITED','ORIGINAL_GONE_PID_REUSED'))
    fixture_plan=copy.deepcopy(plan);fixture_plan['deployed_dll']=str(out/'absent-effective-dll')
    fixture_before=dict(protection=before,remote_protected_sizes={},receipt_sha256='1'*64,existing_sessions=[],plan_sha256=sha(planpath))
    # Isolated imported module preserves production globals; only retail-specific
    # discovery and retail authority admission are substituted for this fixture.
    spec=importlib.util.spec_from_file_location('d5al_fixture_postflight',Path(original.__file__))
    private=importlib.util.module_from_spec(spec);spec.loader.exec_module(private)
    saved_compare=legacy.compare_protection
    legacy.full=full;legacy.remote_sizes=lambda value:{};legacy.compare_protection=operations.content.compare_protection
    private.legacy=lambda:legacy
    private.verify_plan=lambda value:operations.source_pins(plan)
    private.finalization=lambda value,initial,session,approval:dict(episode='B',identity_sha256=sha(source/'identity.json'),owner=native_state['owner'],stop_nonce=stop['stop_nonce'],fixture_only=True)
    post=private.postflight(fixture_plan,fixture_before,source,{},out)
    check('actual-native-production-postflight-owned-copy-protection',post['status']=='PASS_POSTFLIGHT' and not post['protection_errors'] and not post['capture_errors'])
    post.update(status='PARTIAL_POSTFLIGHT',fixture_only=True,no_full_retail_protection_audit=True,scope='Actual production postflight engine with owned-copy discovery and fixture-only authority admission; not a retail preflight or postflight')
    companion=out/'companion';companion.mkdir()
    fresh(companion/'fixture-postflight.json',post)
    fresh(companion/'protection-before.json',before);fresh(companion/'protection-after.json',full(out))
    raw_before=inventory(source)
    arcpath=ROOT/'runtime/session-tools/archive.py';spec=importlib.util.spec_from_file_location('d5al_fixture_archive',arcpath);archive=importlib.util.module_from_spec(spec);spec.loader.exec_module(archive)
    roots=dict(capture=dict(path=str(source),kind='raw-capture'),companion=dict(path=str(companion),kind='private-receipt'))
    fresh(out/'roots.json',roots)
    refuses('partial-postflight-no-successful-terminal',lambda:archive.seal(roots,companion/'fixture-postflight.json',sha(companion/'fixture-postflight.json'),None))
    seal=archive.seal(roots,companion/'fixture-postflight.json',sha(companion/'fixture-postflight.json'),'owned fixture only; no retail preservation admission')
    fresh(out/'seal.json',seal);zip_path=out/'b-native-fixture.zip'
    fresh(out/'create.json',archive.create(out/'seal.json',sha(out/'seal.json'),zip_path));verified=archive.verify(zip_path,seal,sha(zip_path));fresh(out/'verify.json',verified)
    check('actual-every-member-lossless-archive',inventory(source)==raw_before and archive.collect(roots)==seal['files'])
    # Existing host's own finite worker-exit scenario, no process termination.
    failed=out/'unexpected-worker-exit'
    with(out/'unexpected-worker.log').open('xb') as log:
        child=subprocess.Popen([str(build/'package-runtime/sor-d5x-fixture.exe'),str(build/'package-runtime/SorConstructionWinner.dll'),str(failed),'d5ai-worker-exit'],stdout=log,stderr=subprocess.STDOUT,creationflags=subprocess.CREATE_NO_WINDOW);child.wait()
    check('unexpected-native-exit-no-invented-terminal',child.returncode==0 and not(failed/'terminal.json').exists())
    exited=episode.EpisodeBController.__new__(episode.EpisodeBController);exited.session=failed;exited.expected=read_json(failed/'identity.json');exited.lease=None
    check('unexpected-exit-incomplete',exited.poll()['state']=='EXIT_INCOMPLETE')
    fresh(out/'qualification.json',dict(status='PASS',checks=checks,source_session=str(source),archive_sha256=sha(zip_path),archive_members=len(seal['files']),raw_originals='PRESERVED',plan_sha256=sha(planpath),limits='Native worker and evidence real owned fixture. Full protected-file audit exercised on owned copies; production platform inventory and retail authority admission are explicitly substituted. No retail observation or original protected write.',free=operations.guard()))
    print(json.dumps(dict(status='PASS',checks=len(checks),members=len(seal['files']))))

if __name__=='__main__':main()
