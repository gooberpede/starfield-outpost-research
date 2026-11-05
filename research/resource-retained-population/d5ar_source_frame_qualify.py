# SPDX-License-Identifier: GPL-3.0-or-later
"""Owned adversarial controls for the separate D5AR source-planar method.

Reads an explicit authenticated reference-bundle output and project sources;
writes fresh ignored synthetic fixtures/receipt only. Uses owned raw-fixture
helpers under SOR-P-0002. No native execution, game, save/database/configuration
writes, network or installation. Actual reference authentication is separately
executed by d5ar_source_frames.py references and independently repeated in review.
"""
import os
import sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):
    raise RuntimeError('Use pinned Python -E -B without optimization')

import copy
import json
from pathlib import Path
import struct
import subprocess
import uuid

import d5ar_source_frames as method
import d5ar_snapshot as raw
from d5ar_qualify import fixture as raw_fixture, reseal
from d5ad_baseline import ROOT, guard, sha


def fixture(basis, population, context=1):
    value = raw_fixture(context)
    value['build'] = dict(method.FIXTURE_BUILD)
    value['capture_diagnostics'].update(epoch_begin=7, epoch_end=7, lock_state=1,
        copy_begin_filetime=1000, copy_end_filetime=2000, proc_identity_token='proc-pointer-200000')
    descriptor = bytes.fromhex(basis['descriptor_semantic41'])
    descriptor = descriptor[:1] + b'\x11\x22\x33' + descriptor[1:]
    selected = (int(basis['terrain_formid'], 16).to_bytes(4, 'little') + descriptor[:1] +
                descriptor[4:12] + descriptor[20:28] + descriptor[36:44])
    binding = dict(status='OBSERVED_UNQUALIFIED', complete=True,
        manager_pointer_token='runtime-pointer-100000', attached_proc_token='proc-pointer-200000',
        owner_formid_word=int(basis['body_formid'], 16).to_bytes(4, 'little').hex(),
        mode=2, current_descriptor_bytes='00' * 44)
    value['owner_context'] = dict(before=dict(binding), after=dict(binding))
    value['sources'] = value['sources'][:1]
    source = value['sources'][0]
    source.update(allocation_id='source-pointer-300000', holder_id='holder-pointer-400000',
                  owning_grid=None, source_disposition='ALLOCATION_UNKNOWN')
    source['source_diagnostics'] = dict(status='SOURCE_BYTES_UNQUALIFIED', semantic_bytes=selected.hex(),
        visited_token=0xffffffffff, origin_status='SOURCE_ORIGIN_WORDS_UNQUALIFIED',
        origin_input_words=basis['origin_input_words16'], descriptor_status='SOURCE_DESCRIPTOR_UNQUALIFIED',
        source_descriptor_bytes=descriptor.hex())
    geometry = source['geometry']
    geometry.update(source=None, frame=None, population=copy.deepcopy(population))
    geometry['capture'].update(resource_slots=len(population),
        region_total=sum(len(r['regions']) for r in population),
        point_total=sum(g['count'] for r in population for g in r['regions']))
    return reseal(value)


def oracle(basis, population):
    """Direct independent construction from the documented byte layout."""
    metadata = json.dumps(basis, ensure_ascii=True, allow_nan=False,
                          sort_keys=True, separators=(',', ':')).encode('ascii')
    data = bytearray(b'SOR-D5AR-SOURCE-PLANAR\x00\x01')
    data.extend(len(metadata).to_bytes(4, 'little'))
    data.extend(metadata)
    data.extend(len(population).to_bytes(4, 'little'))
    ordered = sorted(population, key=lambda resource: int(resource['resource'], 16))
    for resource in ordered:
        data.extend(int(resource['resource'], 16).to_bytes(4, 'big'))
        data.extend(len(resource['regions']).to_bytes(4, 'little'))
        for region in resource['regions']:
            data.extend(bytes.fromhex(region['header'])[:21])
            data.extend(region['count'].to_bytes(4, 'little'))
            data.extend(bytes.fromhex(region['points']))
    return bytes(data)


def main():
    guard()
    out = Path(sys.argv[1]).resolve()
    reference_path = Path(sys.argv[2]).resolve()
    raw.require(out.is_relative_to(ROOT / '.local-work/d5ar') and not out.exists(), 'Fresh ignored output required')
    raw.require(not any(p.is_symlink() or p.is_junction() for p in (out, *out.parents)), 'No reparse output')
    references = json.loads(reference_path.read_bytes(), object_pairs_hook=raw.unique_pairs)
    raw.require(references['method'] == method.METHOD and references['actual_a0_original_normalized_sha256'] ==
                '0c05d4a4c458b533d1ec7ae3acc8b34698ac48b91ff2965224e5c37ca055da96', 'Wrong reference input')
    sources = {str(Path(module.__file__).resolve()): sha(module.__file__)
               for module in tuple(sys.modules.values()) if getattr(module, '__file__', None) and
               Path(module.__file__).suffix == '.py' and Path(module.__file__).resolve().is_relative_to(ROOT)}
    out.mkdir()
    checks = []
    def check(name, condition):
        raw.require(condition, name)
        checks.append(dict(name=name, status='PASS'))
    def fresh(value):
        result = copy.deepcopy(value)
        result['capture_id'] = str(uuid.uuid4())
        for source in result['sources']:
            if source['geometry'] is not None:
                source['geometry']['snapshot_id'] = result['capture_id']
        return reseal(result)
    def class_is(name, value, expected):
        result = method.classify(reseal(value), references)
        check(name, result['class_name'] == expected)
        return result
    basis = references['actual_a0_frame']
    base = fixture(basis, references['actual_a0_population'])
    derived = method.derive(base)
    check('explicit synthetic role never native', derived['role'] == 'SYNTHETIC_ONLY')
    check('independent full frame projection', derived['sources'][0]['frame'] == basis)
    selected = copy.deepcopy(base)
    selected['outpost'].update(status='ACTIVE_ESTABLISHED_OPERATION_REFERENCE',
                              reference='observed-reference-pointer-500000')
    area = selected['outpost']['area_context']
    area['reference_pointer_token'] = 'runtime-pointer-500000'
    area['selected_reference'] = dict(status='SELECTED_REFERENCE_AT_NATIVE_RESOLUTION_TIME',
        invocation=11, command=22, epoch=7, reference_pointer_token='runtime-pointer-500000',
        formid_word='78563412', type=0x40, observations=1, active=True, copied=True,
        ambiguous=False, linked=True, identity_time='NATIVE_RESOLVED_REFERENCE_LEASE_BEFORE_RELEASE',
        post_release_allocation_continuity='UNKNOWN')
    selection = method.derive(reseal(selected))['selected_reference']
    check('selection identity at native resolution time only', selection['status'] ==
          'QUALIFIED_SELECTED_REFERENCE_AT_NATIVE_RESOLUTION_TIME' and selection['reference_formid'] == '12345678' and
          selection['post_release_allocation_continuity'] == 'UNKNOWN' and selection['unique_player_ownership'] == 'NOT_ESTABLISHED')
    for name, changes in [('ambiguous', dict(ambiguous=True)), ('absent', dict(copied=False)),
                           ('ended scope', dict(active=False)), ('multiple', dict(observations=2)),
                           ('wrong epoch', dict(epoch=8)), ('wrong operand', dict(reference_pointer_token='runtime-pointer-500001')),
                           ('no FormID', dict(formid_word='00000000')), ('invented later lease', dict(post_release_allocation_continuity='QUALIFIED'))]:
        changed = fresh(selected)
        changed['outpost']['area_context']['selected_reference'].update(changes)
        check('selection rejects ' + name, method.derive(reseal(changed))['selected_reference']['status'] == 'UNAVAILABLE/INCONCLUSIVE')
    typed = fresh(selected)
    typed['outpost']['area_context']['selected_reference']['type'] = 0x7f
    check('raw type preserved without invented enum semantics', method.derive(reseal(typed))['selected_reference']['reference_type'] == 0x7f)
    wire = method.normalized(basis, references['actual_a0_population'])
    check('independent complete byte oracle', wire == oracle(basis, references['actual_a0_population']))
    check('versioned derivative differs from historical normalization', raw.digest(wire) !=
          references['actual_a0_original_normalized_sha256'])
    class_is('actual reference represented as synthetic mask3 fixture', base, 'MATCH_MASK3_REFERENCE')
    mask0 = fixture(basis, references['mask0_population'])
    class_is('complete mask0 fixture', mask0, 'MATCH_MASK0_REFERENCE')
    check('independent mask0 byte oracle', method.normalized(basis, references['mask0_population']) ==
          oracle(basis, references['mask0_population']))
    reversed_slots = fresh(base)
    reversed_slots['sources'][0]['geometry']['population'].reverse()
    check('resource slot permutation justified', method.compare(base, reseal(reversed_slots))['sources'][0]['status'] == 'EQUAL_REPRESENTED_BYTES')
    padded = fresh(base)
    source = padded['sources'][0]
    source['source_diagnostics']['source_descriptor_bytes'] = (source['source_diagnostics']['source_descriptor_bytes'][:2] +
                                                               'aabbcc' + source['source_diagnostics']['source_descriptor_bytes'][8:])
    for resource in source['geometry']['population']:
        for region in resource['regions']:
            region['header'] = region['header'][:42] + 'fedcba'
    class_is('only proved source/header padding excluded', padded, 'MATCH_MASK3_REFERENCE')
    check('padding remains different in raw input', reseal(padded)['payload_sha256'] != base['payload_sha256'])
    for name, field, at in [('header scalar', 'header', 0), ('point scalar', 'points', 0),
                            ('fourth point word', 'points', 12)]:
        changed = fresh(base)
        region = changed['sources'][0]['geometry']['population'][0]['regions'][0]
        content = bytearray.fromhex(region[field])
        number = struct.unpack_from('<f', content, at)[0]
        struct.pack_into('<f', content, at, number + 1.)
        region[field] = content.hex()
        result = class_is('equal counts changed ' + name, changed, 'OTHER_QUALIFIED_GEOMETRY')
        check('field difference reported ' + name, result['first_difference_from_mask3'] is not None)
    changed = fresh(base)
    region = next(region for resource in changed['sources'][0]['geometry']['population']
                  for region in resource['regions'] if region['count'] >= 2 and
                  region['points'][:32] != region['points'][32:64])
    check('ordered-point fixture has distinct first pair', region['count'] >= 2 and region['points'][:32] != region['points'][32:64])
    region['points'] = region['points'][32:64] + region['points'][:32] + region['points'][64:]
    class_is('point order never canonicalized', changed, 'OTHER_QUALIFIED_GEOMETRY')
    changed = fresh(base)
    changed['sources'][0]['geometry']['population'][0]['regions'].reverse()
    class_is('region order never canonicalized', changed, 'OTHER_QUALIFIED_GEOMETRY')
    for field in ('header', 'points'):
        changed = fresh(base)
        region = changed['sources'][0]['geometry']['population'][0]['regions'][0]
        data = bytearray.fromhex(region[field]);data[8:12] = b'\0\0\0\x80';region[field] = data.hex()
        class_is('signed zero preserved ' + field, changed, 'OTHER_QUALIFIED_GEOMETRY')
    empty = fresh(base)
    empty['sources'][0].update(source_disposition='EMPTY', geometry=None, geometry_sha256=None)
    class_is('complete empty target is valid novel representation', empty, 'OTHER_QUALIFIED_GEOMETRY')
    check('empty representation is not geographical absence', method.classify(empty, references)['physical_outpost_area'] == 'UNKNOWN')
    other = fresh(base)
    for binding in other['owner_context'].values():binding['owner_formid_word'] = '02000000'
    class_is('different body cannot match by content', other, 'UNAVAILABLE/INCONCLUSIVE')
    check('second genuinely distinct body context derives', method.derive(reseal(other))['sources'][0]['frame']['body_formid'] == '00000002')
    check('generic wrong owner incomparable', method.compare(base, other)['sources'][0]['status'] == 'UNAVAILABLE/INCONCLUSIVE')
    other = fresh(base)
    diagnostic = other['sources'][0]['source_diagnostics']
    descriptor = bytearray.fromhex(diagnostic['source_descriptor_bytes']);descriptor[12] ^= 1
    diagnostic['source_descriptor_bytes'] = descriptor.hex()
    class_is('unknown semantic descriptor word is mandatory', other, 'UNAVAILABLE/INCONCLUSIVE')
    other = fresh(base)
    other['sources'][0]['source_diagnostics']['origin_input_words'] = struct.pack('<4i', 1, 1, 3, 3).hex()
    class_is('same numeric origin different full inputs not substituted', other, 'UNAVAILABLE/INCONCLUSIVE')
    overlay = fresh(base)
    overlay['sources'][0]['geometry']['frame'] = raw_fixture()['sources'][0]['geometry']['frame']
    class_is('unsupported supplied frame cannot override producer contract', overlay, 'UNAVAILABLE/INCONCLUSIVE')
    for name, mutate in [
        ('epoch change', lambda v: v['capture_diagnostics'].update(epoch_end=8)),
        ('missing copy window', lambda v: v['capture_diagnostics'].update(copy_begin_filetime=0)),
        ('no native reader', lambda v: v['capture_diagnostics'].update(lock_state=0)),
        ('lock word outside native u32', lambda v: v['capture_diagnostics'].update(lock_state=(1 << 50) | 1)),
        ('recursive exclusive', lambda v: v['capture_diagnostics'].update(lock_state=0x400001)),
        ('wrong current proc', lambda v: v['capture_diagnostics'].update(proc_identity_token='proc-pointer-999999')),
        ('preview mode', lambda v: [b.update(mode=3) for b in v['owner_context'].values()]),
        ('missing allocation', lambda v: v['sources'][0].update(allocation_id=None)),
        ('failed origin group', lambda v: v['sources'][0]['source_diagnostics'].update(origin_status='READ_FAILED', origin_input_words=None)),
        ('failed descriptor group', lambda v: v['sources'][0]['source_diagnostics'].update(descriptor_status='READ_FAILED', source_descriptor_bytes=None)),
        ('refused envelope', lambda v: (v.update(status='REFUSED'), v['capture_diagnostics'].update(copy_status='COPY_FAILED'))),
    ]:
        changed = fresh(base);mutate(changed)
        class_is(name, changed, 'UNAVAILABLE/INCONCLUSIVE')
    for status in ('SOURCE_LIFETIME_RETIRED', 'SOURCE_RECORDER_UNAVAILABLE'):
        changed = fresh(base)
        changed['sources'][0]['source_diagnostics'].update(status=status, origin_status=status, descriptor_status=status,
            semantic_bytes=None, visited_token=None, origin_input_words=None, source_descriptor_bytes=None)
        class_is(status + ' never derives a source basis', changed, 'UNAVAILABLE/INCONCLUSIVE')
        check(status + ' retains full raw population', changed['sources'][0]['geometry']['population'] == base['sources'][0]['geometry']['population'])
    for name, word, at in [('nonfinite point', 0x7fc00000, 0), ('nonplanar point', 0x3f800000, 8)]:
        changed = fresh(base)
        region = changed['sources'][0]['geometry']['population'][0]['regions'][0]
        data = bytearray.fromhex(region['points']);struct.pack_into('<I', data, at, word);region['points'] = data.hex()
        class_is(name + ' raw retained', changed, 'UNAVAILABLE/INCONCLUSIVE')
    changed = fresh(base)
    changed['sources'][0]['source_diagnostics']['origin_input_words'] = struct.pack('<4i', 671089, 0, 0, 0).hex()
    class_is('unobserved FP rounding premise refused without data loss', changed, 'UNAVAILABLE/INCONCLUSIVE')
    changed = fresh(base)
    changed['capture_diagnostics']['copy_end_filetime'] = 1
    class_is('clock rollback is diagnostic', changed, 'MATCH_MASK3_REFERENCE')
    check('clock rollback disclosed', method.derive(changed)['clock_adjustment_diagnostic'])
    duplicate = fresh(base)
    second = copy.deepcopy(duplicate['sources'][0]);second.update(map_entry_id='map-entry-99',
        allocation_id='source-pointer-300001', holder_id='holder-pointer-400001')
    duplicate['sources'].append(second)
    class_is('duplicate geographic target allocations ambiguous', duplicate, 'UNAVAILABLE/INCONCLUSIVE')
    unknown = fresh(base)
    holder = copy.deepcopy(unknown['sources'][0]);holder.update(map_entry_id='map-entry-98',
        allocation_id=None, holder_id=None, geometry=None, geometry_sha256=None)
    holder['source_diagnostics'].update(status='READ_FAILED', semantic_bytes=None, visited_token=None)
    unknown['sources'].append(holder)
    class_is('unknown resident could hide another target', unknown, 'UNAVAILABLE/INCONCLUSIVE')
    check('unknown holder retained', len(method.derive(unknown)['sources']) == 2)
    old = fresh(base);old['evidence_basis'] = 'UNQUALIFIED_NATIVE'
    old['build'].update(plugin_sha256='336e336259b10b8fcd9623ff0aecf24f6c3654c78275255461f303620b4460e6',
                        source_lock_sha256='84008fe52b0716f6f04a3d8e31303772e21110219eb2b5492161630b1e1ecb56', sfse_sha256=method.SFSE)
    class_is('old five-hook producer cannot self-certify', old, 'UNAVAILABLE/INCONCLUSIVE')
    old = fresh(base)
    old['build'].update(plugin_sha256='45f01bf45e17aaf2621aa94142740e3f89ba5a4626b42789f79316e62e243c7e',
                        source_lock_sha256='b94c58e44e7ca409081bc7916b4657fc658ec3b291b3a899cb8a08dabac1c240')
    class_is('ending-only producer lacks owner admission', old, 'UNAVAILABLE/INCONCLUSIVE')
    old = fresh(base);old['evidence_basis'] = 'UNQUALIFIED_NATIVE'
    old['build'].update(plugin_sha256='48ca0dc8f89a7b43d48b6f6393ef3aeebb3141de6ebea335a1652e02ea37f1ed',
                        source_lock_sha256='e7e8d002064f90e3d5ef63ff34ebc7300c6b202086cba58f878f3ad7d52e3f2d', sfse_sha256=method.SFSE)
    class_is('older lifecycle producer superseded by exact new profile', old, 'UNAVAILABLE/INCONCLUSIVE')
    try:
        method.compare(base, base)
    except ValueError:
        check('duplicate capture identity refused', True)
    else:
        raise ValueError('Duplicate capture accepted')
    outside = ROOT / '.local-work' / ('d5ar-forbidden-reference-' + str(uuid.uuid4()) + '.json')
    existing = out / 'existing-output.json'
    existing.write_bytes(b'Owned preservation sentinel\n')
    for name, destination in (('outside D5AR namespace', outside), ('existing output', existing)):
        result = subprocess.run([sys.executable, '-E', '-B', str(Path(method.__file__)),
                                 'references', str(destination)], capture_output=True)
        check('CLI refuses ' + name, result.returncode != 0 and b'Fresh ignored D5AR output required' in result.stderr and
              (not destination.exists() if destination == outside else destination.read_bytes() == b'Owned preservation sentinel\n'))
    for name, value in (('mask3', base), ('mask0', mask0), ('empty', empty), ('raw-unknown', unknown)):
        with (out / (name + '.json')).open('xb') as stream:stream.write(raw.encoded(reseal(value)) + b'\n')
    complete_partial = out / 'complete-but-unpublished.partial'
    with complete_partial.open('xb') as stream:stream.write((out / 'mask3.json').read_bytes())
    destination = out / 'partial-must-not-classify.json'
    result = subprocess.run([sys.executable, '-E', '-B', str(Path(method.__file__)),
                             'classify', str(complete_partial), str(destination)], capture_output=True)
    check('source-planar CLI refuses complete unpublished input without result', result.returncode != 0 and
          b'Unpublished partial snapshot' in result.stderr and not destination.exists())
    raw.require(all(sha(path) == digest for path, digest in sources.items()), 'Executed source changed')
    receipt = dict(status='PASS', method=method.METHOD, checks=checks, synthetic_only=True,
                   native_execution=False, native_profile=method.NATIVE_BUILD,
                   references=dict(path=str(reference_path), sha256=sha(reference_path)),
                   source_sha256=sources, floors=guard())
    with (out / 'qualification.json').open('xb') as stream:stream.write(raw.encoded(receipt) + b'\n')
    print(json.dumps(dict(status='PASS', controls=len(checks), receipt=str(out / 'qualification.json'))))


if __name__ == '__main__':
    main()
