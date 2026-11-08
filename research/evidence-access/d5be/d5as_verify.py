# SPDX-License-Identifier: GPL-3.0-or-later
"""Verify a D5BE D5AS candidate ZIP with Python's standard library, read-only."""

import argparse
from collections import Counter
from copy import deepcopy
from fractions import Fraction
import hashlib
from io import BytesIO
import json
from math import comb, isfinite
from pathlib import Path
import re
from struct import unpack, unpack_from
from uuid import UUID
from zipfile import BadZipFile, ZipFile


SCHEMA = 'sor-d5be-d5as-geometry/1'
DOMAIN = 'sor-d5as-feynman-source-geometry/1:canonical-body'
FRAME = {'geographic_key': '0:37536:20928:0029d20e', 'body_formid': '0005e0de',
         'source_planar_origin': [-200, -200]}
REFERENCE_PINS = {
    'mask0': (4966, 'bba4c877bc14d8abd3cfe36313e4cd62fd98e510dbf18441b250eacb57b942c4'),
    'mask3': (4858, '7b66c2cce4b0c4c2d52a91a41d02997f12632d0c197681fcf4f21cb87bdbf653'),
}
MASK0 = 'MATCH_MASK0_REFERENCE'
MASK3 = 'MATCH_MASK3_REFERENCE'
OTHER = 'OTHER_QUALIFIED_GEOMETRY'
MASK0_POSITIONS = {7: '359325f8-3088-4997-a348-a559dbd403c3',
                   13: 'adb8bb75-84e1-4b7e-87f9-1a150741f6b4'}
EXCLUDED = '7edfc207-4f95-4cdc-9617-ce847107c49c'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def pin(data):
    return {'bytes': len(data), 'sha256': sha(data)}


def load_json(data):
    def unique(pairs):
        values = dict(pairs)
        require(len(values) == len(pairs), 'Duplicate JSON key')
        return values

    def nonfinite(token):
        raise ValueError(f'Invalid JSON number {token}')

    return json.loads(data, object_pairs_hook=unique, parse_constant=nonfinite)


def inspect_body(data):
    """Walk every field and require exact end-of-body consumption."""
    stream = BytesIO(data)

    def take(length):
        require(length <= len(data) - stream.tell(), 'Truncated canonical body')
        return stream.read(length)

    def u32():
        return unpack('<I', take(4))[0]

    def planar_words(raw):
        require(all(isfinite(value) for value in unpack('<4f', raw)), 'Nonfinite geometry')
        require(unpack_from('<I', raw, 8)[0] in (0, 0x80000000), 'Nonplanar geometry')

    resources = u32()
    previous_form = -1
    regions = points = 0
    for _ in range(resources):
        form = int.from_bytes(take(4), 'big')
        require(form > previous_form, 'Resource FormID order or uniqueness differs')
        previous_form = form
        count = u32()
        regions += count
        for _ in range(count):
            header = take(21)
            planar_words(header[:16])
            require(unpack_from('<I', header, 16)[0] == form, 'Region FormID differs')
            point_count = u32()
            points += point_count
            raw_points = take(16 * point_count)
            for offset in range(0, len(raw_points), 16):
                planar_words(raw_points[offset:offset + 16])
    require(stream.tell() == len(data) and points > 0, 'Canonical body extent or census differs')
    return {'resources': resources, 'regions': regions, 'points': points}


def statistics(counts):
    """Invert exact marginal binomial tails and sum the conditional null masses."""
    n = sum(counts.values())

    def quantile(first, last, target):
        low, high = 0.0, 1.0
        for _ in range(54):
            p = (low + high) / 2
            probability = sum(comb(n, x) * p**x * (1 - p)**(n - x)
                              for x in range(first, last + 1))
            if probability < target:
                low = p
            else:
                high = p
        return (low + high) / 2

    summary = {}
    for name in (MASK0, MASK3, OTHER):
        k = counts[name]
        summary[name] = {
            'count': k, 'fraction': k / n,
            'iid_marginal_ci95': [0.0 if k == 0 else quantile(k, n, .025),
                                  1.0 if k == n else quantile(k + 1, n, .975)],
        }
    result = {'n': n, 'classes': summary, 'binary_proxy_test': 'INCONCLUSIVE_OTHER_GEOMETRY',
              'null': None}
    if not counts[OTHER]:
        k = counts[MASK0]
        masses = [Fraction(comb(n, x) * 6**(n - x), 7**n) for x in range(n + 1)]
        result['binary_proxy_test'] = 'CONDITIONAL_IID_COMPARISON'
        result['null'] = {
            'null_p': '1/7', 'assumes_iid': True,
            'lower_inclusive': float(sum(masses[:k + 1])),
            'upper_inclusive': float(sum(masses[k:])),
            'probability_order_two_sided': float(sum(p for p in masses if p <= masses[k])),
            'all_mask3_equivalent': float(masses[0]),
        }
    return result


def verify(manifest, bodies):
    require(manifest['schema'] == SCHEMA and manifest['body_domain'] == DOMAIN,
            'Wrong schema or geometry byte domain')
    require(manifest['frame'] == FRAME, 'Wrong Feynman source/frame')
    require(set(manifest['references']) == set(REFERENCE_PINS), 'Reference inventory differs')
    require(len(manifest['attempts']) == 31, 'Chronological roster must contain 31 attempts')
    used = set()

    def body(record, name):
        require(record['member'] == name and name in bodies and name not in used,
                f'Missing, duplicated or misplaced body member {name}')
        data = bodies[name]
        require(pin(data) == record['pin'], f'Body hash or size differs for {name}')
        inspect_body(data)
        used.add(name)
        return data

    references = {}
    for label, expected in REFERENCE_PINS.items():
        value = body(manifest['references'][label], f'references/{label}.bin')
        require((len(value), sha(value)) == expected, f'Historical {label} reference pin differs')
        references[label] = value

    captures = set()
    counts = Counter()
    qualified = []
    for index, record in enumerate(manifest['attempts'], 1):
        capture = record['capture_uuid']
        require(str(UUID(capture)) == capture and capture not in captures,
                'Duplicate or noncanonical capture UUID')
        captures.add(capture)
        require(record['attempt'] == index, 'Chronological attempt order differs')
        source = record['original_snapshot']
        require(type(source['bytes']) is int and source['bytes'] > 0 and
                re.fullmatch(r'[0-9a-f]{64}', source['sha256']), 'Malformed original snapshot pin')
        if index == 6:
            require(capture == EXCLUDED and record['status'] == 'EXCLUDED' and
                    record['reason'] == 'SOURCE_LIFETIME_RETIRED' and
                    record['source_entry'] == 'map-entry-56' and
                    record.get('geometry') is None and record.get('position') is None and
                    record.get('classification') is None, 'Wrong exclusion or exclusion leakage')
            continue
        position = len(qualified) + 1
        require(record['position'] == position and record['status'] == 'QUALIFIED',
                'Qualified sample order differs')
        require(record.get('replacement_for_attempt') == (6 if index == 31 else None),
                'Wrong replacement trace')
        value = body(record['geometry'], f'samples/{position:02}.bin')
        classification = OTHER
        if value == references['mask0']:
            classification = MASK0
        elif value == references['mask3']:
            classification = MASK3
        require(classification == record['classification'],
                f'Incorrect recorded classification at position {position}')
        expected = MASK0_POSITIONS.get(position)
        require((capture, classification) == (expected, MASK0) if expected else
                classification == MASK3, f'Historical class or witness differs at {position}')
        counts[classification] += 1
        qualified.append({'position': position, 'capture_uuid': capture, 'classification': classification})
    require(len(qualified) == 30 and used == set(bodies), 'Unexpected sample or body inventory')
    return {'qualified': qualified, 'statistics': statistics(counts)}


def negative_controls(manifest, bodies):
    """Use mutated in-memory copies of actual comparison inputs, never source bytes."""
    changed_body = bytearray(bodies['samples/01.bin'])
    require(inspect_body(changed_body)['points'] > 0, 'No point witness for negative control')
    # Flip a low bit in the last point's fourth word and update the row pin.
    changed_body[-4] ^= 1
    altered = deepcopy(manifest)
    altered['attempts'][0]['geometry']['pin'] = pin(changed_body)
    changed = bodies | {'samples/01.bin': bytes(changed_body)}
    cases = {'altered_body_with_updated_pin': (altered, changed, 'Incorrect recorded classification')}

    wrong_domain = deepcopy(manifest)
    wrong_domain['body_domain'] = 'historical-D5AK-envelope-inclusive'
    cases['wrong_domain'] = (wrong_domain, bodies, 'geometry byte domain')
    wrong_envelope = deepcopy(manifest)
    frame_prefix = b'\x00' * 232  # Synthetic length witness, not original envelope bytes.
    wrapped = frame_prefix + bodies['references/mask3.bin']
    wrong_envelope['references']['mask3']['pin'] = pin(wrapped)
    cases['synthetic_envelope_prefix'] = (wrong_envelope,
        bodies | {'references/mask3.bin': wrapped}, 'Canonical body extent')
    missing = dict(bodies)
    del missing['samples/01.bin']
    cases['missing_sample'] = (manifest, missing, 'Missing, duplicated or misplaced body')
    duplicate = deepcopy(manifest)
    duplicate['attempts'][1]['capture_uuid'] = duplicate['attempts'][0]['capture_uuid']
    cases['duplicate_sample'] = (duplicate, bodies, 'Duplicate or noncanonical capture UUID')
    wrong_class = deepcopy(manifest)
    wrong_class['attempts'][0]['classification'] = MASK0
    cases['incorrect_classification'] = (wrong_class, bodies, 'Incorrect recorded classification')
    result = {}
    for name, (test_manifest, test_bodies, reason) in cases.items():
        try:
            verify(test_manifest, test_bodies)
        except ValueError as error:
            require(reason in str(error), f'Unexpected failure for {name}: {error}')
            result[name] = str(error)
        else:
            raise ValueError(f'Negative control unexpectedly passed: {name}')
    return result


def read_package(data):
    with ZipFile(BytesIO(data)) as archive:
        names = archive.namelist()
        require(len(names) == len(set(names)) == 33 and 'manifest.json' in names,
                'ZIP inventory differs')
        manifest = load_json(archive.read('manifest.json'))
        bodies = {name: archive.read(name) for name in names if name != 'manifest.json'}
    return manifest, bodies


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('package', type=Path)
    parser.add_argument('--sha256', required=True, help='Exact package pin from the evidence index')
    parser.add_argument('--negative-controls', action='store_true')
    args = parser.parse_args()
    try:
        data = args.package.read_bytes()
        require(sha(data) == args.sha256, 'Candidate package SHA-256 differs')
        manifest, bodies = read_package(data)
        result = verify(manifest, bodies)
        if args.negative_controls:
            result['negative_controls'] = negative_controls(manifest, bodies)
    except (OSError, ValueError, TypeError, KeyError, AttributeError, BadZipFile) as error:
        parser.exit(1, f'D5AS verification failed: {error}\n')
    result['package'] = pin(data)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
