"""Native-qualified FNAM discovery inventory; no current menu simulation.
Reads fresh physical records, writes exclusive local graph summary/author CSVs.
Original selector, owned reader provenance. No target/input effects.
"""
from pathlib import Path
import json,struct,collections,csv
W=Path('.local-work/build-catalogue');O=Path('docs/experiments/build-catalogue');rs=json.loads((W/'definitions.json').read_text())['records'];by={r['formid']:r for r in rs}
def fs(r,k):return [bytes.fromhex(v) for t,v in r['fields'] if t==k]
def one(r,k):
 a=fs(r,k);assert len(a)<=1;return a[0] if a else b''
def u(r,k):return int.from_bytes(one(r,k),'little')
def ids(r,k='LNAM'):return [i[0] for b in fs(r,k) for i in struct.iter_unpack('<I',b)]
cats=ids(by[0x58606]);roots=[r for r in rs if r['type']=='COBJ' and ids(r,'FNAM') and ids(r,'FNAM')[0] in cats and not r['flags']&0x20];reached=set();missing=set();cycles=[]
def walk(i,stack=()):
 if i in stack:cycles.append([*stack,i]);return
 if i in reached:return
 r=by.get(i)
 if not r:missing.add(i);return
 reached.add(i)
 if r['type']=='COBJ':walk(u(r,'CNAM'),(*stack,i))
 elif r['type']=='FLST':
  for j in ids(r):walk(j,(*stack,i))
for r in roots:walk(r['formid'])
rc=[by[i] for i in reached if by[i]['type']=='COBJ'];counts=collections.Counter();examples=collections.defaultdict(list)
for r in rc:
 for b in fs(r,'CTDA'):
  k=struct.unpack_from('<H',b,8)[0];counts[f'{k:04x}']+=1
  if len(examples[f'{k:04x}'])<6:examples[f'{k:04x}'].append(f"{r['formid']:08x}")
result=dict(root_rule='COBJ clear flag 0x20; first FNAM resolved to member of OutpostRecipeCategories; physical main ESM only',roots=len(roots),reached_records=len(reached),reached_cobj=len(rc),missing_selected_types=len(missing),missing_ids=[f'{i:08x}' for i in sorted(missing)],cycles=cycles,categories=[dict(id=f'{i:08x}',edid=by[i]['edid'],ordinal=n,roots=sum(ids(r,'FNAM')[0]==i for r in roots)) for n,i in enumerate(cats)],condition_functions=dict(counts),condition_examples=dict(examples),grouped_roots=sum(bool(r['flags']&0x4000000) for r in roots))
(W/'graph02.json').open('x',encoding='utf8').write(json.dumps(result,indent=2)+'\n')
def table(name,rows):
 with (O/name).open('w',encoding='utf8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
table('categories.csv',result['categories'])
selected=set(cats+[0x58606,0x58607,0x2c59d7,0x1a2695,0x299547,0x2331e3,0x2ce193,0x296338,0x293ad1,0x2951f9,0x80675,0x636e8,0x23baa6,0x6d72e,0x6d73d,0x3023d,0x2a76d,0x2998d8,0x2951f7,0x293ad2,0x5ef19,0x5ed87,0x8407,0x20a8b4,0x2965f7,0x27319f,0x245775,0x245794,0x2457c1,0x14e8c2,0x777e6,0x2ac11b,0x2ac0fc])
for i in [0x296338,0x293ad1,0x2951f9]:
 target=u(by[i],'CNAM');selected.add(target);selected.update(ids(by[target]))
rows=[]
for i in sorted(selected):
 if i not in by:continue
 r=by[i];rows.append(dict(formid=f'{i:08x}',type=r['type'],editorid=r['edid'],physical_offset=r['offset'],flags=f"{r['flags']:08x}",target=f"{u(r,'CNAM'):08x}" if one(r,'CNAM') and len(one(r,'CNAM'))==4 else '',first_fnam=f"{ids(r,'FNAM')[0]:08x}" if r['type']=='COBJ' and ids(r,'FNAM') else '',ordered_list_members=len(ids(r)) if r['type']=='FLST' else '',conditions=len(fs(r,'CTDA')),classification='STATIC definition; physical main file; not live menu'))
table('definitions.csv',rows)
print(json.dumps(result,indent=2))
