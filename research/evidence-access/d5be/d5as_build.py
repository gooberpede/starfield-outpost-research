# SPDX-License-Identifier: GPL-3.0-or-later
"""Build a D5AS candidate and custody receipt from local retained evidence."""

import argparse
from io import BytesIO
import json
from math import isclose
from pathlib import Path
from struct import unpack, pack
import sys
from zipfile import ZIP_STORED, ZipFile, ZipInfo

import d5as_verify as reader


ROOT = Path(__file__).resolve().parents[3]
WORK = ROOT / '.local-work/d5be'
LOCAL = ROOT / '.local-work/d5as'
HISTORICAL = ROOT / 'research/resource-retained-population'
PACKAGE = 'd5as-feynman-geometry-v1.zip'
SEAL_PINS = {
    'd5as-closeout-evidence.zip': 'f0660067971738ba341562677efb0a3f0ca198f25478e09fea10880d0de90874',
    'corpus.zip': '4d0dc101ed7bc8204ae29273bf1eb87feeb8cf0b9ac291988da177511f81966b',
    'attempts-02.json': 'f248c86e940accf2643f3f9d4a1778e0d9f84bc03a9d93ec8131e6cebd34eefa',
    'frozen-corpus.json': '16784d4c772895ccad62415011014e2c6165906231498d203ed833f5a30dc598',
    'protection-before02/protection.json': '49b19aa5bd9043ad5486da1216b3475c1490a3787c05cd9ea21a31c94d2ae6d2',
    'protection-after01/protection.json': '0df32300a3564d21e7bea2b05f884ddcdc02f5798daaf4941a8f7e913b02c2f4',
    'series-authorization.json': 'f2ccb3a144578e2d8f50605719a7697cf4ceff2287b27dfb7e47a53b0b3c54e6',
    'freeze-review.json': '2e9318f4adc0d59aad9de4bb829c2be140d492ef04e5a3e212231cb5755d07e1',
}
REQUIRE = reader.require


def json_bytes(value):
    return (json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + '\n').encode('utf-8')


def archive_members(data):
    with ZipFile(BytesIO(data)) as archive:
        names = archive.namelist()
        REQUIRE(len(names) == len(set(names)), 'Duplicate original archive member')
        return {name: archive.read(name) for name in names}


def check_inventory(members, manifest_name, inventory_name, size_key):
    manifest = reader.load_json(members[manifest_name])[inventory_name]
    REQUIRE(set(members) == set(manifest) | {manifest_name}, 'Original member inventory differs')
    for name, record in manifest.items():
        REQUIRE(reader.pin(members[name]) == {'bytes': record[size_key], 'sha256': record['sha256']},
                f'Original member content differs: {name}')


def body_from_population(population):
    """Serialize represented native fields without using the frozen body builder."""
    body = bytearray(pack('<I', len(population)))
    for resource in sorted(population, key=lambda row: row['resource']):
        body.extend(bytes.fromhex(resource['resource']))
        body.extend(pack('<I', len(resource['regions'])))
        for region in resource['regions']:
            header = bytes.fromhex(region['header'])
            points = bytes.fromhex(region['points'])
            REQUIRE(len(header) == 24 and len(points) == 16 * region['count'],
                    'Source field widths differ')
            body.extend(header[:21])
            body.extend(pack('<I', region['count']))
            body.extend(points)
    reader.inspect_body(body)
    return bytes(body)


def geographic_key(diagnostic):
    if diagnostic['status'] != 'SOURCE_BYTES_UNQUALIFIED':
        return None
    terrain, chart, a, b, c, d, e, f = unpack('<IB6i', bytes.fromhex(diagnostic['semantic_bytes']))
    return f'{chart}:{a * 192 + c * 12 + e}:{b * 192 + d * 12 + f}:{terrain:08x}'


def source_custody(series):
    inputs = {name: series.read_file(LOCAL / name) for name in SEAL_PINS}
    for name, expected in SEAL_PINS.items():
        REQUIRE(reader.sha(inputs[name]) == expected, f'Historic digest differs: {name}')
    closeout = archive_members(inputs['d5as-closeout-evidence.zip'])
    check_inventory(closeout, 'manifest.json', 'members', 'bytes')
    for member, loose in {'captures/corpus.zip': 'corpus.zip',
                          'ledger/attempts-02.json': 'attempts-02.json',
                          'results/frozen-corpus.json': 'frozen-corpus.json',
                          'protection/before.json': 'protection-before02/protection.json',
                          'protection/after.json': 'protection-after01/protection.json',
                          'authorization/series-authorization.json': 'series-authorization.json',
                          'review/freeze-review.json': 'freeze-review.json'}.items():
        REQUIRE(closeout[member] == inputs[loose], f'Loose D5AS counterpart differs: {loose}')
    ledger = reader.load_json(inputs['attempts-02.json'])
    frozen = reader.load_json(inputs['frozen-corpus.json'])
    captures = archive_members(inputs['corpus.zip'])
    expected = [item['name'] for item in ledger['files']]
    REQUIRE(len(expected) == 130 and list(captures) == expected, 'Capture inventory/order differs')
    for item in ledger['files']:
        name = item['name']
        REQUIRE(reader.pin(captures[name]) == {key: item[key] for key in ('bytes', 'sha256')} and
                series.read_file(series.CAPTURE / name) == captures[name], f'Capture differs: {name}')
    REQUIRE(reader.load_json(closeout['review/freeze-review.json'])['pins'] == frozen['reviewed_pins'],
            'Independent pre-freeze pins differ from frozen result')
    pins = frozen['reviewed_pins']
    series.review_closeout(ledger, *(reader.load_json(inputs[name]) for name in
                           ('protection-before02/protection.json', 'protection-after01/protection.json',
                            'series-authorization.json', 'freeze-review.json')), pins)
    protection = reader.load_json(inputs['protection-after01/protection.json'])['protection']
    save_name = protection['save52']
    expected_save = protection['protected_live'][save_name]
    saves = [Path(protection['live_path']) / save_name]
    saves.extend(Path(item['path']) for item in protection['backups'][save_name]
                 if item['kind'] == 'LOOSE_BACKUP')
    saves.append(LOCAL / 'protection-after01/restore-rehearsal.sfs')
    REQUIRE(len(saves) >= 3, 'Expected live, loose backup and rehearsal save witnesses')
    for path in saves:
        REQUIRE(path.stat().st_size == expected_save['bytes'] and series.sha(path) == expected_save['sha256'],
                'Protected Save52 witness differs')
    return closeout, captures, ledger, frozen, saves


def original_references(series, ledger):
    frames = series.geometry.frames
    path = frames.baseline.ARCHIVE / 'episode-a.zip'
    archived = archive_members(series.read_file(path))
    check_inventory(archived, 'SOR-MANIFEST.json', 'files', 'size')
    pairs = {'raw/events.bin': frames.baseline.SESSION / 'events.bin',
             'raw/identity.json': frames.baseline.SESSION / 'identity.json',
             'raw/geometry-1.bin': frames.baseline.SESSION / 'geometry-1.bin',
             'notes/receipts/checkpoint-1793680114040295400.json':
                 frames.baseline.NOTES / 'receipts/checkpoint-1793680114040295400.json'}
    for member, loose in pairs.items():
        REQUIRE(archived[member] == series.read_file(loose), f'A0 loose member differs: {member}')
    references = series.geometry.reference_bundle()
    REQUIRE(references['inputs'] == ledger['reference_pins'], 'Pinned reference inventory differs')
    a0 = archived['notes/oracle-snapshot-1.normalized.bin']
    REQUIRE(reader.sha(a0) == frames.baseline.NORMALIZED and len(a0) == 5090 and
            a0[232:] == body_from_population(references['actual_a0_population']),
            'A0 historical envelope/body bridge differs')
    result = {}
    for label, run_index in (('mask0', 0), ('mask3', 1)):
        result[label] = body_from_population(references[f'{label}_population'])
        for project in ('d5aq', 'd5ag'):
            for repeat in ('geometry01', 'geometry02'):
                host = reader.load_json(series.read_file(ROOT / '.local-work' / project / repeat / 'control.json'))
                indices = (run_index,) if run_index == 0 else (1, 2)
                for index in indices:
                    REQUIRE(result[label] == body_from_population(host['runs'][index]['population']),
                            'Fixed native repeated body differs')
    REQUIRE(result['mask3'] == a0[232:], 'Fixed mask 3 does not match exact A0 body')
    return references, result, archived, pairs


def make_candidate(ledger, initial_ledger, frozen, captures, fixed, references):
    rows = sorted(ledger['attempts'], key=lambda r: (r['process']['creation_filetime'], r['utc'],
                                                     r['session_id'], r['capture_id']))
    initial_files = {r['name']: r for r in initial_ledger['files']}
    final_files = {r['name']: r for r in ledger['files']}
    REQUIRE(len(rows) == 31 and initial_ledger['qualified_samples'] == 29 and len(initial_files) == 126 and
            all(final_files[name] == row for name, row in initial_files.items()), 'Initial ledger join differs')
    REQUIRE(set(final_files) - set(initial_files) == {rows[-1]['snapshot'], *rows[-1]['startup_files']},
            'Replacement capture/startup join differs')
    REQUIRE([r['snapshot'] for r in rows if r['eligible']] == ledger['earliest_eligible_candidates'] ==
            [r['snapshot'] for r in frozen['roster']] and not frozen['later_eligible_attempts'],
            'Chronology/qualification differs from reviewed frozen roster')
    bodies = {f'references/{key}.bin': value for key, value in fixed.items()}
    manifest = {'schema': reader.SCHEMA, 'body_domain': reader.DOMAIN, 'frame': reader.FRAME,
                'references': {label: {'member': f'references/{label}.bin', 'pin': reader.pin(value)}
                               for label, value in fixed.items()}, 'attempts': []}
    joins = []
    position = 0
    for attempt, row in enumerate(rows, 1):
        original = captures[row['snapshot']]
        snapshot = reader.load_json(original)
        REQUIRE((snapshot['session_id'], snapshot['capture_id'], snapshot['process']) ==
                (row['session_id'], row['capture_id'], row['process']), 'Snapshot identity join differs')
        record = {'attempt': attempt, 'capture_uuid': row['capture_id'], 'original_snapshot': reader.pin(original)}
        manifest['attempts'].append(record)
        joins.append({'attempt': attempt, 'original_member': row['snapshot'],
                      'startup_members': row['startup_files'], 'eligibility_reasons': row['reasons']})
        if not row['eligible']:
            retired = [s['map_entry_id'] for s in snapshot['sources']
                       if s['source_diagnostics']['status'] == 'SOURCE_LIFETIME_RETIRED']
            REQUIRE(attempt == 6 and retired == ['map-entry-56'] and len(row['reasons']) == 1 and
                    'SOURCE_LIFETIME_RETIRED' in row['reasons'][0], 'Excluded raw diagnostic differs')
            record.update(status='EXCLUDED', reason='SOURCE_LIFETIME_RETIRED', source_entry=retired[0])
            continue
        position += 1
        selected = [s for s in snapshot['sources']
                    if geographic_key(s['source_diagnostics']) == reader.FRAME['geographic_key']]
        REQUIRE(len(selected) == 1, 'Independent geographic selection differs')
        holder = selected[0]
        body = body_from_population(holder['geometry']['population'])
        frozen_row = frozen['roster'][position - 1]
        geometry = frozen_row['geometry']
        REQUIRE(geometry['selected_entry'] == holder['map_entry_id'] and
                geometry['source_frame'] == references['actual_a0_frame'] and
                geometry['canonical_body_hex'] == body.hex() and frozen_row['capture_id'] == row['capture_id'] and
                frozen_row['sha256'] == record['original_snapshot']['sha256'], 'Independent body/freeze join differs')
        name = f'samples/{position:02}.bin'
        bodies[name] = body
        record.update(status='QUALIFIED', position=position, classification=geometry['class_name'],
                      geometry={'member': name, 'pin': reader.pin(body)})
        if attempt == 31:
            record['replacement_for_attempt'] = 6
        joins[-1].update(geometry_member=name, selected_entry=holder['map_entry_id'])
    verified = reader.verify(manifest, bodies)
    reference_stats = frozen['statistics']
    REQUIRE(verified['statistics']['n'] == reference_stats['n'] and
            verified['statistics']['null'] == reference_stats['null'] and
            verified['statistics']['binary_proxy_test'] == reference_stats['binary_proxy_test'],
            'Prespecified binary proxy statistics differ')
    for label, actual in verified['statistics']['classes'].items():
        expected = reference_stats['classes'][label]
        REQUIRE(actual['count'] == expected['count'] and actual['fraction'] == expected['fraction'] and
                all(isclose(left, right, rel_tol=0, abs_tol=1e-14) for left, right in
                    zip(actual['iid_marginal_ci95'], expected['iid_marginal_ci95'], strict=True)),
                'Prespecified marginal interval or census differs')
    return {'manifest.json': json_bytes(manifest)} | bodies, joins


def package_bytes(members):
    sink = BytesIO()
    with ZipFile(sink, 'w', compression=ZIP_STORED) as archive:
        for name, data in sorted(members.items()):
            # Explicit platform, timestamp and attributes for repeatable bytes.
            info = ZipInfo(name)
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data)
    return sink.getvalue()


def hash_inputs(series, paths):
    return {str(path): {'bytes': path.stat().st_size, 'sha256': series.sha(path)} for path in sorted(paths)}


def build(out):
    sys.path.insert(0, str(HISTORICAL))
    import d5as_series as series

    floor_before = series.disk_floor()
    closeout, captures, ledger, frozen, saves = source_custody(series)
    paths = ({LOCAL / name for name in SEAL_PINS} | {series.CAPTURE / name for name in captures} |
             {Path(name) for name in ledger['reference_pins']} | set(saves) |
             {ROOT / name for name in ledger['method_pins']} |
             {series.PACKAGE, LOCAL / 'package.json', LOCAL / 'independent-closeout-review.md',
              LOCAL / 'attempts-01.json', Path(__file__), Path(reader.__file__), Path(sys.executable),
              series.geometry.frames.baseline.SESSION / 'events.bin'})
    before = hash_inputs(series, paths)
    REQUIRE(all(before[name]['sha256'] == digest for name, digest in ledger['reference_pins'].items()) and
            all(before[str(ROOT / name)]['sha256'] == digest for name, digest in ledger['method_pins'].items()),
            'Pinned method or reference input differs')
    references, fixed, a0, a0_pairs = original_references(series, ledger)
    initial = series.read_file(LOCAL / 'attempts-01.json')
    REQUIRE(initial == closeout['ledger/attempts-01.json'], 'Initial eligibility ledger differs')
    REQUIRE(series.discover(references, ledger['documented_deviations']) == ledger,
            'Replay of historical eligibility method differs')
    members, joins = make_candidate(ledger, reader.load_json(initial), frozen, captures, fixed, references)
    payload = package_bytes(members)
    manifest, bodies = reader.read_package(payload)
    reader.verify(manifest, bodies)
    negatives = reader.negative_controls(manifest, bodies)
    REQUIRE(before == hash_inputs(series, paths), 'Read-only source hash guard changed')
    floor_after = series.disk_floor()
    custody = {
        'schema': 'sor-d5be-d5as-custody/1', 'access': 'LOCAL-ONLY', 'inputs': before,
        'closeout_members': {name: reader.pin(data) for name, data in closeout.items()},
        'capture_members': {name: reader.pin(data) for name, data in captures.items()},
        'a0_members': {name: reader.pin(data) for name, data in a0.items()},
        'a0_loose_member_joins': {name: str(path) for name, path in a0_pairs.items()},
        'source_to_derivative': joins,
        'fixed_reference_to_derivative': {
            f'references/{label}.bin': {
                'fixed_control_paths': [str(ROOT / '.local-work' / project / repeat / 'control.json')
                                        for project in ('d5aq', 'd5ag') for repeat in ('geometry01', 'geometry02')],
                'population_run_indices_zero_based': indices,
            } for label, indices in (('mask0', [0]), ('mask3', [1, 2]))
        },
        'candidate_zip': {PACKAGE: reader.pin(payload)},
        'candidate_members': {name: reader.pin(data) for name, data in members.items()},
        'negative_controls': negatives, 'free_bytes_before': floor_before, 'free_bytes_after': floor_after,
        'source_hash_guard': 'EQUAL',
    }
    out.mkdir(parents=True, exist_ok=False)
    for name, data in ((PACKAGE, payload), ('d5as-custody.json', json_bytes(custody))):
        with (out / name).open('xb') as stream:
            stream.write(data)
    print(json.dumps({'candidate_zip': custody['candidate_zip'], 'source_inputs': len(before),
                      'closeout_members': len(closeout), 'capture_members': len(captures), 'a0_members': len(a0),
                      'output_members': len(members), 'negative_controls': negatives}, sort_keys=True))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path, help='Fresh immediate child of .local-work/d5be')
    args = parser.parse_args()
    out = args.output.resolve()
    try:
        REQUIRE(not sys.flags.optimize and sys.dont_write_bytecode and sys.flags.ignore_environment,
                'Run with Python -E -B without optimization')
        REQUIRE(out.parent == WORK and WORK.resolve() == WORK and not out.exists(),
                'Use a fresh immediate child of the task staging directory')
        build(out)
    except (OSError, ValueError, KeyError, RuntimeError) as error:
        parser.exit(1, f'D5AS build failed: {error}\n')


if __name__ == '__main__':
    main()
