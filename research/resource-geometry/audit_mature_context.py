# SPDX-License-Identifier: GPL-3.0-or-later
"""RG2-A1 bounded offline frame/seed discriminator, not a vein prediction.

Reads existing RG1 installed-definition derivative, B1 BIOM maps and RG2-A exact
Save52 joins under .local-work. Imports owned context/geometry (stdlib only).
Writes a NEW JSON beneath .local-work via --output; no target, save, database,
configuration or source mutation. Requires the pinned receipts listed in output.
Both frames are hypotheses. PNDT owner mapping is supported by the newly traced
retail loader/body lookup, conditional on ordinary main-file reconstruction.
"""
import argparse
import hashlib
import json
from pathlib import Path
import struct

import context
from geometry import generation_seed

ROOT = Path(__file__).resolve().parents[2]


def pin(path):
    with path.open('rb') as stream:
        return dict(path=str(path), bytes=path.stat().st_size,
                    sha256=hashlib.file_digest(stream, 'sha256').hexdigest())


def audit():
    definitions = ROOT / '.local-work/resource-geometry/source-definitions01.json'
    joins = ROOT / '.local-work/resource-geometry-live-prep/mature-alternatives.json'
    cases = ROOT / '.local-work/resource-geometry-live-prep/mature-diagnostics.json'
    paths = [definitions, joins, cases, Path(__file__),
             Path(context.__file__), ROOT / 'research/resource-geometry/geometry.py']
    for body in ('feynman v', 'carinae iii-a'):
        paths.append(ROOT / f'.local-work/outpost-biomes/{body}.biom')
    before = [pin(p) for p in paths]
    records = json.loads(definitions.read_text(encoding='utf8'))['records']

    def fields(record):
        return [(tag, bytes.fromhex(value)) for tag, value in record['fields']]

    def last(record, tag):
        return next(v for t, v in reversed(fields(record)) if t == tag)

    by = {r['formid']: r for r in records}
    styles = {r['formid']: int.from_bytes(last(r, 'NNAM'), 'little')
              for r in records if r['type'] == 'BIOM'
              and any(t == 'NNAM' for t, v in fields(r))}
    blocks = {r['formid']: dict(dimensions=struct.unpack('<II', last(r, 'DNAM')))
              for r in records if r['type'] == 'SFBK'}
    patterns, registry = {}, []
    for r in records:
        if r['type'] == 'SFPT' and any(t == 'CNAM' for t, v in fields(r)):
            patterns[r['formid']] = dict(entries=list(zip(
                struct.unpack('<256I', last(r, 'FNAM')), last(r, 'GNAM'))))
            registry.append(dict(id=r['formid'], style=int.from_bytes(last(r, 'CNAM'), 'little')))
    alternatives = json.loads(joins.read_text(encoding='utf8'))
    rows = []
    # Frozen prospective population: user excludes the deleted former R2.
    allowed = {'Feynman V Cu Co Ni IL', 'Carinae III-a Rc Fe'}
    for case in json.loads(cases.read_text(encoding='utf8')):
        if case['name'] not in allowed:
            continue
        join = next(v for v in alternatives if v['name'] == case['name'])
        body = int(case['body'], 16)
        name = 'feynman v' if body == 0x5e0de else 'carinae iii-a'
        m = context.read_map((ROOT / f'.local-work/outpost-biomes/{name}.biom').read_bytes())
        system, parent, index = struct.unpack('<III', next(
            v for t, v in fields(by[body]) if t == 'GNAM' and len(v) == 12))
        selected = context.select_patterns(m, styles, registry, system, index)
        selected['map'] = m
        tag, sx, sy = case['base']
        dx, dy = join['descriptor']['x'], join['descriptor']['y']
        translation = [100 * (sx - dx), 100 * (sy - dy)]
        assert translation == join['translation_candidate']
        variants = []
        for label, origin, center in (
                ('SITE_AS_GENERATOR', [sx, sy], case['center'][:2]),
                ('DESCRIPTOR_AS_GENERATOR', [dx, dy],
                 [case['center'][i] + translation[i] for i in range(2)])):
            halo = context.neighborhood(tag, origin, center, 150, selected,
                                        patterns, blocks, maximum_width=111)
            sources = []
            for s in halo['sources']:
                x, y = s['cell_bounds'][0], s['cell_bounds'][2]
                key = context.packed_seed_key(tag, origin, s['origin'], [x, y], system, index)
                ax, ay = s['geographic_origin']
                nx, ny = s['dimensions']
                masks = sorted({context.mask_lookup(m, tag, a, b)
                                for a in range(ax - 4, ax + nx + 5)
                                for b in range(ay - 4, ay + ny + 5)})
                sources.append(dict(source=s, masks=masks, first_cell=[x, y],
                                    first_key=f'{key:016x}',
                                    crc_with_static_pndt_owner=generation_seed(key, body)))
            variants.append(dict(hypothesis=label, origin=origin, center=center, sources=sources))
        rows.append(dict(name=case['name'], body=case['body'], system=system, index=index,
                         translation=translation, variants=variants,
                         owner_status='STATIC_MAIN_FILE_PNDT_FORMID_TO_BODY_OWNER',
                         geometry_status='UNKNOWN', live_observation=False))
    assert len(rows) == 2
    assert before == [pin(p) for p in paths]
    return dict(schema='sor-rg2a1-frame-discriminator/1', inputs=before, rows=rows,
                qualification='COUNTERFACTUAL_INPUT_DISCRIMINATION_ONLY')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    assert args.output.resolve().is_relative_to((ROOT / '.local-work').resolve())
    with args.output.open('x', encoding='utf8', newline='\n') as stream:
        json.dump(audit(), stream, indent=2)
        stream.write('\n')
    print('PASS two active-site hypotheses audited; no vein predictions emitted')
