# SPDX-License-Identifier: GPL-3.0-or-later
"""Offline/read-only audits, future approved session ACK/STOP and postflight seal.
Never launches/attaches, deploys, edits saves/configuration or modifies Git. Only
request/STOP/new audit/seal files are written. CPython standard library only.
Live control is restricted to this observer's own local session root.
"""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import uuid
import ctypes
from build import ROOT,sha,guard
from inspect_resources import inspect

LIVE=ROOT/'.local-work/local-readiness/live'
GAME=Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield')
def process_state(pid,creation):
    """QUERY_LIMITED_INFORMATION/SYNCHRONIZE metadata only; no debugger/memory."""
    from ctypes import wintypes as w
    k=ctypes.WinDLL('kernel32',use_last_error=True)
    k.OpenProcess.argtypes=[w.DWORD,w.BOOL,w.DWORD];k.OpenProcess.restype=w.HANDLE
    k.GetProcessTimes.argtypes=[w.HANDLE,*([ctypes.POINTER(w.FILETIME)]*4)];k.GetProcessTimes.restype=w.BOOL
    k.WaitForSingleObject.argtypes=[w.HANDLE,w.DWORD];k.WaitForSingleObject.restype=w.DWORD
    k.CloseHandle.argtypes=[w.HANDLE];k.CloseHandle.restype=w.BOOL
    handle=k.OpenProcess(0x101000,False,pid)
    if not handle:return 'GONE' if ctypes.get_last_error()==87 else 'UNKNOWN_ACCESS_ERROR'
    try:
        times=[w.FILETIME() for _ in range(4)]
        if not k.GetProcessTimes(handle,*[ctypes.byref(t) for t in times]):return 'UNKNOWN_TIME_QUERY'
        observed=(times[0].dwHighDateTime<<32)|times[0].dwLowDateTime
        if creation is not None and observed!=creation:return 'ORIGINAL_GONE_PID_REUSED'
        wait=k.WaitForSingleObject(handle,0)
        return 'EXITED' if wait==0 else ('ACTIVE' if wait==258 else 'UNKNOWN_WAIT_ERROR')
    finally:k.CloseHandle(handle)
def fresh(path,value):
    with path.open('x',encoding='utf8',newline='\n') as f:json.dump(value,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
def session_path(value):
    p=Path(value).resolve(strict=True)
    if p.parent!=LIVE.resolve() or p.is_symlink() or not p.is_dir():raise ValueError('not_observer_session')
    for q in (p,*p.parents):
        if q.is_junction() or q.is_symlink():raise ValueError('session_reparse')
    return p
def manifest(build,expected):
    build=Path(build).resolve(strict=True)
    if sha(build/'build.json')!=expected:raise ValueError('reviewed_manifest_hash')
    m=json.loads((build/'build.json').read_text());assert m['version']=='0.8.0' and m['schema']==8
    assert sha(build/'SorNativePositionOracle.dll')==m['files']['Data/SFSE/Plugins/SorNativePositionOracle.dll']['sha256']
    assert sha(build/'SorNativePositionOracle-0.8.0.zip')==m['zip_sha256']
    for p,h in m['protected'].items():
        if sha(p)!=h:raise ValueError('protected_input_changed: '+p)
    for p,h in ((m['game_path'],m['game_hash']),(m['sfse_path'],m['sfse_hash'])):
        if sha(p)!=h:raise ValueError('game_or_sfse_identity')
    for p,h in m['external_runtime'].items():
        if sha(p)!=h:raise ValueError('runtime_prerequisite_changed: '+p)
    for p,h in m['sources'].items():
        if sha(p)!=h:raise ValueError('reviewed_operational_source_changed: '+p)
    return m
def audit_deployed(m,expected=True):
    p=GAME/'Data/SFSE/Plugins/SorNativePositionOracle.dll'
    if expected:
        if sha(p)!=m['files']['Data/SFSE/Plugins/SorNativePositionOracle.dll']['sha256']:raise ValueError('deployed_DLL_identity')
        if sha(GAME/'sfse_1_16_244.dll')!=m['sfse_hash']:raise ValueError('installed_SFSE_identity')
    elif p.exists():raise ValueError('observer_still_deployed')
def session_identity(p,m):
    s=json.loads((p/'session.json').read_text());expected=m['files']['Data/SFSE/Plugins/SorNativePositionOracle.dll']['sha256']
    if (s.get('version'),s.get('schema'),s.get('game_sha256'),s.get('sfse_sha256'),s.get('dll_sha256'))!=('0.8.0',8,m['game_hash'],m['sfse_hash'],expected):raise ValueError('session_identity_mismatch')
    return s
def admission(p,m,s):
    a=json.loads((p/'admission.json').read_text());assert a['sole_thread_observed'] and a['owned_sites_original'] and a['dll_sha256']==s['dll_sha256']
    patches=json.loads((p/'patches.json').read_text())['patches'];by_rva={x['rva']:x for x in patches}
    assert len(by_rva)==len(patches)==len(m['guards'])
    for g in m['guards']:
        x=by_rva[g['site']];assert x['length']==g['length']
        original=bytes.fromhex(g['original']) if g['length']==5 else (int(s['module_base'],16)+g['target']).to_bytes(8,'little')
        assert x['original_sha256']==hashlib.sha256(original).hexdigest()
    return dict(sole_thread_observed=True,site_count=len(patches),startup_wait_ms=a['startup_wait_ms'])
def stop_control(p):
    flag=p/'operator-stop.flag'
    if flag.is_file():
        if flag.stat().st_size!=4:raise ValueError('stop_flag_size')
        with flag.open('r+b') as f:f.write(b'STOP');f.flush();os.fsync(f.fileno())
        return 'STOP_REQUESTED_PREALLOCATED_FLAG'
    guard() # old admission-stage fallback only when allocation remains safe
    with (p/'STOP').open('xb') as f:f.write(b'STOP\n');f.flush();os.fsync(f.fileno())
    return 'STOP_REQUESTED_FILE'
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('action',choices=['preflight','request','status','stop','postflight','seal']);ap.add_argument('--build',type=Path,required=True);ap.add_argument('--manifest-sha256',required=True);ap.add_argument('--session',type=Path);ap.add_argument('--nonce');ap.add_argument('--deployed',action='store_true');ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    if a.action=='stop':
        if a.session is None:raise ValueError('session_required')
        if sha(a.build/'build.json')!=a.manifest_sha256:raise ValueError('reviewed_manifest_hash')
        m=json.loads((a.build/'build.json').read_text());assert m['version']=='0.8.0' and m['schema']==8
        p=session_path(a.session);s=session_identity(p,m)
        # STOP is available even if protected files changed, the deployed DLL
        # vanished or disk queries fail. This overwrites exactly four allocated
        # control bytes. It does not perform admission or certify health.
        result=dict(action='stop',session=str(p),status=stop_control(p),pid=s['pid'])
        try:guard()
        except Exception as exc:result['disk_guard_error']=str(exc);print(json.dumps(result));return
        a.out.parent.mkdir(parents=True,exist_ok=True);fresh(a.out,result);print(json.dumps(result,indent=2));return
    space=guard();m=manifest(a.build,a.manifest_sha256);result=dict(action=a.action,utc=datetime.datetime.now(datetime.UTC).isoformat(),disk=space,manifest_sha256=a.manifest_sha256,protected_count=len(m['protected']))
    if a.action=='preflight':
        if a.deployed:audit_deployed(m)
        result.update(status='PASS_OFFLINE_PINS' if not a.deployed else 'PASS_DEPLOYED_PREFLIGHT',runtime_payload=m['runtime_essential'],existing_sessions=[p.name for p in LIVE.glob('session-*')] if LIVE.exists() else [])
    else:
        if a.session is None:raise ValueError('session_required')
        p=session_path(a.session);s=session_identity(p,m);result.update(session=str(p),process=s['pid'],process_creation_filetime=s['process_creation_filetime'])
        if a.action=='request':
            nonce=uuid.uuid4().hex
            with (p/f'control-{nonce}.request').open('xb') as f:f.write(b'ACK\n');f.flush();os.fsync(f.fileno())
            result.update(nonce=nonce,status='REQUESTED_WAIT_FOR_ACK')
        elif a.action=='status':
            audit_deployed(m)
            failure=next((q.name for q in (p/'failure.json',p/'not-ready.json') if q.is_file()),None)
            if (p/'emergency-status.json').is_file():
                page=json.loads((p/'emergency-status.json').read_text())
                if page.get('error'):failure='emergency: '+page['error']
            retired=(p/'retired.json').is_file();ready=(p/'ready.json').is_file();ack=None
            if ready:result['admission']=admission(p,m,s)
            if a.nonce:
                if len(a.nonce)!=32 or any(c not in '0123456789abcdef' for c in a.nonce):raise ValueError('nonce')
                q=p/f'ack-{a.nonce}.json'
                if q.exists():
                    ack=json.loads(q.read_text());assert ack['nonce']==a.nonce and ack['dll_sha256']==s['dll_sha256'] and ack['pid']==s['pid'] and ack['process_creation_filetime']==s['process_creation_filetime'] and not ack['integrity_failure']
            result.update(status='FAILURE' if failure else ('RETIRED' if retired else ('READY_ACK' if ready and ack else 'WAITING_FOR_READY_OR_ACK')),failure=failure,ack=ack,ready=ready,warning='No elapsed-time or monitoring-cadence STOP; investigate stale progress.')
            if failure:raise ValueError('session_failure: '+failure)
        elif a.action=='postflight':
            audit_deployed(m,False);report=inspect(p);result.update(inspection={k:v for k,v in report.items() if k not in ('events','segments','recoverable_uncommitted_records')})
            state=process_state(s['pid'],s['process_creation_filetime']);result['process_state']=state
            result['status']='PASS_TRANSPORT_POSTFLIGHT' if state in ('GONE','EXITED','ORIGINAL_GONE_PID_REUSED') and report['status']=='RETIRED_INTEGRITY_OK' and (p/'retired.json').is_file() else 'PARTIAL_OR_FAILURE_PRESERVE_AND_ANALYZE'
        elif a.action=='seal':
            state=process_state(s['pid'],s['process_creation_filetime'])
            if state not in ('GONE','EXITED','ORIGINAL_GONE_PID_REUSED'):raise ValueError('original_process_not_confirmed_gone')
            result['process_state']=state
            result.update(status='SEALED_INVENTORY',files={q.relative_to(p).as_posix():dict(length=q.stat().st_size,sha256=sha(q)) for q in sorted(p.rglob('*')) if q.is_file()})
    a.out.parent.mkdir(parents=True,exist_ok=True);fresh(a.out,result);print(json.dumps(result,indent=2))
if __name__=='__main__':main()
