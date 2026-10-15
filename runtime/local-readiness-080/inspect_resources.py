# SPDX-License-Identifier: GPL-3.0-or-later
"""Read-only streaming WAL decoder; optional exclusive JSON report. No target
access or writes to evidence. Stdlib only. Partial tails and missing identities
remain explicit; resource correspondence is never proof of asynchronous ancestry.
"""
import argparse
import hashlib
import json
from pathlib import Path
import struct

SIZE = 3328
NAMES = ('sequence','invocation','parent','thread','qpc','site','kind','phase',
         'reference','command','result','status')
BLOBS = ('ref','base','extra','cell','world','operand','aux','output')

def decode(raw):
    if len(raw)!=SIZE:raise ValueError('record_size')
    e=dict(zip(NAMES,struct.unpack_from('<12Q',raw)))
    e['args']=list(struct.unpack_from('<4Q',raw,96))
    for i,name in enumerate(BLOBS):
        off=128+i*400
        address,length,ok=struct.unpack_from('<QII',raw,off)
        if length>384 or ok not in (0,1):raise ValueError('blob_bounds')
        e[name]=dict(address=address,length=length,ok=bool(ok),bytes=raw[off+16:off+16+length].hex())
    return e

def field(blob,offset,fmt):
    if not blob['ok'] or offset+struct.calcsize(fmt)>blob['length']:return None
    return struct.unpack_from(fmt,bytes.fromhex(blob['bytes']),offset)[0]

def records(root):
    offset=0;seq=0
    with (root/'events.bin').open('rb') as raw,(root/'records.jsonl').open('rb') as wal:
        for line in wal:
            if not line.endswith(b'\n'):raise ValueError('partial_journal_tail')
            r=json.loads(line)
            if r['sequence']!=seq+1 or r['offset']!=offset or r['length']!=SIZE:raise ValueError('wal_order_or_length')
            b=raw.read(SIZE)
            if len(b)!=SIZE or hashlib.sha256(b).hexdigest()!=r['sha256']:raise ValueError('raw_integrity')
            e=decode(b)
            if e['sequence']!=r['sequence']:raise ValueError('record_sequence')
            yield e
            offset+=SIZE;seq+=1
        if raw.read(1):raise ValueError('unjournaled_raw_tail')

def resource(e):
    ptr=e['reference']
    b=e['output'] if e['kind']==109 else e['base']
    return dict(pointer=ptr,form_id=field(b,0x28,'<I') if ptr else None,
                form_type=field(b,0x2e,'<B') if ptr else None,
                status='NULL' if not ptr else 'READ_OK' if b['ok'] else 'UNKNOWN_ID')


def population_signature(populations):
    """Ordered, source-preserving pointer/identity signature; None is unknown."""
    signature=[]
    for p in populations:
        if not p or p['status'] or len(p['members'])!=(p['end']-p['begin'])//8:
            return None
        if any(m['status'] not in ('READ_OK','NULL') for m in p['members']):
            return None
        signature.append(tuple((m['pointer'],m['form_id'],m['form_type'],m['status']) for m in p['members']))
    return tuple(signature)

def inspect(root):
    root=Path(root);inv={};pops={};final_rows={};errors=[];count=0
    try:
        for e in records(root):
            count+=1;key=(e['invocation'],e['phase'],e['args'][0])
            if e['kind']==108:
                pops[key]=dict(begin=e['args'][1],end=e['args'][2],status=e['status'],members=[])
            elif e['kind']==109:
                if key not in pops:raise ValueError('member_without_header')
                pop=pops[key]
                if e['args'][3]!=len(pop['members']):raise ValueError('member_order')
                pop['members'].append(resource(e));pop['status']|=e['status']
            elif e['kind']==110:
                final_rows.setdefault(e['invocation'],[]).append(dict(index=e['args'][3],address=e['operand']['address'],ok=e['operand']['ok']))
            elif e['kind'] in (*range(101,108),111,112):
                entry=inv.setdefault(e['invocation'],dict(kind=e['kind'],parent=e['parent'],thread=e['thread'],site=e['site']))
                if (entry['kind'],entry['parent'],entry['thread'],entry['site'])!=(e['kind'],e['parent'],e['thread'],e['site']):raise ValueError('invocation_identity')
                if e['phase']==1:
                    if 'before' in entry:raise ValueError('duplicate_entry')
                    entry['before']=e
                elif e['phase'] in (2,3):
                    if 'after' in entry or 'before' not in entry:raise ValueError('unpaired_return')
                    entry['after']=e
                else:raise ValueError('invalid_phase')
            else:raise ValueError('unknown_event_kind')
    except (OSError,ValueError,KeyError,TypeError,json.JSONDecodeError) as ex:
        errors.append(str(ex))
    evaluations=[];updates=[];operations=[]
    for ident,v in inv.items():
        before=v.get('before');after=v.get('after')
        if not before or not after:errors.append('incomplete_invocation:'+str(ident))
        if v['parent']:
            ancestor=inv.get(v['parent'])
            if not ancestor or ancestor['thread']!=v['thread']:
                errors.append('missing_or_cross_thread_parent:'+str(ident))
        if v['kind'] in (111,112):
            operations.append(dict(invocation=ident,kind=v['kind'],parent=v['parent'],thread=v['thread'],site=v['site'],
                before=before,after=after,measurement='SOURCE_VISIT' if v['kind']==111 else 'PROVIDER_BOUNDARY',
                geometry_decisions='UNQUALIFIED',cache_hit_miss='NOT_OBSERVED',freshness='UNKNOWN'))
        if v['kind']==101:
            position=before['ref'] if before else dict(ok=False,length=0,bytes='')
            indexed=None
            if position['ok'] and position['length']==24:
                x,y,z,frame,domain=struct.unpack('<fffIQ',bytes.fromhex(position['bytes']))
                indexed=dict(xyz=[x,y,z],frame_index=frame,domain_pointer=domain,
                             provenance='EVALUATION_ARGUMENT_SNAPSHOT',atomic=False)
            populations=[pops.get((ident,2,i)) for i in range(3)]
            prior_populations=[pops.get((ident,1,i)) for i in range(3)]
            complete=bool(before and after and after['phase']==2 and indexed and not before['status'] and not after['status'])
            for p in populations:
                complete=complete and p is not None and p['status']==0 and len(p['members'])==(p['end']-p['begin'])//8
            evaluations.append(dict(invocation=ident,site=v['site'],position=indexed,
                preview_reference=before['command'] if before else None,
                preview_base_form_id=field(before['output'],0x28,'<I') if before else None,
                indexed_domain_form_id=field(before['operand'],0x28,'<I') if before else None,
                indexed_domain_type=field(before['operand'],0x2e,'<B') if before else None,
                radius_bits=before['args'][2] if before else None,
                upper_coordinate_bits=before['args'][3] if before else None,
                query_state_before=before['base'] if before else None,
                query_state_after=after['base'] if after else None,
                interval=[before['qpc'] if before else None,after['qpc'] if after else None],
                populations=populations,prior_populations=prior_populations,complete_snapshot=bool(complete),
                state_pointer=before['args'][0] if before else None,
                within_invocation_population_change='UNKNOWN_INCOMPLETE' if not complete or population_signature(prior_populations) is None or population_signature(populations) is None else 'UNCHANGED' if population_signature(prior_populations)==population_signature(populations) else 'CHANGED',
                refresh_result=after['result']&255 if after else None,
                cache_branch='NOT_OBSERVED',set_change='REQUIRES_COMPARISON',
                overlap_or_instability=after['status'] if after else None))
        if v['kind']==102:
            children=[(i,c) for i,c in inv.items() if c['parent']==ident]
            admitted=[];missing=[]
            for r in final_rows.get(ident,[]):
                matches=[c for _,c in children if c['kind']==106 and c.get('before',{}).get('command')==r['index']]
                if len(matches)==1 and r['ok'] and matches[0].get('after',{}).get('phase')==2:
                    admitted.append(resource(matches[0]['before']))
                else:missing.append(dict(row_address=r['address'],index=r['index'],candidate_count=len(matches)))
            actual=[dict(invocation=i,source=0 if c['kind']==103 else 1,
                         population=pops.get((i,1,0 if c['kind']==103 else 1)))
                    for i,c in children if c['kind'] in (103,104)]
            ctor_count=sum(c['kind']==106 for _,c in children)
            census=final_rows.get(ident,[])
            expected_count=None
            if after and after['output']['ok']:
                start=field(after['output'],0x38,'<Q');end=field(after['output'],0x40,'<Q')
                if start is not None and end is not None and end>=start and (end-start)%0x170==0:expected_count=(end-start)//0x170
            complete=bool(after and after['phase']==2 and not after['status'] and not missing and len(actual)==2
                          and expected_count==len(census)==ctor_count and [r['index'] for r in census]==list(range(len(census))))
            for p in actual:
                pop=p['population']
                complete=complete and pop is not None and pop['status']==0 and len(pop['members'])==(pop['end']-pop['begin'])//8
            predicted=[];seen=set();projection_known=complete
            for p in sorted(actual,key=lambda x:x['source']):
                if not p['population']:projection_known=False;continue
                for m in p['population']['members']:
                    if m['status']=='UNKNOWN_ID':projection_known=False
                    if m['pointer'] and m['pointer'] not in seen:
                        predicted.append(m['form_id']);seen.add(m['pointer'])
            for _,c in children:
                if c['kind']==105:
                    b=c.get('before');a=c.get('after')
                    if not b or not a or a['phase']!=2 or b['status'] or a['status']:projection_known=False;continue
                    value=field(b['base'],0x28,'<I')
                    if value is None:projection_known=False
                    predicted.append(value)
            observed=[m['form_id'] for m in admitted]
            if any(x is None for x in observed):projection_known=False
            updates.append(dict(invocation=ident,command=before['command'] if before else None,
                model=before['args'][1] if before else None,
                interval=[before['qpc'] if before else None,after['qpc'] if after else None],
                rows=admitted,unresolved_rows=missing,actual_common_inputs=actual,
                special_snapshot=pops.get((ident,1,2)),
                complete_row_association=complete,rendering='NOT_OBSERVED',
                searched_before=field(before['output'],0x90,'<B') if before else None,
                searched_after=field(after['output'],0x90,'<B') if after else None,
                native_input_row_reconciliation='NOT_TESTED' if not projection_known else 'AGREE' if predicted==observed else 'DISAGREE',
                expected_row_ids=predicted if projection_known else None,
                native_ancestry='UNRESOLVED_ASYNCHRONOUS',evaluation_candidates=[],allocation_candidates=[],
                displayed_refresh_timing='UNRESOLVED_NO_RENDER_OBSERVATION',candidate_basis='SOURCE_SNAPSHOT_CONTENT_CORRESPONDENCE_ONLY'))
    previous={}
    for e in evaluations:
        key=(e['state_pointer'],e['site'],e['position']['frame_index'],e['position']['domain_pointer']) if e['position'] else None
        value=population_signature(e['populations'])
        if e['complete_snapshot'] and value is not None:
            e['set_change']='NEW_POPULATION_SIGNATURE' if key not in previous else 'UNCHANGED_POPULATIONS' if previous[key]==value else 'CHANGED_POPULATIONS'
            previous[key]=value
        else:e['set_change']='UNKNOWN_INCOMPLETE'
        e['prior_observation_signature_change']=e['set_change']
    # Content correspondence is deliberately NOT a selected producer ancestor.
    previous_ui={}
    for u in updates:
        row_ids=sorted({m['form_id'] for m in u['rows'] if m['form_id'] is not None})
        if u['complete_row_association'] and all(m['status']=='READ_OK' for m in u['rows']):
            u['native_row_set_change']='NEW' if u['model'] not in previous_ui else 'UNCHANGED' if previous_ui[u['model']]==row_ids else 'CHANGED'
            previous_ui[u['model']]=row_ids
        else:u['native_row_set_change']='UNKNOWN_INCOMPLETE'
        u['allocation_candidates']=[i for i,v in inv.items() if v['kind']==107 and v['site']==0x15784a0 and v.get('after',{}).get('command')==u['command'] and v['after']['qpc']<=u['interval'][0]]
        if not u['complete_row_association']:continue
        wanted=[[ (m['pointer'],m['form_id']) for m in p['population']['members'] ]
                for p in sorted(u['actual_common_inputs'],key=lambda x:x['source'])
                if p['population'] and p['population']['status']==0]
        special=u['special_snapshot']
        if len(wanted)!=2 or not special or special['status']:continue
        wanted.append([(m['pointer'],m['form_id']) for m in special['members']])
        for e in evaluations:
            if not e['complete_snapshot'] or e['interval'][1]>u['interval'][0]:continue
            got=[[(m['pointer'],m['form_id']) for m in p['members']] for p in e['populations']]
            if got==wanted:u['evaluation_candidates'].append(e['invocation'])
    terminal=None;terminal_source=None
    for name in ('retired.json','failure.json'):
        if (root/name).exists():terminal=json.loads((root/name).read_text());terminal_source=name
    durable=terminal.get('last_durable_sequence') if terminal else None
    if terminal and (terminal.get('failed') or terminal.get('captured')!=count or durable!=count or terminal.get('active') or terminal.get('queued',0) or terminal.get('losses',0) or terminal.get('attempted')!=count):errors.append('terminal_incomplete_or_failed')
    instrument_failed=bool(terminal and (terminal_source=='failure.json' or terminal.get('error') or terminal.get('integrity_failure')))
    evidence_status='INCOMPLETE' if errors else 'VERIFIED_PREFIX' if not terminal else 'RETIRED_INTEGRITY_OK'
    return dict(schema='sor-local-readiness-report/8',raw_records_verified=count,
        admitted=terminal.get('attempted') if terminal else None,written=terminal.get('captured') if terminal else None,
        durable=durable,status='INSTRUMENT_FAILURE_VERIFIED_EVIDENCE' if instrument_failed and not errors else evidence_status,
        evidence_status=evidence_status,instrument_outcome='FAILED' if instrument_failed else 'NORMAL_RETIREMENT' if terminal else 'UNRETIRED',
        terminal_source=terminal_source,terminal=terminal,
        errors=errors,evaluations=evaluations,ui_updates=updates,operations=operations,
        milestone_A='NOT_TESTED_NO_DISPLAYED_UI_ORACLE',milestone_B='NOT_TESTED',
        limits=['Header rereads do not prove member-level atomicity','Unhooked reset paths forbid universal revision attribution','Candidate equality is correspondence, not ancestry','Numeric runtime FormIDs require independent plugin mapping'])

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('session',type=Path);ap.add_argument('--out',type=Path);a=ap.parse_args()
    result=inspect(a.session)
    if a.out:
        with a.out.open('x',encoding='utf8',newline='\n') as f:json.dump(result,f,indent=2);f.write('\n')
    print(json.dumps(dict(status=result['status'],records=result['raw_records_verified'],evaluations=len(result['evaluations']),ui_updates=len(result['ui_updates']),errors=result['errors'])))
    return 1 if result['errors'] else 0
if __name__=='__main__':raise SystemExit(main())
