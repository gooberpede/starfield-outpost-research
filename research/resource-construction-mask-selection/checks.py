# SPDX-License-Identifier: GPL-3.0-or-later
"""Verify D5A accounting, source pins, frozen outputs and inherited native controls.

Reads only existing authored/local records; writes one exclusive local receipt.
Stdlib only. No target, Git, save or analysis-project writes. Numerical generation
is independently exercised by regression.py; this script checks its result ledger.
"""
import csv
import json
from pathlib import Path
from analyze import ROOT, DOC, LOCAL, pin, write


def main():
    read = lambda name: list(csv.DictReader((DOC / name).open(encoding='utf8')))
    cases, outcomes, matrix = read('cases.csv'), read('outcomes.csv'), read('discrimination.csv')
    assert len(cases) == len(matrix) == 13
    assert len(outcomes) == 90
    assert sum(s['context'] == 'CANDIDATE' for s in cases) == 11
    assert sum(s['footprint_discrimination'] == 'PATH_COUNTS' for s in matrix) == 3
    frozen = json.loads((LOCAL / 'prediction-freeze.json').read_text())
    assert pin(LOCAL / 'conditional-results.json') == frozen['results_sha256']
    assert pin(Path(__file__).with_name('analyze.py')) == frozen['code_sha256']
    for row in read('sources.csv'):
        assert pin(ROOT / row['path']) == row['sha256']
    native = json.loads((LOCAL / 'regression01/native-comparison.json').read_text())
    assert len(native) == 20
    assert all(r['exact_matches'] == 1 and r['callback_equal'] for r in native)
    assert len({(r['body'], r['capture']) for r in native}) == 10
    source_fields = sum(r['source_identity'] is not None for r in native)
    assert source_fields == 6
    pins = []
    for path in ('research/resource-selection-context/controller.cpp',
                 'research/resource-feynman-d5/source_gate.py',
                 '.local-work/resource-selection-context/build12/build.json',
                 '.local-work/recon/resource-availability-cont-01.tsv',
                 '.local-work/recon/resource-milestone-b-producers-01.tsv',
                 '.local-work/workshop-population-rework/specialist/d5-mask01.tsv',
                 '.local-work/workshop-population-rework/specialist/d5-raster02.tsv'):
        pins.append(dict(path=path, sha256=pin(ROOT / path)))
    write(LOCAL / 'checks.json', dict(source_count=13, candidate_count=11,
        conditional_runs=26, resource_rows=90, footprint_contrasts=3,
        native_comparisons=20, exact_controls=10, additional_source_identity_controls=3,
        legacy_source_identity='NOT TESTED for seven original controls',
        prediction_and_source_hashes=True, native_pins=pins))
    print('PASS: 13 sources, 26 branches, 90 rows, ten exact native controls')


if __name__ == '__main__':
    main()
