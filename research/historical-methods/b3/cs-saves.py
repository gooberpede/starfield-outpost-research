from pathlib import Path
import sys,json,struct,hashlib,math
R=Path.cwd();W=R/'.local-work/coordinate-sufficiency';sys.path[:0]=[str(R/'save-analysis/scripts')]
from inventory_historical_saves import guard
from stream_save import decoded_save
from research_two_outpost_anchors import inspect
from research_workshop_origin import workshop_prefix
from research_workshop_components import audit as component_audit
from workshop_inventory import audit,ownership_ledger,constructed_inventory,reference_prefix
from outpost_planetary_location import associations,body_catalog
from outpost_record_framing import iter_records
from validate_mature_outposts import directory
from test_outpost_record_framing import independent
from beacon_terrain_projection import to_square,grid_cell,split_local
from position_quantizer_diagnostic import diagnose
def pin(p):
 p=Path(p)
 with p.open('rb') as f:return dict(path=str(p),bytes=p.stat().st_size,sha256=hashlib.file_digest(f,'sha256').hexdigest())
def write(p,x):p.open('x',encoding='utf8',newline='\n').write(json.dumps(x,indent=2)+'\n')
cat=json.loads((R/'.local-work/save-capacity-location/esm-index-verified.json').read_text());by_pair,by_id=body_catalog(cat['records'])
seed=json.loads((W/'baseline.json').read_text());guard()
cases=[(x['source']['path'].split('Save')[-1].split('_')[0],Path(x['copy']['path']),x['copy']) for x in seed['inputs']]
prior=json.loads((R/'.local-work/two-outpost-anchor/extract-04/manifest.json').read_text())
p=Path(prior['copy']['path']);assert pin(p)['sha256']==prior['copy']['sha256'];cases.append(('25',p,pin(p)))
for label,path,expected in cases:
 assert pin(path)==expected
 with decoded_save(path,W/'scratch',seconds=float('inf')) as (b,m):
  ext=inspect(b,cat['records']);d=directory(b);rs=list(iter_records(b,*d['regions']['region_R3'],d['words'][9]))
  arith=independent(b,*d['regions']['region_R3'],d['words'][9]);assert [(r['offset'],r['end'],r['token'],r['flags']) for r in rs]==[r[:4] for r in arith]
  players=[]
  for r in rs:
   if r['token']!='400014':continue
   q=r['body'];shape=b[q];tail=q+13+4*sum(bool(shape&(1<<i)) for i in range(3))
   pp=dict(record=r,xyz=list(struct.unpack_from('<3f',b,q+1)),xyz_offset=q+1,xyz_hex=b[q+1:q+13].hex(),shape=shape,initial_flag=b[tail] if not shape&0x18 else 0x20 if shape&8 else 0)
   try:pp['prefix']=reference_prefix(b,r,4)
   except ValueError as e:pp['prefix_error']=str(e)
   pp['cache'],pp['points']=associations(b,*ext['global_units'][6],r['refs'][0],by_pair,by_id)
   players.append(pp)
  for bb in ext['beacons']:
   r=bb['record'];pp=bb['prefix'];q=r['body'];shape=b[q];tail=q+13+4*sum(bool(shape&(1<<i)) for i in range(3))
   bb['initial_flag']=b[tail] if not shape&0x18 else 0x20 if shape&8 else 0
   try:bb['workshop']=workshop_prefix(b,r,pp)
   except ValueError as e:bb['workshop_error']=str(e)
   for pt in bb['points']:
    t,u,v=to_square(*pt['pair']);pt['model_cell']=grid_cell(*pt['pair']);pt['center_residual_cells']=[(u+.5)*49152-pt['model_cell'][1]-.5,(v+.5)*49152-pt['model_cell'][2]-.5];pt['diagnostic']=diagnose(*pt['pair'])
  try:components=component_audit(b)
  except ValueError as e:components=dict(error=str(e))
  inv=constructed_inventory(ownership_ledger(audit(b),None),None)
  write(W/('Save'+label+'.json'),dict(source=expected,metrics=m,extraction=ext,players=players,components=components,inventory=inv,independent_records=True,header=b[:24].hex(),build_string_present=b.find(b'1.16.244.0')>=0))
  print(label,'beacons',[(x['token'],x['local_xyz'],x['points']) for x in ext['beacons']],'player',[(x['xyz'],x['record']['refs'][:4]) for x in players],flush=True)
 assert pin(path)==expected
