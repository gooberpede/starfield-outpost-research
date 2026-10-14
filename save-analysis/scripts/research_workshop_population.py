"""SPDX-License-Identifier: GPL-3.0-or-later
Read qualified existing saves; exclusive fresh ignored receipts, scratch removed.
No target/save/Ghidra/Git/network effects. Stdlib/project only; 40GB C/D guards.
Actual type registry and explicit unknowns supplement, never overwrite, old657.
"""
import argparse
import collections
import json
import struct
from pathlib import Path
from inventory_historical_saves import ROOT,identity,guard
from stream_save import decoded_save
from extractor_resources import plugin_tables,saved_form
from outpost_membership import token_value
from validate_mature_outposts import directory
from workshop_population import typed_records,initial_case,initial_prefix
from workshop_population_extras import partial_extras
from test_outpost_record_framing import independent


def audit(b):
    d=directory(b);plugins=plugin_tables(b);a=d['regions']['reference_u32'][0]
    class Table:
        def __len__(self):return d['reference_count']
        def __getitem__(self,i):
            if not 0<=i<len(self):raise IndexError(i)
            return struct.unpack_from('<I',b,a+4+4*i)[0]
    def resolve(t):return saved_form(token_value(t,Table()),plugins)
    counts=collections.Counter();rows=[];frames=[];leads=[]
    for r in typed_records(b):
        if r['buffer_version']!=153:raise ValueError('UNQUALIFIED_BUFFER_VERSION')
        frames.append((r['offset'],r['end'],r['token'],r['flags']))
        case=initial_case(r);counts['type_%02x'%r['form_type']]+=1;counts['case_'+str(case)]+=1
        refs=[resolve(t) for t in r['refs']]
        row=dict(identity=resolve(r['token']),offset=r['offset'],end=r['end'],form_type=r['form_type'],
            flags=r['flags'],case=case,buffer_version_override=r['buffer_version_override'],
            queued_workshop_keyword='starfield.esm:054ba6' in refs)
        if row['queued_workshop_keyword']:leads.append(dict(row,references=refs))
        if case is None:continue
        try:
            p=initial_prefix(b,r);row['prefix']=p
            for name in ('base_token','initial_reference_token','parent_token','placement_parent_token'):
                if p.get(name):row[name.replace('_token','_identity')]=resolve(p[name])
            if r['form_type']!=0x4b and r['flags']&0x80:
                index=p['next_reference_index']
                if index>=len(r['refs']):raise ValueError('BASE_OVERRIDE_QUEUE_BOUNDS')
                row['saved_base_override_identity']=resolve(r['refs'][index])
                if row['saved_base_override_identity']:
                    row['base_identity']=row['saved_base_override_identity']
            try:
                x=partial_extras(b,r,p)
                for e in x['entries']:
                    e['keyword_identity']=resolve(e['keyword_token']);e['target_identity']=resolve(e['target_token'])
                for e in x['alternate_groups']:e['quest_identity']=resolve(e['base_token'])
                for e in x['packin']:e['identities']=[resolve(t) for t in e['tokens']]
                row['extras']=x
            except ValueError as e:row['extras_error']=str(e);counts['extras_error:'+str(e)]+=1
        except ValueError as e:row['prefix_error']=str(e);counts['prefix_error:'+str(e)]+=1
        rows.append(row)
    arithmetic=independent(b,*d['regions']['region_R3'],d['words'][9])
    if frames!=[r[:4] for r in arithmetic]:raise ValueError('INDEPENDENT_FRAMING_MISMATCH')
    return dict(schema='typed-workshop-population/1',counts=dict(counts),references=rows,
        keyword_queue_leads=leads,all_records=len(frames),independent_framing=True,
        population_complete=False,offset_domain='DECODED_LOGICAL_STREAM')


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--inputs',type=Path,required=True)
    ap.add_argument('--run',required=True);ap.add_argument('--labels',nargs='*');args=ap.parse_args()
    if not args.run.isascii() or not args.run.replace('-','').isalnum():raise ValueError('RUN_NAME')
    inputs=json.loads(args.inputs.read_text(encoding='utf8'));out=ROOT/'.local-work/workshop-population-rework'/args.run
    guard();out.mkdir(exist_ok=False);summaries=[]
    for item in inputs:
        if args.labels and item['label'] not in args.labels:continue
        pin=item['pin'];path=Path(pin['path']);assert identity(path)==pin;guard()
        with decoded_save(path,out/'scratch') as (b,metrics):result=audit(b)
        assert identity(path)==pin
        result.update(source=pin,label=item['label'],series=item['series'],decode=metrics)
        with (out/(item['series']+'-'+item['label']+'.json')).open('x',encoding='utf8',newline='\n') as f:
            json.dump(result,f,indent=2);f.write('\n')
        summary=dict(label=item['label'],records=result['all_records'],counts=result['counts'],
            keyword_leads=len(result['keyword_queue_leads']))
        summaries.append(summary);print(item['label'],result['all_records'],summary['keyword_leads'],flush=True)
    with (out/'summary.json').open('x',encoding='utf8',newline='\n') as f:json.dump(summaries,f,indent=2);f.write('\n')
    guard()
