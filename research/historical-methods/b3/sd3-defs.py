"""Original selectors with owned S1 ESM framing: physically reread finite
source-class controls and screenshot resource definitions. No input changes."""
from pathlib import Path
import sys,json,struct,zlib,csv
R=Path.cwd();W=R/'.local-work/sd3-stored';sys.path.insert(0,str(R/'research/s1-storage'))
from catalog import pin,field,props
from inspect_outpost_definitions import subrecords
j=json.loads((R/'.local-work/e2-organic/inventory02.json').read_text());p=Path(j['source']['path']);assert pin(p)==j['source'];by={r['formid']:r for r in j['records']}
ids={0x57c7,0x556e,0x77828,0x55b1,0x7782a,0x55cd,0x245775,0x246b6a,0x260db6,0x260db7,0xf659,0xf65a,0x2c60e9}
ids.update(int(r['formid'],16) for r in json.loads((R/'.local-work/s1-storage/census02.json').read_text())['rows'])
ids.update(int(r['base'],16) for r in csv.DictReader((R/'docs/experiments/containers-displays/definitions.csv').open()) if r['type'] in ('CONT','NPC_') and int(r['base'],16) in by)
selected=[by[i] for i in sorted(ids) if i in by]
with p.open('rb') as f:
 for r in selected:
  f.seek(r['offset']);h=f.read(24);n,flags,fid=struct.unpack_from('<III',h,4);assert fid==r['formid'];b=f.read(n)
  if flags&0x40000:
   size=int.from_bytes(b[:4],'little');b=zlib.decompress(b[4:]);assert len(b)==size
  assert [(k.decode(),v.hex()) for k,v in subrecords(b)]==[tuple(x) for x in r['fields']]
assert pin(p)==j['source']
(W/'definitions01.json').open('x',encoding='utf8').write(json.dumps(dict(source=j['source'],records=selected),indent=2)+'\n')
print('physical rereads',len(selected))
for r in selected:
 if r['type'] in ('IRES','MISC'):print(hex(r['formid']),r['edid'],r['fields'])
