from pathlib import Path
import json,collections,sys,struct
R=Path.cwd();W=R/'.local-work/l3-placement';sys.path[:0]=[str(R/'save-analysis/scripts')]
from stream_save import decoded_save
from workshop_population import typed_records,initial_prefix
from validate_mature_outposts import directory
from extractor_resources import plugin_tables,saved_form
from outpost_membership import token_value
out=[]
for n in [30,31,33,34,35,36]:
 x=json.loads((W/f'Save{n}.json').read_text());rows=[r for r in x['record_states'] if r['type']==0x4a and r['change_flags']&0x1000000];print(n,'bulldozed-channel REFR',len(rows),collections.Counter(r['change_flags'] for r in rows))
 with decoded_save(Path(x['source']['copy']['path']),W/'scratch',seconds=float('inf')) as (b,m):
  d=directory(b);forms=struct.unpack_from('<'+'I'*d['reference_count'],b,d['regions']['reference_u32'][0]+4);plugins=plugin_tables(b)
  def resolve(t):return saved_form(token_value(t,forms),plugins)
  selected=[]
  for r in typed_records(b):
   if r['form_type']!=0x4a or not r['flags']&0x1000000:continue
   row=dict(identity=resolve(r['token']),record=r,refs=[resolve(t) for t in r['refs']],body_hex=bytes(b[r['body']:r['end']]).hex())
   try:
    pp=initial_prefix(b,r);row['prefix']=pp;row['base']=resolve(pp['base_token']) if pp.get('base_token') else None
   except (ValueError,struct.error) as e:row['gap']=str(e)
   selected.append(row)
  out.append(dict(label=x['label'],rows=selected))
for a,c in [(30,31),(31,33),(34,35),(35,36)]:
 aa=json.loads((W/f'Save{a}.json').read_text());cc=json.loads((W/f'Save{c}.json').read_text());ad={r['id']:r for r in aa['record_states']};cd={r['id']:r for r in cc['record_states']};new=[r for k,r in cd.items() if k not in ad];gone=[r for k,r in ad.items() if k not in cd];changed=[dict(before=ad[k],after=r) for k,r in cd.items() if k in ad and (r['body_sha256'],r['refs'],r['change_flags'])!=(ad[k]['body_sha256'],ad[k]['refs'],ad[k]['change_flags'])]
 (W/f'compare-{a}-{c}.json').open('x').write(json.dumps(dict(new=new,gone=gone,changed=changed),indent=2)+'\n');print(a,c,'new/gone/changed',len(new),len(gone),len(changed),'new bulldozed',[(r['id'],hex(r['change_flags'])) for r in new if r['type']==0x4a and r['change_flags']&0x1000000])
(W/'bulldozed-channel01.json').open('x').write(json.dumps(out,indent=2)+'\n')
