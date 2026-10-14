"""SPDX-License-Identifier: GPL-3.0-or-later
Original complete selected ATMO/BIOM/RSGD installed-record census. Reads pinned
38 ESM sources and owned parser, exclusively writes ignored local fields/offsets
with before/after hashes. No target/analysis/Git/network effects. 40GB guard.
Raw definition fields are local evidence, never publication artifacts.
"""
from pathlib import Path
import argparse
import json
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'save-analysis/scripts'))
from inspect_outpost_definitions import esm_records
from inventory_historical_saves import identity, guard

ap = argparse.ArgumentParser()
ap.add_argument('--run', required=True)
args = ap.parse_args()
if not args.run.replace('-', '').isalnum(): raise ValueError('RUN_NAME')
guard()
cache = ROOT/'.local-work/extractor-resource/run01/static-records.json'
cache_before = identity(cache)
sources = json.loads(cache.read_text(encoding='utf8'))['sources']
records, pins = [], []
for s in sources:
    p = Path(s['path']); before = identity(p)
    if before['sha256'] != s['sha256']: raise ValueError('ESM_SOURCE_PIN')
    for r, fs in esm_records(p, {b'TES4', b'ATMO', b'BIOM', b'RSGD'}, repeated=True):
        records.append(dict(plugin=p.name, **r,
            edid=next((v.rstrip(b'\0').decode('utf8','backslashreplace') for k,v in fs if k==b'EDID'), ''),
            fields=[(k.decode('ascii'), v.hex()) for k,v in fs]))
    if identity(p) != before: raise ValueError('ESM_CHANGED')
    pins.append(before)
if identity(cache) != cache_before: raise ValueError('CACHE_CHANGED')
out = ROOT/'.local-work/resource-availability'/(args.run+'.json')
with out.open('x', encoding='utf8', newline='\n') as f:
    json.dump(dict(records=records, sources=pins, cache=cache_before, script=identity(Path(__file__))),f,indent=2)
    f.write('\n')
guard()
from collections import Counter
print(dict(Counter(r['type'] for r in records)))
