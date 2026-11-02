# SPDX-License-Identifier: GPL-3.0-or-later
"""Qualify intra-invocation clock ties without relaxing measurement boundaries.

Reads preserved native short-callback evidence and candidate16 ending sessions.
Writes fresh private receipts only. Actual QPC ties remain unchanged. A declared
owned source/frame premise permits an evaluator check on the actual copied graph;
separate coarsened/decreasing/boundary event models are labeled synthetic.
No native execution, game, save, process, network or Git action.
"""
import argparse
import copy
import json
from pathlib import Path
import sys

from d5ae_baseline import guard, sha
import d5ai_reduce as reducer
from d5ai_operations import worker_json


def main():
    if not __debug__ or sys.flags.optimize:
        raise RuntimeError('Use Python -E -B')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('short_session', type=Path)
    parser.add_argument('build', type=Path)
    parser.add_argument('out', type=Path)
    args = parser.parse_args()
    guard()
    if not args.out.resolve().is_relative_to(reducer.ROOT / '.local-work/d5ai'):
        raise ValueError('Fresh task-local output required')
    args.out.mkdir(exist_ok=False)
    tests = []

    def check(name, condition):
        tests.append(dict(name=name, passed=bool(condition)))
        if not condition:
            raise AssertionError(name)

    journal = reducer.d5ai_read_lifetime.read_prefix(args.short_session, worker_json(args.short_session / 'terminal.json'))
    beginnings = {(e['thread'], e['invocation']): e for e in journal['events'] if e['phase'] == 'BEGIN'}
    ties = [e for e in journal['events'] if e['phase'] == 'END' and
            e['ticks'] == beginnings[(e['thread'], e['invocation'])]['ticks']]
    check('actual-native-short-prefix-has-unchanged-clock-ties', bool(ties))
    check('actual-native-ties-have-causal-phase-sequence',
          all(beginnings[(e['thread'], e['invocation'])]['sequence'] < e['sequence'] for e in ties))
    snapshot = reducer.d5ai_read_geometry.decode((args.short_session / 'geometry-33.bin').read_bytes())
    reducer.d5ai_read_lifetime.qualify_snapshot(snapshot, journal)
    holder = snapshot['holders'][0]
    resources = holder['resources']
    h = snapshot['header']
    # The probe supplies immutable geometry; it does not execute source birth or
    # provider construction. Do not turn this premise into a retail source join.
    value = dict(schema=reducer.SCHEMA, session_id=journal['session_id'], snapshot_id='33',
                 source=dict(key='owned-concurrency-fixture', body_formid=f"{h['owner_formid']:08x}"),
                 frame=dict(basis='source-planar', anchor_i32=[0, 0], origin_i32=[0, 0],
                            clip_center_f32=['00000000'] * 4, clip_half_f32=['00000000'] * 4),
                 capture=dict(complete=True, status='OK', resource_slots=len(resources),
                              region_total=sum(len(r['regions']) for r in resources),
                              point_total=sum(v['count'] for r in resources for v in r['regions'])),
                 availability=dict(boundary_qualified=True, map_scan_complete=True, holder_present=True, exposed=True),
                 generation_quality='UNKNOWN', loss=0,
                 population=[dict(resource=r['resource'], regions=r['regions']) for r in resources])
    proof = dict(header=h, holder_pointer=holder['holder_pointer'],
                 collection_pointers=[r['collection_pointer'] for r in resources],
                 collection_graph=[dict(resource=r['resource'], collection_pointer=r['collection_pointer'],
                                        region_capacity=r['region_capacity'], region_data=r['region_data'],
                                        regions=[dict(storage, count=region['count']) for storage, region in
                                                 zip(r['region_storage'], r['regions'])]) for r in resources])
    observation = dict(envelope=value, proof=proof)
    actual = reducer.d5ai_lifetime.evaluate(observation, observation, journal)
    check('actual-tied-prefix-evaluator-does-not-poison-later-native-graph',
          actual['qualified'] and actual['state'] == 'COMPLETE_COLLECTION_GEOMETRY_SURVIVES')
    digest = sha(args.build / 'SorConstructionWinner.dll')
    native = reducer.inspect(args.build / 'd5ai-life-final', digest, reducer.read_capture.TARGET)
    before, after = native['observations']
    changed = copy.deepcopy(native['lifetime'])
    # Coarsen the leaf collection interval, preserving surrounding parent time.
    begin = next(e for e in changed['events'] if e['phase'] == 'BEGIN' and e['kind'] == 'COLLECTION_GEOMETRY' and
                 e['allocation'] in before['proof']['collection_pointers'])
    end = next(e for e in changed['events'] if e['phase'] == 'END' and e['thread'] == begin['thread'] and e['invocation'] == begin['invocation'])
    end['ticks'] = begin['ticks']
    check('synthetic-coarsened-completed-ending-qualified', reducer.d5ai_lifetime.evaluate(before, after, changed)['qualified'])
    for label in ('decreasing', 'receiver', 'parent', 'thread', 'invocation', 'reorder', 'query-begin-tie', 'query-end-tie', 'baseline-copy-tie'):
        altered = copy.deepcopy(changed)
        a = next(e for e in altered['events'] if e['sequence'] == begin['sequence'])
        b = next(e for e in altered['events'] if e['sequence'] == end['sequence'])
        if label == 'decreasing': b['ticks'] = a['ticks'] - 1
        elif label in ('receiver', 'parent', 'thread', 'invocation'): b[label] += 1
        elif label == 'reorder':
            first, last = altered['events'].index(a), altered['events'].index(b)
            altered['events'][first], altered['events'][last] = b, a
        elif label == 'query-begin-tie': a['ticks'] = b['ticks'] = after['proof']['header']['completion_ticks']
        elif label == 'query-end-tie': b['ticks'] = after['proof']['header']['completion_ticks']
        elif label == 'baseline-copy-tie': a['ticks'] = b['ticks'] = before['proof']['header']['ticks_end']
        check('synthetic-invalid-or-boundary-tie-refused-' + label,
              not reducer.d5ai_lifetime.evaluate(before, after, altered)['qualified'])
    modules = {str(Path(m.__file__).resolve()): sha(m.__file__) for m in list(sys.modules.values())
               if getattr(m, '__file__', None) and Path(m.__file__).suffix == '.py' and
               Path(m.__file__).resolve().is_relative_to(reducer.ROOT)}
    result = dict(tests=tests, passed=len(tests), actual_tie_count=len(ties), actual_graph_result=actual,
                  actual_prefix_sha256=journal['raw_prefix_sha256'], executed_modules=modules,
                  method_sha256=sha(__file__), native_dll_sha256=digest,
                  scope='Actual tied raw prefix and copied owned graph with declared fixture frame/source; synthetic boundary/phase models are not new observations')
    (args.out / 'receipt.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf8', newline='\n')
    for name in modules:
        path = Path(name)
        target = args.out / 'methods' / path.relative_to(reducer.ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(path.read_bytes())
    print(json.dumps(dict(passed=len(tests), actual_ties=len(ties))))


if __name__ == '__main__':
    main()
