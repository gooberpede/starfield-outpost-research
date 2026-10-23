# SPDX-License-Identifier: GPL-3.0-or-later
"""Finish the D1 preparation pipeline with measured field-count inventory.

Reads only the completed corpus variants and local builder manifest; exclusively
writes an ignored local count/size receipt. Stdlib only, no installed inputs,
target operations or source mutations. Counts describe serialized operands,
not scientific coverage or a mathematical minimum.
"""
import argparse
import collections
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]


def leaf_counts(value):
    counts=collections.Counter()
    if isinstance(value,dict):
        for child in value.values():counts.update(leaf_counts(child))
    elif isinstance(value,list):
        for child in value:counts.update(leaf_counts(child))
    else:
        counts[type(value).__name__]+=1
    return counts


def run(build,output):
    if not output.resolve().is_relative_to(ROOT/'.local-work') or output.exists():
        raise ValueError('fresh ignored output required')
    rows=[];pins={}
    manifest=json.loads((build/'manifest.json').read_text())
    for name in ('normalized','expanded'):
        path=build/f'{name}.json';raw=path.read_bytes();pins[str(path)]=hashlib.sha256(raw).hexdigest()
        expected=next(row['sha256'] for row in manifest['variants'] if row['representation']==name)
        if pins[str(path)]!=expected:raise ValueError('completed corpus pin mismatch')
        c=json.loads(raw)['payload'];bodies=list(c['bodies'].values())
        row=dict(representation=name,bytes=len(raw),body_rows=len(bodies),
            constants=len(c['constants']),settings=len(c['settings']),maximum_width_fields=1,
            generation_float_fields=sum(map(len,c['generation_blocks'].values())),
            body_key_integer_fields=2*len(bodies),tile_scalar_fields=sum(len(t) for b in bodies for t in b['tiles'].values()),
            biome_status_fields=sum(len(b['biomes']) for b in bodies),
            resource_scalar_fields=sum(3*len(v['resources']) for b in bodies for v in b['biomes'].values()),
            payload_leaf_value_counts=dict(leaf_counts(c)))
        if name=='normalized':
            row.update(pattern_pairs=sum(map(len,c['patterns'].values())),
                source_dimension_integer_fields=sum(map(len,c['source_blocks'].values())))
        else:
            routes=[r for b in bodies for entries in b['routes'].values() for r in entries]
            row.update(route_slots=len(routes),unresolved_route_slots=sum(r is None for r in routes),
                resolved_route_scalar_fields=sum(len(r) for r in routes if r is not None))
        rows.append(row)
    receipt=dict(schema='sor-d1-field-inventory/1',publication='LOCAL-ONLY',inputs=pins,
        builder_manifest_sha256=hashlib.sha256((build/'manifest.json').read_bytes()).hexdigest(),
        inventory_source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),variants=rows,
        method='Counts actual payload leaves, excluding object-key spelling and envelope digest from leaf count')
    if any(hashlib.sha256(Path(p).read_bytes()).hexdigest()!=h for p,h in pins.items()):
        raise ValueError('corpus changed during inventory')
    with output.open('x',encoding='utf8',newline='\n') as f:
        json.dump(receipt,f,indent=2);f.write('\n')
    print(json.dumps(rows))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--build',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True);args=parser.parse_args();run(args.build,args.output)
