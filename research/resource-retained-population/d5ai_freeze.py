# SPDX-License-Identifier: GPL-3.0-or-later
"""Hash-bind independently reviewed prospective text without changing that text.

Reads explicit proposed text, source/receipt pins and an independently returned
review record. Writes one new private freeze manifest only. No Stage B result,
game, save, process, network, Git/index/ref mutation or implied episode approval.
Review acceptance is an accountable external premise, not inferred from test
counts. Source/prediction amendments require a new prospective record.
"""
import argparse
import datetime
import json
from pathlib import Path
import subprocess
import sys

from d5ae_baseline import guard, sha
from d5ai_geometry import load

ROOT = Path(__file__).resolve().parents[2]


def main():
    if not __debug__ or sys.flags.optimize:
        raise RuntimeError('Use installed Python -E -B')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--text', type=Path, required=True)
    parser.add_argument('--pins', type=Path, required=True)
    parser.add_argument('--review', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    guard()
    if (args.text.resolve() != ROOT / 'docs/experiments/resource-retained-population/d5ai-prediction-text-v1.md' or
            not args.out.resolve().is_relative_to(ROOT / '.local-work/d5ai')):
        raise ValueError('Exact repository text and fresh task-local manifest required')
    pins, review = load(args.pins), load(args.review)
    if (pins['schema'] != 'sor-d5ai-freeze-inputs/1' or
            review['schema'] != 'sor-d5ai-prefreeze-review/1' or
            review['model_rationale'] != 'ACCEPT' or review['measurement_adequacy'] != 'ACCEPT' or
            review['phase_b_results_accessed'] is not False or
            review['pins_sha256'] != sha(args.pins) or review['text_sha256'] != sha(args.text)):
        raise ValueError('Exact substantive pre-freeze acceptance is missing')
    if not review['reviewer'] or not review['review_return_sha256'] or sha(review['review_return_path']) != review['review_return_sha256']:
        raise ValueError('Independent review return provenance missing')
    head = subprocess.check_output(['git', '--no-optional-locks', 'rev-parse', 'HEAD'], cwd=ROOT).decode().strip()
    if head != pins['head']:
        raise ValueError('Reviewed commit baseline changed')
    for path, digest in pins['material'].items():
        if sha(path) != digest:
            raise ValueError('Reviewed source/evidence changed: ' + path)
    if str(args.text.resolve()) not in pins['material'] or pins['material'][str(args.text.resolve())] != sha(args.text):
        raise ValueError('Prediction text is outside reviewed material')
    if pins['material'].get(str(Path(__file__).resolve())) != sha(__file__):
        raise ValueError('Freeze method is outside reviewed source baseline')
    bound = dict(pins['material'])
    bound.update({str(args.pins.resolve()): sha(args.pins), str(args.review.resolve()): sha(args.review),
                  str(Path(review['review_return_path']).resolve()): review['review_return_sha256']})
    value = dict(schema='sor-d5ai-prediction-freeze/1', prediction_id='D5AI-PRED-01', text_version=1,
                 text_path=str(args.text.resolve()), text_sha256=sha(args.text), head=head,
                 utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                 measurement_review='ACCEPT', model_review='ACCEPT', reviewer=review['reviewer'],
                 phase_b_results_accessed=False, pins=bound,
                 authority='Current D5AI brief authorizes prospective freeze only; neither episode is approved',
                 procedural_conformance='AC01 reading-order FAIL remains for separate maintainer disposition')
    with args.out.open('x', encoding='utf8', newline='\n') as stream:
        stream.write(json.dumps(value, indent=2, allow_nan=False) + '\n')
    print(json.dumps(dict(text_sha256=value['text_sha256'], manifest_sha256=sha(args.out))))


if __name__ == '__main__':
    main()
