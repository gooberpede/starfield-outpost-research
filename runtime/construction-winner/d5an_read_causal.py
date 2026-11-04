# SPDX-License-Identifier: GPL-3.0-or-later
# Owned D5AM reader derivative under SOR-P-0002. Bit 4 requires advertised D5AN schema.
"""Authenticate and independently interpret a stopped D5AM causal sidecar.

Reads only supplied session bytes and external DLL hash; optional --out writes a
new derivative. Does not repair raw evidence or operate a process. Stdlib only.
This reader establishes journal integrity and scoped edges, not scheduler joins
or full observer adequacy. Unknown native/lifetime history remains inconclusive.
"""
import os
import sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE','0') not in ('','0'):
    raise RuntimeError('Python optimization is forbidden; invoke with -E -B')
import argparse
import hashlib
import json
from pathlib import Path
import re
import struct
import zlib

NAMES='sequence kind thread ticks lock generation invocation selection source epoch hazards old_state new_state status site'.split()
KINDS='unused register pending acquired recursive reader_registered reader_release writer_release recursive_release exclusive_approach exclusive_return visited_done reset_begin reset_end retire reader_acquired'.split()

def unique(pairs):
    result={}
    for key,value in pairs:
        if key in result:
            raise ValueError('Duplicate JSON key: '+key)
        result[key]=value
    return result


def nonfinite(value):
    raise ValueError('Nonfinite JSON constant: '+value)


def registration_windows(rows,issues):
    """Return conditional, disjoint-boundary witnesses; never total-sort atomics.

    A pending stamp is after its XADD. A provider approach stamp is before the
    helper's pending XADD and CAS. Successful-acquisition stamps occur while
    exclusive ownership is held. These native premises require separately
    qualified bridges/lifetimes; a core miss still identifies the constructor.
    """
    if any(issue in issues for issue in ('MISSING_OR_DUPLICATE_REGISTRATION','UNKNOWN_INITIAL_HOLDERS')):
        return []
    contexts={}
    for row in rows:
        key=(row['thread'],row['invocation'],row['selection'],row['source'])
        contexts.setdefault(key,[]).append(row)
    calls=[]
    for key,parts in contexts.items():
        approach=None;pending=None
        for row in parts:
            if row['kind']==9:
                approach=row;pending=None
            elif row['kind']==2:
                pending=row
            elif row['kind']==3 and pending is not None:
                calls.append(dict(key=key,approach=approach,pending=pending,acquired=row))
                approach=None;pending=None
    witnesses=[]
    for earlier in calls:
        for later in calls:
            b,a=earlier['acquired'],later['acquired']
            if a['thread']==b['thread'] or not b['ticks']<a['ticks']:
                continue
            rule='OVERLAPPING_INTERVALS_UNKNOWN'
            boundaries=[]
            used=[r for call in (earlier,later) for r in (call['approach'],call['pending'],call['acquired']) if r]
            first=min(r['ticks'] for r in used);last=max(r['ticks'] for r in used)
            invalidators=[r for r in rows if r['kind'] in (12,13,14) and first<=r['ticks']<=last]
            if any(r['status'] or r['hazards'] for r in used) or invalidators:
                rule='RELEVANT_LIFECYCLE_OR_CONTEXT_UNCERTAINTY'
            elif later['approach'] and b['ticks']<later['approach']['ticks']:
                rule='EARLIER_ACQUISITION_BEFORE_OTHER_HELPER_ENTRY'
                boundaries=[b['sequence'],later['approach']['sequence']]
            elif earlier['approach'] and later['pending']['ticks']<earlier['approach']['ticks']:
                rule='PRIOR_PENDING_WRITER_OVERTAKEN'
                boundaries=[later['pending']['sequence'],earlier['approach']['sequence'],b['sequence']]
            witnesses.append(dict(earlier_acquisition=b['sequence'],later_acquisition=a['sequence'],
                                  interpretation=rule,disjoint_callback_boundaries=boundaries,
                                  basis='CONDITIONAL_NATIVE_INTERVALS',
                                  limit='No winner/miss or upstream eligibility claim without qualified core/task/source joins; added probes can alter this order.'))
    return witnesses

def read(session,dll_hash):
    if not isinstance(dll_hash,str) or not re.fullmatch('[0-9a-f]{64}',dll_hash):
        raise ValueError('Exact lowercase external DLL SHA-256 required')
    session=Path(session)
    identity_raw=(session/'identity.json').read_bytes()
    identity=json.loads(identity_raw,object_pairs_hook=unique,parse_constant=nonfinite)
    if not isinstance(identity,dict) or identity.get('dll_sha256')!=dll_hash:
        raise ValueError('External candidate DLL identity mismatch')
    if identity.get('causal_schema')!='sor-d5am-causal/1':
        raise ValueError('Identity does not declare this causal schema')
    raw=(session/'causal.bin').read_bytes()
    if len(raw)<96:
        raise ValueError('Truncated causal header')
    magic,version,size,reserved=struct.unpack_from('<4Q',raw)
    if (magic,version,size,reserved)!=(0x31434c4d41354453,1,128,0):
        raise ValueError('Causal header/schema mismatch')
    if raw[32:96]!=hashlib.sha256(identity_raw).hexdigest().encode('ascii'):
        raise ValueError('Causal identity binding mismatch')
    if (len(raw)-96)%136:
        raise ValueError('Truncated causal frame')
    events=[]
    for offset in range(96,len(raw),136):
        length,crc=struct.unpack_from('<II',raw,offset)
        payload=raw[offset+8:offset+136]
        if length!=128 or zlib.crc32(payload)!=crc:
            raise ValueError('Causal frame length/CRC mismatch')
        row=dict(zip(NAMES,struct.unpack_from('<15Q',payload)))
        row['request']=list(struct.unpack_from('<2i',payload,120))
        if row['sequence']!=len(events)+1 or not 1<=row['kind']<len(KINDS):
            raise ValueError('Causal sequence/kind mismatch')
        if row['status']&~15:
            raise ValueError('Unknown causal status bits')
        if not row['lock'] or not row['thread'] or (not row['generation'] and
                (not row['status']&8 or row['kind'] not in (2,3,4,5,6,7,8,15))):
            raise ValueError('Causal identity field unavailable')
        old,new,kind=row['old_state'],row['new_state'],row['kind']
        delta={2:0x1000,3:0x400000,4:0x400000,5:1,6:-1,7:-0x401000,8:-0x400000}.get(kind)
        if delta is not None and (old>0xffffffff or new!=((old+delta)&0xffffffff)):
            raise ValueError('Contradictory recorded atomic operands')
        if kind==3 and old&0xffc00fff:
            raise ValueError('Acquisition violates pinned native CAS predicate')
        if kind==3 and not old&0x3ff000:
            raise ValueError('Acquisition lacks a pending writer count')
        if kind==4 and not old&0xffc00000:
            raise ValueError('Recursive acquisition without prior exclusive depth')
        if kind==6 and not old&0xfff:
            raise ValueError('Reader release without an old reader count')
        if kind==7 and old&0xffc00000!=0x400000:
            raise ValueError('Final writer release violates depth predicate')
        if kind==8 and old&0xffc00000<0x800000:
            raise ValueError('Recursive release incorrectly marks final depth')
        if kind==1 and (old>0xffffffff or new>0xffffffff):
            raise ValueError('Initial state/owner exceeds native width')
        events.append(row)
    terminal_path=session/'terminal.json'
    terminal=json.loads(terminal_path.read_bytes(),object_pairs_hook=unique,parse_constant=nonfinite) if terminal_path.exists() else None
    reasons=[]
    bridge_schema=identity.get('causal_bridge_admission_schema')
    if bridge_schema not in (None,'sor-d5am-causal-bridge/1'):
        raise ValueError('Unknown native causal bridge admission schema')
    bridge_declared=bridge_schema is not None
    def bridge_metrics(value,terminal=False):
        active,faults=value.get('causal_bridge_active'),value.get('causal_native_counter_faults')
        if type(active) is not int or not 0<=active<2**64 or type(faults) is not int or faults&~(7 if identity.get('counter_schema')=='sor-d5an-counter/1' else 3) or faults<0:
            raise ValueError('Missing or malformed native causal bridge accounting')
        if terminal and active:
            raise ValueError('Terminal retains admitted native causal bridges')
        if faults and value.get('causal_failed') is not True:
            raise ValueError('Native causal counter failure omitted from recorder failure')
        return faults
    terminal_bridge_faults=None
    if terminal is None:
        reasons.append('NO_TERMINAL_ACCOUNTING')
    else:
        if not isinstance(terminal,dict) or any(terminal.get(k)!=v for k,v in identity.items()):
            raise ValueError('Terminal full session/producer identity mismatch')
        counters=('causal_written','causal_enqueued','causal_active','causal_drops',
                  'causal_reentrant','causal_baseline_unknown','causal_multiowner','causal_uncertain')
        if any(type(terminal.get(k)) is not int or not 0<=terminal[k]<2**64 for k in counters):
            raise ValueError('Missing or invalid causal accounting')
        if type(terminal.get('causal_failed')) is not bool or type(terminal.get('failed')) is not bool:
            raise ValueError('Missing or invalid failure accounting')
        if 'causal_counter_overflow' in terminal and type(terminal['causal_counter_overflow']) is not bool:
            raise ValueError('Malformed causal overflow accounting')
        if terminal.get('causal_written')!=len(events) or terminal.get('causal_enqueued')!=len(events) or terminal.get('causal_active')!=0:
            raise ValueError('Terminal causal accounting mismatch')
        if terminal.get('causal_drops') or terminal.get('causal_reentrant') or terminal.get('causal_failed'):
            reasons.append('RECORDER_LOSS_OR_FAILURE')
        if terminal.get('causal_baseline_unknown') or terminal.get('causal_multiowner'):
            reasons.append('UNKNOWN_BASELINE_OR_MULTIOWNER')
        if terminal['causal_uncertain']:
            reasons.append('REGISTRY_GENERATION_UNCERTAINTY')
        if terminal['causal_uncertain']<sum(bool(row['status']&8) for row in events):
            raise ValueError('Registry uncertainty accounting contradicts recorded events')
        if terminal['failed'] or terminal.get('output_faults')!=0 or terminal.get('output_fault')!='none':
            reasons.append('CORE_OUTPUT_FAILURE')
        if terminal.get('causal_counter_overflow') is True or terminal.get('counter_overflow') is True:
            reasons.append('COUNTER_OVERFLOW')
        if terminal.get('resident_inert') is not True:
            reasons.append('NOT_OWNED_INERT_STOP')
        if bridge_declared:
            terminal_bridge_faults=bridge_metrics(terminal,True)
    acknowledgments=[]
    flush_path=session/'flush.jsonl'
    if not flush_path.exists():
        reasons.append('NO_CORE_ACK_BINDING')
    else:
        previous=0;previous_telemetry=None;previous_bridge_faults=0
        for line in flush_path.read_bytes().splitlines(keepends=True):
            if not line.endswith(b'\n'):
                raise ValueError('Torn core ACK while binding causal accounting')
            ack=json.loads(line,object_pairs_hook=unique,parse_constant=nonfinite)
            if not isinstance(ack,dict) or ack.get('identity_sha256')!=hashlib.sha256(identity_raw).hexdigest():
                raise ValueError('ACK full identity hash mismatch')
            value=ack.get('causal_written')
            if type(value) is not int or not previous<=value<=len(events):
                raise ValueError('ACK causal prefix count invalid')
            monotonic=('causal_written','causal_enqueued','causal_drops','causal_reentrant',
                       'causal_baseline_unknown','causal_multiowner','causal_uncertain')
            if any(type(ack.get(k)) is not int or not 0<=ack[k]<2**64 for k in monotonic):
                raise ValueError('Missing or invalid ACK causal telemetry')
            if ack['causal_written']>ack['causal_enqueued'] or type(ack.get('causal_failed')) is not bool:
                raise ValueError('ACK causal accounting contradiction')
            if previous_telemetry and (any(ack[k]<previous_telemetry[k] for k in monotonic) or
                                       previous_telemetry['causal_failed'] and not ack['causal_failed']):
                raise ValueError('ACK causal loss/counter history regressed')
            if bridge_declared:
                faults=bridge_metrics(ack)
                if faults&previous_bridge_faults!=previous_bridge_faults:
                    raise ValueError('ACK native causal counter fault history regressed')
                previous_bridge_faults=faults
            previous=value
            previous_telemetry=ack
            acknowledgments.append(value)
        if not acknowledgments:
            reasons.append('NO_CORE_ACK_BINDING')
        if terminal is not None and previous_telemetry and (any(terminal[k]<previous_telemetry[k] for k in monotonic) or
                                                           previous_telemetry['causal_failed'] and not terminal['causal_failed']):
            raise ValueError('Terminal erases ACK causal loss/counter history')
        if bridge_declared and terminal_bridge_faults is not None and terminal_bridge_faults&previous_bridge_faults!=previous_bridge_faults:
            raise ValueError('Terminal erases native causal counter fault history')
    groups={}
    for row in events:
        groups.setdefault((row['lock'],row['generation']),[]).append(row)
    histories=[]
    for (lock,generation),rows in groups.items():
        registrations=[r for r in rows if r['kind']==1]
        issues=[]
        if len(registrations)!=1:
            issues.append('MISSING_OR_DUPLICATE_REGISTRATION')
        elif registrations[0]['status']:
            issues.append('UNKNOWN_INITIAL_HOLDERS')
        if any(r['status'] for r in rows):
            issues.append('REPORTED_UNCERTAINTY')
        # Timestamps are callback stamps after transitions. Cross-thread sequence
        # order is never used as the native atomic transition order.
        pending={};acquisitions=[];prior_by_thread={}
        for row in rows:
            previous=prior_by_thread.get(row['thread'])
            if previous is not None and row['ticks']<previous:
                issues.append('SAME_THREAD_CALLBACK_CLOCK_REVERSED')
            prior_by_thread[row['thread']]=row['ticks']
            if row['kind']==2:
                pending.setdefault(row['thread'],[]).append(row)
            elif row['kind']==3:
                candidates=pending.get(row['thread'],[])
                if not candidates:
                    issues.append('ACQUISITION_WITHOUT_RECORDED_PENDING')
                    matched=[]
                else:
                    matched=[candidates.pop(0)]
                    keys=('invocation','selection','source','request')
                    if any(matched[0][k]!=row[k] for k in keys):
                        issues.append('PENDING_ACQUISITION_CONTEXT_MISMATCH')
                acquisitions.append(dict(thread=row['thread'],invocation=row['invocation'],
                                         selection=row['selection'],source=row['source'],request=row['request'],
                                         acquired_event=row['sequence'],pending_events=[r['sequence'] for r in matched]))
        if any(pending.values()):
            issues.append('UNRESOLVED_PENDING_WRITER')
        histories.append(dict(lock=lock,generation=generation,events=len(rows),issues=sorted(set(issues)),acquisitions=acquisitions,
                              registration_witnesses=registration_windows(rows,issues)))
    return dict(schema='sor-d5am-causal-read/1',raw_sha256=hashlib.sha256(raw).hexdigest(),
                identity_sha256=hashlib.sha256(identity_raw).hexdigest(),dll_sha256=dll_hash,
                events=events,histories=histories,integrity='AUTHENTICATED_FRAMES',
                causal_completeness='INCONCLUSIVE',reasons=sorted(set(reasons)),
                native_bridge_admission_declared=bridge_declared,
                native_bridge_accounting_complete=bool(bridge_declared and terminal_bridge_faults==0 and acknowledgments and
                    terminal is not None and not any(reason not in ('UNKNOWN_BASELINE_OR_MULTIOWNER','REGISTRY_GENERATION_UNCERTAINTY') for reason in reasons)),
                sidecar_accounting_complete=bool(terminal is not None and not any(reason not in (
                    'UNKNOWN_BASELINE_OR_MULTIOWNER','REGISTRY_GENERATION_UNCERTAINTY') for reason in reasons)),
                coverage_refusals=[reason for reason in reasons if reason in (
                    'UNKNOWN_BASELINE_OR_MULTIOWNER','REGISTRY_GENERATION_UNCERTAINTY')],
                acknowledgment_counts=acknowledgments,
                warning='CRC and identity bindings validate framing, not source provenance, native coverage, core completeness or semantics.',
                limit='No scheduler task joins or assertion of complete ordinary shared-release-site census. Probe timing can change arbitration; callback sequence is not atomic transition order.')

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('session',type=Path)
    p.add_argument('--dll-sha256',required=True);p.add_argument('--out',type=Path);args=p.parse_args()
    result=read(args.session,args.dll_sha256)
    encoded=json.dumps(result,indent=2)+'\n'
    if args.out:
        root=Path(__file__).resolve().parents[2]
        target=args.out.absolute()
        if not target.resolve().is_relative_to(root/'.local-work/d5an') or any(p.is_symlink() or p.is_junction() for p in (target,*target.parents)):
            raise ValueError('Output must be a new non-reparse D5AM-local derivative')
        import ctypes
        for drive in ('C:/','D:/'):
            available=ctypes.c_ulonglong()
            if not ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(drive),ctypes.byref(available),None,None) or available.value<40_000_000_000:
                raise RuntimeError('Both caller-available disk floors must hold before output')
        with args.out.open('x',encoding='utf8',newline='\n') as f:
            f.write(encoded)
    print(json.dumps(dict(integrity=result['integrity'],events=len(result['events']),causal_completeness=result['causal_completeness'])))

if __name__=='__main__':
    main()
