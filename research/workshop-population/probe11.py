# Original stdlib evidence join. Reads only specialist native exports; writes CREATE_NEW JSON.
import re,json,hashlib
from pathlib import Path
root=Path(__file__).parent
def read(n):
 p=root/f'native{n}.tsv';s=p.read_text();assert s.rstrip().endswith('END');return s
def funcs(s):
 return {m[1]:m[2] for m in re.finditer(r'FUNCTION\t([0-9a-f]+)\n(.*?)(?=\n(?:FUNCTION\t|XREF\t|DATA\t|END)|\Z)',s,re.S)}
s73,s74,s75,s72,s76=(read(n) for n in (73,74,75,72,76))
ctors=funcs(s74)|funcs(s76);factories=funcs(s75)
slots48={m[2]:dict(vtable=m[1],factory=m[3]) for m in re.finditer(r'LOAD_SLOT\t([0-9a-f]+)\t([^\n\t]+)::vftable\t([0-9a-f]+)\t',s75) if m[3] in factories and m[2]+'_Runtime::vftable' in factories[m[3]]}
slots90={m[2]:dict(vtable=m[1],reader=m[3]) for m in re.finditer(r'LOAD_SLOT\t([0-9a-f]+)\t([^\n\t]+)::vftable\t([0-9a-f]+)\t',s72) if '_Runtime' in m[2] and '<' not in m[2]}
grammar={'1402b56d0':[],'1402b5640':['u32','u32','u8'],'1402b9090':['u32 N + N storageIDs','u32 M + M {u16,storageID}'],'1402bb650':['u32 N + N storageIDs','u32 M + M storageIDs'],'1402bc670':['u32 N + N storageIDs'],'1402bf070':['u32 N + N storageIDs'],'1402c3270':['u32 N + N storageIDs','u32 M + M storageIDs'],'1402c6360':['u32 N + N storageIDs'],'1402c7be0':['u32 N + N storageIDs'],'1402c8ac0':['u8','u32','u32']}
rows=[]
for reg,b in funcs(s73).items():
 cm=re.search(r'local_50 = FUN_([0-9a-f]+);',b)
 if not cm:continue
 ctor=cm[1];nm=re.search(r'FUN_1428cba80\([^\n]*\(byte \*\)"([^"]+)"',b)
 name=nm[1] if nm else 'Kill'
 cb=ctors[ctor];cl=re.findall(r'\b(BGS\w+Activity)::vftable',cb)
 if not cl:
  helpers=[h for h in re.findall(r'FUN_([0-9a-f]+)\(',cb) if h in ctors and h!=ctor]
  assert len(helpers)==1,(name,helpers)
  cl=re.findall(r'\b(BGS\w+Activity)::vftable',ctors[helpers[0]])
 cls=set(cl);assert len(cls)==1,(name,cls);cls=cls.pop();fac=slots48[cls]
 runtime=set(re.findall(r'\b(BGS\w+Activity_Runtime)::vftable',factories[fac['factory']]))
 assert len(runtime)==1,(name,runtime);runtime=runtime.pop();reader=slots90[runtime]
 rows.append(dict(name=name,registration=reg,constructor=ctor,activity_class=cls,activity_vtable=fac['vtable'],runtime_factory=fac['factory'],runtime_class=runtime,runtime_vtable=reader['vtable'],custom_reader_90=reader['reader'],custom_prefix_when_StarbornManager_null=grammar[reader['reader']],common_reader_70='1402b5fc0',common_suffix=['u32 counter','u8 status']))
assert len(rows)==30 and len({r['name'] for r in rows})==30
pins=[dict(name=f'native{n}.tsv',sha256=hashlib.sha256((root/f'native{n}.tsv').read_bytes()).hexdigest()) for n in (72,73,74,75,76)]
with (root/'activity-dispatch01.json').open('x') as f:json.dump(dict(executable_sha256='7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28',address_domain='preferred VA base140000000',storageID='u32 low24 queued token through14186bc80',custom_gate='145fb4b78 StarbornManager is null',coverage='all30 identified native registry initializers; unique concrete primary runtime joins',sources=pins,rows=rows),f,indent=2);f.write('\n')
print('joined',len(rows),'activities')
