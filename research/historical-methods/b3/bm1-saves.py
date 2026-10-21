"""BM1 selected historical positive-witness search. Reads pinned originals via
protected stream reader, writes exclusive ignored JSON; scratch context-cleaned.
Uses owned prefix/extras grammar, adds native B4/u32 and DE/counted rows from
BM1 n011/n013. Unsupported extras stop; no absence or loaded-state inference.
"""
from pathlib import Path
import sys,json,struct,collections,hashlib,inspect
R=Path.cwd();W=R/'.local-work/construction-variants'
sys.path[:0]=[str(R/'.local-work/cr1-crew'),str(R/'save-analysis/scripts'),str(R/'research/s1-storage')]
from inventory_historical_saves import guard
from stream_save import decoded_save
from extractor_resources import plugin_tables,saved_form
from outpost_membership import token_value
from validate_mature_outposts import directory
from workshop_population import typed_records,initial_prefix
from catalog import pin
import crew_extras
# Source-informed adaptation of maintainer-owned parser, not a new save grammar.
source=inspect.getsource(crew_extras.extra_view)
source=source.replace("elif tag == 0x9c:","elif tag == 0x9c:")
source=source.replace("if tag == 0x9c:","if tag == 0xb4:\n            row['original_base_u32'] = int.from_bytes(c.take(4), 'little')\n        elif tag == 0xde:\n            row['connections'] = []\n            for _ in range(c.count()):\n                target = refs(1)[0]\n                row['connections'].append(dict(target=target, pairs=[list(struct.unpack('<ii', c.take(8))) for _ in range(c.count())]))\n        elif tag == 0x9c:")
scope=dict(crew_extras.__dict__);exec(source,scope);view=scope['extra_view']
(W/'extras-adapted.py').write_text(source,encoding='utf8',newline='\n') if not (W/'extras-adapted.py').exists() else None
definitions=json.loads((W/'definitions02.json').read_text());by={r['formid']:r for r in definitions['records']}
habbeh=[r for r in by.values() if r['type']=='STBH' and r['edid'].startswith('OB_') and ('Hab' in r['edid'] or 'Airlock' in r['edid'] or 'Cargo' in r['edid'])]
targets={int.from_bytes(bytes.fromhex(v),'little') for r in habbeh for k,v in r['fields'] if k=='PNAM'}
candidates={0x15804,0x2c60e9}|targets|{r['formid'] for r in by.values() if r['type'] in ['STAT','PKIN','CONT','ACTI','DOOR'] and any(s in r['edid'].lower() for s in ['opi','ophhab','opshab','opmhab','outpoststorage','airlock'])}
inventory=json.loads((R/'.local-work/historical-inventory/scan-01/inventory.json').read_text());inv={r['inventory_id']:r for r in inventory}
for label in sys.argv[1:]:
 guard();src=inv[label]['source'];path=Path(src['path']);before=pin(path);assert before['sha256']==src['sha256'] and before['bytes']==src['size']
 out=W/('saved2-'+label+'.json');assert not out.exists();rows=[];counts=collections.Counter();gaps=collections.Counter()
 with decoded_save(path,W/'save-scratch') as (data,decoded):
  dr=directory(data);forms=struct.unpack_from('<'+'I'*dr['reference_count'],data,dr['regions']['reference_u32'][0]+4);plugins=plugin_tables(data)
  def resolve(t):return saved_form(token_value(t,forms),plugins)
  for rec in typed_records(data):
   counts['all_records']+=1
   if rec['form_type']!=0x4a:continue
   counts['REFR']+=1
   try:p=initial_prefix(data,rec)
   except (ValueError,struct.error) as e:gaps[str(e)]+=1;continue
   base=resolve(p['base_token']) if p.get('base_token') else None
   if base is None or not base.startswith('starfield.esm:') or int(base.split(':')[1],16) not in candidates:continue
   row=dict(identity=resolve(rec['token']),base=base,editorid=by[int(base.split(':')[1],16)]['edid'],record=rec,prefix=p)
   try:row['extras']=view(data,rec,p,resolve)
   except (ValueError,struct.error) as e:row['extra_gap']=str(e)
   rows.append(row)
 assert pin(path)==before
 j=dict(label=label,source=before,unchanged=True,decoded=decoded,counts=counts,prefix_gaps=gaps,candidate_base_count=len(candidates),rows=rows,grammar_source=pin(R/'.local-work/cr1-crew/crew_extras.py'),adaptation=pin(W/'extras-adapted.py'))
 out.open('x',encoding='utf8').write(json.dumps(j,indent=2)+'\n')
 positives=[(r['identity'],r['editorid'],[(e['type'],e.get('original_base_u32'),e.get('connections')) for e in r.get('extras',{}).get('extras',[]) if e['type'] in ['b4','de']]) for r in rows]
 print(label,'rows',len(rows),'with B4/DE',sum(bool(r[2]) for r in positives),positives[:2],flush=True)
guard()
