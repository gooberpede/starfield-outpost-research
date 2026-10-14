"""Original bounded executable literal leads; stdlib PE section mapping only.
Reads installed pinned executable, writes exclusive local receipt. No effects.
Literal proximity is a lead, not semantics. Hash verified before/after.
"""
import struct,json,hashlib
from pathlib import Path
p=Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield/Starfield.exe');b=p.read_bytes();sha=hashlib.sha256(b).hexdigest();assert sha=='7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28'
pe=struct.unpack_from('<I',b,0x3c)[0];n=struct.unpack_from('<H',b,pe+6)[0];sz=struct.unpack_from('<H',b,pe+20)[0];sections=[]
for j in range(n):
 a=pe+24+sz+40*j;vs,va,rawsz,raw=struct.unpack_from('<4I',b,a+8);sections.append((raw,rawsz,va))
rows=[]
for needle in [b'OutpostBeacon',b'WorkshopBeacon',b'WorkshopRefType']:
 start=0
 while True:
  a=b.find(needle,start)
  if a<0:break
  end=b.find(b'\0',a);text=b[a:end].decode('ascii',errors='replace');va=next((0x140000000+v+a-r for r,s,v in sections if r<=a<r+s),None);rows.append(dict(offset=a,va=f'{va:x}' if va else None,literal=text));start=a+1
assert hashlib.sha256(p.read_bytes()).hexdigest()==sha
with Path('.local-work/workshop-population-rework/specialist/location-literals26.json').open('x',encoding='utf8') as f:json.dump(dict(source=str(p),sha256=sha,rows=rows),f,indent=2)
print(rows)
