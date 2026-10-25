# SPDX-License-Identifier: GPL-3.0-or-later
"""Verify input pins, native export bounds and unchanged ten-control ledger.

Reads source registers, existing native exports and frozen local result ledgers.
Writes one exclusive ignored checks receipt. Python stdlib/project-owned audit
only; no native execution, regeneration, target, save, DB, Git or network writes.
Integrity assertions validate inputs/transcriptions, not scientific semantics.
"""
import argparse
import csv
import json
from pathlib import Path
from audit import ROOT, OUT, pin, write

DOC = ROOT / 'docs/experiments/resource-population-lifecycle'
EXE = '7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28'


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--label', default='checks')
    args = ap.parse_args()
    assert args.label and all(c in 'abcdefghijklmnopqrstuvwxyz0123456789-' for c in args.label)
    rows = list(csv.DictReader((DOC / 'sources.csv').open(encoding='utf8')))
    for row in rows:
        assert pin(ROOT / row['path']) == row['sha256'], row['path']
    native = list(csv.DictReader((DOC / 'native.csv').open(encoding='utf8')))
    for row in native:
        text = (ROOT / row['export_path']).read_text(encoding='utf8')
        assert EXE in text and 'BASE\t140000000' in text
        assert row['static_va'][2:].lower() in text.lower(), row['id']
        assert int(row['static_va'], 16) - 0x140000000 == int(row['rva'], 16)
    for name in ('d5c-lifecycle01', 'd5c-load02', 'd5c-init03'):
        path = ROOT / f'.local-work/workshop-population-rework/specialist/{name}.tsv'
        assert path.read_text(encoding='utf8').rstrip().endswith('END')
        log = path.with_suffix('.log').read_text(encoding='utf8')
        assert 'SCRIPT ERROR' not in log and 'ERROR ' not in log
        assert '-readOnly' in (OUT / 'commands.json').read_text(encoding='utf8')
    # Check historical expected identities before trusting a newly minted ledger.
    registers = ['docs/experiments/native-availability-map/sources.csv',
                 'docs/experiments/native-availability-map/region-sources.csv',
                 'docs/experiments/spatial-equivalence-feasibility/geometry-lifetime/sources.csv',
                 'docs/experiments/resource-combined-acquisition/phase-b-sources.csv']
    expected = {}
    for name in registers:
        for row in csv.DictReader((ROOT / name).open(encoding='utf8')):
            expected[row['path'].replace('\\', '/')] = row['sha256']
    crosschecked = 0
    for row in rows:
        if row['path'] in expected:
            assert row['sha256'] == expected[row['path']], row['path']
            crosschecked += 1
    controls = ROOT / '.local-work/resource-construction-mask-selection/regression01/native-comparison.json'
    comparison = json.loads(controls.read_text())
    assert len(comparison) == 20
    assert len({(r['body'], r['capture']) for r in comparison}) == 10
    assert all(r['exact_matches'] == 1 and r['callback_equal'] for r in comparison)
    freeze_root = ROOT / '.local-work/resource-construction-mask-selection'
    frozen = json.loads((freeze_root / 'prediction-freeze.json').read_text())
    assert pin(freeze_root / 'conditional-results.json') == frozen['results_sha256']
    write(OUT / f'{args.label}.json', dict(input_pins=len(rows), historical_pin_crosschecks=crosschecked,
        native_groups=len(native), exact_control_identities=10, historical_comparison_rows=20,
        geometry_rerun=False, frozen_prediction_unchanged=True, new_exports_complete=3,
        scientific_semantics='Manual native inspection and independent review; not proved by assertions'))
    print('PASS:', len(rows), 'pins;', crosschecked, 'historical crosschecks; ten unchanged control identities')


if __name__ == '__main__':
    main()
