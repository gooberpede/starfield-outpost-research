"""Replay native-backed extra extensions on frozen selected record bodies.
Reads local component receipts only; writes new local instance joins. No inputs
edited; raw bodies never incorporated into authored documentation."""
from pathlib import Path
import sys,json
R=Path.cwd();W=R/'.local-work/sd1-containers';sys.path[:0]=[str(W),str(R/'save-analysis/scripts')]
from extras_sd1 import extra_view
out=[]
for label in ['HIST-0021','HIST-0036','HIST-0255']:
 j=json.loads((W/('components-'+label+'.json')).read_text());rows=[]
 for relation in j['sections'][1]['rows']:
  for role,ident,slot in [('fixture',relation['identity'],None)]+[('item',x,i) for i,g in enumerate(relation['resolved_groups']) for x in g]:
   r=j['records'].get(ident)
   if not r or 'prefix' not in r:continue
   b=bytearray(r['record']['end']);b[r['record']['body']:r['record']['end']]=bytes.fromhex(r['body_hex']);resolve=dict(zip(r['record']['refs'],r['queue'])).__getitem__
   row=dict(role=role,identity=ident,fixture=relation['identity'],slot=slot,base=r['base'],offset=r['record']['offset'],flags=r['prefix'].get('saved_form_flags'),xyz=r['prefix'].get('xyz'))
   try:row['extras']=extra_view(b,r['record'],r['prefix'],resolve)
   except (ValueError,IndexError) as e:row['gap']=str(e)
   rows.append(row)
 out.append(dict(label=label,source=j['source'],rows=rows))
(W/'instance-joins02.json').open('x',encoding='utf8').write(json.dumps(out,indent=2)+'\n')
for j in out:
 for r in j['rows']:
  print(j['label'],r['role'],r['identity'],r['base'],r.get('extras',{}).get('status',r.get('gap')),[(e['type'],e.get('references'),len(e.get('modifications',[]))) for e in r.get('extras',{}).get('extras',[])])
