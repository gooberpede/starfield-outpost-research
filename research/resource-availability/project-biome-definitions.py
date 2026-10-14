"""SPDX-License-Identifier: GPL-3.0-or-later
Original offline BIOM/RSGD/IRES identity projection. Reads explicit local primary
record receipts, resolves each file's masters/compact domain via owned reader,
retains differing overrides as UNKNOWN, exclusively writes ignored local JSON.
No live, ESM, target/database/Git/network writes or external dependency.
"""
from pathlib import Path
import argparse
from collections import defaultdict, Counter
import json
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'save-analysis/scripts'))
from extractor_resources import fields, qualified, u32
from resource_availability import biome_rnam_resources
from inventory_historical_saves import guard, identity

ap = argparse.ArgumentParser()
ap.add_argument('--definitions', type=Path, required=True)
ap.add_argument('--run', required=True)
args = ap.parse_args()
if not args.run.replace('-', '').isalnum(): raise ValueError('RUN_NAME')
guard()
ires = ROOT/'.local-work/extractor-resource/run01/static-records.json'
pins = {str(p):identity(p) for p in (ires,args.definitions)}
rs = json.loads(ires.read_text(encoding='utf8'))['records']+json.loads(args.definitions.read_text(encoding='utf8'))['records']
masters = {r['plugin'].lower():[v.rstrip(b'\0').decode('utf8').lower() for v in fields(r,'MAST')]
           for r in rs if r['type']=='TES4'}
flags = {r['plugin'].lower():r['flags'] for r in rs if r['type']=='TES4'}
def q(r,fid):
    p = r['plugin'].lower()
    return qualified(p,fid,masters[p],flags)
versions = defaultdict(list)
for r in rs:
    if r['type'] not in ('BIOM','RSGD','IRES'): continue
    if r['type'] == 'RSGD':
        pending, paired = None, []
        for tag, raw in r['fields']:
            value = bytes.fromhex(raw)
            if tag == 'RNAM':
                if pending is not None: raise ValueError('RSGD_UNPAIRED_RNAM')
                pending = u32(value)
                if not pending: raise ValueError('RSGD_NULL_RNAM_UNQUALIFIED')
            elif tag == 'DNAM':
                if pending is None or len(value) != 560: raise ValueError('RSGD_DNAM_SAMPLE_DOMAIN')
                paired.append(q(r,pending)); pending = None
        if pending is not None: raise ValueError('RSGD_UNPAIRED_RNAM')
        edges = tuple(paired)
    else:
        edges = tuple(q(r,u32(v)) for v in fields(r,'RNAM')) if r['type']=='BIOM' else ()
    # Absent BIOM/RSGD list field is an explicit semantic gap here, not empty terrain.
    if r['type']!='IRES' and not fields(r,'RNAM'): edges = None
    versions[q(r,r['formid'])].append(dict(kind=r['type'],rnam=edges))
definitions = {key:rows[0] if all(r==rows[0] for r in rows) else None for key,rows in versions.items()}
results = {key:biome_rnam_resources(key,definitions) for key,rows in versions.items() if rows[0]['kind']=='BIOM'}
summary = dict(status_counts=dict(Counter(r['status'] for r in results.values())),
               water_declared_count=sum('starfield.esm:0083ec' in (r['resource_set'] or []) for r in results.values()),
               rsgd_pair_domain='nonzero u32 RNAM followed by observed 560-byte DNAM; geometry not decoded')
if {p:identity(Path(p)) for p in pins} != pins: raise ValueError('INPUT_CHANGED')
out = ROOT/'.local-work/resource-availability'/(args.run+'.json')
with out.open('x', encoding='utf8', newline='\n') as f:
    json.dump(dict(results=results, summary=summary, definition_context=definitions,
                   conflicts=[k for k,v in definitions.items() if v is None],
                   inputs=pins, script=identity(Path(__file__))), f, indent=2)
    f.write('\n')
guard()
print(summary)
