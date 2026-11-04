# SPDX-License-Identifier: GPL-3.0-or-later
"""Read D5AN fixed counter-fault provenance from an identity-bound closed session.

Reads identity/terminal JSON and the candidate DLL for image/export binding;
optionally writes an exclusive local receipt. Python stdlib; no target/process, save, deployment, database, network or
Git mutation. Old N0/N1 recordings are explicitly legacy, never retrofitted with
producer provenance. A publishing first-fault record is incomplete evidence.
"""
import os
import sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE','0') not in ('','0'):
    raise RuntimeError('Python optimization is forbidden; invoke with -E -B')
import argparse
import hashlib
import json
from pathlib import Path

SCHEMA='sor-d5an-counter/1'
COUNTERS={1:'shared core active (scheduler)',2:'scheduler C++ active',3:'scheduler drops',
    4:'scheduler reentrant',5:'scheduler allocation tokens',6:'scheduler registry faults',
    7:'scheduler identity faults',8:'scheduler ASM active',9:'scheduler registry publication serial',
    10:'scheduler registry retirement serial',11:'scheduler written',31:'other scheduler object',
    32:'causal C++ active',33:'shared core active (causal)',34:'causal drops',
    35:'causal reentrant',36:'causal generation tokens',37:'causal unknown baseline',
    38:'causal multiowner',39:'causal uncertainty',40:'causal written',
    41:'causal registry serial',42:'causal ASM active',63:'other causal object'}
PRODUCERS={1:'scheduler C++ helper',2:'scheduler ASM core admission',3:'scheduler ASM own admission',
    4:'causal C++ helper',5:'causal ASM core admission',6:'causal ASM own admission',
    7:'scheduler registry publication',8:'scheduler registry retirement',9:'scheduler written',
    10:'causal C++ own teardown',11:'causal C++ core teardown',12:'scheduler C++ own teardown',
    13:'scheduler C++ core teardown',14:'scheduler ASM own teardown',15:'scheduler ASM core teardown',
    16:'causal ASM own teardown',17:'causal ASM core teardown',18:'causal written',19:'causal C++ constructor rollback'}
FIELDS=('publication','ids','id','producer','class','value','thread','address','return_va','enabled','scheduler_bits','causal_bits')
PRODUCER_IDS={1:set(range(1,8))|{31},2:{1},3:{8},4:set(range(32,42))|{63},
    5:{33},6:{42},7:{9},8:{10},9:{11},10:{32},11:{33},12:{2},13:{1},14:{8},15:{1},
    16:{42},17:{33},18:{40},19:{32}}

def require(value,message):
    if not value:raise ValueError(message)

def strict(path):
    def pairs(rows):
        value={}
        for key,item in rows:
            require(key not in value,'Duplicate JSON key: '+key);value[key]=item
        return value
    return json.loads(Path(path).read_bytes(),object_pairs_hook=pairs)

def read(session,dll_sha256=None,dll=None):
    session=Path(session);identity_path=session/'identity.json';terminal_path=session/'terminal.json'
    identity=strict(identity_path);terminal=strict(terminal_path)
    require(all(terminal.get(k)==v for k,v in identity.items()),'Terminal/identity mismatch')
    if dll_sha256 is not None:require(identity.get('dll_sha256')==dll_sha256,'Unexpected producer DLL')
    base=dict(schema='sor-d5an-counter-reading/1',identity_sha256=hashlib.sha256(identity_path.read_bytes()).hexdigest(),
        terminal_sha256=hashlib.sha256(terminal_path.read_bytes()).hexdigest(),dll_sha256=identity['dll_sha256'])
    if identity.get('counter_schema')!=SCHEMA:
        require('counter_schema' not in identity,'Unsupported counter schema')
        require('counter_fault_schema' not in terminal,'Unadvertised diagnostic schema')
        return dict(base,disposition='LEGACY_NO_PROVENANCE',complete=False)
    require(terminal.get('counter_fault_schema')==SCHEMA,'Missing or unsupported diagnostic schema')
    require(dll is not None,'Exact candidate DLL path required for D5AN address attribution')
    dll=Path(dll)
    require(hashlib.sha256(dll.read_bytes()).hexdigest()==identity['dll_sha256'],'Actual candidate DLL bytes differ')
    sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'research/resource-retained-population'))
    from d5an_pe import inspect as inspect_pe
    pe=inspect_pe(dll)
    module=identity.get('counter_dll_base');helper=identity.get('counter_helper_rva');leave=identity.get('counter_leave_rva')
    require(all(type(v) is int and v>0 for v in (module,helper,leave)),'Missing observer DLL address domain')
    require(helper==pe['exports'].get('D5AN_counter_next') and leave==pe['exports'].get('D5AN_counter_leave'),'Helper addresses differ from exact candidate exports')
    values={name:terminal.get('counter_fault_'+name) for name in FIELDS}
    require(all(type(v) is int and 0<=v<2**64 for v in values.values()),'Malformed/missing counter diagnostic integer')
    known=sum(1<<key for key in COUNTERS)
    require(not values['ids']&~known,'Unknown counter source bitmap bit')
    sched,causal=values['scheduler_bits'],values['causal_bits']
    require(not (sched|causal)&~7,'Unknown native counter fault bit')
    require(type(terminal.get('scheduler_counter_overflow')) is bool and terminal['scheduler_counter_overflow']==bool(sched&1),'Scheduler saturation aggregate contradiction')
    require(type(terminal.get('scheduler_counter_contention')) is bool and terminal['scheduler_counter_contention']==bool(sched&2),'Scheduler contention aggregate contradiction')
    require(type(terminal.get('causal_native_counter_faults')) is int and terminal['causal_native_counter_faults']==causal,'Causal aggregate contradiction')
    require(not sched or terminal.get('scheduler_failed') is True,'Scheduler native failure omitted')
    require(not causal or terminal.get('causal_failed') is True,'Causal native failure omitted')
    require(not sched or values['ids']&((1<<32)-1),'Scheduler aggregate lacks source bitmap')
    require(not causal or values['ids']&~((1<<32)-1),'Causal aggregate lacks source bitmap')
    p=values['publication'];require(p in (0,1,2),'Invalid fault publication state')
    if p==1:
        require(terminal.get('failed') is True and terminal.get('resident_inert') is True,'Incomplete hard-fault record lacks failed inert terminal')
        return dict(base,disposition='INCOMPLETE_PUBLICATION',complete=False,publication=1,
            ids=values['ids'],note='First writer has not published a complete record; remaining fields are not evidence.')
    if p==0:
        require(all(v==0 for v in values.values()),'Unpublished diagnostic fields are nonzero')
        return dict(base,disposition='NO_COUNTER_FAULT_RECORDED',complete=True,
            note='No counter diagnostic is recorded; this is not proof of complete capture or absence of other failures.')
    require(values['id'] in COUNTERS and values['producer'] in PRODUCERS,'Unknown counter or producer')
    require(values['id'] in PRODUCER_IDS[values['producer']],'Counter/producer contradiction')
    require(values['ids']&(1<<values['id']),'First fault missing from source bitmap')
    require(values['class'] in (1,2),'Unknown fault class')
    require((values['class']==2)==(values['producer'] in set(range(10,18))|{19}),'Fault class/producer contradiction')
    require((sched if values['id']<32 else causal)&(1 if values['class']==1 else 4),'Published fault omitted from native aggregate')
    if values['class']==1:
        require(values['value'] in ((2**64-2,2**64-1) if values['id'] in (9,10) else (2**64-1,)),'Fault saturation value contradiction')
    else:require(values['value']==0,'Fault underflow value contradiction')
    require(values['enabled'] in (0,1),'Invalid enabled context')
    require(values['thread']>0 and values['address']>0 and values['return_va']>0,'Missing exact fault context')
    require(all(module<=values[key]<module+pe['image_bytes'] for key in ('address','return_va')),'Fault address outside exact observer image')
    require(terminal.get('failed') is True and terminal.get('resident_inert') is True,'Hard counter fault lacks failed inert terminal')
    return dict(base,disposition='PUBLISHED_COUNTER_FAULT',complete=True,first=values,
        counter=COUNTERS[values['id']],producer=PRODUCERS[values['producer']],
        observer_dll_base=module,producer_return_rva=values['return_va']-module,
        fault_class='SATURATION' if values['class']==1 else 'TEARDOWN_UNDERFLOW',
        address_domain='Runtime VA in this owned process only; not an RVA, file offset or persisted ID',
        ordering='First successful diagnostic claimant, not proven earliest physical fault across threads')

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('session',type=Path)
    parser.add_argument('--dll-sha256');parser.add_argument('--dll',type=Path);parser.add_argument('--out',type=Path)
    args=parser.parse_args();value=read(args.session,args.dll_sha256,args.dll)
    if args.out:
        root=Path(__file__).resolve().parents[2]/'.local-work/d5an';out=args.out.resolve()
        require(out.is_relative_to(root) and not any(p.is_symlink() or p.is_junction() for p in (out,*out.parents)),'Task-local non-reparse output required')
        from sys import path
        path.insert(0,str(root.parents[1]/'research/resource-retained-population'))
        from d5am_lock_qualify import guard
        guard()
        with out.open('x',encoding='utf8',newline='\n') as stream:json.dump(value,stream,indent=2);stream.write('\n')
    print(json.dumps(value))

if __name__=='__main__':main()
