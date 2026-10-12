# SPDX-License-Identifier: GPL-3.0-or-later
"""External operational checks for the unchanged 0.3.0 candidate.
Offline audit reads files/process names only. Future approved admission/monitor
reads instrument receipts and limited process creation metadata, publishes
ACK/STOP and exclusive ignored receipts. No target memory, launch, deployment,
save/config writes, native calls or debugger. stdlib + existing project helpers.
"""
import argparse
from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
import struct
import sys
import time
import uuid
import zipfile

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'runtime/native-oracle-030'))
import operate as native
from build import guard,sha
from inspect_events import inspect

def read(p):return json.loads(Path(p).read_text(encoding='utf8'))
def now():return datetime.now(timezone.utc).isoformat()
def write(p,value):
    guard();p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('x',encoding='utf8',newline='\n') as f:
        import os
        json.dump(value,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())

def lock_file(path,expected):
    if sha(path)!=expected:raise ValueError('release_lock_hash')
    lock=read(path)
    if lock['version']!='0.3.0' or lock['schema']!=3:raise ValueError('release_lock_schema')
    return lock

def pins(lock):
    failures=[str(p) for p,s in lock['pins'].items() if not Path(p).is_file() or sha(p)!=s]
    if failures:raise ValueError('protected_or_source_hash:'+repr(failures))

def saves(folder):
    folder=Path(folder)
    if not folder.is_dir():raise ValueError('save_directory_missing')
    return {str(p):dict(bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(folder.iterdir()) if p.is_file() and p.suffix.lower()=='.sfs'}

def archive_check(lock):
    with zipfile.ZipFile(lock['zip']) as z:
        if z.testzip() or len(z.namelist())!=len(set(z.namelist())) or set(z.namelist())!=set(lock['package']):raise ValueError('archive_members')
        if any(hashlib.sha256(z.read(n)).hexdigest()!=s for n,s in lock['package'].items()):raise ValueError('archive_member_hash')

def installation(lock,mode):
    game=Path(lock['game_dir']);plugins=game/'Data/SFSE/Plugins'
    inventory=[dict(path=str(p),bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(plugins.glob('*')) if p.is_file()]
    if mode=='deployed':
        if sorted(p.name for p in plugins.glob('*.dll'))!=['SorNativePositionOracle.dll']:raise ValueError('plugin_conflict')
        for n,s in lock['package'].items():
            p=game/n
            if not p.is_file() or sha(p)!=s:raise ValueError('installed_package:'+n)
    elif mode=='postflight':
        if any((game/n).exists() for n in lock['package']):raise ValueError('candidate_removal_incomplete')
    if mode in ('deployed','postflight'):
        for n,s in lock['installed_loader'].items():
            if sha(game/n)!=s:raise ValueError('installed_loader_hash')
    return inventory

def audit(lock,mode,out):
    space=guard();pins(lock);archive_check(lock);inventory=installation(lock,mode)
    for name in ('save_dir','live_root','game_dir'):
        if not Path(lock[name]).is_dir():raise ValueError('required_directory_missing:'+name)
    running=native.processes() # Toolhelp names only; never OpenProcess here.
    if running:raise ValueError('target_loader_debugger_present:'+repr(running))
    out=Path(out);out.mkdir(exist_ok=False)
    result=dict(utc=now(),mode=mode,pass_check=True,disk=space,plugin_inventory=inventory,
                prior_sessions=[p.name for p in Path(lock['live_root']).glob('session-*')],
                save_inventory=saves(lock['save_dir']),version='0.3.0',lock_pins=len(lock['pins']),
                limits='No live admission/deployment attestation. Vortex profile and gameplay require operator confirmation.')
    write(out/'audit.json',result);return result

def session_path(lock,session):
    original=Path(session).absolute()
    for part in (original,*original.parents):
        if part.is_symlink() or part.is_junction():raise ValueError('session_reparse')
    p=original.resolve(strict=True)
    if p.parent!=Path(lock['live_root']).resolve() or not p.name.startswith('session-'):raise ValueError('session_path')
    return p

def admission(lock,session,run):
    session=session_path(lock,session);before=read(Path(run)/'audit.json')
    if before['mode']!='deployed' or not before['pass_check'] or session.name in before['prior_sessions']:raise ValueError('not_fresh_deployed_session')
    ready=read(session/'ready.json');admit=read(session/'admission.json');patches=read(session/'patches.json')
    expected=dict(component='SorNativePositionOracle',version='0.3.0',schema=3,event_size=17768,
                  dll_sha256=lock['dll_sha256'],game_sha256=lock['game_sha256'],sfse_sha256=lock['sfse_sha256'],
                  grid_channel=True,center_channel=True,heartbeat_ms=1000,health_deadline_ms=15000)
    if any(ready.get(k)!=v for k,v in expected.items()) or ready.get('synthetic'):raise ValueError('ready_identity')
    identity=('pid','process_creation_filetime','dll_sha256','module_base','qpc_frequency','version','schema')
    if any(any(r.get(k)!=ready.get(k) for k in identity) for r in (admit,patches)):raise ValueError('receipt_identity')
    if any(admit.get(k) is not True for k in ('owned_sites_original','sole_thread_observed','standard_overlays_accepted')) or admit.get('patches_installed_at_receipt') is not False:raise ValueError('admission_gate')
    if type(ready.get('startup_wait_ms')) is not int or ready['startup_wait_ms']<0 or type(ready.get('qpc_frequency')) is not int or ready['qpc_frequency']<=0:raise ValueError('startup_clock')
    base=int(ready['module_base'],16);edits=patches['patches'];relays=patches['relays']
    if len(edits)!=13 or len(relays)!=11:raise ValueError('owned_site_count')
    for i,site in enumerate(lock['calls']):
        e=edits[i];relay=relays[i];va=int(relay['runtime_va'],16);target=int(relay['target_va'],16)
        expected_call=b'\xe8'+struct.pack('<i',va-(base+site['rva']+5))
        if int(e['runtime_va'],16)!=base+site['rva'] or e['length']!=5 or e['original_sha256']!=site['sha256'] or e['installed_sha256']!=hashlib.sha256(expected_call).hexdigest():raise ValueError('owned_call_guard')
        relay_bytes=b'\xff\x25'+bytes(4)+struct.pack('<Q',target)
        if relay['length']!=14 or relay['protection']!='PAGE_EXECUTE_READ' or relay['sha256']!=hashlib.sha256(relay_bytes).hexdigest():raise ValueError('relay_guard')
    if len({r['runtime_va'] for r in relays})!=11:raise ValueError('duplicate_relay')
    for i,e in enumerate(edits[11:]):
        expected_slot=hashlib.sha256(struct.pack('<Q',base+0xad8ec0)).hexdigest()
        if int(e['runtime_va'],16)!=base+0x4b916f0+i*8 or e['length']!=8 or e['original_sha256']!=expected_slot or e['installed_sha256']==expected_slot:raise ValueError('callback_slot')
    if edits[11]['installed_sha256']!=edits[12]['installed_sha256']:raise ValueError('callback_slot_disagreement')
    modules=[json.loads(s) for s in (session/'modules-pre-edit.jsonl').read_text(encoding='utf8').splitlines()]
    if not modules:raise ValueError('module_inventory_missing')
    candidates=[m for m in modules if Path(m['path']).name.lower()=='sornativepositionoracle.dll' and m['sha256']==lock['dll_sha256']]
    if len(candidates)!=1:raise ValueError('loaded_candidate_identity')
    low=int(candidates[0]['base'],16);high=low+candidates[0]['size']
    if any(not low<=int(r['target_va'],16)<high for r in relays):raise ValueError('relay_target_outside_candidate')
    return dict(pass_check=True,utc=now(),identity={k:ready[k] for k in identity},modules=modules,
                self_attestation='Plugin-owned-site checks; no external live memory read',
                module_review='Operator/Codex must assess specific competing instrumentation; overlays accepted')

def monitor_sample(session,lock,previous_tick,tick,health_check=native.check_health):
    if previous_tick is not None and tick-previous_tick>10:raise ValueError('external_monitor_gap_over_10s')
    guard()
    if any((session/n).exists() for n in ('failure.json','not-ready.json')):raise ValueError('worker_failure')
    if sum((session/n).stat().st_size for n in ('events.bin','records.jsonl') if (session/n).exists())>512*1024**2:raise ValueError('output_stop_threshold_512MiB')
    report=health_check(session)
    if not report['pass_check']:raise ValueError('health:'+report.get('reason','failed'))
    return report

def monitor(lock,session,run):
    # Validate ownership before any write; never STOP a prior protected session.
    session=session_path(lock,session);run=Path(run);before=read(run/'audit.json')
    if before['mode']!='deployed' or session.name in before['prior_sessions']:raise ValueError('not_fresh_deployed_session')
    try:return monitor_owned(lock,session,run)
    except Exception as exc:
        try:
            if not (session/'STOP').exists():native.request_stop(session)
        finally:print(json.dumps(dict(pass_check=False,error=str(exc),STOP_requested=(session/'STOP').exists())))
        return False

def monitor_owned(lock,session,run):
    session=session_path(lock,session);run=Path(run);admit=admission(lock,session,run);write(run/'admission.json',admit)
    # The module assessment is explicit operator/Codex testimony, not inferred from names.
    attestation=read(run/'operator-confirmation.json')
    if not all(attestation.get(k) is True for k in ('vortex_profile_confirmed','no_competing_native_instrument','pre_edit_modules_assessed')):raise ValueError('operator_confirmation')
    nonce=uuid.uuid4().hex;native.publish_request(session,nonce);start=time.monotonic();previous=None;ack=False;failure=None
    receipt_hashes={n:sha(session/n) for n in ('ready.json','admission.json','patches.json','modules-pre-edit.jsonl')}
    journal=run/'monitor.jsonl'
    try:
        with journal.open('x',encoding='utf8',newline='\n') as f:
            import os
            while not (session/'STOP').exists():
                tick=time.monotonic();report=monitor_sample(session,lock,previous,tick)
                if any(sha(session/n)!=s for n,s in receipt_hashes.items()):raise ValueError('startup_receipt_changed')
                if tick-start>1200:raise ValueError('session_stop_threshold_20min')
                row=dict(utc=now(),elapsed=tick-start,gap=None if previous is None else tick-previous,health=report)
                f.write(json.dumps(row)+'\n');f.flush();os.fsync(f.fileno());previous=tick
                if not ack:
                    challenged=native.check_health(session,nonce)
                    if challenged['pass_check']:
                        if time.monotonic()-start>15:raise ValueError('initial_nonce_ACK_over_15s')
                        write(run/'monitor-ready.json',dict(pass_check=True,utc=now(),nonce=nonce,elapsed=time.monotonic()-start));ack=True
                    elif challenged.get('reason')!='nonce_not_acknowledged_once' or time.monotonic()-start>=15:raise ValueError('initial_nonce_ACK:'+challenged.get('reason','failed'))
                time.sleep(3)
    except Exception as exc:failure=str(exc)
    finally:
        if not (session/'STOP').exists():native.request_stop(session)
    # No unhook/kill/retry: terminal observation only, bounded to30 seconds.
    deadline=time.monotonic()+30
    while not (session/'retired.json').exists() and time.monotonic()<deadline:
        if (session/'failure.json').exists():break
        time.sleep(3)
    write(run/'monitor-ended.json',dict(utc=now(),failure=failure,initial_ACK=ack,retired_receipt_present=(session/'retired.json').exists(),limits='Terminal completeness requires offline inspector. No forced target recovery.'))
    return failure is None and ack and (session/'retired.json').exists()

def postflight(lock,session,run,out):
    result=audit(lock,'postflight',out);before=read(Path(run)/'audit.json')['save_inventory']
    after=result['save_inventory'];changes=dict(new=[p for p in after if p not in before],missing=[p for p in before if p not in after],changed=[p for p in after if p in before and after[p]!=before[p]])
    write(Path(out)/'save-differences.json',changes)
    for receipt in (Path(run)/'checkpoints').glob('*/receipt.json'):
        entry=read(receipt)
        if sha(entry['source'])!=entry['sha256'] or sha(entry['copy'])!=entry['sha256']:raise ValueError('new_checkpoint_integrity')
    report=inspect(session_path(lock,session));write(Path(out)/'inspection.json',report)
    from branch_inspect import analyze
    write(Path(out)/'branch-analysis.json',analyze(report))
    return report['diagnostics']['worker_evidence_qualified'] and not report['truncated_journal'] and not report['unreferenced_tail_bytes']

def checkpoint(lock,run,source,label):
    """Future approved fresh manual slot only; exclusive protected copy, no save edit."""
    source=Path(source).resolve(strict=True);run=Path(run)
    if label not in ('Q030-before','Q030-after') or source.parent!=Path(lock['save_dir']).resolve() or source.suffix.lower()!='.sfs':raise ValueError('checkpoint_selection')
    before=read(run/'audit.json')['save_inventory']
    if str(source) in before or str(source) in lock['pins']:raise ValueError('checkpoint_is_preexisting_save')
    guard()
    if source.stat().st_size>64*1024**2:raise ValueError('checkpoint_size_bound')
    data=source.read_bytes();expected=hashlib.sha256(data).hexdigest();out=run/'checkpoints'/label;out.mkdir(parents=True,exist_ok=False)
    target=out/source.name
    with target.open('xb') as f:
        import os
        f.write(data);f.flush();os.fsync(f.fileno())
    if sha(source)!=expected or sha(target)!=expected:raise ValueError('checkpoint_copy_integrity')
    write(out/'receipt.json',dict(utc=now(),label=label,source=str(source),copy=str(target),sha256=expected,
                                 lineage='OPERATOR_ATTESTED_NOT_INFERRED_FROM_FILENAME'))

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--lock',type=Path,required=True);p.add_argument('--lock-sha',required=True)
    sub=p.add_subparsers(dest='command',required=True)
    a=sub.add_parser('audit');a.add_argument('--mode',choices=['offline','deployed','postflight'],default='offline');a.add_argument('--out',type=Path,required=True)
    a=sub.add_parser('admit');a.add_argument('--session',type=Path,required=True);a.add_argument('--run',type=Path,required=True)
    a=sub.add_parser('monitor');a.add_argument('--session',type=Path,required=True);a.add_argument('--run',type=Path,required=True)
    a=sub.add_parser('postflight');a.add_argument('--session',type=Path,required=True);a.add_argument('--run',type=Path,required=True);a.add_argument('--out',type=Path,required=True)
    a=sub.add_parser('inventory');a.add_argument('--out',type=Path,required=True)
    a=sub.add_parser('checkpoint');a.add_argument('--run',type=Path,required=True);a.add_argument('--source',type=Path,required=True);a.add_argument('--label',required=True)
    a=p.parse_args();lock=lock_file(a.lock,a.lock_sha)
    if a.command=='audit':audit(lock,a.mode,a.out)
    elif a.command=='admit':print(json.dumps(admission(lock,a.session,a.run),indent=2))
    elif a.command=='monitor':raise SystemExit(0 if monitor(lock,a.session,a.run) else 2)
    elif a.command=='inventory':write(a.out,saves(lock['save_dir']))
    elif a.command=='checkpoint':checkpoint(lock,a.run,a.source,a.label)
    else:raise SystemExit(0 if postflight(lock,a.session,a.run,a.out) else 2)
if __name__=='__main__':main()
