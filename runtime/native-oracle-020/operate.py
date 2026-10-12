# SPDX-License-Identifier: GPL-3.0-or-later
"""Local preflight/control/postflight receipts for the reviewed card.
Reads build/module/save/frozen/source files and Windows process names/PIDs;
writes new ignored receipts/attestations/STOP only. No process-memory access,
launch, native attachment, target writes, game/Vortex/settings/save changes.
--deployed checks user-installed bytes; it does not deploy them.
"""
import argparse
import ctypes
from ctypes import wintypes as W
from datetime import datetime,timezone
import json
from pathlib import Path
import re
from build import ROOT,CONFIG,sha,guard

GAME=Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield')
LIVE=ROOT/'.local-work/native-oracle-live'
def new_json(path,data):
    import os
    guard();path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('x',encoding='utf8',newline='\n') as f:json.dump(data,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
def processes():
    class Entry(ctypes.Structure):
        _fields_=[('size',W.DWORD),('usage',W.DWORD),('pid',W.DWORD),('heap',ctypes.c_size_t),('module',W.DWORD),('threads',W.DWORD),('parent',W.DWORD),('priority',W.LONG),('flags',W.DWORD),('name',W.WCHAR*260)]
    kernel=ctypes.WinDLL('kernel32',use_last_error=True)
    kernel.CreateToolhelp32Snapshot.argtypes=[W.DWORD,W.DWORD];kernel.CreateToolhelp32Snapshot.restype=W.HANDLE
    for name in ('Process32FirstW','Process32NextW'):
        f=getattr(kernel,name);f.argtypes=[W.HANDLE,ctypes.POINTER(Entry)];f.restype=W.BOOL
    kernel.CloseHandle.argtypes=[W.HANDLE];kernel.CloseHandle.restype=W.BOOL
    snapshot=kernel.CreateToolhelp32Snapshot(2,0)
    if snapshot==ctypes.c_void_p(-1).value:raise ctypes.WinError(ctypes.get_last_error())
    rows=[];entry=Entry();entry.size=ctypes.sizeof(entry)
    try:
        if not kernel.Process32FirstW(snapshot,ctypes.byref(entry)):raise ctypes.WinError(ctypes.get_last_error())
        while True:
            if entry.name.lower() in ('starfield.exe','sfse_loader.exe','x64dbg.exe','x32dbg.exe','windbg.exe'):rows.append(dict(name=entry.name,pid=entry.pid))
            if not kernel.Process32NextW(snapshot,ctypes.byref(entry)):
                if ctypes.get_last_error()!=18:raise ctypes.WinError(ctypes.get_last_error())
                break
    finally:kernel.CloseHandle(snapshot)
    return rows
def preflight(build,deployed,postflight=False):
    manifest=json.loads((build/'build.json').read_text());baseline=json.loads((ROOT/'.local-work/native-oracle/baseline.json').read_text())
    checks=[]
    def pin(path,expected):
        actual=sha(path) if Path(path).is_file() else None;checks.append(dict(path=str(path),expected=expected,actual=actual,pass_check=actual==expected))
    pin(build/'SorNativePositionOracle-0.2.0.zip',manifest['zip_sha256']);pin(GAME/'Starfield.exe',manifest['game_hash'])
    sfse=GAME/'sfse_1_16_244.dll' if deployed or postflight else Path(manifest['sfse_path']);pin(sfse,manifest['sfse_hash'])
    pin(sfse.parent/'sfse_loader.exe','16916c2ec47e31774e3d550609a1844fcb368b03060c03511891564b7f5f7526')
    for row in baseline['protected']:pin(row['path'],row['expected'])
    for name,expected in manifest['sources'].items():pin(ROOT/name,expected)
    if deployed:
        for name,info in manifest['files'].items():
            if name.startswith('Data/SFSE/Plugins/'):pin(GAME/name,info['sha256'])
        plugin_dir=GAME/'Data/SFSE/Plugins';dlls=sorted(p.name for p in plugin_dir.glob('*.dll'))
        checks.append(dict(name='only reviewed SFSE plugin DLL',actual=dlls,pass_check=dlls==['SorNativePositionOracle.dll']))
        checks.append(dict(name='default grid and center config; Q E always on',pass_check=(plugin_dir/'SorNativePositionOracle.config').read_bytes()==CONFIG))
    running=processes();checks.append(dict(name='target and debugger processes absent',actual=running,pass_check=not running))
    space=guard()
    return dict(kind='postflight' if postflight else 'preflight',utc=datetime.now(timezone.utc).isoformat(),deployed=deployed,pass_check=all(c['pass_check'] for c in checks),disk=space,checks=checks,
        limits='File/module pins and process-name inventory only; no live pointer/patch inspection or Vortex profile attestation. Normal Steam/NVIDIA overlays accepted by continuation brief; only owned-site conflicts/identity/startup/health failures block. Runtime admission required; process-name inventory is limited.')
def process_identity(pid):
    kernel=ctypes.WinDLL('kernel32',use_last_error=True)
    kernel.OpenProcess.argtypes=[W.DWORD,W.BOOL,W.DWORD];kernel.OpenProcess.restype=W.HANDLE
    kernel.GetProcessTimes.argtypes=[W.HANDLE,*([ctypes.POINTER(W.FILETIME)]*4)];kernel.GetProcessTimes.restype=W.BOOL
    kernel.GetExitCodeProcess.argtypes=[W.HANDLE,ctypes.POINTER(W.DWORD)];kernel.GetExitCodeProcess.restype=W.BOOL
    kernel.CloseHandle.argtypes=[W.HANDLE]
    handle=kernel.OpenProcess(0x1000,False,pid)
    if not handle:raise ctypes.WinError(ctypes.get_last_error())
    try:
        times=[W.FILETIME() for _ in range(4)];code=W.DWORD()
        if not kernel.GetProcessTimes(handle,*[ctypes.byref(t) for t in times]) or not kernel.GetExitCodeProcess(handle,ctypes.byref(code)):raise ctypes.WinError(ctypes.get_last_error())
        if code.value!=259:raise RuntimeError('target_not_active')
        return (times[0].dwHighDateTime<<32)|times[0].dwLowDateTime
    finally:kernel.CloseHandle(handle)

def valid_health_counts(row):
    scalar=('health_sequence','qpc','flushed_events','flushed_offset','queue_depth','lost','health_timeouts','depth_errors')
    uint=lambda v:type(v) is int and 0<=v<2**64
    return (all(uint(row.get(k)) for k in scalar) and type(row.get('stopping')) is bool
            and all(type(row.get(k)) is list and len(row[k])==3 and all(uint(v) for v in row[k]) for k in ('active','entered')))

def valid_health_transition(previous,row,frequency):
    if type(frequency) is not int or frequency<=0:return False
    if row['lost'] or row['depth_errors'] or row['health_timeouts']:return False
    if row['flushed_offset']!=row['flushed_events']*17768 or row['queue_depth']>4096:return False
    if previous:
        gap=row['qpc']-previous['qpc']
        if not 0<=gap<=frequency*15:return False
        if row['flushed_events']<previous['flushed_events']:return False
        if any(a<b for a,b in zip(row['entered'],previous['entered'])):return False
    return True

def check_health(session,nonce=None,now=None,verify_process=True):
    # verify_process=False is for original disposable tests, never a CLI option.
    try:
        ready=json.loads((session/'ready.json').read_text(encoding='utf8'))
        if ready.get('component')!='SorNativePositionOracle' or ready.get('version')!='0.2.0' or ready.get('schema')!=2 or ready.get('event_size')!=17768:raise ValueError('ready_schema')
        if any((session/n).exists() for n in ('failure.json','not-ready.json','retired.json','STOP')):raise ValueError('failure_or_stopped')
        if verify_process and process_identity(ready['pid'])!=ready['process_creation_filetime']:raise ValueError('process_identity')
        rows=[]
        for line in (session/'health.jsonl').read_bytes().splitlines(keepends=True):
            if not line.endswith(b'\n'):break
            row=json.loads(line)
            if not valid_health_counts(row):raise ValueError('health_counter_schema')
            if row['health_sequence']!=len(rows)+1:raise ValueError('health_sequence')
            if any(row.get(k)!=ready.get(k) for k in ('component','version','pid','process_creation_filetime','dll_sha256','qpc_frequency')):raise ValueError('health_identity')
            if not valid_health_transition(rows[-1] if rows else None,row,ready.get('qpc_frequency')):raise ValueError('historical_health_failure')
            rows.append(row)
        if not rows:raise ValueError('health_missing')
        current=now or datetime.now(timezone.utc)
        required=[rows[-1]]
        if nonce:
            if not re.fullmatch('[0-9a-f]{32}',nonce):raise ValueError('nonce_schema')
            matches=[r for r in rows if r['nonce']==nonce]
            if len(matches)!=1:raise ValueError('nonce_not_acknowledged_once')
            required+=matches
        for row in required:
            age=(current-datetime.fromisoformat(row['health_utc'].replace('Z','+00:00'))).total_seconds()
            if not -2<=age<=15 or row['stopping'] or row['lost'] or row['depth_errors'] or row.get('health_timeouts',0):raise ValueError('stale_or_failed_health')
        return dict(pass_check=True,nonce=nonce,latest=rows[-1],limits='Fresh durable worker response/process metadata only; not native boundary reachability or no competing code anywhere.')
    except Exception as e:return dict(pass_check=False,error=type(e).__name__,reason=str(e))

def publish_request(session,nonce,before_publish=None):
    """Windows same-directory rename publishes a flushed payload without replacement.
    A .pending file is deliberately outside the worker request filename grammar.
    """
    import os
    guard()
    pending=session/('control-'+nonce+'.pending')
    final=session/('control-'+nonce+'.request')
    with pending.open('xb') as f:
        if before_publish:before_publish(pending,final)
        f.write(b'ACK\n');f.flush();os.fsync(f.fileno())
    # Path.rename on Windows fails if destination already exists.
    pending.rename(final)

def request_stop(session):
    # Emergency retirement must remain available below the capture disk floor.
    import os
    with (session/'STOP').open('xb') as f:
        f.write(b'STOP\n');f.flush();os.fsync(f.fileno())

def main():
    ap=argparse.ArgumentParser(description=__doc__);sub=ap.add_subparsers(dest='command',required=True)
    p=sub.add_parser('preflight');p.add_argument('--build',type=Path,required=True);p.add_argument('--deployed',action='store_true');p.add_argument('--postflight',action='store_true');p.add_argument('--receipt',required=True)
    p=sub.add_parser('control');p.add_argument('session',type=Path);p.add_argument('action',choices=['STOP','mark','challenge']);p.add_argument('--label');p.add_argument('--note',default='')
    p=sub.add_parser('health');p.add_argument('session',type=Path);p.add_argument('--nonce')
    a=ap.parse_args()
    if a.command=='preflight':
        if not re.fullmatch('[a-zA-Z0-9-]+',a.receipt):raise ValueError('receipt_name')
        try:report=preflight(a.build.resolve(),a.deployed,a.postflight)
        except Exception as e:report=dict(pass_check=False,error=type(e).__name__,message=str(e),utc=datetime.now(timezone.utc).isoformat())
        out=ROOT/'.local-work/native-oracle-020/operations'/(a.receipt+'.json');new_json(out,report);print(json.dumps(dict(receipt=str(out),pass_check=report['pass_check'])));raise SystemExit(0 if report['pass_check'] else 2)
    session=a.session.resolve(strict=True)
    if session.parent!=LIVE.resolve() or not session.name.startswith('session-'):raise ValueError('session_path')
    ready=json.loads((session/'ready.json').read_text())
    if ready.get('component')!='SorNativePositionOracle' or ready.get('version')!='0.2.0':raise ValueError('session_identity')
    if a.command=='health':
        report=check_health(session,a.nonce);print(json.dumps(report));raise SystemExit(0 if report['pass_check'] else 2)
    if a.action=='challenge':
        import uuid,os
        nonce=uuid.uuid4().hex;publish_request(session,nonce)
        print(json.dumps(dict(session=str(session),nonce=nonce)));return
    if a.action=='STOP':
        request_stop(session)
    else:
        if not a.label or not re.fullmatch('[a-zA-Z0-9-]{1,96}',a.label):raise ValueError('label')
        new_json(session/(a.label+'.operator.json'),dict(utc=datetime.now(timezone.utc).isoformat(),label=a.label,note=a.note,operator_attestation=True,scientific_identity='NOT_INFERRED_FROM_OPERATOR_NOTE'))
    print(json.dumps(dict(session=str(session),action=a.action)))
if __name__=='__main__':main()
