# SPDX-License-Identifier: GPL-3.0-or-later
"""Cross-check D5AQ deliverables against native and independent evidence.

Reads explicit census/startup/geometry receipts, authored CSV and source files.
Writes one fresh ignored JSON. Child processes only exercise early optimization
refusal, before native or target-sensitive imports; no game, save, database,
network, configuration or Git mutation. Stop on snapshot, schema, coverage,
geometry, native/oracle or guard mismatch. Preserve diagnostics and failed output.
"""
import os
import sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):
    raise RuntimeError('Use pinned Python -E -B without optimization')

import argparse
from collections import Counter
import csv
import json
from pathlib import Path
import subprocess
from d5ap_analyze import ROOT, guard, require, sha, write


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--census', type=Path, required=True)
    parser.add_argument('--startup', type=Path, required=True)
    parser.add_argument('--geometry', type=Path, nargs=2, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    floors = guard()
    out = args.out.resolve()
    require(out.is_relative_to(ROOT / '.local-work/d5aq') and not out.exists(), 'Fresh D5AQ output')
    require(not any(p.is_symlink() or p.is_junction() for p in (out, *out.parents)), 'No reparse output')
    census = json.loads(args.census.read_bytes())
    startup = json.loads(args.startup.read_bytes())
    methods = ROOT / 'research/resource-retained-population'
    require(census['sources']['d5aq_census.py'] == sha(methods / 'd5aq_census.py'), 'Census source differs from executed snapshot')
    require(census['sources']['d5aq_oracle.py'] == sha(methods / 'd5aq_oracle.py'), 'Independent oracle source differs')
    require(startup['method_sha256'] == sha(methods / 'd5aq_startup.py'), 'Native sampler source differs')
    expected = {(x, y) for x in range(-2, 12) for y in range(-2, 12)}
    indexed = {tuple(r['query']): r['reference'] for r in census['cells']}
    require(set(indexed) == expected and len(census['cells']) == 196, 'Complete arithmetic cohort')
    native = {(r['branch'], tuple(r['original_int2'])): r['mask'] for r in startup['rows']}
    require(len(startup['rows']) == len(native) == 392 and set(q for _, q in native) == expected, 'Complete native cohort')
    require(all(native[branch, q] == indexed[q]['mask'] for branch in ('fma', 'nonfused') for q in expected), 'Native sampler versus independent census')
    rows = list(csv.DictReader((ROOT / 'docs/experiments/resource-retained-population/d5aq-request-mask-map.csv').open(encoding='utf8')))
    require(len(rows) == 196 and {(int(r['original_x']), int(r['original_y'])) for r in rows} == expected, 'Authored CSV coverage')
    for r in rows:
        q = int(r['original_x']), int(r['original_y'])
        require(int(r['mask'], 16) == indexed[q]['mask'] and [int(r['face_x']), int(r['face_y'])] == indexed[q]['face'], 'Authored CSV differs from evidence')
    require(len({r['density_task'] for r in rows}) == len({r['layer_task'] for r in rows}) == 196, 'CSV task identity')
    require({r['density_task'] for r in rows}.isdisjoint({r['layer_task'] for r in rows}), 'Task families conflated')
    geometry = [json.loads(p.read_bytes()) for p in args.geometry]
    populations = [[r['population'] for r in g['runs']] for g in geometry]
    require(populations[0] == populations[1], 'Independent geometry process mismatch')
    historical = json.loads((ROOT / '.local-work/d5ag/geometry01/control.json').read_bytes())
    require(populations[0] == [r['population'] for r in historical['runs']], 'Historical full D5AG geometry mismatch')
    for g in geometry:
        require(g['method_sha256'] == sha(methods / 'd5aq_geometry.py'), 'Geometry adapter source changed')
        require(not g['errors'] and all(c['exact_points_bounds'] for r in g['runs'] for c in r['planar_model_comparison']), 'Complete planar comparison')
    counts = [[sum(len(p['regions']) for p in run), sum(region['count'] for p in run for region in p['regions'])] for run in populations[0]]
    require(counts == [[74, 193], [78, 180], [78, 180]], 'Complete population counts')
    extra = json.loads((ROOT / '.local-work/d5aq/extra-inputs01.json').read_bytes())
    require(extra['special_is_none'] and not extra['everywhere'], 'Extra-pass scope changed')
    optimization = []
    entries = sorted(methods.glob('d5aq_*.py'))
    for entry in entries:
        for mode in ('O', 'OO', 'environment'):
            command = [sys.executable, '-B']
            env = dict(os.environ)
            if mode == 'environment':
                env['PYTHONOPTIMIZE'] = '1'
            else:
                command += ['-E', '-' + mode]
            result = subprocess.run(command + [str(entry)], cwd=ROOT, env=env, capture_output=True,
                                    creationflags=subprocess.CREATE_NO_WINDOW)
            message = result.stdout + result.stderr
            require(result.returncode != 0 and (b'Use pinned Python' in message or b'Optimized Python is prohibited' in message), 'Early optimization refusal: ' + entry.name)
            optimization.append(dict(file=entry.name, mode=mode, exit=result.returncode))
    inputs = [args.census, args.startup, *args.geometry, ROOT / '.local-work/d5aq/extra-inputs01.json']
    write(out, dict(status='PASS', inputs={str(p): sha(p) for p in inputs},
                    native_vs_oracle_cells=392, csv_rows=196, mask_counts=dict(Counter(r['mask'] for r in rows)),
                    independent_native_populations_equal=True, historical_d5ag_equal=True,
                    complete_counts=counts, optimization=optimization,
                    source_hashes={p.name: sha(p) for p in entries},
                    floors=floors, postflight_floors=guard(), method_sha256=sha(__file__)))
    print(json.dumps(dict(status='PASS', cells=392, counts=counts, optimization_refusals=len(optimization))))


if __name__ == '__main__':
    main()
