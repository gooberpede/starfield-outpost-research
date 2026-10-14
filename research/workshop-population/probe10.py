# Original read-only save type-run census, exclusive ignored output. Existing decoder scratch removed.
import json,sys,collections,struct
from pathlib import Path
sys.path.insert(0,str(Path.cwd()/'save-analysis/scripts'))
from stream_save import decoded_save
from validate_mature_outposts import directory
from outpost_record_framing import Reader,iter_records
from inventory_historical_saves import identity
rows=[];mapping=bytes.fromhex('4a4b4c4e4f50495a5b321e1f22232425262728292c2f3031353637390c0d5d5784177f88758755535169333f604d1b3e9a0e34ae425254b7bebdd8')
assert len(mapping)==59
for s in json.loads(Path('.local-work/workshop-population-rework/regions01.json').read_text()):
 path=Path(s['source']['path']);before=identity(path);assert before==s['source']
 with decoded_save(path,Path('.local-work/workshop-population-rework/specialist/scratch')) as (b,metrics):
  d=directory(b);d['auxiliary_words']=list(struct.unpack_from('<15I',b,d['offset']+40));at=d['auxiliary_words'][1];c=Reader(b,at,len(b));n=c.count();ts=[]
  for i in range(n):
   t=c.take(1)[0];count=c.count();assert t<len(mapping);ts.append(dict(change_type=t,form_type=mapping[t],count=count))
  assert sum(t['count'] for t in ts)==d['words'][9]
  count=collections.Counter();dynamic=collections.Counter();runs=iter(ts);run=next(runs);remaining=run['count'];examples={}
  for r in iter_records(b,*d['regions']['region_R3'],d['words'][9]):
   while remaining==0:run=next(runs);remaining=run['count']
   remaining-=1;ft=run['form_type'];count[ft]+=1
   if int(r['token'],16)>>22==2:dynamic[ft]+=1
   examples.setdefault(ft,dict(token=r['token'],offset=r['offset']))
  assert remaining==0
  rows.append(dict(label=s['label'],source=before,decode=metrics,directory=d,format_version=int.from_bytes(b[16:20],'little'),buffer_version=b[20],type_table=dict(offset=at,end=c.p,runs=ts,total=sum(t['count'] for t in ts)),form_counts=[dict(form_type=k,count=v,dynamic=dynamic[k],example=examples[k]) for k,v in sorted(count.items())]))
  print(s['label'],at,n,'sum',sum(count.values()),'REFR',count[0x4a],dynamic[0x4a],'ACHR',count[0x4b],dynamic[0x4b],flush=True)
 assert identity(path)==before
Path('.local-work/workshop-population-rework/specialist/header-type-table03.json').open('x',encoding='utf8').write(json.dumps(rows,indent=2))
