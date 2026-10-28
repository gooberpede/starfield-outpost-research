# SPDX-License-Identifier: GPL-3.0-or-later
"""Offline D5M exit analysis; no target, debugger or protected-input writes.

Reads a completed capture, qualified dump metadata, existing dump/EXE bytes,
Windows event receipt and pre/post protection receipts. Uses only stdlib and
the owned build hash helper. Writes one fresh ignored forensic summary.
The native capture source closure remains unchanged; this is postflight analysis.
"""
import argparse
from collections import Counter
from datetime import datetime,timezone
import json
from pathlib import Path
import struct
import subprocess
from build import ROOT,LOCAL,pin


def analyze(capture,metadata,windows,preflight,postflight,comparison):
    def read(p):return json.loads(p.read_text(encoding='utf8'))
    events=[json.loads(s) for s in (capture/'events.jsonl').read_text().splitlines()]
    control=[json.loads(s) for s in (capture/'control.jsonl').read_text().splitlines()]
    session=events[0];dump=read(metadata);fault_tid=dump['thread'];fault_va=int(dump['exception_address'],16)
    assert session['kind']=='SESSION' and session['synthetic'] is False
    assert dump['pid']==session['pid'] and dump['module']['base']==session['module_base']
    assert dump['creation_unix_seconds']==session['creation_filetime_100ns']//10000000-11644473600
    assert fault_va-session['module_base']==0x9829b0
    assert [r['sequence'] for r in control]==list(range(1,len(control)+1))
    received=[r for r in control if r['action']=='EVENT_RECEIVED']
    assert [r['debug_event_sequence'] for r in received]==list(range(1,len(received)+1))
    pending=None;pairs=0;errors=[];owned=set();closed=0
    for r in control:
        action=r['action']
        if action=='CONTINUE_INTENT':
            assert pending is None
            pending=tuple(r[k] for k in ('pid','tid','debug_event_sequence','disposition'))
        elif action=='CONTINUE_RESULT':
            assert pending==tuple(r[k] for k in ('pid','tid','debug_event_sequence','disposition'))
            pending=None;pairs+=1
            if not r['ok'] or r['error']:errors.append(r)
        elif action=='DUPLICATE' and r['ok']:
            assert r['owned'] not in owned;owned.add(r['owned'])
        elif action=='EVENT_FILE_OWNED':
            assert r['handle'] not in owned;owned.add(r['handle'])
        elif action=='CLOSE_OWNED' and r['ok']:
            assert r['handle'] in owned;owned.remove(r['handle']);closed+=1
    assert pending is None and pairs==len(received)
    assert not owned and control[-1]['action']=='CONTROL_END'
    assert control[-1]['owned_remaining']==control[-1]['plain_remaining']==0
    exceptions=[r for r in received if r['event']==1]
    fault_exceptions=[r for r in exceptions if r['tid']==fault_tid]
    registrations=[r for r in control if r['action']=='THREAD_REGISTER' and r['tid']==fault_tid]
    barrier=next(r for r in events if r['kind']=='ARM_BARRIER')
    fault_barrier=[r for r in barrier['threads'] if r['tid']==fault_tid]
    grid_traps=[r for r in control if r['action']=='TRAP_CONTEXT' and r['site']==10]
    last_grid=grid_traps[-1];grid_seq=last_grid['debug_event_sequence']
    grid_boundary=[r for r in control if r['debug_event_sequence'] in (grid_seq,grid_seq+1) and r['action'] in
        ('EVENT_RECEIVED','TRAP_CONTEXT','TRAP_BYTE','PATCH_READBACK','SET_CONTROL','STEP_PREPARED','TF_CLEAR_READBACK','STEP_REARMED','CONTINUE_INTENT','CONTINUE_RESULT')]
    assert any(r['action']=='STEP_REARMED' and r['step_site']==-1 for r in grid_boundary)
    assert any(r['action']=='PATCH_READBACK' and r['site']==10 and r['byte']==204 for r in grid_boundary)
    assert any(r['action']=='TF_CLEAR_READBACK' and not r['eflags']&0x100 for r in grid_boundary)
    raw=Path(dump['path']).read_bytes();assert pin(dump['path'])==dump['sha256']
    exe=Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield/Starfield.exe')
    assert pin(exe)==session['image_sha256'];pe=exe.read_bytes();at=struct.unpack_from('<I',pe,0x3c)[0]
    stamp=struct.unpack_from('<I',pe,at+8)[0];size=struct.unpack_from('<I',pe,at+24+56)[0]
    assert dump['module']['timestamp']==stamp and dump['module']['size']==size
    count,directory=struct.unpack_from('<2I',raw,8)
    module_at=next(struct.unpack_from('<3I',raw,directory+i*12)[2] for i in range(count) if struct.unpack_from('<I',raw,directory+i*12)[0]==4)
    versions=[]
    for i in range(struct.unpack_from('<I',raw,module_at)[0]):
        at=module_at+4+i*108
        if struct.unpack_from('<Q',raw,at)[0]==session['module_base']:
            sig,layout,ms,ls=struct.unpack_from('<4I',raw,at+24);assert sig==0xfeef04bd
            versions=[ms>>16,ms&65535,ls>>16,ls&65535]
    assert versions==[1,16,244,0]
    win=read(windows);since=datetime.fromisoformat(win['since_utc'].replace('Z','+00:00'))
    qualified=[r for r in win['events'] if datetime.fromisoformat(r['time_utc'].replace('Z','+00:00'))>=since]
    application=next(r for r in qualified if r['id']==1000)
    import xml.etree.ElementTree as ET
    data=[e.text for e in ET.fromstring(application['xml']).findall('.//{*}EventData/{*}Data')]
    assert int(data[8],16)==session['pid'] and int(data[9],16)==session['creation_filetime_100ns']
    assert int(data[6],16)==int(dump['exception_code'],16) and int(data[7],16)==0x9829b0
    before,after=read(preflight),read(postflight);assert read(comparison)['ok']
    start=read(ROOT/'.local-work/d5m-phase-b/start.json')
    assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==start['head']
    assert pin(ROOT/'.git/index')==start['index_sha256']
    return dict(schema='sor-d5m-exit-analysis/1',method_sha256=pin(__file__),
        inputs={str(p):pin(p) for p in (capture/'events.jsonl',capture/'control.jsonl',metadata,windows,preflight,postflight,comparison)},
        session=session,event_rows=len(events),event_kinds=dict(Counter(r['kind'] for r in events)),
        sample_sites=dict(Counter(r['site'] for r in events if r['kind']=='SAMPLE')),
        control_rows=len(control),debug_events=len(received),continuation_pairs=pairs,continue_errors=errors,
        dispositions=dict(Counter(r['disposition'] for r in control if r['action']=='CONTINUE_RESULT')),
        owned_handle_closes=closed,ownership_replay_empty=not owned,final_control=control[-1],
        fatal_diagnostics=[r for r in control if r['action']=='CONTROLLER_FATAL'],
        recorded_exception_threads=sorted({r['tid'] for r in exceptions}),fault_thread=fault_tid,
        fault_thread_barrier=fault_barrier,fault_thread_registrations=registrations,fault_thread_exception_events=fault_exceptions,
        last_grid_transition=grid_boundary,last_exception=exceptions[-1],
        deferred_traps=sum(r['kind']=='DEFERRED_TRAP' for r in events),
        api_error_rows=[r for r in control if r.get('ok') is False or (r['action']=='PEER_SUSPEND_RESULT' and r['error'])],
        target_exit=next(r for r in events if r['kind']=='EXIT'),controller_exit=read(capture/'controller-exit.json'),
        dump_identity=dict(version=versions,pe_timestamp=stamp,image_size=size,sha256=dump['sha256'],
            fault_va=dump['exception_address'],module_base=hex(session['module_base']),fault_rva=dump['exception_rva'],tf=dump['tf']),
        qualified_windows_events=[dict(id=r['id'],record_id=r['record_id'],time_utc=r['time_utc']) for r in qualified],
        older_windows_records_excluded=len(win['events'])-len(qualified),
        protected_names=len(before['protected_live']),protected_equal=True,head=start['head'],index_sha256=start['index_sha256'],
        plugins=dict(before=next(v for k,v in before['file_guards'].items() if k.lower().endswith('plugins.txt')),
            after=next(v for k,v in after['file_guards'].items() if k.lower().endswith('plugins.txt')),
            content_equal=before['config']==after['config']),
        limits='Complete observed control trail does not establish hidden-thread state, missing-delivery cause or retail construction semantics.')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for n in ('capture','dump-metadata','windows','preflight','postflight','comparison','output'):p.add_argument('--'+n,type=Path,required=True)
    a=p.parse_args();assert a.output.resolve().is_relative_to(LOCAL)
    result=analyze(a.capture,a.dump_metadata,a.windows,a.preflight,a.postflight,a.comparison)
    with a.output.open('x',encoding='utf8',newline='\n') as f:json.dump(result,f,indent=2);f.write('\n')
    print('Forensic continuity/identity/ownership checks PASS:',result['control_rows'],'control rows;',len(result['fault_thread_exception_events']),'fault-thread exception events')
