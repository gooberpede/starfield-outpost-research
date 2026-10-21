"""Read missing selected template bases and PTST records at actual ESM headers.
Writes ignored JSON; original unchanged. No target or other mutations.
"""
from pathlib import Path
import json,sys,struct,zlib
R=Path.cwd();W=R/'.local-work/construction-variants';sys.path[:0]=[str(R/'research/s1-storage'),str(R/'save-analysis/scripts')]
from catalog import pin
from inspect_outpost_definitions import subrecords
from inventory_historical_saves import guard
guard();j=json.loads((W/'definitions02.json').read_text());known={r['formid'] for r in j['records']};ts=json.loads((W/'templates02.json').read_text())['records'];wanted={r['base'] for r in ts}-known
wanted|={0x2389ae,0x178a46};esm=Path(j['source']['path']);assert pin(esm)==j['source'];out=[];p=0
with esm.open('rb') as f:
 while p<esm.stat().st_size:
  f.seek(p);h=f.read(24);n,flags,fid=struct.unpack_from('<III',h,4);tag=h[:4]
  if tag==b'GRUP':p+=24;continue
  if fid in wanted or tag==b'PTST':
   b=f.read(n)
   if flags&0x40000:sz=int.from_bytes(b[:4],'little');b=zlib.decompress(b[4:]);assert len(b)==sz
   fs=[(k.decode(),v.hex()) for k,v in subrecords(b)];edid=next((bytes.fromhex(v).rstrip(b'\0').decode() for k,v in fs if k=='EDID'),'')
   out.append(dict(offset=p,type=tag.decode(),formid=fid,flags=flags,edid=edid,fields=fs))
  p+=24+n
assert pin(esm)==j['source']
(W/'extra-definitions01.json').open('x',encoding='utf8').write(json.dumps(dict(source=j['source'],missing_base_ids=sorted(wanted),records=out),indent=2)+'\n')
print('extra records',len(out),'missing',wanted-{r['formid'] for r in out})
