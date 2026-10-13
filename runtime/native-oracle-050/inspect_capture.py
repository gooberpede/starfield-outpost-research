# SPDX-License-Identifier: GPL-3.0-or-later
"""Read sealed schema5 evidence, frozen predictions; write exclusive derivative.
No process access, engine calls, native-result synthesis, or input modification.
Raw records remain authoritative. Pointer samples are not atomic ownership.
"""
import argparse
import json
from pathlib import Path
import struct
import route_inspect as r
from inspect_events import compare, digest, PREDICTION_HASH, ROOT, SIZE, raw

PAIRS={1:(4,5),7:(8,9),10:(11,12),22:(23,24),40:(41,44),42:(43,44),48:(49,44),50:(51,52),53:(54,55)}
CHILD={25:26,27:28,29:30,31:32,33:34,35:36,37:38,45:46}
KNOWN=set(PAIRS)|{v for p in PAIRS.values() for v in p}|set(CHILD)|set(CHILD.values())|{2,3,6,20,39,56}

def analyze(events,module_base=None,synthetic=False):
    predictions=json.loads((ROOT/'docs/experiments/engine-oracle/predictions.json').read_bytes())
    if digest((ROOT/'docs/experiments/engine-oracle/predictions.json').read_bytes())!=PREDICTION_HASH:raise ValueError('frozen_changed')
    groups={};seen=set();defects=[]
    for e in events:
        if not e['sequence']:raise ValueError('zero_sequence')
        if e['sequence'] in seen:raise ValueError('duplicate_sequence')
        seen.add(e['sequence']);groups.setdefault(e['invocation'],[]).append(e)
        if e['kind'] not in KNOWN:defects.append([e['invocation'],'unknown_kind'])
    scopes={}
    for key,es in groups.items():
        es.sort(key=lambda e:e['sequence']);first,last=es[0],es[-1];tag=first['kind']
        identity=all(all(e[k]==first[k] for k in ('parent','thread','reference','context')) for e in es)
        ordered=all(a['qpc']<=b['qpc'] for a,b in zip(es,es[1:]))
        valid=bool(key and identity and ordered)
        if tag in PAIRS:
            valid &= last['kind']==PAIRS[tag][0] and sum(e['kind']==tag for e in es)==1 and sum(e['kind'] in PAIRS[tag] for e in es)==1
            if tag==1:valid &= [e['kind'] for e in es] in ([1,4],[1,2,4],[1,2,6,3,4])
            elif tag==7:valid &= all(e['kind']==20 for e in es[1:-1])
            elif tag in (50,53,22,40,42,48,10):valid &= len(es)==2
        elif tag in CHILD:valid &= len(es)==2 and last['kind']==CHILD[tag]
        else:valid=False
        scopes[key]=dict(kind=tag,normal_complete=bool(valid),parent=first['parent'],thread=first['thread'],first=first['sequence'],last=last['sequence'])
    for key,s in scopes.items():
        if s['kind'] in CHILD and scopes.get(s['parent'],{}).get('kind')!=22:s['normal_complete']=False
        if s['parent']:
            p=scopes.get(s['parent'])
            if not p or not(p['first']<s['first']<s['last']<p['last'] and p['thread']==s['thread']):s['normal_complete']=False
    for _ in scopes:
        for s in scopes.values():
            if s['parent'] in scopes and not scopes[s['parent']]['normal_complete']:s['normal_complete']=False
    generic=r.reconcile(events,module_base)
    travel=[];workshop=[]
    for key,s in scopes.items():
        es=groups[key];first,last=es[0],es[-1]
        if s['kind'] in (50,53):
            block=raw(first,'block',96)
            observed=list(struct.unpack('<12Q',block)) if block else None
            source=raw(first,'source',64 if s['kind']==50 else 0x98)
            travel.append(dict(invocation=key,**s,observed_register_stack_values=observed,
                decision=observed[2] if observed else None,caller_return=observed[0] if observed else None,
                caller_frame=observed[1] if observed else None,source_hex=source.hex() if source else None,
                native_target_reference=first['reference'],native_base_form=struct.unpack_from('<I',raw(first,'base',0x30),0x28)[0] if raw(first,'base',0x30) else None,
                command_8d=source[0x8d] if source and s['kind']==53 else None,
                command_8e=source[0x8e] if source and s['kind']==53 else None,
                asynchronous_identity='UNASSOCIATED: no synthetic thread/time/value join',
                marker_creation='UNKNOWN',ship_movement='OPERATOR_OBSERVATION_REQUIRED'))
        if s['kind']==1:
            grids=[e for e in es if e['kind']==3]
            rows=[]
            for e in grids:
                result=compare(e,predictions)
                pre=[v for v in es if v['kind']==6];centers=[v for v in es if v['kind']==2]
                linked=bool(all(v['status']==0 for v in es) and all(v['blobs']['ref']==first['blobs']['ref'] for v in es if v['kind'] in (2,6,3)) and s['normal_complete'] and len(pre)==len(centers)==len(grids)==1 and all(e['blobs'][n]==pre[0]['blobs'][n] for n in ('input_hierarchy','floor_xy','source','translation','center')) and raw(e,'center',12)==raw(centers[0],'center',12))
                if not linked:result['classification']='PARTIAL_INVOCATION'
                if synthetic:result['classification']='SYNTHETIC_QUALIFICATION_ONLY'
                result['paired']=linked;rows.append(result)
            workshop.append(dict(invocation=key,**s,grid=rows,full_durable_equivalence='NOT TESTED: independently validate saved-to-loaded frame and restoration join'))
    for row in generic['routes']:
        if not scopes.get(row['invocation'],{}).get('normal_complete'):row['scientific_complete']=False
        if synthetic:
            row['scientific_complete']=False
            for grid in row['grid']:grid['classification']='SYNTHETIC_QUALIFICATION_ONLY'
    return dict(schema='sor-050-analysis/1',synthetic=synthetic,scopes=scopes,defects=defects,
        structurally_complete=all(s['normal_complete'] for s in scopes.values()) and not defects,
        deepest_observed='GRID' if any(e['kind'] in (3,34) for e in events) else 'WORKSHOP' if workshop else 'ROUTE' if generic['routes'] else 'TRAVEL_COMMAND' if travel else 'E' if generic['e_invocations'] else 'Q' if generic['q_invocations'] else 'NO_NATIVE_HITS',
        travel=travel,workshop=workshop,generic=generic,native_workshop_equivalence='NOT TESTED',frozen_prediction_sha256=PREDICTION_HASH)

def inspect(session):
    session=Path(session);ready=json.loads((session/'ready.json').read_bytes())
    if (ready.get('component'),ready.get('version'),ready.get('schema'),ready.get('event_size'))!=('SorNativePositionOracle','0.5.0',5,SIZE):raise ValueError('ready_identity')
    events,integrity=r.records(session)
    result=analyze(events,int(ready['module_base'],16),ready.get('synthetic',False));result['integrity']=integrity
    from operate import valid_health_counts,valid_health_transition
    health=[];tail=False
    for line in (session/'health.jsonl').read_bytes().splitlines(keepends=True):
        if not line.endswith(b'\n'):tail=True;break
        h=json.loads(line)
        if not valid_health_counts(h) or h['health_sequence']!=len(health)+1 or not valid_health_transition(health[-1] if health else None,h,ready['qpc_frequency']):raise ValueError('health_integrity')
        if any(h.get(k)!=ready.get(k) for k in ('component','version','schema','pid','process_creation_filetime','dll_sha256','module_base','qpc_frequency')):raise ValueError('health_identity')
        health.append(h)
    retired=json.loads((session/'retired.json').read_bytes()) if (session/'retired.json').exists() else None
    entered=[sum(e['kind']==7 for e in events),sum(e['kind']==10 for e in events),sum(e['kind'] in (1,22,40,42,48,50,53) for e in events)]
    clean=bool(retired and health and not tail and all(retired.get(k)==ready.get(k) for k in ('component','version','schema','pid','process_creation_filetime','dll_sha256','module_base','qpc_frequency')) and retired.get('events')==len(events) and all(retired.get(k)==0 for k in ('lost','health_timeouts','depth_errors')) and retired.get('patches_retained') and retired.get('resident_inert_until_exit'))
    clean &= bool(health and health[-1]['entered']==entered and health[-1]['active']==[0,0,0] and health[-1]['stopping'] and health[-1]['queue_depth']==0 and health[-1]['flushed_events']==len(events))
    clean &= not any((session/n).exists() for n in ('failure.json','not-ready.json')) and not integrity['journal_incomplete_tail'] and not integrity['raw_unjournaled_bytes']
    result['instrumentation_complete']=bool(clean and result['structurally_complete'])
    if not result['instrumentation_complete']:
        for row in result['generic']['routes']:row['scientific_complete']=False
        for row in result['workshop']:
            for grid in row['grid']:grid['classification']='PARTIAL_CAPTURE'
    result['heartbeat_gaps_over_15s']=[(b['qpc']-a['qpc'])/ready['qpc_frequency'] for a,b in zip(health,health[1:]) if b['qpc']-a['qpc']>ready['qpc_frequency']*15]
    result['target_survival']='REQUIRES_POSTFLIGHT';return result

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('session',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    with a.output.open('x',encoding='utf8',newline='\n') as f:json.dump(inspect(a.session),f,indent=2);f.write('\n')
