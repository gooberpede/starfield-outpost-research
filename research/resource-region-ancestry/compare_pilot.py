# SPDX-License-Identifier: GPL-3.0-or-later
"""Offline C1E accepted-region versus immutable Feynman v2 geometry comparison.

Reads closed native receipts, frozen complete geometry and unchanged owned area
evaluator. Writes only a fresh ignored derivative. No target/process, save,
definition/config, prediction, Git or analysis database mutation; stdlib only.
Numeric coordinate equality is not a producer/input/source identity assertion.
"""
import argparse
import json
from pathlib import Path
import struct
import sys
from qualify import independent, pin, write, LOCAL, ROOT
sys.path.insert(0,str(ROOT/'save-analysis/scripts'))
from resource_spatial import evaluate_region


def words(values):
    return struct.pack('<'+'f'*len(values),*values)


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--receipts',type=Path,required=True)
    ap.add_argument('--analysis',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    a=ap.parse_args()
    assert a.receipts.resolve().is_relative_to(LOCAL) and a.output.resolve().is_relative_to(LOCAL)
    freeze_path=ROOT/'docs/experiments/resource-geometry-mature-context/freeze-mature-v2.json'
    freeze=json.loads(freeze_path.read_text())
    frozen_pin=next(r for r in freeze['complete_geometry'] if 'feynman' in r['path'])
    assert pin(frozen_pin['path'])==frozen_pin['sha256']
    frozen=json.loads(Path(frozen_pin['path']).read_text())
    population=[r for s in frozen['sources'] for r in s['regions']]
    events=[json.loads(l) for l in (a.receipts/'events.jsonl').read_text().splitlines()]
    samples=[r for r in events if r['kind']=='SAMPLE']
    assert len(samples)==len(list(a.receipts.glob('capture-*.bin')))
    for r in samples:
        assert independent(a.receipts/f'capture-{r["capture"]:05d}.bin')[1]==r
    joins=json.loads(a.analysis.read_text())
    assert joins['event_sha256']==pin(a.receipts/'events.jsonl')
    verified={j['capture'] for j in joins['joins'] if j['accepted_region_to_transfer']}
    accepted=[]
    for r in samples:
        if r['capture'] not in verified:
            continue
        h=bytes.fromhex(r['geometry']['raw_region']);pts=bytes.fromhex(r['geometry']['ordered_xyzw'])
        n=struct.unpack_from('<I',h,24)[0]
        assert len(pts)==n*16
        formid=struct.unpack_from('<I',bytes.fromhex(r['selected']['raw_resource']),40)[0]
        candidates=[g for g in population if int(g['resource'],16)==formid]
        path_matches=[g for g in candidates if b''.join(words(p) for p in g['points'])==pts]
        matches=[g for g in path_matches if words(g['native_bound'])==h[:16]]
        q=struct.unpack('<3f',bytes.fromhex(r['qb_retained_bits']))
        radius,upper=struct.unpack_from('<2f',bytes.fromhex(r['raw_closure']),16)
        diagnostic=evaluate_region(q,radius,upper,struct.unpack_from('<3f',h),struct.unpack_from('<f',h,12)[0],list(struct.iter_unpack('<4f',pts)))
        accepted.append(dict(capture=r['capture'],formid=f'{formid:08x}',point_count=n,
            source_ordinal=r['source_ordinal'],region_ordinal=r['selected']['ordinal'],
            capture_sha256=pin(a.receipts/f'capture-{r["capture"]:05d}.bin'),
            frozen_resource_paths=len(candidates),ordered_point_matches=len(path_matches),complete_geometry_matches=len(matches),
            matches=[dict(source=g['source'],cell=g['cell']) for g in matches],
            qb_bits=r['qb_retained_bits'],qb_xy_equals_frozen_center=words(q[:2])==words(frozen['center']),
            native_radius=radius,native_absolute_upper=upper,
            conditional_area_replay=diagnostic,
            replay_admission='CONDITIONAL_RETAINED_QUERY_STABILITY; PER_USE_QC_QV_QE_UNOBSERVED',
            selected_generation_source='UNKNOWN',generation_inputs='UNKNOWN',cache_epoch='UNKNOWN'))
    value=dict(experiment='RG2-C1E_PHASE_B',freeze_sha256=pin(freeze_path),frozen_geometry_pin=frozen_pin,
        raw_event_sha256=pin(a.receipts/'events.jsonl'),analysis_sha256=pin(a.analysis),accepted=accepted,
        counts=dict(samples=len(samples),decisions=sum('decision' in r for r in samples),
            accepts=sum(r.get('decision')=='ACCEPT' for r in samples),rejects=sum(r.get('decision')=='REJECT' for r in samples)),
        snapshot_completeness='VISITED_TERMINALS_ONLY_NOT_REGION_CENSUS',
        coordinate_rule='No fitting/transform applied; raw binary32 numeric comparison in declared frozen model coordinates; producer/frame identity not inferred')
    write(a.output,value)
    print(json.dumps(value,indent=2))


if __name__=='__main__':
    main()
