"""Original B1 offline demonstrator. Reads pinned map/save receipts only; writes
exclusive local JSON. Applies the accepted conditional ordinary frame model;
does not invoke native code, reproduce visual blending or predict loaded state.
"""
from pathlib import Path
import sys,json,struct,math,collections,hashlib
R=Path.cwd();W=R/'.local-work/outpost-biomes';sys.path.insert(0,str(R/'save-analysis/scripts'))
from beacon_terrain_projection import grid_cell,f32,split_local
def pin(p):
 p=Path(p)
 with p.open('rb') as f:return dict(path=str(p.resolve()),bytes=p.stat().st_size,sha256=hashlib.file_digest(f,'sha256').hexdigest())
def readmap(path):
 b=path.read_bytes();v,flag,n=struct.unpack_from('<BBI',b);assert v==5
 ids=struct.unpack_from('<'+str(n)+'I',b,6);p=6+4*n;nf=struct.unpack_from('<I',b,p)[0];p+=4;assert nf==2
 faces=[]
 for face in range(nf):
  width,height,count=struct.unpack_from('<III',b,p);p+=12;assert width*height==count and width and height
  off=p;values=struct.unpack_from('<'+str(count)+'I',b,p);p+=4*count
  maskcount=struct.unpack_from('<I',b,p)[0];p+=4;assert maskcount==count;maskoff=p;p+=maskcount
  faces.append(dict(width=width,height=height,offset=off,values=values,maskoffset=maskoff,mask=list(b[maskoff:p])))
 assert p==len(b);return dict(version=v,flag=flag,catalog=ids,faces=faces)
def lookup(m,t,i,j):
 # Native 14078d660 cell-center chart, 14078ee90 reflection, 1423390f0 raster.
 u=(i+.5)/49152-.5;v=(j+.5)/49152-.5
 if t in (2,3):t=int(t!=2);u=-u;v=-v
 face=m['faces'][t];w,h=face['width'],face['height'];a=min(w-1,max(0,math.floor(min(1,max(0,u+.5))*w)));b=min(h-1,max(0,math.floor((1-min(1,max(0,v+.5)))*h)))
 return face['values'][b*w+a],(t,a,b),face['offset']+4*(b*w+a)
def enumerate_cells(cx,cy,r=150):
 out=[]
 for qy in range(math.floor((cy-r)/100)-1,math.floor((cy+r)/100)+2):
  for qx in range(math.floor((cx-r)/100)-1,math.floor((cx+r)/100)+2):
   dx=max(qx*100-cx,0,cx-(qx+1)*100);dy=max(qy*100-cy,0,cy-(qy+1)*100);d2=dx*dx+dy*dy
   if d2<r*r:out.append((qx,qy,d2))
 return out
maps={body:readmap(W/name) for body,name in [(0x3f59f,'kreet.biom'),(0x5e0de,'feynman v.biom'),(0x5e4da,'carinae iii-a.biom')]}
rows=[];inputs=[]
for label in ['HIST-0035','HIST-0210','HIST-0267','Kreet25','Kreet39','Kreet31','Kreet33']:
 path=W/(label+'-r3.json');x=json.loads(path.read_text());inputs.append(pin(path))
 for b in x['extraction']['beacons']:
  body=b['proposed_body_formid'];names=[n['text'] for n in b['name_for_comparison']];name=names[0] if names else 'UNNAMED'
  if body is None and x.get('worlds',{}):
   joined=[v for v in x['worlds'].get('rows',[]) if v['world']==b['parent_token']]
   if len(joined)==1 and len(b['points'])==1 and int(joined[0]['body'],16)==b['points'][0]['body_formid']:body=int(joined[0]['body'],16)
  if body not in maps or (label.startswith('HIST') and name not in ['Carinae III-a Rc Fe','Feynman V Cu Co Ni IL','Feynman V Cu IL F']):continue
  wp=b.get('workshop');assert wp and wp['delta_hex']=='000000000000000000000000';C=b['local_xyz'];frame=b['initial_flag'];site=grid_cell(*b['points'][0]['pair']);desc=None;world=None
  if x.get('worlds',{}):
   world,=[a for a in x['worlds']['rows'] if a['world']==b['parent_token']]
   desc,=[a for a in x['descriptors']['descriptors'] if a['world_token']==world['secondary'] and a['body']==world['body']]
  if frame==0xb:
   assert desc is not None;t=desc['tag'];base=[desc['x'],desc['y']]
   if t in (2,3):base=[49151-v for v in base]
  elif frame==0x2b:
   t,*base=site;assert t in (0,1)
  else:raise ValueError('UNQUALIFIED_FRAME')
  cells=[];m=maps[body]
  for qx,qy,d2 in enumerate_cells(*C[:2]):
   i=base[0]+qx;j=base[1]+qy;assert 0<=i<49152 and 0<=j<49152,'SEAM_NOT_TESTED_HERE'
   fid,pixel,off=lookup(m,t,i,j);cells.append(dict(q=[qx,qy],cell=[t,i,j],biome=f'{fid:08x}',pixel=pixel,map_byte_offset=off,min_distance_squared=d2))
  q=[split_local(v)[0] for v in C[:2]];actual=[t,base[0]+q[0],base[1]+q[1]]
  # Independent integer raster-address cross-check for all examined fine cells.
  for c in cells:
   tt,i,j=c['cell'];assert tt in (0,1);face=m['faces'][tt];assert face['width']==face['height']==256
   col=i//192;row=255-j//192;assert list(c['pixel'])==[tt,col,row]
   raw=(W/('kreet.biom' if body==0x3f59f else 'feynman v.biom' if body==0x5e0de else 'carinae iii-a.biom')).read_bytes()
   assert int.from_bytes(raw[c['map_byte_offset']:c['map_byte_offset']+4],'little')==int(c['biome'],16)
  margin=min(abs(math.sqrt(c['min_distance_squared'])-150) for c in cells)
  # Also calculate rejection-side margin, so near-outside cells cannot be hidden.
  for qy in range(math.floor((C[1]-150)/100)-1,math.floor((C[1]+150)/100)+2):
   for qx in range(math.floor((C[0]-150)/100)-1,math.floor((C[0]+150)/100)+2):
    dx=max(qx*100-C[0],0,C[0]-(qx+1)*100);dy=max(qy*100-C[1],0,C[1]-(qy+1)*100);margin=min(margin,abs(math.hypot(dx,dy)-150))
  assert margin>.001
  row=dict(sample=label,save=x['source'],decoded_sha256=x['metrics']['decoded_sha256'],name=name,token=b['token'],parent=b['parent_token'],record_offset=b['record']['offset'],xyz_offset=b['xyz_offset'],body=f'{body:08x}',frame=f'{frame:02x}',center=C,workshop=wp,site=list(site),world=world,descriptor=desc,base=[t,*base],center_cell=actual,cells=cells,biomes=sorted({c['biome'] for c in cells}),numeric_boundary_margin=margin,coverage='CONDITIONAL_SAVED_FRAME_ORDINARY_BASE_BIOME')
  rows.append(row);print(label,name,'base',row['base'],'center',actual,'cells',len(cells),'biomes',row['biomes'],'margin',margin)
# Mathematical controls challenge centre/boundary-only sampling and tangencies.
checks={}
disk=enumerate_cells(150,150,150);checks['enclosed_cell_included']=(1,1) in [(x,y) for x,y,d in disk]
checks['enclosed_cell_no_circle_boundary']=max(math.hypot(x-150,y-150) for x in (100,200) for y in (100,200))<150
checks['tangent_cell_excluded']=not any(x==3 and y==1 for x,y,d in disk)
checks['negative_floor_included']=any(x==-2 for x,y,d in enumerate_cells(-.1,0))
checks['strict_small_cap_included']=any(x==2 and y==0 for x,y,d in enumerate_cells(50.00001,50))
checks['strict_small_gap_excluded']=not any(x==2 and y==0 for x,y,d in enumerate_cells(49.99999,50))
for body,m in maps.items():
 for t in (0,1):
  for i,j in [(0,0),(191,191),(192,192),(49151,49151),(25124,32448)]:
   a=lookup(m,t,i,j);tt,xx,yy=a[1];checks[f'raster-{body:x}-{t}-{i}-{j}']=(xx==i//192 and yy==255-j//192)
 # Reflected chart normalization must match mirrored integer centre indices.
 for t,normal in [(2,0),(3,1)]:checks[f'reflection-{body:x}-{t}']=lookup(m,t,120,456)[0]==lookup(m,normal,49031,48695)[0]
assert all(checks.values()),checks
(W/'model-r2.json').open('x',encoding='utf8').write(json.dumps(dict(rows=rows,checks=checks,inputs=inputs,tool=pin(__file__)),indent=2)+'\n')
print('PASS mathematical checks',len(checks))
