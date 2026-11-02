# SPDX-License-Identifier: GPL-3.0-or-later
"""Challenge native snapshot joins using authenticated disposable-host evidence.

Reads a supplied native build/session and checks DLL bytes against build receipts.
Creates exclusive local derivative receipts only. In-memory mutations are labelled
synthetic adversaries, never new native observations. No native execution, game,
save, database, network or Git operations. Requires Python -E -B; preserves inputs.
"""
import sys
if not __debug__ or sys.flags.optimize:
    raise RuntimeError('Use Python -E -B')

import argparse
import copy
import json
from pathlib import Path

from d5ae_baseline import guard, sha
from d5ai_geometry import compare
import d5ai_reduce as reducer


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('build', type=Path)
    parser.add_argument('out', type=Path)
    args = parser.parse_args()
    guard()
    if not args.out.resolve().is_relative_to(reducer.ROOT / '.local-work/d5ai'):
        raise ValueError('Task-local output required')
    args.out.mkdir(exist_ok=False)
    build = reducer.load(args.build / 'build.json')
    dll = args.build / 'SorConstructionWinner.dll'
    digest = sha(dll)
    if (digest not in build['outputs'].values() or build['source_unchanged'] is not True or
            not all(row['pass_exit'] for row in build['cases'])):
        raise ValueError('DLL/build correspondence failed')
    session = args.build / 'd5ai-retained'
    result = reducer.inspect(session, digest, reducer.read_capture.TARGET)
    raw_snapshot = reducer.d5ai_read_geometry.read_session(session)['snapshots'][0]
    events = result['events']
    original = result['observations'][0]
    selected_birth = original['proof']['source']['birth_sequence']
    selected_publication = original['proof']['source']['publication_sequence']
    tests = []

    def check(name, condition):
        tests.append(dict(name=name, passed=bool(condition)))
        if not condition:
            raise AssertionError(name)

    check('actual-native-positive-target-envelope', original['envelope']['availability']['holder_present'])

    def refused(name, snapshot, altered):
        try:
            reducer.envelope(snapshot, altered, result['session_id'], reducer.read_capture.TARGET)
        except ValueError:
            check(name, True)
        else:
            check(name, False)

    for kind, name in ((14, 'missing-birth'), (15, 'missing-publication')):
        refused(name, raw_snapshot, [e for e in events if e['kind'] != kind])
    for name in ('birth-status', 'birth-epoch', 'birth-loss', 'wrong-token', 'late-publication',
                 'duplicate-birth-serial', 'fence-during-snapshot'):
        altered = copy.deepcopy(events)
        birth = next(e for e in altered if e['sequence'] == selected_birth)
        pub = next(e for e in altered if e['sequence'] == selected_publication)
        if name == 'birth-status': birth['status'] = 1
        elif name == 'birth-epoch': birth['epoch'] += 1
        elif name == 'birth-loss': birth['d'] += 1
        elif name == 'wrong-token': birth['a'] += 1
        elif name == 'late-publication': pub['ticks'] = raw_snapshot['header']['ticks_end']
        elif name == 'duplicate-birth-serial': altered.append(dict(birth, source=birth['source'] + 0x1000, sequence=999))
        elif name == 'fence-during-snapshot': altered.append(dict(pub, kind=10, ticks=raw_snapshot['header']['ticks_begin'], a=1))
        refused(name, raw_snapshot, altered)
    for reverse in (False, True):
        snapshot = copy.deepcopy(raw_snapshot)
        altered = copy.deepcopy(events)
        birth = next(e for e in altered if e['sequence'] == selected_birth)
        pub = next(e for e in altered if e['sequence'] == selected_publication)
        new_source = birth['source'] + 0x10000
        altered.extend([dict(birth, source=new_source, selection=birth['selection'] + 1000, sequence=1000),
                        dict(pub, source=new_source, sequence=1001)])
        duplicate = copy.deepcopy(snapshot['holders'][0])
        duplicate['source_pointer'] = new_source
        duplicate['holder_pointer'] += 0x1000
        snapshot['holders'].append(duplicate)
        if reverse:
            snapshot['holders'].reverse()
        refused('duplicate-qualified-geography-order-' + str(reverse), snapshot, altered)
    snapshot = copy.deepcopy(raw_snapshot)
    snapshot['header']['owner_formid'] += 1
    refused('wrong-body-context', snapshot, events)
    snapshot = copy.deepcopy(raw_snapshot)
    snapshot['holders'] = []
    value, proof = reducer.envelope(snapshot, events, result['session_id'], reducer.read_capture.TARGET)
    absent = dict(envelope=value, proof=proof)
    certificate = reducer.relation(original, absent, events, events, result['lifetime'])
    check('complete-empty-map-unavailable-without-generation',
          compare(original['envelope'], value, certificate)['outcome'] == 'UNAVAILABLE')
    snapshot = copy.deepcopy(raw_snapshot)
    snapshot['holders'][0]['source_pointer'] += 0x10000
    refused('unknown-holder-is-not-absence', snapshot, events)
    for reverse in (False, True):
        snapshot = copy.deepcopy(raw_snapshot)
        unknown_holder = copy.deepcopy(snapshot['holders'][0])
        unknown_holder['source_pointer'] += 0x10000
        snapshot['holders'].append(unknown_holder)
        if reverse:
            snapshot['holders'].reverse()
        refused('unknown-holder-prevents-unique-target-' + str(reverse), snapshot, events)
    # Explicitly synthetic later boundary; original native execution supplies
    # the independent initialized bytes, but this is not a second native visit.
    second = copy.deepcopy(original)
    second['envelope']['snapshot_id'] = 'synthetic-later'
    second['proof']['header']['ticks_begin'] = raw_snapshot['header']['completion_ticks'] + 10
    second['proof']['header']['completion_ticks'] += 20
    certificate = reducer.relation(original, second, events, events, result['lifetime'])
    check('continuous-history-certificate', certificate['qualified'] and certificate['relation'] == 'CONTINUOUS')
    check('continuous-equal-representation', compare(original['envelope'], second['envelope'], certificate)['outcome'] == 'RETAINED')
    interrupted = copy.deepcopy(events)
    interrupted.append(dict(interrupted[0], kind=10, ticks=raw_snapshot['header']['completion_ticks'] + 1))
    check('retention-gap-fence-refused', not reducer.relation(original, second, interrupted, interrupted, result['lifetime'])['qualified'])
    second['proof']['holder_pointer'] += 0x1000
    check('different-pointer-without-construction-refused', not reducer.relation(original, second, events, events, result['lifetime'])['qualified'])
    for name in ('return-descriptor', 'zero-invocation', 'zero-selection'):
        altered = copy.deepcopy(events)
        proof = original['proof']['generation']
        g = next(e for e in altered if e['sequence'] == proof['generate_sequence'])
        if name == 'return-descriptor':
            returned = next(e for e in altered if e['sequence'] == proof['return_sequence'])
            returned['descriptor'] = '01' + returned['descriptor'][2:]
        else:
            key = 'invocation' if name == 'zero-invocation' else 'selection'
            for event in altered:
                if event['invocation'] == proof['invocation'] and event['selection'] == proof['selection']:
                    event[key] = 0
        check('generation-context-' + name, reducer.generation(altered, original['proof']['source'],
              original['proof']['holder_pointer'], raw_snapshot['header']) is None)
    for reason in (0, 1, 5, 6):
        altered = copy.deepcopy(events)
        altered.append(dict(altered[0], kind=10, a=reason, ticks=raw_snapshot['header']['ticks_begin'] - 1))
        try:
            reducer.owner_context(altered, raw_snapshot['header'], 0x5e0de)
        except ValueError:
            check('owner-changing-fence-refused-' + str(reason), True)
        else:
            check('owner-changing-fence-refused-' + str(reason), False)
    # Synthetic epoch/fence histories anchored to one actual native generation.
    # This isolates owner carry from unrelated later generations; it is not a
    # fabricated native return or a second gameplay observation.
    generating = next(e for e in events if e['sequence'] == original['proof']['generation']['generate_sequence'])
    returned = next(e for e in events if e['kind'] == 8 and e['invocation'] == generating['invocation'])
    anchor = [copy.deepcopy(generating), copy.deepcopy(returned)]
    synthetic_header = copy.deepcopy(raw_snapshot['header'])
    synthetic_header.update(ticks_begin=returned['ticks'] + 100,
                            completion_ticks=returned['ticks'] + 200,
                            epoch=generating['epoch'] + 2)

    def carry_refused(name, history, header):
        try:
            reducer.owner_context(history, header, 0x5e0de)
        except ValueError:
            check(name, True)
        else:
            check(name, False)

    for reason in (2, 3, 4):
        begin = dict(generating, kind=10, a=reason, ticks=returned['ticks'] + 10,
                     epoch=generating['epoch'] + 1, sequence=10000)
        end = dict(begin, kind=11, ticks=returned['ticks'] + 20,
                   epoch=generating['epoch'] + 2, sequence=10001)
        history = anchor + [begin, end]
        check('paired-owner-preserving-fence-' + str(reason),
              reducer.owner_context(history, synthetic_header, 0x5e0de)['owner_formid'] == '0005e0de')
        carry_refused('missing-fence-begin-' + str(reason), anchor + [end], synthetic_header)
        carry_refused('missing-fence-end-' + str(reason), anchor + [begin], synthetic_header)
        carry_refused('wrong-fence-receiver-' + str(reason),
                      anchor + [begin, dict(end, proc=end['proc'] + 8)], synthetic_header)
        carry_refused('collapsed-fence-timestamp-' + str(reason),
                      anchor + [begin, dict(end, ticks=begin['ticks'])], synthetic_header)
    carry_refused('unexplained-owner-epoch', anchor, synthetic_header)
    outcomes = {}
    for label, expected in (('retained', 'RETAINED'), ('rebuilt-equal', 'REBUILT_IDENTICAL'),
                            ('rebuilt-different', 'REBUILT_DIFFERENT'), ('unavailable', 'UNAVAILABLE')):
        native = reducer.inspect(args.build / ('d5ai-' + label), digest, reducer.read_capture.TARGET)
        check('native-qualified-pair-' + label, len(native['observations']) == 2)
        before, after = native['observations']
        certificate = reducer.relation(before, after, native['events'], native['events'], native['lifetime'])
        verdict = compare(before['envelope'], after['envelope'], certificate)
        check('native-four-outcome-' + label, verdict['outcome'] == expected)
        outcomes[label] = verdict
    output = dict(tests=tests, passed=len(tests), outcomes=outcomes, build_sha256=sha(args.build / 'build.json'),
                  dll_sha256=digest, lifecycle_sha256=result['lifecycle_raw_sha256'],
                  native_snapshot_sha256=original['raw_sha256'], method_sha256=sha(__file__),
                  reducer_sha256=sha(Path(reducer.__file__)),
                  distinction='One actual native positive; remaining named mutated histories are synthetic adversaries')
    (args.out / 'receipt.json').write_text(json.dumps(output, indent=2) + '\n', encoding='utf8', newline='\n')
    for method in (Path(__file__), Path(reducer.__file__)):
        (args.out / method.name).write_bytes(method.read_bytes())
    print(json.dumps(dict(passed=len(tests))))


if __name__ == '__main__':
    main()
