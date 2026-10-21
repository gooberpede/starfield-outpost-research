"""LO1 original finite metadata selector over owned ESM framing. Immutable main
ESM reads; exclusive local selected fields/offsets, no save or target effects."""
from pathlib import Path
import sys,json
R=Path.cwd();W=R/'.local-work/lo1-locations'
sys.path.insert(0,str(R/'save-analysis/scripts'))
from inspect_outpost_definitions import esm_records
from inventory_historical_saves import guard
sys.path.insert(0,str(R/'research/s1-storage'))
from catalog import pin
base=json.loads((W/'baseline.json').read_text());p=Path(next(x['path'] for x in base['protected'] if x['path'].endswith('Starfield.esm')))
guard();before=pin(p);rows=[];counts={}
for r,fs in esm_records(p,{b'LCTN',b'FACT',b'STDT',b'GMST',b'DFOB'},repeated=True):
 counts[r['type']]=counts.get(r['type'],0)+1
 ed=next((v.rstrip(b'\0').decode('utf8') for k,v in fs if k==b'EDID'),'')
 if any(s in ed.lower() for s in ['narion','schrodinger','kreet','systemlevel','systemchallenge','freestar','maxdeployed']) or r['type']=='STDT':
  rows.append(dict(**r,edid=ed,fields=[(k.decode(),v.hex()) for k,v in fs]))
assert before==pin(p)
(W/'metadata01.json').open('x',encoding='utf8').write(json.dumps(dict(source=before,counts=counts,records=rows),indent=2)+'\n')
print(counts,'selected',len(rows))
for r in rows:
 if any(s in r['edid'].lower() for s in ['narion','schrodinger','kreet']) and r['type']!='LCTN' or r['type']=='LCTN' and r['edid'].lower() in ['kreetlocation','narionlocation','schrodingerlocation','schrodingeriilocation']:
  print(r['type'],hex(r['formid']),r['edid'],[(k,v) for k,v in r['fields'] if k not in ['KSIZ','KWDA']])
guard()
