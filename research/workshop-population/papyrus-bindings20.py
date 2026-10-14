"""Strict bounded VM prefix/object-binding table from native91/92/93.
Reads string/type metadata and both object header tables; stops before variable
payloads. Target-only output and VM-EID containment of rawLE leads. No VM dump.
"""
import sys,json,struct,collections
from pathlib import Path
sys.path.insert(0,'save-analysis/scripts')
from inventory_historical_saves import identity,guard
from stream_save import decoded_save
from outpost_record_framing import Reader
from validate_mature_outposts import directory
from extractor_resources import plugin_tables,saved_form
from outpost_membership import token_value
base=Path('.local-work/workshop-population-rework');out=base/'specialist';guard()
inputs=[base/'papyrus-leads01.json',out/'native91.tsv',out/'native92.tsv',out/'native93.tsv',Path(__file__)]
pins=[identity(p) for p in inputs];old=json.loads(inputs[0].read_text());src=old['source'];assert identity(Path(src['path']))==src;unit=old['unit'];targets={r['identity'] for r in old['rows']};result=dict(inputs=pins,source=src,unit=unit)
with decoded_save(Path(src['path']),out/'papyrus-scratch20') as (b,metrics):
 c=Reader(b,unit['body'],unit['end']);sections=[]
 def u(n):return int.from_bytes(c.take(n),'little')
 try:
  version=u(2);assert version==10
  count=u(4);assert count<=(c.end-c.p)//2;strings=[c.take(u(2)).decode('utf8') for _ in range(count)];sections.append(dict(name='stringtable',count=count,end=c.p))
  def si():
   v=u(4);assert v<len(strings),('STRING_INDEX_BOUNDS',c.p,v);return v
  nt=u(4);ns=u(4);types=[]
  for _ in range(nt):
   name=si();parent=si();fields=[(si(),si()) for _ in range(u(4))];flags=[si() for _ in range(u(4))];types.append(dict(name=name,parent=parent,fields=fields,flags=flags))
  sections.append(dict(name='scripttypes',count=nt,end=c.p))
  for _ in range(ns):name=si();fields=[(si(),si()) for _ in range(u(4))]
  sections.append(dict(name='structtypes',count=ns,end=c.p))
  d=directory(b);a=d['regions']['reference_u32'][0];plugins=plugin_tables(b)
  class Table:
   def __len__(self):return d['reference_count']
   def __getitem__(self,i):
    if not 0<=i<len(self):raise IndexError(i)
    return struct.unpack_from('<I',b,a+4+4*i)[0]
  bound=[];allEIDs={};knownBE=[];kind_counts=collections.Counter();aux_counts=collections.Counter();nb=u(4);start=c.p
  for ordinal in range(nb):
   at=c.p;eid=u(8);name=si();kind=u(2);aux=u(2);kind_counts[kind]+=1;aux_counts[(kind,aux)]+=1;formoffset=c.p
   if kind in (0,1,2):
    token=c.take(3).hex();form=saved_form(token_value(token,Table()),plugins);raw=None
   elif kind==3:raw=u(4);token=None;form=None
   else:raise ValueError(('UNKNOWN_HANDLE_KIND',kind,c.p))
   flag=u(1);allEIDs[eid]=dict(offset=at,script=strings[name],handle_identity=form,kind=kind)
   if form in targets:bound.append(dict(ordinal=ordinal,offset=at,end=c.p,eid=eid,script_index=name,script=strings[name],kind=kind,aux=aux,token=token,identity=form,flag=flag,formref_offset=formoffset));knownBE.append(formoffset)
  sections.append(dict(name='bound-object-headers',count=nb,start=start,end=c.p))
  nu=u(4);start=c.p
  for ordinal in range(nu):
   at=c.p;eid=u(8);name=si();allEIDs[eid]=dict(offset=at,script=strings[name],handle_identity=None,kind=None)
  sections.append(dict(name='unbound-object-headers',count=nu,start=start,end=c.p))
  expectedBE=sorted(p for r in old['rows'] for p in r['patterns']['FormRefBE']);assert sorted(knownBE)==expectedBE,('UNCLASSIFIED_BE_LEADS',len(knownBE),len(expectedBE))
  le=[]
  for r in old['rows']:
   for at in r['patterns']['FormRefLE']:
    candidates=[]
    for start in range(max(unit['body'],at-5),min(at+1,unit['end']-7)):
     eid=struct.unpack_from('<Q',b,start)[0]
     if eid in allEIDs:candidates.append(dict(eid=eid,word_offset=start,binding=allEIDs[eid]))
    le.append(dict(target=r['identity'],lead_offset=at,known_VM_EID_containment=candidates,typed_direct_formref=at in knownBE))
  result.update(handle_kind_counts=dict(kind_counts),handle_aux_counts=[dict(kind=k[0],aux=k[1],count=v) for k,v in sorted(aux_counts.items())],target_script_definitions=[dict(name=strings[t['name']],parent=strings[t['parent']],fields=[dict(name=strings[a],type=strings[b]) for a,b in t['fields']],flags=[strings[a] for a in t['flags']]) for t in types if strings[t['name']] in {r['script'] for r in bound}],status='STRICT_PREFIX_AND_OBJECT_HEADERS_CLOSED',version=version,decode=metrics,sections=sections,first_unparsed_offset=c.p,target_bindings=bound,typed_BE_leads=len(knownBE),LE_leads=le,LE_known_EID_count=sum(bool(x['known_VM_EID_containment']) for x in le),limits='Both object header tables decoded exactly from unit start; fullVM tail not parsed. VM object IDs identify script objects, not ordinary FormIDs; typed form handles use directBE writer contract. Absence of an object binding does not prove physical nonexistence.')
 except (ValueError,AssertionError,IndexError) as error:result.update(status='RETAINED_PREFIX_GAP',error=str(error),offset=c.p,sections=sections)
assert identity(Path(src['path']))==src and [identity(p) for p in inputs]==pins
with (out/'papyrus-bindings20.json').open('x',encoding='utf8') as f:json.dump(result,f,indent=2);f.write('\n')
print(result['status'],result.get('error'),result.get('sections'),result.get('typed_BE_leads'),result.get('LE_known_EID_count'))
