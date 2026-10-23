# SPDX-License-Identifier: GPL-3.0-or-later
"""Read closed receipts and frozen requests; write exclusive offline derivatives.

Requires Python stdlib and owned geometry/context modules. No target, save,
configuration, database, Git or network effects. The sole counterfactual is the
pre-existing SITE_AS_GENERATOR frame, never a searched offset or seed.
"""
import argparse
import collections
import copy
import hashlib
import json
from pathlib import Path
import struct
import sys

ROOT = Path(__file__).resolve().parents[2]
LOCAL = ROOT / '.local-work/resource-carinae-source-context'
sys.path[:0] = [str(ROOT / 'research/resource-geometry'),
               str(ROOT / 'save-analysis/scripts')]
import geometry
import context
from qualify import independent


def pin(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def signature(row, xyw=False):
    if xyw:
        return b''.join(struct.pack('<3f', p[0], p[1], p[3]) for p in row['points'])
    return struct.pack('<4f', *row['native_bound']) + b''.join(
        struct.pack('<4f', *p) for p in row['points'])


def comparisons(rows, population):
    results = []
    for row in rows:
        raw = bytes.fromhex(row['geometry']['raw_region'])
        points = list(struct.iter_unpack('<4f', bytes.fromhex(row['geometry']['ordered_xyzw'])))
        fid = int.from_bytes(bytes.fromhex(row['selected']['raw_resource'])[40:44], 'little')
        region = dict(points=points, native_bound=struct.unpack_from('<4f', raw))
        resource = [g for g in population if int(g['resource'], 16) == fid]
        results.append(dict(capture=row['capture'], resource=f'0x{fid:08x}',
            paths=len(resource), full_exact=sum(signature(g) == signature(region) for g in resource),
            xyw_exact=sum(signature(g, True) == signature(region, True) for g in resource),
            geometry_sha256=hashlib.sha256(signature(region)).hexdigest(),
            native_bound=region['native_bound'], ordered_xyzw=points,
            source_ordinal=row['source_ordinal'], source_slot_va=hex(row['source_slot']),
            source_key_va=hex(row['source_key']), wrapper_va=hex(row['selected']['source_wrapper']),
            generation_epoch='UNKNOWN'))
    return results


def translated_consumer(rows, delta):
    """Candidate frame projection: one rounded binary32 add per XY component.

    Width and Z words stay unchanged. This derivative is not native geometry
    evidence and does not assert a historical transformation or rounding route.
    """
    projected = copy.deepcopy(rows)
    for row in projected:
        bound = bytearray.fromhex(row['geometry']['raw_region'])
        points = bytearray.fromhex(row['geometry']['ordered_xyzw'])
        for data, starts in ((bound, [0]), (points, range(0, len(points), 16))):
            for start in starts:
                for axis in (0, 1):
                    at = start + axis * 4
                    value = struct.unpack_from('<f', data, at)[0]
                    struct.pack_into('<f', data, at, value + delta[axis])
        row['geometry']['raw_region'] = bound.hex()
        row['geometry']['ordered_xyzw'] = points.hex()
    return projected


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--geometry', type=Path, required=True)
    args = ap.parse_args()
    assert all(p.resolve().is_relative_to(LOCAL) and not p.exists() for p in (args.output, args.geometry))
    receipts = ROOT / '.local-work/resource-carinae/retail-attempt02'
    full_path = ROOT / '.local-work/resource-installed-settings/c2b-geometry01.json'
    frozen_path = ROOT / '.local-work/resource-geometry-mature-context/site-carinae-initial02.json'
    frames_path = ROOT / '.local-work/resource-geometry-mature-context/frame-discriminator02.json'
    constants_path = ROOT / '.local-work/resource-milestone-b-spatial-constants.json'
    paths = [full_path, frozen_path, frames_path, constants_path, Path(__file__),
             ROOT / 'research/resource-geometry/geometry.py', ROOT / 'research/resource-geometry/context.py',
             receipts / 'events.jsonl', *receipts.glob('capture-*.bin'), *receipts.glob('capture-*.ack.json')]
    before = {str(p): pin(p) for p in paths}
    rows = [independent(p)[1] for p in sorted(receipts.glob('capture-*.bin'))]
    events = [json.loads(line) for line in (receipts / 'events.jsonl').read_text().splitlines()]
    assert rows == [e for e in events if e['kind'] == 'SAMPLE'] and len(rows) == 2587
    acks = [e for e in events if e['kind'] == 'ACK_ACCEPTED']
    assert len(acks) == len(rows) and all(e['accepted'] for e in acks)
    assert not [e for e in events if e['kind'] in ('LOSS', 'EXCEPTION')]
    transfer = rows[-1]
    assert transfer['ancestry'] == 'BOUND_TRANSFER'
    accepted = [e for e in rows if e.get('decision') == 'ACCEPT']
    assert {e['capture'] for e in accepted} == {1270, 1280, 1301}
    for row in accepted:
        assert row['ancestry'] == 'BOUND_CALLBACK' and row['required_reads_complete']
        assert all(row[k] == transfer[k] for k in ('pid', 'tid', 'thread_lifetime', 'updater_token',
                                                  'updater_bp', 'temporary_set', 'binding_reference', 'raw_binding_extra'))
        assert bytes.fromhex(row['raw_binding_extra'])[0x98:0xa0].hex() == '91bac704da9b1e34'
        assert row['file_provenance']['main_file_identity']
        assert any(m['pointer'] == row['resource_pointer'] for m in transfer['refresh_payload']['members'])
    full = json.loads(full_path.read_text())
    baseline = [g for s in full if s['site'] == 'Carinae' for g in s['regions']]
    assert collections.Counter(g['resource'] for g in baseline) == {'000057c7': 259, '000057c9': 505, '00005df1': 131}
    frozen = json.loads(frozen_path.read_text())
    constants = {int(c['va'], 16): c['float'] for c in json.loads(constants_path.read_text())['constants']}
    constants.update({int(c['va'], 16): c['value'] for c in frozen['constants']})
    frames = next(r for r in json.loads(frames_path.read_text())['rows'] if r['name'] == 'Carinae III-a Rc Fe')
    variant = next(v for v in frames['variants'] if v['hypothesis'] == 'SITE_AS_GENERATOR')
    alternate = []
    for s in (s for s in full if s['site'] == 'Carinae'):
        req = copy.deepcopy(s['request'])
        source = next(x['source'] for x in variant['sources'] if x['source']['id'] == req['source'])
        req.update(origin=source['origin'], clip_center=source['clip_center'], clip_half=source['clip_half'])
        for xy in req['packed_keys']:
            cell = list(map(int, xy.split(',')))
            req['packed_keys'][xy] = context.packed_seed_key(0, variant['origin'], req['origin'], cell, frames['system'], frames['index'])
        req['provenance'] = 'C2B pre-existing SITE_AS_GENERATOR candidate; actual native selection UNKNOWN'
        result = geometry.populate_source(req, constants)
        assert result['status'] == 'CONDITIONAL_PLANAR_SOURCE', result
        alternate.append(dict(site='Carinae', request=req, regions=result['regions']))
    alternative = [g for s in alternate for g in s['regions']]
    descriptor = next(v for v in frames['variants'] if v['hypothesis'] == 'DESCRIPTOR_AS_GENERATOR')
    delta = [variant['center'][i] - descriptor['center'][i] for i in (0, 1)]
    assert delta == [900, 800]
    summary = dict(schema='sor-c2b-context/1', captures=len(rows), ack_count=len(acks),
        decisions=dict(collections.Counter(e['decision'] for e in rows if 'decision' in e)),
        baseline=comparisons(accepted, baseline),
        alternate=dict(status='CANDIDATE_FRAME_NOT_OBSERVED', origin=variant['origin'],
            query_xy=variant['center'], paths=len(alternative),
            raw_numeric_comparisons_without_frame_alignment=comparisons(accepted, alternative),
            conditional_consumer_frame_projection=dict(delta_xy=delta,
                arithmetic='one binary32-rounded addition per bound/point XY component; width and Z unchanged',
                status='CONDITIONAL_SPATIAL_COMPARISON_NOT_NATIVE_GEOMETRY_EQUALITY',
                comparisons=comparisons(translated_consumer(accepted, delta), alternative))),
        common_correction='NONE_ESTABLISHED', first_missing_operand='SOURCE_KEY_REFERENT_AND_MANAGER_FRAME_AT_CONSUMPTION',
        historical_generation_inputs='UNKNOWN', publication='REVIEW-REQUIRED',
        inputs=before)
    assert before == {str(p): pin(p) for p in paths}
    for path, value in ((args.geometry, alternate), (args.output, summary)):
        with path.open('x', encoding='utf8', newline='\n') as stream:
            json.dump(value, stream, indent=2)
            stream.write('\n')
    print(json.dumps({k: v for k, v in summary.items() if k != 'inputs'}, indent=2))


if __name__ == '__main__':
    main()
