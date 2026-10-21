"""SD2 owned SD1 inline-base survey adaptation. Reads immutable canonical
historical originals, hashes pre/post, strict temporary decode with cleanup.
Writes new local-only candidate/capability receipts; no save/data mutations."""
from pathlib import Path
import sys,json,struct,collections,traceback
R=Path.cwd();W=R/'.local-work/sd2-shared';sys.path[:0]=[str(R/'research/s1-storage'),str(R/'.local-work/da1-defense'),str(R/'research/r1-robots'),str(R/'.local-work/cr1-crew'),str(R/'save-analysis/scripts')]
from catalog import pin
from saved import inventory
from crew_extras import extra_view
from inventory_historical_saves import guard
from stream_save import decoded_save
from extractor_resources import plugin_tables,saved_form
from outpost_membership import token_value
from validate_mature_outposts import directory
from workshop_population import typed_records,initial_prefix
inv=json.loads((R/'.local-work/historical-inventory/scan-01/inventory.json').read_text());selection=[];missing=[];out=[]
for entry in inv:
 label=entry['inventory_id'];src=entry['source'];p=Path(src['path'])
 if not p.is_file():missing.append(label);continue
 selection.append(label)
 guard();before=pin(p);assert before['sha256']==src['sha256']
 row=dict(label=label,source=before,candidates=[],prefix_gaps={},counts={})
 try:
  with decoded_save(p,W/'save-scratch') as (data,decoded):
   dr=directory(data);forms=struct.unpack_from('<'+'I'*dr['reference_count'],data,dr['regions']['reference_u32'][0]+4);plugins=plugin_tables(data)
   def resolve(t):return saved_form(token_value(t,forms),plugins)
   gaps=collections.Counter();counts=collections.Counter();candidates=[];addon_refs=0
   for rec in typed_records(data):
    if rec['form_type']!=0x4a:continue
    counts['REFR']+=1
    try:pref=initial_prefix(data,rec)
    except (ValueError,struct.error,IndexError) as e:gaps[str(e)]+=1;continue
    base=resolve(pref['base_token']) if pref.get('base_token') else None
    if base and base.lower().startswith('sfbgs00d.esm:'):addon_refs+=1
    if not base or base.lower() not in ('sfbgs00d.esm:02af77','sfbgs00d.esm:2af77'):continue
    item=dict(identity=resolve(rec['token']),base=base,record=rec,prefix=pref,queue=[resolve(t) for t in rec['refs']],body_hex=bytes(data[rec['body']:rec['end']]).hex())
    try:item['extras']=extra_view(data,rec,pref,resolve);item['inventory']=inventory(data,rec,item['extras'],resolve)
    except (ValueError,struct.error,IndexError) as e:item['gap']=str(e)
    candidates.append(item)
   row.update(decoded=decoded,candidates=candidates,prefix_gaps=dict(gaps),counts=dict(counts),addon_inline_refs=addon_refs,plugins=plugins,status='QUALIFIED_INLINE_BASE_SEARCH')
 except (ValueError,struct.error,IndexError,AssertionError) as e:
  row.update(status='CAPABILITY_FAILURE',error=repr(e),traceback=traceback.format_exc())
 assert pin(p)==before;row['source_unchanged']=True
 (W/('saved-'+label+'.json')).open('x',encoding='utf8').write(json.dumps(row,indent=2)+'\n');out.append({k:v for k,v in row.items() if k in ('label','status','error','source','counts','prefix_gaps','addon_inline_refs')}|dict(candidate_count=len(row['candidates'])))
 print(label,row['status'],len(row['candidates']),flush=True)
(W/'corpus01.json').open('x',encoding='utf8').write(json.dumps(dict(selection=selection,missing=missing,results=out),indent=2)+'\n');guard()
