# SPDX-License-Identifier: GPL-3.0-or-later
"""Witness-blind PNDT/SFTR selection from installed definitions and saved geography.

Reads the pinned ESM and owned frozen site geography only. Writes exclusive
ignored tables and a selected trace. No native receipts, expected SFPT, observed
source anchors, geometry scores, runtime, network or configuration operations.
"""
import argparse
import json
from pathlib import Path
from installed import ESM, load_trees
from predict import ROOT, pin


def run(output):
    assert output.resolve().is_relative_to(ROOT / '.local-work/resource-pattern-selection')
    expected_esm = '1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7'
    assert pin(ESM) == expected_esm
    sites = [('Carinae', 0x0005e4da), ('Feynman', 0x0005e0de)]
    trees = load_trees([owner for site, owner in sites])
    result = dict(schema='sor-c2d-installed-selection/1', mode='INSTALLED_LINKED_TREE',
        inputs={str(ESM): expected_esm}, sites=[])
    table_output = output.with_suffix('.tables.json')
    tables = {}
    for site, owner in sites:
        path = ROOT / f'.local-work/resource-geometry-mature-context/site-{site.lower()}-initial02.json'
        result['inputs'][str(path)] = pin(path)
        geography = json.loads(path.read_text())
        lo, hi = geography['halo']['owner_cell_bounds']
        targets = sorted({(geography['tag'], x // 192, y // 192)
                   for x in range(lo[0], hi[0] + 1) for y in range(lo[1], hi[1] + 1)})
        upstream = trees[owner]
        tables[site] = upstream['tables']
        traces = []
        for chart, cx, cy in targets:
            slot = cx * 256 + cy
            pattern, flags = upstream['tables'][chart][slot]
            traces.append(dict(chart=chart, coarse=[cx, cy], native_face_slot=slot,
                selected=f'0x{pattern:08x}', flags=f'0x{flags:02x}',
                candidate_order='NOT CONSUMED: linked precomputed SFTR',
                seed='NOT CONSUMED: linked precomputed SFTR',
                decision='PNDT FNAM -> typed SFTR -> face FNAM/GNAM -> X*256+Y'))
        result['sites'].append(dict(site=site, pndt=f'0x{owner:08x}',
            pndt_file_offset=upstream['pndt']['offset'], tree=f'0x{upstream["tree"]["formid"]:08x}',
            tree_file_offset=upstream['tree']['offset'], components=upstream['components'], traces=traces,
            qualification='STATIC installed-main prediction; effective runtime overrides/epoch unobserved'))
    for path in (Path(__file__), ROOT / 'research/resource-pattern-selection/installed.py',
                 ROOT / 'save-analysis/scripts/inspect_outpost_definitions.py'):
        result['inputs'][str(path)] = pin(path)
    assert all(pin(Path(p)) == h for p, h in result['inputs'].items())
    with table_output.open('x', encoding='utf8', newline='\n') as f:
        json.dump(tables, f)
        f.write('\n')
    result['tables_path'] = str(table_output)
    result['tables_sha256'] = pin(table_output)
    with output.open('x', encoding='utf8', newline='\n') as f:
        json.dump(result, f, indent=2)
        f.write('\n')
    print(json.dumps(result['sites'], indent=2))


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output', type=Path, required=True)
    run(p.parse_args().output)
