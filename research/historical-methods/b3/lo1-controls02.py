"""LO1 owned ESM/SD3 localization framing reuse. Physically reread finite
body/system/location/faction controls and English labels. Writes local JSON only."""
from pathlib import Path
import sys,json,struct,zlib,hashlib
R=Path.cwd();W=R/'.local-work/lo1-locations';sys.path.insert(0,str(R/'save-analysis/scripts'))
from inspect_outpost_definitions import esm_records
from inventory_historical_saves import guard
sys.path.insert(0,str(R/'research/s1-storage'));from catalog import pin
guard();base=json.loads((W/'baseline.json').read_text());p=Path(next(x['path'] for x in base['protected'] if x['path'].endswith('Starfield.esm')));before=pin(p)
ids={0x3f59f,0x5e0b5,0x5e5e8,0x5e630,0x615b0,0x61547,0x1b170,0x1b1d3,0x1b1cd,0x546df,0x638e5,0x3e4f4a,0x3e4f4b,0x137e5c};rows=[]
for r,fs in esm_records(p,{b'LCTN',b'FACT',b'STDT',b'PNDT',b'KYWD',b'DFOB'},repeated=True):
 if r['formid'] in ids:rows.append(dict(**r,fields=[(k.decode(),v.hex()) for k,v in fs]))
assert len(rows)==len(ids) and before==pin(p)
(W/'controls02.json').open('x',encoding='utf8').write(json.dumps(dict(source=before,records=rows),indent=2)+'\n')
ids={int.from_bytes(bytes.fromhex(v),'little') for r in rows for k,v in r['fields'] if k=='FULL'}
p=Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield/Data/Starfield - Localization.ba2');before=pin(p)
with p.open('rb') as f:
 magic,v,kind,n,names=struct.unpack('<4sI4sIQ',f.read(24));assert (magic,v,kind)==(b'BTDX',2,b'GNRL')
 f.seek(32);entries=[struct.unpack('<I4sIIQIII',f.read(36)) for _ in range(n)];f.seek(names);fn=[f.read(int.from_bytes(f.read(2),'little')).decode() for _ in range(n)]
 i=fn.index('strings/starfield_en.strings');off,packed,size=entries[i][4:7];f.seek(off);b=f.read(packed or size)
 if packed:b=zlib.decompress(b)
 assert len(b)==size;count,sz=struct.unpack_from('<II',b);start=8+8*count;assert start+sz==len(b);found={}
 for j in range(count):
  key,ofs=struct.unpack_from('<II',b,8+j*8)
  if key in ids:
   pos=start+ofs;end=b.index(0,pos);found[f'{key:08x}']=b[pos:end].decode('utf8')
assert before==pin(p) and len(found)==len(ids)
(W/'localization02.json').open('x',encoding='utf8').write(json.dumps(dict(source=before,member=fn[i],member_sha256=hashlib.sha256(b).hexdigest(),strings=found),indent=2)+'\n')
print('physical controls',len(rows),'localized',found);guard()
