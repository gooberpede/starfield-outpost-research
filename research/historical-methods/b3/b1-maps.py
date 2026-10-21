"""B1 original bounded installed-source verification. Owned BA2 framing method:
research/c1-cargo/sources.py. Reads PlanetData BA2, main ESM, current native
exports; writes exclusive ignored selected map bytes/JSON. No target/save/DB
mutation, third-party implementation, download or external disclosure.
"""
from pathlib import Path
import sys,json,struct,zlib,hashlib,collections
R=Path.cwd();W=R/'.local-work/outpost-biomes'
sys.path.insert(0,str(R/'save-analysis/scripts'))
from inventory_historical_saves import guard
from inspect_outpost_definitions import esm_records
def pin(p):
 p=Path(p)
 with p.open('rb') as f:return dict(path=str(p.resolve()),bytes=p.stat().st_size,sha256=hashlib.file_digest(f,'sha256').hexdigest())
def write(p,x):p.open('x',encoding='utf8',newline='\n').write(json.dumps(x,indent=2)+'\n')
guard();D=Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield/Data')
arc=D/'Starfield - PlanetData.ba2';before=pin(arc);maps=[]
with arc.open('rb') as f:
 magic,version,kind,n,names=struct.unpack('<4sI4sIQ',f.read(24));assert (magic,version,kind)==(b'BTDX',2,b'GNRL')
 f.seek(32);entries=[struct.unpack('<I4sIIQIII',f.read(36)) for _ in range(n)];f.seek(names)
 filenames=[f.read(int.from_bytes(f.read(2),'little')).decode() for _ in range(n)]
 for i,name in enumerate(filenames):
  if name not in ['planetdata/biomemaps/'+s+'.biom' for s in ['kreet','feynman v','carinae iii-a']]:continue
  guard();_,_,_,_,off,packed,unpacked,_=entries[i];f.seek(off);b=f.read(packed or unpacked)
  if packed:
   z=zlib.decompressobj();b=z.decompress(b,unpacked+1);assert z.eof and not z.unused_data and not z.unconsumed_tail
  assert len(b)==unpacked
  out=W/(name.rsplit('/',1)[1]);out.open('xb').write(b)
  print(name,'bytes',len(b),'head',b[:64].hex())
  maps.append(dict(member=name,archive_record_index=i,archive_data_offset=off,packed=packed,unpacked=unpacked,local=pin(out)))
assert pin(arc)==before
write(W/'map-inputs.json',dict(archive=before,maps=maps,reader=pin(__file__)))
esm=D/'Starfield.esm';before=pin(esm);selected=[]
for rec,fs in esm_records(esm,{b'BIOM',b'PNDT',b'RSGD',b'RSCS'},repeated=True):
 if rec['type']=='PNDT' and rec['formid'] not in (0x3f59f,0x5e0de,0x5e4da):continue
 selected.append(dict(**rec,fields=[(t.decode(),b.hex()) for t,b in fs]))
assert pin(esm)==before;write(W/'definitions.json',dict(source=before,records=selected))
print('selected definitions',dict(collections.Counter(x['type'] for x in selected)))
