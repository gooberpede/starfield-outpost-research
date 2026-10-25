# SPDX-License-Identifier: GPL-3.0-or-later
"""Verify inherited native/source pins and frozen geometry controls without rerun.

Reads D5C/D5D source ledgers, unchanged comparison/freeze records and authored
Python/JSON files. Writes exclusive local JSON. No targets, saves, database,
configuration, predictor regeneration, network or Git mutation.
"""
import ast
import csv
import json
from build import ROOT, SRC, LOCAL, pin


def main():
    paths = {}
    for name in ('resource-population-lifecycle', 'resource-construction-demand'):
        register = ROOT / f'docs/experiments/{name}/sources.csv'
        for row in csv.DictReader(register.open(encoding='utf8')):
            path = ROOT / row['path']
            assert pin(path) == row['sha256'], row['path']
            paths[str(path)] = row['sha256']
    control = ROOT / '.local-work/resource-construction-mask-selection/regression01/native-comparison.json'
    rows = json.loads(control.read_text())
    assert len(rows) == 20 and len({(r['body'], r['capture']) for r in rows}) == 10
    assert all(r['exact_matches'] == 1 and r['callback_equal'] for r in rows)
    frozen = ROOT / '.local-work/resource-construction-mask-selection'
    freeze = json.loads((frozen / 'prediction-freeze.json').read_text())
    assert pin(frozen / 'conditional-results.json') == freeze['results_sha256']
    for path in SRC.glob('*.py'):
        ast.parse(path.read_text(encoding='utf8'), filename=str(path))
    json.loads((SRC / 'event.schema.json').read_text())
    result = dict(inherited_pins=len(paths), controls=10, control_rows=20,
        geometry_rerun=False, frozen_alternatives_unchanged=True,
        inputs=paths, authored_sources={p.name:pin(p) for p in SRC.glob('*') if p.is_file()})
    with (LOCAL / 'verification01.json').open('x', encoding='utf8', newline='\n') as stream:
        json.dump(result, stream, indent=2)
        stream.write('\n')
    print(len(paths), 'pins; ten geometry controls integrity-only; frozen alternatives unchanged')


if __name__ == '__main__':
    main()
