# SPDX-License-Identifier: GPL-3.0-or-later
"""Independently check complete native representations and copy adversaries.

Reads D5AH fresh receipts, D5AG controls and the separate D5S planar model;
writes exclusive ignored verification JSON and the authored identity manifest.
No native execution, game, save, database, network or Git mutation. Stdlib only.
Preserves resource/region/point order and duplicates; rejects partial byte arrays.
Stop on identity, schema, oracle, output uniqueness or caller-space failure.
"""
from pathlib import Path
import copy
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


def canonical(run):
    output = []
    keys = set()
    for resource in run['population']:
        key = resource['resource']
        if key in keys:
            raise ValueError('Duplicate represented resource key')
        keys.add(key)
        regions = []
        for region in resource['regions']:
            header = bytes.fromhex(region['header'])
            points = bytes.fromhex(region['points'])
            n = region['count']
            if len(header) != 24 or n < 0 or len(points) != n * 16:
                raise ValueError('Incomplete representation')
            scalars = struct.unpack('<' + 'f' * (len(points) // 4), points)
            if not all(math.isfinite(v) for v in scalars + struct.unpack('<4f', header[:16])):
                raise ValueError('Nonfinite geometry')
            if struct.unpack_from('<I', header, 16)[0] != int(key, 16):
                raise ValueError('Region identity disagrees with collection')
            regions.append((header, n, points))
        output.append((key, regions))
    return output


def main():
    if not __debug__ or sys.flags.optimize:
        raise RuntimeError('Use Python -E -B')
    free = guard()
    out = ROOT / '.local-work/d5ah' / sys.argv[1]
    if not out.resolve().is_relative_to(ROOT / '.local-work/d5ah'):
        raise ValueError('Task-local receipt required')
    out.mkdir(exist_ok=False)
    files = [ROOT / '.local-work' / task / label / 'control.json'
             for task, label in [('d5ah', 'geometry01'), ('d5ah', 'geometry02'),
                                 ('d5ag', 'geometry01'), ('d5ag', 'geometry02')]]
    receipts = [json.loads(path.read_bytes()) for path in files]
    full = [[canonical(run) for run in receipt['runs']] for receipt in receipts]
    assert all(populations == full[0] for populations in full)
    assert full[0][0] != full[0][1] and full[0][1] == full[0][2]
    model_path = ROOT / '.local-work/d5s/geometry.json'
    model = json.loads(model_path.read_bytes())
    assert all(receipt['model_input_sha256'] == sha(model_path) for receipt in receipts)
    totals = []
    for run, index in zip(receipts[0]['runs'], [0, 1, 1]):
        for item in run['population']:
            expected = [r for r in model['results'][index]['full']['regions']
                        if r['resource'] == item['resource']]
            actual = item['regions']
            assert len(actual) == len(expected)
            for a, e in zip(actual, expected):
                assert a['count'] == len(e['points'])
                assert bytes.fromhex(a['points']) == b''.join(struct.pack('<4f', *p) for p in e['points'])
                assert bytes.fromhex(a['header'])[:16] == struct.pack('<4f', *e['native_bound'])
        totals.append(dict(query=run['original_query'], mask=run['low_mask'],
                           resources=len(run['population']),
                           regions=sum(len(r['regions']) for r in run['population']),
                           points=sum(r['count'] for v in run['population'] for r in v['regions'])))
    checks = {}
    changed = copy.deepcopy(receipts[0]['runs'][1])
    r = changed['population'][0]['regions'][0]
    r['points'] = (struct.pack('<f', 98765) + bytes.fromhex(r['points'])[4:]).hex()
    checks['single_coordinate_change_detected'] = canonical(changed) != full[0][1]
    malformed = copy.deepcopy(changed)
    malformed['population'][0]['regions'][0]['points'] = r['points'][:-2]
    try:
        canonical(malformed)
    except ValueError:
        checks['partial_copy_rejected'] = True
    assert checks.get('partial_copy_rejected')
    copy_path = ROOT / '.local-work/d5ah/copy02/copy.json'
    copied = json.loads(copy_path.read_bytes())
    assert [r['copied_points'] for r in copied['cases']] == [2, 0, 0, 1]
    assert [r['native_outer_success'] for r in copied['cases']] == [True, False, True, True]
    assert copied['source_mutation_does_not_change_copy']
    assert all(checks.values())
    selected = files + [model_path, copy_path, ROOT / '.local-work/d5ah/inputs02.json',
                        ROOT / '.local-work/d5ah/snapshot01.json',
                        ROOT / 'research/resource-retained-population/d5ah_controls.py',
                        ROOT / 'research/resource-retained-population/d5af_geometry.py',
                        ROOT / 'research/resource-retained-population/d5ah_copy.py',
                        Path(sys.executable)]
    sources = [dict(id=f'D5AH-M{i:03}', path=str(p), sha256=sha(p),
                    bytes=p.stat().st_size, locator='Complete file; exact method and input identities retained',
                    lineage='SOR-P-0002 owned methods / installed tool; no outside incorporation',
                    eligibility='LOCAL-ONLY' if '.local-work' in str(p) or p == Path(sys.executable)
                    else 'REVIEW-REQUIRED') for i, p in enumerate(selected, 1)]
    tool_rows = list(csv.DictReader((DOC / 'd5s-sources.csv').open(encoding='utf8')))
    for identifier in [f'D5S-T{i:02}' for i in range(1, 7)]:
        row = next(r for r in tool_rows if r['id'] == identifier)
        path = Path(row['path'])
        assert sha(path) == row['sha256'], identifier
        sources.append(dict(id='D5AH-' + identifier, path=str(path), sha256=sha(path),
                            bytes=path.stat().st_size,
                            locator='Selected installed launcher/JAR/CRT identity; not entire dependency closure',
                            lineage='d5s-sources.csv row ' + identifier,
                            eligibility='LOCAL-ONLY'))
    with (DOC / 'd5ah-sources.csv').open('w', encoding='utf8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(sources[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(sources)
    result = dict(sources=sources, totals=totals, adversaries=checks, free=free,
                  complete_cross_process_equality=True, equal_mask3_queries=True,
                  complete_mask0_difference=True, independent_planar_bytes=True,
                  method_sha256=sha(__file__),
                  scope='Complete represented fixed ordinary-stage population; no retail or whole-generator execution')
    (out / 'verification.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf8', newline='\n')
    print(json.dumps(dict(totals=totals, adversaries=checks)))


if __name__ == '__main__':
    main()
