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
LOCAL=ROOT/'.local-work/resource-combined-acquisition'
spec=importlib.util.spec_from_file_location('c1d_transport',ROOT/'research/resource-oracle-retail/collect.py')
transport=importlib.util.module_from_spec(spec)
spec.loader.exec_module(transport)
from qualify import independent
sys.path.append(str(ROOT/"research/resource-tungsten-acquisition"))
from reduce import Tracker


def acquire(command, output, tracker, synthetic=False, stop_after_construction=False):
    """Shared durable pump; caller supplies an already admitted fixed command.

    Synthetic dispatch can only select a pinned fixture. Retail admission stays
    in main and is never bypassed by this helper or a synthetic authority file.
    """
    incoming=queue.Queue(maxsize=64)
    with (output/'stderr.txt').open('xb') as err:
        p=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=err,text=True)
        def reader():
            for line in p.stdout:
                incoming.put(line)
            incoming.put(None)
        threading.Thread(target=reader,daemon=True).start()
        session=None;stop=False;captures=acks=0;success_capture=None;success_ack=False;losses=0
        with (output/'events.jsonl').open('x',encoding='utf8',newline='\n') as events:
            while True:
                if not stop and ((output/'STOP').exists() or min(shutil.disk_usage(d).free for d in ('C:/','D:/'))<40_000_000_000):
                    p.stdin.write('STOP\n');p.stdin.flush();stop=True
                try:line=incoming.get(timeout=1)
                except queue.Empty:continue
                if line is None:break
                row=json.loads(line);row['synthetic']=synthetic
                events.write(json.dumps(row)+'\n');events.flush();os.fsync(events.fileno())
                if row['kind']=='SESSION':session=row
                if row['kind']=='ACK_ACCEPTED' and row['accepted']:
                    acks+=1
                    if row['capture']==success_capture:success_ack=True
                if row['kind'] in ('LOSS','EXCEPTION'):losses+=1
                if row['kind']!='SAMPLE':
                    tracker.feed(row)
                    continue
                captures+=1
                assert session is not None
                complete=row['required_reads_complete'] and all(row[k]['status']=='COMPLETE' for k in ('geometry','selected','refresh_payload','source_context') if k in row)
                complete &= all(row.get(k,True) for k in ('qb_retained_read','closure_read','descriptor_read'))
                path=output/f'capture-{row["capture"]:05d}.bin'
                transport.persist(path,[session,row,dict(kind='END',complete=complete)],synthetic=synthetic)
                assert independent(path)[1]==row
                outcome=tracker.feed(row)
                useful=(outcome=="CONSUMPTION" and bool(tracker.constructions)) or (outcome=="CONSTRUCTION" and stop_after_construction)
                suffix=' STOP' if useful else ' CONSUMER' if outcome=='CONSTRUCTION' else ' PRODUCER' if row['site']=='spatial_transfer_payload' and row['active_updaters']==0 else ''
                p.stdin.write(f'ACK {row["capture"]}{suffix}\n');p.stdin.flush()
                if useful:stop=True;success_capture=row["capture"]
            code=p.wait()
    transport.write(output/'accounting.json',dict(controller_exit=code,captures=captures,accepted_acks=acks,stop_requested=stop,scientific_result=tracker.result()["status"], reduction=tracker.result(),success_capture=success_capture,success_ack=success_ack,loss_events=losses,generation_epoch="UNKNOWN"))
    result=json.loads((output/'accounting.json').read_text(encoding='utf8'))
    assert code==0 and captures==acks
    return result


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--stop-after-construction',action='store_true')
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
    card=ROOT/'docs/experiments/resource-combined-acquisition/run-card.md'
    approval=json.loads(a.approval.read_text(encoding='utf8'))
    pre=json.loads(a.preflight.read_text(encoding='utf8'))
    manifest=json.loads((a.build/'build.json').read_text(encoding='utf8'))
    assert approval['stop_after_construction'] is a.stop_after_construction
    assert approval['status']=='GO_PHASE_B' and approval['human_instruction'].strip()
    assert approval['card_sha256']==transport.pin(card)
    assert approval['build_sha256']==pre['build_sha256']==transport.pin(a.build/'build.json')
    assert approval['preflight_sha256']==transport.pin(a.preflight) and approval['cloud_disabled_confirmed'] is True
    assert approval['used'] is False and manifest['exit_code']==0
    for p,h in manifest['files'].items():
        assert transport.pin(p)==h
    for p,h in pre['code_pins'].items():
        assert transport.pin(p)==h
    tracker=Tracker()
    from save_policy import load_policy, policy_hash, sizes, partition
    assert pre['schema']=='sor-d5b-preflight/1'
    policy=pre['save_policy']
    assert pre['save_policy_sha256']==policy_hash(policy)==policy_hash(load_policy())
    assert pre['status']=='OFFLINE_CHECKED_NOT_AUTHORIZED'
    # Full protected hashes were checked offline before launch. This bounded
    # admission check retains name/size checks without hashing during gameplay.
    current=sizes(Path(pre['live_path']),policy)
    live_parts=partition(current,policy)
    assert not live_parts['unclassified']
    assert {n:r['bytes'] for n,r in live_parts['protected'].items()}=={n:r['bytes'] for n,r in pre['protected_live'].items()}
    folder=Path(pre['backup_path'])
    assert {p.relative_to(folder).as_posix():p.stat().st_size for p in folder.rglob('*') if p.is_file()}=={n:r['bytes'] for n,r in pre['backup'].items()}
    master=Path(pre['fresh_master_path'])
    assert {p.name:p.stat().st_size for p in master.iterdir() if p.is_file()}=={n:r['bytes'] for n,r in pre['fresh_master'].items()}
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
    command=[str(a.build.resolve()/'sor-d5b-controller.exe'),'--retail-pilot',str(a.pid)]
    transport.write(a.output/'config.json',dict(command=command,approval=approval,preflight_sha256=transport.pin(a.preflight),process=process,synthetic=False))
    acquire(command,a.output,tracker,stop_after_construction=a.stop_after_construction)


def synthetic_main():
    """Qualify the operational transport on a pinned disposable fixture only."""
    from d5b_contract import MODES
    ap=argparse.ArgumentParser(description=synthetic_main.__doc__)
    ap.add_argument('--synthetic-qualification',action='store_true',required=True)
    ap.add_argument('--build',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--mode',choices=MODES,required=True)
    ap.add_argument('--stop-after-construction',action='store_true')
    a=ap.parse_args()
    build=a.build.resolve();output=a.output.resolve()
    assert build.is_relative_to(LOCAL) and output.is_relative_to(LOCAL)
    manifest=json.loads((build/'build.json').read_text(encoding='utf8'))
    assert manifest['exit_code']==0
    for path,digest in manifest['files'].items():
        assert transport.pin(path)==digest,path
    output.mkdir(exist_ok=False)
    command=[str(build/'sor-d5b-fixture-controller.exe'),'--synthetic-fixture',transport.pin(build/'sor-d5b-fixture.exe'),a.mode]
    transport.write(output/'config.json',dict(command=command,synthetic=True,build_sha256=transport.pin(build/'build.json')))
    result=acquire(command,output,Tracker(),synthetic=True,stop_after_construction=a.stop_after_construction)
    print(result['scientific_result'])


if __name__=='__main__':
    if '--synthetic-qualification' in sys.argv:
        synthetic_main()
    else:
        main()
