"""SPDX-License-Identifier: GPL-3.0-or-later
Original research probe; read installed DFOB/DOBJ/TES4, preserve source hashes,
write only fresh ignored local JSON. Stdlib/project ESM reader, 40GB guards,
no external programs, engine/database/Git/network effects. Raw fields local only.
"""
from pathlib import Path
import json
import sys
import argparse

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'save-analysis/scripts'))
from inspect_outpost_definitions import esm_records
from inventory_historical_saves import identity, guard

guard()
ap = argparse.ArgumentParser()
ap.add_argument('--run', required=True)
args = ap.parse_args()
if not args.run.replace('-', '').isalnum(): raise ValueError('RUN_NAME')
cache = ROOT/'.local-work/extractor-resource/run01/static-records.json'
cache_before = identity(cache)
pins = json.loads(cache.read_text(encoding='utf8'))['sources']
records, sources = [], []
for expected in pins:
    path = Path(expected['path']); before = identity(path)
    if before['sha256'] != expected['sha256']: raise ValueError('SOURCE_PIN')
    for row, fields in esm_records(path, {b'DFOB', b'DOBJ', b'TES4'}, repeated=True):
        records.append(dict(plugin=path.name, **row,
            edid=next((v.rstrip(b'\0').decode('utf8') for k, v in fields if k == b'EDID'), ''),
            fields=[(k.decode('ascii'), v.hex()) for k, v in fields]))
    if identity(path) != before: raise ValueError('SOURCE_CHANGED')
    sources.append(before)
if identity(cache) != cache_before: raise ValueError('CACHE_CHANGED')
out = ROOT/'.local-work/resource-availability'/(args.run+'.json')
with out.open('x', encoding='utf8', newline='\n') as f:
    json.dump(dict(records=records, sources=sources, cache=cache_before, script=identity(Path(__file__))), f, indent=2)
    f.write('\n')
guard()
print('records', len(records), 'sources', len(sources))
