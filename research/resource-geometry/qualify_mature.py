# SPDX-License-Identifier: GPL-3.0-or-later
"""RG2-A1 conditional mature ordinary-initialization baseline.

Adapted from owned qualify_sites.py at task HEAD; original retained unchanged.
Reads exact existing local definition/map/frame/selection/angular receipts and
fresh EXE constants. Writes exclusive --output JSON beneath .local-work.
Stdlib/owned math only; no save decode, target/database/configuration effects.
Not a historical loaded/rebased-manager reconstruction or native spatial oracle.
Everywhere follows inspected native order, uses its own DNAM/rarity6, weight1.
"""
from pathlib import Path
import sys,json,struct,hashlib,math,argparse
R=Path(__file__).resolve().parents[2];W=R/'.local-work/resource-geometry';M=R/'.local-work/resource-geometry-mature-context'
ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--sample',choices=['Feynman','Carinae'],required=True);ap.add_argument('--name',required=True);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
assert not args.output.exists()
assert args.output.resolve().is_relative_to((R/'.local-work').resolve())
def pin(p):
 p=Path(p)
 with p.open('rb') as f:return dict(path=str(p),bytes=p.stat().st_size,sha256=hashlib.file_digest(f,'sha256').hexdigest())
inputs=[W/'source-definitions01.json',M/'selection-empty-local.json',R/'.local-work/outpost-biomes/model-r2.json',R/('.local-work/outpost-biomes/'+('feynman v' if args.sample=='Feynman' else 'carinae iii-a')+'.biom'),R/'.local-work/resource-milestone-b-spatial-constants.json',Path(__file__),R/'research/resource-geometry/geometry.py',R/'research/resource-geometry/context.py']
inputs += [M/'angular-discriminator01.json',R/'.local-work/resource-geometry-live-prep/mature-diagnostics.json',R/'.local-work/resource-geometry-live-prep/mature-alternatives.json',M/'selection-inherited-water.json']
before=[pin(p) for p in inputs]
import context,geometry
rows=json.loads((W/'source-definitions01.json').read_text())['records'];by={r['formid']:r for r in rows}
def fs(r):return [(t,bytes.fromhex(v)) for t,v in r['fields']]
def last(r,t):return next(v for k,v in reversed(fs(r)) if k==t)
styles={r['formid']:int.from_bytes(last(r,'NNAM'),'little') for r in rows if r['type']=='BIOM' and any(t=='NNAM' for t,v in fs(r))}
blocks={r['formid']:dict(dimensions=struct.unpack('<II',last(r,'DNAM'))) for r in rows if r['type']=='SFBK'}
patterns={};registry=[]
for r in rows:
 if r['type']!='SFPT' or not any(t=='CNAM' for t,v in fs(r)):continue
 f=list(struct.unpack('<256I',last(r,'FNAM')));g=last(r,'GNAM')
 patterns[r['formid']]=dict(entries=list(zip(f,g)))
 registry.append(dict(id=r['formid'],style=int.from_bytes(last(r,'CNAM'),'little')))
m=context.read_map((R/('.local-work/outpost-biomes/'+('feynman v' if args.sample=='Feynman' else 'carinae iii-a')+'.biom')).read_bytes())
body=0x5e0de if args.sample=='Feynman' else 0x5e4da
p=by[body];system,parent,index=struct.unpack('<III',next(v for t,v in fs(p) if t=='GNAM' and len(v)==12))
selected=context.select_patterns(m,styles,registry,system,index);selected['map']=m
frames=json.loads((R/'.local-work/resource-geometry-live-prep/mature-diagnostics.json').read_text())
frame=next(f for f in frames if f['name']==args.name and int(f['body'],16)==body)
assert frame['frame']=='2b'
angular=next(f for f in json.loads((M/'angular-discriminator01.json').read_text()) if f['name']==args.name)
assert all(f['matches_descriptor'] for f in angular['snaps'])
assert {f['mode'] for f in angular['snaps']}=={'avx','fma'}
assert all(f['raw_cell']==frame['base'] for f in angular['snaps'])
descriptor=frame['descriptor'];tag=descriptor['tag'];origin=[descriptor['x'],descriptor['y']]
assert tag==0 and all(x%96==0 for x in origin)
translation=[100*(frame['base'][i+1]-origin[i]) for i in range(2)]
center=[frame['center'][i]+translation[i] for i in range(2)]
# Qualification is explicitly the static ordinary initialization route on the
# installed main-file/default-settings baseline. It is not a captured historical
# manager/rebase epoch. Center translation uses exact represented saved values;
# final native translation rounding remains a small unvalidated boundary term.
# Independently chosen fixed lattice, including beacon and offsets; declared
# before geometry generation. No target label, production or UI resource list.
offsets=([[dx,dy] for dx in range(-300,301,100) for dy in range(-300,301,100)]
         if args.sample=='Feynman' else
         [[dx,dy] for dx in (-100,0,100) for dy in (-100,0,100)]+[[155,0],[-155,0],[0,155],[0,-155]])
queries=[[center[0]+dx,center[1]+dy] for dx,dy in offsets]
query_radius=max(150,max(math.hypot(*v) for v in offsets))
maximum_width=max(max(struct.unpack_from('<2f',b,40*(i+7)+8)) for record in rows if record['type']=='RSGD' for t,b in fs(record) if t=='DNAM' for i in range(7))
halo=context.neighborhood(tag,origin,center,query_radius,selected,patterns,blocks,maximum_width=maximum_width)
blob=Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield/Starfield.exe').read_bytes()
assert hashlib.sha256(blob).hexdigest()=='7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28'
pe=struct.unpack_from('<I',blob,0x3c)[0];n,opt=struct.unpack_from('<H',blob,pe+6)[0],struct.unpack_from('<H',blob,pe+20)[0]
sections=[struct.unpack_from('<IIII',blob,pe+24+opt+i*40+8) for i in range(n)]
cs=json.loads((R/'.local-work/resource-milestone-b-spatial-constants.json').read_text())['constants']
assert all(blob[x['file_offset']:x['file_offset']+4].hex()==x['bytes'] for x in cs)
c={int(x['va'],16):x['float'] for x in cs}
scalars=[]
for va in (0x144f03f50,0x144f04cb8,0x144f04250,0x144f041cc,0x144f040c0,0x144f03eec,0x144f03d6c):
 rva=va-0x140000000;s=next(s for s in sections if s[1]<=rva<s[1]+s[2]);off=s[3]+rva-s[1];v=struct.unpack_from('<f',blob,off)[0];c[va]=v
 scalars.append(dict(va=hex(va),offset=off,raw=blob[off:off+4].hex(),value=v))
planet=next(p for p in json.loads((M/'selection-empty-local.json').read_text())['rows'] if int(p['body'],16)==body)
alternate=next(p for p in json.loads((M/'selection-inherited-water.json').read_text())['rows'] if int(p['body'],16)==body)
assert planet['families']==alternate['families']
results=[]
for source in halo['sources']:
 biome=source['resource_biome'];view=next(v for v in planet['biome_results'] if int(v['orchestration']['biome']['form_id'],16)==biome)
 assert view['orchestration']['special_selection'] is None
 family=view['family_access']['family'];root=int(family['root']['form_id'],16)
 rid=int(view['orchestration']['effective_rsgd']['form_id'],16)
 raw=None;candidate=None
 for t,b in fs(by[rid]):
  if t=='RNAM':candidate=int.from_bytes(b,'little')
  if t=='DNAM' and candidate==root:raw=b;break
 assert raw is not None
 selected_ids=[int(x,16) for x in family['emitted_form_ids']]
 rar={f:int.from_bytes(last(by[f],'SNAM'),'little')&255 for f in selected_ids}
 # Query-mask uniformity over ownership + merge proves first-query independence
 # for these interior sources. Enforce a conservative 4-cell margin.
 ax,ay=source['geographic_origin'];dx,dy=source['dimensions']
 masks={context.mask_lookup(m,tag,x,y) for x in range(ax-4,ax+dx+5) for y in range(ay-4,ay+dy+5)}
 assert len(masks)==1,masks
 mask=next(iter(masks))&15
 ordered=[]
 for fid in sorted(selected_ids,key=lambda f:-rar[f]):
  rarity=rar[fid];block=list(struct.unpack_from('<10f',raw,40*(rarity+7)))
  assert max(block[2:4])<=maximum_width
  weights=[c[0x144f04250],c[0x144f041cc],c[0x144f040c0],c[0x144f03eec],0]
  weight=weights[rarity] if mask==8 or mask<rarity else 1
  ordered.append(dict(resource=f'{fid:08x}',block=block,weight=weight))
 # Native separate Everywhere processing follows main and Special; own
 # descriptor and weight 1. No Special selection in these qualified model rows.
 everywhere=[int(e['resource_form_id'],16) for e in view['orchestration']['effective_rsgd']['entries'] if int.from_bytes(last(by[int(e['resource_form_id'],16)],'SNAM'),'little')&255==6]
 assert len(everywhere)<=1
 for fid in everywhere:
  payload=None;candidate=None
  for t,b in fs(by[rid]):
   if t=='RNAM':candidate=int.from_bytes(b,'little')
   if t=='DNAM' and candidate==fid:payload=b;break
  assert payload is not None,'requires native alternate descriptor resolution'
  block=list(struct.unpack_from('<10f',payload,40*(6+7)))
  assert max(block[2:4])<=maximum_width
  ordered.append(dict(resource=f'{fid:08x}',block=block,weight=1.0))
 xmin,xmax,ymin,ymax=source['cell_bounds']
 keys={f'{x},{y}':context.packed_seed_key(tag,origin,source['origin'],[x,y],system,index) for x in range(xmin,xmax) for y in range(ymin,ymax)}
 req=dict(source=source['id'],provenance=f'RG2-A1 static ordinary INITIALIZATION frame, PNDT owner and main-file selection; {args.sample}/{args.name}; historical/rebased context UNOBSERVED',origin=source['origin'],owner_key=body,clip_center=source['clip_center'],clip_half=source['clip_half'],context_qualified=True,order_qualified=True,cell_bounds=source['cell_bounds'],packed_keys=keys,ordered_resources=ordered)
 result=geometry.populate_source(req,c);assert result['status']=='CONDITIONAL_PLANAR_SOURCE',result
 paths=result['regions']
 for path in paths:
  path['nominal']=geometry.nominal_strips(path['points'],center)
  path['unbounded_region_union_circle']=geometry.region_circle(path['points'],center)
  path['bounded_region_circle']=geometry.bounded_region_circle(path['points'],center)
 fixed=[dict(point=q,resources=sorted({p['resource'] for p in paths if geometry.region_membership(p['points'],q)=='INTERIOR'})) for q in queries]
 results.append(dict(source=source,mask=mask,request=req,regions=paths,fixed_queries=fixed,cells=len(result['cells']),words=sum(len(x['words']) for x in result['cells'])))
 print(source['id'],'mask',mask,'resources',[(x['resource'],x['weight']) for x in ordered],'paths',len(paths),'hits',[(p['resource'],p['cell']) for p in paths if p['nominal'].get('intersection')=='POSITIVE_AREA'])
allpaths=[p for s in results for p in s['regions']]
fixed=[dict(point=q,resources=sorted({p['resource'] for p in allpaths if geometry.region_membership(p['points'],q)=='INTERIOR'})) for q in queries]
assert before==[pin(p) for p in inputs]
out=dict(sample=args.sample,name=args.name,tag=tag,status='CONDITIONAL_MAIN_FILE_DEFAULT_SETTINGS_ORDINARY_INITIALIZATION',translation=translation,source_frame_basis='native angular landing-snap matches exact joined secondary descriptor; AVX/FMA diagnostic agreement; scalar cos/native epoch unobserved',uncertainties=['historical selected/rebased context','effective overrides/component-selected alternate RSGD','scalar-cos/native FP environment','final center translation rounding','native marginal quaternion/terrain/POI admission'],historical_cache_correspondence='UNOBSERVED',inputs=before,center=center,origin=origin,system=system,index=index,pattern=dict(seed=selected['seed'],words=selected['draw_count'],sha256=selected['words_sha256']),halo={k:v for k,v in halo.items() if k!='sources'},constants=scalars,sources=results,fixed_queries=fixed)
args.output.open('x',encoding='utf8',newline='\n').write(json.dumps(out,indent=2)+'\n')
print('fixed lattice positives',sum(bool(x['resources']) for x in fixed),'negatives',sum(not x['resources'] for x in fixed))
