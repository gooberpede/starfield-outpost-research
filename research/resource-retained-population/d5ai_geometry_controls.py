# SPDX-License-Identifier: GPL-3.0-or-later
"""Qualify complete comparison with independent planar and damaged-input oracles.

Reads two explicitly named fresh native receipts and the pinned D5S planar model.
Writes exclusive local fixtures, normalized bytes and a receipt. Stdlib only;
no native execution, game/save/database/network/Git operations. Requires -E -B.
Stop on oracle/identity/schema/disk failure. Inputs and failed outputs remain intact.
SOR-P-0002: native population layout and model lineage from D5AF/D5AH methods.
"""
import argparse
import copy
import csv
import hashlib
import io
import json
from pathlib import Path
import struct

from d5ae_baseline import guard, sha
from d5ai_geometry import SCHEMA, compare, load, normalize

ROOT = Path(__file__).resolve().parents[2]


def words(values):
    return [struct.pack('<f', v).hex() for v in values]


def envelope(run):
    population = copy.deepcopy(run['population'])
    return dict(schema=SCHEMA, snapshot_id=run['label'], session_id='fixture-process-one',
                source=dict(key='0:37536:20928:0029d20e', body_formid='0005e0de'),
                frame=dict(anchor_i32=[37536, 20928], origin_i32=[-200, -200],
                           clip_center_f32=words([300, 300, 0, 0]),
                           clip_half_f32=words([700, 700, 0, 0]), basis='source-planar'),
                capture=dict(complete=True, status='OK', resource_slots=len(population),
                             region_total=sum(len(r['regions']) for r in population),
                             point_total=sum(v['count'] for r in population for v in r['regions'])),
                availability=dict(boundary_qualified=True, map_scan_complete=True,
                                  holder_present=True, exposed=True),
                generation_quality='UNKNOWN', loss=0, population=population)


def inverse_oracle(data, snapshot):
    """Independently decode normalized framing and compare every original byte."""
    stream = io.BytesIO(data)

    def word():
        raw = stream.read(4)
        if len(raw) != 4:
            raise ValueError('Normalized stream truncated')
        return int.from_bytes(raw, 'little')

    if json.loads(stream.read(word())) != snapshot['source']:
        return False
    if json.loads(stream.read(word())) != snapshot['frame']:
        return False
    if word() != len(snapshot['population']):
        return False
    for resource in sorted(snapshot['population'], key=lambda r: int(r['resource'], 16)):
        if stream.read(4).hex() != resource['resource'] or word() != len(resource['regions']):
            return False
        for region in resource['regions']:
            if stream.read(21).hex() != region['header'][:42] or word() != region['count']:
                return False
            if stream.read(region['count'] * 16).hex() != region['points']:
                return False
    return stream.read() == b''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('out', type=Path)
    parser.add_argument('native', type=Path, nargs=2)
    args = parser.parse_args()
    guard()
    if not args.out.resolve().is_relative_to(ROOT / '.local-work/d5ai'):
        raise ValueError('Task-local output required')
    args.out.mkdir(exist_ok=False)
    model_path = ROOT / '.local-work/d5s/geometry.json'
    rows = list(csv.DictReader((ROOT / 'docs/experiments/resource-retained-population/d5s-sources.csv').open(encoding='utf8')))
    expected = next(r['sha256'] for r in rows if Path(r['path']).resolve() == model_path.resolve())
    if sha(model_path) != expected:
        raise ValueError('Independent model identity differs')
    model = load(model_path)
    receipts = [load(p) for p in args.native]
    if any(r['model_input_sha256'] != expected for r in receipts):
        raise ValueError('Native/model provenance differs')
    tests = []

    def check(name, condition):
        tests.append(dict(name=name, passed=bool(condition)))
        if not condition:
            raise AssertionError(name)

    snapshots = [envelope(r) for r in receipts[0]['runs']]
    second = [envelope(r) for r in receipts[1]['runs']]
    for i, snapshot in enumerate(snapshots):
        check(f'fresh-process-full-content-{i}', normalize(snapshot) == normalize(second[i]))
        check(f'independent-normalized-inverse-{i}', inverse_oracle(normalize(snapshot), snapshot))
        oracle = model['results'][0 if i == 0 else 1]['full']['regions']
        actual_keys = [r['resource'] for r in snapshot['population']]
        check(f'complete-resource-key-census-{i}',
              len(actual_keys) == len(set(actual_keys)) and set(actual_keys) == {r['resource'] for r in oracle})
        # Independent arithmetic supplies every original point and bound. Native
        # flags remain opaque exact bytes, tested separately for preservation.
        for resource in snapshot['population']:
            expected_regions = [r for r in oracle if r['resource'] == resource['resource']]
            check(f'complete-region-census-{i}-{resource["resource"]}', len(expected_regions) == len(resource['regions']))
            for ordinal, (actual, reference) in enumerate(zip(resource['regions'], expected_regions)):
                check(f'point-bound-oracle-{i}-{resource["resource"]}-{ordinal}',
                      bytes.fromhex(actual['header'])[:16] == struct.pack('<4f', *reference['native_bound'])
                      and actual['count'] == len(reference['points'])
                      and bytes.fromhex(actual['points']) == b''.join(struct.pack('<4f', *p) for p in reference['points']))
        (args.out / f'population-{i}.json').write_text(json.dumps(snapshot, indent=2) + '\n', encoding='utf8', newline='\n')
        (args.out / f'population-{i}.normalized').write_bytes(normalize(snapshot))
    a, b, c = snapshots
    retained = dict(qualified=True, relation='CONTINUOUS', loss=0,
                    before=[b['session_id'], b['snapshot_id']], after=[c['session_id'], c['snapshot_id']])
    rebuilt = dict(retained, relation='RECONSTRUCTED')
    check('retained-positive', compare(b, c, retained)['outcome'] == 'RETAINED')
    check('rebuilt-identical-positive', compare(b, c, rebuilt)['outcome'] == 'REBUILT_IDENTICAL')
    different = dict(rebuilt, before=[a['session_id'], a['snapshot_id']], after=[b['session_id'], b['snapshot_id']])
    check('rebuilt-different-mask0-mask3', compare(a, b, different)['outcome'] == 'REBUILT_DIFFERENT')
    check('false-continuity-refused', compare(a, b, dict(different, relation='CONTINUOUS'))['outcome'] == 'INCONCLUSIVE')
    for malformed_frame in ([], None, 1, 'not-a-frame'):
        damaged = copy.deepcopy(c)
        damaged['frame'] = malformed_frame
        check('malformed-frame-' + repr(malformed_frame), compare(b, damaged, rebuilt)['outcome'] == 'INCONCLUSIVE')
    for relation in ('POINTER_EQUAL', 'UNKNOWN'):
        check('ambiguous-lifetime-' + relation, compare(b, c, dict(qualified=True, relation=relation, loss=0))['outcome'] == 'INCONCLUSIVE')
    check('wrong-certificate-binding', compare(b, c, dict(retained, before=['other', 'other']))['outcome'] == 'INCONCLUSIVE')
    fresh = copy.deepcopy(c)
    fresh['session_id'] = 'fixture-process-two'
    joined = dict(retained, after=[fresh['session_id'], fresh['snapshot_id']])
    check('cross-process-retention-refused', compare(b, fresh, joined)['outcome'] == 'INCONCLUSIVE')
    check('cross-process-equal-rebuild', compare(b, fresh, dict(joined, relation='RECONSTRUCTED'))['outcome'] == 'REBUILT_IDENTICAL')
    native_frame = dict(basis='consumed-descriptor-v1', owner_formid='0005e0de',
                        descriptor_semantic=(b'\0' + bytes(40)).hex())
    na, nb = copy.deepcopy(b), copy.deepcopy(c)
    na['frame'] = copy.deepcopy(native_frame)
    nb['frame'] = copy.deepcopy(native_frame)
    check('descriptor-frame-positive', compare(na, nb, rebuilt)['outcome'] == 'REBUILT_IDENTICAL')
    nb['frame']['descriptor_semantic'] = (b'\0' + bytes(39) + b'\1').hex()
    check('descriptor-frame-word-change-refused', compare(na, nb, rebuilt)['outcome'] == 'INCONCLUSIVE')
    nb['frame']['descriptor_semantic'] = (b'\1' + bytes(40)).hex()
    check('unqualified-chart-refused', compare(na, nb, rebuilt)['outcome'] == 'INCONCLUSIVE')
    for field in ('boundary_qualified', 'map_scan_complete'):
        changed = copy.deepcopy(c)
        changed['availability'][field] = False
        check('availability-refusal-' + field, compare(b, changed, rebuilt)['outcome'] == 'INCONCLUSIVE')
    changed = copy.deepcopy(c)
    changed['availability']['exposed'] = False
    check('existing-but-unexposed', compare(b, changed, rebuilt)['outcome'] == 'UNAVAILABLE')
    changed['availability']['holder_present'] = False
    changed['population'] = []
    changed['capture'].update(resource_slots=0, region_total=0, point_total=0)
    check('map-absent-qualified', compare(b, changed, rebuilt)['outcome'] == 'UNAVAILABLE')
    changed['availability']['map_scan_complete'] = False
    check('missing-observation-is-not-absence', compare(b, changed, rebuilt)['outcome'] == 'INCONCLUSIVE')
    mutations = {}
    for name in ('truncated-region', 'missing-point', 'formid-substitution', 'region-order',
                 'resource-order', 'wrong-frame', 'partial', 'allocation-failure', 'loss',
                 'nan', 'flag', 'padding', 'signed-zero', 'unknown-point-word', 'point-order'):
        x = copy.deepcopy(c)
        region = x['population'][0]['regions'][0]
        if name == 'truncated-region': x['population'][0]['regions'].pop()
        elif name == 'missing-point': region['points'] = region['points'][:-32]
        elif name == 'formid-substitution': x['population'][0]['resource'] = '00000001'
        elif name == 'region-order': x['population'][0]['regions'].reverse()
        elif name == 'resource-order': x['population'].reverse()
        elif name == 'wrong-frame': x['frame']['origin_i32'][0] += 1
        elif name == 'partial': x['capture']['complete'] = False
        elif name == 'allocation-failure': x['capture']['status'] = 'ALLOCATION_FAILED'
        elif name == 'loss': x['loss'] = 1
        elif name == 'nan': region['points'] = '0000c07f' + region['points'][8:]
        elif name == 'flag': region['header'] = region['header'][:40] + 'ff' + region['header'][42:]
        elif name == 'padding': region['header'] = region['header'][:42] + 'aabbcc'
        elif name == 'signed-zero': region['points'] = region['points'][:16] + '00000080' + region['points'][24:]
        elif name == 'unknown-point-word': region['points'] = region['points'][:24] + '00000000' + region['points'][32:]
        elif name == 'point-order':
            region = next(v for r in x['population'] for v in r['regions'] if v['count'] > 1)
            chunks = [region['points'][i:i + 32] for i in range(0, len(region['points']), 32)]
            region['points'] = ''.join(reversed(chunks))
        verdict = compare(b, x, rebuilt)['outcome']
        expected_verdict = ('REBUILT_IDENTICAL' if name in ('padding', 'resource-order') else
                            'REBUILT_DIFFERENT' if name in ('region-order', 'flag', 'signed-zero', 'unknown-point-word', 'point-order') else 'INCONCLUSIVE')
        check('adversary-' + name, verdict == expected_verdict)
        mutations[name] = verdict
    empty = copy.deepcopy(c)
    empty['population'][0]['regions'][0].update(count=0, points='')
    empty['capture']['point_total'] -= c['population'][0]['regions'][0]['count']
    check('zero-length-region-preserved', normalize(empty) != normalize(c))
    malformed = args.out / 'duplicate.json'
    malformed.write_bytes(b'{"schema":"sor-d5ai-geometry/1","schema":"forged"}')
    try:
        load(malformed)
    except ValueError:
        check('duplicate-json-key-refused', True)
    else:
        check('duplicate-json-key-refused', False)
    paths = [*args.native, model_path, Path(__file__), Path(__file__).with_name('d5ai_geometry.py')]
    result = dict(tests=tests, passed=len(tests), mutations=mutations,
                  inputs={str(p): sha(p) for p in paths},
                  scope='Offline complete represented geometry and modeled evidence certificates; no retail boundary qualification')
    (args.out / 'receipt.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf8', newline='\n')
    for method in (Path(__file__), Path(__file__).with_name('d5ai_geometry.py')):
        (args.out / method.name).write_bytes(method.read_bytes())
    print(json.dumps(dict(passed=len(tests), mutations=mutations)))


if __name__ == '__main__':
    main()
