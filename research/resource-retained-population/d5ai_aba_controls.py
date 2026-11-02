# SPDX-License-Identifier: GPL-3.0-or-later
"""Qualify irreversible baseline ending before later same-address mutation.

Reads a separately pinned fixture-only derivative with unchanged production
sources and retained worker objects; never executes a target. Actual combined
native evidence and explicitly synthetic order/exception/loss models are separate.
Writes fresh private receipts only; no game, save, network or Git mutation.
"""
import argparse
import copy
import json
from pathlib import Path
import sys

from d5ae_baseline import guard, sha
import d5ai_reduce as reducer


def main():
    if not __debug__ or sys.flags.optimize:
        raise RuntimeError('Use Python -E -B')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('witness', type=Path)
    parser.add_argument('out', type=Path)
    args = parser.parse_args()
    guard()
    if not args.out.resolve().is_relative_to(reducer.ROOT / '.local-work/d5ai'):
        raise ValueError('Fresh task-local output required')
    args.out.mkdir(exist_ok=False)
    receipt_path = args.witness / 'qualification.json'
    receipt = reducer.load(receipt_path)
    if (receipt['schema'] != 'sor-d5ai-combined-ABA-native/1' or receipt['status'] != 'PASS' or
            receipt['inputs_unchanged'] is not True or receipt['native_exit'] != 0 or
            receipt['strict_sequence_and_QPC_order'] is not True):
        raise ValueError('Combined native ordering evidence incomplete')
    for name, digest in receipt['inputs'].items():
        if sha(name) != digest:
            raise ValueError('Native witness input changed: ' + name)
    digest = sha(args.witness / 'SorConstructionWinner.dll')
    if digest != receipt['test_dll_sha256']:
        raise ValueError('Fixture derivative changed')
    native = reducer.inspect(args.witness / 'session', digest, reducer.read_capture.TARGET)
    before, after = native['observations']
    journal = native['lifetime']
    tests = []

    def check(name, condition):
        tests.append(dict(name=name, passed=bool(condition)))
        if not condition:
            raise AssertionError(name)

    value = reducer.d5ai_lifetime.evaluate(before, after, journal)
    check('actual-combined-old-geometry-ending-retained',
          value['qualified'] and value['state'] == 'PRIOR_COLLECTION_GEOMETRY_ENDED')
    old = next(v for v in value['collections'] if v['allocation'] == receipt['baseline_collection'])
    check('actual-earliest-old-ending-not-conflated-with-address-reuse',
          old['ending_end_sequence'] == receipt['old_ending']['sequence'] and
          old['post_ending_address_activity'][0]['begin_sequence'] == receipt['new_same_address_mutation']['sequence'])
    certificate = reducer.relation(before, after, native['events'], native['events'], journal)
    comparison = reducer.compare(before['envelope'], after['envelope'], certificate)
    check('consumer-unavailability-independent-of-later-address-mutation', comparison['outcome'] == 'UNAVAILABLE')
    ends = {(e['thread'], e['invocation']): e for e in journal['events'] if e['phase'] == 'END'}
    c_begin = next(e for e in journal['events'] if e['kind'] == 'COLLECTION_GEOMETRY' and e['phase'] == 'BEGIN')
    c_end = ends[(c_begin['thread'], c_begin['invocation'])]
    m_begin = next(e for e in journal['events'] if e['kind'] == 'COLLECTION_MUTATION' and e['phase'] == 'BEGIN')
    m_end = ends[(m_begin['thread'], m_begin['invocation'])]

    def mutated(label):
        changed = copy.deepcopy(journal)
        a = next(e for e in changed['events'] if e['sequence'] == c_begin['sequence'])
        b = next(e for e in changed['events'] if e['sequence'] == c_end['sequence'])
        m = next(e for e in changed['events'] if e['sequence'] == m_begin['sequence'])
        n = next(e for e in changed['events'] if e['sequence'] == m_end['sequence'])
        if label == 'ending-mutation-time-tie': m['ticks'] = b['ticks']
        elif label == 'overlapping-mutation': m['ticks'] = a['ticks']
        elif label == 'exceptional-ending': b['status'] = 16
        elif label == 'loss': changed['loss'] = 1
        elif label == 'mutation-before-ending':
            pair = [m, n]
            changed['events'] = pair + [e for e in changed['events'] if e not in pair]
            low = max(before['proof']['header']['completion_ticks'],
                      before['proof']['header']['lifetime_end']['ticks']) + 1
            high = after['proof']['header']['ticks_begin'] - 1
            check('synthetic-order-model-has-bounded-native-gap', high - low > 100)
            ids = {e['invocation']: i + 1 for i, e in enumerate(v for v in changed['events'] if v['phase'] == 'BEGIN')}
            for i, e in enumerate(changed['events'], 1):
                e.update(sequence=i, ticks=low + i * (high - low) // (len(changed['events']) + 1),
                         invocation=ids[e['invocation']], parent=ids.get(e['parent'], 0))
        result = reducer.d5ai_lifetime.evaluate(before, after, changed)
        check('synthetic-uncertain-old-history-refused-' + label, not result['qualified'])

    for label in ('ending-mutation-time-tie', 'overlapping-mutation', 'exceptional-ending', 'loss', 'mutation-before-ending'):
        mutated(label)
    later_exception = copy.deepcopy(journal)
    next(e for e in later_exception['events'] if e['sequence'] == m_end['sequence'])['status'] = 16
    exception_result = reducer.d5ai_lifetime.evaluate(before, after, later_exception)
    check('synthetic-later-exception-cannot-revive-old-content',
          exception_result['qualified'] and exception_result['state'] == 'PRIOR_COLLECTION_GEOMETRY_ENDED' and
          m_end['sequence'] in exception_result['recorded_exception_sequences'] and
          exception_result['collections'][0]['post_ending_address_activity'][0]['end_status'] == 16)
    # Holder teardown cannot suppress mutation of an externally retained
    # collection. This model removes the child clear, preserving paired holder
    # and mutation records and explicitly resequencing the synthetic history.
    held = copy.deepcopy(journal)
    held['events'] = [e for e in held['events'] if e['kind'] != 'COLLECTION_GEOMETRY']
    for i, e in enumerate(held['events'], 1):
        e['sequence'] = i
    held['records'] = len(held['events'])
    held['coverage_mark'].update(cursor=held['records'], generation_before=held['records'], generation_after=held['records'])
    check('synthetic-holder-ending-alone-does-not-end-collection',
          not reducer.d5ai_lifetime.evaluate(before, after, held)['qualified'])
    # Per-collection precedence must not erase the surviving collection in a
    # separately observed partial population. Append a modeled later mutation
    # to only the actually ended constituent, using a fresh invocation.
    partial = reducer.inspect(reducer.ROOT / '.local-work/d5ai-recorder/build16/d5ai-life-partial',
                              receipt['candidate16_sha256'], reducer.read_capture.TARGET)
    pa, pb = partial['observations']
    pj = copy.deepcopy(partial['lifetime'])
    initial = reducer.d5ai_lifetime.evaluate(pa, pb, pj)
    ended = next(c for c in initial['collections'] if c['state'] == 'ENDED')
    last_tick = max(e['ticks'] for e in pj['events'])
    check('synthetic-partial-mutation-fits-before-return', last_tick + 3 < pb['proof']['header']['ticks_begin'])
    invocation = max(e['invocation'] for e in pj['events']) + 1
    begin = dict(m_begin, sequence=len(pj['events']) + 1, invocation=invocation, parent=0,
                 thread=pj['events'][0]['thread'], allocation=ended['allocation'], receiver=ended['allocation'] + 8,
                 ticks=last_tick + 1)
    pj['events'].extend([begin, dict(begin, phase='END', sequence=begin['sequence'] + 1, ticks=last_tick + 2)])
    pj['records'] = len(pj['events'])
    pj['coverage_mark'].update(cursor=pj['records'], generation_before=pj['records'], generation_after=pj['records'])
    result = reducer.d5ai_lifetime.evaluate(pa, pb, pj)
    check('synthetic-precedence-is-per-collection-in-partial-population',
          result['qualified'] and result['state'] == 'PARTIAL_COLLECTION_GEOMETRY_SURVIVES' and
          result['census']['surviving_with_nested_backing'] == initial['census']['surviving_with_nested_backing'])
    # A further clear of the reused address is also new address activity, not
    # a second ending attributed to the baseline allocation.
    again = copy.deepcopy(journal)
    last_tick = max(e['ticks'] for e in again['events'])
    check('synthetic-new-lifetime-clear-fits-before-return', last_tick + 3 < after['proof']['header']['ticks_begin'])
    extra = dict(c_begin, sequence=len(again['events']) + 1,
                 invocation=max(e['invocation'] for e in again['events']) + 1, parent=0, ticks=last_tick + 1)
    again['events'].extend([extra, dict(extra, phase='END', sequence=extra['sequence'] + 1, ticks=last_tick + 2)])
    extra_result = reducer.d5ai_lifetime.evaluate(before, after, again)
    extra_old = next(c for c in extra_result['collections'] if c['allocation'] == receipt['baseline_collection'])
    check('synthetic-later-ending-not-attributed-to-old-allocation',
          extra_result['qualified'] and len(extra_old['ending_sequences']) == 1 and
          len(extra_old['post_ending_address_activity']) == 2)
    modules = {str(Path(m.__file__).resolve()): sha(m.__file__) for m in list(sys.modules.values())
               if getattr(m, '__file__', None) and Path(m.__file__).suffix == '.py' and
               Path(m.__file__).resolve().is_relative_to(reducer.ROOT)}
    output = dict(tests=tests, passed=len(tests), actual_storage=value, actual_comparison=comparison,
                  native_receipt_sha256=sha(receipt_path), actual_test_dll_sha256=digest,
                  candidate16_lineage_sha256=receipt['candidate16_sha256'], executed_modules=modules,
                  method_sha256=sha(__file__), scope='Actual combined fixture ordering; remaining named models are synthetic, not new observations')
    (args.out / 'receipt.json').write_text(json.dumps(output, indent=2) + '\n', encoding='utf8', newline='\n')
    for name in modules:
        path = Path(name)
        target = args.out / 'methods' / path.relative_to(reducer.ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(path.read_bytes())
    print(json.dumps(dict(passed=len(tests), actual_storage=value['state'])))


if __name__ == '__main__':
    main()
