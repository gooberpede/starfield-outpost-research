# SPDX-License-Identifier: GPL-3.0-or-later
"""Read-only D5AS controls using sealed local Pilot04/A0/fixed-native evidence.

Synthetic mutations stay in memory and carry a separate evidence role. This
program prints a JSON receipt. It does not operate the game, write inputs,
execute native binaries, create captures, or access the network.
"""

from collections import Counter
from copy import deepcopy
import csv
from datetime import datetime, timedelta, timezone
from io import BytesIO
import json
from pathlib import Path
import struct
import sys
import uuid

import d5as_geometry as method
import d5ar_snapshot as raw
import d5ar_source_frames as frames


def reseal(value):
    for entry in value['sources']:
        if entry['geometry'] is not None:
            entry['geometry_sha256'] = raw.digest(raw.encoded(entry['geometry']))
    return raw.seal(value)


def fixture(pilot, refs, variant='mask3', sequence=1):
    """Create a labeled fixture with one positively attributed source."""
    value = deepcopy(pilot)
    target = next(row for row in value['sources']
                  if raw.candidate_source_key(row['source_diagnostics']) == frames.TARGET)
    value['sources'] = [target]
    payload = target['geometry']
    value.update(evidence_basis='SYNTHETIC', capture_id=str(uuid.UUID(int=2 * sequence, version=4)),
                 session_id=str(uuid.UUID(int=2 * sequence + 1, version=4)))
    stamp = datetime(2026, 11, 7, tzinfo=timezone.utc) + timedelta(minutes=sequence)
    value['utc'] = stamp.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    ticks = (stamp - datetime(1601, 1, 1, tzinfo=timezone.utc)) // timedelta(microseconds=1) * 10
    value['process'].update(pid=1000 + sequence, creation_filetime=ticks - 1_000_000)
    value['capture_diagnostics'].update(copy_begin_filetime=ticks + 1, copy_end_filetime=ticks + 10_000)
    payload.update(session_id=value['session_id'], snapshot_id=value['capture_id'],
                   population=deepcopy(refs[('mask0' if variant == 'mask0' else 'mask3') + '_population']))
    if variant == 'other':
        region = next(region for row in payload['population'] for region in row['regions'] if region['count'])
        first = region['points'][:32]
        width = '0000803f' if first[24:] != '0000803f' else '00000040'
        region['points'] = first[:24] + width + region['points'][32:]
    regions = [r for row in payload['population'] for r in row['regions']]
    payload['capture'].update(resource_slots=len(payload['population']), region_total=len(regions),
                              point_total=sum(r['count'] for r in regions))
    counts = payload['capture']
    value['capture_diagnostics']['required_bytes'] = (224 + 32 * counts['resource_slots'] +
                                                     56 * counts['region_total'] + 16 * counts['point_total'])
    return reseal(value)


def independent_body(population):
    """Independent field-level construction of the complete comparison wire."""
    stream = BytesIO()
    stream.write(len(population).to_bytes(4, 'little'))
    for record in sorted(population, key=lambda r: r['resource']):
        form = int(record['resource'], 16)
        stream.write(form.to_bytes(4, 'big'))
        stream.write(len(record['regions']).to_bytes(4, 'little'))
        for region in record['regions']:
            header = bytes.fromhex(region['header'])
            x, y, z, radius, header_form, kind, _padding = struct.unpack('<IIIIIB3s', header)
            raw.require(header_form == form, 'Independent oracle resource identity mismatch')
            stream.write(struct.pack('<IIIIIBI', x, y, z, radius, header_form, kind, region['count']))
            points = tuple(struct.iter_unpack('<4I', bytes.fromhex(region['points'])))
            raw.require(len(points) == region['count'], 'Independent oracle point count mismatch')
            for point in points:
                stream.write(struct.pack('<4I', *point))
    return stream.getvalue()


def main():
    raw.guard()
    paths = (Path(__file__), Path(method.__file__), Path(sys.executable))
    pins = {str(path): frames.sha(path) for path in paths}
    pilot, refs = method.pilot_snapshot(), method.reference_bundle()
    checks = []

    def check(name, result):
        raw.require(result, 'Failed control: ' + name)
        checks.append(name)

    historical = frames.classify(pilot, refs)
    scoped = method.classify(pilot, refs)
    check('frozen historical producer refusal', historical['class_name'] == 'UNAVAILABLE/INCONCLUSIVE' and
          historical['reason'] == 'Producer interval profile not admitted')
    check('versioned Pilot04 source selection among all 36 rows',
          scoped['eligible'] and scoped['readable_source_count'] == 36 and scoped['selected_entry'] == 'map-entry-6')
    reduced = deepcopy(pilot)
    reduced['sources'].pop()
    refusal = method.admit(reseal(reduced), refs)
    check('resealed whole non-target row deletion fails native census extent',
          not refusal['eligible'] and 'required bytes' in refusal['reason'])
    check('Pilot04 exact fixed3 result', scoped['class_name'] == 'MATCH_MASK3_REFERENCE')
    check('Pilot04 exact independent receipt', (scoped['body_length'], scoped['body_sha256']) ==
          method.REFERENCE_BODIES['actual_a0'])
    review_path = method.LOCAL / 'review-pilot04-feynman-comparison01.json'
    review_bytes = review_path.read_bytes()
    review = json.loads(review_bytes, object_pairs_hook=raw.unique_pairs)
    check('rejoins pinned independent Pilot04 review',
          raw.digest(review_bytes) == '3b1d72edede5d3b3c054d1f1e383e6a4e8efd1f6c9f24640081cc82aafe6f6cc' and
          review['snapshot_sha256'] == method.PILOT_SNAPSHOT_SHA256 and
          review['archive_sha256'] == method.PILOT_ARCHIVE_SHA256 and
          review['target_entry'] == scoped['selected_entry'] and review['target_frame'] == scoped['source_frame'] and
          review['target_body_sha256'] == scoped['body_sha256'])
    selected = next(row for row in pilot['sources'] if row['map_entry_id'] == scoped['selected_entry'])
    diagnostic = selected['source_diagnostics']
    terrain, chart, ax, ay, bx, by, cx, cy = struct.unpack('<IB6i', bytes.fromhex(diagnostic['semantic_bytes']))
    coordinates = chart, 192 * ax + 12 * bx + cx, 192 * ay + 12 * by + cy, terrain
    check('independent Pilot04 geographic operands and owner',
          coordinates == (0, 37536, 20928, 0x29d20e) and
          struct.unpack('<I', bytes.fromhex(pilot['owner_context']['before']['owner_formid_word'])) == (0x5e0de,))
    descriptor = bytes.fromhex(diagnostic['source_descriptor_bytes'])
    semantic = bytes([descriptor[0]]) + descriptor[4:44]
    ox, oy, px, py = struct.unpack('<4i', bytes.fromhex(diagnostic['origin_input_words']))
    check('independent full semantic descriptor and exact origin',
          semantic.hex() == refs['actual_a0_frame']['descriptor_semantic41'] and
          (ox, oy, px, py) == (0, 0, 2, 2) and
          [(ox - px) * 100, (oy - py) * 100] == scoped['source_frame']['native_origin_i32'])

    bodies = {name: independent_body(refs[name + '_population']) for name in method.REFERENCE_BODIES}
    for key, body in bodies.items():
        check('independent canonical full fields ' + key, (len(body), raw.digest(body)) == method.REFERENCE_BODIES[key] and
              body == frames.body_bytes(refs[key + '_population']))
    for path in method.D5AG_ORACLES:
        runs = json.loads(path.read_bytes(), object_pairs_hook=raw.unique_pairs)['runs']
        check('independent D5AG body construction ' + path.parent.name,
              [independent_body(run['population']) for run in runs] ==
              [bodies['mask0'], bodies['mask3'], bodies['mask3']])
    check('all Pilot04 body bytes equal A0 and fixed3 only',
          bytes.fromhex(scoped['canonical_body_hex']) == bodies['actual_a0'] == bodies['mask3'] != bodies['mask0'])
    a0_path = frames.ROOT / '.local-work/d5al/baseline01/a0.normalized.bin'
    a0_envelope = a0_path.read_bytes()
    source_size, = struct.unpack_from('<I', a0_envelope)
    frame_size, = struct.unpack_from('<I', a0_envelope, 4 + source_size)
    body_at = 8 + source_size + frame_size
    check('separate A0 envelope digest and independently extracted body',
          len(a0_envelope) == 5090 and raw.digest(a0_envelope) == frames.baseline.NORMALIZED and
          body_at == 232 and a0_envelope[body_at:] == bodies['actual_a0'])
    check('first fixed0 difference is ordered collection size',
          scoped['first_difference_from_mask0'] == dict(resource='000057cf', field='region_count', left=18, right=57))
    census = next(path for path in method.DEPENDENCY_PINS if path.name == 'd5aq-request-mask-map.csv')
    with census.open(encoding='utf-8', newline='') as stream:
        rows = list(csv.DictReader(stream))
    directly_sampled = [row for row in rows if row['classification'] == 'PROVEN']
    check('independent C1 coordinate census and single N2 directly sampled case',
          len({(row['original_x'], row['original_y']) for row in rows}) == 196 and
          {row['input_contract'] for row in rows} == {'D5AQ-C1'} and
          Counter(row['classification'] for row in rows) == {'CONDITIONAL': 195, 'PROVEN': 1} and
          [(r['original_x'], r['original_y'], r['mask']) for r in directly_sampled] == [('-2', '11', '0x3')] and
          Counter(row['mask'] for row in rows) == {'0x0': 28, '0x3': 168})

    synthetic = fixture(pilot, refs)
    check('synthetic role cannot be admitted through native path', not method.admit(synthetic, refs)['eligible'])
    check('native role cannot be admitted through synthetic path', not method.admit(pilot, refs, synthetic=True)['eligible'])
    for variant, expected in (('mask0', 'MATCH_MASK0_REFERENCE'), ('mask3', 'MATCH_MASK3_REFERENCE'),
                              ('other', 'OTHER_QUALIFIED_GEOMETRY')):
        value = fixture(pilot, refs, variant)
        result = method.classify(value, refs, synthetic=True)
        check('synthetic reference control ' + variant,
              result['eligible'] and result['class_name'] == expected and result['role'] == 'SYNTHETIC')
    altered = fixture(pilot, refs, 'other')
    altered_result = method.classify(altered, refs, synthetic=True)
    check('eligibility independent of mask reference bodies',
          method.admit(altered, {'actual_a0_frame': refs['actual_a0_frame']}, synthetic=True)['eligible'])
    check('new geometry with same counts retains fourth word difference',
          altered_result['geometry_counts'] == scoped['geometry_counts'] and
          altered_result['first_difference_from_mask3']['word'] == 3)
    copied = deepcopy(synthetic)
    regions = copied['sources'][0]['geometry']['population']
    regions.reverse()
    region = next(row for r in regions for row in r['regions'])
    region['header'] = region['header'][:42] + 'a1b2c3'
    check('resource-order and header-padding changes preserve canonical equality',
          method.classify(reseal(copied), refs, synthetic=True)['class_name'] == 'MATCH_MASK3_REFERENCE')
    adjustment = deepcopy(synthetic)
    adjustment['capture_diagnostics']['copy_end_filetime'] = 1
    check('wall-clock adjustment is diagnostic',
          method.admit(reseal(adjustment), refs, synthetic=True)['clock_adjustment_diagnostic'])

    def rejection(name, mutation, reason, seal=True):
        value = deepcopy(synthetic)
        source = value['sources'][0]
        payload = source['geometry']
        region = next(r for resource in payload['population'] for r in resource['regions'] if r['count'])
        mutation(value, source, payload, region)
        try:
            if seal:
                reseal(value)
        except ValueError as error:
            check(name, reason in str(error))
        else:
            result = method.admit(value, refs, synthetic=True)
            check(name, not result['eligible'] and reason in result['reason'])

    rejection('historical D5AR DLL profile outside D5AS', lambda v, *_: v.update(build=frames.NATIVE_BUILD),
              'producer profile differs')
    rejection('one different source lock', lambda v, *_: v['build'].update(source_lock_sha256='0' * 64),
              'producer profile differs')
    rejection('producer refusal retained', lambda v, *_: (v.update(status='REFUSED'),
              v['capture_diagnostics'].update(copy_status='NATIVE_READER_BUSY')), 'NATIVE_READER_BUSY')
    rejection('reader count zero', lambda v, *_: v['capture_diagnostics'].update(lock_state=0), 'native reader')
    rejection('exclusive owner lock state', lambda v, *_: v['capture_diagnostics'].update(lock_state=0x400001), 'native reader')
    rejection('epoch changed', lambda v, *_: v['capture_diagnostics'].update(epoch_end=99), 'lifecycle')
    rejection('copy end missing', lambda v, *_: v['capture_diagnostics'].update(copy_end_filetime=0), 'copy interval')
    rejection('copy extent too small', lambda v, *_: v['capture_diagnostics'].update(required_bytes=16),
              'required bytes')
    rejection('ProcGen differs', lambda v, *_: v['capture_diagnostics'].update(proc_identity_token='proc-pointer-65536'),
              'Copy ProcGen differs')
    rejection('owner manager replaced', lambda v, *_: v['owner_context']['after'].update(manager_pointer_token='runtime-pointer-65536'),
              'changed current owner')
    rejection('owner descriptor mutation within copy', lambda v, *_: v['owner_context']['after'].update(current_descriptor_bytes='00' * 44),
              'changed current owner')
    rejection('wrong owner both ends', lambda v, *_: [o.update(owner_formid_word='00010000')
              for o in v['owner_context'].values()], 'mode or body')
    rejection('wrong owner mode both ends', lambda v, *_: [o.update(mode=1)
              for o in v['owner_context'].values()], 'mode or body')
    rejection('source semantic and descriptor projection disagree', lambda v, s, *_:
              s['source_diagnostics'].update(source_descriptor_bytes='01' + s['source_diagnostics']['source_descriptor_bytes'][2:]),
              'Geography and full descriptor disagree')
    rejection('same key but altered semantic descriptor word', lambda v, s, *_:
              s['source_diagnostics'].update(source_descriptor_bytes=s['source_diagnostics']['source_descriptor_bytes'][:24] + '00' * 4 +
              s['source_diagnostics']['source_descriptor_bytes'][32:]), 'coordinate basis differs')
    rejection('same key but altered origin input', lambda v, s, *_:
              s['source_diagnostics'].update(origin_input_words='01000000' + s['source_diagnostics']['origin_input_words'][8:]),
              'coordinate basis differs')

    def duplicate(value, source, *_):
        extra = deepcopy(source)
        extra.update(map_entry_id='map-entry-1000', allocation_id='source-pointer-65536', holder_id='holder-pointer-65536')
        value['sources'].append(extra)

    def retired(value, source, *_):
        duplicate(value, source)
        diagnostic = value['sources'][-1]['source_diagnostics']
        for field in ('status', 'origin_status', 'descriptor_status'):
            diagnostic[field] = 'SOURCE_LIFETIME_RETIRED'
        for field in ('semantic_bytes', 'origin_input_words', 'source_descriptor_bytes', 'visited_token'):
            diagnostic[field] = None

    rejection('duplicate geographic target', duplicate, 'found 2')
    rejection('unreadable retained source can conceal second target', retired, 'SOURCE_LIFETIME_RETIRED')
    rejection('duplicate map entry', lambda v, s, *_: v['sources'].append(deepcopy(s)), 'duplicate map entry')
    rejection('empty target holder', lambda v, s, *_: (
              v['capture_diagnostics'].update(required_bytes=224),
              s.update(geometry=None, geometry_sha256=None, source_disposition='EMPTY')),
              'no nonempty complete geometry')
    rejection('false source/frame overlay', lambda v, s, p, r: p.update(frame=dict(
              basis='consumed-descriptor-v1', owner_formid='0005e0de', descriptor_semantic='00' * 41)), 'geometry overlay')
    rejection('truncated point array', lambda v, s, p, r: r.update(points=r['points'][:-2]), 'hex')
    rejection('nonfinite point', lambda v, s, p, r: r.update(points='0000c07f' + r['points'][8:]), 'Nonfinite point')
    rejection('nonplanar point', lambda v, s, p, r: r.update(points=r['points'][:16] + '0000803f' + r['points'][24:]),
              'outside proved native plane')
    rejection('geometry mutated without valid hashes', lambda v, s, p, r: r.update(
              points='0000803f' + r['points'][8:]), 'Raw geometry hash mismatch', seal=False)
    rejection('invalid whole-envelope checksum', lambda v, *_: v.update(payload_sha256='0' * 64),
              'Snapshot hash mismatch', seal=False)

    check('exact method, control driver and interpreter source preserved',
          pins == {str(path): frames.sha(path) for path in paths})
    input_pins = refs['inputs'] | {str(a0_path): raw.digest(a0_envelope), str(review_path): raw.digest(review_bytes),
                                   str(method.PILOT_ARCHIVE): method.PILOT_ARCHIVE_SHA256}
    print(json.dumps(dict(status='PASS', method=method.METHOD, checks=checks, check_count=len(checks),
                          historical_disposition=historical['reason'],
                          pilot={k: v for k, v in scoped.items() if k != 'canonical_body_hex'},
                          source_pins=pins, reference_inputs=input_pins, reference_bodies=method.REFERENCE_BODIES,
                          disk_floors=raw.guard())))


if __name__ == '__main__':
    main()
