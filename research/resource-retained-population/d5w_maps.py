# SPDX-License-Identifier: GPL-3.0-or-later
"""Render original D5W sampling and causal figures from authored evidence.

Reads D5T candidates, C1 native references and the frozen D5W point receipt. Writes SVG,
CSV and JSON into a fresh directory. Reuses owned D5V SVG text/frame primitives;
no native execution, raw save, installed data, Ghidra or network access.
"""
from pathlib import Path
import csv
import hashlib
import json
import math
import sys
import xml.etree.ElementTree as ET
from d5v_maps import start, native_panel
from d5u_c1_maps import text, finish

ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / 'docs/experiments/resource-retained-population'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def box(lines, x, y, w, labels, color='#ffffff'):
    height = 24 * len(labels) + 22
    lines.append(f'<rect x="{x}" y="{y}" width="{w}" height="{height}" rx="8" fill="{color}" stroke="#708da0"/>')
    for i, label in enumerate(labels):
        lines.append(text(x + 14, y + 26 + i * 24, label, 15))
    return height


def arrow(lines, x1, y1, x2, y2, conditional=False):
    dash = 'stroke-dasharray="7 5"' if conditional else ''
    lines.append(f'<path d="M{x1} {y1}L{x2} {y2}" fill="none" stroke="#466a82" stroke-width="2" {dash} marker-end="url(#arrow)"/>')


def main():
    output = Path(sys.argv[1]).resolve()
    assert not output.exists()
    output.mkdir(parents=True)
    candidate_path = DOC / 'd5t/candidates.csv'
    with candidate_path.open(encoding='utf8') as stream:
        candidates = list(csv.DictReader(stream))
    reference_path = DOC / 'd5u/outposts/D2-84e101.json'
    ref = json.loads(reference_path.read_text())['reference']
    assert ref['descriptor'] == [37536, 20928]
    center = ref['center'][:2]
    lattice = [dict(original_int2=[int(r['local_x']), int(r['local_y'])],
                    native_xy=[100 * int(r['local_x']), 100 * int(r['local_y'])],
                    body_face=[int(r['face_x']), int(r['face_y'])],
                    mask=int(r['mask']), registration_index=int(r['registration_index']),
                    qualification=r['feasibility']) for r in candidates]
    lines = start('Sampling locations and proposed authority · Feynman V Cu IL F', 1050)
    for i, label in enumerate([
        'Prospective D5S descriptor O = (37536, 20928), chart 0; source anchor A = O.',
        'Absolute native descriptor-frame X/Y below. The outpost centre is (81.19074249267578, 90.27748107910156).',
        'Colored cells classify integer query nodes only; continuous raster boundaries and retail frequency are not measured.'
    ]):
        lines.append(text(32, 77 + i * 25, label, 14))
    left, top, size = 100, 185, 630
    lo, hi = -400, 1400
    scale = size / (hi - lo)
    def point(x, y):
        return left + (x - lo) * scale, top + (hi - y) * scale
    lines.append(f'<rect x="{left}" y="{top}" width="{size}" height="{size}" fill="white" stroke="#708da0"/>')
    for row in lattice:
        x, y = point(*row['native_xy'])
        color = '#d7e6f5' if row['mask'] == 3 else '#f7dfb3'
        lines += [f'<rect data-query="{row["original_int2"][0]},{row["original_int2"][1]}" data-mask="{row["mask"]}" x="{x:.6f}" y="{y-100*scale:.6f}" width="{100*scale}" height="{100*scale}" fill="{color}" stroke="#ffffff"/>',
                  f'<circle cx="{x:.6f}" cy="{y:.6f}" r="1.8" fill="#6c7982"/>']
    for value in range(-400, 1401, 200):
        x, y = point(value, value)
        lines += [text(x, top + size + 23, str(value), 12, 'text-anchor="middle"'),
                  text(left - 10, y + 4, str(value), 12, 'text-anchor="end"')]
    def rectangle(low, high, color, dash):
        x, y = point(low, high)
        lines.append(f'<rect x="{x:.6f}" y="{y:.6f}" width="{(high-low)*scale}" height="{(high-low)*scale}" fill="none" stroke="{color}" stroke-width="2.5" stroke-dasharray="{dash}"/>')
    rectangle(0, 1000, '#1e4967', '1 0')
    rectangle(-200, 1200, '#7d3e77', '7 4')
    cx, cy = point(*center)
    lines.append(f'<circle data-role="outpost-disk" data-native-x="{center[0]}" data-native-y="{center[1]}" cx="{cx}" cy="{cy}" r="{150*scale}" fill="none" stroke="#1c2730" stroke-width="1.5"/>')
    markers = [
        ('D5S owner winner', [1000, 1100], 'winner', '#12633c'),
        ('D5S peer winner', [-200, -200], 'winner', '#8c4015'),
        ('Earliest registration / incremental claim', [-200, 1100], 'claim', '#186a9e'),
        ('Source anchor / quantized beacon candidate', [0, 0], 'hypothesis', '#874398'),
        ('Nominal footprint centre', [500, 500], 'hypothesis', '#874398'),
        ('Generator clipping centre', [300, 300], 'hypothesis', '#874398'),
        ('Saved centre / beacon', center, 'reference', '#172630')]
    for label, xy, kind, color in markers:
        x, y = point(*xy)
        if kind == 'winner':
            shape = f'<circle cx="{x}" cy="{y}" r="7" fill="{color}" stroke="white" stroke-width="2"/>'
        elif kind == 'claim':
            shape = f'<path d="M{x} {y-9}l8 15h-16Z" fill="{color}" stroke="white" stroke-width="2"/>'
        elif kind == 'reference':
            shape = f'<path d="M{x-7} {y}h14 M{x} {y-7}v14" stroke="{color}" stroke-width="2"/>'
        else:
            shape = f'<rect x="{x-6}" y="{y-6}" width="12" height="12" fill="white" stroke="{color}" stroke-width="2" stroke-dasharray="3 2"/>'
        lines.append(shape)
    legends = [
        'Solid outline: nominal [0, 1000)².',
        'Dashed outline: query support [-200, 1200)².',
        'Blue cells: mask 3; amber cells: mask 0.',
        'Gray dots: individually unproved candidates.',
        'Solid disks: D5S proved first-miss witnesses.',
        'Triangle: incremental queue claim only.',
        'Purple squares: proposed canonical locations;',
        'no native authoritative use is established.',
        'Black cross: qualified historical saved centre.',
        'Circle: full 150-native-unit reference radius.',
        '',
        'Owner: Int2 (10, 11) → (1000, 1100), mask 3.',
        'Peer: Int2 (-2, -2) → (-200, -200), mask 0.',
        'Early: Int2 (-2, 11) → (-200, 1100), mask 3.',
        '',
        'Source anchor: (0, 0); nominal centre: (500, 500).',
        'Generator origin: (-200, -200); clip centre: (300, 300).',
        'Saved beacon floors to cell (0, 0) if used as a root;',
        'the area consumer does not make it authoritative.'
    ]
    for i, label in enumerate(legends):
        lines.append(text(770, 205 + i * 29, label, 13))
    lines += [text(415, 875, 'Absolute native descriptor-frame X (native units)', 15, 'text-anchor="middle"'),
              '<text x="30" y="500" font-size="15" text-anchor="middle" transform="rotate(-90 30 500)">Absolute native descriptor-frame Y (native units)</text>',
              text(32, 930, 'Node display: native XY = 100 × original Int2; body-face cells = O + Int2. Native query-to-chart arithmetic remains D5S/D5T-qualified.', 13),
              text(32, 959, 'Origin (0, 0) is the actual descriptor/source anchor coincidence in this specified frame; no outpost-centred translation is applied.', 13),
              text(32, 988, 'The historical reference shares this descriptor, but its loaded epoch is unknown. Shapes and whole-outpost alternatives are in the linked C1 views.', 13)]
    (output / 'sampling.svg').write_text(finish(lines), encoding='utf8', newline='\n')
    # Paired causal paths deliberately share an initialization prefix.
    lines = start('Paired critical paths · first constructing miss', 1190)
    lines += [text(32, 78, 'Solid arrows: proved local prerequisites. Dashed arrows: selected scheduling continuation; no duration or probability scale.', 15)]
    box(lines, 110, 110, 1060, [
        'Initialize descriptor / owner / empty ProcGen → complete source Grid → write valid terrain focus.',
        'RuntimeService AcquireHandles → placement/file preparation → inclusive [-16, 23]² registration.',
        'Coordinate → layer preparation + density neighbors → ready ProcGen service commands → actual worker queue.'
    ])
    arrow(lines, 360, 205, 360, 270)
    arrow(lines, 920, 205, 920, 270)
    for x, route in [(80, 'Owner'), (700, 'Peer')]:
        labels = ([
            'Owner continuation: activation batch complete.',
            'ProcGen pump returns; owner claims local back.',
            'Import rotation is included; no global FIFO.'
        ] if route == 'Owner' else [
            'Peer continuation: activation batch complete.',
            'ProcGen pump is preempted; peer claims front.',
            'Completion wakes do not add a second running pump.'
        ])
        box(lines, x, 270, 500, labels)
        arrow(lines, x + 250, 365, x + 250, 425, True)
        labels = ([
            '58 earlier density claims are outside target support.',
            'Index 845: original Int2 (10, 11), mask 3.',
            'Source selection; shared visited check false.'
        ] if route == 'Owner' else [
            '28 earlier density claims are outside target support.',
            'Index 874: original Int2 (-2, -2), mask 0.',
            'Source selection; shared visited check false.'
        ])
        box(lines, x, 425, 500, labels)
        arrow(lines, x + 250, 520, x + 250, 585)
        box(lines, x, 585, 500, [
            'Exclusive ProcGen +0x40 acquire → map lookup.',
            'First miss → insert wrapper → synchronous generation.',
            'Publish visited; later map hits retain the sample.'
        ], '#eaf2f6')
    box(lines, 80, 760, 1120, [
        'Both D5S witnesses keep ContentManager layer preparation pending and delay competing cell/terrain routes.',
        'These are permitted native scheduling choices, not measured ordinary arrival frequencies or exceptional-state tests.',
        'Layer (-2, 11) has no target-capable density neighbor: releasing preparation adds a real competing path.',
        'Other ordinary ingress: cell singleton; admitted bounded-LOD 3×3; terrain file/height work; warm key/aggregate reuse.'
    ])
    box(lines, 80, 935, 1120, [
        'Incremental opportunity: target query (-2, 11) registers at 419; first mask-0 density query registers at 833.',
        'If early target work runs to the miss before overtaking work, mask 3 has a causal head start of 414 registrations.',
        'No latency bound enforces this. Batch 875 gives owner mask 0; whole-batch owner/peer can give opposite masks.',
        'Native claims are token-queue controls. Full ordinary ingress and source-map arbitration remain separate evidence.'
    ], '#fff6e7')
    (output / 'critical-paths.svg').write_text(finish(lines), encoding='utf8', newline='\n')
    lines = start('Three stability targets across population transitions', 840)
    box(lines, 50, 120, 370, ['Same retained episode', 'No reset, erasure or invalid lifetime.', 'Successful copied regions remain owned.'], '#eaf2f6')
    box(lines, 455, 120, 370, ['Qualified broad reset', 'Map and visited state cleared.', 'New successful demand may construct.'], '#fff6e7')
    box(lines, 860, 120, 370, ['Fresh loading / new manager', 'Taken reset or fresh stores.', 'Old pointers do not persist as identity.'], '#fff6e7')
    arrow(lines, 420, 165, 455, 165)
    arrow(lines, 825, 165, 860, 165)
    labels = [
        ['Area resource identities', 'Same admitted geometry and query → same set.', 'Different shapes can still return the same names.'],
        ['Exact deposit geometry', 'Stable held geometry is a retention contract.', 'Fresh equality needs complete inputs and winner class.'],
        ['Fixed extractor availability', 'Point predicate ∩ effective produced resources.', 'Area equality does not imply point equality.']
    ]
    for i, label in enumerate(labels):
        box(lines, 70, 300 + i * 145, 1130, label)
    lines += [text(32, 780, 'Retirement alone can leave visited state and suppress reconstruction. None of these arrows asserts a retail variation rate or bug cause.', 14)]
    (output / 'stability.svg').write_text(finish(lines), encoding='utf8', newline='\n')
    # Reuse qualified native deposit silhouettes; add the newly tested fixed point.
    point_receipt_path = ROOT / '.local-work/d5w/point01.json'
    point_receipt = json.loads(point_receipt_path.read_text())
    geometry = json.loads(reference_path.read_text())
    assert point_receipt['source_geometry_sha256'] == sha(reference_path)
    assert [r['accepted'] for r in point_receipt['results']] == [False, True]
    query = point_receipt['query'][:2]
    selections = [[v for v in geometry['layers'] if v['variant_count'] == 1 or
                   (v['source_id'] == 'U25' and v['mask'] == mask)] for mask in (0, 3)]
    lines = start('Equal area identities; different resource admission at one fixed point', 1610)
    lines += [text(32, 78, 'Feynman V Cu IL F · conditional historical native descriptor frame · no observed gameplay transition', 15),
              text(32, 106, 'P = ' + str(point_receipt['query']) + ' native XYZ; Ionic Liquids point predicate: mask 0 rejects, mask 3 accepts.', 14),
              text(32, 134, 'Both 150-unit area sets remain Copper / Fluorine / Ionic Liquids. Other placement gates and produced-resource state are conditional.', 14)]
    bounds = [r['native_bound'] for selection in selections for layer in selection for r in layer['regions']]
    cx, cy = center
    xmin = min([cx - 150] + [b[0] - max(b[3], .5) for b in bounds])
    xmax = max([cx + 150] + [b[0] + max(b[3], .5) for b in bounds])
    ymin = min([cy - 150] + [b[1] - max(b[3], .5) for b in bounds])
    ymax = max([cy + 150] + [b[1] + max(b[3], .5) for b in bounds])
    span = max(xmax - xmin, ymax - ymin) + 80
    mx, my = (xmin + xmax) / 2, (ymin + ymax) / 2
    full = [mx - span / 2, mx + span / 2, my - span / 2, my + span / 2]
    point_panels = []
    for row, viewport in enumerate(([cx - 240, cx + 240, cy - 240, cy + 240], full)):
        for i, selection in enumerate(selections):
            panel = native_panel(lines, f'point-{row}-{i}', 80 + 620 * i, 225 + row * 700,
                                 480, viewport, center, 150, selection, geometry['palette'],
                                 ('Detail' if row == 0 else 'Full extent') + f' · mask {0 if i == 0 else 3}',
                                 'Ionic Liquids at P: ' + ('REJECT' if i == 0 else 'ACCEPT'))
            px = panel['left'] + (query[0] - viewport[0]) * panel['scale']
            py = panel['top'] + (viewport[3] - query[1]) * panel['scale']
            lines += [f'<path data-role="fixed-point" data-native-x="{query[0]}" data-native-y="{query[1]}" d="M{px-7} {py-7}l14 14 M{px-7} {py+7}l14 -14" stroke="white" stroke-width="5"/>',
                      f'<path d="M{px-7} {py-7}l14 14 M{px-7} {py+7}l14 -14" stroke="#bd263c" stroke-width="2.5"/>',
                      text(px + 10, py + 18, 'P', 14, 'fill="#9b1831" paint-order="stroke" stroke="white" stroke-width="3"')]
            panel['fixed_point_native'] = query
            panel['fixed_point_pixels'] = [px, py]
            point_panels.append(panel)
    lines += [text(32, 1530, 'Red X: identical test point. Black centre / beacon / circle: qualified saved reference and full 150-native-unit radius.', 14),
              text(32, 1558, 'IRES TINC: dark green Copper; green Fluorine; turquoise Ionic Liquids. All relevant source layers included; U23 has zero disk overlap.', 13),
              text(32, 1586, 'Silhouettes approximate marginal segment rounding. Acceptance is the original executed native point predicate, not a pixel test.', 13)]
    (output / 'fixed-point.svg').write_text(finish(lines), encoding='utf8', newline='\n')
    context_rejections = []
    for layer in geometry['layers']:
        if layer['source_id'] == 'U25':
            continue
        regions = [r for r in layer['regions'] if r['resource'] == point_receipt['resource']]
        margins = [math.dist(query, r['native_bound'][:2]) - max(r['native_bound'][3], .5) for r in regions]
        assert all(m > 0 for m in margins)
        context_rejections.append(dict(layer=layer['id'], resource_regions=len(regions),
                                       minimum_outside_bound_native=min(margins) if margins else None,
                                       classification='DERIVED rejection by the native XY broadphase bound; not new execution'))
    point_data = dict(query=point_receipt['query'], resource=point_receipt['resource'],
                      scope=point_receipt['scope'], source_geometry_sha256=sha(reference_path),
                      native_receipt_sha256=sha(point_receipt_path),
                      results=point_receipt['results'], context_rejections=context_rejections,
                      panels=point_panels)
    (output / 'point-comparison.json').write_text(json.dumps(point_data, indent=2) + '\n', encoding='utf8', newline='\n')
    with (output / 'sampling.csv').open('w', encoding='utf8', newline='') as stream:
        writer = csv.writer(stream, lineterminator='\n')
        writer.writerow(['query_x', 'query_y', 'native_x', 'native_y', 'face_x', 'face_y', 'mask', 'registration_index', 'qualification'])
        for row in lattice:
            writer.writerow(row['original_int2'] + row['native_xy'] + row['body_face'] +
                            [row['mask'], row['registration_index'], row['qualification']])
    model = dict(schema='sor-d5w-figures/1', frame='Absolute native descriptor-frame XY; prospective D5S descriptor [37536,20928], chart 0',
                 sampling=dict(descriptor=ref['descriptor'], source_anchor=[0, 0], nominal=[0, 1000], support=[-200, 1200],
                               center=center, radius=150, native_units_per_cell=100, viewport=[lo, hi, lo, hi],
                               pixel_left=left, pixel_top=top, pixel_size=size, pixels_per_native_unit=scale,
                               markers=[dict(label=a, native_xy=b, classification=c) for a, b, c, _ in markers]),
                 inputs={str(p.relative_to(ROOT)): sha(p) for p in [candidate_path, reference_path, DOC / 'd5v/spatial.json']},
                 reused_outpost_figures={str((DOC / 'd5v' / n).relative_to(ROOT)): sha(DOC / 'd5v' / n)
                                        for n in ('D2-83388f.svg', 'D2-84e101.svg')},
                 limits='Discrete query classification; canonical samples are hypotheses; conditional retained geometry and historical references, not retail overlays',
                 renderer_sha256=sha(__file__))
    for path in output.glob('*.svg'):
        ET.fromstring(path.read_text(encoding='utf8'))
    (output / 'figures.json').write_text(json.dumps(model, indent=2) + '\n', encoding='utf8', newline='\n')
    print('Rendered sampling, paired paths and stability; pinned existing full-extent outpost comparisons.')


if __name__ == '__main__':
    main()
