# SPDX-License-Identifier: GPL-3.0-or-later
"""Offline schema-3 Q path reconstruction. No process access or original writes.
Uses authenticated records/health from inspect_events; private field samples
remain samples. Only an exclusive derived JSON output is written by the CLI.
"""
import argparse
import json
from pathlib import Path
import struct
from inspect_events import inspect, raw

ORDER = [(0,1),(4,4),(8,4),(0x10,1),(0xc,4),(0x14,4),
         (0x18,4),(0x20,1),(0x1c,4),(0x24,4),(0x28,4)]

def mismatch(a,b):
    if a is None or b is None or len(a)!=44 or len(b)!=44:
        raise ValueError('hierarchy_read_missing')
    return next((hex(o) for o,n in ORDER if a[o:o+n]!=b[o:o+n]),None)

def value(e):
    b=raw(e,'result',8)
    if b is None:raise ValueError('helper_return_missing')
    return struct.unpack_from('<Q',b)[0]

def args(e):
    b=raw(e,'input_hierarchy',32)
    if b is None:raise ValueError('helper_arguments_missing')
    return struct.unpack_from('<4Q',b)

def copied(e,name,address,n):
    b=e['blobs'][name]
    if b['address']!=address or raw(e,name,n) is None:
        raise ValueError('output_address_or_read_'+name)

def path(items,healthy):
    """Fail closed; caller supplies integrity/health result, not absence guesses."""
    out=dict(invocation=items[0]['invocation'],classification='UNQUALIFIED',
             ordered_stages=[e['kind'] for e in items],reason=None,
             shared_fields='SAMPLES_NOT_ATOMIC_BRANCH_OPERANDS',
             rectangle_result='NOT_RECONSTRUCTED_SHARED_RECTANGLE_RACE',
             native_equivalence='NOT_TESTED')
    try:
        if not healthy:raise ValueError('capture_incomplete_or_unhealthy')
        first,last=items[0],items[-1]
        if first['kind']!=7 or last['kind']!=8:raise ValueError('normal_Q_pair_missing')
        if any(any(e[k]!=first[k] for k in ('invocation','thread','parent','reference','context')) for e in items):raise ValueError('ancestry_mismatch')
        if any(a['sequence']>=b['sequence'] or a['qpc']>b['qpc'] for a,b in zip(items,items[1:])):raise ValueError('order_mismatch')
        result=raw(last,'result',4);start_latch=raw(first,'center',1);end_latch=raw(last,'center',1)
        if result is None or start_latch is None or end_latch is None:raise ValueError('Q_return_or_latch_missing')
        if struct.unpack('<I',result[:4])[0]!=int(end_latch[0]!=0):raise ValueError('Q_return_latch_contradiction')
        stages=iter(items[1:-1]);current=next(stages,None)
        def take(k):
            nonlocal current
            if current is None or current['kind']!=k:raise ValueError('missing_or_unexpected_stage_'+str(k))
            e=current;current=next(stages,None);return e
        resolver=take(13);early=None;resolved=value(resolver)
        if args(resolver)[2]!=first['context']:raise ValueError('resolver_candidate_argument')
        context=raw(first,'context_raw',40)
        if context is None:raise ValueError('Q_context_missing')
        owner_slot,latch_slot,world,rect,angular_source=struct.unpack_from('<5Q',context)
        if args(resolver)[0]!=world:raise ValueError('resolver_world_argument')
        if value(resolver)==0:
            fallback=take(14)
            if args(fallback)[0]!=args(resolver)[1]:raise ValueError('fallback_key_argument')
            resolved=value(fallback)
            if value(fallback)==0:early='FALLBACK_NULL'
            else:
                copied(fallback,'ref',resolved,0x30)
                form=raw(fallback,'ref',0x30)
                if form is None:raise ValueError('fallback_type_missing')
                if form[0x2e]!=0x56:early='FALLBACK_TYPE_NOT_56'
        if early is None:
            overlay=take(15)
            if args(overlay)[1]!=resolved:raise ValueError('overlay_resolved_argument')
            if args(overlay)[0]!=owner_slot:raise ValueError('overlay_owner_slot_argument')
            if value(overlay)==0:early='OVERLAY_NULL'
            elif current is None:early='LANDSCAPE_NULL_STATIC_PATH'
            else:
                a=take(16);b=take(17)
                if args(a)[2]!=first['context']:raise ValueError('A_candidate_argument')
                if args(a)[0]!=args(b)[0]:raise ValueError('landscape_argument_contradiction')
                packed=raw(b,'floor_xy',8)
                out['packed_key_sample_disagreement']=None if packed is None else struct.unpack_from('<Q',packed)[0]!=args(b)[2]
                copied(b,'candidate',args(a)[1],44);copied(b,'source',args(b)[1],44)
                offset=mismatch(raw(b,'candidate',44),raw(b,'source',44))
                entered=current is not None and current['kind']==20
                if offset is not None:
                    if entered:raise ValueError('E_contradicts_hierarchy_mismatch')
                    early='HIERARCHY_MISMATCH_AT_'+offset
                elif entered:take(20);early='E_ENTERED'
                else:early='OVERLAY_BIT0_CLEAR_STATIC_PATH'
                sample=raw(b,'extra',0x34)
                if sample is not None:
                    out['sampled_overlay_bit0']=bool(sample[0x20]&1)
                    if offset is None:out['sample_path_disagreement']=bool(sample[0x20]&1)!=entered
                if current is not None:
                    angular=take(18);delta=take(19)
                    if args(angular)[2]!=angular_source:raise ValueError('angular_source_argument')
                    if args(angular)[0]!=args(a)[0] or args(delta)[0]!=args(a)[0]:raise ValueError('final_landscape_argument')
                    copied(angular,'center',args(angular)[2],24)
                    copied(delta,'translation',args(delta)[1],8)
                    copied(delta,'source',args(delta)[2],44);copied(delta,'candidate',args(delta)[3],44)
                    if raw(delta,'translation',8) is None:raise ValueError('final_delta_missing')
                    out['final_delta']=list(struct.unpack('<2i',raw(delta,'translation',8)))
                    out['final_geometry']='REACHED_DELTA_SHARED_RECTANGLE_SAMPLE_ONLY'
                else:
                    if end_latch[0]!=0:raise ValueError('missing_final_geometry_nonzero_latch')
                    out['final_geometry']='LATCH_ZERO_STATIC_PATH'
        if early in ('FALLBACK_NULL','FALLBACK_TYPE_NOT_56','OVERLAY_NULL','LANDSCAPE_NULL_STATIC_PATH') and start_latch!=end_latch:
            raise ValueError('early_return_latch_changed')
        if current is not None:raise ValueError('unexpected_trailing_stage')
        out.update(classification='SCOPED_PATH_RECONSTRUCTION',reason=early,
                   evidence_basis='HELPER_COMPLETIONS_AND_PINNED_STATIC_CFG')
    except (ValueError,KeyError,TypeError,struct.error) as exc:out['reason']=str(exc)
    return out

def analyze(report):
    groups={}
    for e in report['raw_events']:groups.setdefault(e['invocation'],[]).append(e)
    healthy=report['diagnostics']['worker_evidence_qualified'] and not report['truncated_journal'] and not report['unreferenced_tail_bytes']
    rows=[path(items,healthy) for items in groups.values() if items[0]['kind']==7]
    if report['provenance'].get('synthetic'):
        for row in rows:row['qualification_only']=True
    return dict(schema='sor-q-branch-analysis/3',rows=rows,
                native_equivalence='NOT_TESTED',limits='No branch instruction tracing; shared operands are samples. No general enumeration absence or guaranteed full-oracle trigger.')

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('session',type=Path);ap.add_argument('--output',required=True,type=Path);a=ap.parse_args()
    from build import guard
    guard();report=analyze(inspect(a.session))
    with a.output.open('x',encoding='utf8',newline='\n') as f:json.dump(report,f,indent=2);f.write('\n')
if __name__=='__main__':main()
