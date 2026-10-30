# SPDX-License-Identifier: GPL-3.0-or-later
"""Check D5W figure fidelity, exact native point inputs and deterministic replay.

Reads authored figures/geometry and frozen local point evidence. Runs the owned
SVG renderer into fresh ignored scratch; writes a new check receipt. No native
execution, game, raw save, Ghidra, network or Git mutation.
"""
from pathlib import Path
import csv
import hashlib
import json
import math
import subprocess
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / 'docs/experiments/resource-retained-population'
NS = '{http://www.w3.org/2000/svg}'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding='utf8'))


def main():
    output = Path(sys.argv[1]).resolve()
    assert output.is_relative_to(ROOT / '.local-work') and not output.exists()
    output.mkdir(parents=True)
    data = DOC / 'd5w'
    metadata = read(data / 'figures.json')
    assert metadata['renderer_sha256'] == sha(Path(__file__).with_name('d5w_maps.py'))
    for p, h in metadata['inputs'].items():
        assert sha(ROOT / p) == h, p
    for p, h in metadata['reused_outpost_figures'].items():
        assert sha(ROOT / p) == h, p
    files = sorted(data.glob('*.svg'))
    assert len(files) == 4
    for path in files:
        root = ET.parse(path).getroot()
        ids = [e.attrib['id'] for e in root.iter() if 'id' in e.attrib]
        assert len(ids) == len(set(ids)), path.name
        assert root.find(NS + 'title') is not None
    sampling = ET.parse(data / 'sampling.svg').getroot()
    with (data / 'sampling.csv').open(encoding='utf8') as stream:
        queries = list(csv.DictReader(stream))
    rectangles = {e.attrib['data-query']: e for e in sampling.iter(NS + 'rect') if 'data-query' in e.attrib}
    assert len(queries) == len(rectangles) == 196
    s = metadata['sampling']
    scale = s['pixels_per_native_unit']
    low, high, _, _ = s['viewport']
    error = 0
    for q in queries:
        key = q['query_x'] + ',' + q['query_y']
        e = rectangles[key]
        assert e.attrib['data-mask'] == q['mask']
        nx, ny = float(q['native_x']), float(q['native_y'])
        assert nx == 100 * int(q['query_x']) and ny == 100 * int(q['query_y'])
        assert int(q['face_x']) == 37536 + int(q['query_x'])
        assert int(q['face_y']) == 20928 + int(q['query_y'])
        px = s['pixel_left'] + (nx - low) * scale
        py = s['pixel_top'] + (high - ny - 100) * scale
        error = max(error, abs(float(e.attrib['x']) - px), abs(float(e.attrib['y']) - py))
    assert error < 1e-6
    point = read(data / 'point-comparison.json')
    native = read(ROOT / '.local-work/d5w/point01.json')
    assert sha(ROOT / '.local-work/d5w/point01.json') == point['native_receipt_sha256']
    assert native['wrapper_sha256'] == sha(Path(__file__).with_name('d5w_point.py'))
    assert point['query'] == native['query'] and point['results'] == native['results']
    geometry = read(DOC / 'd5u/outposts/D2-84e101.json')
    assert sha(DOC / 'd5u/outposts/D2-84e101.json') == point['source_geometry_sha256']
    assert math.dist(point['query'][:2], geometry['reference']['center'][:2]) < 150
    for result in native['results']:
        layer = next(v for v in geometry['layers'] if v['source_id'] == 'U25' and v['mask'] == result['mask'])
        regions = [r for r in layer['regions'] if r['resource'] == '000057d4']
        assert len(regions) == len(result['regions'])
        for r, actual in zip(regions, result['regions']):
            expected = hashlib.sha256(bytes.fromhex(r['native_bound_le'] + r['ordered_xyzw_le'])).hexdigest()
            assert actual['geometry_sha256'] == expected
    assert [r['accepted'] for r in point['results']] == [False, True]
    other_count = 0
    for row in point['context_rejections']:
        layer = next(v for v in geometry['layers'] if v['id'] == row['layer'])
        regions = [r for r in layer['regions'] if r['resource'] == point['resource']]
        assert layer['source_id'] != 'U25' and len(regions) == row['resource_regions']
        margins = [math.dist(point['query'][:2], r['native_bound'][:2]) - max(r['native_bound'][3], .5) for r in regions]
        assert all(m > 179 for m in margins)
        assert (min(margins) if margins else None) == row['minimum_outside_bound_native']
        other_count += len(regions)
    assert other_count == 29
    root = ET.parse(data / 'fixed-point.svg').getroot()
    fixed = [e for e in root.iter(NS + 'path') if e.attrib.get('data-role') == 'fixed-point']
    circles = [e for e in root.iter(NS + 'circle') if e.attrib.get('data-role') == 'outpost-disk']
    assert len(fixed) == 4 and len(circles) == 8
    numerical = 0
    for panel, marker in zip(point['panels'], fixed):
        xmin, xmax, ymin, ymax = panel['bounds_native']
        scale = panel['scale']
        x, y = point['query'][:2]
        expected = [panel['left'] + (x - xmin) * scale, panel['top'] + (ymax - y) * scale]
        assert expected == panel['fixed_point_pixels']
        assert float(marker.attrib['data-native-x']) == x
        assert float(marker.attrib['data-native-y']) == y
        assert marker.attrib['d'].startswith(f'M{expected[0]-7} {expected[1]-7}')
        group = next(e for e in root.iter(NS + 'g') if e.attrib.get('id') == panel['id'])
        for circle in group.iter(NS + 'circle'):
            if circle.attrib.get('data-role') == 'outpost-disk':
                assert abs(float(circle.attrib['r']) / scale - 150) < 1e-7
        for r in [r for v in geometry['layers'] if v['id'] in panel['layer_ids'] for r in v['regions']]:
            for xy in [r['native_bound'][:2]] + [p[:2] for p in r['points']]:
                px, py = panel['left'] + (xy[0] - xmin) * scale, panel['top'] + (ymax - xy[1]) * scale
                back = [xmin + (px - panel['left']) / scale, ymax - (py - panel['top']) / scale]
                assert max(abs(a - b) for a, b in zip(xy, back)) < 1e-9
                numerical += 1
            if '-1-' in panel['id']:
                bx, by, _, radius = r['native_bound']
                assert xmin <= bx - max(radius, .5) and bx + max(radius, .5) <= xmax
                assert ymin <= by - max(radius, .5) and by + max(radius, .5) <= ymax
    subprocess.run([sys.executable, '-B', str(Path(__file__).with_name('d5w_maps.py')), str(output / 'replay')], check=True)
    replay = [p for p in (output / 'replay').iterdir()]
    assert len(replay) == 7
    for p in replay:
        assert p.read_bytes() == (data / p.name).read_bytes(), p.name
    result = dict(schema='sor-d5w-figure-checks/1', sampling_nodes=196,
                  max_sampling_pixel_error=error, fixed_point_panels=4,
                  numerical_roundtrips=numerical, full_extent_bound_containment='PASS',
                  point_geometry_identity='PASS', other_source_ionic_bounds_rejected=other_count,
                  svg_replay='byte identical',
                  sources={str(p.relative_to(ROOT)): sha(p) for p in files},
                  method_sha256=sha(__file__))
    (output / 'checks.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf8', newline='\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
