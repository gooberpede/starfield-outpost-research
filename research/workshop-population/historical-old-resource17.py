"""All96 older originals, exact type2 BSResource::ID continuity.
Native14180e450/e6c0 modern blob branch applies version>=0x47; all observed
older122/143 qualify that branch. No FormType map or script semantics transferred.
Read originals only; exclusive target-only receipts; full pins and40GB guards.
"""
import sys,json,struct,bisect,collections
from pathlib import Path
sys.path.insert(0,'save-analysis/scripts')
from inventory_historical_saves import identity,guard
from stream_save import decoded_save
from workshop_global_units import global_units
from outpost_record_framing import Reader
base=Path('.local-work/workshop-population-rework');out=base/'specialist';guard()
inputs=[out/'historical-targetcensus12.jsonl',out/'historical-targetcensus13.jsonl',out/'historical-resource15.json',out/'native30.tsv',out/'native31.tsv',Path(__file__)]
pins=[identity(p) for p in inputs];samples=[]
for p in inputs[:2]:samples.extend(x for x in map(json.loads,p.read_text().splitlines()) if x['status']=='FRAMING_ONLY_NULL_TYPE')
assert len(samples)==96 and len({x['source']['path'] for x in samples})==96
resource=json.loads(inputs[2].read_text());expected={r['identity']:r['resource_ID'] for r in resource['results'][0]['target_rows']};targets=sorted(int(s.split(':')[1],16) for s in expected);results=[]
with (out/'historical-old-resource17.jsonl').open('x',encoding='utf8') as dest:
 for x in samples:
  guard();pin=x['source'];assert identity(Path(pin['path']))==pin;r=dict(inventory_id=x['inventory_id'],source=pin,metadata=x['metadata'],status='PENDING')
  try:
   with decoded_save(Path(pin['path']),out/'old-resource-scratch17') as (b,metrics):
    assert b[0x14]>=0x47
    unit=next(r for r in global_units(b) if r['type']==2);c=Reader(b,unit['out_of_line_pointer'],len(b));header=struct.unpack('<3I',c.take(12));blobs=[]
    for _ in range(4):n=int.from_bytes(c.take(4),'little');blobs.append(c.take(n))
    for a in blobs[:3]:assert len(a)==4+4*header[2] and int.from_bytes(a[:4],'little')==header[2]
    raw=blobs[3];n=int.from_bytes(raw[:4],'little');assert len(raw)==4+8*n;index=0;selected=[]
    for start,count in struct.iter_unpack('<II',raw[4:]):
     assert start+count<=0x100000000
     left=bisect.bisect_left(targets,start);right=bisect.bisect_left(targets,start+count)
     for fid in targets[left:right]:
      ident=f'DYNAMIC:{fid:08x}';i=index+fid-start;triple=[struct.unpack_from('<I',a,4+4*i)[0] for a in blobs[:3]];selected.append(dict(identity=ident,resource_ID=triple,Save52_resource_ID=expected[ident],exact_match=triple==expected[ident],array_index=i))
     index+=count
    assert index==header[2]
    r.update(status='NATIVE_VERSION_BRANCH_TYPE2_CLOSED',buffer_version=b[0x14],unit=unit,header=header,decode=metrics,end=c.p,target_rows=selected,targets_present=len(selected),exact_matches=sum(s['exact_match'] for s in selected))
  except (ValueError,AssertionError,IndexError,KeyError) as error:r.update(status='RETAINED_TYPE2_GAP',error=str(error))
  assert identity(Path(pin['path']))==pin
  dest.write(json.dumps(r)+'\n');dest.flush();results.append({k:v for k,v in r.items() if k not in ('target_rows','decode','metadata')});print(x['inventory_id'],r['status'],r.get('targets_present'),r.get('exact_matches'),flush=True)
assert [identity(p) for p in inputs]==pins
with (out/'historical-old-resource17-summary.json').open('x',encoding='utf8') as f:json.dump(dict(inputs=pins,samples=results,status_counts=dict(collections.Counter(x['status'] for x in results)),target_count=171,scope='Numeric full resource triple continuity only; no oldFormType assignment and no ownership inferred from a triple.'),f,indent=2);f.write('\n')
