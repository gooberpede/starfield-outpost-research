# SPDX-License-Identifier: GPL-3.0-or-later
"""Read-only inventories; original Toolhelp metadata binding from project patterns.
Offline files mode: local config/load-order contents+hashes and game file metadata.
Future approved modules mode: bounded cooperative worker-receipt inventory and
disk hashes, fresh ACK and limited creation metadata. No external loader snapshot.
"""
import argparse
import ctypes
from ctypes import wintypes as W
import json
import subprocess
import sys
import time
import uuid
import re
import hashlib
from pathlib import Path
from procedure import ROOT,read,write,sha,guard,lock_file,session_path,native,now

CONFIGS=[Path('C:/Users/User/AppData/Local/Starfield')/n for n in ('Plugins.txt','loadorder.txt')]+[
    Path('C:/Users/User/Documents/My Games/Starfield')/n for n in ('Starfield.ini','StarfieldCustom.ini','StarfieldPrefs.ini')]

def files(lock,out,configs=CONFIGS):
    guard();rows=[]
    for path in configs:
        try:
            if not path.exists():rows.append(dict(path=str(path),state='ABSENT'));continue
            if path.stat().st_size>1024**2:raise ValueError('config_size_bound')
            raw=path.read_bytes()
            rows.append(dict(path=str(path),state='PRESENT',bytes=len(raw),sha256=sha(path),
                             content=raw.decode('utf-8-sig',errors='strict')))
        except Exception as exc:
            write(out,dict(pass_check=False,utc=now(),rows=rows,unreadable=str(path),error=str(exc)));return False
    game=Path(lock['game_dir'])
    if not game.is_dir():raise ValueError('game_missing')
    inventory=[dict(path=str(p),bytes=p.stat().st_size) for p in sorted(game.iterdir()) if p.is_file()]
    data=[dict(path=str(p),bytes=p.stat().st_size) for p in sorted((game/'Data').iterdir()) if p.is_file()]
    write(out,dict(pass_check=True,utc=now(),rows=rows,game_inventory=inventory,data_inventory=data,
                   limits='Absent is distinct from unreadable; profile selection remains operator-confirmed. No save parsing.'))
    return True

def module_snapshot(pid):
    raise RuntimeError('external_module_snapshot_disabled')


def inventory_files(session):
    files={}
    for path in session.glob('modules-*.jsonl'):
        if path.name=='modules-pre-edit.jsonl':continue
        match=re.fullmatch(r'modules-([1-9][0-9]*)\.jsonl',path.name)
        if not match:raise ValueError('inventory_filename')
        if path.is_symlink() or path.is_junction():raise ValueError('inventory_reparse')
        files[int(match[1])]=path
    if not files or len(files)>2048 or sorted(files)!=list(range(1,len(files)+1)):raise ValueError('inventory_sequence')
    return files

def read_inventory(path,lock,ready):
    if path.stat().st_size>1024**2:raise ValueError('inventory_size_bound')
    data=path.read_bytes()
    if not data or len(data)>1024**2 or not data.endswith(b'\n'):raise ValueError('inventory_incomplete')
    rows=[json.loads(line) for line in data.decode('utf8').splitlines()]
    if not 1<=len(rows)<=2048:raise ValueError('inventory_count')
    bases=set();paths=set()
    for row in rows:
        path=Path(row['path']);base=int(row['base'],16);size=row['size']
        if not path.is_absolute() or not re.fullmatch('[A-Za-z]:',path.drive):raise ValueError('inventory_nonlocal_path')
        if type(size) is not int or size<=0 or base<=0 or base+size>=2**64:raise ValueError('inventory_address')
        if base in bases or str(path).casefold() in paths:raise ValueError('inventory_duplicate')
        bases.add(base);paths.add(str(path).casefold())
        readable=row.get('hash_status')=='READ_OK' and re.fullmatch('[0-9a-f]{64}',row.get('sha256',''))
        if readable:
            guard()
            if sha(path)!=row['sha256']:raise ValueError('inventory_disk_hash')
        else:row['assessment']='UNREADABLE_NONCRITICAL_UNLESS_REQUIRED_IDENTITY_OR_SPECIFIC_CONFLICT'
    required=[('Starfield.exe',lock['game_sha256']),('sfse_1_16_244.dll',lock['sfse_sha256']),('SorNativePositionOracle.dll',lock['dll_sha256'])]
    required.extend((Path(p).name,h) for p,h in lock.get('external_runtime_prerequisites',{}).items())
    for name,expected in required:
        found=[row for row in rows if Path(row['path']).name.casefold()==name.casefold()]
        if len(found)!=1 or found[0]['sha256']!=expected or found[0].get('hash_status')!='READ_OK':raise ValueError('inventory_required_identity:'+name)
        if name=='Starfield.exe' and int(found[0]['base'],16)!=int(ready['module_base'],16):raise ValueError('inventory_game_base')
    return rows,data

def modules(lock,session):
    if lock.get('module_inventory_source')!='040_WORKER_COOPERATIVE_INVENTORY':raise ValueError('cooperative_inventory_contract_not_pinned')
    session=session_path(lock,session);ready=read(session/'ready.json')
    expected=dict(component='SorNativePositionOracle',version='0.4.0',schema=4,event_size=17768,
                  dll_sha256=lock['dll_sha256'],game_sha256=lock['game_sha256'],sfse_sha256=lock['sfse_sha256'])
    if any(ready.get(k)!=v for k,v in expected.items()) or ready.get('synthetic'):raise ValueError('session_identity')
    initial=native.check_health(session)
    if not initial['pass_check']:raise ValueError('initial_health:'+initial.get('reason','failed'))
    before=inventory_files(session)
    nonce=uuid.uuid4().hex;start=time.monotonic();native.publish_request(session,nonce)
    while True:
        health=native.check_health(session,nonce)
        if health['pass_check']:
            if time.monotonic()-start>15:raise ValueError('inventory_ACK_late')
            break
        if health.get('reason')!='nonce_not_acknowledged_once' or time.monotonic()-start>=15:raise ValueError('inventory_ACK:'+health.get('reason','failed'))
        time.sleep(0.25)
    files=inventory_files(session);path=files[len(files)];rows,data=read_inventory(path,lock,ready)
    if inventory_files(session)!=files or path.read_bytes()!=data:raise ValueError('inventory_changed_during_read')
    final=native.check_health(session,nonce)
    if not final['pass_check']:raise ValueError('final_health:'+final.get('reason','failed'))
    health_rows=[json.loads(line) for line in (session/'health.jsonl').read_bytes().splitlines(keepends=True) if line.endswith(b'\n')]
    acknowledged=[row for row in health_rows if row.get('nonce')==nonce]
    if len(acknowledged)!=1:raise ValueError('inventory_ACK_receipt')
    if inventory_files(session)!=files or path.read_bytes()!=data:raise ValueError('inventory_changed_after_health')
    if read(session/'ready.json')!=ready:raise ValueError('ready_changed')
    return dict(pass_check=True,utc=now(),pid=ready['pid'],process_creation_filetime=ready['process_creation_filetime'],
                source='040_WORKER_COOPERATIVE_INVENTORY',inventory_file=str(path),
                inventory_sha256=hashlib.sha256(data).hexdigest(),inventory_serial=len(files),pre_ACK_inventory_serial=len(before),
                nonce=nonce,ACK_health_sequence=acknowledged[0]['health_sequence'],modules=rows,
                limits='Last complete worker-emitted inventory plus fresh worker progress. ACK has no inventory digest/serial. Separate set/inventory scans can race, including A-B-A leaving an older snapshot. Not exact ACK-time membership, independent external enumeration, or live-byte proof. Assess specific competing instrumentation; overlays accepted.')

def bounded_modules(lockpath,locksha,session,out,runner=subprocess.run):
    # Timeout terminates only this inventory helper, never the game/loader/observer.
    try:
        result=runner([sys.executable,'-B',str(Path(__file__).resolve()),'--lock',str(lockpath),
                       '--lock-sha',locksha,'worker','--session',str(session)],capture_output=True,text=True,timeout=30)
        if result.returncode:raise ValueError('module_worker:'+result.stderr[-2000:])
        report=json.loads(result.stdout)
        if report.get('pass_check') is not True:raise ValueError('module_inventory_failed')
    except Exception as exc:write(out,dict(pass_check=False,utc=now(),error=str(exc)));return False
    write(out,report);return True

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--lock',type=Path,required=True);p.add_argument('--lock-sha',required=True)
    sub=p.add_subparsers(dest='command',required=True)
    a=sub.add_parser('files');a.add_argument('--out',type=Path,required=True)
    a=sub.add_parser('modules');a.add_argument('--session',type=Path,required=True);a.add_argument('--out',type=Path,required=True)
    a=sub.add_parser('worker');a.add_argument('--session',type=Path,required=True)
    a=p.parse_args();lock=lock_file(a.lock,a.lock_sha)
    if a.command=='worker':print(json.dumps(modules(lock,a.session)));return
    ok=files(lock,a.out) if a.command=='files' else bounded_modules(a.lock,a.lock_sha,a.session,a.out)
    raise SystemExit(0 if ok else 2)
if __name__=='__main__':main()
