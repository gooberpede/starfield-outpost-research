from pathlib import Path
import sys,json,re,hashlib,zipfile
R=Path.cwd();W=R/'.local-work/l3-placement';sys.path[:0]=[str(R/'save-analysis/scripts')]
from inspect_outpost_definitions import esm_records
from inventory_historical_saves import guard
guard();seed=json.loads((W/'baseline.json').read_text());p=next(Path(x['path']) for x in seed['protected'] if Path(x['path']).name=='Starfield.esm');rows=[]
for h,fs in esm_records(p,{b'GMST',b'AVIF',b'DFOB',b'KYWD',b'PKIN',b'ACTI',b'STAT',b'FLOR',b'LCTN'},repeated=True):
 edid=next((v.rstrip(b'\0').decode('utf8') for k,v in fs if k==b'EDID'),'')
 if re.search(r'(workshop|outpost).*(radius|bulldoz|clear|restric|intersect|overlap|beacon|power01|extractor)',edid,re.I) or h['formid'] in [0x2031e1,0x05ef19,0x29a8c6,0x2c60e9]:rows.append(dict(**h,edid=edid,fields=[(k.decode(),v.hex()) for k,v in fs]))
(W/'definitions01.json').open('x',encoding='utf8').write(json.dumps(dict(source=next(x for x in seed['protected'] if x['path']==str(p)),records=rows),indent=2)+'\n')
for r in rows:
 if r['type'] in ['GMST','AVIF','DFOB','KYWD']:print(r['type'],hex(r['formid']),r['edid'],r['fields'])
z=next(Path(x['path']) for x in seed['protected'] if Path(x['path']).name=='ContentResources.zip');scripts=[]
with zipfile.ZipFile(z) as f:
 for n in f.namelist():
  if n.endswith('.psc'):
   b=f.read(n);txt=b.decode('utf8',errors='replace');ls=[(i+1,l) for i,l in enumerate(txt.splitlines()) if re.search('bulldoz|restrictedbuild|buildradius|clear.*clutter',l,re.I)]
   if ls:scripts.append(dict(member=n,sha256=hashlib.sha256(b).hexdigest(),lines=ls))
(W/'scripts01.json').open('x').write(json.dumps(scripts,indent=2)+'\n');print('script hits',len(scripts))
