# SPDX-License-Identifier: GPL-3.0-or-later
"""Independently validate the stopped D5AM scheduler journal and identity joins.

Reads immutable supplied session bytes and an externally pinned DLL identity;
optionally writes a new D5AM-local derivative. Stdlib only. No pointer traversal,
repair, process, deployment, save, database, network or Git action. Registry and
task uncertainty is separate from byte integrity; pre/post callback stamps do
not establish the exact native claim CAS or normal retail scheduling frequency.
"""
import os
import sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE','') not in ('','0'):
    raise RuntimeError('Python optimization is forbidden; invoke with -E -B')

import argparse
import hashlib
import json
from pathlib import Path
import re
import struct
import zlib

NAMES='sequence kind thread ticks node allocation family server rank serial dependencies registered state_flags pool mode status core_invocation core_selection source claim_context route epoch hazards extra'.split()
KINDS='unused published activated dispatch retire ready_tree_before dependency_decrement callback_begin callback_end provider claim_return queue_before queue_return'.split()
COUNTERS='scheduler_written scheduler_enqueued scheduler_active scheduler_drops scheduler_reentrant scheduler_registry_faults scheduler_identity_faults'.split()
MONOTONIC=[k for k in COUNTERS if k!='scheduler_active']


def unique(pairs):
    result={}
    for key,value in pairs:
        if key in result:
            raise ValueError('Duplicate JSON key: '+key)
        result[key]=value
    return result


def nonfinite(value):
    raise ValueError('Nonfinite JSON constant: '+value)


def read(session,dll):
    if not isinstance(dll,str) or not re.fullmatch('[0-9a-f]{64}',dll):
        raise ValueError('Exact lowercase external DLL SHA-256 required')
    session=Path(session)
    identity_raw=(session/'identity.json').read_bytes()
    identity=json.loads(identity_raw,object_pairs_hook=unique,parse_constant=nonfinite)
    identity_hash=hashlib.sha256(identity_raw).hexdigest()
    if not isinstance(identity,dict) or identity.get('dll_sha256')!=dll or identity.get('scheduler_schema')!='sor-d5am-scheduler/1':
        raise ValueError('Scheduler producer/schema identity mismatch')
    bridge_schema=identity.get('scheduler_bridge_admission_schema')
    if bridge_schema not in (None,'sor-d5am-scheduler-bridge/1'):
        raise ValueError('Unknown scheduler native admission schema')
    bridge_declared=bridge_schema is not None
    fault_flags=('scheduler_counter_overflow','scheduler_counter_contention')
    for field,expected in (('scheduler_dispatch_argument_schema','r8-low-byte/1'),
                           ('scheduler_ready_serial_schema','consumed-r9/1')):
        if identity.get(field) not in (None,expected):
            raise ValueError('Unknown scheduler native operand schema: '+field)
    raw=(session/'scheduler.bin').read_bytes()
    if len(raw)<96 or struct.unpack_from('<4Q',raw)!=(0x314843534d413544,1,272,0):
        raise ValueError('Scheduler header/schema mismatch')
    if raw[32:96]!=identity_hash.encode('ascii') or (len(raw)-96)%280:
        raise ValueError('Scheduler identity binding or frame alignment mismatch')
    events=[]
    for offset in range(96,len(raw),280):
        length,crc=struct.unpack_from('<II',raw,offset)
        payload=raw[offset+8:offset+280]
        if length!=272 or zlib.crc32(payload)!=crc:
            raise ValueError('Scheduler payload length/CRC mismatch')
        values=struct.unpack('<24Q2i6I6Q',payload)
        row=dict(zip(NAMES,values[:24]))
        row.update(request=list(values[24:26]),native_key=list(values[26:29]),
                   discriminator=list(values[29:32]),queue=list(values[32:38]))
        if row['sequence']!=len(events)+1 or not 1<=row['kind']<len(KINDS) or not row['thread']:
            raise ValueError('Scheduler sequence/kind/thread mismatch')
        if row['kind']==3 and identity.get('scheduler_dispatch_argument_schema') and row['extra']>255:
            raise ValueError('Dispatch argument exceeds its native byte domain')
        events.append(row)
    reasons=[];coverage=[]
    terminal_path=session/'terminal.json'
    terminal=json.loads(terminal_path.read_bytes(),object_pairs_hook=unique,parse_constant=nonfinite) if terminal_path.exists() else None

    def metrics(value):
        if any(type(value.get(k)) is not int or not 0<=value[k]<2**64 for k in COUNTERS):
            raise ValueError('Missing or invalid scheduler counter')
        if type(value.get('scheduler_failed')) is not bool or value['scheduler_written']>value['scheduler_enqueued']:
            raise ValueError('Scheduler failure/accounting mismatch')
        for flag in fault_flags:
            if (bridge_declared or flag in value) and type(value.get(flag)) is not bool:
                raise ValueError('Malformed scheduler counter fault')
        if (bridge_declared or 'scheduler_bridge_active' in value) and (type(value.get('scheduler_bridge_active')) is not int or not 0<=value['scheduler_bridge_active']<2**64):
            raise ValueError('Malformed scheduler bridge admission count')
        if any(value.get(flag) is True for flag in fault_flags) and not value['scheduler_failed']:
            raise ValueError('Native scheduler fault omitted from recorder failure')

    if terminal is None:
        reasons.append('NO_TERMINAL_ACCOUNTING')
    else:
        if not isinstance(terminal,dict) or any(terminal.get(k)!=v for k,v in identity.items()):
            raise ValueError('Terminal full identity mismatch')
        metrics(terminal)
        if terminal['scheduler_written']!=len(events) or terminal['scheduler_enqueued']!=len(events) or terminal['scheduler_active']:
            raise ValueError('Terminal scheduler count mismatch')
        if terminal.get('scheduler_bridge_active',0):
            raise ValueError('Terminal has an admitted native scheduler bridge')
        if terminal['scheduler_drops'] or terminal['scheduler_reentrant'] or terminal['scheduler_failed']:
            reasons.append('SCHEDULER_RECORDER_LOSS_OR_FAILURE')
        if terminal.get('failed') is not False or terminal.get('output_faults')!=0 or terminal.get('output_fault')!='none':
            reasons.append('CORE_OUTPUT_FAILURE')
        if terminal.get('counter_overflow') is True:
            reasons.append('COUNTER_OVERFLOW')
        if terminal.get('scheduler_counter_overflow') is True or terminal.get('scheduler_counter_contention') is True:
            reasons.append('SCHEDULER_COUNTER_FAULT')
        if terminal.get('resident_inert') is not True:
            reasons.append('NOT_OWNED_INERT_STOP')
        if terminal['scheduler_registry_faults'] or terminal['scheduler_identity_faults']:
            coverage.append('TASK_REGISTRY_OR_IDENTITY_UNCERTAINTY')
    flush=session/'flush.jsonl';previous=None;acks=[]
    if not flush.exists():
        reasons.append('NO_CORE_ACK_BINDING')
    else:
        for line in flush.read_bytes().splitlines(keepends=True):
            if not line.endswith(b'\n'):
                raise ValueError('Torn scheduler-bound ACK')
            ack=json.loads(line,object_pairs_hook=unique,parse_constant=nonfinite)
            if not isinstance(ack,dict) or ack.get('identity_sha256')!=identity_hash:
                raise ValueError('ACK scheduler identity mismatch')
            metrics(ack)
            if ack['scheduler_written']>len(events):
                raise ValueError('ACK exceeds scheduler sidecar')
            if previous and (any(ack[k]<previous[k] for k in MONOTONIC) or previous['scheduler_failed'] and not ack['scheduler_failed']):
                raise ValueError('Scheduler ACK counters/failure regressed')
            if previous and any(previous.get(flag) is True and ack.get(flag) is not True for flag in fault_flags):
                raise ValueError('Scheduler ACK native fault history regressed')
            previous=ack;acks.append(ack['scheduler_written'])
        if not acks:
            reasons.append('NO_CORE_ACK_BINDING')
        if terminal is not None and previous and (any(terminal[k]<previous[k] for k in MONOTONIC) or previous['scheduler_failed'] and not terminal['scheduler_failed']):
            raise ValueError('Terminal erased scheduler ACK history')
        if terminal is not None and previous and any(previous.get(flag) is True and terminal.get(flag) is not True for flag in fault_flags):
            raise ValueError('Terminal erased scheduler native fault history')
    groups={};allocation_nodes={}
    for e in events:
        if e['allocation']:
            groups.setdefault((e['node'],e['allocation']),[]).append(e)
            allocation_nodes.setdefault(e['allocation'],set()).add(e['node'])
    histories=[]
    for (node,allocation),rows in groups.items():
        births=[e for e in rows if e['kind']==1]
        issues=[]
        if len(births)!=1 or not node:
            issues.append('MISSING_OR_DUPLICATE_TYPED_PUBLICATION')
        if len(allocation_nodes[allocation])!=1:
            issues.append('ALLOCATION_ID_COLLIDES_ACROSS_NODES')
        if any(e['status'] for e in rows):
            issues.append('REPORTED_TASK_UNCERTAINTY')
        clean=[e for e in rows if not e['status']]
        if any(e['family'] not in (1,2) for e in clean):
            issues.append('INVALID_TYPED_FAMILY')
        if len({(e['family'],tuple(e['native_key']),tuple(e['request']),tuple(e['discriminator'])) for e in clean})>1:
            issues.append('RECORDED_TASK_IDENTITY_CHANGED')
        provider=[dict(sequence=e['sequence'],core_invocation=e['core_invocation'],
                       core_selection=e['core_selection'],thread=e['thread'],request=e['request'],status=e['status'])
                  for e in rows if e['kind']==9]
        histories.append(dict(node=node,allocation=allocation,records=len(rows),issues=issues,provider_joins=provider))
    return dict(schema='sor-d5am-scheduler-read/1',identity_sha256=identity_hash,
                raw_sha256=hashlib.sha256(raw).hexdigest(),dll_sha256=dll,events=events,histories=histories,
                byte_accounting_complete=bool(terminal is not None and not reasons),reasons=reasons,
                native_bridge_admission_declared=bridge_declared,
                native_bridge_accounting_complete=bool(bridge_declared and terminal is not None and not reasons),
                coverage_refusals=coverage,acknowledgment_counts=acks,task_completeness='INCONCLUSIVE',
                limit='Direct copied fields and typed-node associations only; claim return and ready-tree-before callbacks are bounds, not exact CAS/serial-publication times. Native site/ABI/caller coverage, core/provider joins and scoped lifecycle proof require separate qualification.')


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('session',type=Path);p.add_argument('--dll-sha256',required=True);p.add_argument('--out',type=Path)
    args=p.parse_args();result=read(args.session,args.dll_sha256)
    if args.out:
        target=args.out.absolute();root=Path(__file__).resolve().parents[2]
        if not target.resolve().is_relative_to(root/'.local-work/d5am') or any(x.is_symlink() or x.is_junction() for x in (target,*target.parents)):
            raise ValueError('Fresh non-reparse D5AM-local output required')
        import ctypes
        for drive in ('C:/','D:/'):
            free=ctypes.c_ulonglong()
            if not ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(drive),ctypes.byref(free),None,None) or free.value<40_000_000_000:
                raise RuntimeError('Both caller-available disk floors must hold')
        with target.open('x',encoding='utf8',newline='\n') as stream:
            json.dump(result,stream,indent=2);stream.write('\n')
    print(json.dumps(dict(events=len(result['events']),byte_accounting_complete=result['byte_accounting_complete'],task_completeness=result['task_completeness'])))


if __name__=='__main__':
    main()
