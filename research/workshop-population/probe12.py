"""Original strict type4 census from native77/78; stdlib/project readers only.
Reads pinned saves and local receipts. Writes exclusive specialist JSON and
temporary decoded scratch cleaned by decoded_save. No source/target/DB effects.
Stops on failed pins, bounds, nonzero storage high byte, or nonclosure.
"""
import sys,json,struct,collections
from pathlib import Path
sys.path.insert(0,'save-analysis/scripts')
from inventory_historical_saves import identity,guard
from stream_save import decoded_save
from outpost_record_framing import Reader
from validate_mature_outposts import directory
from extractor_resources import plugin_tables,saved_form
from outpost_membership import token_value
base=Path('.local-work/workshop-population-rework');out=base/'specialist';guard()
paths=[base/'global-census01.json',base/'nonowner-da01.json',base/'reviewer-class-check06.json',base/'additional-roots01.json',base/'typed-full03/mature-Save52.json',Path('.local-work/workshop-inventory/final05/mature-Save52.json'),out/'native77.tsv',out/'native78.tsv',Path(__file__)]
pins=[identity(p) for p in paths]
global_=json.loads(paths[0].read_text());da=json.loads(paths[1].read_text());classes=json.loads(paths[2].read_text());additional=json.loads(paths[3].read_text());typed=json.loads(paths[4].read_text());old=json.loads(paths[5].read_text())
groups={r['identity'] for r in da['nonnull_groups'] if str(r['identity']).startswith('DYNAMIC:')}
missing={r['identity'] for r in da['nonnull_groups'] if r['identity'] in groups and not r['r3_record']}
parents={r['parent'] for r in classes['rows'] if r.get('parent')}
beacons={r['owner_identity'] for r in old['owners']}
roots={r['instance_identity'] for r in old['constructed_instances']}|{r['instance_identity'] for r in additional['additional_roots']}
members={r['identity'] for r in typed['keyword_queue_leads']}
targets={'DA_groups':groups,'missing_DA_groups':missing,'source_parents':parents,'beacons':beacons,'roots':roots,'explicit_members':members}
assert [len(x) for x in targets.values()]==[31,17,64,19,848,8628]
results=[]
for item in global_:
 pin=item['source'];assert identity(Path(pin['path']))==pin
 with decoded_save(Path(pin['path']),out/'scratch12') as (b,metrics):
  unit=next(r for r in item['units'] if r['type']==4);c=Reader(b,unit['body'],unit['end']);d=directory(b);a=d['regions']['reference_u32'][0];plugins=plugin_tables(b);refs=[]
  class Table:
   def __len__(self):return d['reference_count']
   def __getitem__(self,i):
    if not 0<=i<len(self):raise IndexError(i)
    return struct.unpack_from('<I',b,a+4+4*i)[0]
  def u(n):return int.from_bytes(c.take(n),'little')
  def ref(role):
   at=c.p;word=u(4);assert word>>24==0,('STORAGE_HIGH_BYTE',at,word)
   token=f'{word:06x}';r=dict(offset=at,word=word,token=token,identity=saved_form(token_value(token,Table()),plugins),role=role);refs.append(r);return r
  def color():
   at=c.p;n=u(4);return dict(offset=at,saved_count=n,colors=c.take(min(n,3)*12).hex())
  tables=[]
  n=u(4);rows=[]
  for ordinal in range(n):
   row=dict(ordinal=ordinal,offset=c.p,owner=ref('SpaceshipTemplate.owner'),index=u(2),template=ref('SpaceshipTemplate.template'));row['pairs']=[dict(left=ref('SpaceshipTemplate.pair.left'),right=ref('SpaceshipTemplate.pair.right')) for _ in range(u(8))];row['end']=c.p;rows.append(row)
  tables.append(dict(type='SpaceshipTemplate',count=n,rows=rows,end=c.p))
  n=u(4);rows=[]
  for ordinal in range(n):
   row=dict(ordinal=ordinal,offset=c.p,owner=ref('CustomShipComponent.owner'),index=u(2),first=ref('CustomShipComponent.first'),second=ref('CustomShipComponent.second'))
   k=u(4);row['saved_vector_count']=k;row['vector_words']=[u(4) for _ in range(min(k,3))];row['parts']=[]
   for j in range(u(4)):
    part=dict(offset=c.p,source=ref('CustomShipComponent.part.source'),transform=c.take(24).hex(),value=u(4),colors=color(),index=j);part['end']=c.p;row['parts'].append(part)
   size=u(4);row['name']=c.take(size).decode('utf8');row['final_value']=u(4);row['end']=c.p;rows.append(row)
  tables.append(dict(type='CustomShipComponent',count=n,rows=rows,end=c.p))
  assert c.p==c.end,('BODY_NONCLOSURE',c.p,c.end)
  matches={name:[r for r in refs if r['identity'] in vals] for name,vals in targets.items()} if item['label']=='Save52' else {}
  results.append(dict(label=item['label'],source=pin,unit=unit,decode=metrics,closure=True,end=c.p,tables=tables,typed_references=refs,matches=matches,reference_identity_counts=dict(collections.Counter(r['identity'] for r in refs))))
 assert identity(Path(pin['path']))==pin
assert [identity(p) for p in paths]==pins
result=dict(schema='strict-native-type4/1',inputs=pins,target_counts={k:len(v) for k,v in targets.items()},results=results,limits='Typed saved-ID census. Ship classification requires separate static definition/base context; wrappers alone do not prove physical reference type or owner. No overall population completeness claim.')
with (out/'type4-census01.json').open('x',encoding='utf8') as f:json.dump(result,f,indent=2);f.write('\n')
for x in results:print(x['label'],[(t['type'],t['count']) for t in x['tables']],len(x['typed_references']),{k:len(v) for k,v in x['matches'].items()},x['closure'])
