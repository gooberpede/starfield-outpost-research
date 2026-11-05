# SPDX-License-Identifier: GPL-3.0-or-later
"""Execute bounded offline D5AR interchange controls on owned synthetic inputs.

Reads exact module sources and explicit output path; writes fresh ignored fixture
files and qualification receipt. No game/native execution, save/database reads,
network or installs. SOR-P-0002 geometry layout derives from D5AI evidence.
"""
import os
import sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):
    raise RuntimeError('Use pinned Python -E -B without optimization')

import copy
from datetime import datetime, timezone
import json
from pathlib import Path
import struct
import subprocess
import uuid

import d5ar_snapshot as snapshot


def fixture(context=1):
    session, capture = str(uuid.uuid4()), str(uuid.uuid4())
    source = dict(key=f'{context}:100:200:00000001', body_formid=f'{context:08x}')
    frame = dict(basis='source-planar', anchor_i32=[context, 0], origin_i32=[0, 0],
                 clip_center_f32=['00000000'] * 4, clip_half_f32=['0000803f'] * 4)
    population = []
    for form, count in ((12, 2), (7, 1)):
        header = struct.pack('<4fIB3s', 1., 2., 3., 4., form, 1, b'abc')
        population.append(dict(resource=f'{form:08x}', regions=[dict(header=header.hex(), count=count,
                            points=(struct.pack('<4f', 1., 2., 3., 4.) * count).hex())]))
    geometry = dict(schema='sor-d5ai-geometry/1', session_id=session, snapshot_id=capture,
                    source=source, frame=frame, capture=dict(complete=True, status='OK', resource_slots=2,
                    region_total=2, point_total=3), population=population, loss=0,
                    generation_quality='UNKNOWN')
    holder = dict(allocation_id='allocation-1', map_entry_id='map-entry-1', holder_id='holder-1',
                  owning_grid='grid-1', source_disposition='IDENTIFIED', area_association='UNKNOWN',
                  source_diagnostics=dict(status='NOT_CAPTURED', semantic_bytes=None, visited_token=None,
                                          descriptor_status='NOT_CAPTURED', source_descriptor_bytes=None,
                                          origin_status='NOT_CAPTURED', origin_input_words=None),
                  geometry=geometry, geometry_sha256=snapshot.digest(snapshot.encoded(geometry)))
    unknown = dict(allocation_id=None, map_entry_id='map-entry-2', holder_id=None, owning_grid=None,
                   source_diagnostics=dict(status='NOT_CAPTURED', semantic_bytes=None, visited_token=None,
                                           descriptor_status='NOT_CAPTURED', source_descriptor_bytes=None,
                                           origin_status='NOT_CAPTURED', origin_input_words=None),
                   source_disposition='ALLOCATION_UNKNOWN', area_association='UNKNOWN', geometry=None,
                   geometry_sha256=None)
    return snapshot.seal(dict(schema=snapshot.SCHEMA, method=snapshot.METHOD, capture_id=capture,
        session_id=session, utc=datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        process=dict(pid=100 + context, creation_filetime=context),
        build=dict(game_exe_sha256='0' * 64, sfse_sha256='1' * 64, plugin_sha256='2' * 64,
                   source_lock_sha256='3' * 64, game_version='1.16.244.0'),
        scope='RESIDENT_MAP_CENSUS_AREA_ASSOCIATION_UNKNOWN',
        owner_context={side: dict(status='NOT_CAPTURED', complete=False, manager_pointer_token=None,
                                  attached_proc_token=None, owner_formid_word=None, mode=None,
                                  current_descriptor_bytes=None) for side in ('before', 'after')},
        capture_diagnostics=dict(copy_status='COPIED_UNQUALIFIED', epoch_begin=0, epoch_end=0,
                                 copy_begin_filetime=0, copy_end_filetime=0,
                                 lock_state=1, required_bytes=1000, proc_identity_token='fixture-proc'),
        outpost=dict(status='SOURCE_REPORTED', reference=f'fixture-beacon-{context}',
                     area_context=dict(world=f'fixture-world-{context}', radius=context * 100)),
        sources=[holder, unknown], status='COPIED_UNQUALIFIED', evidence_basis='SYNTHETIC'))


def reseal(value):
    for source in value['sources']:
        if source['geometry'] is not None:
            source['geometry_sha256'] = snapshot.digest(snapshot.encoded(source['geometry']))
    return snapshot.seal(value)


def independent_normalized(value):
    """Independent direct byte construction, without calling the normalizer."""
    source = json.dumps(value['source'], sort_keys=True, separators=(',', ':')).encode()
    frame = json.dumps(value['frame'], sort_keys=True, separators=(',', ':')).encode()
    pieces = [struct.pack('<I', len(source)), source, struct.pack('<I', len(frame)), frame,
              struct.pack('<I', len(value['population']))]
    for resource in sorted(value['population'], key=lambda x: int(x['resource'], 16)):
        pieces.extend([bytes.fromhex(resource['resource']), struct.pack('<I', len(resource['regions']))])
        for region in resource['regions']:
            pieces.extend([bytes.fromhex(region['header'])[:21], struct.pack('<I', region['count']),
                           bytes.fromhex(region['points'])])
    return b''.join(pieces)


def main():
    root = Path(__file__).resolve().parents[2]
    out = Path(sys.argv[1]).resolve()
    snapshot.guard()
    snapshot.require(out.is_relative_to(root / '.local-work/d5ar') and not out.exists(), 'Fresh ignored D5AR output required')
    snapshot.require(not any(p.is_symlink() or p.is_junction() for p in (out, *out.parents)), 'No reparse outputs')
    entries = sorted(Path(__file__).parent.glob('d5ar_*.py')) + [root / 'runtime/outpost-geometry-snapshot/build.py']
    executed = sorted(set(entries + [Path(snapshot.geometry.__file__), Path(__file__).with_name('d5ad_baseline.py')]))
    source_pins = {str(p.relative_to(root)): snapshot.digest(p.read_bytes()) for p in executed}
    out.mkdir(parents=True)
    checks = []

    def check(name, condition):
        snapshot.require(condition, name)
        checks.append(dict(name=name, result='PASS'))

    def refuses(name, operation):
        try:
            operation()
        except (ValueError, OSError, KeyError, TypeError):
            check(name, True)
        else:
            raise ValueError('Failed refusal: ' + name)

    a = fixture()
    first = snapshot.publish(a, out)
    check('exclusive flushed publication and decoding', snapshot.load(first) == a)
    refuses('same capture cannot overwrite finalized file', lambda: snapshot.publish(a, out))
    b = copy.deepcopy(a)
    b['capture_id'] = str(uuid.uuid4())
    b['sources'][0]['geometry']['snapshot_id'] = b['capture_id']
    reseal(b)
    check('full raw independent oracle', independent_normalized(a['sources'][0]['geometry']) ==
          snapshot.geometry.normalize(a['sources'][0]['geometry']))
    check('equal complete represented geometry', snapshot.compare(a, b)['sources'][0]['status'] == 'EQUAL_REPRESENTED_BYTES')
    b['sources'][0]['geometry']['population'].reverse()
    reseal(b)
    check('justified resource slot permutation', snapshot.compare(a, b)['sources'][0]['status'] == 'EQUAL_REPRESENTED_BYTES')
    b['sources'][0]['geometry']['population'][0]['regions'][0]['header'] = (
        b['sources'][0]['geometry']['population'][0]['regions'][0]['header'][:-6] + 'ffffff')
    reseal(b)
    check('raw padding retained semantic exclusion only', snapshot.compare(a, b)['sources'][0]['status'] == 'EQUAL_REPRESENTED_BYTES')
    b['sources'][0]['geometry']['population'][0]['regions'][0]['points'] = (
        struct.pack('<4f', 2., 2., 3., 4.).hex())
    reseal(b)
    check('equal counts altered point rejected as equality', snapshot.compare(a, b)['sources'][0]['status'] == 'DIFFERENT_REPRESENTED_BYTES')
    distinct = fixture(2)
    check('different world source cannot match by geometry hash', all(r['status'] == 'UNAVAILABLE_INCOMPARABLE' for r in snapshot.compare(a, distinct)['sources']))
    check('unknown holder retained', snapshot.validate(distinct)['sources'][1]['source_disposition'] == 'ALLOCATION_UNKNOWN')
    check('distinct snapshots unique names', snapshot.publish(distinct, out) != first)
    for name, mutation in [
        ('wrong owner', lambda v: v['sources'][0]['geometry']['source'].update(body_formid='wrong')),
        ('truncated points', lambda v: v['sources'][0]['geometry']['population'][0]['regions'][0].update(points='00')),
        ('altered scalar count', lambda v: v['sources'][0]['geometry']['capture'].update(point_total=99)),
        ('duplicate map entries', lambda v: v['sources'].append(copy.deepcopy(v['sources'][0]))),
        ('unknown fields', lambda v: v.update(unproved=True)),
        ('missing process creation', lambda v: v['process'].update(creation_filetime=0)),
        ('invented native qualification', lambda v: v.update(evidence_basis='QUALIFIED_NATIVE')),
        ('unsupported outpost census', lambda v: v.update(scope='COMPLETE_OUTPOST')),
        ('failed holder with geometry', lambda v: v['sources'][0].update(source_disposition='COPY_FAILED')),
        ('unknown nested semantic field', lambda v: v['sources'][0]['geometry'].update(unverified_semantics=1)),
        ('unknown nested capture field', lambda v: v['sources'][0]['geometry']['capture'].update(unverified_semantics=1)),
        ('incomplete capture', lambda v: v['sources'][0]['geometry']['capture'].update(complete=False)),
    ]:
        value = copy.deepcopy(a)
        mutation(value)
        refuses(name, lambda value=value: reseal(value))
    broken = out / 'truncated.snapshot.json'
    broken.write_bytes(first.read_bytes()[:-8])
    refuses('truncated file', lambda: snapshot.load(broken))
    duplicate = out / 'duplicate.snapshot.json'
    duplicate.write_bytes(b'{"schema":1,"schema":2}')
    refuses('duplicate JSON frame key', lambda: snapshot.load(duplicate))
    refuses('duplicate capture comparison', lambda: snapshot.compare(a, a))
    refused = copy.deepcopy(b)
    refused['status'] = 'REFUSED'
    reseal(refused)
    check('refused invocation never comparable', all(r['status'] == 'UNAVAILABLE_INCOMPARABLE' for r in snapshot.compare(a, refused)['sources']))
    check('every missing holder has disposition row', len(snapshot.compare(a, b)['sources']) == 3)
    wrong = copy.deepcopy(b)
    wrong['sources'][0]['geometry']['source']['body_formid'] = '00000009'
    reseal(wrong)
    check('valid different source owner incomparable', all(r['status'] == 'UNAVAILABLE_INCOMPARABLE' for r in snapshot.compare(a, wrong)['sources']))
    wrong['sources'][0]['geometry']['frame'] = dict(basis='consumed-descriptor-v1', owner_formid='00000001', descriptor_semantic='00' * 41)
    refuses('valid mismatched consumed-frame owner', lambda: reseal(wrong))
    wrong = copy.deepcopy(b)
    wrong['sources'][0]['geometry']['frame']['anchor_i32'][0] += 1
    reseal(wrong)
    check('valid different frame incomparable', all(r['status'] == 'UNAVAILABLE_INCOMPARABLE' for r in snapshot.compare(a, wrong)['sources']))
    unknown = copy.deepcopy(b)
    unknown['sources'][0]['source_disposition'] = 'ALLOCATION_UNKNOWN'
    unknown['sources'][0]['geometry']['source'] = None
    unknown['sources'][0]['geometry']['frame'] = None
    reseal(unknown)
    check('healthy unknown-source raw geometry preserved', snapshot.validate(unknown)['sources'][0]['geometry']['population'] == b['sources'][0]['geometry']['population'])
    check('unknown raw populations never dropped', len(snapshot.compare(a, unknown)['sources']) == 4)
    for status in ('SOURCE_LIFETIME_RETIRED', 'SOURCE_RECORDER_UNAVAILABLE'):
        held = copy.deepcopy(unknown)
        diagnostic = held['sources'][0]['source_diagnostics']
        diagnostic.update(status=status, origin_status=status, descriptor_status=status)
        reseal(held)
        check(status + ' preserves healthy raw geometry', held['sources'][0]['geometry'] == unknown['sources'][0]['geometry'])
        diagnostic['origin_status'] = 'NOT_CAPTURED'
        refuses(status + ' cannot leave a partially admitted source group', lambda held=held: reseal(held))
        diagnostic['origin_status'] = status
        diagnostic['source_descriptor_bytes'] = '00' * 44
        refuses(status + ' cannot retain an apparent source certificate', lambda held=held: reseal(held))
    target = copy.deepcopy(b)
    target['sources'][0]['source_diagnostics'] = dict(status='SOURCE_BYTES_UNQUALIFIED',
        descriptor_status='NOT_CAPTURED', source_descriptor_bytes=None,
        origin_status='SOURCE_ORIGIN_WORDS_UNQUALIFIED', origin_input_words=struct.pack('<4i', 0, 0, 2, 2).hex(),
        semantic_bytes=(struct.pack('<IB6i', 0x29d20e, 0, 195, 109, 8, 0, 0, 0)).hex(), visited_token=2 ** 63 + 9)
    reseal(target)
    diagnostic = snapshot.feynman_diagnostic(target)
    check('offline target diagnostic preserves u64 token without mask inference',
          len(diagnostic['candidate_matches']) == 1 and diagnostic['sampled_mask'] == 'UNKNOWN' and
          diagnostic['status'] == 'UNAVAILABLE/INCONCLUSIVE')
    check('unobserved source not interpreted as absence', diagnostic['absence_of_geographical_resources'] == 'NOT_ESTABLISHED')
    nonfinite = copy.deepcopy(b)
    region = nonfinite['sources'][0]['geometry']['population'][0]['regions'][0]
    region['points'] = '0000c07f' + region['points'][8:]
    reseal(nonfinite)
    check('nonfinite raw points retained without comparison', snapshot.compare(a, nonfinite)['sources'][0]['status'] == 'RAW_GEOMETRY_NOT_COMPARABLE')
    multi = copy.deepcopy(b)
    extra = copy.deepcopy(multi['sources'][0])
    extra.update(allocation_id='allocation-3', map_entry_id='map-entry-3', holder_id='holder-3', owning_grid='grid-2')
    extra['geometry']['source']['key'] = '1:300:400:00000003'
    multi['sources'].append(extra)
    reseal(multi)
    check('multiple populations including unrelated resident retained', len(snapshot.validate(multi)['sources']) == 3)
    empty = copy.deepcopy(b)
    empty['sources'][0]['geometry']['population'] = []
    empty['sources'][0]['geometry']['capture'].update(resource_slots=0, region_total=0, point_total=0)
    reseal(empty)
    check('represented empty collection valid but no geographical absence', snapshot.compare(a, empty)['sources'][0]['status'] == 'DIFFERENT_REPRESENTED_BYTES')
    fourth = copy.deepcopy(a)
    fourth['capture_id'] = str(uuid.uuid4())
    fourth['sources'][0]['geometry']['snapshot_id'] = fourth['capture_id']
    region = fourth['sources'][0]['geometry']['population'][0]['regions'][0]
    region['points'] = region['points'][:24] + '0000a040' + region['points'][32:]
    reseal(fourth)
    check('fourth point word preserved in equality', snapshot.compare(a, fourth)['sources'][0]['status'] == 'DIFFERENT_REPRESENTED_BYTES')
    check('field-level fourth-word diagnostic', snapshot.compare(a, fourth)['sources'][0]['first_semantic_field_difference']['word'] == 3)
    refuses('failed write path', lambda: snapshot.publish(fixture(), out / 'absent'))
    partial_value = fixture()
    partial_name = partial_value['utc'].replace('-', '').replace(':', '') + '_' + partial_value['session_id'] + '_' + partial_value['capture_id'] + '.partial'
    (out / partial_name).write_bytes(b'crash-prefix')
    refuses('existing crash partial cannot be recycled', lambda: snapshot.publish(partial_value, out))
    check('crash partial retained', (out / partial_name).read_bytes() == b'crash-prefix')
    failed_flush = fixture()
    failed_name = failed_flush['utc'].replace('-', '').replace(':', '') + '_' + failed_flush['session_id'] + '_' + failed_flush['capture_id']
    original_fsync = snapshot.os.fsync
    def injected_fsync_failure(fd):
        raise OSError('Injected flush failure on owned fixture')
    try:
        snapshot.os.fsync = injected_fsync_failure
        refuses('injected flush failure', lambda: snapshot.publish(failed_flush, out))
    finally:
        snapshot.os.fsync = original_fsync
    failed_partial = out / (failed_name + '.partial')
    check('flush failure partial retained and no complete file', failed_partial.exists() and not (out / (failed_name + '.snapshot.json')).exists())
    snapshot.validate(json.loads(failed_partial.read_bytes()))
    check('flush-failed partial contains structurally complete valid bytes', True)
    refuses('reader rejects complete unpublished partial', lambda: snapshot.read_snapshot(failed_partial))
    for mode, flags, optimize in [('O', ['-O'], ''), ('OO', ['-OO'], ''), ('inherited', [], '1')]:
        env = dict(os.environ, PYTHONOPTIMIZE=optimize)
        target = out / (mode + '-forbidden.json')
        p = subprocess.run([sys.executable, '-E', '-B', *flags, str(Path(snapshot.__file__)), str(first), '--out', str(target)],
                           env=env, capture_output=True)
        check('optimization refusal no output ' + mode, p.returncode != 0 and not target.exists() and b'without optimization' in p.stderr)
    import d5ar_statistics as stats
    from fractions import Fraction
    check('exact fixed30 PMF sums to one', sum(stats.distribution()) == Fraction(1))
    check('zero outcome exact probability', stats.distribution()[0] == Fraction(6, 7) ** 30)
    check('one outcome exact probability', stats.distribution()[1] == 30 * Fraction(1, 7) * Fraction(6, 7) ** 29)
    check('zero upper confidence boundary', abs(stats.interval(0)[1] - (1 - .025 ** (1 / 30))) < 1e-14)
    for k in range(31):
        low, high = stats.interval(k)
        check('confidence interval contains estimate ' + str(k), 0 <= low <= k / 30 <= high <= 1)
    guards = []
    guard_errors = (
        b'RuntimeError: Use pinned Python -E -B without optimization',
        b'RuntimeError: Optimization forbidden; invoke pinned Python -E -B',
        b'RuntimeError: Pinned Python -E -B required',
        b'RuntimeError: Use pinned Python -E -B',
    )
    for entry in entries:
        for mode in ('O', 'OO', 'inherited'):
            target = out / (entry.stem + '-' + mode + '-forbidden')
            env = dict(os.environ, PYTHONOPTIMIZE='2' if mode == 'inherited' else '')
            command = [sys.executable, '-E', '-B'] + ([] if mode == 'inherited' else ['-' + mode]) + [str(entry), str(target)]
            result = subprocess.run(command, env=env, capture_output=True)
            diagnostic = result.stderr.rstrip().splitlines()
            check('early guard ' + entry.name + ' ' + mode, result.returncode != 0 and
                  bool(diagnostic) and diagnostic[-1] in guard_errors and not result.stdout and not target.exists())
            guards.append(dict(entry=entry.name, mode=mode, exit=result.returncode, no_output=True))
    snapshot.require({str(p.relative_to(root)): snapshot.digest(p.read_bytes()) for p in executed} == source_pins,
                     'Qualification source changed during execution')
    receipt = dict(status='PASS', checks=checks, synthetic_only=True, native_controls='NOT TESTED',
        files=source_pins,
        interpreter=dict(path=sys.executable, version=sys.version, sha256=snapshot.digest(Path(sys.executable).read_bytes())),
        floors=snapshot.guard(), optimization=guards)
    (out / 'qualification.json').write_bytes(snapshot.encoded(receipt) + b'\n')
    print(json.dumps(dict(status='PASS', checks=len(checks), receipt=str(out / 'qualification.json'))))


if __name__ == '__main__':
    main()
