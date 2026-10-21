from pathlib import Path
import sys,json,struct,collections,hashlib
R=Path.cwd();W=R/'.local-work/l3-placement';sys.path[:0]=[str(R/'save-analysis/scripts'),str(R/'.local-work/cr1-crew')]
from inventory_historical_saves import guard
from stream_save import decoded_save
from workshop_inventory import audit,ownership_ledger,constructed_inventory
from workshop_population import typed_records,initial_prefix
from extractor_resources import plugin_tables,saved_form
from outpost_membership import token_value
from validate_mature_outposts import directory
from crew_extras import extra_view
from test_outpost_record_framing import independent
def pin(p):
 with p.open('rb') as f:return dict(path=str(p),bytes=p.stat().st_size,sha256=hashlib.file_digest(f,'sha256').hexdigest())
seed=json.loads((W/'baseline.json').read_text());guard()
for row in seed['inputs']:
 p=Path(row['copy']['path']);assert pin(p)==row['copy'];label=p.name.split('_')[0];out=W/(label+'.json');assert not out.exists()
 with decoded_save(p,W/'scratch',seconds=float('inf')) as (b,metrics):
  raw=audit(b);d=directory(b);arith=independent(b,*d['regions']['region_R3'],d['words'][9]);assert [(r['offset'],r['end'],r['token'],r['change_flags']) for r in raw['records']]==[r[:4] for r in arith]
  inv=constructed_inventory(ownership_ledger(raw,None),None)
  forms=struct.unpack_from('<'+'I'*d['reference_count'],b,d['regions']['reference_u32'][0]+4);plugins=plugin_tables(b)
  def resolve(t):return saved_form(token_value(t,forms),plugins)
  beacons=[];state=[];gaps=collections.Counter()
  for r in typed_records(b):
   state.append(dict(id=resolve(r['token']),type=r['form_type'],offset=r['offset'],end=r['end'],change_flags=r['flags'],body_sha256=hashlib.sha256(b[r['body']:r['end']]).hexdigest(),refs=[resolve(t) for t in r['refs']]))
   if r['form_type']!=0x4a:continue
   try:prefix=initial_prefix(b,r)
   except (ValueError,struct.error) as e:gaps[str(e)]+=1;continue
   if not prefix.get('base_token') or resolve(prefix['base_token'])!='starfield.esm:2c60e9':continue
   x=dict(identity=resolve(r['token']),record=r,prefix=prefix,refs=[resolve(t) for t in r['refs']])
   try:x['extras']=extra_view(b,r,prefix,resolve)
   except (ValueError,struct.error) as e:x['extra_gap']=str(e)
   beacons.append(x)
  result=dict(label=label,source=row,decode=metrics,inventory=inv,beacons=beacons,record_states=state,prefix_gaps=dict(gaps),build_string_present=b.find(b'1.16.244.0')>=0,header_hex=bytes(b[:24]).hex(),independent_record_walk=True)
 assert pin(p)==row['copy'] and pin(Path(row['source']['path']))==row['source']
 out.open('x',encoding='utf8').write(json.dumps(result,indent=2)+'\n');print(label,'roots',len(inv['constructed_instances']),'beacons',len(beacons),'records',len(state),flush=True)
