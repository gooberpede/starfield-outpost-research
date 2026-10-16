# SPDX-License-Identifier: GPL-3.0-or-later
"""Original bounded offline definition inventory for E1 continuation.
Reads installed Starfield.esm with the established owned stdlib ESM reader;
writes exclusive ignored PERK metadata/fields and selection summaries. No game,
save, analysis-project or network effects; no outside dependencies. Requires
repository cwd, installed CPython, pinned ESM and C:/D: free-space guards.
Full field inventory is LOCAL-ONLY. This is not an economic simulator.
"""
from pathlib import Path
import hashlib
import json
import sys
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'save-analysis/scripts'))
from inspect_outpost_definitions import esm_records
from inventory_historical_saves import guard

def pin(p):
    with p.open('rb') as f:
        h = hashlib.file_digest(f, 'sha256').hexdigest()
    return dict(path=str(p), size=p.stat().st_size, sha256=h)

guard()
p = Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield/Data/Starfield.esm')
before = pin(p)
assert before['sha256'] == '1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7'
rows = []
for header, fs in esm_records(p, {b'PERK'}, repeated=True):
    rows.append(dict(**header, edid=next((v.rstrip(b'\0').decode('utf8') for k,v in fs if k==b'EDID'), ''),
                     fields=[(k.decode(),v.hex()) for k,v in fs]))
assert before == pin(p)
out = ROOT/'.local-work/e1-production/perks01.json'
out.open('x', encoding='utf8', newline='\n').write(json.dumps(dict(source=before, records=rows),indent=2)+'\n')
selected = [dict(formid=f"{r['formid']:08x}", offset=r['offset'], edid=r['edid'],
                 entries=[v for k,v in r['fields'] if k in {'PRKE','DATA','EPFT','EPFD','EPF2','EPF3'}])
            for r in rows if any(s in r['edid'].lower() for s in ['outpost','robot','magperk','magazine','resource','payload'])]
out = ROOT/'.local-work/e1-production/perk-selection01.json'
out.open('x',encoding='utf8',newline='\n').write(json.dumps(selected,indent=2)+'\n')
guard()
print('PERK records',len(rows),'selected',len(selected))
for r in selected:
    print(r['formid'],r['edid'],r['entries'])
