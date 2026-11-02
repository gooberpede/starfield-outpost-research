# SPDX-License-Identifier: GPL-3.0-or-later
"""Demonstrate both prospective equality oracles with existing full native inputs.

Reads completed candidate-host sessions, never collects Stage B results or starts
a process. Executes the final source/frame/lifetime intake and full comparator
on distinct real host processes carrying native mask-0/3/3 populations. Writes
new private receipts only. These are instrument controls, not prediction outcomes.
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
    parser.add_argument('build', type=Path)
    parser.add_argument('out', type=Path)
    args = parser.parse_args()
    guard()
    if not args.out.resolve().is_relative_to(reducer.ROOT / '.local-work/d5ai'):
        raise ValueError('Fresh task-local output required')
    args.out.mkdir(exist_ok=False)
    build = reducer.load(args.build / 'build.json')
    digest = sha(args.build / 'SorConstructionWinner.dll')
    if digest not in build['outputs'].values() or not all(c['pass_exit'] for c in build['cases']):
        raise ValueError('Exact native build/case evidence required')
    tests, operands = [], {}

    def check(name, condition):
        tests.append(dict(name=name, passed=bool(condition)))
        if not condition:
            raise AssertionError(name)

    for label, expected in (('mask0', (3, 74, 193)), ('mask3a', (3, 78, 180)), ('mask3b', (3, 78, 180))):
        native = reducer.inspect(args.build / ('d5ai-native-' + label), digest, reducer.read_capture.TARGET)
        check('full-qualified-intake-' + label, len(native['observations']) == 1 and not native['refused'])
        operand = native['observations'][0]
        capture = operand['envelope']['capture']
        check('complete-census-' + label, tuple(capture[k] for k in ('resource_slots', 'region_total', 'point_total')) == expected)
        operands[label] = native
    comparisons = {}
    for name, first, second, expected in (
            ('confirming-oracle', 'mask3a', 'mask3b', 'REBUILT_IDENTICAL'),
            ('contradicting-oracle', 'mask0', 'mask3a', 'REBUILT_DIFFERENT')):
        a, b = operands[first], operands[second]
        before, after = a['observations'][0], b['observations'][0]
        pa, pb = before['proof']['process_identity'], after['proof']['process_identity']
        check('actual-process-births-distinct-' + name,
              (pa['pid'], pa['creation_filetime']) != (pb['pid'], pb['creation_filetime']))
        check('same-host-executable-' + name, pa['host_sha256'] == pb['host_sha256'])
        check('same-source-and-consumed-frame-' + name,
              before['envelope']['source'] == after['envelope']['source'] and
              before['envelope']['frame'] == after['envelope']['frame'])
        certificate = reducer.relation(before, after, a['events'], b['events'], b['lifetime'])
        check('positive-distinct-process-reconstruction-' + name,
              certificate['qualified'] and certificate['relation'] == 'RECONSTRUCTED' and
              certificate['process_relation'] == 'DISTINCT_PROCESSES')
        result = reducer.compare(before['envelope'], after['envelope'], certificate)
        check('practical-full-content-' + name, result['outcome'] == expected)
        comparisons[name] = dict(result=result, certificate=certificate, before=before, after=after)
        fake = copy.deepcopy(after)
        fake['proof']['process_identity'] = copy.deepcopy(pa)
        check('different-nonce-is-not-new-process-' + name,
              not reducer.relation(before, fake, a['events'], b['events'], b['lifetime'])['qualified'])
    modules = {}
    for module in list(sys.modules.values()):
        name = getattr(module, '__file__', None)
        if name:
            path = Path(name).resolve()
            if path.is_relative_to(reducer.ROOT) and path.is_file() and path.suffix == '.py':
                modules[str(path)] = sha(path)
    result = dict(schema='sor-d5ai-prediction-measurement-controls/1', tests=tests, passed=len(tests),
                  comparisons=comparisons, dll_sha256=digest, build_sha256=sha(args.build / 'build.json'),
                  method_sha256=sha(__file__), executed_modules=modules,
                  scope='Offline prior native inputs in independent owned processes; no retail/Stage B or forecast truth claim')
    (args.out / 'receipt.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf8', newline='\n')
    for path in modules:
        destination = args.out / 'methods' / Path(path).relative_to(reducer.ROOT)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(Path(path).read_bytes())
    print(json.dumps(dict(passed=len(tests), outcomes={k: v['result']['outcome'] for k, v in comparisons.items()})))


if __name__ == '__main__':
    main()
