"""Fresh bounded physical main-ESM census, owned framing method. Reads installed
ESM; writes exclusive ignored JSON, no target/analysis edits. Stdlib only.
Selected payloads <=16MiB, strict compressed closure, original hashes pre/post.
"""
from pathlib import Path
import sys,json,struct,zlib,collections
R=Path.cwd();W=R/'.local-work/build-catalogue'
sys.path.insert(0,str(R/'save-analysis/scripts'));sys.path.insert(0,str(R/'research/s1-storage'))
from inventory_historical_saves import guard
from inspect_outpost_definitions import subrecords
from catalog import pin
guard();baseline=json.loads((W/'baseline.json').read_text());src=Path(next(p['path'] for p in baseline['protected'] if p['path'].endswith('Starfield.esm')));before=pin(src);assert before in baseline['protected']
wanted={'COBJ','FLST','KYWD','DFOB','FURN','GLOB','AVIF','IRES','PKIN','CONT','RSPJ'};rs=[];counts=collections.Counter();p=0;total=src.stat().st_size;stack=[total]
with src.open('rb') as f:
 while p<total:
  while p==stack[-1] and len(stack)>1:stack.pop()
  assert p+24<=stack[-1];f.seek(p);h=f.read(24);t=h[:4].decode();n,flags,fid=struct.unpack_from('<III',h,4);end=p+(n if t=='GRUP' else n+24);assert p+24<=end<=stack[-1];counts[t]+=1
  if t=='GRUP':stack.append(end);p+=24;continue
  if t in wanted:
   assert n<=16*1024*1024;b=f.read(n)
   if flags&0x40000:
    size=int.from_bytes(b[:4],'little');assert size<=16*1024*1024;d=zlib.decompressobj();b=d.decompress(b[4:],size+1);assert len(b)==size and d.eof and not d.unused_data and not d.unconsumed_tail
   fs=[(t.decode(),v.hex()) for t,v in subrecords(b)];edid=next((bytes.fromhex(v).rstrip(b'\0').decode('utf8') for t,v in fs if t=='EDID'),'');rs.append(dict(offset=p,type=t,formid=fid,flags=flags,edid=edid,fields=fs))
  p=end
assert p==total and all(e==total for e in stack);assert pin(src)==before
(W/'definitions.json').open('x',encoding='utf8').write(json.dumps(dict(source=before,selected_types=sorted(wanted),counts=counts,records=rs),indent=2)+'\n')
print('PASS fresh census',len(rs),'selected records',len([r for r in rs if r['type']=='COBJ']),'COBJ')
