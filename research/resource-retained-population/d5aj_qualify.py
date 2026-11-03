# SPDX-License-Identifier: GPL-3.0-or-later
"""Repeat actual A0 derivations and challenge source-scoped adverse histories.

Reads immutable stopped Episode A and original owned readers. Synthetic controls
change in-memory event/snapshot copies only; no engine execution is implied.
An independent fixed-offset wire walk checks every holder/resource/region/point.
Writes fresh ignored D5AJ receipts and a versioned source lock. Stdlib only;
no process, save, original evidence, analysis database, network or Git mutation.
"""
import sys
if not __debug__ or sys.flags.optimize:
    raise RuntimeError('Use Python -E -B')
import argparse
import copy
import hashlib
import json
from pathlib import Path
import struct
import zlib

from d5ae_baseline import ROOT, guard, sha
from d5aj_audit import SESSION, DLL, NONCE, write
import d5ai_reduce as original
import d5ai_checkpoint as original_checkpoint
import d5aj_reduce as scoped
import d5aj_checkpoint as checkpoint
from d5aj_scope import continuity


def independent_wire(snapshot, events):
    """Walk raw bytes independently of the production reader's Struct objects."""
    raw = (SESSION / 'events.bin').read_bytes()
    for i, event in enumerate(events):
        at = i * 328
        magic, size, low, crc = struct.unpack_from('<IIII', raw, at)
        words = struct.unpack_from('<18Q2i', raw, at + 16)
        names = 'sequence kind invocation parent thread ticks epoch hazards status proc source frame holder a b c d selection'.split()
        if (magic, size, low, crc) != (0x31505253, 312, i + 1, zlib.crc32(raw[at + 16:at + 328])):
            raise AssertionError('Independent core authentication')
        if any(event[name] != value for name, value in zip(names, words[:18])) or event['request'] != list(words[18:]):
            raise AssertionError('Independent core scalar disagreement')
        if event['source_bytes'] != raw[at + 168:at + 280].hex() or event['descriptor'] != raw[at + 280:at + 324].hex():
            raise AssertionError('Independent core payload disagreement')
    raw = (SESSION / 'geometry-1.bin').read_bytes()
    at = 456
    totals = [0, 0, 0]
    normalized = {}
    for holder in snapshot['holders']:
        values = struct.unpack_from('<4Q2I', raw, at)
        at += 40
        if values[0] != holder['source_pointer'] or values[1] != holder['holder_pointer']:
            raise AssertionError('Independent holder pointers')
        # Capacity and occupied count precede the two opaque holder words.
        if values[2] != holder['resource_capacity'] or values[3] != len(holder['resources']):
            raise AssertionError('Independent resource census')
        populations = []
        for resource in holder['resources']:
            formid, reserved, pointer, count, capacity, data = struct.unpack_from('<II4Q', raw, at)
            at += 40
            if (f'{formid:08x}', reserved, pointer, count, capacity, data) != (resource['resource'], 0, resource['collection_pointer'], len(resource['regions']), resource['region_capacity'], resource['region_data']):
                raise AssertionError('Independent resource fields')
            regions = []
            for region in resource['regions']:
                header = raw[at:at + 24]
                count, capacity, data, address = struct.unpack_from('<4Q', raw, at + 24)
                at += 56
                points = raw[at:at + count * 16]
                at += count * 16
                if header.hex() != region['header'] or count != region['count'] or points.hex() != region['points']:
                    raise AssertionError('Independent complete geometry bytes')
                if struct.unpack_from('<I', header, 16)[0] != formid:
                    raise AssertionError('Independent header resource')
                regions.append(header[:21] + struct.pack('<I', count) + points)
                totals[2] += count
            populations.append((formid, b''.join(regions)))
            totals[0] += 1
            totals[1] += len(regions)
        normalized[holder['source_pointer']] = hashlib.sha256(b''.join(struct.pack('<I', k) + v for k, v in sorted(populations))).hexdigest()
    if at != len(raw) or totals != [102, 2984, 7372]:
        raise AssertionError('Independent geometry end/census')
    return dict(core_records=len(events), geometry_bytes=at, resources=totals[0], regions=totals[1], points=totals[2],
                holder_semantic_content_sha256=normalized)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('out', type=Path)
    args = parser.parse_args()
    if not args.out.resolve().is_relative_to(ROOT / '.local-work/d5aj'):
        raise ValueError('Fresh local output required')
    guard()
    args.out.mkdir(parents=True, exist_ok=False)
    immutable_paths = [p for p in SESSION.iterdir() if p.is_file()]
    immutable_paths += [Path(original.__file__), Path(original_checkpoint.__file__),
                        ROOT / 'docs/experiments/resource-retained-population/d5ai-predictions.md',
                        ROOT / 'docs/experiments/resource-retained-population/d5ai-prediction-text-v1.md']
    immutable_before = {str(p): sha(p) for p in immutable_paths}
    tests = []

    def check(name, condition, basis='SYNTHETIC in-memory adverse contract'):
        tests.append(dict(name=name, passed=bool(condition), basis=basis))
        if not condition:
            raise AssertionError(name)

    actual = scoped.inspect(SESSION, DLL, scoped.read_capture.TARGET)
    historical = original.inspect(SESSION, DLL, original.read_capture.TARGET)
    check('original-refusal-unchanged', not historical['observations'] and historical['refused'][0]['reason'] == 'Unidentified occupied holders prevent unique geographical selection or absence', 'ACTUAL immutable stopped capture, frozen method')
    check('one-qualified-A0-no-A1', len(actual['observations']) == 1 and not actual['refused'], 'ACTUAL immutable stopped capture, new method')
    sidecar = scoped.d5ai_read_geometry.read_session(SESSION)
    snapshot = sidecar['snapshots'][0]
    events = actual['events']
    value = actual['observations'][0]
    check('target-complete-content', value['envelope']['capture'] == dict(complete=True, status='OK', resource_slots=3, region_total=78, point_total=180), 'ACTUAL immutable A0')
    independent = independent_wire(snapshot, events)
    check('independent-full-wire-census', independent['core_records'] == 32155, 'INDEPENDENT raw fixed-offset walk')
    prefix = checkpoint.inspect_prefix(SESSION, DLL, 1, NONCE, scoped.read_capture.TARGET, 0x5e0de)
    check('actual-prefix-stopped-content-identical', scoped.normalize(prefix['envelope']) == scoped.normalize(value['envelope']), 'ACTUAL acknowledged prefix vs stopped capture')
    check('checkpoint-grants-no-live-permission', not prefix['permission_to_depart'] and not prefix['live_worker_verified'] and not prefix['complete_session'], 'ACTUAL reader contract')
    try:
        original_checkpoint.inspect_prefix(SESSION, DLL, 1, NONCE, original.read_capture.TARGET, 0x5e0de)
    except ValueError as error:
        check('original-prefix-refusal-reproduced', str(error) == historical['refused'][0]['reason'], 'ACTUAL frozen checkpoint')
    else:
        check('original-prefix-refusal-reproduced', False)
    h = snapshot['header']
    target = value['proof']['source']
    ids = [scoped.source_identity(events, v['source_pointer'], h) for v in snapshot['holders']]
    check('all36-identified-and-geographically-unique', len(ids) == len({i['key'] for i in ids}) == 36, 'ACTUAL all occupied holders')
    check('all36-have9-disjoint-grid-pairs', all(len(i['continuity']['crossed']) == 9 for i in ids), 'ACTUAL complete source intervals')
    all_holder_proofs = []
    for holder, identity in zip(snapshot['holders'], ids):
        generation = scoped.generation(events, identity, holder['holder_pointer'], h)
        check('all-holder-generation-frame-' + str(len(all_holder_proofs) + 1), generation is not None, 'ACTUAL individually joined holder')
        proof = dict(generation=generation, header=h, holder_pointer=holder['holder_pointer'],
                     collection_pointers=[r['collection_pointer'] for r in holder['resources']])
        scoped.qualify_construction(proof, actual['lifetime'])
        all_holder_proofs.append(dict(source=identity, generation=generation,
                                      holder_pointer=holder['holder_pointer'], content_lifetime='QUALIFIED'))
    # Reconcile the entire capture's fences independently of source qualification.
    opened = {}
    epoch = 1
    reason_counts = {}
    for e in sorted((e for e in events if e['kind'] in (10, 11)), key=lambda e: (e['ticks'], e['sequence'])):
        key = e['thread'], e['proc'], e['a']
        if e['status']:
            raise AssertionError('Exceptional global fence')
        epoch += int(e['kind'] == 10 or e['a'] != 0)
        if e['epoch'] != epoch:
            raise AssertionError('Global epoch accounting')
        if e['kind'] == 10:
            if key in opened:
                raise AssertionError('Ambiguous global nesting')
            opened[key] = e
            reason_counts[e['a']] = reason_counts.get(e['a'], 0) + 1
        elif key not in opened or opened.pop(key)['ticks'] >= e['ticks']:
            raise AssertionError('Global pair accounting')
    check('all117-fence-pairs-and232-increments-accounted', not opened and epoch == 233 and sum(reason_counts.values()) == 117, 'ACTUAL entire captured interval')
    reduced = [e for e in events if e['kind'] in (4, 5, 6, 8, 10, 11, 14, 15)]

    def refuse(name, mutate):
        ev = copy.deepcopy(reduced)
        snap = copy.deepcopy(snapshot)
        life = copy.deepcopy(actual['lifetime'])
        mutate(ev, snap, life)
        try:
            envelope, proof = scoped.envelope(snap, ev, actual['session_id'], scoped.read_capture.TARGET)
            proof['lifetime_coverage'] = scoped.d5ai_read_lifetime.qualify_snapshot(snap, life)
            scoped.qualify_construction(proof, life)
        except (ValueError, KeyError):
            check(name, True)
        else:
            check(name, False)

    source = target['source_pointer']
    birth_seq = target['birth_sequence']
    pub_seq = target['publication_sequence']
    find = lambda ev, seq: next(e for e in ev if e['sequence'] == seq)
    fence_seq = target['continuity']['crossed'][0]['begin']
    def field(seq, name, val):
        return lambda ev, sn, li: find(ev, seq).__setitem__(name, val)
    for name, seq, key, val in (
        ('relevant-owning-grid-clear', fence_seq, 'proc', target['owning_grid']),
        ('map-erase-even-unlike-receiver-domain', fence_seq, 'a', 2),
        ('source-retirement', fence_seq, 'a', 4),
        ('broad-reset', fence_seq, 'a', 0),
        ('procgen-destruction', fence_seq, 'a', 1),
        ('owner-replacement', fence_seq, 'a', 5),
        ('whole-manager-reset', fence_seq, 'a', 6),
        ('unknown-fence-origin', fence_seq, 'proc', 0),
        ('exceptional-clear', fence_seq, 'status', 16),
        ('nested-or-overlapping-clear', fence_seq, 'hazards', 2),
        ('ambiguous-callback-order', fence_seq + 1, 'ticks', find(reduced, fence_seq)['ticks']),
        ('unexplained-epoch-change', fence_seq, 'epoch', 1000),
        ('birth-inside-invalidating-scope', birth_seq, 'hazards', 1),
        ('birth-loss-generation', birth_seq, 'd', 1),
        ('contradictory-owner-event', 7481, 'a', 0),
        ('incorrect-generating-output-holder', 7481, 'd', 0),
        ('incorrect-generation-proc', 7481, 'proc', 0),
        ('incorrect-consumed-frame', 7480, 'descriptor', '00' * 44),
        ('source-birth-tied-to-snapshot', birth_seq, 'ticks', h['ticks_begin']),
    ):
        refuse(name, field(seq, key, val))
    refuse('missed-fence-begin', lambda ev, sn, li: ev.remove(find(ev, fence_seq)))
    refuse('missed-fence-end', lambda ev, sn, li: ev.remove(find(ev, fence_seq + 1)))
    refuse('unpublished-target', lambda ev, sn, li: ev.remove(find(ev, pub_seq)))
    refuse('prearming-source', lambda ev, sn, li: ev.remove(find(ev, birth_seq)))
    refuse('duplicate-publication', lambda ev, sn, li: ev.append(copy.deepcopy(find(ev, pub_seq))))
    refuse('duplicate-allocation-token', lambda ev, sn, li: ev.append(copy.deepcopy(find(ev, birth_seq))))
    # Pointer ABA after construction cannot borrow the previous generation frame.
    def aba(ev, sn, li):
        birth = copy.deepcopy(find(ev, birth_seq))
        pub = copy.deepcopy(find(ev, pub_seq))
        birth.update(sequence=90000, selection=90000, ticks=h['ticks_begin'] - 100)
        pub.update(sequence=90001, ticks=h['ticks_begin'] - 90)
        ev.extend([birth, pub])
    refuse('same-source-pointer-free-reallocation-ABA', aba)
    # Two positively identified target-key holders must still refuse uniqueness.
    other = ids[0]
    def collision(ev, sn, li):
        raw = find(ev, birth_seq)['source_bytes']
        a = find(ev, other['birth_sequence'])
        a['source_bytes'] = raw
        a['a'] = target['token']
    refuse('two-genuine-target-key-holders', collision)
    refuse('positive-target-plus-unknown-holder', lambda ev, sn, li: ev.remove(find(ev, other['birth_sequence'])))
    # An absence candidate plus an unknown holder remains inconclusive.
    def absence_unknown(ev, sn, li):
        ev.remove(find(ev, other['birth_sequence']))
        sn['holders'] = [v for v in sn['holders'] if v['source_pointer'] != source]
    refuse('absent-target-with-unknown-holder', absence_unknown)
    refuse('incomplete-capture', lambda ev, sn, li: sn.__setitem__('complete_representation', False))
    refuse('wrong-consumer-owner', lambda ev, sn, li: sn['header'].__setitem__('owner_formid', 1))
    refuse('wrong-consumer-kind', lambda ev, sn, li: sn['header'].__setitem__('boundary', 1))
    refuse('missing-native-consumer-pointer', lambda ev, sn, li: sn['header'].__setitem__('consumer', 0))
    refuse('missing-native-manager-pointer', lambda ev, sn, li: sn['header'].__setitem__('manager', 0))
    refuse('missing-native-procgen-pointer', lambda ev, sn, li: sn['header'].__setitem__('proc', 0))
    refuse('incomplete-native-consumer-scan', lambda ev, sn, li: sn['header'].__setitem__('scan_result', 0))
    refuse('capture-loss', lambda ev, sn, li: sn['header'].__setitem__('loss', 1))
    refuse('nonfinite-consumer-query', lambda ev, sn, li: sn['header'].__setitem__('query_hex', '0000c07f' + sn['header']['query_hex'][8:]))
    refuse('lifetime-journal-cutoff', lambda ev, sn, li: li.__setitem__('qualified_from_ticks', h['ticks_begin']))
    def content_event(kind, allocation):
        def mutate(ev, sn, li):
            begin = dict(li['events'][0], kind=kind, allocation=allocation, phase='BEGIN',
                         invocation=999999, thread=999999, ticks=h['ticks_begin'] - 10)
            li['events'].extend([begin, dict(begin, phase='END', ticks=h['ticks_begin'] - 5)])
        return mutate
    refuse('holder-resource-map-ending', content_event('HOLDER_RESOURCE_MAP', value['proof']['holder_pointer']))
    refuse('collection-content-ending', content_event('COLLECTION_GEOMETRY', value['proof']['collection_pointers'][0]))
    refuse('collection-content-mutation', content_event('COLLECTION_MUTATION', value['proof']['collection_pointers'][0]))
    # A token collision alone cannot relabel geography: identity comes from bytes.
    collision_events = copy.deepcopy(reduced)
    find(collision_events, other['birth_sequence'])['a'] = target['token']
    # Keep constructor bytes internally consistent while leaving geographical fields.
    raw = bytearray.fromhex(find(collision_events, other['birth_sequence'])['source_bytes'])
    struct.pack_into('<Q', raw, 0x68, target['token'])
    find(collision_events, other['birth_sequence'])['source_bytes'] = raw.hex()
    token_identity = scoped.source_identity(collision_events, other['source_pointer'], h)
    check('equal-token-does-not-conflate-geography', token_identity['key'] == other['key'] and token_identity['key'] != target['key'])
    # Same geography under another ProcGen cannot certify this output holder.
    refuse('same-geography-other-procgen-owner', field(7481, 'proc', h['proc'] + 0x1000))
    # Complete but empty/partial represented output retains UNKNOWN native quality.
    empty = copy.deepcopy(snapshot)
    chosen = next(v for v in empty['holders'] if v['source_pointer'] == source)
    chosen['resources'] = []
    ev, _ = scoped.envelope(empty, reduced, actual['session_id'], scoped.read_capture.TARGET)
    check('represented-empty-does-not-claim-successful-generation', ev['generation_quality'] == 'UNKNOWN' and ev['capture']['point_total'] == 0)
    # The decoder, not a plausible envelope, guards recorded structural counts.
    data = (SESSION / 'geometry-1.bin').read_bytes()
    for name, raw in [('truncated-point-array', data[:-1]), ('incorrect-header-census', data[:112] + struct.pack('<Q', 9999) + data[120:])]:
        try:
            scoped.d5ai_read_geometry.decode(raw)
        except ValueError:
            check(name, True)
        else:
            check(name, False)
    # Re-read retained authentic disposable native outputs with the exact new
    # reducer. These are native fixture records, never new retail observations.
    build = ROOT / '.local-work/d5ai-recorder/build16'
    fixture_dll = sha(build / 'SorConstructionWinner.dll')
    fixture_cases = {}
    for case in ('d5ai-retained', 'd5ai-rebuilt-equal', 'd5ai-rebuilt-different',
                 'd5ai-unavailable', 'd5ai-life-aba', 'd5ai-life-mutation',
                 'd5ai-life-external-holder', 'd5ai-life-external-collection',
                 'd5ai-life-final', 'd5ai-life-partial'):
        current = scoped.inspect(build / case, fixture_dll, scoped.read_capture.TARGET)
        prior = original.inspect(build / case, fixture_dll, original.read_capture.TARGET)
        check('retained-native-fixture-regression-' + case,
              len(current['observations']) == len(prior['observations']) and current['refused'] == prior['refused'],
              'REPLAY authenticated native fixture bytes; no new native execution')
        comparison = None
        if len(current['observations']) == 2:
            a, b = current['observations']
            cert = scoped.relation(a, b, current['events'], current['events'], current['lifetime'])
            comparison = scoped.compare(a['envelope'], b['envelope'], cert)
            old_cert = original.relation(*prior['observations'], prior['events'], prior['events'], prior['lifetime'])
            check('retained-native-comparison-regression-' + case,
                  comparison['outcome'] == original.compare(prior['observations'][0]['envelope'], prior['observations'][1]['envelope'], old_cert)['outcome'],
                  'REPLAY native fixture bytes with original/new relation')
        fixture_cases[case] = dict(refused=current['refused'], observations=len(current['observations']), comparison=comparison)
    retained = scoped.inspect(build / 'd5ai-retained', fixture_dll, scoped.read_capture.TARGET)
    a, b = copy.deepcopy(retained['observations'])
    after_snapshot = copy.deepcopy(scoped.d5ai_read_geometry.read_session(build / 'd5ai-retained')['snapshots'][1])
    synthetic_events = copy.deepcopy(retained['events'])
    low = a['proof']['header']['completion_ticks']
    high = b['proof']['header']['ticks_begin']
    if high - low < 50:
        raise AssertionError('Native fixture has no counterfactual interval')
    epoch = a['proof']['header']['epoch']
    grid = a['proof']['source']['owning_grid']
    base = max(e['sequence'] for e in synthetic_events)
    template = next(e for e in events if e['kind'] == 10)
    for i in range(18):
        synthetic_events.append(dict(template, kind=10 if i % 2 == 0 else 11, a=3, proc=grid + 0x1000,
                                     epoch=epoch + i + 1, ticks=low + i + 1, sequence=base + i + 1,
                                     status=0, hazards=1 if i % 2 == 0 else 0, thread=999))
    after_snapshot['header']['epoch'] += 18
    after_snapshot['header']['completion_epoch'] += 18
    ev, proof = scoped.envelope(after_snapshot, synthetic_events, b['envelope']['session_id'], scoped.read_capture.TARGET)
    proof['lifetime_coverage'] = scoped.d5ai_read_lifetime.qualify_snapshot(after_snapshot, retained['lifetime'])
    proof['process_identity'] = b['proof']['process_identity']
    scoped.qualify_construction(proof, retained['lifetime'])
    modeled_b = dict(envelope=ev, proof=proof)
    cert = scoped.relation(a, modeled_b, synthetic_events, synthetic_events, retained['lifetime'])
    check('future-retention-across-nine-disjoint-Grid-clears', scoped.compare(a['envelope'], ev, cert)['outcome'] == 'RETAINED',
          'SYNTHETIC nine-fence extension of native retained fixture; not an A1')
    relevant = copy.deepcopy(synthetic_events)
    next(e for e in relevant if e['sequence'] == base + 1)['proc'] = grid
    cert = scoped.relation(a, modeled_b, relevant, relevant, retained['lifetime'])
    check('future-retention-refuses-relevant-Grid-clear', not cert['qualified'])
    source_paths = [Path(checkpoint.__file__), Path(scoped.__file__), ROOT / 'research/resource-retained-population/d5aj_scope.py']
    source_paths += [ROOT / 'research/resource-retained-population' / n for n in ('d5ai_geometry.py', 'd5ai_lifetime.py', 'd5ae_baseline.py')]
    source_paths += [ROOT / 'runtime/construction-winner' / n for n in ('read_capture.py', 'reduce_v3.py', 'reduce_v4.py', 'd5ai_read_geometry.py', 'd5ai_read_lifetime.py')]
    lock = dict(schema='sor-d5aj-source-lock/1', repository_root=str(ROOT), dll_sha256=DLL,
                interpreter_sha256=sha(sys.executable), sources={str(p.resolve()): sha(p) for p in source_paths})
    write(args.out / 'source-lock.json', lock)
    checkpoint.verify_source_lock(args.out / 'source-lock.json', sha(args.out / 'source-lock.json'), DLL)
    check('exact-versioned-source-lock-closure', True, 'ACTUAL source/interpreter/producer hashes')
    from d5aj_gates import GATES, assess
    gate_rows = [assess(g, s) for g in GATES for s in ('PASS', 'FAIL', 'PENDING')]
    for row in gate_rows:
        response = row['proposed_response']
        valid = not row['permission_to_act'] and row['preserve_evidence'] and row['exclusive_operator_stop']
        if row['state'] == 'PENDING':
            valid = valid and response == 'WAIT_FOR_EVIDENCE'
        elif row['state'] == 'PASS':
            valid = valid and response == 'CONTINUE_WITHIN_APPROVED_ACTIONS'
        elif row['category'] in ('SAFETY', 'INTEGRITY'):
            valid = valid and response in ('STOP', 'HOLD_ADMISSION')
        else:
            valid = valid and response not in ('STOP', 'HOLD_ADMISSION')
        check('policy-no-authority-and-purpose-consistent-' + row['gate'] + '-' + row['state'], valid, 'OFFLINE proposed gate oracle, not controller execution')
    check('policy-departure-still-requires-baseline', assess('baseline_prefix_qualified', 'FAIL')['proposed_response'] == 'HOLD_DEPARTURE')
    check('policy-query-still-requires-arm-ACK', assess('geometry_arm_ack', 'FAIL')['proposed_response'] == 'HOLD_QUERY')
    check('policy-ordinary-fence-is-scientific-qualification', assess('global_epoch_changed', 'FAIL')['proposed_response'] == 'QUALIFY_SOURCE_SCOPE')
    immutable_after = {str(p): sha(p) for p in immutable_paths}
    check('immutable-input-bytes-unchanged', immutable_before == immutable_after, 'ACTUAL before/after SHA-256 of original session, methods and predictions')
    write(args.out / 'qualification.json', dict(method=scoped.METHOD, tests=tests, passed=len(tests),
          independent=independent, global_fence_pairs=reason_counts, original_refusal=historical['refused'], fixture_cases=fixture_cases,
          all_holder_proofs=all_holder_proofs,
          gate_rows=gate_rows,
          scoped_observation=value, prefix=prefix, source_lock_sha256=sha(args.out / 'source-lock.json'),
          method_sha256=sha(__file__), inputs_unchanged=immutable_before == immutable_after, immutable_inputs=immutable_after,
          source_hashes={str(Path(m.__file__).resolve()): sha(m.__file__) for m in (scoped, checkpoint, original, original_checkpoint)}))
    print(json.dumps(dict(passed=len(tests), method=scoped.METHOD, out=str(args.out))))


if __name__ == '__main__':
    main()
