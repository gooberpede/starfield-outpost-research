"""Original target-only BGSLocation native103 census. Read-only pinned save.
Stdlib/project readers; writes exclusive local receipt, cleaned decode scratch.
No target/DB/Git effects. Stops on source mutation or body/queue nonclosure.
"""
import sys,json,struct,collections
from pathlib import Path
sys.path.insert(0,'save-analysis/scripts')
from inventory_historical_saves import identity,guard
from stream_save import decoded_save
from workshop_population import typed_records
from outpost_record_framing import Reader
from extractor_resources import plugin_tables,saved_form
from validate_mature_outposts import directory
from outpost_membership import token_value
base=Path('.local-work/workshop-population-rework');out=base/'specialist'
lead=json.loads((base/'nonref-targets01.json').read_text());pin=lead['source'];path=Path(pin['path']);guard();assert identity(path)==pin
rows=[]
with decoded_save(path,out/'scratch23') as (b,metrics):
 d=directory(b);a=d['regions']['reference_u32'][0];plugins=plugin_tables(b)
 class Table:
  def __len__(self):return d['reference_count']
  def __getitem__(self,i):
   if not 0<=i<len(self):raise IndexError(i)
   return struct.unpack_from('<I',b,a+4+4*i)[0]
 def resolve(t):return saved_form(token_value(t,Table()),plugins)
 for r in typed_records(b):
  if r['form_type']!=0x75:continue
  c=Reader(b,r['body'],r['end']);qi=0;f=r['flags'];fields={}
  def u(n):return int.from_bytes(c.take(n),'little')
  def ref():
   global qi
   t=r['refs'][qi];qi+=1;return resolve(t)
  assert ref()==resolve(r['token'])
  if f&1:fields['form_flags']=u(4);fields['aux_flags']=u(2)
  if f&(1<<27):fields['1dc']=u(1);fields['1dd']=u(1)
  if f&(1<<30):fields['1b0']=[{'reference':ref(),'value':u(4)} for _ in range(c.count())]
  if f&(1<<24):fields['1c0']=[ref() for _ in range(c.count())]
  if f&(1<<29):fields['130']=[ref() for _ in range(c.count())]
  if f&(1<<28):fields['140']=[{'type':ref(),'reference':ref()} for _ in range(c.count())]
  if f&2:fields['aa']=u(1)
  if f&(1<<26):fields['b0']=c.take(16).hex()
  if f&(1<<31):fields['1e0']=ref()
  if f&4:fields['parent_c0']=ref()
  if f&(1<<25):raise ValueError(('KEYWORD_COMPONENT_PENDING',hex(f),r['offset'],c.p,qi))
  if f&(1<<23):fields['d8']=ref()
  assert c.p==c.end,('BODY_NONCLOSURE',r['offset'],hex(f),c.p,c.end)
  assert qi==len(r['refs']),('QUEUE_NONCLOSURE',qi,len(r['refs']))
  rows.append(dict(identity=resolve(r['token']),offset=r['offset'],end=r['end'],body=r['body'],flags=f,buffer_version=r['buffer_version'],fields=fields,queue_consumed=qi,closure=True))
assert identity(path)==pin
result=dict(schema='native-BGSLocation/1',source=pin,decode=metrics,count=len(rows),rows=rows,limits='Native saved field census. Location reference type association is distinct from WorkshopItem forward ownership; consumer qualification separate.')
with (out/'location-census23.json').open('x',encoding='utf8') as stream:json.dump(result,stream,indent=2);stream.write('\n')
print(len(rows),collections.Counter(hex(r['flags']) for r in rows))
