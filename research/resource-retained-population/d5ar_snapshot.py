# SPDX-License-Identifier: GPL-3.0-or-later
"""Offline D5AR owned snapshot interchange and comparator, stdlib only.

Reads explicit JSON files, never processes or pointers. Writes exclusive local
results/synthetic snapshots only. Uses owned D5AI geometry normalization under
SOR-P-0002; native attribution remains an independent proof obligation. The CLI
enforces caller-available disk floors before input reads and output publication.
"""
import os
import sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):
    raise RuntimeError('Use pinned Python -E -B without optimization')

import argparse
import ctypes
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import struct
import uuid

from d5ad_baseline import guard
import d5ai_geometry as geometry

SCHEMA = 'sor-d5ar-resident-snapshot/1'
METHOD = 'sor-d5ar-offline/0.1.0'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def encoded(value):
    return json.dumps(value, ensure_ascii=True, allow_nan=False, sort_keys=True,
                      separators=(',', ':')).encode('ascii')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'Duplicate JSON field: ' + key)
        result[key] = value
    return result


def read_snapshot(path):
    guard()
    path = Path(path)
    require(path.suffix.casefold() != '.partial' and path.resolve().suffix.casefold() != '.partial',
            'Unpublished partial snapshot')
    raw = path.read_bytes()
    value = json.loads(raw, object_pairs_hook=unique_pairs,
                       parse_constant=lambda x: (_ for _ in ()).throw(ValueError('Nonfinite JSON: ' + x)))
    validate(value)
    return value, digest(raw)


def load(path):
    return read_snapshot(path)[0]


def exact_keys(value, keys):
    require(type(value) is dict and set(value) == set(keys.split()), 'Missing or unknown fields')


def identifier(value):
    require(type(value) is str and str(uuid.UUID(value)) == value, 'Canonical UUID required')


def sha_word(value):
    geometry.hexadecimal(value, 32)


def raw_geometry(payload):
    """Validate lossless raw arrays even when geographic/frame identity is unknown."""
    exact_keys(payload, 'schema session_id snapshot_id source frame capture population loss generation_quality')
    require(payload['schema'] == geometry.SCHEMA, 'Unsupported geometry schema')
    exact_keys(payload['capture'], 'complete status resource_slots region_total point_total')
    capture = payload['capture']
    require(capture['complete'] is True and capture['status'] == 'OK' and geometry.uint(payload['loss'], 64) == 0, 'Incomplete geometry')
    require(payload['generation_quality'] in ('UNKNOWN', 'KNOWN_PARTIAL', 'SOURCE_REPORTED_SUCCESS'), 'Unknown generation-quality code')
    require(type(payload['population']) is list and len(payload['population']) == geometry.uint(capture['resource_slots'], 32), 'Resource traversal incomplete')
    keys, regions, points = set(), 0, 0
    for resource in payload['population']:
        exact_keys(resource, 'resource regions')
        form = geometry.hexadecimal(resource['resource'], 4)
        require(form not in keys and type(resource['regions']) is list, 'Duplicate resource or invalid regions')
        keys.add(form)
        for region in resource['regions']:
            exact_keys(region, 'header count points')
            header = geometry.hexadecimal(region['header'], 24)
            count = geometry.uint(region['count'], 32)
            geometry.hexadecimal(region['points'], count * 16)
            require(struct.unpack_from('<I', header, 16)[0] == int(resource['resource'], 16), 'Header resource mismatch')
            regions += 1
            points += count
    require(regions == geometry.uint(capture['region_total'], 32) and points == geometry.uint(capture['point_total'], 32), 'Region/point traversal incomplete')
    if payload['source'] is not None:
        exact_keys(payload['source'], 'key body_formid')
        require(type(payload['source']['key']) is str and bool(payload['source']['key']), 'Missing source key')
        geometry.hexadecimal(payload['source']['body_formid'], 4)
    if payload['frame'] is not None:
        geometry.frame(payload['frame'])
    if (payload['source'] is not None and payload['frame'] is not None and
            payload['frame']['basis'] == 'consumed-descriptor-v1'):
        require(payload['source']['body_formid'] == payload['frame']['owner_formid'], 'Source/frame owner mismatch')


def validate(value):
    exact_keys(value, 'schema method capture_id session_id utc process build scope outpost sources status evidence_basis payload_sha256 capture_diagnostics owner_context')
    require(value['schema'] == SCHEMA and value['method'] == METHOD, 'Unsupported schema/method')
    identifier(value['capture_id'])
    identifier(value['session_id'])
    stamp = datetime.strptime(value['utc'], '%Y-%m-%dT%H:%M:%S.%fZ')
    require(stamp.strftime('%Y-%m-%dT%H:%M:%S.%fZ') == value['utc'], 'Six-digit UTC precision required')
    exact_keys(value['process'], 'pid creation_filetime')
    require(geometry.uint(value['process']['pid'], 32) > 0 and
            geometry.uint(value['process']['creation_filetime'], 64) > 0, 'Missing process identity')
    exact_keys(value['build'], 'game_exe_sha256 sfse_sha256 plugin_sha256 source_lock_sha256 game_version')
    for key in ('game_exe_sha256', 'sfse_sha256', 'plugin_sha256', 'source_lock_sha256'):
        sha_word(value['build'][key])
    require(value['build']['game_version'] == '1.16.244.0', 'Build outside current method scope')
    require(value['scope'] == 'RESIDENT_MAP_CENSUS_AREA_ASSOCIATION_UNKNOWN', 'Unproved area scope')
    require(value['evidence_basis'] in ('SYNTHETIC', 'UNQUALIFIED_NATIVE'), 'Native qualification unavailable in v1')
    require(value['status'] in ('COPIED_UNQUALIFIED', 'REFUSED'), 'Unsupported overall disposition')
    diagnostics = value['capture_diagnostics']
    exact_keys(diagnostics, 'copy_status copy_begin_filetime copy_end_filetime epoch_begin epoch_end lock_state required_bytes proc_identity_token')
    require(type(diagnostics['copy_status']) is str and bool(diagnostics['copy_status']), 'Missing native copy disposition')
    for key in ('copy_begin_filetime', 'copy_end_filetime', 'epoch_begin', 'epoch_end', 'lock_state', 'required_bytes'):
        geometry.uint(diagnostics[key], 64)
    require(diagnostics['proc_identity_token'] is None or type(diagnostics['proc_identity_token']) is str, 'Invalid owner diagnostic')
    require(value['status'] != 'COPIED_UNQUALIFIED' or diagnostics['copy_status'] == 'COPIED_UNQUALIFIED', 'Contradictory capture disposition')
    exact_keys(value['outpost'], 'status reference area_context')
    require(value['outpost']['status'] in ('UNKNOWN', 'ABSENT_UNPROVEN', 'AMBIGUOUS', 'SOURCE_REPORTED', 'ACTIVE_ESTABLISHED_OPERATION_REFERENCE'), 'Unsupported outpost certificate')
    require(value['outpost']['reference'] is None or type(value['outpost']['reference']) is str, 'Invalid diagnostic reference')
    require(type(value['outpost']['area_context']) is dict, 'Area diagnostics required')
    exact_keys(value['owner_context'], 'before after')
    for binding in value['owner_context'].values():
        exact_keys(binding, 'status complete manager_pointer_token attached_proc_token owner_formid_word mode current_descriptor_bytes')
        require(binding['status'] in ('NOT_CAPTURED', 'NO_MANAGER', 'READ_FAILED', 'READ_EXCEPTION', 'OBSERVED_UNQUALIFIED'), 'Unknown owner diagnostic')
        require(type(binding['complete']) is bool and binding['complete'] == (binding['status'] == 'OBSERVED_UNQUALIFIED'), 'Owner diagnostic completeness mismatch')
        if binding['complete']:
            require(type(binding['manager_pointer_token']) is str and type(binding['attached_proc_token']) is str, 'Missing owner pointer diagnostics')
            geometry.hexadecimal(binding['owner_formid_word'], 4)
            geometry.hexadecimal(binding['current_descriptor_bytes'], 44)
            geometry.uint(binding['mode'], 8)
        else:
            require(all(binding[k] is None for k in ('manager_pointer_token', 'attached_proc_token', 'owner_formid_word', 'mode', 'current_descriptor_bytes')), 'Partial owner diagnostic cannot imply complete context')
    require(type(value['sources']) is list, 'Source list required')
    allocations, entries = set(), set()
    for source in value['sources']:
        exact_keys(source, 'allocation_id map_entry_id holder_id owning_grid source_disposition area_association geometry geometry_sha256 source_diagnostics')
        diagnostic = source['source_diagnostics']
        exact_keys(diagnostic, 'status semantic_bytes visited_token origin_status origin_input_words descriptor_status source_descriptor_bytes')
        lifetime_refusals = ('SOURCE_LIFETIME_RETIRED', 'SOURCE_RECORDER_UNAVAILABLE')
        statuses = tuple(diagnostic[k] for k in ('status', 'origin_status', 'descriptor_status'))
        if any(status in lifetime_refusals for status in statuses):
            require(len(set(statuses)) == 1, 'Source lifetime refusal must cover every diagnostic group')
        require(diagnostic['descriptor_status'] in ('NOT_CAPTURED', 'READ_FAILED', 'SOURCE_DESCRIPTOR_UNQUALIFIED') + lifetime_refusals, 'Unknown source descriptor diagnostic')
        if diagnostic['descriptor_status'] == 'SOURCE_DESCRIPTOR_UNQUALIFIED':
            geometry.hexadecimal(diagnostic['source_descriptor_bytes'], 44)
        else:
            require(diagnostic['source_descriptor_bytes'] is None, 'Partial source descriptor cannot imply complete bytes')
        require(diagnostic['origin_status'] in ('NOT_CAPTURED', 'READ_FAILED', 'SOURCE_ORIGIN_WORDS_UNQUALIFIED') + lifetime_refusals, 'Unknown source-origin diagnostic')
        if diagnostic['origin_status'] == 'SOURCE_ORIGIN_WORDS_UNQUALIFIED':
            geometry.hexadecimal(diagnostic['origin_input_words'], 16)
        else:
            require(diagnostic['origin_input_words'] is None, 'Partial origin payload cannot imply complete words')
        require(diagnostic['status'] in ('NOT_CAPTURED', 'READ_FAILED', 'SOURCE_BYTES_UNQUALIFIED') + lifetime_refusals, 'Unknown source diagnostic')
        if diagnostic['status'] == 'SOURCE_BYTES_UNQUALIFIED':
            geometry.hexadecimal(diagnostic['semantic_bytes'], 29)
            geometry.uint(diagnostic['visited_token'], 64)
        else:
            require(diagnostic['semantic_bytes'] is None and diagnostic['visited_token'] is None, 'Unqualified partial scalar payload')
        require(source['source_disposition'] in ('IDENTIFIED', 'ALLOCATION_UNKNOWN', 'EMPTY', 'MALFORMED', 'COPY_FAILED'), 'Unknown source disposition')
        require(source['area_association'] == 'UNKNOWN', 'Area relation not established')
        for name in ('allocation_id', 'map_entry_id', 'holder_id', 'owning_grid'):
            require(source[name] is None or (type(source[name]) is str and bool(source[name])), 'Invalid identity domain')
        require(source['map_entry_id'] is not None and source['map_entry_id'] not in entries, 'Missing/duplicate map entry')
        entries.add(source['map_entry_id'])
        if source['allocation_id'] is not None:
            require(source['allocation_id'] not in allocations, 'Duplicate source allocation')
            allocations.add(source['allocation_id'])
        payload = source['geometry']
        if payload is None:
            require(source['geometry_sha256'] is None and source['source_disposition'] != 'IDENTIFIED', 'Missing identified geometry')
        else:
            require(source['source_disposition'] in ('IDENTIFIED', 'ALLOCATION_UNKNOWN'), 'Failed or empty holder cannot carry comparable geometry')
            raw_geometry(payload)
            if source['source_disposition'] == 'ALLOCATION_UNKNOWN':
                require(payload['source'] is None, 'Unknown allocation cannot certify geographic source')
            require(payload['session_id'] == value['session_id'] and payload['snapshot_id'] == value['capture_id'], 'Geometry observation binding')
            require(source['geometry_sha256'] == digest(encoded(payload)), 'Raw geometry hash mismatch')
    require(value['payload_sha256'] == digest(encoded({k: v for k, v in value.items() if k != 'payload_sha256'})), 'Snapshot hash mismatch')
    return value


def seal(value):
    value['payload_sha256'] = digest(encoded({k: v for k, v in value.items() if k != 'payload_sha256'}))
    return validate(value)


def publish(value, directory):
    """Flush a fresh exclusive partial file, then publish without replacement.

    Windows MoveFileExW uses WRITE_THROUGH and omits REPLACE_EXISTING. Failure
    leaves the .partial artifact. No deletion, recycling or disk-quota truncation.
    The directory must already exist and contain no reparse ancestors.
    """
    guard()
    validate(value)
    original_path = Path(directory).absolute()
    root = Path(directory).resolve()
    require(root.is_dir() and not any(p.is_symlink() or p.is_junction() for p in (original_path, *original_path.parents, root, *root.parents)), 'Existing plain output directory required')
    basename = value['utc'].replace('-', '').replace(':', '') + '_' + value['session_id'] + '_' + value['capture_id']
    final = root / (basename + '.snapshot.json')
    partial = root / (basename + '.partial')
    require(not final.exists(), 'Snapshot already finalized')
    data = encoded(value) + b'\n'
    with partial.open('xb') as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    require(partial.read_bytes() == data, 'Partial verification failed')
    guard()
    kernel = ctypes.WinDLL('kernel32', use_last_error=True)
    move = kernel.MoveFileExW
    move.argtypes = [ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_uint32]
    move.restype = ctypes.c_int
    if not move(str(partial), str(final), 0x8):
        raise ctypes.WinError(ctypes.get_last_error())
    return final


def first_field_difference(left, right):
    """Locate a semantic difference by resource, region and ordered point word."""
    a = {r['resource']: r for r in left['population']}
    b = {r['resource']: r for r in right['population']}
    for form in sorted(a.keys() | b.keys()):
        if form not in a or form not in b:
            return dict(resource=form, field='resource_presence')
        x, y = a[form]['regions'], b[form]['regions']
        if len(x) != len(y):
            return dict(resource=form, field='region_count', left=len(x), right=len(y))
        for index, (u, v) in enumerate(zip(x, y)):
            if u['header'][:42] != v['header'][:42]:
                return dict(resource=form, region=index, field='semantic_header', left=u['header'][:42], right=v['header'][:42])
            if u['count'] != v['count']:
                return dict(resource=form, region=index, field='point_count', left=u['count'], right=v['count'])
            for word in range(u['count'] * 4):
                p, q = u['points'][word * 8:word * 8 + 8], v['points'][word * 8:word * 8 + 8]
                if p != q:
                    return dict(resource=form, region=index, point=word // 4, word=word % 4, field='ordered_point_word', left=p, right=q)
    return None


def candidate_source_key(diagnostic):
    """Decode a diagnostic candidate, never an allocation/frame certificate.

    Owned read_capture.py supplies geographic key arithmetic under SOR-P-0002.
    Each original signed source word remains independently preserved in raw data.
    """
    if diagnostic['status'] != 'SOURCE_BYTES_UNQUALIFIED':
        return None
    raw = geometry.hexadecimal(diagnostic['semantic_bytes'], 29)
    terrain = struct.unpack_from('<I', raw)[0]
    chart = raw[4]
    a, b, c, d, e, f = struct.unpack_from('<6i', raw, 5)
    return f'{chart}:{a * 192 + c * 12 + e}:{b * 192 + d * 12 + f}:{terrain:08x}'


def feynman_diagnostic(value):
    """Offline target selection only; no producer target or mask inference."""
    validate(value)
    target = '0:37536:20928:0029d20e'
    matches = []
    unobserved = []
    for source in value['sources']:
        candidate = candidate_source_key(source['source_diagnostics'])
        if candidate is None:
            unobserved.append(source['map_entry_id'])
        if candidate == target:
            payload = source['geometry']
            matches.append(dict(map_entry_id=source['map_entry_id'], candidate_key=candidate,
                                source_disposition=source['source_disposition'],
                                represented_counts=payload['capture'] if payload is not None else None,
                                raw_geometry_sha256=source['geometry_sha256']))
    return dict(schema='sor-d5ar-feynman-diagnostic/1', status='UNAVAILABLE/INCONCLUSIVE',
                target_candidate=target, candidate_matches=matches, unreadable_source_entries=unobserved,
                source_frame_outpost_qualification='NOT_ESTABLISHED', sampled_mask='UNKNOWN',
                absence_of_geographical_resources='NOT_ESTABLISHED',
                reason='Raw source candidates select diagnostics only; v1 has no authenticated native source/frame/outpost certificate')


def compare(left, right):
    """Compare exact normalized geometry after source/frame identity checks.

    Result describes represented bytes only; all v1 evidence is unqualified for
    retail inference. Mismatched contexts remain incomparable, never novel masks.
    """
    validate(left)
    validate(right)
    require(left['capture_id'] != right['capture_id'], 'Duplicate capture identity')
    rows = []
    def identified(source):
        return source['geometry'] is not None and source['geometry']['source'] is not None
    a = {s['geometry']['source']['key']: s for s in left['sources'] if identified(s)}
    b = {s['geometry']['source']['key']: s for s in right['sources'] if identified(s)}
    require(len(a) == sum(identified(s) for s in left['sources']) and
            len(b) == sum(identified(s) for s in right['sources']), 'Ambiguous geographic source')
    for key in sorted(a.keys() | b.keys()):
        status, first_difference, field_difference = 'UNAVAILABLE_INCOMPARABLE', None, None
        if key in a and key in b:
            x, y = a[key]['geometry'], b[key]['geometry']
            if (left['status'] == right['status'] == 'COPIED_UNQUALIFIED' and
                    x['frame'] is not None and y['frame'] is not None and
                    x['source'] == y['source'] and x['frame'] == y['frame'] and left['build'] == right['build']):
                try:
                    raw_x, raw_y = geometry.normalize(x), geometry.normalize(y)
                except ValueError:
                    status = 'RAW_GEOMETRY_NOT_COMPARABLE'
                else:
                    status = 'EQUAL_REPRESENTED_BYTES' if raw_x == raw_y else 'DIFFERENT_REPRESENTED_BYTES'
                    first_difference = next((i for i, (u, v) in enumerate(zip(raw_x, raw_y)) if u != v),
                                            min(len(raw_x), len(raw_y)) if len(raw_x) != len(raw_y) else None)
                    field_difference = first_field_difference(x, y)
        rows.append(dict(source_key=key, status=status, first_normalized_byte_difference=first_difference,
                         first_semantic_field_difference=field_difference))
    for side, value in (('left', left), ('right', right)):
        for source in value['sources']:
            if not identified(source):
                rows.append(dict(source_key=None, side=side, map_entry_id=source['map_entry_id'],
                                 source_disposition=source['source_disposition'], status='UNAVAILABLE_INCOMPARABLE',
                                 first_normalized_byte_difference=None, first_semantic_field_difference=None))
    return dict(schema='sor-d5ar-comparison/1', qualification='UNQUALIFIED_NO_NATIVE_CERTIFICATE',
                historical_mask='UNKNOWN', sources=rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('left', type=Path)
    parser.add_argument('right', type=Path, nargs='?')
    parser.add_argument('--out', required=True, type=Path)
    parser.add_argument('--feynman', action='store_true', help='Offline candidate-source diagnostic only')
    args = parser.parse_args()
    left, left_hash = read_snapshot(args.left)
    inputs = {str(args.left): left_hash}
    require(not args.feynman or args.right is None, 'Feynman diagnostic takes one snapshot')
    if args.right:
        right, right_hash = read_snapshot(args.right)
        inputs[str(args.right)] = right_hash
        result = compare(left, right)
    elif args.feynman:
        result = feynman_diagnostic(left)
    else:
        result = dict(schema=SCHEMA, status='REPRESENTATION_VALID_UNQUALIFIED', capture_id=left['capture_id'],
                      capture_status=left['status'], copy_status=left['capture_diagnostics']['copy_status'],
                      outpost_status=left['outpost']['status'], represented_entries=len(left['sources']))
    result['input_sha256'] = inputs
    result['decoder_sha256'] = digest(Path(__file__).read_bytes())
    guard()
    with args.out.open('xb') as stream:
        stream.write(encoded(result) + b'\n')


if __name__ == '__main__':
    main()
