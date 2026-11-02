# SPDX-License-Identifier: GPL-3.0-or-later
"""Validate and compare complete owned geometry snapshots, without target access.

Reads explicit JSON files; writes one exclusive JSON result. Stdlib only.
No process, native pointer, save, database, network or Git operations. The caller
must independently establish the capture and lifetime certificates. These checks
validate representation and refuse uncertainty; they do not prove native coverage.
Region layout follows the pinned evidence in `d5ai-sources.csv`.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import struct

SCHEMA = 'sor-d5ai-geometry/1'


def uint(value, bits):
    if type(value) is not int or not 0 <= value < 2 ** bits:
        raise ValueError('Invalid unsigned integer')
    return value


def hexadecimal(value, size):
    if not isinstance(value, str) or not re.fullmatch('[0-9a-f]{' + str(size * 2) + '}', value):
        raise ValueError('Noncanonical or incomplete hexadecimal bytes')
    return bytes.fromhex(value)


def finite(data):
    if not all(math.isfinite(x) for x in struct.unpack('<' + 'f' * (len(data) // 4), data)):
        raise ValueError('Nonfinite geometry; preserve raw, refuse comparison')


def frame(value):
    if not isinstance(value, dict):
        raise ValueError('Frame must be an object')
    if value.get('basis') == 'consumed-descriptor-v1':
        if set(value) != {'basis', 'owner_formid', 'descriptor_semantic'}:
            raise ValueError('Incomplete native descriptor frame')
        hexadecimal(value['owner_formid'], 4)
        descriptor = hexadecimal(value['descriptor_semantic'], 41)
        if descriptor[0] != 0:
            raise ValueError('Native chart/seam not qualified')
        return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()
    required = {'anchor_i32', 'origin_i32', 'clip_center_f32', 'clip_half_f32', 'basis'}
    if set(value) != required or value['basis'] != 'source-planar':
        raise ValueError('Unsupported or incomplete frame')
    for name in ('anchor_i32', 'origin_i32'):
        if len(value[name]) != 2 or any(type(x) is not int or not -(2 ** 31) <= x < 2 ** 31 for x in value[name]):
            raise ValueError('Invalid frame coordinate')
    for name in ('clip_center_f32', 'clip_half_f32'):
        if len(value[name]) != 4:
            raise ValueError('Incomplete frame scalars')
        for word in value[name]:
            finite(hexadecimal(word, 4))
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def normalize(snapshot):
    """Sort unique resource keys; preserve region/point order and exact floats."""
    if snapshot['schema'] != SCHEMA:
        raise ValueError('Unsupported geometry schema')
    for field in ('snapshot_id', 'session_id'):
        if not isinstance(snapshot[field], str) or not snapshot[field]:
            raise ValueError('Missing observation identity')
    capture = snapshot['capture']
    if capture['complete'] is not True or capture['status'] != 'OK':
        raise ValueError('Incomplete, failed or interrupted snapshot')
    if uint(snapshot['loss'], 64) != 0:
        raise ValueError('Loss-contaminated observation')
    source = snapshot['source']
    if set(source) != {'key', 'body_formid'} or not isinstance(source['key'], str) or not source['key']:
        raise ValueError('Incomplete source identity')
    hexadecimal(source['body_formid'], 4)
    prefix = json.dumps(source, sort_keys=True, separators=(',', ':')).encode()
    if snapshot['frame'] is None:
        availability = available(snapshot)
        if availability['holder_present'] or availability['exposed'] or snapshot['population']:
            raise ValueError('Missing frame for represented geometry')
        framed = b'NO_RESIDENT_GEOMETRY'
    else:
        framed = frame(snapshot['frame'])
    if (snapshot['frame'] is not None and snapshot['frame']['basis'] == 'consumed-descriptor-v1' and
            snapshot['frame']['owner_formid'] != source['body_formid']):
        raise ValueError('Source owner and frame owner disagree')
    result = bytearray(struct.pack('<I', len(prefix)) + prefix + struct.pack('<I', len(framed)) + framed)
    resources = snapshot['population']
    if not isinstance(resources, list) or len(resources) != uint(capture['resource_slots'], 32):
        raise ValueError('Resource traversal incomplete')
    result += struct.pack('<I', len(resources))
    keys, regions, points = set(), 0, 0
    for resource in sorted(resources, key=lambda r: int(r['resource'], 16)):
        if set(resource) != {'resource', 'regions'}:
            raise ValueError('Unknown resource fields require a schema revision')
        key = hexadecimal(resource['resource'], 4)
        if key in keys:
            raise ValueError('Duplicate resource map key')
        keys.add(key)
        represented = resource['regions']
        if not isinstance(represented, list):
            raise ValueError('Invalid region array')
        result += key + struct.pack('<I', len(represented))
        for region in represented:
            if set(region) != {'header', 'count', 'points'}:
                raise ValueError('Unknown region fields require a schema revision')
            header = hexadecimal(region['header'], 24)
            count = uint(region['count'], 32)
            data = hexadecimal(region['points'], count * 16)
            finite(header[:16])
            finite(data)
            if struct.unpack_from('<I', header, 16)[0] != int(resource['resource'], 16):
                raise ValueError('Region FormID differs from resource key')
            # Native copy initializes 21 header bytes; three trailing padding
            # bytes are retained in raw input but excluded from semantic equality.
            result += header[:21] + struct.pack('<I', count) + data
            regions += 1
            points += count
    if regions != uint(capture['region_total'], 32) or points != uint(capture['point_total'], 32):
        raise ValueError('Region/point traversal incomplete')
    return bytes(result)


def available(snapshot):
    value = snapshot['availability']
    if value['boundary_qualified'] is not True or value['map_scan_complete'] is not True:
        raise ValueError('No qualified consumer availability observation')
    if type(value['holder_present']) is not bool or type(value['exposed']) is not bool:
        raise ValueError('Invalid availability predicates')
    if value['exposed'] and not value['holder_present']:
        raise ValueError('Exposure without represented holder')
    if not value['holder_present'] and snapshot['population']:
        raise ValueError('Absent holder contradicts population')
    return value


def compare(before, after, lineage):
    """Classify only with independent qualified availability and lifetime input."""
    try:
        a, b = normalize(before), normalize(after)
        av, bv = available(before), available(after)
        if before['source'] != after['source']:
            raise ValueError('Source comparison contract differs')
        if not av['exposed']:
            raise ValueError('Baseline not exposed to qualified consumer')
        if not bv['exposed']:
            return dict(outcome='UNAVAILABLE', reason='Qualified consumer boundary reports no exposure',
                        holder_present=bv['holder_present'], content_equal=None,
                        prior_storage=lineage.get('prior_storage', dict(qualified=False, state='UNKNOWN')))
        if frame(before['frame']) != frame(after['frame']):
            raise ValueError('Frame comparison contract differs')
        equal = a == b
        if lineage['qualified'] is not True or uint(lineage['loss'], 64) != 0:
            raise ValueError('Unqualified lifetime history')
        if lineage['before'] != [before['session_id'], before['snapshot_id']] or lineage['after'] != [after['session_id'], after['snapshot_id']]:
            raise ValueError('Lifetime certificate belongs to other observations')
        relation = lineage['relation']
        if relation == 'CONTINUOUS':
            if before['session_id'] != after['session_id']:
                raise ValueError('Continuous lifetime cannot cross processes/sessions')
            if not equal:
                raise ValueError('Content mutation during claimed retained lifetime')
            outcome = 'RETAINED'
        elif relation == 'RECONSTRUCTED':
            outcome = 'REBUILT_IDENTICAL' if equal else 'REBUILT_DIFFERENT'
        else:
            raise ValueError('Missing positive lifetime relation')
        return dict(outcome=outcome, content_equal=equal,
                    prior_storage=lineage.get('prior_storage', dict(qualified=False, state='UNKNOWN')),
                    before_normalized_sha256=hashlib.sha256(a).hexdigest(),
                    after_normalized_sha256=hashlib.sha256(b).hexdigest(),
                    equality_method='Complete normalized byte comparison')
    except (ValueError, KeyError, TypeError, struct.error, OverflowError) as error:
        return dict(outcome='INCONCLUSIVE', reason=str(error), content_equal=None)


def load(path):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError('Duplicate JSON key')
            result[key] = value
        return result
    return json.loads(Path(path).read_bytes(), object_pairs_hook=unique,
                      parse_constant=lambda x: (_ for _ in ()).throw(ValueError('Nonfinite JSON')))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('before', type=Path)
    parser.add_argument('after', type=Path)
    parser.add_argument('lineage', type=Path)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    result = compare(load(args.before), load(args.after), load(args.lineage))
    result['inputs'] = {str(p): hashlib.sha256(p.read_bytes()).hexdigest()
                        for p in (args.before, args.after, args.lineage)}
    result['method_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    with args.out.open('x', encoding='utf8', newline='\n') as stream:
        stream.write(json.dumps(result, indent=2) + '\n')
    print(result['outcome'])


if __name__ == '__main__':
    main()
