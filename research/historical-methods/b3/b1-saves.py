"""B1 selected protected-save rereads, adapted from owned cs-saves.py/cs-more.py.
Reads selected originals/current immutable archives and owned body catalogue;
exclusive ignored JSON and decoder scratch only; no game or original writes.
"""
from pathlib import Path
import sys,json,hashlib,struct
R=Path.cwd();W=R/'.local-work/outpost-biomes';sys.path.insert(0,str(R/'save-analysis/scripts'))
from inventory_historical_saves import guard,metadata
from stream_save import decoded_save
from research_two_outpost_anchors import inspect
from research_workshop_origin import workshop_prefix
from research_durable_center import resource_rows
from saved_world_components import find_world_components
from outpost_planetary_location import body_catalog
from research_workshop_components import audit as component_audit
from outpost_record_framing import iter_records
from test_outpost_record_framing import independent
from planet_world_key import find_unit3_context,unit3_world_descriptors
def pin(p):
 p=Path(p)
 with p.open('rb') as f:return dict(path=str(p.resolve()),bytes=p.stat().st_size,sha256=hashlib.file_digest(f,'sha256').hexdigest())
def write(p,x):p.open('x',encoding='utf8',newline='\n').write(json.dumps(x,indent=2)+'\n')
survey=json.loads((W/'survey.json').read_text());cases=[]
for label in ['HIST-0035','HIST-0210','HIST-0267']:
 x=next(x for x in survey['rows'] if x['id']==label);assert x['identity_matches'];cases.append((label,Path(x['current']['path']),x['current']))
for label,old in [('Kreet25','coordinate-sufficiency/Save25.json'),('Kreet39','coordinate-sufficiency/Save39.json'),('Kreet31','l3-placement/Save31.json'),('Kreet33','l3-placement/Save33.json')]:
 x=json.loads((R/'.local-work'/old).read_text());print(label,'receipt keys',list(x)[:4],flush=True)
 source=x.get('source')
 if source is not None and 'path' not in source:source=source['copy']
 if source is None:
  source=x['input']
 p=Path(source['path']);actual=pin(p);assert actual['sha256']==source['sha256'];cases.append((label,p,actual))
catpath=R/'.local-work/save-capacity-location/esm-index-verified.json';cat=json.loads(catpath.read_text())
bp,bi=body_catalog(cat['records']);bodykeys={k:f'{v[0]["formid"]:08X}' for k,v in bp.items() if len(v)==1}
write(W/'save-inputs-r3.json',dict(cases=[dict(label=a,source=c) for a,b,c in cases],catalog=pin(catpath)))
for label,p,expected in cases:
 guard();assert pin(p)==expected
 with decoded_save(p,W/'scratch',seconds=float('inf')) as (b,m):
  x=inspect(b,cat['records']);d=x['directory'];rs=list(iter_records(b,*d['regions']['region_R3'],d['words'][9]));other=independent(b,*d['regions']['region_R3'],d['words'][9]);assert [(r['offset'],r['end'],r['token'],r['flags']) for r in rs]==[r[:4] for r in other]
  for bb in x['beacons']:
   r=bb['record'];q=r['body'];shape=b[q];tail=q+13+4*sum(bool(shape&(1<<i)) for i in range(3));bb['initial_flag']=b[tail] if not shape&0x18 else 0x20 if shape&8 else 0
   try:bb['workshop']=workshop_prefix(b,r,bb['prefix'],resource_reader=resource_rows)
   except ValueError as e:bb['workshop_error']=str(e)
  try:components=component_audit(b)
  except ValueError as e:components=dict(error=str(e))
  try:
   ctx=find_unit3_context(b,d['regions']['region_R1'][0],x['global_units'][4][0]-8);descs,end=unit3_world_descriptors(b,ctx);desc=dict(context=ctx,descriptors=descs,end=end)
  except (ValueError,KeyError) as e:desc=dict(error=str(e))
  worlds=None
  if desc.get('descriptors'):
   parents={int(z['parent_token'],16) for z in x['beacons']}
   try:worlds=find_world_components(b,*x['global_units'][6],parents,bodykeys,desc['descriptors'])
   except ValueError as e:worlds=dict(error=str(e))
  write(W/(label+'-r3.json'),dict(source=expected,metrics=m,metadata=metadata(b),extraction=x,components=components,descriptors=desc,worlds=worlds,independent_record_walk=True))
 assert pin(p)==expected
 print(label,'beacons',len(x['beacons']),'descriptors',len(desc.get('descriptors',[])),flush=True)
