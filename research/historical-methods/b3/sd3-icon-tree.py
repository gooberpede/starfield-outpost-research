"""Owned L2 timeline-reader adaptation, bounded icon instance metadata only.
Reads local Locations SWF; writes local metadata, never renders/extracts artwork."""
from pathlib import Path
import struct,zlib,json
W=Path('.local-work/sd3-stored');raw=(W/'LocationsPage.swf').read_bytes();b=raw[:8]+zlib.decompress(raw[8:]);start=8+(5+4*(b[8]>>3)+7)//8+4
sprites={};hits=[];names=('OrganicIcon_mc','InorganicIcon_mc','Icon_mc','ResourceName_tf','BackgroundColor_mc','Symbol_mc','Text_tf','Rarity_mc')
def tags(lo,hi,owner):
 p=lo;out=[]
 while p<hi:
  off=p;h=int.from_bytes(b[p:p+2],'little');p+=2;kind,n=h>>6,h&63
  if n==63:n=int.from_bytes(b[p:p+4],'little');p+=4
  assert p+n<=hi;v=b[p:p+n];out.append(dict(kind=kind,offset=off,bytes=n))
  if kind==39:
   ident,frames=struct.unpack_from('<HH',v);sprites[str(ident)]=dict(id=ident,frames=frames,offset=off,tags=tags(p+4,p+n,ident))
  if kind in (26,70):
   for name in names:
    if name.encode()+b'\0' not in v:continue
    at=3 if kind==26 else 4
    if kind==70 and (v[1]&8 or (v[1]&16 and v[0]&2)):at=v.index(0,at)+1
    hits.append(dict(owner=owner,kind=kind,offset=off,flags=v[0],character=int.from_bytes(v[at:at+2],'little') if v[0]&2 else None,name=name))
  p+=n
 assert p==hi;return out
tags(start,len(b),'root')
(W/'icon-tree01.json').open('x').write(json.dumps(dict(bindings=hits,sprites=sprites),indent=2)+'\n')
print([h for h in hits if h['owner']==53])
