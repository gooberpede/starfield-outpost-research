# SPDX-License-Identifier: GPL-3.0-or-later
"""Authenticate and decode the complete D5AI native sidecar representation.

Reads only supplied local session bytes and their identity-bound flush receipts.
Writes a new JSON output only when requested. Stdlib only; no process, save,
network, deployment or analysis-project operation. A valid raw representation
does not prove native generation success, source lifetime or retail semantics.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import struct

HEADER = struct.Struct('<22Q24sII9Q44sI16Q')
HOLDER = struct.Struct('<4Q2I')
RESOURCE = struct.Struct('<II4Q')
REGION = struct.Struct('<24s4Q')
MARK = ('cursor ticks generation_before generation_after active_before active_after loss failed').split()
NAMES = ('magic version request snapshot proc epoch hazards loss ticks_begin ticks_end status '
         'map_capacity holders resources regions points payload_bytes lock_owner lock_state '
         'thread boundary consumer').split()
TAIL = ('completion_ticks completion_epoch completion_hazards iterator scan_capacity '
        'scan_result manager mode owner_formid').split()
STATUS = ('OK', 'READ_FAULT', 'MALFORMED', 'ARENA_FULL', 'INTERRUPTED',
          'EXCLUSIVE_RECURSION', 'CONSUMER_UNFINISHED', 'CONSUMER_PARTIAL')


def sha(data):
    return hashlib.sha256(data).hexdigest()


def loads_unique(data):
    def object_pairs(pairs):
        value = {}
        for key, item in pairs:
            if key in value:
                raise ValueError('Duplicate JSON key: ' + key)
            value[key] = item
        return value
    return json.loads(data, object_pairs_hook=object_pairs)


def regular_bytes(path):
    path = Path(path)
    if path.is_symlink() or path.is_junction() or not path.is_file():
        raise ValueError('Nonregular session evidence file: ' + path.name)
    return path.read_bytes()


def decode(data):
    """Decode one native file; reject a false complete census or malformed frame."""
    if len(data) < HEADER.size:
        raise ValueError('Truncated native header')
    fields = HEADER.unpack_from(data)
    h = dict(zip(NAMES, fields[:22]))
    h.update(query_hex=fields[22].hex(), radius_bits=fields[23], upper_bits=fields[24])
    h.update(zip(TAIL, fields[25:34]))
    h['descriptor_hex'] = fields[34].hex()
    h['preunlock_seen'] = fields[35]
    h['lifetime_start'] = dict(zip(MARK, fields[36:44]))
    h['lifetime_end'] = dict(zip(MARK, fields[44:52]))
    if h['magic'] != 0x3149413544524f53 or h['version'] != 2:
        raise ValueError('Unsupported native header')
    if h['status'] >= len(STATUS) or h['payload_bytes'] != len(data) - HEADER.size:
        raise ValueError('Native size or status mismatch')
    if h['holders'] > h['map_capacity']:
        raise ValueError('Holder census exceeds native map capacity')
    if not h['request'] or not h['snapshot'] or h['ticks_end'] < h['ticks_begin']:
        raise ValueError('Invalid native identity or clock')
    h['status_name'] = STATUS[h['status']]
    position = HEADER.size
    observed = dict(resources=0, regions=0, points=0)

    def take(codec):
        nonlocal position
        if codec.size > len(data) - position:
            raise ValueError('Truncated nested record')
        result = codec.unpack_from(data, position)
        position += codec.size
        return result

    def population():
        nonlocal position
        holders, keys = [], set()
        if h['holders'] > (len(data) - position) // HOLDER.size:
            raise ValueError('Impossible holder census')
        for _ in range(h['holders']):
            source, holder, capacity, count, a, b = take(HOLDER)
            if source in keys or not source or not holder or count > capacity:
                raise ValueError('Invalid holder identity or census')
            keys.add(source)
            current = dict(source_pointer=source, holder_pointer=holder,
                           resource_capacity=capacity, opaque_holder_words=[a, b], resources=[])
            forms = set()
            if count > (len(data) - position) // RESOURCE.size:
                raise ValueError('Impossible resource census')
            for _ in range(count):
                form, reserved, collection, regions, region_capacity, region_data = take(RESOURCE)
                if (reserved or form in forms or not collection or regions > region_capacity or
                        region_capacity > 0xffffffff or (region_capacity and region_data < 0x10000)):
                    raise ValueError('Invalid resource identity')
                forms.add(form)
                resource = dict(resource=f'{form:08x}', collection_pointer=collection, regions=[],
                                region_capacity=region_capacity, region_data=region_data, region_storage=[])
                if regions > (len(data) - position) // REGION.size:
                    raise ValueError('Impossible region census')
                for _ in range(regions):
                    header, count_points, point_capacity, point_data, region_address = take(REGION)
                    if (count_points > point_capacity or point_capacity > 0xffffffff or
                            (point_capacity and point_data < 0x10000) or
                            region_address != region_data + len(resource['regions']) * 48):
                        raise ValueError('Invalid nested allocation shape')
                    size = count_points * 16
                    if size > len(data) - position:
                        raise ValueError('Truncated point array')
                    points = data[position:position + size]
                    position += size
                    resource['regions'].append(dict(header=header.hex(), count=count_points,
                                                    points=points.hex()))
                    resource['region_storage'].append(dict(region_address=region_address,
                                                           point_capacity=point_capacity, point_data=point_data))
                    observed['points'] += count_points
                    observed['regions'] += 1
                current['resources'].append(resource)
                observed['resources'] += 1
            holders.append(current)
        if position != len(data) or any(h[k] != n for k, n in observed.items()):
            raise ValueError('Nested geometry census mismatch')
        return holders

    result = dict(header=h, holders=[], complete_representation=False, native_quality='UNKNOWN')
    try:
        result['holders'] = population()
    except ValueError as error:
        if h['status'] == 0:
            raise
        result['partial_decode_error'] = str(error)
    if h['status'] == 0:
        if (h['hazards'] or h['completion_hazards'] or h['completion_epoch'] != h['epoch'] or
                h['completion_ticks'] < h['ticks_end'] or h['iterator'] != h['scan_capacity'] or
                h['scan_capacity'] != h['map_capacity'] or h['scan_result'] != 1 or h['preunlock_seen'] != 1 or
                h['lock_state'] & 0xffc00000 or h['lock_owner'] == h['thread'] or
                h['boundary'] != 2 or not h['manager']):
            raise ValueError('False complete consumer boundary')
        result['complete_representation'] = True
    return result


def read_session(session):
    """Preserve valid snapshots and report missing/unflushed files independently."""
    session = Path(session).absolute()
    for p in (session, *session.parents):
        if p.is_symlink() or p.is_junction():
            raise ValueError('Reparse session path')
    if session.resolve() != session:
        raise ValueError('Noncanonical session path')
    identity = regular_bytes(session / 'identity.json')
    identity_hash = sha(identity)
    identity_value = loads_unique(identity)
    if identity_value.get('schema') != 'sor-d5x/4':
        raise ValueError('Unsupported lifecycle identity')
    if (identity_value.get('geometry_schema') != 'sor-d5ai-raw/2' or
            identity_value.get('geometry_header_bytes') != 456 or
            len(identity_value.get('geometry_sites', [])) != 3 or
            identity_value.get('context_schema') != 'sor-d5ai-context/1' or
            len(identity_value.get('context_sites', [])) != 2):
        raise ValueError('Complete geometry and whole-context metadata required')
    geometry = identity_value['geometry_sites']
    context = identity_value['context_sites']
    if ([s.get('bytes') for s in geometry] != [5, 5, 9] or
            [s.get('reason') for s in context] != [5, 6] or
            [s.get('bytes') for s in context] != [5, 5] or
            len({s.get('va') for s in geometry + context}) != 5):
        raise ValueError('Missing, duplicate or reordered native observation site')
    result = dict(schema='sor-d5ai-reader/2', identity_sha256=identity_hash,
                  lifecycle_identity=identity_value, snapshots=[], errors=[])
    paths = {p for p in session.iterdir() if re.fullmatch(r'geometry-[1-9][0-9]*\.(bin|json)', p.name)}
    ids = set()
    for stem in sorted({p.stem for p in paths}):
        try:
            raw_path, receipt_path = (session / (stem + suffix) for suffix in ('.bin', '.json'))
            data = regular_bytes(raw_path)
            receipt_bytes = regular_bytes(receipt_path)
            receipt = loads_unique(receipt_bytes)
            if (receipt.get('schema') != 'sor-d5ai-raw/2' or receipt.get('identity_sha256') != identity_hash or
                    receipt.get('sha256') != sha(data) or receipt.get('bytes') != len(data) or
                    receipt.get('flushed') is not True or receipt.get('native_quality') != 'UNKNOWN'):
                raise ValueError('Unqualified native flush receipt')
            snapshot = decode(data)
            h = snapshot['header']
            if (receipt.get('snapshot_id') != h['snapshot'] or receipt.get('request_id') != h['request'] or
                    receipt.get('capture_status') != h['status'] or stem != f"geometry-{h['snapshot']}" or
                    h['snapshot'] in ids):
                raise ValueError('Snapshot identity mismatch')
            ids.add(h['snapshot'])
            snapshot.update(path=str(raw_path), sha256=sha(data), receipt_sha256=sha(receipt_bytes))
            result['snapshots'].append(snapshot)
        except (ValueError, OSError, struct.error, KeyError, TypeError) as error:
            result['errors'].append(dict(stem=stem, error=str(error)))
    result['snapshots'].sort(key=lambda s: s['header']['snapshot'])
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('session', type=Path)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    result = read_session(args.session)
    with args.out.open('x', encoding='utf8', newline='\n') as stream:
        stream.write(json.dumps(result, indent=2) + '\n')
    return 1 if result['errors'] else 0


if __name__ == '__main__':
    raise SystemExit(main())
