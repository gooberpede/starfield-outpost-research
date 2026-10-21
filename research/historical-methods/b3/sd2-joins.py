"""SD2 focused saved owner joins, read-only originals and owned typed readers.
Re-decodes H18/H36/H257; writes exclusive local JSON, scratch cleaned."""
from pathlib import Path
import sys,json,struct
R=Path.cwd();W=R/'.local-work/sd2-shared';sys.path[:0]=[str(R/'research/s1-storage'),str(R/'.local-work/cr1-crew'),str(R/'save-analysis/scripts')]
from catalog import pin
from inventory_historical_saves import guard
from stream_save import decoded_save
from extractor_resources import plugin_tables,saved_form
from outpost_membership import token_value
from validate_mature_outposts import directory
from workshop_population import typed_records,initial_prefix
from crew_extras import extra_view
from saved import inventory
results=[]
for label in ['HIST-0018','HIST-0036','HIST-0257']:
 j=json.loads((W/('saved-'+label+'.json')).read_text());before=j['source'];p=Path(before['path']);assert pin(p)==before;guard()
 wanted={e['target'] for r in j['candidates'] for e0 in r.get('extras',{}).get('extras',[]) if e0['type']=='4c' for e in e0['entries'] if e['keyword']=='starfield.esm:054ba6'};found=[]
 with decoded_save(p,W/'join-scratch') as (data,decoded):
  dr=directory(data);forms=struct.unpack_from('<'+'I'*dr['reference_count'],data,dr['regions']['reference_u32'][0]+4);plugins=plugin_tables(data)
  def resolve(t):return saved_form(token_value(t,forms),plugins)
  for rec in typed_records(data):
   ident=resolve(rec['token'])
   if ident not in wanted and ident!='starfield.esm:000014':continue
   row=dict(identity=ident,record=rec,queue=[resolve(t) for t in rec['refs']],body_hex=bytes(data[rec['body']:rec['end']]).hex())
   if rec['form_type']==0x4a:
    pref=initial_prefix(data,rec);row['prefix']=pref;row['base']=resolve(pref['base_token']) if pref.get('base_token') else None
    try:row['extras']=extra_view(data,rec,pref,resolve);row['inventory']=inventory(data,rec,row['extras'],resolve)
    except (ValueError,IndexError,struct.error) as e:row['gap']=repr(e)
   found.append(row)
 assert pin(p)==before
 results.append(dict(label=label,source=before,decoded=decoded,owner_ids=sorted(wanted),records=found,source_unchanged=True));print(label,'owners',len(wanted),'found',[(r['identity'],r.get('base')) for r in found],flush=True)
(W/'joins01.json').open('x',encoding='utf8').write(json.dumps(results,indent=2)+'\n');guard()
