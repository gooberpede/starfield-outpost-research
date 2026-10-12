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
    pin(build/'SorNativePositionOracle-0.1.0.zip',manifest['zip_sha256']);pin(GAME/'Starfield.exe',manifest['game_hash'])
    sfse=GAME/'sfse_1_16_244.dll' if deployed else Path(manifest['sfse_path']);pin(sfse,manifest['sfse_hash'])
    pin(sfse.parent/'sfse_loader.exe','16916c2ec47e31774e3d550609a1844fcb368b03060c03511891564b7f5f7526')
    for row in baseline['protected']:pin(row['path'],row['expected'])
    for name,expected in manifest['sources'].items():pin(ROOT/name,expected)
    if deployed:
        for name,info in manifest['files'].items():
            if name.startswith('Data/SFSE/Plugins/'):pin(GAME/name,info['sha256'])
        plugin_dir=GAME/'Data/SFSE/Plugins';dlls=sorted(p.name for p in plugin_dir.glob('*.dll'))
        checks.append(dict(name='only reviewed SFSE plugin DLL',actual=dlls,pass_check=dlls==['SorNativePositionOracle.dll']))
        checks.append(dict(name='default grid and center config',pass_check=(plugin_dir/'SorNativePositionOracle.config').read_bytes()==CONFIG))
    running=processes();checks.append(dict(name='target and debugger processes absent',actual=running,pass_check=not running))
    space=guard()
    return dict(kind='postflight' if postflight else 'preflight',utc=datetime.now(timezone.utc).isoformat(),deployed=deployed,pass_check=all(c['pass_check'] for c in checks),disk=space,checks=checks,
        limits='File/module pins and process-name inventory only; no live pointer/patch inspection or Vortex profile attestation. User confirms exclusive profile; plugin startup guards/READY complete live admission.')
def main():
    ap=argparse.ArgumentParser(description=__doc__);sub=ap.add_subparsers(dest='command',required=True)
    p=sub.add_parser('preflight');p.add_argument('--build',type=Path,required=True);p.add_argument('--deployed',action='store_true');p.add_argument('--postflight',action='store_true');p.add_argument('--receipt',required=True)
    p=sub.add_parser('control');p.add_argument('session',type=Path);p.add_argument('action',choices=['STOP','mark']);p.add_argument('--label');p.add_argument('--note',default='')
    a=ap.parse_args()
    if a.command=='preflight':
        if not re.fullmatch('[a-zA-Z0-9-]+',a.receipt):raise ValueError('receipt_name')
        try:report=preflight(a.build.resolve(),a.deployed,a.postflight)
        except Exception as e:report=dict(pass_check=False,error=type(e).__name__,message=str(e),utc=datetime.now(timezone.utc).isoformat())
        out=ROOT/'.local-work/native-oracle/operations'/(a.receipt+'.json');new_json(out,report);print(json.dumps(dict(receipt=str(out),pass_check=report['pass_check'])));raise SystemExit(0 if report['pass_check'] else 2)
    session=a.session.resolve(strict=True)
    if session.parent!=LIVE.resolve() or not session.name.startswith('session-'):raise ValueError('session_path')
    ready=json.loads((session/'ready.json').read_text())
    if ready.get('component')!='SorNativePositionOracle' or ready.get('version')!='0.1.0':raise ValueError('session_identity')
    if a.action=='STOP':
        guard()
        with (session/'STOP').open('xb') as f:f.write(b'STOP\n');f.flush();__import__('os').fsync(f.fileno())
    else:
        if not a.label or not re.fullmatch('[a-zA-Z0-9-]{1,96}',a.label):raise ValueError('label')
        new_json(session/(a.label+'.operator.json'),dict(utc=datetime.now(timezone.utc).isoformat(),label=a.label,note=a.note,operator_attestation=True,scientific_identity='NOT_INFERRED_FROM_OPERATOR_NOTE'))
    print(json.dumps(dict(session=str(session),action=a.action)))
if __name__=='__main__':main()
