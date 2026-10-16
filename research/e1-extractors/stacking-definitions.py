# SPDX-License-Identifier: GPL-3.0-or-later
"""Original bounded offline Research Project/recipe field inventory.
Reads pinned installed Starfield.esm through the owned stdlib ESM reader; writes
exclusive ignored numeric field JSON. No game/save/project/process/network/index
effects; requires repository cwd, installed CPython and C:/D: disk guard.
Raw fields remain LOCAL-ONLY. No outside implementation or dependencies.
"""
from pathlib import Path
import hashlib
import json
import sys
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'save-analysis/scripts'))
from inspect_outpost_definitions import esm_records
from inventory_historical_saves import guard

guard()
path = Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield/Data/Starfield.esm')
def sha(p):
    with p.open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()
pin = sha(path)
assert pin == '1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7'
rows = []
for header, fields in esm_records(path, {b'RSPJ', b'COBJ'}, repeated=True):
    rows.append(dict(**header, edid=next((v.rstrip(b'\0').decode('utf8') for k,v in fields if k==b'EDID'), ''),
                     fields=[(k.decode(),v.hex()) for k,v in fields]))
assert sha(path) == pin
out = ROOT/'.local-work/e1-stacking/research-definitions01.json'
with out.open('x',encoding='utf8',newline='\n') as f:
    json.dump(dict(source=str(path), sha256=pin, records=rows), f, indent=2)
    f.write('\n')
guard()
print({kind:sum(r['type']==kind for r in rows) for kind in ['RSPJ','COBJ']})
for r in rows:
    if r['type']=='RSPJ':
        print(f"{r['formid']:08x}",r['offset'],r['edid'],[(k,v) for k,v in r['fields'] if k not in {'EDID','DESC','FULL','MODL','CTDA'}])
