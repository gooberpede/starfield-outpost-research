# SPDX-License-Identifier: GPL-3.0-or-later
"""One definition-backed C1G replay, never a seed/weight search. Reads C1F/C1E
closed receipts, frozen requests, pinned main-GMST provenance and owned evaluator.
Writes one fresh ignored JSON. No target/save/config/Git/database/network writes.
This adds a separately named diagnostic; never rewrites original predictions.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import struct
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT/'research/resource-generation-ancestry'),
               str(ROOT/'research/resource-region-ancestry'),
               str(ROOT/'research/resource-geometry')]
from investigate import signature, compare
from qualify import independent
import geometry


def pin(path):
    with Path(path).open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--provenance', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    a = ap.parse_args()
    assert a.output.resolve().is_relative_to(ROOT/'.local-work/resource-selection-operands')
    assert not a.output.exists()
    provenance = json.loads(a.provenance.read_text())
    gmst = next(r for r in provenance['selected_main_records'] if r['editor_id'] == 'fInactiveResourceChanceMultExotic')
    assert gmst['formid'] == 0x226b0d
    raw = bytes.fromhex(dict(gmst['fields'])['DATA'])
    assert raw == bytes.fromhex('cdcc4c3d')
    weight = struct.unpack('<f', raw)[0]
    freeze = json.loads((ROOT/'docs/experiments/resource-geometry-mature-context/freeze-mature-v2.json').read_text())
    record = next(p for p in freeze['complete_geometry'] if 'feynman' in p['path'])
    assert pin(record['path']) == record['sha256']
    frozen = json.loads(Path(record['path']).read_text())
    receipts = ROOT/'.local-work/resource-region-ancestry/retail-attempt01'
    samples = [independent(p)[1] for p in sorted(receipts.glob('capture-*.bin'))]
    assert len(samples) == 967
    observed = []
    for r in samples:
        if r.get('decision') == 'ACCEPT':
            h = bytes.fromhex(r['geometry']['raw_region'])
            pts = bytes.fromhex(r['geometry']['ordered_xyzw'])
            fid = struct.unpack_from('<I', bytes.fromhex(r['selected']['raw_resource']), 40)[0]
            observed.append(dict(resource=f'{fid:08x}', signature=pts+h[:16]))
    assert {r['resource'] for r in observed} == {'000057d4', '000057cf', '000057ce', '000057cb'}
    cs = json.loads((ROOT/'.local-work/resource-milestone-b-spatial-constants.json').read_text())['constants']
    constants = {int(c['va'], 16):c['float'] for c in cs}
    constants.update({int(c['va'], 16):c['value'] for c in frozen['constants']})
    base, generated, changes = [], [], []
    for source in frozen['sources']:
        req = copy.deepcopy(source['request'])
        baseline = geometry.populate_source(req, constants)['regions']
        assert [signature(r) for r in baseline] == [signature(r) for r in source['regions']]
        base.extend(baseline)
        for resource in req['ordered_resources']:
            # This six-source corpus's only exotic entry is IL (C1F ledger).
            if resource['resource'] == '000057d4':
                changes.append(dict(source=req['source'], resource=resource['resource'],
                                    old=resource['weight'], new=weight, gmst=gmst['formid']))
                resource['weight'] = weight
        generated.extend(geometry.populate_source(req, constants)['regions'])
    assert len(base) == 156
    match = compare(observed, generated)
    # Report actual comparison; a scientific miss must be retained, not tuned.
    extra = [r for r in generated if r['resource'] == '000057d4' and r['source'] == '0:25116:32448:00257f38' and r['cell'] == [11, 1]]
    out = dict(provenance_sha256=pin(a.provenance), frozen_sha256=record['sha256'],
               c1e_event_sha256=pin(receipts/'events.jsonl'), raw_receipts_verified=len(samples),
               variant='installed-main-GMST-exotic-only', weight_bits=raw.hex(), weight=weight,
               changes=changes, baseline_count=len(base), generated_count=len(generated),
               baseline_matches=compare(observed, base), native_matches=match,
               all_four_exact=all(match.values()), extra_il_11_1=len(extra),
               conclusion='CONDITIONAL diagnostic only; effective/historical loaded value UNKNOWN')
    with a.output.open('x', encoding='utf8', newline='\n') as f:
        json.dump(out, f, indent=2)
        f.write('\n')
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    main()
