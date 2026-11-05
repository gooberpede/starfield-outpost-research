# SPDX-License-Identifier: GPL-3.0-or-later
"""Authenticate actual A0 and existing fixed-input native reference bytes.

Reads immutable D5AK A0 raw/archive inputs through owned D5AL independent wire
oracle and source-qualified reducer; reads pinned D5AQ complete native controls.
Writes exclusive ignored receipt only, never original files. Uses SOR-P-0002
methods, stdlib and declared pinned interpreter; no new native execution or game.
"""
import os
import sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):
    raise RuntimeError('Use pinned Python -E -B without optimization')

import csv
import json
import struct
from pathlib import Path
from d5ap_analyze import ROOT, guard, require, sha, write
import d5al_baseline as baseline
import d5ai_geometry as canonical
from d5ar_qualify import independent_normalized


def main():
    out = Path(sys.argv[1]).resolve()
    floors = guard()
    require(out.is_relative_to(ROOT / '.local-work/d5ar') and not out.exists(), 'Fresh ignored D5AR receipt')
    require(not any(p.is_symlink() or p.is_junction() for p in (out, *out.parents)), 'No reparse outputs')
    observation, full, census = baseline.baseline_observation()
    require(full == independent_normalized(observation['envelope']), 'Independent A0 full byte oracle')
    raw_a0 = (baseline.SESSION / 'geometry-1.bin').read_bytes()
    # Offsets follow the authenticated 456-byte Raw2 Header, not a guessed
    # current-frame substitute. Record agreement only as a research diagnostic.
    current_descriptor = raw_a0[280:281] + raw_a0[284:324]
    construction_frame = observation['envelope']['frame']
    current_frame_diagnostic = dict(query_indexed_hex=raw_a0[176:200].hex(),
        radius_upper_hex=raw_a0[200:208].hex(), owner_formid=struct.unpack_from('<Q', raw_a0, 272)[0],
        current_descriptor_semantic=current_descriptor.hex(),
        matches_consumed_construction_descriptor=(construction_frame['basis'] == 'consumed-descriptor-v1' and
                                                 current_descriptor.hex() == construction_frame['descriptor_semantic']),
        translation_table_not_in_header=True, qualification='DIAGNOSTIC_ONLY')
    source_rows = list(csv.DictReader((ROOT / 'docs/experiments/resource-retained-population/d5aq-sources.csv').open(encoding='utf8')))
    paths = [ROOT / '.local-work/d5aq' / name / 'control.json' for name in ('geometry01', 'geometry02')]
    fixed = []
    for path in paths:
        expected = next(r['sha256'] for r in source_rows if Path(r['path']).as_posix() == path.relative_to(ROOT).as_posix())
        require(sha(path) == expected, 'Historical fixed-native reference changed')
        value = json.loads(path.read_bytes())
        require(not value['errors'] and all(p['exact_points_bounds'] for run in value['runs'] for p in run['planar_model_comparison']), 'Native versus independent model failure')
        fixed.append(value['runs'])
    require([r['population'] for r in fixed[0]] == [r['population'] for r in fixed[1]], 'Distinct native host output changed')
    counts = [[sum(len(r['regions']) for r in run['population']), sum(g['count'] for r in run['population'] for g in r['regions'])] for run in fixed[0]]
    require(counts == [[74, 193], [78, 180], [78, 180]], 'Fixed complete output totals changed')
    # This is an exact content-only cross-check, deliberately excluding an
    # invented equality between runtime consumed-descriptor and fixture frames.
    def body(population):
        result = []
        for resource in sorted(population, key=lambda r: int(r['resource'], 16)):
            result.append((resource['resource'], [(g['header'][:42], g['count'], g['points']) for g in resource['regions']]))
        return result
    actual_body = body(observation['envelope']['population'])
    equal = [actual_body == body(run['population']) for run in fixed[0]]
    write(out, dict(status='PASS', a0_normalized_sha256=baseline.NORMALIZED, a0_normalized_bytes=len(full),
                    authenticated_holders=len(census), fixed_counts=counts, content_only_equal_to_a0=equal,
                    a0_current_consumer_diagnostics=current_frame_diagnostic,
                    qualified_cross_frame_comparison=False, historical_sampled_mask_inferred=False,
                    reason='Fixed source-planar and actual consumed-descriptor frames are distinct; content equality alone supplies no effective-input equivalence',
                    inputs={str(p): sha(p) for p in paths}, anchor_inputs={str(p): value for p, value in baseline.ANCHORS.items()},
                    method_sha256=sha(__file__), floors=floors, postflight_floors=guard()))
    print(json.dumps(dict(status='PASS', bytes=len(full), holders=len(census), content_only_equal=equal, cross_frame_qualified=False)))


if __name__ == '__main__':
    main()
