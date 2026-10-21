"""BM1 finite main-ESM census; reads installed file using owned bounded reader.
Writes ignored JSON only. All physical selected types, ordered fields preserved;
no override merge, game execution or inputs modified. CPython -B, stdlib.
"""
from pathlib import Path
import sys,json,collections,struct
R=Path.cwd();W=R/'.local-work/construction-variants'
sys.path.insert(0,str(R/'save-analysis/scripts'));sys.path.insert(0,str(R/'research/s1-storage'))
from inspect_outpost_definitions import esm_records
from inventory_historical_saves import guard
from catalog import pin
guard();base=json.loads((W/'baseline.json').read_text());esm=Path(next(x['path'] for x in base['protected'] if x['path'].endswith('Starfield.esm')));before=pin(esm)
assert before in base['protected']
counts=collections.Counter();p=0;total=esm.stat().st_size
with esm.open('rb') as f:
 while p<total:
  f.seek(p);h=f.read(24);n=int.from_bytes(h[4:8],'little');t=h[:4].decode();counts[t]+=1;p+=24 if t=='GRUP' else n+24
assert p==total
wanted={t.encode() for t in counts if t not in ['GRUP','LAND','NAVM','CELL','REFR','ACHR','PGRE','PHZD','PMIS','PARW','PBAR','PBEA','PCON','PFLA','NPC_','INFO','DIAL','QUST','SCEN','PACK','RSPJ','PERK','PNDT']}
wanted={x.encode() for x in ['STAT','ACTI','CONT','PKIN','COBJ','FLST','KYWD','DFOB','SNBH','SNTP','MSWP','STMP','STBH','STND','LMSW','MATT','OMOD','AVIF','SCOL','MSTT','DOOR']}
rows=[]
for r,fs in esm_records(esm,wanted,repeated=True):
 edid=next((v.rstrip(b'\0').decode('utf8') for t,v in fs if t==b'EDID'),'')
 # Keep every relevant component-definition type; remaining types retain index.
 full=r['type'] in ['STAT','ACTI','CONT','PKIN','COBJ','FLST','KYWD','DFOB','SNBH','SNTP','MSWP','STMP','STBH','STND','LMSW','MATT','OMOD','AVIF','SCOL','MSTT','DOOR']
 rows.append(dict(**r,edid=edid,fields=[(t.decode(),v.hex()) for t,v in fs] if full else []))
assert pin(esm)==before
(W/'definitions02.json').open('x',encoding='utf8').write(json.dumps(dict(source=before,counts=counts,selected_types=sorted(x.decode() for x in wanted),records=rows),indent=2)+'\n')
print('headers',dict(counts),'indexed',len(rows))
