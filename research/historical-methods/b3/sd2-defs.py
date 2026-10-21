"""SD2 original physical definition reader; owned catalog/ESM framing.
Reads pinned main index/ESM, installed SFBGS00D.esm and its script archives.
Writes exclusive local-only receipts; no installed/source changes or execution."""
from pathlib import Path
import sys,json,struct,zlib,re
R=Path.cwd();W=R/'.local-work/sd2-shared';sys.path.insert(0,str(R/'research/s1-storage'))
from catalog import pin,field,fields,words
from inspect_outpost_definitions import esm_records,subrecords
from inventory_historical_saves import guard
guard();D=Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield/Data');p=D/'SFBGS00D.esm';before=pin(p);rs=[]
class AllTags:
 def __contains__(self,k):return True
for h,fs in esm_records(p,AllTags(),repeated=True):
 rs.append(dict(**h,edid=next((v.rstrip(b'\0').decode('utf8') for k,v in fs if k==b'EDID'),''),fields=[(k.decode(),v.hex()) for k,v in fs]))
assert pin(p)==before
hits=[r for r in rs if re.search('shared|outpost.*storage',r['edid'],re.I)]
deps=set()
for r in hits:
 for k,v in r['fields']:
  b=bytes.fromhex(v)
  if k in ('KWDA','CNAM','BNAM','FNAM','LNAM') and len(b)%4==0:deps.update(x[0] for x in struct.iter_unpack('<I',b))
main=json.loads((R/'.local-work/e2-organic/inventory02.json').read_text());assert pin(D/'Starfield.esm')==main['source']
selected=[r for r in rs if r in hits or r['formid'] in deps or r['type']=='TES4']
selectedmain=[r for r in main['records'] if r['formid'] in deps or r['type']=='COBJ' and re.search('Outpost.*(Storage|Fabricator|Greenhouse|Transfer)|Research',r['edid'],re.I)]
# Physically validate every selected cache record, including compressed framing.
with (D/'Starfield.esm').open('rb') as f:
 for r in selectedmain:
  f.seek(r['offset']);h=f.read(24);n,flags,fid=struct.unpack_from('<III',h,4);assert(h[:4].decode(),fid)==(r['type'],r['formid']);b=f.read(n)
  if flags&0x40000:
   size=int.from_bytes(b[:4],'little');b=zlib.decompress(b[4:]);assert len(b)==size
  assert [(k.decode(),v.hex()) for k,v in subrecords(b)]==[tuple(x) for x in r['fields']]
assert pin(D/'Starfield.esm')==main['source']
(W/'definitions01.json').open('x',encoding='utf8').write(json.dumps(dict(addon_source=before,addon_records=selected,main_source=main['source'],main_records=selectedmain,physical_main_rereads=len(selectedmain)),indent=2)+'\n')
for r in selected:
 print(r['type'],hex(r['formid']),r['edid'],r['fields'] if r in hits else '',flush=True)
print('MAIN',len(selectedmain));guard()
