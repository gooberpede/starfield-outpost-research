# SPDX-License-Identifier: GPL-3.0-or-later
"""Authenticate inherited primary windows and cross-check complete native output.

Reads D5AG/D5AF geometry receipts, source ledgers and selected primary files.
Writes a fresh ignored JSON receipt and authored source-identity CSV. Stdlib
only; no native execution, game, save, database opening, network or Git mutation.
SOR-P-0002: project-owned source-ledger and geometry comparison conventions.
Stop on identity, output, binary schema, oracle or caller-space failure.
"""
from pathlib import Path
import csv
import hashlib
import json
import math
import struct
import sys

from d5ae_baseline import guard

ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / 'docs/experiments/resource-retained-population'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def population(run):
    """Keep order and duplicates; validate all represented native scalar bytes."""
    result = []
    for resource in run['population']:
        regions = []
        for region in resource['regions']:
            header = bytes.fromhex(region['header'])
            points = bytes.fromhex(region['points'])
            if len(header) != 24 or len(points) != region['count'] * 16:
                raise ValueError('Incomplete native representation')
            if not all(math.isfinite(x) for x in struct.unpack('<'+'f'*(len(points)//4), points)):
                raise ValueError('Nonfinite point operand')
            regions.append((header.hex(), region['count'], points.hex()))
        result.append((resource['resource'], regions))
    return result


def main():
    if not __debug__ or sys.flags.optimize:
        raise RuntimeError('Use Python -E -B')
    guard()
    out = (ROOT / '.local-work/d5ag' / sys.argv[1]).resolve()
    if not out.is_relative_to(ROOT / '.local-work/d5ag'):
        raise ValueError('Task-local output required')
    out.mkdir(exist_ok=False)
    selected = {
        'd5v-sources.csv': {'V-S021', 'V-S030'},
        'd5s-sources.csv': {'D5S-T01', 'D5S-T02', 'D5S-T03', 'D5S-T04', 'D5S-T05', 'D5S-T06'},
        'd5ad-sources.csv': {'D5AD-SV97', 'D5AD-SV134', 'D5AD-SV137', 'D5AD-SV146',
                           'D5AD-IN002', 'D5AD-SV27'},
    }
    sources = []
    for ledger, identifiers in selected.items():
        rows = list(csv.DictReader((DOC / ledger).open(encoding='utf8')))
        for identifier in sorted(identifiers):
            row = next(r for r in rows if r['id'] == identifier)
            path = ROOT / row['path']
            if sha(path) != row['sha256']:
                raise ValueError('Primary evidence drift: '+identifier)
            sources.append(dict(id='D5AG-'+identifier, path=row['path'].replace('\\', '/'),
                                sha256=row['sha256'], static_va=row['static_va'],
                                line_start=row.get('line_start', row.get('first_line')),
                                line_end=row.get('line_end', row.get('last_line')),
                                lineage=ledger+':'+identifier, eligibility='LOCAL-ONLY'))
    files = [ROOT / '.local-work' / task / name / 'control.json'
             for task, name in [('d5ag', 'geometry01'), ('d5ag', 'geometry02'),
                                ('d5af', 'geometry08'), ('d5af', 'geometry09')]]
    receipts = [json.loads(p.read_bytes()) for p in files]
    populations = [[population(run) for run in r['runs']] for r in receipts]
    if not all(p == populations[0] for p in populations):
        raise ValueError('Cross-process or inherited full-output mismatch')
    if populations[0][0] == populations[0][1] or populations[0][1] != populations[0][2]:
        raise ValueError('Contrast/repetition failed')
    if not all(all(x['exact_points_bounds'] for x in run['planar_model_comparison'])
               for r in receipts for run in r['runs']):
        raise ValueError('Independent planar oracle failed')
    totals = []
    for run in receipts[0]['runs']:
        totals.append(dict(query=run['original_query'], mask=run['low_mask'],
                           resources=len(run['population']),
                           regions=sum(len(r['regions']) for r in run['population']),
                           points=sum(v['count'] for r in run['population'] for v in r['regions'])))
    fields = list(sources[0])
    with (DOC / 'd5ag-sources.csv').open('w', encoding='utf8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator='\n')
        writer.writeheader()
        writer.writerows(sources)
    result = dict(method_sha256=sha(__file__), sources=sources,
                  inputs={str(p): sha(p) for p in files}, totals=totals,
                  complete_ordered_representations_equal_across_processes=True,
                  distinct_masks_differ=True, all_planar_oracles=True, free=guard(),
                  scope='Supplied ordinary-stage contract; not retail geometry or whole generator')
    (out / 'verification.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf8', newline='\n')
    print(json.dumps(dict(totals=totals, authenticated_windows=len(sources))))


if __name__ == '__main__':
    main()
