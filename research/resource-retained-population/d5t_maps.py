# SPDX-License-Identifier: GPL-3.0-or-later
"""Build D5T geometry, candidate catalogue and canonical SVGs from local receipts.

Reads D5S registration/raster and D5T native results plus three IRES field rows.
Checks receipt consistency, then writes explicit requested research derivatives
under docs/experiments/resource-retained-population/d5t. Uses only the stdlib and
owned geometry code. No target, native execution, save, database or network I/O.
Native XYZ/width and bound scalars are retained losslessly as JSON numbers.
SVG disks/rectangles reconstruct the planar competition footprint; floating
native predicate rounding at marginal boundaries is not a continuous SVG shape.
"""
from collections import Counter
import csv
import hashlib
import json
import math
from pathlib import Path
import struct
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
LOCAL = ROOT / '.local-work/d5t'
DOC = ROOT / 'docs/experiments/resource-retained-population/d5t'
NAMES = {'000057d4': 'Ionic Liquids', '000057d0': 'Fluorine', '000057cf': 'Copper'}
ORDER = list(NAMES)


def read(path):
    return json.loads(path.read_text(encoding='utf8'))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def json_file(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n', encoding='utf8', newline='\n')


def primitives(points):
    """Continuous planar disks and max-width rectangles, before bound clipping."""
    shapes = [dict(kind='disk', center=p[:2], radius=p[3]) for p in points if p[3] > 0]
    for a, b in zip(points, points[1:]):
        dx, dy = b[0]-a[0], b[1]-a[1]
        length = math.hypot(dx, dy)
        if length == 0 or max(a[3], b[3]) <= 0:
            continue
        px, py = -dy/length*max(a[3], b[3]), dx/length*max(a[3], b[3])
        shapes.append(dict(kind='rectangle', vertices=[[a[0]+px, a[1]+py], [b[0]+px, b[1]+py],
                                                      [b[0]-px, b[1]-py], [a[0]-px, a[1]-py]]))
    return shapes


def svg_map(outcomes, palette, comparison=False):
    """Identical 680-pixel plots: X right, Y up; native range [-500,1200]."""
    width = 1660 if comparison else 880
    lines = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="1005" viewBox="0 0 {width} 1005">',
             '<title>Feynman V outpost 2: ordinary generation outcomes</title>',
             '<desc>Reconstructed generation-competition footprints from native retained points and bounds. '
             'One fixed source, not a terrain or Workshop availability map. Native rounding at marginal boundaries is not reproduced.</desc>',
             f'<rect width="{width}" height="1005" fill="#f8fafc"/>',
             '<g font-family="Segoe UI,Arial,sans-serif" fill="#182b36">',
             '<text x="32" y="36" font-size="25" font-weight="600">Feynman V · Outpost 2</text>',
             '<text x="32" y="62" font-size="15">Ordinary generation · fixed source 0:37536:20928:0029d20e · build 1.16.244.0</text>',
             '<text x="32" y="85" font-size="14">Native retained geometry · reconstructed competition footprint · marginal rounding is not reproduced.</text>']
    for panel, outcome in enumerate(outcomes):
        left, top = 82 + 800*panel, 180
        scale = .4
        def point(x, y):
            return left+(x+500)*scale, top+(1200-y)*scale
        def txt(x, y, text, size=13, extra=''):
            lines.append(f'<text x="{x}" y="{y}" font-size="{size}" {extra}>{text}</text>')
        counts = Counter(r['resource'] for r in outcome['regions'])
        txt(left, 119, f"{outcome['id']} · ordinary mask {outcome['mask']}", 21, 'font-weight="600"')
        txt(left, 143, ' / '.join(f'{NAMES[r]} {counts[r]}' for r in ORDER), 14)
        lines.append(f'<rect x="{left}" y="{top}" width="680" height="680" fill="white" stroke="#bccbd2"/>')
        for v in range(-400, 1201, 200):
            x, y = point(v, v)
            lines.extend([f'<path d="M{x} {top}v680 M{left} {y}h680" stroke="#e5ebef" fill="none"/>'])
            txt(x, top+701, str(v), 12, 'text-anchor="middle"')
            txt(left-10, y+4, str(v), 12, 'text-anchor="end"')
        ox, oy = point(0, 0)
        lines.append(f'<path d="M{ox} {top}v680 M{left} {oy}h680" stroke="#bac8d0" fill="none"/>')
        # Resource groups are separate, so same-resource overlaps do not darken.
        for resource in reversed(ORDER):
            color = palette[resource]['rgb']
            lines.append(f'<g fill="{color}" stroke="{color}" stroke-width="0.7">')
            for index, region in enumerate(outcome['regions']):
                if region['resource'] != resource:
                    continue
                bx, by, bz, radius = region['native_bound']
                bx, by = point(bx, by)
                clip_id = f'b{panel}_{index}'
                lines.append(f'<defs><clipPath id="{clip_id}"><circle cx="{bx:.9f}" cy="{by:.9f}" r="{max(radius,.5)*scale:.9f}"/></clipPath></defs>')
                lines.append(f'<g clip-path="url(#{clip_id})">')
                for shape in region['primitives']:
                    if shape['kind'] == 'disk':
                        x, y = point(*shape['center'])
                        lines.append(f'<circle cx="{x:.9f}" cy="{y:.9f}" r="{shape["radius"]*scale:.9f}"/>')
                    else:
                        vertices = ' '.join(f'{x:.9f},{y:.9f}' for x,y in (point(*v) for v in shape['vertices']))
                        lines.append(f'<polygon points="{vertices}"/>')
                lines.append('</g>')
            lines.append('</g>')
        lines.append(f'<path d="M{ox-5} {oy}h10 M{ox} {oy-5}v10" stroke="#172f42" stroke-width="1.5"/>')
        txt(ox+7, oy-7, 'source anchor (0, 0)', 11)
        txt(left+340, top+729, 'X · native source-frame units', 14, 'text-anchor="middle"')
        txt(left-51, top+340, 'Y ↑', 14)
    legend_y = 958
    for i, resource in enumerate(ORDER):
        x = 32+i*245
        lines.append(f'<rect x="{x}" y="{legend_y-13}" width="20" height="14" fill="{palette[resource]["rgb"]}"/>')
        lines.append(f'<text x="{x+28}" y="{legend_y}" font-size="14">{NAMES[resource]} · IRES tint</text>')
    lines.append('<text x="32" y="985" font-size="12">Same frame and scale. No beacon position, terrain, retail frequency or metre conversion is implied.</text>')
    lines.extend(['</g>', '</svg>'])
    text = '\n'.join(lines)+'\n'
    ET.fromstring(text)
    return text


def main():
    DOC.mkdir(exist_ok=True)
    native = read(LOCAL/'native-full05.json')
    old = read(LOCAL/'geometry.json')
    census = read(LOCAL/'winner-candidates05.json')['global_fifo_raster_census']
    queries = {tuple(r['original_int2']):r for r in read(LOCAL/'native-queries05.json')['rows']}
    assert len(census) == 196 and {tuple(r['query']) for r in census} == {(x,y) for x in range(-2,12) for y in range(-2,12)}
    assert set(r['mask'] for r in census) == {0,3}
    assert native['runs'][1]['regions'] == native['runs'][2]['regions']
    assert all(r['native'] == r['planar'] for r in native['spatial_checks'])
    assert not native['errors']
    palette = {}
    for record in read(LOCAL/'ires-fields.json'):
        resource = f"{record['header']['formid']:08x}"
        fields = dict(record['fields'])
        tint = bytes.fromhex(fields['TINC'])
        palette[resource] = dict(name=NAMES[resource], rgb='#'+tint[:3].hex(), tinc=tint.hex(),
                                 record_file_offset=record['header']['offset'],
                                 basis='IRES TINC first, second, third bytes; native loader channels +0xe0/+0xe4/+0xe8; SVG opacity 1')
    rows = []
    for r in sorted(census, key=lambda v: tuple(v['query'])):
        q = r['query']
        converted = queries[tuple(q)]
        assert converted['converted_face_cell'] == [37536+q[0],20928+q[1]]
        assert r['mask'] == (0 if q[1] < 0 else 3)
        weights = native['runs'][0 if r['mask']==0 else 1]['weights']
        rows.append(dict(candidate=f'TQ-{q[0]+2:02d}-{q[1]+2:02d}', local_x=q[0], local_y=q[1],
                         face_x=37536+q[0], face_y=20928+q[1], chart=converted['chart'],
                         normalized_x=converted['normalized_xy'][0],normalized_y=converted['normalized_xy'][1],
                         registration_index=r['index'],
                         mask=r['mask'], ionic_weight=weights[0], fluorine_weight=weights[1], copper_weight=weights[2],
                         outcome_if_winning=f"O{r['mask']}",
                         feasibility='PROVEN D5S owner' if q==[10,11] else 'PROVEN D5S peer' if q==[-2,-2] else 'SUPPORT CANDIDATE; individual arbitration not asserted',
                         inclusion='inside target padded support; mask classified for any successful target-emitting first miss'))
    with (DOC/'candidates.csv').open('w',encoding='utf8',newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator='\n')
        writer.writeheader();writer.writerows(rows)
    outcomes = []
    for run, original in zip(native['runs'][:2], old['results']):
        outcome = dict(id=run['outcome'],mask=run['mask'],weights=run['weights'],
                       equivalence_class=f"A intersect M{run['mask']}; see catalogue.md for admissibility predicate A",
                       witness_original_query=[-2,-2] if run['mask']==0 else [10,11],
                       witness_face_cell=[37534,20926] if run['mask']==0 else [37546,20939],
                       input_contract=original['request'],regions=[])
        for index, region in enumerate(run['regions']):
            data = bytes.fromhex(region['points'])
            points = [list(struct.unpack_from('<4f',data,i)) for i in range(0,len(data),16)]
            bound = list(struct.unpack('<4f',bytes.fromhex(region['header'][:32])))
            outcome['regions'].append(dict(id=f"{run['outcome']}-R{index:03d}",resource=region['resource'],
                                          name=NAMES[region['resource']],points_xyz_width=points,
                                          native_bound=bound,primitives=primitives(points)))
        outcomes.append(outcome)
    document = dict(schema='sor-d5t-geometry/1', source='0:37536:20928:0029d20e',
                    coordinate_basis='D5S manager/source frame; nominal source anchor (0,0); X right and Y up; native units',
                    rendering=dict(product='generation-competition footprint',
                                   rule='union positive-width disks and consecutive max-width rectangles; intersect native bound disk of radius max(r,0.5)',
                                   transformation='SVG x=82+0.4*(X+500), y=180+0.4*(1200-Y); comparison panel adds 800 to x',
                                   extents=[-500,1200,-500,1200],scale_pixels_per_native_unit=.4,
                                   approximation='Continuous planar segment boundaries use binary64 sqrt vertices; native atan2/quaternion and binary32 marginal predicate rounding is not represented. Native points and bounds are exact.',
                                   clipping='Per-region native bound only; no source-box polygon clipping; view contains all primitives'),
                    palette=palette, native_receipt_sha256=sha(LOCAL/'native-full05.json'),outcomes=outcomes)
    json_file(DOC/'geometry.json', document)
    for outcome in outcomes:
        (DOC/f"{outcome['id']}.svg").write_text(svg_map([outcome],palette),encoding='utf8',newline='\n')
    (DOC/'comparison.svg').write_text(svg_map(outcomes,palette,True),encoding='utf8',newline='\n')
    common = []
    for resource in ORDER:
        sets = [{json.dumps(r['points_xyz_width']) for r in o['regions'] if r['resource']==resource} for o in outcomes]
        common.append(dict(resource=resource,shared_paths=len(sets[0]&sets[1]),only_O0=len(sets[0]-sets[1]),only_O3=len(sets[1]-sets[0])))
    # Full primitive coverage check: display bounds do not crop any deposit.
    for outcome in outcomes:
        for region in outcome['regions']:
            for shape in region['primitives']:
                vertices = shape.get('vertices')
                if vertices is None:
                    x,y=shape['center'];r=shape['radius'];vertices=[[x-r,y-r],[x+r,y+r]]
                assert all(-500<=v<=1200 for p in vertices for v in p)
    result = dict(mask_counts=dict(Counter(r['mask'] for r in census)),
                  native_regions=[len(o['regions']) for o in outcomes],spatial_probes=len(native['spatial_checks']),
                  shared_paths=common,artifacts={p.name:sha(p) for p in DOC.iterdir() if p.suffix in ('.csv','.json','.svg')},
                  code_sha256=sha(Path(__file__)))
    json_file(LOCAL/'map-checks.json',result)
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
