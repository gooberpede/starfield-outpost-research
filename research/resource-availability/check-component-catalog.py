"""SPDX-License-Identifier: GPL-3.0-or-later
Read existing qualified component receipts and fresh replay; compare exact audit
objects, inventory field domains and source pins. Exclusive ignored output only.
No target/save/database/network/Git effects. No wire word is a runtime owner ID
without native storage-ID resolution. CTName is not a saved-type registry.
Prerequisite: research_workshop_components.py --labels S1 Save52 fresh replay.
"""
from pathlib import Path
import argparse
import json
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'save-analysis/scripts'))
from inventory_historical_saves import identity, guard

ap = argparse.ArgumentParser()
ap.add_argument('--fresh', required=True)
ap.add_argument('--run', required=True)
a = ap.parse_args()
if not a.run.replace('-', '').isalnum(): raise ValueError('RUN_NAME')
guard()
rows, pins = [], {}
for label in ('S1', 'Save52'):
    old = ROOT/'.local-work/workshop-population-rework/components02'/(label+'.json')
    fresh = Path(a.fresh)/(label+'.json')
    for path in (old, fresh): pins[str(path)] = identity(path)
    x, y = [json.loads(p.read_text(encoding='utf8')) for p in (old, fresh)]
    for key in ('unit', 'names', 'sections', 'exact_body_closure', 'source', 'label'):
        if x[key] != y[key]: raise ValueError(('REPLAY_MISMATCH', label, key))
    if x['decode']['decoded_sha256'] != y['decode']['decoded_sha256']:
        raise ValueError('DECODE_MISMATCH')
    source = Path(y['source']['path'])
    if identity(source) != y['source']: raise ValueError('ORIGINAL_CHANGED')
    pins[str(source)] = identity(source)
    rows.append(dict(label=label, exact_replay=True, sections=len(y['sections']),
                     exact_body_closure=y['exact_body_closure'],
                     ctname_count=len(y['names']),
                     section_names=[s['name'] for s in y['sections']],
                     runtime_owner_scalar=259487,
                     runtime_owner_to_wire_storage_id='UNRESOLVED',
                     ctperbiome_to_stream_fields='UNRESOLVED',
                     same_invocation_spatial_biome='UNKNOWN',
                     complete_region_array='UNKNOWN'))
for path, pin in pins.items():
    if identity(Path(path)) != pin: raise ValueError('INPUT_CHANGED')
guard()
result = dict(schema='resource-component-catalog/1', rows=rows, pins=pins,
              statement='Exact sampled framing replay; no verified CTPerBiome stream mapping. '
                        'No literal owner-word or type-name absence is persistence proof.')
out = ROOT/'.local-work/resource-availability'/(a.run+'.json')
with out.open('x', encoding='utf8', newline='\n') as f:
    json.dump(result, f, indent=2); f.write('\n')
print('PASS exact component replay; source mapping UNRESOLVED')
