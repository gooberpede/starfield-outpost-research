"""Replay native-qualified row/extra grammar on frozen H256/257 candidate bodies.
No original or live effects. Writes exclusive local receipt, unsupported stops."""
from pathlib import Path
import sys,json,struct
R=Path.cwd();W=R/'.local-work/sd1-containers';sys.path[:0]=[str(W),str(R/'save-analysis/scripts')]
from extras_sd1 import extra_view
from outpost_record_framing import Reader
out=[]
for label in ['HIST-0256','HIST-0257']:
 j=json.loads((W/f'saved-{label}.json').read_text());rows=[]
 for r in j['rows']:
  if not ('Mannequin' in r['edid'] or 'Storage_' in r['edid']):continue
  rec=r['record'];b=bytearray(rec['end']);b[rec['body']:rec['end']]=bytes.fromhex(r['body_hex']);resolve=dict(zip(rec['refs'],r['queue'])).__getitem__
  row={k:r[k] for k in ('identity','base','edid','record','prefix')};row['extras']=r.get('extras');row['inventory']=[]
  if not r.get('extras',{}).get('status')=='COUNT_CLOSED' or not rec['flags']&0x08000020:
   row['status']='NO_QUALIFIED_INVENTORY_BRANCH';rows.append(row);continue
  c=Reader(b,r['extras']['body_end'],rec['end']);ri=r['extras']['next_reference_index'];n=c.count();row['item_count']=n
  try:
   for i in range(n):
    item=dict(item=resolve(rec['refs'][ri]),offset=c.p,stacks=[]);ri+=1;row['inventory'].append(item)
    for k in range(c.count()):
     ex=extra_view(b,dict(rec,flags=0x40),dict(form_prefix_end=c.p,next_reference_index=ri),resolve)
     stack=dict(extras=ex);item['stacks'].append(stack)
     if ex['status']!='COUNT_CLOSED':raise ValueError('UNSUPPORTED_STACK_EXTRA')
     c.p=ex['body_end'];ri=ex['next_reference_index'];stack['count']=struct.unpack('<i',c.take(4))[0]
    item['row_state']=int.from_bytes(c.take(4),'little');item['byte']=c.take(1)[0];item['end']=c.p
   row.update(status='ROW_AND_QUEUE_CLOSED' if ri==len(rec['refs']) else 'ROW_CLOSED_QUEUE_REMAINDER',inventory_end=c.p,queue_used=ri,queue_count=len(rec['refs']),tail_bytes=rec['end']-c.p)
  except (ValueError,IndexError) as e:row['status']=str(e)
  rows.append(row)
 out.append(dict(label=label,source=j['source'],rows=rows))
(W/'stock-joins02.json').open('x',encoding='utf8').write(json.dumps(out,indent=2)+'\n')
for j in out:
 for r in j['rows']:print(j['label'],r['identity'],r['edid'],r['status'],[(x['item'],x.get('row_state'),[(s.get('count'),s['extras']['status'],[e['type'] for e in s['extras'].get('extras',[])]) for s in x['stacks']]) for x in r['inventory']])
