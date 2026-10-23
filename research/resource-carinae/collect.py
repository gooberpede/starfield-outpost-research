# SPDX-License-Identifier: GPL-3.0-or-later
"""FUTURE APPROVAL ONLY: attach to newly Steam-launched, pinned disposable game.

Does not launch Steam/game. Requires explicit maintainer approval receipt bound
to this card, executable build and fresh offline preflight. Declared debugger
DR/RF intervention and process disposal. No save/config writes or restoration.
Uses unchanged owned C1D SRO1 fsync/readback pipeline, stdlib and Windows tooling.
Writes raw native bytes exclusively to a new ignored local directory.
"""
import argparse
import datetime
import json
from pathlib import Path
import queue
import shutil
import subprocess
import sys
import threading
import os
import importlib.util

ROOT=Path(__file__).resolve().parents[2]
LOCAL=ROOT/'.local-work/resource-carinae'
spec=importlib.util.spec_from_file_location('c1d_transport',ROOT/'research/resource-oracle-retail/collect.py')
transport=importlib.util.module_from_spec(spec)
spec.loader.exec_module(transport)
from qualify import independent


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--retail-pilot',action='store_true',required=True)
    ap.add_argument('--approval',type=Path,required=True)
    ap.add_argument('--preflight',type=Path,required=True)
    ap.add_argument('--build',type=Path,required=True)
    ap.add_argument('--pid',type=int,required=True)
    ap.add_argument('--launch-utc',required=True)
    ap.add_argument('--output',type=Path,required=True)
    a=ap.parse_args()
    assert a.pid>0
    for path in (a.approval,a.preflight,a.build,a.output):
        assert path.resolve().is_relative_to(LOCAL)
        for p in (path.resolve(),*path.resolve().parents):
            assert not p.exists() or not p.lstat().st_file_attributes & 0x400
    card=ROOT/'docs/experiments/resource-carinae/run-card.md'
    approval=json.loads(a.approval.read_text())
    pre=json.loads(a.preflight.read_text())
    manifest=json.loads((a.build/'build.json').read_text())
    assert approval['status']=='GO_PHASE_B' and approval['human_instruction'].strip()
    assert approval['card_sha256']==transport.pin(card)
    assert approval['build_sha256']==pre['build_sha256']==transport.pin(a.build/'build.json')
    assert approval['preflight_sha256']==transport.pin(a.preflight) and approval['cloud_disabled_confirmed'] is True
    assert approval['used'] is False and manifest['exit_code']==0
    for p,h in manifest['files'].items():
        assert transport.pin(p)==h
    for p,h in pre['code_pins'].items():
        assert transport.pin(p)==h
    assert pre['live']==pre['backup'] and pre['status']=='OFFLINE_CHECKED_NOT_AUTHORIZED'
    for folder in (Path(pre['live_path']),Path(pre['backup_path'])):
        assert {p.relative_to(folder).as_posix():p.stat().st_size for p in folder.rglob('*') if p.is_file()}=={n:r['bytes'] for n,r in pre['live'].items()}
    assert min(shutil.disk_usage(d).free for d in ('C:/','D:/'))>=40_000_000_000
    process=json.loads(subprocess.check_output(['powershell','-NoProfile','-Command',
        f'Get-Process -Id {a.pid} | Select-Object Id,Path,@{{n="StartUtc";e={{$_.StartTime.ToUniversalTime().ToString("o")}}}} | ConvertTo-Json'],text=True))
    expected='C:/Program Files (x86)/Steam/steamapps/common/Starfield/Starfield.exe'
    assert Path(process['Path'])==Path(expected)
    assert datetime.datetime.fromisoformat(a.launch_utc)>datetime.datetime.fromisoformat(pre['utc'])
    assert datetime.datetime.fromisoformat(process['StartUtc'])>datetime.datetime.fromisoformat(a.launch_utc)
    assert transport.pin(expected)==pre['exe_sha256']
    a.output.mkdir(exist_ok=False)
    # Consume the local operational gate before attachment; does not create authority.
    used=a.approval.with_suffix('.consumed.json')
    transport.write(used,dict(approval_sha256=transport.pin(a.approval),pid=a.pid,output=str(a.output)))
    command=[str(a.build.resolve()/'sor-c2a-controller.exe'),'--retail-pilot',str(a.pid)]
    transport.write(a.output/'config.json',dict(command=command,approval=approval,preflight_sha256=transport.pin(a.preflight),process=process,synthetic=False))
    incoming=queue.Queue(maxsize=64)
    with (a.output/'stderr.txt').open('xb') as err:
        p=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=err,text=True)
        def reader():
            for line in p.stdout:
                incoming.put(line)
            incoming.put(None)
        threading.Thread(target=reader,daemon=True).start()
        session=None;accepted={};stop=False;captures=acks=0
        with (a.output/'events.jsonl').open('x',encoding='utf8',newline='\n') as events:
            while True:
                if not stop and ((a.output/'STOP').exists() or min(shutil.disk_usage(d).free for d in ('C:/','D:/'))<40_000_000_000):
                    p.stdin.write('STOP\n');p.stdin.flush();stop=True
                try:line=incoming.get(timeout=1)
                except queue.Empty:continue
                if line is None:break
                row=json.loads(line);row['synthetic']=False
                events.write(json.dumps(row)+'\n');events.flush();os.fsync(events.fileno())
                if row['kind']=='SESSION':session=row
                if row['kind']=='THREAD_END':
                    accepted={k:v for k,v in accepted.items() if k[0]!=row['tid']}
                if row['kind']=='ACK_ACCEPTED' and row['accepted']:acks+=1
                if row['kind']!='SAMPLE':continue
                captures+=1
                assert session is not None
                complete=row['required_reads_complete'] and all(row[k]['status']=='COMPLETE' for k in ('geometry','selected','refresh_payload') if k in row)
                complete &= all(row.get(k,True) for k in ('qb_retained_read','closure_read','descriptor_read'))
                path=a.output/f'capture-{row["capture"]:05d}.bin'
                transport.persist(path,[session,row,dict(kind='END',complete=complete)],synthetic=False)
                assert independent(path)[1]==row
                key=(row['tid'],row['thread_lifetime'],row['updater_token'])
                if row.get('decision')=='ACCEPT' and row['ancestry']=='BOUND_CALLBACK' and complete and row['file_provenance']['main_file_identity']:
                    raw=bytes.fromhex(row['selected']['raw_resource']);formid=int.from_bytes(raw[40:44],'little')
                    if formid in (0x57c7,0x57c9,0x5df1):
                        accepted.setdefault(key,{})[row['resource_pointer']]=formid
                useful=False
                if 'refresh_payload' in row:
                    payload=row['refresh_payload']
                    useful=row['ancestry']=='BOUND_TRANSFER' and payload['status']=='COMPLETE' and any(accepted.get(key,{}).get(m['pointer'])==0x57c7 for m in payload.get('members') or [])
                    accepted.pop(key,None)
                assert len(accepted)<=4096,'local active-invocation memory budget'
                p.stdin.write(f'ACK {row["capture"]}'+(' STOP' if useful else '')+'\n');p.stdin.flush()
                if useful:stop=True
            code=p.wait()
    transport.write(a.output/'accounting.json',dict(controller_exit=code,captures=captures,accepted_acks=acks,stop_requested=stop))
    assert code==0 and captures==acks


if __name__=='__main__':
    main()
