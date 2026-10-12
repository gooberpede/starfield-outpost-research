# SPDX-License-Identifier: GPL-3.0-or-later
"""User-authorized external timing correction; approved observer is unchanged.
Reads frozen base lock, source pins, owned fresh-session receipts and health.
Writes exclusive run/ACK/warning/STOP receipts only. No target memory, launch,
deployment, config/save writes, debugger or native calls. Stdlib/project code.
Timing-only warnings never request STOP. Missing fresh ACK never permits load.
Disk, output volume, identity, corruption and actual worker failures stay hard.
"""
import argparse
import json
from pathlib import Path
import time
import uuid
from datetime import datetime, timezone
import procedure as p

BASE_SHA='060db14e0000146ed13537c6b59b688eff238132819b0e42f24a94588f69ab6b'


def timing_reasons(elapsed,gap=None,ack_elapsed=None):
    reasons=[]
    if gap is not None and gap>10:reasons.append('external_sample_gap_over_10s')
    if elapsed>1200:reasons.append('monitored_interval_over_20min')
    if ack_elapsed is not None and ack_elapsed>15:reasons.append('initial_ACK_over_15s')
    return reasons


def sample(session,lock,previous,tick,health_check=None):
    # The frozen sampler still applies every real disk/output/worker guard.
    # Suppress only its elapsed external-gap check; assess that independently.
    result=p.monitor_sample(session,lock,None,tick,health_check or p.native.check_health)
    return result,timing_reasons(0,None if previous is None else tick-previous)


def warning(run,seen,reason,details):
    if reason in seen:return
    p.write(run/('timing-warning-'+reason+'.json'),dict(utc=p.now(),reason=reason,
        details=details,requires_user_confirmation=True,automatic_STOP=False,
        instruction='Keep healthy monitoring running. Ask user before further gameplay. Continue only on their confirmation; STOP on their request or a genuine hard failure.'))
    seen.add(reason)
    print(json.dumps(dict(timing_confirmation_required=reason,automatic_STOP=False)),flush=True)


def monitor(lock,session,run):
    session=p.session_path(lock,session);run=Path(run)
    before=p.read(run/'audit.json')
    if before['mode']!='deployed' or session.name in before['prior_sessions']:
        raise ValueError('not_fresh_deployed_session')
    seen=set();failure=None;ack=False
    try:
        p.write(run/'admission.json',p.admission(lock,session,run))
        a=p.read(run/'operator-confirmation.json')
        if not all(a.get(k) is True for k in ('vortex_profile_confirmed','no_competing_native_instrument','pre_edit_modules_assessed')):
            raise ValueError('operator_confirmation')
        ready=p.read(session/'ready.json');ready_time=(session/'ready.json').stat().st_mtime
        creation=(ready['process_creation_filetime']-116444736000000000)/10000000
        if ready_time-creation>150:
            warning(run,seen,'external_READY_over_150s',dict(seconds=ready_time-creation,basis='process creation to durable READY file; not claimed user click time'))
        if time.time()-ready_time>120:
            warning(run,seen,'admission_over_2min',dict(seconds=time.time()-ready_time))
        nonce=uuid.uuid4().hex;p.native.publish_request(session,nonce)
        start=time.monotonic();previous=None
        hashes={n:p.sha(session/n) for n in ('ready.json','admission.json','patches.json','modules-pre-edit.jsonl')}
        with (run/'monitor.jsonl').open('x',encoding='utf8',newline='\n') as f:
            import os
            while not (session/'STOP').exists():
                tick=time.monotonic();report,reasons=sample(session,lock,previous,tick)
                if any(p.sha(session/n)!=h for n,h in hashes.items()):raise ValueError('startup_receipt_changed')
                for reason in reasons+timing_reasons(tick-start):
                    warning(run,seen,reason,dict(elapsed=tick-start,gap=None if previous is None else tick-previous))
                f.write(json.dumps(dict(utc=p.now(),elapsed=tick-start,gap=None if previous is None else tick-previous,health=report,timing_warnings=sorted(seen)))+'\n')
                f.flush();os.fsync(f.fileno());previous=tick
                if not ack:
                    challenged=p.native.check_health(session,nonce)
                    elapsed=time.monotonic()-start
                    if challenged['pass_check']:
                        for reason in timing_reasons(0,ack_elapsed=elapsed):warning(run,seen,reason,dict(seconds=elapsed))
                        p.write(run/'monitor-ready.json',dict(pass_check=True,utc=p.now(),nonce=nonce,elapsed=elapsed,
                            timing_confirmation_required=sorted(seen),load_permission='Fresh ACK plus user timing confirmations and exact pre-load identity required'))
                        ack=True
                    elif challenged.get('reason')=='nonce_not_acknowledged_once':
                        rows=[json.loads(line) for line in (session/'health.jsonl').read_bytes().splitlines(keepends=True) if line.endswith(b'\n')]
                        if sum(row.get('nonce')==nonce for row in rows)>1:raise ValueError('duplicate_nonce_ACK')
                        if elapsed>15:warning(run,seen,'initial_ACK_pending_over_15s',dict(seconds=elapsed,load_permitted=False))
                    elif challenged.get('reason')=='stale_or_failed_health':
                        # Recheck actual worker health independently. A prompt ACK
                        # can age while this external process is descheduled.
                        latest=p.native.check_health(session)
                        if not latest['pass_check']:raise ValueError('initial_nonce_ACK:'+latest.get('reason','failed'))
                        rows=[json.loads(line) for line in (session/'health.jsonl').read_bytes().splitlines(keepends=True) if line.endswith(b'\n')]
                        matches=[row for row in rows if row.get('nonce')==nonce]
                        if len(matches)!=1:raise ValueError('initial_nonce_ACK_count')
                        row=matches[0]
                        age=(datetime.now(timezone.utc)-datetime.fromisoformat(row['health_utc'].replace('Z','+00:00'))).total_seconds()
                        if age<=15 or row['stopping'] or row['lost'] or row['depth_errors'] or row.get('health_timeouts',0):raise ValueError('initial_nonce_ACK_failed')
                        warning(run,seen,'initial_ACK_aged_during_external_wait',dict(seconds=age,load_permitted=False))
                        nonce=uuid.uuid4().hex;p.native.publish_request(session,nonce)
                    else:raise ValueError('initial_nonce_ACK:'+challenged.get('reason','failed'))
                time.sleep(3)
    except Exception as exc:failure=str(exc)
    finally:
        if not (session/'STOP').exists():p.native.request_stop(session)
    deadline=time.monotonic()+30
    while not (session/'retired.json').exists() and time.monotonic()<deadline:
        if (session/'failure.json').exists():break
        time.sleep(3)
    p.write(run/'monitor-ended.json',dict(utc=p.now(),failure=failure,initial_ACK=ack,
        retired_receipt_present=(session/'retired.json').exists(),timing_warnings=sorted(seen),
        timing_confirmation_status='Review separate user decisions; not inferred from monitor success',
        limits='No in-process unpatch, kill or restart. Complete terminal evidence requires frozen inspector.'))
    return failure is None and ack and (session/'retired.json').exists()


if __name__=='__main__':
    a=argparse.ArgumentParser(description=__doc__)
    a.add_argument('--lock',type=Path,required=True);a.add_argument('--policy',type=Path,required=True);a.add_argument('--policy-sha',required=True)
    a.add_argument('--session',type=Path,required=True);a.add_argument('--run',type=Path,required=True);v=a.parse_args()
    if p.sha(v.policy)!=v.policy_sha:raise ValueError('timing_policy_hash')
    policy=p.read(v.policy)
    if policy['base_lock_sha256']!=BASE_SHA:raise ValueError('base_lock')
    for name,expected in policy['sources'].items():
        if p.sha(p.ROOT/name)!=expected:raise ValueError('timing_source_pin:'+name)
    lock=p.lock_file(v.lock,BASE_SHA);p.pins(lock)
    raise SystemExit(0 if monitor(lock,v.session,v.run) else 2)
