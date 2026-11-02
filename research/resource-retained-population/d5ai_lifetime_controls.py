# SPDX-License-Identifier: GPL-3.0-or-later
"""Challenge final native recorder lifetime evidence and synthetic counterexamples.

Reads explicitly pinned disposable-host build/session files; writes fresh local
receipts only. No native execution, process, save, network or Git operations.
Mutated histories/graphs are synthetic adversaries, never native observations.
The positive cases must come from actual final recorder hooks and worker output.
"""
import argparse
import copy
import json
from pathlib import Path
import sys

from d5ae_baseline import guard, sha
import d5ai_reduce as reducer
from d5ai_lifetime import evaluate


def main():
    if not __debug__ or sys.flags.optimize:
        raise RuntimeError('Use Python -E -B')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('build', type=Path)
    parser.add_argument('out', type=Path)
    args = parser.parse_args()
    guard()
    if not args.out.resolve().is_relative_to(reducer.ROOT / '.local-work/d5ai'):
        raise ValueError('Task-local fresh output required')
    args.out.mkdir(exist_ok=False)
    build = reducer.load(args.build / 'build.json')
    digest = sha(args.build / 'SorConstructionWinner.dll')
    if (digest not in build['outputs'].values() or build['source_unchanged'] is not True or
            not all(row['pass_exit'] for row in build['cases'])):
        raise ValueError('Exact qualified native build required')
    tests, cases = [], {}

    def check(name, condition):
        tests.append(dict(name=name, passed=bool(condition)))
        (args.out / 'attempt.json').write_text(json.dumps(dict(tests=tests), indent=2) + '\n',
                                              encoding='utf8', newline='\n')
        if not condition:
            raise AssertionError(name)

    expected = {
        'external-holder': ('COMPLETE_COLLECTION_GEOMETRY_SURVIVES', 'SURVIVES'),
        'external-collection': ('COMPLETE_COLLECTION_GEOMETRY_SURVIVES', 'ENDED'),
        'final': ('PRIOR_COLLECTION_GEOMETRY_ENDED', 'ENDED'),
        'partial': ('PARTIAL_COLLECTION_GEOMETRY_SURVIVES', 'ENDED'),
        'aba': ('PRIOR_COLLECTION_GEOMETRY_ENDED', 'ENDED'),
        'empty-null': ('EMPTY_CONTENT_LIFETIMES_SURVIVE', 'SURVIVES'),
        'empty-spare': ('COMPLETE_COLLECTION_GEOMETRY_SURVIVES', 'SURVIVES'),
    }
    for label, (state, holder_state) in expected.items():
        native = reducer.inspect(args.build / ('d5ai-life-' + label), digest, reducer.read_capture.TARGET)
        check('actual-native-pair-' + label, len(native['observations']) == 2)
        before, after = native['observations']
        verdict = evaluate(before, after, native['lifetime'])
        check('actual-native-storage-' + label, verdict['qualified'] and verdict['state'] == state)
        check('actual-native-holder-' + label, verdict['holder']['state'] == holder_state)
        if label != 'aba':
            check('actual-consumer-unavailable-' + label,
                  after['envelope']['availability']['exposed'] is False)
        cases[label] = dict(storage=verdict, before=before, after=after,
                            lifetime_prefix_sha256=native['lifetime']['raw_prefix_sha256'])
    native = reducer.inspect(args.build / 'd5ai-retained', digest, reducer.read_capture.TARGET)
    before, after = native['observations']
    journal = native['lifetime']
    mutation = reducer.inspect(args.build / 'd5ai-life-mutation', digest, reducer.read_capture.TARGET)
    check('actual-native-mutation-does-not-prove-storage-free',
          evaluate(*mutation['observations'], mutation['lifetime'])['state'] == 'UNKNOWN')
    check('actual-native-present-storage-survives', evaluate(before, after, journal)['qualified'])
    check('retention-needs-positive-journal', not reducer.relation(before, after, native['events'], native['events'])['qualified'])
    for label in ('late-onset', 'loss', 'incomplete', 'wrong-session', 'short-watermark'):
        altered = copy.deepcopy(journal)
        if label == 'late-onset': altered['qualified_from_ticks'] = before['proof']['header']['ticks_begin'] + 1
        elif label == 'loss': altered['loss'] = 1
        elif label == 'incomplete': altered['complete'] = False
        elif label == 'wrong-session': altered['session_id'] = 'foreign'
        elif label == 'short-watermark': altered['qualified_through_ticks'] = after['proof']['header']['completion_ticks'] - 1
        check('synthetic-journal-refused-' + label, not evaluate(before, after, altered)['qualified'])
    shortened = copy.deepcopy(before)
    shortened['proof']['collection_pointers'].pop()
    shortened['proof']['collection_graph'].pop()
    check('synthetic-shortened-baseline-graph-refused', not evaluate(shortened, after, journal)['qualified'])
    empty = reducer.inspect(args.build / 'd5ai-life-empty-null', digest, reducer.read_capture.TARGET)
    empty_before, empty_after = empty['observations']
    alias = copy.deepcopy(empty_before)
    new_resource = f"{int(alias['envelope']['population'][0]['resource'], 16) + 1:08x}"
    alias['envelope']['population'].append(dict(resource=new_resource, regions=[]))
    alias['envelope']['capture']['resource_slots'] += 1
    alias['proof']['collection_pointers'].append(alias['proof']['collection_pointers'][0])
    alias['proof']['collection_graph'].append(dict(copy.deepcopy(alias['proof']['collection_graph'][0]), resource=new_resource))
    check('synthetic-identical-empty-alias-qualified', evaluate(alias, empty_after, empty['lifetime'])['qualified'])
    alias['proof']['collection_graph'][-1].update(region_capacity=1, region_data=0x100000)
    check('synthetic-contradictory-empty-alias-refused', not evaluate(alias, empty_after, empty['lifetime'])['qualified'])
    bad_region = copy.deepcopy(empty_before)
    bad_region['proof']['collection_graph'][0]['region_data'] = 0x100000
    check('synthetic-zero-capacity-nonnull-region-is-unknown',
          not evaluate(bad_region, empty_after, empty['lifetime'])['qualified'])
    bad_point = copy.deepcopy(before)
    first_region = bad_point['envelope']['population'][0]['regions'][0]
    old_count = first_region['count']
    first_region.update(count=0, points='')
    bad_point['envelope']['capture']['point_total'] -= old_count
    bad_point['proof']['collection_graph'][0]['regions'][0].update(count=0, point_capacity=0, point_data=0x100000)
    check('synthetic-zero-capacity-nonnull-point-is-unknown', not evaluate(bad_point, after, journal)['qualified'])
    partial_native = reducer.inspect(args.build / 'd5ai-life-partial', digest, reducer.read_capture.TARGET)
    mixed, mixed_after = copy.deepcopy(partial_native['observations'])
    actual_partial = evaluate(mixed, mixed_after, partial_native['lifetime'])
    survivor = next(c['allocation'] for c in actual_partial['collections'] if c['state'] == 'SURVIVES')
    graph_row = next(r for r in mixed['proof']['collection_graph'] if r['collection_pointer'] == survivor)
    semantic_row = next(r for r in mixed['envelope']['population'] if r['resource'] == graph_row['resource'])
    mixed['envelope']['capture']['region_total'] -= len(semantic_row['regions'])
    mixed['envelope']['capture']['point_total'] -= sum(r['count'] for r in semantic_row['regions'])
    semantic_row['regions'] = []
    graph_row.update(region_capacity=0, region_data=0, regions=[])
    mixed_result = evaluate(mixed, mixed_after, partial_native['lifetime'])
    check('synthetic-only-null-empty-survivor-does-not-prove-backing',
          mixed_result['state'] == 'ONLY_EMPTY_CONTENT_LIFETIMES_SURVIVE' and
          mixed_result['census']['surviving_with_nested_backing'] == 0)
    graph_row.update(region_capacity=1, region_data=0x100000)
    spare_result = evaluate(mixed, mixed_after, partial_native['lifetime'])
    check('synthetic-spare-empty-survivor-preserves-backing-distinction',
          spare_result['state'] == 'PARTIAL_COLLECTION_GEOMETRY_SURVIVES' and
          spare_result['census']['surviving_with_nested_backing'] == 1)
    # Challenge first-snapshot frame attribution independently of later retention.
    # These are synthetic overlays on authentic joined construction operands.
    construction = before['proof']['generation']
    for label in ('holder-ending', 'collection-ending', 'mutation', 'late-construction-coverage'):
        altered = copy.deepcopy(journal)
        if label == 'late-construction-coverage':
            altered['qualified_from_ticks'] = construction['return_ticks'] + 1
        else:
            kind = {'holder-ending': 'HOLDER_RESOURCE_MAP', 'collection-ending': 'COLLECTION_GEOMETRY',
                    'mutation': 'COLLECTION_MUTATION'}[label]
            pointer = before['proof']['holder_pointer'] if label == 'holder-ending' else before['proof']['collection_pointers'][0]
            altered['events'].append(dict(kind=kind, phase='BEGIN', allocation=pointer,
                                          thread=1, invocation=999999, ticks=construction['return_ticks']))
        try:
            reducer.qualify_construction(before['proof'], altered)
        except ValueError:
            check('synthetic-stale-construction-frame-refused-' + label, True)
        else:
            check('synthetic-stale-construction-frame-refused-' + label, False)
    for kind in ('HOLDER_RESOURCE_MAP', 'COLLECTION_GEOMETRY', 'COLLECTION_MUTATION'):
        pointer = before['proof']['holder_pointer'] if kind == 'HOLDER_RESOURCE_MAP' else before['proof']['collection_pointers'][0]
        begin = dict(kind=kind, phase='BEGIN', allocation=pointer, thread=1, invocation=999998,
                     ticks=construction['return_ticks'] - 2)
        for offset, should_pass in ((-1, True), (0, False), (1, False)):
            altered = copy.deepcopy(journal)
            altered['events'].extend([begin, dict(begin, phase='END', ticks=construction['return_ticks'] + offset)])
            try:
                reducer.qualify_construction(before['proof'], altered)
            except ValueError:
                check('synthetic-construction-interval-' + kind + '-' + str(offset), not should_pass)
            else:
                check('synthetic-construction-interval-' + kind + '-' + str(offset), should_pass)
    # Use an authentic ending pair, then move its END exactly onto completion.
    native_end = reducer.inspect(args.build / 'd5ai-life-final', digest, reducer.read_capture.TARGET)
    a, b = native_end['observations']
    missing = copy.deepcopy(native_end['lifetime'])
    check('native-journal-nonempty-for-gap-adversary', bool(missing['events']))
    missing['events'].pop(0)
    check('synthetic-missing-sequence-refused', not evaluate(a, b, missing)['qualified'])
    exceptional = copy.deepcopy(native_end['lifetime'])
    next(e for e in exceptional['events'] if e['phase'] == 'END')['status'] = 16
    check('synthetic-exceptional-ending-is-unknown', not evaluate(a, b, exceptional)['qualified'])
    tied = copy.deepcopy(native_end['lifetime'])
    pointer = a['proof']['holder_pointer']
    ending = next(e for e in tied['events'] if e['kind'] == 'HOLDER_RESOURCE_MAP' and
                  e['phase'] == 'END' and e['allocation'] == pointer and e['ticks'] > a['proof']['header']['ticks_end'])
    ending['ticks'] = b['proof']['header']['completion_ticks']
    check('synthetic-end-tied-to-completion-refused', not evaluate(a, b, tied)['qualified'])
    output = dict(tests=tests, passed=len(tests), native_cases=cases, dll_sha256=digest,
                  build_sha256=sha(args.build / 'build.json'), method_sha256=sha(__file__),
                  evaluator_sha256=sha(reducer.d5ai_lifetime.__file__),
                  reader_sha256=sha(reducer.d5ai_read_lifetime.__file__))
    (args.out / 'receipt.json').write_text(json.dumps(output, indent=2) + '\n', encoding='utf8', newline='\n')
    for path in (Path(__file__), Path(reducer.d5ai_lifetime.__file__), Path(reducer.d5ai_read_lifetime.__file__)):
        (args.out / path.name).write_bytes(path.read_bytes())
    print(json.dumps(dict(passed=len(tests))))


if __name__ == '__main__':
    main()
