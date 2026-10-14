"""Native-qualified handle encoding necessary-condition leads, not VM framing.
Writer141fa48c0 forces all171 FF targets direct80 big-endian FormRef; reader
141f51020 uses u16kind,u16aux,three-byteFormRef for kinds0..2. Retain all byte
matches, adjacent fields and locations; do not claim structured table membership.
"""
import sys,json,struct
from pathlib import Path
sys.path.insert(0,'save-analysis/scripts')
from inventory_historical_saves import identity,guard
from stream_save import decoded_save
base=Path('.local-work/workshop-population-rework');out=base/'specialist';guard()
inputs=[base/'papyrus-leads01.json',out/'native84.tsv',out/'native85.tsv',Path(__file__)]
pins=[identity(p) for p in inputs];old=json.loads(inputs[0].read_text());src=old['source'];assert identity(Path(src['path']))==src
with decoded_save(Path(src['path']),out/'papyrus-scratch18') as (b,metrics):
 unit=old['unit'];a,z=unit['body'],unit['end'];rows=[]
 for r in old['rows']:
  fid=int(r['identity'].split(':')[1],16);assert 0xff000000<=fid<=0xfffffffe
  token=(0x800000|fid)&0xffffff;pattern=token.to_bytes(3,'big');positions=[];p=a
  while True:
   p=b.find(pattern,p,z)
   if p<0:break
   prefix=struct.unpack_from('<HH',b,p-4) if p-4>=a else None
   positions.append(dict(formref_offset=p,prefix_kind=prefix[0] if prefix else None,prefix_aux=prefix[1] if prefix else None,handle_start=p-4 if prefix else None,context_start=max(a,p-12),context=b[max(a,p-12):min(z,p+20)].hex(),native_handle_prefix_candidate=prefix is not None and prefix[0] in (0,1,2)));p+=1
  assert [x['formref_offset'] for x in positions]==r['patterns']['FormRefBE']
  rows.append(dict(identity=r['identity'],direct_writer_formref=pattern.hex(),BE_occurrences=positions,LE_occurrences=r['patterns']['FormRefLE'],necessary_formref_present=bool(positions)))
assert identity(Path(src['path']))==src and [identity(p) for p in inputs]==pins
with (out/'papyrus-handle-leads18.json').open('x',encoding='utf8') as f:json.dump(dict(inputs=pins,source=src,unit=unit,decode=metrics,rows=rows,limits='Necessary direct-handle encoding audit only. Candidate prefix validity does not establish table grammar or identify a script/property. LE scalar/index leads remain unclassified until native table producer/consumer is recovered.'),f,indent=2);f.write('\n')
print(len(rows),sum(r['necessary_formref_present'] for r in rows),sum(p['native_handle_prefix_candidate'] for r in rows for p in r['BE_occurrences']))
