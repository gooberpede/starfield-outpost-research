# SPDX-License-Identifier: GPL-3.0-or-later
"""Bounded L1 read-only saved corroboration; repository cwd, CPython -B.

Reads frozen metadata and selected original saves, L1 definitions, owned typed
reference/prefix/link readers and prior supported root ledger. Writes exclusive
ignored JSON per sample; raw bytes remain local. No game, original-save,
database, Git or network effects. Both-drive guard and source rehashes apply.
Unknown leading extras/prefixes remain explicit gaps, never absence evidence.
Owned methods: R1 scan.py/links.py, CR1 extra_view, Workshop population framing.
"""
from pathlib import Path
import sys,json,struct,collections,argparse,hashlib
R=Path.cwd();W=R/'.local-work/l1-limits'
sys.path[:0]=[str(R/'research/r1-robots'),str(R/'research/cr1-crew'),str(R/'save-analysis/scripts'),str(R/'.local-work/cr1-crew')]
from links import actor_prefix,explicit_actor_links
from crew_extras import extra_view
from inventory_historical_saves import guard
from stream_save import decoded_save
from extractor_resources import plugin_tables,saved_form
from outpost_membership import token_value
from validate_mature_outposts import directory
from workshop_population import typed_records,initial_prefix
from workshop_population_extras import partial_extras

def pin(p):
 with p.open('rb') as f:return dict(path=str(p),bytes=p.stat().st_size,sha256=hashlib.file_digest(f,'sha256').hexdigest())

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--samples',nargs='+',required=True);a=ap.parse_args();guard()
 inv=json.loads((R/'.local-work/historical-inventory/scan-01/inventory.json').read_text());inputs={r['inventory_id']:r['source'] for r in inv}
 for r in json.loads((R/'.local-work/workshop-inventory/inputs27.json').read_text()):
  if r['series']=='manual-S0-S7C':inputs[r['label']]=r['pin']
 defs=json.loads((W/'definitions01.json').read_text())['records'];recipes=[r for r in defs if r['type']=='COBJ' and dict(r['fields']).get('JNAM')=='967c0f00'];turrets={f"starfield.esm:{int.from_bytes(bytes.fromhex(dict(r['fields'])['CNAM']),'little'):06x}" for r in recipes}
 for label in a.samples:
  assert label in inputs;src=inputs[label];path=Path(src['path']);before=pin(path);assert before['sha256']==src['sha256'];guard();out=W/('save-'+label+'.json');assert not out.exists()
  result=dict(source=before,label=label,turrets=[],beacons=[],player=[],prefix_gaps=collections.Counter(),record_count=0)
  with decoded_save(path,W/'scratch') as (data,decoded):
   result['decoded']=decoded;dr=directory(data);forms=struct.unpack_from('<'+'I'*dr['reference_count'],data,dr['regions']['reference_u32'][0]+4);plugins=plugin_tables(data)
   def resolve(t):return saved_form(token_value(t,forms),plugins)
   for rec in typed_records(data):
    result['record_count']+=1
    if rec['form_type'] not in [0x4a,0x4b]:continue
    try:p=actor_prefix(data,rec) if rec['form_type']==0x4b else initial_prefix(data,rec)
    except (ValueError,struct.error) as e:result['prefix_gaps'][str(e)]+=1;continue
    base=resolve(p['base_token']) if p.get('base_token') else None;ident=resolve(rec['token'])
    if base not in turrets and base!='starfield.esm:2c60e9' and ident!='starfield.esm:000014':continue
    row=dict(identity=ident,base=base,record=rec,prefix=p,queue=[resolve(t) for t in rec['refs']],body_hex=bytes(data[rec['body']:rec['end']]).hex())
    if base in turrets:
     try:row['links']=explicit_actor_links(data,rec,resolve)
     except (ValueError,struct.error) as e:row['link_gap']=str(e)
     result['turrets'].append(row)
    elif ident=='starfield.esm:000014':
     try:row['extras']=extra_view(data,rec,p,resolve)
     except (ValueError,struct.error) as e:row['extra_gap']=str(e)
     result['player'].append(row)
    else:
     try:row['extras']=extra_view(data,rec,p,resolve)
     except (ValueError,struct.error) as e:row['extra_gap']=str(e)
     result['beacons'].append(row)
  assert before==pin(path);result['source_unchanged']=True
  out.open('x',encoding='utf8').write(json.dumps(result,indent=2)+'\n');print(label,'turrets',len(result['turrets']),'beacons',len(result['beacons']),'player',len(result['player']),flush=True)
 guard()
if __name__=='__main__':main()
