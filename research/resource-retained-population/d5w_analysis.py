# SPDX-License-Identifier: GPL-3.0-or-later
"""Evaluate D5W scheduling, source controls and inherited consumer evidence.

Reads authored tables and authenticated local receipts/exports. Writes a fresh
ignored analysis JSON. Does not execute native instructions, access saves,
modify Ghidra or Git, install dependencies, or use the network. Owned D5S
consistency checks are reused under SOR-P-0002 with their source hash recorded.
"""
from pathlib import Path
from collections import Counter
import csv
import hashlib
import json
import shutil
import struct
import sys
import re

ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / 'docs/experiments/resource-retained-population'
LOCAL = ROOT / '.local-work/d5w'


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding='utf8'))


def rows(path):
    with Path(path).open(encoding='utf8', newline='') as stream:
        return list(csv.DictReader(stream))


def main():
    output = Path(sys.argv[1]).resolve()
    assert output.is_relative_to(ROOT / '.local-work') and not output.exists()
    initial = read(LOCAL / 'initial.json')
    floor = {drive: shutil.disk_usage(drive).free for drive in ('C:/', 'D:/')}
    assert min(floor.values()) >= 40_000_000_000
    for category in ('installed', 'database'):
        assert {p: sha(p) for p in initial[category]} == initial[category]
    inherited = read(LOCAL / 'inherited-index.json')
    for p, h in inherited['paths'].items():
        assert sha(ROOT / p) == h, p
    lease = ROOT / '.local-work/resources-evidence-consolidation/d5u-c1-input-lease01'
    members = read(lease / 'LEASE.json')
    assert members['state'] == 'OPEN'
    for row in members['rows']:
        p = lease / row['path']
        assert p.stat().st_size == row['bytes'] and sha(p) == row['sha256']
    recovered = []
    for row in inherited['missing']:
        member = next(r for r in members['rows'] if r['path'] == row['path'])
        assert member['sha256'] == row['expected']
        recovered.append(row['path'])
    import d5s_controls
    prior = d5s_controls.check(ROOT / '.local-work/d5s')
    candidates = rows(DOC / 'd5t/candidates.csv')
    lookup = {(int(r['local_x']), int(r['local_y'])): r for r in candidates}
    assert len(lookup) == 196
    assert Counter(int(r['mask']) for r in candidates) == {0: 28, 3: 168}
    registration = read(ROOT / '.local-work/d5s/registration.json')['density_order']
    eligible = [(i, q) for i, q in enumerate(registration) if tuple(q) in lookup]
    assert eligible[0] == (419, [-2, 11])
    first0 = next((i, q) for i, q in eligible if lookup[tuple(q)]['mask'] == '0')
    assert first0 == (833, [-2, -1])
    native = read(LOCAL / 'native01.json')
    assert native['code_sha256'] == sha(Path(__file__).with_name('d5w_native.py'))
    claims = []
    for run in native['runs']:
        assert sorted(run['claims']) == list(range(1720))
        i = next(i for i in run['claims'] if tuple(registration[i]) in lookup)
        assert i == run['first_index']
        claims.append({k: v for k, v in run.items() if k != 'claims'} |
                      {'mask': int(lookup[tuple(run['first_query'])]['mask'])})
    catalogue = {r['source_id']: r for r in rows(DOC / 'd5u/catalogue.csv')}
    assert json.loads(catalogue['U01']['histogram']) == {'8': 196}
    assert json.loads(catalogue['U26']['histogram']) == {'0': 24, '1': 4, '3': 168}
    # Authenticate exact geometry bytes against the already executed predicate receipt.
    consumer = read(ROOT / '.local-work/d5v/native05.json')
    assert consumer['passed'] == len(consumer['rows']) == len(consumer['point_rows']) == 606
    by_label = {r['label']: r for r in consumer['rows']}
    point_label = {r['label']: r for r in consumer['point_rows']}
    cases = {}
    for case in ('D2-83388f', 'D2-84e101'):
        data = read(DOC / 'd5u/outposts' / (case + '.json'))
        ref = data['reference']
        frame = next(r for r in rows(ROOT / 'docs/experiments/static-exhaustion/saved-center-frame.csv')
                     if r['sample'] == 'HIST-0267' and r['token'] == ref['beacon_token'])
        projection = next(r for r in rows(ROOT / 'docs/experiments/durable-center/projection.csv')
                          if r['sample'] == 'HIST-0267' and r['token'] == ref['beacon_token'])
        local = [float(projection['local_' + a]) for a in 'xyz']
        assert struct.pack('<3f', *local).hex() == frame['center_hex']
        assert projection['compensation'] == '00' * 12
        center = [struct.unpack('<f', struct.pack('<f', local[k] + 100 *
                  (int(frame['site_' + a]) - int(frame['origin_' + a]))))[0]
                  for k, a in enumerate('xy')] + local[2:]
        assert center == ref['center'] == ref['beacon']
        layers = []
        for layer in data['layers']:
            area, point = Counter(), Counter()
            for i, region in enumerate(layer['regions']):
                label = f'{case}/{layer["id"]}/{i}'
                witness = by_label[label]
                payload = bytes.fromhex(region['native_bound_le'] + region['ordered_xyzw_le'])
                assert hashlib.sha256(payload).hexdigest() == witness['geometry_sha256']
                assert witness['native_accepted'] == region['ordinary_callback']['accepted']
                if witness['native_accepted']:
                    area[region['resource']] += 1
                if point_label[label]['native_point']:
                    point[region['resource']] += 1
            layers.append(dict(id=layer['id'], source_id=layer['source_id'], mask=layer['mask'],
                               variant_count=layer['variant_count'], area=dict(area), point=dict(point),
                               geometry_sha256=hashlib.sha256(json.dumps(layer['regions'], sort_keys=True).encode()).hexdigest()))
        cases[case] = dict(reference=ref, layers=layers, palette=data['palette'])
    special = point_label['area-versus-point']
    assert special['native_area'] and not special['native_point']
    # Check every exported direct relative CALL against installed instruction bytes.
    exe = Path(next(p for p in initial['installed'] if p.endswith('Starfield.exe')))
    image = exe.read_bytes()
    pe = struct.unpack_from('<I', image, 0x3c)[0]
    opts = struct.unpack_from('<H', image, pe + 20)[0]
    count = struct.unpack_from('<H', image, pe + 6)[0]
    base = struct.unpack_from('<Q', image, pe + 48)[0]
    sections = [struct.unpack_from('<IIII', image, pe + 24 + opts + i * 40 + 8) for i in range(count)]
    def offset(va):
        for _, start, size, raw in sections:
            if start <= va - base < start + size:
                return raw + va - base - start
        raise ValueError(hex(va))
    exports, call_count, data_count, failed_exports = {}, 0, 0, []
    for path in sorted(LOCAL.glob('export*/native.tsv')):
        if not path.with_name('result.json').exists():
            assert path.parent.name in ('export10', 'export26')
            assert not path.read_text().endswith('END\n')
            failed_exports.append(dict(path=str(path.relative_to(ROOT)), sha256=sha(path),
                                       reason='Unsupported @ request (10) or missing defined getter function (26); incomplete, excluded from successful call checks'))
            continue
        receipt = read(path.with_name('result.json'))
        assert sha(path) == receipt['sha256'] and receipt['database_unchanged']
        for at, target in re.findall(r'^([0-9a-f]+)\tCALL 0x([0-9a-f]+)$', path.read_text(), re.M):
            va = int(at, 16)
            off = offset(va)
            assert image[off] == 0xe8
            assert va + 5 + struct.unpack_from('<i', image, off + 1)[0] == int(target, 16)
            call_count += 1
        for at, value in re.findall(r'^([0-9a-f]+)\t([0-9a-f]{1,16})$', path.read_text(), re.M):
            assert struct.unpack_from('<Q', image, offset(int(at, 16)))[0] == int(value, 16)
            data_count += 1
        exports[str(path.relative_to(ROOT))] = sha(path)
    inputs = [DOC / 'd5t/candidates.csv', DOC / 'd5u/catalogue.csv',
              DOC / 'd5v/spatial.json', ROOT / '.local-work/d5v/native05.json',
              LOCAL / 'native01.json', lease / 'LEASE.json']
    result = dict(schema='sor-d5w-analysis/1', method_sha256=sha(__file__),
                  identity='PASS', free=floor, recovered_archived_members=recovered,
                  inherited_authenticated_files=len(inherited['paths']), d5s=prior,
                  direct_calls_verified=call_count, data_words_verified=data_count,
                  exports=exports, failed_exports=failed_exports,
                  registration=dict(first_target=eligible[0], first_mask0=first0,
                                    intervening_registrations=first0[0]-eligible[0][0],
                                    meaning='Ordinal readiness opportunity, not elapsed latency or probability'),
                  claims=claims, cases=cases,
                  controls={k: catalogue[k] for k in ('U01', 'U26')},
                  area_point_control=special,
                  inputs={str(p.relative_to(ROOT)): sha(p) for p in inputs})
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('x', encoding='utf8', newline='\n') as stream:
        stream.write(json.dumps(result, indent=2) + '\n')
    print(json.dumps(dict(direct_calls=call_count, first_target=eligible[0], first_mask0=first0,
                          claims=len(claims), recovered=len(recovered), cases=list(cases)), indent=2))


if __name__ == '__main__':
    main()
