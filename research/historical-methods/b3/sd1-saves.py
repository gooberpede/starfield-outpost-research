"""SD1 observational saved candidate search. Owned typed prefixes, DA1 actor
links, S1 inventory grammar. Hash originals pre/post; temporary decoding cleaned.
Writes local-only receipts, no active-save writes. Unknowns never imply empty."""
from pathlib import Path
import sys,json,struct,collections
R=Path.cwd();W=R/'.local-work/sd1-containers';sys.path[:0]=[str(R/'research/s1-storage'),str(R/'.local-work/da1-defense'),str(R/'research/r1-robots'),str(R/'.local-work/cr1-crew'),str(R/'save-analysis/scripts')]
from catalog import pin
from saved import inventory
from links_da1 import actor_prefix,explicit_actor_links
from crew_extras import extra_view
from inventory_historical_saves import guard
from stream_save import decoded_save
from extractor_resources import plugin_tables,saved_form
from outpost_membership import token_value
from validate_mature_outposts import directory
from workshop_population import typed_records,initial_prefix
cs=json.loads((W/'census01.json').read_text());by={r['formid']:r for r in cs['definitions']};ids={int(r['base'],16) for r in cs['rows']};ids.update(int(r['base'],16) for r in cs['children'] if r['base_type'] in ('CONT','NPC_'));bases={f'starfield.esm:{i:06x}':by[i] for i in ids if i in by}
inv={r['inventory_id']:r['source'] for r in json.loads((R/'.local-work/historical-inventory/scan-01/inventory.json').read_text())}
labels=sys.argv[1:] or ['HIST-0036','HIST-0077','HIST-0083','HIST-0255','HIST-0267']
for label in labels:
 out=W/('saved-'+label+'.json')
 if out.exists():continue
 src=inv[label];p=Path(src['path']);before=pin(p);assert before['sha256']==src['sha256'];guard();rows=[];gaps=collections.Counter();counts=collections.Counter()
 with decoded_save(p,W/'save-scratch') as (data,decoded):
  dr=directory(data);forms=struct.unpack_from('<'+'I'*dr['reference_count'],data,dr['regions']['reference_u32'][0]+4);plugins=plugin_tables(data)
  def resolve(t):return saved_form(token_value(t,forms),plugins)
  for rec in typed_records(data):
   counts[f'type_{rec["form_type"]:02x}']+=1
   if rec['form_type'] not in (0x4a,0x4b):continue
   try:pref=actor_prefix(data,rec) if rec['form_type']==0x4b else initial_prefix(data,rec)
   except (ValueError,struct.error,IndexError) as e:gaps[str(e)]+=1;continue
   base=resolve(pref['base_token']) if pref.get('base_token') else None
   if base not in bases:continue
   row=dict(identity=resolve(rec['token']),base=base,edid=bases[base]['edid'],record=rec,prefix=pref,queue=[resolve(t) for t in rec['refs']],body_hex=bytes(data[rec['body']:rec['end']]).hex())
   try:row['extras']=extra_view(data,rec,pref,resolve);row['inventory']=inventory(data,rec,row['extras'],resolve)
   except (ValueError,struct.error,IndexError) as e:row['gap']=str(e)
   if rec['form_type']==0x4b:
    try:row['actor_links']=explicit_actor_links(data,rec,resolve)
    except (ValueError,struct.error,IndexError) as e:row['actor_gap']=str(e)
   rows.append(row)
 assert pin(p)==before;out.open('x',encoding='utf8').write(json.dumps(dict(label=label,source=before,decoded=decoded,rows=rows,counts=counts,prefix_gaps=gaps,source_unchanged=True),indent=2)+'\n')
 print(label,'candidates',len(rows),collections.Counter(r['edid'] for r in rows),flush=True)
guard()
