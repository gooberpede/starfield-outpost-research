import sys,json,struct,collections
from pathlib import Path
sys.path.insert(0,'save-analysis/scripts')
from stream_save import decoded_save
from inventory_historical_saves import identity,guard
from outpost_record_framing import Reader
out=Path('.local-work/workshop-population-rework');guard();inputs=json.loads((out/'global-census01.json').read_text());results=[]
targets=[0xff000000|(int(t,16)&0x3fffff) for t in ['81b59b','81ca6e','823948','82437e','827530','82a828','82d5ec','82d607','841343','85d48a']]
for item in inputs:
 pin=item['source'];assert identity(Path(pin['path']))==pin
 with decoded_save(Path(pin['path']),out/'scratch') as (b,metrics):
  unit=next(r for r in item['units'] if r['type']==2);c=Reader(b,unit['out_of_line_pointer'],len(b));header=struct.unpack('<3I',c.take(12));blobs=[]
  for i in range(4):
   n=int.from_bytes(c.take(4),'little');at=c.p;raw=c.take(n);blobs.append(dict(index=i,offset=at,size=n,head=raw[:40].hex()))
  arrays=[]
  for blob in blobs[:3]:
   raw=b[blob['offset']:blob['offset']+blob['size']];n=int.from_bytes(raw[:4],'little');assert len(raw)==4+4*n;arrays.append(list(struct.unpack_from('<'+'I'*n,raw,4)))
  blob=blobs[3];raw=b[blob['offset']:blob['offset']+blob['size']];n=int.from_bytes(raw[:4],'little');assert len(raw)==4+8*n
  ids=[fid for a,n in struct.iter_unpack('<II',raw[4:]) for fid in range(a,a+n)]
  assert all(len(a)==header[2] for a in arrays) and len(ids)==header[2]
  rows=[dict(saved_id=f'{fid:08x}',components=[a[i] for a in arrays]) for i,fid in enumerate(ids)]
  results.append(dict(label=item['label'],source=pin,header=header,blobs=blobs,end=c.p,rows=rows,target_matches=[r for r in rows if int(r['saved_id'],16) in targets]))
  print(item['label'],header,'rows',len(rows),'targets',results[-1]['target_matches'],flush=True)
 assert identity(Path(pin['path']))==pin
(out/'type2-probe01.json').open('x',encoding='utf8').write(json.dumps(results,indent=2)+'\n')
