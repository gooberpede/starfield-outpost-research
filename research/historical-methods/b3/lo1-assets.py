"""Owned SD3 timeline reader adaptation: immutable local SWF, symbol/frame and
named instance metadata only. No movie execution, renderer or artwork export."""
from pathlib import Path
import struct,zlib,json,hashlib
W=Path('.local-work/lo1-locations');S=Path('.local-work/sd3-stored');raw=(S/'LocationsPage.swf').read_bytes();b=raw if raw[:3]==b'FWS' else raw[:8]+zlib.decompress(raw[8:]);assert len(b)==int.from_bytes(b[4:8],'little')
start=8+(5+4*(b[8]>>3)+7)//8+4;sprites={};hits=[]
names=('BuildLimitMeter_mc','FactionIcon_mc','Galaxy2DMap_mc','Galaxy2DMapMC','SystemViewHolder_mc','SystemViewHolderMC','SystemView_mc','Body_mc','Highlight_mc','OverviewInfoPanel_mc','OutpostView_mc','CargoLinks_mc','Crew_mc','NeededPower_mc','TotalPower_mc','Production_mc','LevelState_mc')
def tags(lo,hi,owner):
 p=lo;out=[];frame=1
 while p<hi:
  off=p;h=int.from_bytes(b[p:p+2],'little');p+=2;kind,n=h>>6,h&63
  if n==63:n=int.from_bytes(b[p:p+4],'little');p+=4
  assert p+n<=hi;v=b[p:p+n]
  if kind==1:frame+=1
  if kind==43:out.append(dict(frame=frame,label=v.split(b'\0')[0].decode('utf8'),offset=off))
  if kind==39:
   ident,frames=struct.unpack_from('<HH',v);sprites[str(ident)]=dict(id=ident,frames=frames,offset=off,labels=tags(p+4,p+n,ident),sha256=hashlib.sha256(v).hexdigest())
  if kind in (26,70):
   for name in names:
    if name.encode()+b'\0' not in v:continue
    at=3 if kind==26 else 4
    if kind==70 and (v[1]&8 or (v[1]&16 and v[0]&2)):at=v.index(0,at)+1
    hits.append(dict(owner=owner,kind=kind,offset=off,flags=v[0],character=int.from_bytes(v[at:at+2],'little') if v[0]&2 else None,name=name))
  p+=n
 assert p==hi;return out
tags(start,len(b),'root')
syms=json.loads((S/'assets01.json').read_text())['locations']['symbols']
(W/'assets01.json').open('x').write(json.dumps(dict(input_sha256=hashlib.sha256(raw).hexdigest(),bindings=hits,sprites=sprites,symbols=syms),indent=2)+'\n')
for h in hits:
 if h['name'] in ('BuildLimitMeter_mc','FactionIcon_mc','Body_mc','SystemView_mc','Highlight_mc'):print(h,'sprite',sprites.get(str(h['character'])))
