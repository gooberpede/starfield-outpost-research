import json,sys,struct,collections
from pathlib import Path
sys.path.insert(0,'save-analysis/scripts')
from stream_save import decoded_save
from inventory_historical_saves import identity,guard
from extractor_resources import plugin_tables,saved_form
from outpost_membership import token_value
from validate_mature_outposts import directory
out=Path('.local-work/workshop-population-rework');xs=json.loads((out/'type6-walk12.json').read_text());da=json.loads((out/'nonowner-da01.json').read_text());targets={r['identity'] for r in da['nonnull_groups']};results=[];guard()
for x in xs:
 pin=x['source'];assert identity(Path(pin['path']))==pin
 with decoded_save(Path(pin['path']),out/'scratch') as (b,m):
  d=directory(b);a=d['regions']['reference_u32'][0];plugins=plugin_tables(b)
  class Table:
   def __len__(self):return d['reference_count']
   def __getitem__(self,i):
    if not 0<=i<len(self):raise IndexError(i)
    return struct.unpack_from('<I',b,a+4+4*i)[0]
  def resolve(word):return saved_form(token_value(f'{word&0xffffff:06x}',Table()),plugins)
  section=next(s for s in x['sections'] if s['name']=='140602460');names=collections.Counter();rows=[]
  for outer in section['rows']:
   for group in outer['data']:
    for event in group['entries']:
     names[event['text']]+=1
     if event['text']=='Build Workshop Item':
      r=dict(source_group=resolve(group['id_word']),raw=event['raw'],counter=event['common_activity_runtime'],ids_a=[resolve(w) for w in event.get('derived_ids',[])],ids_b=[resolve(w) for w in event.get('derived_ids_b',[])])
      r['candidate_group_matches']=sorted((set(r['ids_a'])|set(r['ids_b']))&targets);rows.append(r)
  results.append(dict(label=x['label'],source=pin,names=dict(names),build_workshop_activities=rows,scope='Activity history/context, not owner or physical-instance authority'))
  print(x['label'],dict(names),'build',rows,flush=True)
 assert identity(Path(pin['path']))==pin
(out/'activity-census01.json').open('x',encoding='utf8').write(json.dumps(results,indent=2)+'\n')
