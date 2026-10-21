"""Original recursive main-ESM recipe/list census and PKIN child acquisition.
Read-only pinned ESM; local raw JSON plus authored numeric CSV. No game effects.
Reuses owned S1 catalog helpers and assembly header-walk method."""
from pathlib import Path
import sys,json,struct,zlib,csv
R=Path.cwd();W=R/'.local-work/sd1-containers';sys.path.insert(0,str(R/'research/s1-storage'))
from catalog import pin,field,fields,props,words
from inspect_outpost_definitions import subrecords,esm_records
from inventory_historical_saves import guard
guard();j=json.loads((R/'.local-work/e2-organic/inventory02.json').read_text());by={r['formid']:r for r in j['records']};src=Path(j['source']['path']);assert pin(src)==j['source']
for h,fs in esm_records(src,{b'ACTI',b'STAT',b'FURN',b'MSTT',b'CONT',b'NPC_',b'COBJ',b'PKIN',b'FLST',b'KYWD',b'STMP',b'RACE'},repeated=True):
 by[h['formid']]=dict(**h,edid=next((v.rstrip(b'\0').decode('utf8') for k,v in fs if k==b'EDID'),''),fields=[(k.decode(),v.hex()) for k,v in fs])
def expand(i,chain=()):
 assert i not in chain
 if i not in by:
  yield dict(formid=i,type='UNINDEXED',edid='UNINDEXED',offset=None,fields=[]),chain+(i,)
  return
 r=by[i];chain=chain+(i,)
 if r['type']=='FLST':
  for v in fields(r,'LNAM'):yield from expand(int.from_bytes(v,'little'),chain)
 elif r['type']=='COBJ':
  p=int.from_bytes(field(r,'CNAM'),'little')
  if p:yield from expand(p,chain)
 else:yield r,chain
roots=[]
for r in by.values():
 if r['type']!='COBJ' or not r['edid'].startswith('co_Outpost_'):continue
 p=int.from_bytes(field(r,'CNAM'),'little')
 if not p or p not in by:continue
 leaves=list(expand(p))
 if any(x['type']=='NPC_' and 'Mannequin' in x['edid'] or x['type']=='CONT' and (b'BGSDisplayCase\0' in fields(x,'BFCB') or 'ShipOutpost_Loot_Storage' in x['edid']) for x,c in leaves) or 'StorageBinList' in r['edid']:
  roots.append((r,leaves))
rows=[];packins={}
for r,leaves in roots:
 for x,chain in leaves:
  if x['type']=='PKIN':packins[x['formid']]=x
  rows.append(dict(recipe=f'{r["formid"]:08x}',recipe_editorid=r['edid'],recipe_offset=r['offset'],base=f'{x["formid"]:08x}',base_editorid=x['edid'],type=x['type'],base_offset=x['offset'],chain='>'.join(f'{i:08x}' for i in chain),carryweight=props(x).get(0x2dc),display_component=b'BGSDisplayCase\0' in fields(x,'BFCB'),dc_slots=len(field(x,'DCSD'))//16,dc_words=[list(v) for v in struct.iter_unpack('<IIII',field(x,'DCSD'))],filter=field(x,'ONAM').hex(),properties=props(x)))
# Also generic-case recipes select PKINs without a display component on root.
for r in by.values():
 if r['type']=='COBJ' and r['edid'].startswith('co_Outpost_Display_'):
  p=int.from_bytes(field(r,'CNAM'),'little')
  if p:
   for x,chain in expand(p):
    if x['type']=='PKIN':packins[x['formid']]=x
cells={int.from_bytes(field(r,'CNAM'),'little'):r for r in packins.values()};children=[]
with src.open('rb') as f:
 end=src.stat().st_size;stack=[(end,None)];pos=0
 while pos<end:
  while pos==stack[-1][0] and len(stack)>1:stack.pop()
  f.seek(pos);h=f.read(24);assert len(h)==24;tag=h[:4];n,flags,fid=struct.unpack_from('<III',h,4);stop=pos+(n if tag==b'GRUP' else n+24);assert pos+24<=stop<=stack[-1][0];cell=stack[-1][1]
  if tag==b'GRUP':
   if struct.unpack_from('<I',h,12)[0]==6:cell=flags
   stack.append((stop,cell));pos+=24;continue
  if tag in (b'REFR',b'ACHR') and cell in cells:
   b=f.read(n)
   if flags&0x40000:
    size=int.from_bytes(b[:4],'little');b=zlib.decompress(b[4:]);assert len(b)==size
   fs=[(k.decode(),v.hex()) for k,v in subrecords(b)];base=int.from_bytes(bytes.fromhex(dict(fs)['NAME']),'little');br=by.get(base)
   children.append(dict(formid=f'{fid:08x}',offset=pos,packin=f'{cells[cell]["formid"]:08x}',base=f'{base:08x}',base_type=br['type'] if br else None,base_editorid=br['edid'] if br else None,fields=fs,base_fields=br['fields'] if br else None))
  pos=stop
assert pin(src)==j['source'];guard()
(W/'census01.json').open('x',encoding='utf8').write(json.dumps(dict(rows=rows,packins=list(packins.values()),children=children,source=pin(src),definitions=list(by.values())),indent=2)+'\n')
print('roots',len(roots),'rows',len(rows),'unique',len(set(x['base'] for x in rows)),'packins',len(packins),'children',len(children))
for x in rows:print(x['recipe'],x['base'],x['base_editorid'],'C',x['carryweight'],'slots',x['dc_slots'])
for x in children:
 if x['base_type'] in ('CONT','NPC_'):print('child',x['packin'],x['formid'],x['base'],x['base_editorid'])
