import json,sys,struct,zlib,collections
from pathlib import Path
sys.path.insert(0,'save-analysis/scripts')
from workshop_definition_context import context
from inspect_outpost_definitions import esm_records,subrecords
from extractor_resources import qualified
from inventory_historical_saves import identity,guard
out=Path('.local-work/workshop-population-rework');x=json.loads((out/'default-links-01.json').read_text(encoding='utf8'));links=x['workshop_links']
wanted={r[k] for r in links for k in ('reference','target')};paths=[Path(r['path']) for r in x['sources']]
assert [identity(p) for p in paths]==x['sources'];guard()
ctx=context(paths,wanted);headers={}
for p in paths:
 r,fs=next(esm_records(p,{b'TES4'},repeated=True));headers[p.name.lower()]=dict(flags=r['flags'],masters=[v.rstrip(b'\0').decode().lower() for t,v in fs if t==b'MAST'])
flags={p:h['flags'] for p,h in headers.items()};byname={p.name.lower():p for p in paths}
for key,variants in ctx['records'].items():
 for r in variants:
  plugin=r['plugin'].lower();h=headers[plugin]
  def q(fid):return qualified(plugin,fid,h['masters'],flags)
  with byname[plugin].open('rb') as f:
   f.seek(r['offset']);rh=f.read(24);size=int.from_bytes(rh[4:8],'little');raw=f.read(size)
  if r['flags']&0x40000:
   n=int.from_bytes(raw[:4],'little');dec=zlib.decompressobj();raw=dec.decompress(raw[4:],n+1);assert dec.eof and len(raw)==n and not dec.unused_data and not dec.unconsumed_tail
  fs=list(subrecords(raw));names=[v for t,v in fs if t==b'NAME'];assert all(len(v)==4 for v in names)
  r['base_identities']=[q(int.from_bytes(v,'little')) for v in names]
  r['linked_defaults']=[dict(keyword=q(k),target=q(t)) for tag,v in fs if tag==b'XLKR' for k,t in struct.iter_unpack('<II',v)]
assert [identity(p) for p in paths]==x['sources']
(out/'default-catalog01.json').open('x',encoding='utf8').write(json.dumps(ctx,indent=2)+'\n')
print('targets',[(k,[(r['base_identities'],r['editor_id']) for r in ctx['records'].get(k,[])]) for k in sorted({r['target'] for r in links})],flush=True)
bases={b for vs in ctx['records'].values() for r in vs for b in r['base_identities']};bc=context(paths,bases)
(out/'default-bases01.json').open('x',encoding='utf8').write(json.dumps(bc,indent=2)+'\n')
print('PASS',len(ctx['records']),len(bc['records']))
