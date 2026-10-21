from pathlib import Path
import sys,json,struct,zlib,zipfile,hashlib
R=Path.cwd();W=R/'.local-work/coordinate-sufficiency';sys.path.insert(0,str(R/'save-analysis/scripts'))
from inventory_historical_saves import guard
from stream_save import decoded_save
from planet_world_key import find_unit3_context,unit3_world_descriptors
from inspect_outpost_definitions import subrecords,esm_records
from beacon_terrain_projection import grid_cell,grid_centre,to_square
from position_quantizer_diagnostic import diagnose
seed=json.loads((W/'baseline.json').read_text());paths={Path(x['path']).name:Path(x['path']) for x in seed['protected']};guard()
def write(p,x):p.open('x',encoding='utf8',newline='\n').write(json.dumps(x,indent=2)+'\n')
out={}
with zipfile.ZipFile(paths['ContentResources.zip']) as z:
 for n in z.namelist():
  if n.lower() in ['scripts/source/game.psc','scripts/source/objectreference.psc','scripts/source/actor.psc','scripts/source/location.psc']:
   b=z.read(n);out[n]=dict(sha256=hashlib.sha256(b).hexdigest(),text=b.decode('utf-8-sig'))
write(W/'papyrus-sources.json',out)
esm=paths['Starfield.esm'];off=1402105313
with esm.open('rb') as f:
 f.seek(off);h=f.read(24);assert h[:4]==b'PNDT' and struct.unpack_from('<I',h,12)[0]==0x3f59f
 n,flags=struct.unpack_from('<II',h,4);raw=f.read(n);payload=zlib.decompress(raw[4:]) if flags&0x40000 else raw
 if flags&0x40000:assert len(payload)==int.from_bytes(raw[:4],'little')
 fs=list(subrecords(payload));entries=[]
 for tag,data in fs:
  if tag==b'BDST':break
  if tag!=b'CNAM':continue
  assert len(data)%20==0
  marker=b'CNAM'+struct.pack('<H',len(data))+data;relative=payload.index(marker)+6
  for q in range(0,len(data),20):
   lat,lon,world=struct.unpack_from('<ddI',data,q)
   entries.append(dict(pair_payload_offset=relative+q,latitude=lat,longitude=lon,world=f'{world:08X}',disk_hex=data[q:q+20].hex(),cell=grid_cell(lon,lat),diagnostic=diagnose(lon,lat)))
links=[]
for rec,fs in esm_records(esm,{b'WRLD',b'LCTN'},repeated=True):
 if rec['formid'] not in (0x325868,0x28a08):continue
 links.append(dict(record=rec,fields=[(t.decode(),b.hex()) for t,b in fs if t in (b'EDID',b'FULL',b'WCTR',b'WNAM',b'PNAM',b'NAM2',b'LCNL',b'LNAM',b'XLCN',b'CNAM')]))
write(W/'fixed.json',dict(record_file_offset=off,header=h.hex(),entries=entries,links=links))
for label in ['37','38','39','25']:
 x=json.loads((W/('Save'+label+'.json')).read_text());p=Path(x['source']['path'])
 with decoded_save(p,W/'scratch',seconds=float('inf')) as (b,m):
  d=x['extraction']['directory'];a=d['regions']['region_R1'][0];u4=x['extraction']['global_units']['4'][0]-8
  ctx=find_unit3_context(b,a,u4);descs,end=unit3_world_descriptors(b,ctx)
 write(W/('Save'+label+'-descriptors.json'),dict(context=ctx,descriptors=descs,end=end))
print('sources',list(out),'fixed',entries,'links',links)
