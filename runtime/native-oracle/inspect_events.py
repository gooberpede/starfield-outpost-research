# SPDX-License-Identifier: GPL-3.0-or-later
"""Offline, read-only native evidence validation and comparisons.
Reads events/journal/ready/frozen predictions; writes exclusive new JSON only.
Never contacts a process, modifies originals or tunes frozen expectations.
No complete saved-to-current-frame validation is automated by this inspector.
"""
import argparse
import hashlib
import json
from pathlib import Path
import struct
import sys

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'save-analysis/scripts'))
from durable_position_v2 import offset
HEADER=struct.Struct('<11Q');BLOB=struct.Struct('<QII1024s')
NAMES='ref base extra cell world context_raw source candidate translation landscape center input_hierarchy floor_xy result block merge scale'.split()
SIZE=HEADER.size+len(NAMES)*BLOB.size
PREDICTION_HASH='a8a7402697ed866a3410d4bd58796de513c7ca11f89e770a80deb5a8651a0487'
def digest(b):return hashlib.sha256(b).hexdigest()
def decode(data):
    if len(data)!=SIZE:raise ValueError('event_size')
    out=dict(zip('sequence invocation parent qpc reference context thread kind status mxcsr last_error'.split(),HEADER.unpack_from(data)))
    out['blobs']={}
    for i,name in enumerate(NAMES):
        address,length,ok,raw=BLOB.unpack_from(data,HEADER.size+i*BLOB.size)
        if length>1024 or ok not in (0,1):raise ValueError('blob_schema')
        out['blobs'][name]=dict(address=address,length=length,ok=bool(ok),hex=raw[:length].hex() if ok else None)
    return out
def raw(event,name,n=0):
    b=event['blobs'][name]
    return bytes.fromhex(b['hex']) if b['ok'] and b['length']>=n else None
def hierarchy(b):
    if b is None:return None
    return [b[0],struct.unpack_from('<i',b,4)[0]*192+struct.unpack_from('<i',b,0x14)[0]*12+struct.unpack_from('<i',b,0x24)[0],struct.unpack_from('<i',b,8)[0]*192+struct.unpack_from('<i',b,0x18)[0]*12+struct.unpack_from('<i',b,0x28)[0]]
def compare(e,predictions):
    out=dict(invocation=e['invocation'],classification='UNASSESSED',native_center_hex=None,native_hierarchy=None,saved_frame_comparison='UNASSESSED_REQUIRES_INDEPENDENT_FRAME_JOIN')
    b=raw(e,'base',0x30);w=raw(e,'extra',0xa0);land=raw(e,'landscape',0x58);center=raw(e,'center',12)
    out['native_center_hex']=None if center is None else center.hex()
    out['native_hierarchy']=hierarchy(raw(e,'result',44))
    if b is None or w is None or land is None or center is None or e['status']:
        out['reason']='partial_or_racy_identity';return out
    workshop=w[0x98:0xa0].hex();body=f'{struct.unpack_from("<I",land,0x54)[0]:08X}'
    base=struct.unpack_from('<I',b,0x28)[0]
    candidates=[p for p in predictions if p['identity']['workshop_id']==workshop and p['body']==body]
    out.update(workshop_id=workshop,body=body,ordinary_base=base==0x2c60e9,frozen_candidates=[p['source']['sample'] for p in candidates])
    if base!=0x2c60e9 or not candidates:out['reason']='unqualified_identity';return out
    out['center_bytes_equal']=[center.hex()==p['center_hex'] for p in candidates]
    # Native-input replay checks actual center+translation -> floor and hierarchy;
    # translated XY remains DERIVED, never relabelled as a captured register.
    tr=raw(e,'translation',12);xy=raw(e,'floor_xy',8);src=raw(e,'input_hierarchy',44);result=raw(e,'result',44)
    block=raw(e,'block',4);merge=raw(e,'merge',4);scale=raw(e,'scale',4)
    if None in (tr,xy,src,result,block,merge,scale):out['reason']='missing_grid_inputs';return out
    if struct.unpack_from('<I',land,0x50)[0]!=256 or (struct.unpack('<I',block)[0]+struct.unpack('<I',merge)[0])&0xffffffff!=12 or scale.hex()!='0ad7233c':
        out['reason']='unsupported_native_grid_parameters';return out
    if e['mxcsr']&0x6000:out['reason']='non_nearest_rounding';return out
    import math
    f32=lambda v:struct.unpack('<f',struct.pack('<f',v))[0]
    c=struct.unpack('<3f',center);t=struct.unpack('<3f',tr);s=struct.unpack('<f',scale)[0]
    if any(not math.isfinite(v) for v in (*c,*t)):out['reason']='nonfinite';return out
    if any(0<abs(v)<2**-126 for v in (*c,*t)):out['reason']='subnormal_input_unqualified';return out
    try:translated=[f32(c[i]+t[i]) for i in range(2)]
    except OverflowError:out['reason']='binary32_overflow';return out
    if any(not math.isfinite(v) for v in translated):out['reason']='nonfinite';return out
    if any(0<abs(v)<2**-126/s for v in translated):out['reason']='subnormal_scale_unqualified';return out
    try:expected_floor=[math.floor(f32(v*s)) for v in translated]
    except (OverflowError,ValueError):out['reason']='binary32_scale_overflow';return out
    if any(not -2**31<=i<2**31 for i in expected_floor):out['reason']='floor_out_of_range';return out
    native_floor=list(struct.unpack('<2i',xy));native_source=hierarchy(src)
    try:expected_grid=list(offset(*native_source,*native_floor))
    except ValueError:out['reason']='unsupported_source_hierarchy';return out
    out.update(classification='CONDITIONAL_NATIVE_INPUT_REPLAY',derived_translated_xy_hex=struct.pack('<2f',*translated).hex(),native_floor=native_floor,derived_floor=expected_floor,
        floor_equal=native_floor==expected_floor,native_source=native_source,derived_grid=expected_grid,grid_equal=out['native_hierarchy']==expected_grid)
    return out
def inspect(session):
    ready=json.loads((session/'ready.json').read_text())
    if ready.get('component')!='SorNativePositionOracle' or ready.get('version')!='0.1.0' or ready.get('event_size')!=SIZE:raise ValueError('ready_schema')
    frozen=(ROOT/'docs/experiments/engine-oracle/predictions.json').read_bytes()
    if digest(frozen)!=PREDICTION_HASH:raise ValueError('frozen_prediction_hash')
    predictions=json.loads(frozen);events=[];truncated=False;offset_bytes=0
    with (session/'events.bin').open('rb') as binary:
        for line in (session/'records.jsonl').read_bytes().splitlines(keepends=True):
            if not line.endswith(b'\n'):truncated=True;break
            row=json.loads(line)
            if row['offset']!=offset_bytes or row['length']!=SIZE:raise ValueError('journal_extent')
            data=binary.read(SIZE)
            if digest(data)!=row['sha256']:raise ValueError('raw_hash')
            e=decode(data)
            if any(row[k]!=e[k] for k in ('sequence','invocation','kind')):raise ValueError('journal_event_identity')
            events.append(e);offset_bytes+=SIZE
        orphans=len(binary.read())
    groups={};sequences=set()
    for e in events:
        if e['sequence'] in sequences:raise ValueError('duplicate_sequence')
        sequences.add(e['sequence']);groups.setdefault(e['invocation'],[]).append(e)
    rows=[]
    for key,items in groups.items():
        begins=[e for e in items if e['kind']==1];ends=[e for e in items if e['kind'] in (4,5)]
        paired=len(begins)==len(ends)==1 and ends[0]['kind']==4 and begins[0]['thread']==ends[0]['thread'] and begins[0]['reference']==ends[0]['reference'] and begins[0]['context']==ends[0]['context']
        for e in items:
            if e['kind']!=3:continue
            same=[v for v in items if v['kind']==2 and v['sequence']<e['sequence'] and v['thread']==e['thread'] and v['reference']==e['reference'] and v['context']==e['context'] and raw(v,'center',12)==raw(e,'center',12)]
            pre=[v for v in items if v['kind']==6 and v['sequence']<e['sequence'] and all(v[k]==e[k] for k in ('reference','context','thread')) and all(v['blobs'][k]==e['blobs'][k] for k in ('input_hierarchy','floor_xy','source','translation','center'))]
            paired=paired and bool(begins) and bool(ends) and begins[0]['sequence']<e['sequence']<ends[0]['sequence'] and all(begins[0][k]==e[k] for k in ('reference','context','thread'))
            r=compare(e,predictions)
            r['paired']=paired;r['native_center_event_count']=len(same)
            r['native_grid_begin_count']=len(pre)
            order= len(same)==len(pre)==1 and bool(begins) and bool(ends) and begins[0]['sequence']<same[0]['sequence']<pre[0]['sequence']<e['sequence']<ends[0]['sequence']
            if not paired or not order or len(items)!=5 or any(v['parent']!=e['parent'] for v in items):r['classification']='PARTIAL_INVOCATION';r['paired']=False
            if ready.get('synthetic'):r['classification']='SYNTHETIC_QUALIFICATION_ONLY'
            rows.append(r)
    return dict(schema='sor-native-oracle-analysis/1',provenance=ready,events=len(events),invocations=len(groups),truncated_journal=truncated,unreferenced_tail_bytes=orphans,
        comparisons=rows,scientific_result='NO_FULL_EQUIVALENCE_CLAIM',raw_events=events)
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('session',type=Path);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
    from build import guard
    guard();report=inspect(a.session)
    with a.output.open('x',encoding='utf8',newline='\n') as f:json.dump(report,f,indent=2);f.write('\n')
if __name__=='__main__':main()
