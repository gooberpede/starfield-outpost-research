"""Original selective type4 context join. Reads all installed ESM headers and
exact wanted static definitions plus pinned local type4/R3 receipts; exclusive
specialist JSON only. No target/DB effects, no third-party implementation.
"""
import json,sys,collections
from pathlib import Path
sys.path.insert(0,'save-analysis/scripts')
from workshop_definition_context import context
from inventory_historical_saves import identity
base=Path('.local-work/workshop-population-rework');out=base/'specialist'
inputs=[out/'type4-census01.json',base/'typed-full03/mature-Save52.json',base/'definition-80.json',Path(__file__)]
pins=[identity(p) for p in inputs];census=json.loads(inputs[0].read_text());typed=json.loads(inputs[1].read_text());ctx=json.loads(inputs[2].read_text())
saved={r['identity']:r for r in typed['references']}
identities={r['identity'] for x in census['results'] for r in x['typed_references'] if r['identity']}
wanted={s for s in identities if not s.startswith('DYNAMIC:')}
for s in identities:
 r=saved.get(s,{});p=r.get('prefix') or {};baseid=p.get('base_identity') or r.get('base_identity')
 if baseid and not baseid.startswith('DYNAMIC:'):wanted.add(baseid)
data=Path(r'C:/Program Files (x86)/Steam/steamapps/common/Starfield/Data')
paths=[p for p in data.glob('*.esm') if p.name in ctx['header_census']];assert len(paths)==38
definitions=context(paths,wanted)
rows=[]
for s in sorted(identities):
 r=saved.get(s);rows.append(dict(identity=s,definitions=definitions['records'].get(s,[]),saved_reference=r))
assert [identity(p) for p in inputs]==pins
result=dict(schema='type4-exact-context/1',inputs=pins,definition_context=definitions,rows=rows,limits='All override variants retained; no load-order inference. A missing R3 does not mean nonexistent. Component names and PKIN classes alone do not establish ships-only semantics.')
with (out/'type4-context01.json').open('x',encoding='utf8') as f:json.dump(result,f,indent=2);f.write('\n')
print('identities',len(identities),'static',len(wanted),'found',len(definitions['records']),'types',dict(collections.Counter(v['record_type'] for variants in definitions['records'].values() for v in variants)))
