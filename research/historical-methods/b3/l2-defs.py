# Targeted fresh definitions/setting provenance; owned esm_records and PE method.
from pathlib import Path
import json,sys,re,struct,zipfile
R=Path.cwd();W=R/'.local-work/l2-budget';sys.path[:0]=[str(R/'research/cr2-skills'),str(R/'save-analysis/scripts')]
from definitions import pin
from inspect_outpost_definitions import esm_records
from inventory_historical_saves import guard
guard();seed=json.loads((W/'baseline.json').read_text());esm=next(Path(x['path']) for x in seed['protected'] if Path(x['path']).name=='Starfield.esm');before=pin(esm)
rows=[]
for h,fs in esm_records(esm,{b'GMST',b'AVIF',b'DFOB',b'NPC_',b'CONT',b'PKIN',b'STAT',b'COBJ',b'REFR'},repeated=True):
 edid=next((v.rstrip(b'\0').decode('utf8') for k,v in fs if k==b'EDID'),'')
 if any(x in edid.lower() for x in ['budget','workshopcurrent','workshopmax','outpostbeacon','outpoststoragesolid','outpostrobot','outpostextractor','outpostpower01','workshoplight','containermass','workshopobject']):
  rows.append(dict(**h,edid=edid,fields=[(k.decode(),v.hex()) for k,v in fs]))
assert before==pin(esm);(W/'definitions01.json').open('x').write(json.dumps(dict(source=before,records=rows),indent=2)+'\n')
for r in rows:
 if r['type'] in ['GMST','AVIF','DFOB']:print(r['type'],hex(r['formid']),r['edid'],r['fields'])
exe=next(Path(x['path']) for x in seed['protected'] if Path(x['path']).name=='Starfield.exe');b=exe.read_bytes();pe=struct.unpack_from('<I',b,0x3c)[0];count=struct.unpack_from('<H',b,pe+6)[0];opt=struct.unpack_from('<H',b,pe+20)[0]
def readva(va):
 rva=va-0x140000000
 for i in range(count):
  vsize,vbase,size,off=struct.unpack_from('<IIII',b,pe+24+opt+40*i+8)
  if vbase<=rva<vbase+size:return struct.unpack_from('<f',b,off+rva-vbase)[0]
constants={hex(va):readva(va) for va in [0x144f044e8,0x144f04980,0x144f04f28]}
configs=[]
for p in [exe.parent/'Starfield.ini',Path('C:/Users/User/Documents/My Games/Starfield/Starfield.ini'),Path('C:/Users/User/Documents/My Games/Starfield/StarfieldCustom.ini')]:
 txt=p.read_text(encoding='utf-8-sig',errors='replace');matches=[line for line in txt.splitlines() if any(s in line.lower() for s in ['budget','workshop'])];configs.append(dict(source=pin(p),selected_lines=matches))
z=exe.parent/'Tools/ContentResources.zip';scripts=[]
with zipfile.ZipFile(z) as f:
 for n in f.namelist():
  if n.endswith('.psc'):
   bb=f.read(n)
   if any(s in bb.lower() for s in [b'workshopcurrentbudget',b'budgetbaseline',b'budgetmultiplier',b'currenttriangles',b'maxtriangles']):
    scripts.append(dict(member=n,lines=[(i+1,line) for i,line in enumerate(bb.decode('utf8',errors='replace').splitlines()) if 'budget' in line.lower() or 'triangle' in line.lower()]))
(W/'settings01.json').open('x').write(json.dumps(dict(constants=constants,configs=configs,scripts=scripts,zip=pin(z)),indent=2)+'\n');print('constants',constants,'scripts',scripts)
