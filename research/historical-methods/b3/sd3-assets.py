"""Original bounded SWF metadata reader, owned BA2 framing. Extracts only
OrganicIcons SWF locally; reports SymbolClass IDs and definition tag metadata.
No artwork rendering or binary incorporation; installed input is read-only."""
from pathlib import Path
import json,struct,zlib,hashlib
R=Path.cwd();W=R/'.local-work/sd3-stored'
def digest(b):return hashlib.sha256(b).hexdigest()
p=Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield/Data/Starfield - Interface.ba2')
with p.open('rb') as f:
 magic,version,kind,n,names=struct.unpack('<4sI4sIQ',f.read(24));assert (magic,version,kind)==(b'BTDX',2,b'GNRL')
 f.seek(32);entries=[struct.unpack('<I4sIIQIII',f.read(36)) for _ in range(n)]
 f.seek(names);fn=[f.read(int.from_bytes(f.read(2),'little')).decode() for _ in range(n)]
 idx=fn.index('interface/organicicons.swf');_,_,_,_,off,packed,size,_=entries[idx];f.seek(off);b=f.read(packed or size)
 if packed:b=zlib.decompress(b)
 assert len(b)==size;(W/'OrganicIcons.swf').open('xb').write(b)
def tags(b,start,end):
 pos=start
 while pos<end:
  at=pos;h=int.from_bytes(b[pos:pos+2],'little');pos+=2;k,n=h>>6,h&63
  if n==63:n=int.from_bytes(b[pos:pos+4],'little');pos+=4
  assert pos+n<=end
  yield at,k,b[pos:pos+n];pos+=n
def movie(path):
 raw=path.read_bytes();b=raw if raw[:3]==b'FWS' else raw[:8]+zlib.decompress(raw[8:]);assert len(b)==int.from_bytes(b[4:8],'little')
 start=8+(5+4*(b[8]>>3)+7)//8+4;symbols=[];definitions=[];imports=[]
 for at,k,payload in tags(b,start,len(b)):
  if k in (76,56):
   pos=2
   for _ in range(int.from_bytes(payload[:2],'little')):
    cid=int.from_bytes(payload[pos:pos+2],'little');pos+=2;end=payload.index(0,pos);name=payload[pos:end].decode();pos=end+1;symbols.append(dict(tag=k,id=cid,name=name,offset=at))
  if k in (2,22,32,83,39,87,10,48,75):definitions.append(dict(tag=k,id=int.from_bytes(payload[:2],'little'),offset=at,bytes=len(payload),sha256=digest(payload)))
  if k in (57,71):imports.append(dict(tag=k,offset=at,payload_hex=payload.hex()))
 return dict(path=str(path),sha256=digest(raw),symbols=symbols,definitions=definitions,imports=imports)
out=dict(organic=movie(W/'OrganicIcons.swf'),locations=movie(W/'LocationsPage.swf'))
(W/'assets01.json').open('x',encoding='utf8').write(json.dumps(out,indent=2)+'\n')
print('organic symbols',len(out['organic']['symbols']));print([(s['name'],s['id']) for s in out['organic']['symbols'] if any(n in s['name'].lower() for n in ('adhes','frame','amino','generic','analges'))])
