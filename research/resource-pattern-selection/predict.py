# SPDX-License-Identifier: GPL-3.0-or-later
"""Generate witness-blind C2D conditional selection traces at repository root.

Reads only installed map/definition derivatives and frozen site geography.
Writes one exclusive ignored JSON; stdlib and owned context/selector methods.
No native captures, expected results, geometry, network or target operations.
"""
import argparse
import hashlib
import json
from pathlib import Path
import struct
from selector import predict
import context

ROOT = Path(__file__).resolve().parents[2]


def pin(path):
    with Path(path).open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def definitions(path):
    rows = json.loads(path.read_text())['records']
    def last(row, name):
        return bytes.fromhex(next(v for k, v in reversed(row['fields']) if k == name))
    styles = {r['formid']: int.from_bytes(last(r, 'NNAM'), 'little') for r in rows
              if r['type'] == 'BIOM' and any(k == 'NNAM' for k, v in r['fields'])}
    registry = [dict(id=r['formid'], style=int.from_bytes(last(r, 'CNAM'), 'little'))
                for r in rows if r['type'] == 'SFPT' and any(k == 'CNAM' for k, v in r['fields'])]
    return styles, registry


def run(output):
    assert output.resolve().is_relative_to(ROOT / '.local-work/resource-pattern-selection')
    paths = [ROOT / '.local-work/resource-geometry/source-definitions01.json',
             Path(__file__), ROOT / 'research/resource-pattern-selection/selector.py',
             ROOT / 'research/resource-geometry/context.py', ROOT / 'research/resource-geometry/geometry.py']
    sites = [('Carinae', 'carinae iii-a'), ('Feynman', 'feynman v')]
    for site, map_name in sites:
        paths += [ROOT / f'.local-work/outpost-biomes/{map_name}.biom',
                  ROOT / f'.local-work/resource-geometry-mature-context/site-{site.lower()}-initial02.json']
    pins = {str(p): pin(p) for p in paths}
    styles, registry = definitions(paths[0])
    result = dict(schema='sor-c2d-blind-selection/1', inputs=pins, sites=[])
    for site, map_name in sites:
        geography = json.loads((ROOT / f'.local-work/resource-geometry-mature-context/site-{site.lower()}-initial02.json').read_text())
        m = context.read_map((ROOT / f'.local-work/outpost-biomes/{map_name}.biom').read_bytes())
        lo, hi = geography['halo']['owner_cell_bounds']
        targets = {(geography['tag'], x // 192, y // 192)
                   for x in range(lo[0], hi[0] + 1) for y in range(lo[1], hi[1] + 1)}
        kwargs = dict(surface_seed=0x20201215, rotate=False,
            qualification=dict(effective_map=False, runtime_registration_order=False,
                               effective_surface_seed=False, effective_rotation=False))
        calculated = predict(m, styles, registry, geography['system'], geography['index'], targets, **kwargs)
        inherited = context.select_patterns(m, styles, registry, geography['system'], geography['index'])
        assert calculated['tables'] == inherited['tables']
        calculated.pop('tables')
        result['sites'].append(dict(site=site, system=geography['system'], body_index=geography['index'],
            crc_operands_le=struct.pack('<III', geography['index'], geography['system'], kwargs['surface_seed']).hex(),
            registry_basis='Installed main-file record order; runtime order UNKNOWN',
            surface_seed='0x20201215', rotate=False, **calculated))
    assert pins == {str(p): pin(p) for p in paths}
    with output.open('x', encoding='utf8', newline='\n') as f:
        json.dump(result, f, indent=2)
        f.write('\n')
    print(json.dumps(result['sites'], indent=2))


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output', type=Path, required=True)
    run(p.parse_args().output)
