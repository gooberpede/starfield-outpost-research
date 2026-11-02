# SPDX-License-Identifier: GPL-3.0-or-later
"""Recheck historical B1/B2 dispatch and refuse geometry/lifetime promotion.

Executes unchanged owned historical readers on pinned retained evidence, compares
complete reductions, and challenges new intake with old identities. Writes fresh
private JSON only. No native execution, process, save, network or Git mutation.
SOR-P-0002 covers the owned original readers and their frozen package copies.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import sys

from d5ae_baseline import guard, sha
import d5ai_reduce as reducer


def main():
    if not __debug__ or sys.flags.optimize:
        raise RuntimeError('Use Python -E -B')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('out', type=Path)
    args = parser.parse_args()
    guard()
    root = reducer.ROOT
    if not args.out.resolve().is_relative_to(root / '.local-work/d5ai'):
        raise ValueError('Fresh task-local output required')
    args.out.mkdir(exist_ok=False)
    tests, results = [], {}

    def check(name, condition):
        tests.append(dict(name=name, passed=bool(condition)))
        if not condition:
            raise AssertionError(name)

    baseline = reducer.load(root / '.local-work/d5ai/baseline.json')
    for name in ('read_capture.py', 'reduce_v3.py', 'reduce_v4.py'):
        path = root / 'runtime/construction-winner' / name
        check('historical-source-unchanged-' + name, sha(path) == baseline['files'][path.relative_to(root).as_posix()]['sha256'])
    cases = (
        ('b1', 'ceb439b14ddc4db8b734526a124f1e879b64cd457774a87a6a67852fd4489894',
         'cd4762095a422fb537844546e923fff667e894a63b082b0205f3107786f49a5c',
         '20160e2ccdf183c84baddae0214c0438eb471b3eb0ec34dee0632bb5880ddaeb',
         'build24', 19780),
        ('b2', '5ed302aea9da7dc2261163b3dd1816e670a3c2f39891f1ec8d20094afa72b3a1',
         '4a8feb68f667f417967a0cd4a332cefde768658d254ead8d555b3e5f44515218',
         '9d2f0bab159f3ec23186426fb4833eb645578d2a43612bb2e8def6b1af455dcc',
         'p3-native-final04', 32141))
    for label, nonce, raw_hash, dll_hash, package, records in cases:
        session = root / '.local-work/d5x/live' / ('session-' + nonce)
        check('raw-identity-' + label, sha(session / 'events.bin') == raw_hash)
        original_path = root / '.local-work/d5x' / package / 'package-runtime/read_capture.py'
        spec = importlib.util.spec_from_file_location('d5ai_owned_historical_' + label, original_path)
        original = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(original)
        old, current = original.inspect(session, dll_hash), reducer.read_capture.inspect(session, dll_hash)
        check('complete-frozen-reduction-equality-' + label, old == current)
        check('record-census-' + label, current['durable_records'] == records and not current['damage'])
        if label == 'b1':
            check('b1-first-construction-not-invented', not current['chains'])
        identity = reducer.load(session / 'identity.json')
        for operation, name in (
                (lambda: reducer.validate_candidate_identity(identity), 'new-intake'),
                (lambda: reducer.d5ai_read_geometry.read_session(session), 'raw2-reader')):
            try:
                operation()
            except ValueError:
                check('old-capture-not-upgraded-' + label + '-' + name, True)
            else:
                check('old-capture-not-upgraded-' + label + '-' + name, False)
        results[label] = dict(reduction=current, frozen_reader=str(original_path), frozen_reader_sha256=sha(original_path),
                              scientific_classification='Historical findings unchanged; no full geometry/lifetime certificate added')
    output = dict(tests=tests, passed=len(tests), results=results, method_sha256=sha(__file__),
                  current_reader_sha256=sha(reducer.read_capture.__file__),
                  scope='Historical transport/reduction compatibility only; B1 PARTIAL science and B2 limits remain unchanged')
    (args.out / 'receipt.json').write_text(json.dumps(output, indent=2) + '\n', encoding='utf8', newline='\n')
    print(json.dumps(dict(passed=len(tests))))


if __name__ == '__main__':
    main()
