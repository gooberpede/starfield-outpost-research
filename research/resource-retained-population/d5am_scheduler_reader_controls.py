# SPDX-License-Identifier: GPL-3.0-or-later
"""Independently encode scheduler wire fixtures and challenge reader refusals.

Reads the owned new scheduler reader. Writes only synthetic session files and
an exclusive qualification receipt in a fresh D5AM-local directory. Uses Python
stdlib, with no native/game/database/save/deployment/network/Git action. These
are parser and explicit uncertainty controls, not scheduler-producer, ABI, actual
claim-order, full task-coverage or retail prediction validation.
"""
import os
import sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE','') not in ('','0'):
    raise RuntimeError('Python optimization is forbidden; invoke with -E -B')

import hashlib
import importlib.util
import json
from pathlib import Path
import re
import struct
import subprocess
import zlib
from d5ad_baseline import guard,sha

ROOT=Path(__file__).resolve().parents[2]
READER=ROOT/'runtime/construction-winner/d5am_read_scheduler.py'
DLL='b'*64
NAMES='sequence kind thread ticks node allocation family server rank serial dependencies registered state_flags pool mode status core_invocation core_selection source claim_context route epoch hazards extra'.split()


def require(value,message):
    if not value:
        raise ValueError(message)


def event(sequence,kind,**changes):
    e=dict(zip(NAMES,[0]*24))
    e.update(sequence=sequence,kind=kind,thread=101,ticks=sequence*10,node=0x1000,
             allocation=1,family=1,server=0x2000,rank=7,serial=17,dependencies=3,
             registered=1,state_flags=2,pool=0x3000,mode=2,core_invocation=9,
             core_selection=10,source=0x4000,claim_context=0x5000,route=0x0101,
             epoch=4,extra=99,request=[-8,11],native_key=[1,2,3],
             discriminator=[4,5,6],queue=[7,8,9,10,11,12])
    e.update(changes)
    return e


def main():
    require(len(sys.argv) in (2,3) and re.fullmatch('[a-z0-9-]+',sys.argv[1]),'Fresh bounded label and optional component directory required')
    out=ROOT/'.local-work/d5am'/sys.argv[1]
    require(not any(p.is_symlink() or p.is_junction() for p in (out,*out.parents)),'Reparse output path')
    before=guard();out.mkdir(parents=True,exist_ok=False)
    spec=importlib.util.spec_from_file_location('d5am_scheduler_under_test',READER)
    reader=importlib.util.module_from_spec(spec);spec.loader.exec_module(reader)
    reader_pin=sha(READER)
    ident=dict(schema='sor-d5x/4',retail=False,scheduler_schema='sor-d5am-scheduler/1',
               scheduler_bridge_admission_schema='sor-d5am-scheduler-bridge/1',
               scheduler_dispatch_argument_schema='r8-low-byte/1',scheduler_ready_serial_schema='consumed-r9/1',
               dll_sha256=DLL,nonce='d'*64,pid=1,creation_filetime=2,qpc_frequency=10_000_000)
    positive=[event(1,1),event(2,7),event(3,9),event(4,8)]
    checks=[]

    def fixture(name,rows=None,raw_change=None,terminal_change=None,ack_change=None,no_terminal=False,identity_change=None):
        folder=out/name;folder.mkdir();rows=positive if rows is None else rows
        observed=dict(ident);observed.update(identity_change or {})
        identity=(json.dumps(observed,separators=(',',':'))+'\n').encode()
        digest=hashlib.sha256(identity).hexdigest()
        raw=struct.pack('<4Q',0x314843534d413544,1,272,0)+digest.encode()
        for e in rows:
            payload=struct.pack('<24Q2i6I6Q',*(e[k] for k in NAMES),*e['request'],*e['native_key'],*e['discriminator'],*e['queue'])
            raw+=struct.pack('<II',272,zlib.crc32(payload))+payload
        terminal=dict(observed,scheduler_written=len(rows),scheduler_enqueued=len(rows),scheduler_active=0,
                      scheduler_bridge_active=0,scheduler_counter_overflow=False,scheduler_counter_contention=False,
                      scheduler_drops=0,scheduler_reentrant=0,scheduler_registry_faults=0,
                      scheduler_identity_faults=0,scheduler_failed=False,failed=False,
                      output_faults=0,output_fault='none',resident_inert=True)
        if terminal_change:
            terminal_change(terminal)
        ack={k:v for k,v in terminal.items() if k.startswith('scheduler_') and k not in ('scheduler_schema','scheduler_sites')}
        ack['identity_sha256']=digest
        if ack_change:
            ack_change(ack)
        (folder/'identity.json').write_bytes(identity)
        (folder/'scheduler.bin').write_bytes(raw_change(raw) if raw_change else raw)
        (folder/'flush.jsonl').write_text(json.dumps(ack)+'\n',encoding='utf8',newline='\n')
        if not no_terminal:
            (folder/'terminal.json').write_text(json.dumps(terminal),encoding='utf8',newline='\n')
        return folder

    result=reader.read(fixture('positive'),DLL)
    require(result['events']==positive and result['byte_accounting_complete'],'All independent wire fields differ')
    require(result['task_completeness']=='INCONCLUSIVE' and not result['histories'][0]['issues'],'Parser invented complete task coverage')
    require(result['native_bridge_accounting_complete'],'Declared native scheduler accounting omitted')
    checks.append('all-independent-wire-fields-and-no-native-promotion')

    def refuse(name,**kwargs):
        folder=fixture(name,**kwargs)
        try:
            reader.read(folder,DLL)
        except (ValueError,KeyError,TypeError):
            checks.append(name)
        else:
            raise ValueError('Adverse scheduler input accepted: '+name)
    refuse('partial-header',raw_change=lambda raw:raw[:95])
    refuse('partial-frame',raw_change=lambda raw:raw[:-1])
    refuse('wrong-header',raw_change=lambda raw:bytes([raw[0]^1])+raw[1:])
    refuse('wrong-identity-binding',raw_change=lambda raw:raw[:32]+b'0'*64+raw[96:])
    refuse('payload-crc',raw_change=lambda raw:raw[:110]+bytes([raw[110]^1])+raw[111:])
    refuse('unknown-kind',rows=[event(1,13)])
    refuse('sequence-gap',rows=[event(1,1),event(3,9)])
    refuse('zero-thread',rows=[event(1,1,thread=0)])
    refuse('other-session-terminal',terminal_change=lambda t:t.update(nonce='e'*64))
    refuse('missing-counter',terminal_change=lambda t:t.pop('scheduler_drops'))
    refuse('bool-counter',terminal_change=lambda t:t.update(scheduler_drops=False))
    refuse('wrong-written',terminal_change=lambda t:t.update(scheduler_written=3))
    refuse('active-terminal',terminal_change=lambda t:t.update(scheduler_active=1))
    refuse('native-bridge-active-terminal',terminal_change=lambda t:t.update(scheduler_bridge_active=1))
    refuse('malformed-counter-flag',terminal_change=lambda t:t.update(scheduler_counter_overflow=1))
    refuse('other-ack-identity',ack_change=lambda a:a.update(identity_sha256='0'*64))
    refuse('ack-exceeds-file',ack_change=lambda a:a.update(scheduler_written=5,scheduler_enqueued=5))
    refuse('terminal-erases-ack-loss',ack_change=lambda a:a.update(scheduler_drops=1))
    refuse('unknown-native-feature',identity_change=dict(scheduler_bridge_admission_schema='unknown'))
    refuse('unknown-dispatch-operand-feature',identity_change=dict(scheduler_dispatch_argument_schema='unknown'))
    refuse('unknown-ready-operand-feature',identity_change=dict(scheduler_ready_serial_schema='unknown'))
    refuse('dispatch-operand-outside-byte',rows=[event(1,1),event(2,3,extra=256)])
    routed=reader.read(fixture('actual-dispatch-operand-distinct-from-node-mode',rows=[event(1,1),event(2,3,extra=171,mode=2)]),DLL)
    require(routed['events'][1]['extra']==171 and routed['events'][1]['mode']==2,'Native dispatch operand conflated with node storage')
    checks.append('actual-dispatch-operand-distinct-from-node-mode')
    ready=reader.read(fixture('consumed-ready-serial-full-native-domain',rows=[event(1,1),event(2,5,serial=0,extra=2**64-1)]),DLL)
    require(ready['events'][1]['extra']==2**64-1 and ready['events'][1]['serial']==0 and ready['byte_accounting_complete'],
            'Consumed engine serial confused with old node serial or observer counter')
    checks.append('consumed-ready-serial-full-native-domain')
    for field in ('scheduler_bridge_active','scheduler_counter_overflow','scheduler_counter_contention'):
        refuse('missing-native-terminal-'+field,terminal_change=lambda t,field=field:t.pop(field))
        refuse('missing-native-ack-'+field,ack_change=lambda a,field=field:a.pop(field))
    refuse('native-fault-without-recorder-failure',terminal_change=lambda t:t.update(scheduler_counter_overflow=True))
    refuse('terminal-erases-native-overflow',ack_change=lambda a:a.update(scheduler_counter_overflow=True,scheduler_failed=True),
           terminal_change=lambda t:t.update(scheduler_failed=True))
    folder=fixture('ack-erases-native-contention',terminal_change=lambda t:t.update(scheduler_counter_overflow=True,scheduler_counter_contention=True,scheduler_failed=True))
    final=json.loads((folder/'flush.jsonl').read_bytes());first=dict(final,scheduler_counter_overflow=False);second=dict(final,scheduler_counter_contention=False)
    (folder/'flush.jsonl').write_text(json.dumps(first)+'\n'+json.dumps(second)+'\n',encoding='utf8',newline='\n')
    try:
        reader.read(folder,DLL)
    except ValueError:
        checks.append('ack-erases-native-contention')
    else:
        raise ValueError('Native scheduler fault history regressed')
    legacy=reader.read(fixture('earlier-no-native-feature',identity_change=dict(scheduler_bridge_admission_schema=None)),DLL)
    require(legacy['byte_accounting_complete'] and not legacy['native_bridge_accounting_complete'],'Old journal promoted to native admission proof')
    checks.append('earlier-byte-valid-without-native-admission-proof')
    native_fault=reader.read(fixture('declared-native-fault',terminal_change=lambda t:t.update(scheduler_counter_contention=True,scheduler_failed=True)),DLL)
    require(not native_fault['byte_accounting_complete'] and not native_fault['native_bridge_accounting_complete'],'Native fault promoted')
    checks.append('declared-native-fault')
    for name,change in (('declared-loss',dict(scheduler_drops=1)),('declared-failure',dict(scheduler_failed=True)),
                        ('core-output-failure',dict(output_fault='fixture',output_faults=1)),
                        ('counter-overflow',dict(counter_overflow=True)),('not-inert',dict(resident_inert=False))):
        result=reader.read(fixture(name,terminal_change=lambda t,change=change:t.update(change)),DLL)
        require(not result['byte_accounting_complete'],name)
        checks.append(name)
    result=reader.read(fixture('registry-uncertainty',terminal_change=lambda t:t.update(scheduler_registry_faults=1)),DLL)
    require(result['byte_accounting_complete'] and result['coverage_refusals'],'Science uncertainty incorrectly equated with byte failure')
    checks.append('registry-uncertainty-separate-from-byte-integrity')
    result=reader.read(fixture('no-terminal',no_terminal=True),DLL)
    require(not result['byte_accounting_complete'] and 'NO_TERMINAL_ACCOUNTING' in result['reasons'],'No terminal promoted')
    checks.append('no-terminal')
    for name,rows,issue in (
        ('missing-publication',[event(1,9)],'MISSING_OR_DUPLICATE_TYPED_PUBLICATION'),
        ('duplicate-publication',[event(1,1),event(2,1)],'MISSING_OR_DUPLICATE_TYPED_PUBLICATION'),
        ('allocation-collision',[event(1,1),event(2,1,node=0x2000)],'ALLOCATION_ID_COLLIDES_ACROSS_NODES'),
        ('reported-node-aba',[event(1,1),event(2,9,status=4)],'REPORTED_TASK_UNCERTAINTY'),
        ('changed-family',[event(1,1),event(2,9,family=2)],'RECORDED_TASK_IDENTITY_CHANGED'),
        ('changed-native-key',[event(1,1),event(2,9,native_key=[1,2,4])],'RECORDED_TASK_IDENTITY_CHANGED'),
        ('changed-task-request',[event(1,1),event(2,9,request=[-9,11])],'RECORDED_TASK_IDENTITY_CHANGED'),
        ('changed-discriminator',[event(1,1),event(2,9,discriminator=[4,5,7])],'RECORDED_TASK_IDENTITY_CHANGED'),
        ('unknown-family',[event(1,1,family=0)],'INVALID_TYPED_FAMILY')):
        result=reader.read(fixture(name,rows=rows),DLL)
        require(any(issue in h['issues'] for h in result['histories']),name)
        checks.append(name)
    for entry in (READER,Path(__file__)):
        for flags,env in ((['-E','-B','-O'],None),(['-E','-B','-OO'],None),(['-E','-B'],dict(os.environ,PYTHONOPTIMIZE='1'))):
            p=subprocess.run([sys.executable,*flags,str(entry),'--help'],env=env,capture_output=True)
            require(p.returncode and b'optimization' in p.stderr.lower(),'Optimization not refused')
            checks.append(entry.name+':'+('inherited-env' if env else flags[-1]))
    require(sha(READER)==reader_pin,'Reader changed during controls')
    component=None
    if len(sys.argv)==3:
        folder=Path(sys.argv[2]).resolve()
        require(folder.is_relative_to(ROOT/'.local-work/d5am'),'D5AM-local retained component required')
        source=json.loads((folder/'qualification.json').read_bytes())
        require(source['state']=='PASS','Component did not pass its own contract')
        dll=folder/'SorConstructionWinner-0.9.0-D5AM-scheduler-component.dll'
        require(sha(dll)==source['dll_sha256'],'Compiled component identity mismatch')
        captures={}
        for path in sorted(folder.glob('*.bin')):
            raw=path.read_bytes()
            require(len(raw)>=96 and (len(raw)-96)%280==0,'Component derivative shape')
            require(struct.unpack_from('<4Q',raw)==(0x314843534d413544,1,272,0),'Component derivative header')
            require(raw[32:96]==source['synthetic_identity'].encode(),'Synthetic identity label changed')
            rows=[]
            for offset in range(96,len(raw),280):
                length,crc=struct.unpack_from('<II',raw,offset);payload=raw[offset+8:offset+280]
                require(length==272 and zlib.crc32(payload)==crc,'Component derivative CRC')
                values=struct.unpack('<24Q2i6I6Q',payload)
                row=dict(zip(NAMES,values[:24]));row.update(request=list(values[24:26]),native_key=list(values[26:29]),discriminator=list(values[29:32]),queue=list(values[32:38]))
                require(1<=row['kind']<=12 and (not rows or rows[-1]['sequence']+1==row['sequence']),'Component derivative order')
                rows.append(row)
            captures[path.stem]=dict(sha256=sha(path),records=len(rows),
                                     sequence_origin=rows[0]['sequence']-1 if rows else None,
                                     kinds=[row['kind'] for row in rows],
                                     statuses=[row['status'] for row in rows],
                                     provider_allocations=[row['allocation'] for row in rows if row['kind']==9])
        require(captures['publication-before-synchronous-work']['kinds']==[1,2,3,7,9,8],'Native typed publication/dispatch scope changed')
        require(captures['density-layer-nested-provider-join']['provider_allocations']==[1,2,1],'Native nested provider scope changed')
        require(any(status&4 for status in captures['native-paused-producer-aba']['statuses']),'Actual paused native producer lacks ABA refusal')
        component=dict(qualification_sha256=sha(folder/'qualification.json'),dll_sha256=source['dll_sha256'],captures=captures,
                       scope='Independent decode of re-encoded compiled-component queue events. Synthetic header and truncated prefixes are not an authenticated production spool, flush or session identity.')
        checks.extend(['component-all-wire-fields-CRC-and-order','component-publication-before-dispatch',
                       'component-nested-provider-identity-restoration','component-native-paused-producer-ABA-refused'])
    receipt=dict(schema='sor-d5am-scheduler-reader-controls/1',result='PASS',checks=checks,component_replay=component,
                 reader_sha256=reader_pin,method_sha256=sha(__file__),initial_free=before,final_free=guard(),
                 scope='Independent synthetic wire/refusal controls only; no producer/native/task-coverage/retail qualification.')
    with (out/'qualification.json').open('x',encoding='utf8',newline='\n') as stream:
        json.dump(receipt,stream,indent=2);stream.write('\n')
    print(json.dumps(dict(result='PASS',checks=len(checks),out=str(out))))


if __name__=='__main__':
    main()
