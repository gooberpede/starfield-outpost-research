# SPDX-License-Identifier: GPL-3.0-or-later
"""Separate D5AR source-planar derivation and exact offline classification.

Reads explicit snapshots and authenticated existing A0/fixed-native references.
Writes one exclusive JSON; no process, save, database, configuration or network
access. Uses project-owned D5AL authentication under SOR-P-0002. This new contract
does not change the frozen raw decoder or historical D5AI normalization. Native
admission requires the exact independently reviewed producer profile below;
checksums are integrity checks, not signatures or proof against fabricated data.
"""
import os
import sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):
    raise RuntimeError('Use pinned Python -E -B without optimization')

import argparse
import csv
import json
import math
from pathlib import Path
import re
import struct
import zlib

import d5ar_snapshot as raw
from d5ad_baseline import ROOT, guard, sha
import d5al_baseline as baseline

METHOD = 'sor-d5ar-source-planar/1'
EXE = '7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28'
SFSE = '28c5bda41d9959c885efcb6e889de69e92767c80a1a66842d711d215f722f82b'
TARGET = '0:37536:20928:0029d20e'
MODEL_SHA = '9594ab2aa34856bcc3b8ecb249b46b0063ef4b5d1af80d4e557542f2d6657ccf'
REFERENCE_LEDGER_SHA = '2c20c721936a45d23c83ae335a8d6c3bc2be7b75dacb0501a5e0c625bd6b8d61'
# Candidate profile remains REVIEW-REQUIRED until exact independent review.
# Both owner/map admission and synchronized source-ending history are required.
NATIVE_BUILD = dict(game_version='1.16.244.0', game_exe_sha256=EXE, sfse_sha256=SFSE,
                    plugin_sha256='8fadade8fde699238af1eadd06065b4dd92f161471499cf03961166639270fe0',
                    source_lock_sha256='1470a6368cec252ae5ac8d3a8bcb8f2291249177a8fd4d53e6145dc0d47bf1f5')
FIXTURE_BUILD = dict(game_version='1.16.244.0', game_exe_sha256=EXE,
                     sfse_sha256='1' * 64, plugin_sha256='2' * 64,
                     source_lock_sha256='9' * 64)


def pointer(value, prefix):
    raw.require(type(value) is str and re.fullmatch(re.escape(prefix) + r'[1-9][0-9]*', value),
                'Missing canonical pointer diagnostic')
    result = int(value[len(prefix):])
    raw.require(0x10000 <= result <= 0xffffffffffffffff, 'Pointer outside method domain')
    return result


def native_origin(words):
    """Model original signed dword arithmetic only where f32 conversion is exact.

    This avoids inventing an unobserved MXCSR rounding mode for large inputs.
    Refused basis operands remain losslessly available in the raw snapshot.
    """
    values = struct.unpack('<4i', bytes.fromhex(words))
    def i32(value):
        return (value + 2 ** 31) % 2 ** 32 - 2 ** 31
    result = []
    for a, b in ((values[0], values[2]), (values[1], values[3])):
        product = i32(i32(a - b) * 100)
        represented = struct.unpack('<f', struct.pack('<f', product))[0]
        raw.require(represented == product and -2 ** 31 <= represented < 2 ** 31,
                    'Origin needs an unobserved floating-point environment')
        result.append(product)
    return result


def frame_record(diagnostic, body):
    raw.require(diagnostic['status'] == 'SOURCE_BYTES_UNQUALIFIED' and
                diagnostic['origin_status'] == 'SOURCE_ORIGIN_WORDS_UNQUALIFIED' and
                diagnostic['descriptor_status'] == 'SOURCE_DESCRIPTOR_UNQUALIFIED',
                'Required source diagnostic unavailable')
    selected = bytes.fromhex(diagnostic['semantic_bytes'])
    descriptor = bytes.fromhex(diagnostic['source_descriptor_bytes'])
    projection = selected[:4] + descriptor[:1] + descriptor[4:12] + descriptor[20:28] + descriptor[36:44]
    raw.require(selected == projection, 'Geography and full descriptor disagree')
    return dict(basis='native-source-planar-v1', game_exe_sha256=EXE,
                geographic_key=raw.candidate_source_key(diagnostic), body_formid=body,
                terrain_formid=f'{int.from_bytes(selected[:4], "little"):08x}',
                descriptor_semantic41=(descriptor[:1] + descriptor[4:]).hex(),
                origin_input_words16=diagnostic['origin_input_words'],
                native_origin_i32=native_origin(diagnostic['origin_input_words']))


def body_bytes(population):
    """Complete ordered represented content, excluding only proved header padding."""
    pieces = [struct.pack('<I', len(population))]
    forms = set()
    for resource in sorted(population, key=lambda row: int(row['resource'], 16)):
        form = raw.geometry.hexadecimal(resource['resource'], 4)
        raw.require(form not in forms, 'Duplicate resource')
        forms.add(form)
        pieces.extend((form, struct.pack('<I', len(resource['regions']))))
        for region in resource['regions']:
            header = raw.geometry.hexadecimal(region['header'], 24)
            count = raw.geometry.uint(region['count'], 32)
            points = raw.geometry.hexadecimal(region['points'], count * 16)
            raw.require(int.from_bytes(header[16:20], 'little') == int(resource['resource'], 16),
                        'Header resource mismatch')
            raw.require(all(math.isfinite(v) for v in struct.unpack('<4f', header[:16])),
                        'Nonfinite header')
            raw.require(int.from_bytes(header[8:12], 'little') in (0, 0x80000000),
                        'Header outside proved native plane')
            for offset in range(0, len(points), 16):
                raw.require(all(math.isfinite(v) for v in struct.unpack_from('<4f', points, offset)),
                            'Nonfinite point')
                raw.require(int.from_bytes(points[offset + 8:offset + 12], 'little') in (0, 0x80000000),
                            'Point outside proved native plane')
            pieces.extend((header[:21], struct.pack('<I', count), points))
    return b''.join(pieces)


def normalized(frame, population):
    basis = raw.encoded(frame)
    return b'SOR-D5AR-SOURCE-PLANAR\x00\x01' + struct.pack('<I', len(basis)) + basis + body_bytes(population)


def selected_reference(value):
    """Check the admitted producer's selection-time record, never a later lease."""
    result = dict(status='UNAVAILABLE/INCONCLUSIVE', post_release_allocation_continuity='UNKNOWN',
                  unique_player_ownership='NOT_ESTABLISHED', physical_area_membership='UNKNOWN')
    try:
        area = value['outpost']['area_context']
        record = area['selected_reference']
        raw.exact_keys(record, 'status invocation command epoch reference_pointer_token formid_word type observations active copied ambiguous linked identity_time post_release_allocation_continuity')
        raw.require(record['status'] == 'SELECTED_REFERENCE_AT_NATIVE_RESOLUTION_TIME' and
                    record['identity_time'] == 'NATIVE_RESOLVED_REFERENCE_LEASE_BEFORE_RELEASE' and
                    record['post_release_allocation_continuity'] == 'UNKNOWN', 'Wrong selected-reference time claim')
        for key in ('active', 'copied', 'ambiguous', 'linked'):
            raw.require(type(record[key]) is bool, 'Invalid selection flag')
        raw.require(record['active'] and record['copied'] and record['linked'] and not record['ambiguous'] and
                    raw.geometry.uint(record['observations'], 32) == 1, 'Absent/ambiguous/unlinked selection')
        for key in ('invocation', 'command', 'epoch'):
            raw.require(raw.geometry.uint(record[key], 64) > 0, 'Missing selection scope')
        raw.require(record['epoch'] == value['capture_diagnostics']['epoch_begin'], 'Selection/copy lifecycle changed')
        pointer(record['reference_pointer_token'], 'runtime-pointer-')
        raw.require(record['reference_pointer_token'] == area['reference_pointer_token'] and
                    value['outpost']['status'] == 'ACTIVE_ESTABLISHED_OPERATION_REFERENCE', 'Different established-operation operand')
        identity = raw.geometry.hexadecimal(record['formid_word'], 4)
        formid = int.from_bytes(identity, 'little')
        raw.geometry.uint(record['type'], 8)
        raw.require(formid != 0, 'No nonzero selected FormID for identity admission')
        result.update(status='QUALIFIED_SELECTED_REFERENCE_AT_NATIVE_RESOLUTION_TIME',
                      reference_formid=f'{formid:08x}', reference_type=record['type'],
                      operation_invocation=record['invocation'], command_generation=record['command'])
    except (ValueError, TypeError, KeyError) as error:
        result['reason'] = str(error)
    return result


def derive(value):
    """Derive only the exact admitted producer's ordinary current-map contract.

    Synthetic premises are a separate role and never become native evidence.
    Callers cannot supply a profile, a qualified flag or their own certificate.
    """
    raw.validate(value)
    synthetic = value['evidence_basis'] == 'SYNTHETIC'
    profiles = [FIXTURE_BUILD, NATIVE_BUILD] if synthetic else [NATIVE_BUILD]
    raw.require(any(profile is not None and value['build'] == profile for profile in profiles),
                'Producer interval profile not admitted')
    raw.require(value['status'] == 'COPIED_UNQUALIFIED', 'Refused capture')
    context = value['capture_diagnostics']
    raw.geometry.uint(context['lock_state'], 32)
    raw.require(context['copy_status'] == 'COPIED_UNQUALIFIED' and
                context['epoch_begin'] >= 1 and context['epoch_begin'] == context['epoch_end'] and
                context['lock_state'] & 0xfff and not context['lock_state'] & 0xffc00000 and
                context['copy_begin_filetime'] > 0 and context['copy_end_filetime'] > 0,
                'Incomplete reader/lifecycle/copy premises')
    owner = value['owner_context']
    before, after = owner['before'], owner['after']
    raw.require(before['complete'] and after['complete'], 'Owner binding unavailable')
    for field in ('manager_pointer_token', 'attached_proc_token', 'owner_formid_word'):
        raw.require(before[field] == after[field], 'Owner binding changed')
    pointer(before['manager_pointer_token'], 'runtime-pointer-')
    pointer(before['attached_proc_token'], 'proc-pointer-')
    raw.require(before['attached_proc_token'] == context['proc_identity_token'], 'Different current ProcGen')
    # The accepted graph is established current-owner operation, not preview.
    raw.require(before['mode'] == after['mode'] == 2, 'Owner mode outside qualified contract')
    body = int.from_bytes(bytes.fromhex(before['owner_formid_word']), 'little')
    raw.require(body != 0, 'No current body')
    rows = []
    for source in value['sources']:
        row = dict(map_entry_id=source['map_entry_id'], source_disposition=source['source_disposition'],
                   status='UNAVAILABLE/INCONCLUSIVE', frame=None, population=None)
        try:
            pointer(source['allocation_id'], 'source-pointer-')
            pointer(source['holder_id'], 'holder-pointer-')
            raw.require(source['source_disposition'] in ('ALLOCATION_UNKNOWN', 'EMPTY'),
                        'Holder disposition outside exact producer contract')
            basis = frame_record(source['source_diagnostics'], f'{body:08x}')
            if source['source_disposition'] == 'EMPTY':
                raw.require(source['geometry'] is None, 'Unexpected empty payload')
                population = []  # Exact producer sets EMPTY only after complete zero-resource traversal.
            else:
                raw.require(source['geometry'] is not None, 'Population not copied')
                raw.require(source['geometry']['frame'] is None, 'Unsupported frame overlay for this producer')
                population = source['geometry']['population']
            wire = normalized(basis, population)
            row.update(status='QUALIFIED_REPRESENTED_SOURCE_PLANAR', frame=basis, population=population,
                       normalized_sha256=raw.digest(wire), normalized_bytes=len(wire),
                       source_allocation_scope='PROTECTED_SOURCE_GROUP_READ_ONLY_NO_LATER_LIFETIME_CLAIM')
        except (ValueError, TypeError, KeyError) as error:
            row['reason'] = str(error)
        rows.append(row)
    return dict(method=METHOD, role='SYNTHETIC_ONLY' if synthetic else 'PINNED_ORDINARY_NATIVE_GRAPH',
                capture_id=value['capture_id'], sources=rows, physical_outpost_area='UNKNOWN',
                historical_sampled_mask='UNKNOWN',
                selected_reference=selected_reference(value),
                origin_authentication='EXTERNAL_ACQUISITION_PROVENANCE_REQUIRED_NOT_A_SIGNATURE',
                clock_adjustment_diagnostic=context['copy_end_filetime'] < context['copy_begin_filetime'])


def reference_bundle():
    """Reauthenticate primary A0 and two pinned native hosts; do not trust a receipt flag."""
    guard()
    observation, original, census = baseline.baseline_observation()
    raw.require(raw.digest(original) == baseline.NORMALIZED and len(original) == 5090, 'Actual A0 normalization differs')
    certificate = json.loads((baseline.NOTES / 'receipts/checkpoint-1793680114040295400.json').read_bytes())
    events = baseline.SESSION / 'events.bin'
    event_bytes = events.read_bytes()
    raw.require(raw.digest(event_bytes[:certificate['acknowledged_bytes']]) == certificate['raw_prefix_sha256'],
                'A0 acknowledged prefix differs')
    frame = event_bytes[(2082 - 1) * 328:2082 * 328]
    raw.require(len(frame) == 328, 'Missing exact A0 birth')
    magic, size, sequence, crc = struct.unpack_from('<4I', frame)
    payload = frame[16:]
    fields = struct.unpack_from('<18Q', payload)
    source_proof = observation['proof']['source']
    raw.require((magic, size, sequence) == (0x31505253, 312, 2082) and zlib.crc32(payload) == crc and
                fields[0] == 2082 and fields[1] == 14 and fields[17] == source_proof['allocation'] == 932 and
                fields[10] == source_proof['source_pointer'] and source_proof['birth_sequence'] == 2082,
                'A0 allocation/birth integrity differs')
    source = payload[152:264]
    diagnostic = dict(status='SOURCE_BYTES_UNQUALIFIED', origin_status='SOURCE_ORIGIN_WORDS_UNQUALIFIED',
                      descriptor_status='SOURCE_DESCRIPTOR_UNQUALIFIED',
                      semantic_bytes=(source[:4] + source[0x38:0x39] + source[0x3c:0x44] + source[0x4c:0x54] + source[0x5c:0x64]).hex(),
                      source_descriptor_bytes=source[0x38:0x64].hex(),
                      origin_input_words=b''.join(source[o:o + 4] for o in (0x10, 0x14, 0x20, 0x24)).hex())
    basis = frame_record(diagnostic, observation['envelope']['source']['body_formid'])
    raw.require(basis['geographic_key'] == TARGET and basis['descriptor_semantic41'] ==
                observation['envelope']['frame']['descriptor_semantic'], 'A0 actual consumed/source descriptor join differs')
    actual_population = observation['envelope']['population']
    actual_body = body_bytes(actual_population)
    metadata_path = ROOT / '.local-work/d5s/geometry.json'
    raw.require(sha(metadata_path) == MODEL_SHA, 'Fixed native model metadata differs')
    metadata = json.loads(metadata_path.read_bytes())
    requests = [row['request'] for row in metadata['results']]
    fields = ('origin', 'source', 'owner_key', 'clip_center', 'clip_half', 'cell_bounds')
    raw.require(len(requests) == 2 and all(requests[0][key] == requests[1][key] for key in fields),
                'Fixed coordinate context differs between masks')
    # Resource weights intentionally differ by sampled mask. They are inputs to
    # represented shape, not a coordinate transform or equality prerequisite.
    request = requests[0]
    raw.require(request['origin'] == basis['native_origin_i32'] == [-200, -200] and
                request['source'] == TARGET and request['owner_key'] == int(basis['body_formid'], 16),
                'Fixed source/body/numeric-origin bridge unavailable')
    ledger_path = ROOT / 'docs/experiments/resource-retained-population/d5aq-sources.csv'
    raw.require(sha(ledger_path) == REFERENCE_LEDGER_SHA, 'Frozen reference source ledger changed')
    ledger = list(csv.DictReader(ledger_path.open(encoding='utf8')))
    hosts, inputs = [], {str(metadata_path): MODEL_SHA, str(ledger_path): REFERENCE_LEDGER_SHA}
    for name in ('geometry01', 'geometry02'):
        path = ROOT / '.local-work/d5aq' / name / 'control.json'
        expected = next(row['sha256'] for row in ledger if row['path'].replace('\\', '/') == path.relative_to(ROOT).as_posix())
        raw.require(sha(path) == expected, 'Fixed host changed')
        inputs[str(path)] = expected
        value = json.loads(path.read_bytes())
        raw.require(not value['errors'] and value['model_input_sha256'] == MODEL_SHA, 'Fixed native method failure')
        copied = path.parent / 'geometry.json'
        execution_path = path.parent / 'execution.json'
        execution = json.loads(execution_path.read_bytes())
        raw.require(sha(copied) == MODEL_SHA and execution['exit'] == 0 and
                    execution['inputs'].get(str(metadata_path)) == MODEL_SHA,
                    'Fixed execution/input provenance differs')
        inputs[str(copied)] = MODEL_SHA
        inputs[str(execution_path)] = sha(execution_path)
        raw.require(all(p['exact_points_bounds'] for run in value['runs'] for p in run['planar_model_comparison']),
                    'Independent fixed point/bounds oracle differs')
        hosts.append(value['runs'])
    raw.require([row['population'] for row in hosts[0]] == [row['population'] for row in hosts[1]], 'Fixed hosts differ')
    wires = [body_bytes(row['population']) for row in hosts[0]]
    raw.require([wire == actual_body for wire in wires] == [False, True, True], 'Actual A0 full-field reference bridge differs')
    return dict(method=METHOD, actual_a0_frame=basis, actual_a0_population=actual_population,
                actual_a0_original_normalized_sha256=baseline.NORMALIZED,
                actual_a0_derivative_sha256=raw.digest(normalized(basis, actual_population)),
                authenticated_resident_holders=len(census),
                fixed_numeric_bridge=dict(source_key=TARGET, body_formid=basis['body_formid'],
                                          native_origin_i32=request['origin'],
                                          full_source_object_in_fixed_fixture=False,
                                          historical_effective_inputs_equivalent='NOT_ESTABLISHED'),
                mask0_population=hosts[0][0]['population'], mask3_population=hosts[0][1]['population'],
                fixed_reference_equals_actual_a0=[False, True, True],
                fixed_per_mask_request_inputs=requests,
                inputs=inputs | {str(path): digest for path, digest in baseline.ANCHORS.items()},
                a0_acknowledged_prefix_sha256=certificate['raw_prefix_sha256'])


def classify(value, references):
    result = dict(method=METHOD, class_name='UNAVAILABLE/INCONCLUSIVE', historical_sampled_mask='UNKNOWN',
                  physical_outpost_area='UNKNOWN', study_eligibility='NOT_ADJUDICATED_BY_GEOMETRY_CLASSIFIER',
                  reference_event_scope='EXACT_REPRESENTED_CONTENT_ONLY',
                  effective_generation_input_equivalence='NOT_ESTABLISHED_BY_THIS_METHOD')
    try:
        derived = derive(value)
        result['derivation'] = derived
        target, unreadable = [], []
        for source, row in zip(value['sources'], derived['sources']):
            key = raw.candidate_source_key(source['source_diagnostics'])
            if key is None:
                unreadable.append(source['map_entry_id'])
            if key == TARGET:
                target.append(row)
        raw.require(len(target) == 1 and not unreadable, 'Missing/ambiguous target or unidentified resident entries')
        selected = target[0]
        raw.require(selected['status'] == 'QUALIFIED_REPRESENTED_SOURCE_PLANAR', selected.get('reason', 'Source basis unavailable'))
        raw.require(selected['frame'] == references['actual_a0_frame'], 'Source/body/full coordinate basis differs from authenticated A0')
        wire = body_bytes(selected['population'])
        mask0 = body_bytes(references['mask0_population'])
        mask3 = body_bytes(references['mask3_population'])
        raw.require(mask0 != mask3 and mask3 == body_bytes(references['actual_a0_population']), 'Invalid reference bridge')
        result['class_name'] = ('MATCH_MASK0_REFERENCE' if wire == mask0 else
                                'MATCH_MASK3_REFERENCE' if wire == mask3 else 'OTHER_QUALIFIED_GEOMETRY')
        result['first_difference_from_mask3'] = raw.first_field_difference(
            dict(population=selected['population']), dict(population=references['mask3_population']))
        result['role'] = derived['role']
    except (ValueError, TypeError, KeyError) as error:
        result['reason'] = str(error)
    return result


def compare(left, right):
    a, b = derive(left), derive(right)
    raw.require(a['capture_id'] != b['capture_id'], 'Duplicate capture identity')
    raw.require(a['role'] == b['role'], 'Different evidence roles')
    def index(value):
        rows = [row for row in value['sources'] if row['frame'] is not None]
        result = {row['frame']['geographic_key']: row for row in rows}
        raw.require(len(result) == len(rows), 'Ambiguous geographic source')
        return result
    x, y = index(a), index(b)
    rows = []
    for key in sorted(x.keys() | y.keys()):
        row = dict(source_key=key, status='UNAVAILABLE/INCONCLUSIVE')
        if key in x and key in y and x[key]['frame'] == y[key]['frame']:
            p, q = normalized(x[key]['frame'], x[key]['population']), normalized(y[key]['frame'], y[key]['population'])
            row.update(status='EQUAL_REPRESENTED_BYTES' if p == q else 'DIFFERENT_REPRESENTED_BYTES',
                       first_normalized_byte_difference=next((n for n, pair in enumerate(zip(p, q)) if pair[0] != pair[1]),
                                                            min(len(p), len(q)) if len(p) != len(q) else None),
                       first_semantic_field_difference=raw.first_field_difference(x[key], y[key]))
        rows.append(row)
    for side, value in (('left', a), ('right', b)):
        rows.extend(dict(side=side, map_entry_id=row['map_entry_id'], status=row['status'], reason=row.get('reason'))
                    for row in value['sources'] if row['frame'] is None)
    return dict(method=METHOD, role=a['role'], sources=rows, historical_sampled_mask='UNKNOWN', physical_outpost_area='UNKNOWN')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=('references', 'classify', 'compare'))
    parser.add_argument('paths', type=Path, nargs='+')
    args = parser.parse_args()
    guard()
    sources = {str(Path(module.__file__).resolve()): sha(module.__file__)
               for module in tuple(sys.modules.values())
               if getattr(module, '__file__', None) and Path(module.__file__).suffix == '.py' and
               Path(module.__file__).resolve().is_relative_to(ROOT)}
    required = dict(references=1, classify=2, compare=3)[args.mode]
    raw.require(len(args.paths) == required, 'Wrong number of paths')
    destination = args.paths[-1].absolute()
    raw.require(destination.resolve().is_relative_to(ROOT / '.local-work/d5ar') and
                destination.parent.is_dir() and not destination.exists(), 'Fresh ignored D5AR output required')
    raw.require(not any(path.is_symlink() or path.is_junction() for path in
                        (destination, *destination.parents, destination.resolve(), *destination.resolve().parents)),
                'No reparse output')
    inputs = {}
    if args.mode == 'references':
        result = reference_bundle()
    else:
        left, original_hash = raw.read_snapshot(args.paths[0])
        inputs[str(args.paths[0])] = original_hash
        if args.mode == 'compare':
            right, original_hash = raw.read_snapshot(args.paths[1])
            inputs[str(args.paths[1])] = original_hash
            result = compare(left, right)
        else:
            references = reference_bundle()
            result = classify(left, references)
            result['reference_bundle_sha256'] = raw.digest(raw.encoded(references))
    result['input_sha256'] = inputs
    raw.require(all(sha(path) == digest for path, digest in sources.items()), 'Executed source changed during analysis')
    result['source_sha256'] = sources
    guard()
    with destination.open('xb') as stream:
        stream.write(raw.encoded(result) + b'\n')


if __name__ == '__main__':
    main()
