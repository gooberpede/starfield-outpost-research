"""Original exhaustive available historical modern-header target scan.
Reads frozen scan04 originals in place, no copies/source writes. Native-qualified
typed R3 and supported prefix/extras readers; small exclusive per-save JSONL.
Checks C/D40GB, frozen full identity and source before/after. Unsupported body
semantics retained as gaps, never guessed. Cross-save FFIDs not owner authority.
"""
import sys,json,struct,collections,time
from pathlib import Path
sys.path.insert(0,'save-analysis/scripts')
from inventory_historical_saves import identity,guard,metadata
from stream_save import decoded_save
from workshop_population import typed_records,initial_case,initial_prefix
from workshop_population_extras import partial_extras as linked_prefix
from validate_mature_outposts import directory
from extractor_resources import saved_form
from historical_plugins03 import plugin_tables
from outpost_membership import token_value
root=Path('.local-work/workshop-population-rework');out=root/'specialist'
paths=[out/'historical-all-input11.json',root/'nonowner-da01.json',Path('.local-work/workshop-inventory/final05/mature-Save52.json'),Path(__file__)]
pins=[identity(p) for p in paths];inventory=json.loads(paths[0].read_text());da=json.loads(paths[1].read_text());old=json.loads(paths[2].read_text())
groups={r['identity'] for r in da['nonnull_groups'] if str(r['identity']).startswith('DYNAMIC:')}
members={r['identity'] for r in da['rows'] if groups&set((r.get('da') or {}).get('identities',[]))}
owners={r['owner_identity'] for r in old['owners']};canonical={r['target'] for r in json.loads((root/'nonowner-relations01.json').read_text())['rows']};targets=groups|members|owners|canonical
assert len(groups)==31 and len(owners)==19
group_tokens={f'{0x800000|(int(g.split(chr(58))[1],16)&0x3fffff):06x}' for g in groups}
summary=[];began=time.monotonic();receipt=out/'historical-targetcensus11.jsonl'
with receipt.open('x',encoding='utf8') as dest:
 for item in inventory:
  guard();src=item['source'];path=Path(src['path']);r=dict(inventory_id=item['inventory_id'],source=src,frozen_metadata=item.get('metadata'),status='PENDING')
  if not path.is_file():r['status']='MISSING_ORIGINAL'
  else:
   current=identity(path)
   r['frozen_source']=src; r['frozen_identity_match']=current==src; src=current; r['source']=src
   if False:pass
   else:
    versions=[v['text'] for v in item.get('metadata',{}).get('build_strings',[])]
    if False:r['status']='OLDER_HEADER_UNQUALIFIED'
    else:
     try:
      with decoded_save(path,out/'historical-scratch11') as (b,metrics):
       md=metadata(b);r.update(metadata=md,decode=metrics,buffer_version=b[0x14]);assert [v['text'] for v in md['build_strings']][0]=='1.16.244.0','OLDER_HEADER_UNQUALIFIED'
       if b[0x14]!=153:raise ValueError('UNQUALIFIED_BUFFER_VERSION')
       d=directory(b);a=d['regions']['reference_u32'][0];plugins=plugin_tables(b)
       class Table:
        def __len__(self):return d['reference_count']
        def __getitem__(self,i):
         if not 0<=i<len(self):raise IndexError(i)
         return struct.unpack_from('<I',b,a+4+4*i)[0]
       def resolve(t):return saved_form(token_value(t,Table()),plugins)
       rows=[];count=0;types=collections.Counter()
       for record in typed_records(b):
        count+=1;types[record['form_type']]+=1;own=resolve(record['token'])
        if own not in targets and not group_tokens&set(record['refs']):continue
        refs=[resolve(t) for t in record['refs']]
        row=dict(identity=own,offset=record['offset'],end=record['end'],form_type=record['form_type'],flags=record['flags'],buffer_version=record['buffer_version'],references=refs,groups_mentioned=sorted(groups&set(refs)),self_target_categories=[name for name,s in [('group',groups),('DA_member',members),('owner',owners),('canonical191',canonical)] if own in s],case=initial_case(record))
        if row['case'] is not None:
         try:
          p=initial_prefix(b,record);row['prefix']=p
          for name,key in [('base_identity','base_token'),('parent_identity','parent_token'),('placement_parent_identity','placement_parent_token')]:
           if p.get(key):row[name]=resolve(p[key])
          e=linked_prefix(b,record,p);row['extras']=e
          row['links']=[dict(x,keyword_identity=resolve(x['keyword_token']),target_identity=resolve(x['target_token'])) for x in e['entries']]
          row['alternate_group_identities']=[dict(x,quest_identity=resolve(x['base_token'])) for x in e['alternate_groups']]
          row['packin_identities']=[dict(x,identities=[resolve(t) for t in x['tokens']]) for x in e['packin']]
         except (ValueError,IndexError,KeyError,TypeError) as error:row['semantic_gap']=str(error)
        rows.append(row)
       assert count==d['words'][9]
       r.update(status='QUALIFIED_TYPED_R3_CLOSED',record_count=count,form_type_counts=dict(types),target_rows=rows,target_row_count=len(rows),groups_found=sorted({x['identity'] for x in rows}&groups),members_found=sorted({x['identity'] for x in rows}&members),owners_found=sorted({x['identity'] for x in rows}&owners))
     except (ValueError,AssertionError,IndexError,KeyError) as error:r.update(status='RETAINED_UNQUALIFIED_FAILURE',error=str(error))
    r['source_after']=identity(path)
    if r['source_after']!=src:raise RuntimeError('SOURCE_CHANGED_DURING_SCAN')
  dest.write(json.dumps(r)+'\n');dest.flush();summary.append({k:v for k,v in r.items() if k not in ('target_rows','frozen_metadata','decode','metadata')})
  print(item['inventory_id'],r['status'],r.get('target_row_count',0),flush=True)
assert [identity(p) for p in paths]==pins
result=dict(schema='available-modern-historical-targets/1',inputs=pins,target_counts=dict(groups=len(groups),DA_members=len(members),owners=len(owners),canonical191=len(canonical)),groups=sorted(groups),DA_members=sorted(members),owners=sorted(owners),inventory_count=len(inventory),status_counts=dict(collections.Counter(r['status'] for r in summary)),seconds=time.monotonic()-began,samples=summary,limits='All inventory originals checked; only first-header1.16.244.0/buffer153 uses pinned native semantics. Cross-character or cross-playthrough FFID equality is a lead, not persistence/ownership authority. Unknown extras retained, no target absence conclusion from decoder gap.')
with (out/'historical-targetcensus11-summary.json').open('x',encoding='utf8') as f:json.dump(result,f,indent=2);f.write('\n')
print(result['status_counts'],result['target_counts'],flush=True)
