"""Exact native153 type2 target triples for fully matching member cohorts.
Only two observed positive fingerprint saves from completed05. Stdlib/project,
readonly originals; exclusive numeric receipt; before/after identity and guards.
"""
import sys,json,struct
from pathlib import Path
sys.path.insert(0,'save-analysis/scripts')
from inventory_historical_saves import identity,guard
from stream_save import decoded_save
from workshop_global_units import global_units
from outpost_record_framing import Reader
base=Path('.local-work/workshop-population-rework');out=base/'specialist';guard()
inputs=[out/'historical-targetcensus05.jsonl',out/'historical-targetcensus05-summary.json',base/'type2-probe01.json',Path(__file__)]
pins=[identity(p) for p in inputs];samples=[json.loads(l) for l in inputs[0].read_text().splitlines()];summary=json.loads(inputs[1].read_text());old=json.loads(inputs[2].read_text());targets=set(summary['groups'])|set(summary['DA_members'])|set(summary['owners'])|{r['target'] for r in json.loads((base/'nonowner-relations01.json').read_text())['rows']}
expected={f'DYNAMIC:{r["saved_id"]}':r['components'] for x in old if x['label']=='Save52' for r in x['rows'] if f'DYNAMIC:{r["saved_id"]}' in targets};assert len(targets)==171
results=[]
for x in samples:
 if x['inventory_id'] not in ('HIST-0210','HIST-0267'):continue
 pin=x['source'];assert identity(Path(pin['path']))==pin
 with decoded_save(Path(pin['path']),out/'resource-scratch15') as (b,metrics):
  assert b[0x14]==153
  unit=next(r for r in global_units(b) if r['type']==2);c=Reader(b,unit['out_of_line_pointer'],len(b));header=struct.unpack('<3I',c.take(12));blobs=[]
  for _ in range(4):n=int.from_bytes(c.take(4),'little');blobs.append(c.take(n))
  arrays=[]
  for raw in blobs[:3]:
   n=int.from_bytes(raw[:4],'little');assert len(raw)==4+4*n and n==header[2];arrays.append(raw)
  raw=blobs[3];n=int.from_bytes(raw[:4],'little');assert len(raw)==4+8*n
  selected=[];index=0
  for start,count in struct.iter_unpack('<II',raw[4:]):
   for fid in range(start,start+count):
    ident=f'DYNAMIC:{fid:08x}'
    if ident in targets:
     triple=[struct.unpack_from('<I',a,4+4*index)[0] for a in arrays];selected.append(dict(identity=ident,resource_ID=triple,Save52_resource_ID=expected[ident],exact_match=triple==expected[ident],array_index=index))
    index+=1
  assert index==header[2] and len(selected)==len(expected)
  results.append(dict(inventory_id=x['inventory_id'],source=pin,decode=metrics,unit=unit,header=header,end=c.p,target_rows=selected,exact_matches=sum(r['exact_match'] for r in selected)))
 assert identity(Path(pin['path']))==pin
assert [identity(p) for p in inputs]==pins
with (out/'historical-resource15.json').open('x',encoding='utf8') as f:json.dump(dict(schema='historical-exact-resource-triple/1',inputs=pins,results=results,limits='Full BSResource::ID equality corroborates identity continuity; it does not create missing physical records or recover an owner edge.'),f,indent=2);f.write('\n')
print([(x['inventory_id'],len(x['target_rows']),x['exact_matches']) for x in results])
