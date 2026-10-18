# SPDX-License-Identifier: GPL-3.0-or-later
"""R1 metadata-first historical robot scan, repository cwd, installed CPython.

Reads frozen 278-input metadata, then bounded mature supported originals; owned
stream/typed/prefix/extra readers. Writes exclusive local receipts, metadata CSV.
No original/target/database/Git/network writes. Does not infer absence from gaps.
Adapted CR1 corpus.py and CR3 scan.py; raw bodies remain local. Guard each input.
"""
from pathlib import Path
import argparse
import sys,json,struct,csv,collections
R=Path.cwd();W=R/'.local-work/r1-robots';D=R/'docs/experiments/robots'
sys.path[:0]=[str(R/'research/cr1-crew'),str(R/'save-analysis/scripts'),str(R/'.local-work/cr1-crew'),str(R/'research/cr2-skills')]
import hashlib
def pin(path):
 with path.open('rb') as f:return dict(path=str(path),bytes=path.stat().st_size,sha256=hashlib.file_digest(f,'sha256').hexdigest())
from current import actor_prefix,explicit_actor_links
from crew_extras import extra_view
from inventory_historical_saves import guard
from stream_save import decoded_save
from extractor_resources import plugin_tables,saved_form
from outpost_membership import token_value
from validate_mature_outposts import directory
from workshop_population import typed_records,initial_prefix
ROBOTS={f'starfield.esm:{x:06x}' for x in [0x4297c,0x4297d,0xbd67e,0x1d8ee5,0x1d924e,0x1d9250,0x1f416e,0x337eab]}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--extend',action='store_true');args=ap.parse_args()
 guard(); inv=json.loads((R/'.local-work/historical-inventory/scan-01/inventory.json').read_text())
 prior={p.stem:json.loads(p.read_text()) for p in (R/'.local-work/cr1-current/corpus').glob('*.json')}
 selected=[];ledger=[]
 for row in inv:
  label=row['inventory_id']; old=prior.get(label)
  # Existing CR1 metadata selection is a reproducible mature stratum. Later
  # mature metadata inputs are added after the initial search if needed.
  choose=old is not None and 'error' not in old
  if args.extend and old is None:
   choose=row['metadata']['level_candidate']['value']>=290 and row['metadata']['build_strings'][0]['text']=='1.16.244.0' and row['framing']['declared_decoded_size']<=64*1024*1024
  ledger.append(dict(sample=label,sha256=row['source']['sha256'],inventory_status=row['status'],selected=choose,reason=('MATURE_CR1_SUPPORTED' if old else 'EXTENDED_MATURE_CURRENT') if choose else old.get('error','OUTSIDE_INITIAL_MATURE_STRATUM') if old else 'OUTSIDE_INITIAL_MATURE_STRATUM'))
  if choose:selected.append((label,row['source']))
 with (D/'corpus.csv').open('w',encoding='utf8',newline='') as f:
  w=csv.DictWriter(f,list(ledger[0]),lineterminator='\n');w.writeheader();w.writerows(ledger)
 invout=W/('inventory02.json' if args.extend else 'inventory01.json')
 if not invout.exists():invout.open('x',encoding='utf8').write(json.dumps(dict(total=len(inv),selected=len(selected),method='All supported CR1 mature inputs; extension adds remaining current-build mature <=64MiB metadata inputs to seek robot-only owners' if args.extend else '278 frozen protected metadata inputs; all supported CR1 mature inputs selected before robot content search'),indent=2)+'\n')
 for label,src in selected:
  out=W/(label+'.json')
  if out.exists():continue
  guard();path=Path(src['path'])
  if not path.exists():
   out.open('x',encoding='utf8').write(json.dumps(dict(source=src,missing=True,locator_check='Frozen source absent; existing_archives empty; no absence inference'),indent=2)+'\n');print(label,'MISSING original',flush=True);continue
  before=pin(path);assert before['sha256']==src['sha256']
  result=dict(source=before,robots=[],owners=[],actor_prefix_gaps=collections.Counter())
  with decoded_save(path,W/'scratch') as (data,decoded):
   result['decoded']=decoded;dr=directory(data);forms=struct.unpack_from('<'+'I'*dr['reference_count'],data,dr['regions']['reference_u32'][0]+4);plugins=plugin_tables(data)
   def resolve(t):return saved_form(token_value(t,forms),plugins)
   for rec in typed_records(data):
    if rec['form_type'] not in [0x4a,0x4b]:continue
    try:p=actor_prefix(data,rec) if rec['form_type']==0x4b else initial_prefix(data,rec)
    except (ValueError,struct.error) as e:
     if rec['form_type']==0x4b:result['actor_prefix_gaps'][str(e)]+=1
     continue
    base=resolve(p['base_token']) if p.get('base_token') else None
    if base not in ROBOTS and base!='starfield.esm:2c60e9':continue
    r=dict(identity=resolve(rec['token']),base=base,record=rec,prefix=p,queue=[resolve(t) for t in rec['refs']],body_hex=bytes(data[rec['body']:rec['end']]).hex())
    try:r['extras']=extra_view(data,rec,p,resolve)
    except (ValueError,struct.error) as e:r['extra_gap']=str(e)
    if base in ROBOTS:
     try:r['links']=explicit_actor_links(data,rec,resolve)
     except (ValueError,struct.error) as e:r['link_gap']=str(e)
     result['robots'].append(r)
    else:result['owners'].append(r)
  assert pin(path)==before;result['source_unchanged']=True
  out.open('x',encoding='utf8').write(json.dumps(result,indent=2)+'\n')
  print(label,'robots',len(result['robots']),'owners',len(result['owners']),flush=True)
 guard()
if __name__=='__main__':main()
