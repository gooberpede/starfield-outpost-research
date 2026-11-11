# SPDX-License-Identifier: GPL-3.0-or-later
"""D5BU selected geography reread, adapted from owned CS and B1 methods."""
import argparse
import csv
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import struct
import sys
import zlib
sys.path.insert(0, str(Path(__file__).resolve().parent))
from beacon_terrain_projection import grid_cell, split_local
from d5bt_reader import ROOT, disk_guard, pin, require
from inspect_outpost_definitions import esm_records, subrecords
from outpost_planetary_location import associations, body_catalog
from outpost_record_framing import iter_records
from planet_world_key import find_unit3_context, unit3_world_descriptors
from research_durable_center import resource_rows
from research_two_outpost_anchors import inspect
from research_workshop_components import audit as component_audit
from research_workshop_origin import workshop_prefix
from saved_world_components import find_world_components
from test_outpost_record_framing import independent
from verify_d5bu_controls import decode_member, member_pins
ESM = (1457098709, '1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7')
BA2 = (22468821, '2fb1fff5d8fc074718bf05022c099f3c87ef70e00050229b368ae7d680fbe5d5')
MAPS = {'carinae iii-a.biom': 'bd9a3370b1c1b827cecdbdce318ee1f8af0608c4aade8e4e443968c2a720550f', 'feynman v.biom': 'bd06d24e8ca1788481f6a4388c0e262b863b8b376a521752cf3d286c69f23863', 'kreet.biom': 'd1badcd0b67cc4ff5f67e4199f0383b99ae3aa043e1199a1885011e80cde6b50'}
MEMBERS = {1: 'Save37', 2: 'Save38', 3: 'Kreet39', 40: 'HIST-0267', 47: 'Kreet25', 49: 'HIST-0035', 53: 'Save26'}
PARENTS = {1: '725868', 2: '81482d', 3: '839160'}

def write(path, value):
    with path.open('x', encoding='utf8', newline='\n') as stream:
        json.dump(value, stream, indent=2, sort_keys=True)
        stream.write('\n')

def extract_maps(archive, output):
    require(pin(archive) == BA2, 'BA2_IDENTITY')
    wanted = {f'planetdata/biomemaps/{name}': name for name in MAPS}
    found = set()
    with archive.open('rb') as stream:
        magic, version, kind, count, names = struct.unpack('<4sI4sIQ', stream.read(24))
        require((magic, version, kind) == (b'BTDX', 2, b'GNRL') and 32 + 36 * count <= names < BA2[0], 'BA2_DIRECTORY')
        stream.seek(32)
        entries = [struct.unpack('<I4sIIQIII', stream.read(36)) for _ in range(count)]
        stream.seek(names)
        filenames = [stream.read(int.from_bytes(stream.read(2), 'little')).decode() for _ in entries]
        for name, entry in zip(filenames, entries, strict=True):
            if name not in wanted:
                continue
            short = wanted[name]
            _, _, _, _, offset, packed, size, _ = entry
            require(short not in found and size == 655414 and (32 + 36 * count <= offset <= names - (packed or size)), 'BA2_SELECTED_MEMBER')
            stream.seek(offset)
            data = stream.read(packed or size)
            if packed:
                decoder = zlib.decompressobj()
                data = decoder.decompress(data, size + 1)
                require(decoder.eof and (not decoder.unused_data) and (not decoder.unconsumed_tail), 'BA2_ZLIB')
            require(len(data) == size and hashlib.sha256(data).hexdigest() == MAPS[short], 'BIOME_IDENTITY')
            disk_guard(output, size)
            with (output / short).open('xb') as target:
                target.write(data)
            found.add(short)
    require(found == MAPS.keys() and pin(archive) == BA2, 'BA2_POSTFLIGHT')

def spatial_catalog(esm):
    records = []
    for record, fields in esm_records(esm, {b'PNDT', b'STDT', b'WRLD', b'CELL', b'LCTN'}):
        record['edid'] = fields.get(b'EDID', b'').rstrip(b'\x00').decode('utf8', 'backslashreplace')
        record['fields'] = {k.decode(): v.hex() for k, v in fields.items() if len(v) <= 256}
        records.append(record)
    return records

def fixed_lab(esm, player, model):
    with esm.open('rb') as stream:
        stream.seek(1402105313)
        header = stream.read(24)
        n, flags, form = struct.unpack_from('<III', header, 4)
        require(header[:4] == b'PNDT' and form == 259487 and flags & 262144, 'LAB_PNDT')
        packed = stream.read(n)
    payload = zlib.decompress(packed[4:])
    require(len(payload) == int.from_bytes(packed[:4], 'little'), 'LAB_PNDT_LENGTH')
    lat, lon, world = struct.unpack_from('<ddI', payload, 38856)
    require(world == 3299432 and grid_cell(lon, lat) == (0, 14312, 12774), 'LAB_CELL')
    require(any((tag == b'CNAM' and payload[38856:38876] in field for tag, field in subrecords(payload))), 'LAB_CNAM')
    require(any((p['pair'] == [lon, lat] for p in player['points'])), 'LAB_SAVE37_PAIR')
    case, = [row for row in model['rows'] if row['sample'] == 'Kreet39']
    require(case['world']['offset'] == 278737 and case['descriptor']['offset'] == 3890 and ('02b20e7831e037e0' in case['descriptor'].values()), 'SAVE39_DESCRIPTOR')
    return dict(cell=[0, 14312, 12774], pndt_offset=1402105313, payload_offset=38856)

def extract_save(data, catalog, number):
    x = inspect(data, catalog)
    d = x['directory']
    region = d['regions']['region_R3']
    records = list(iter_records(data, *region, d['words'][9]))
    arithmetic = independent(data, *region, d['words'][9])
    require([(r['offset'], r['end'], r['token'], r['flags']) for r in records] == [r[:4] for r in arithmetic], 'GEOGRAPHY_INDEPENDENT_FRAMING')
    by_pair, by_id = body_catalog(catalog)
    bodykeys = {key: f"{values[0]['formid']:08X}" for key, values in by_pair.items() if len(values) == 1}
    player = None
    if number in PARENTS:
        record, = [r for r in records if r['token'] == '400014']
        parent = record['refs'][0]
        require(parent == PARENTS[number], 'PLAYER_PARENT')
        offset = record['body'] + 1
        _, points = associations(data, *x['global_units'][6], parent, by_pair, by_id)
        player = dict(parent=parent, offset=offset, xyz=struct.unpack_from('<3f', data, offset), points=points)
    for beacon in x['beacons']:
        record = beacon['record']
        q = record['body']
        shape = data[q]
        tail = q + 13 + 4 * sum((bool(shape & 1 << axis) for axis in range(3)))
        beacon['initial_flag'] = data[tail] if not shape & 24 else 32 if shape & 8 else 0
        try:
            beacon['workshop'] = workshop_prefix(data, record, beacon['prefix'], resource_reader=resource_rows)
        except ValueError as error:
            beacon['workshop_error'] = str(error)
    try:
        components = component_audit(data)
    except ValueError as error:
        components = dict(error=str(error))
    try:
        ctx = find_unit3_context(data, d['regions']['region_R1'][0], x['global_units'][4][0] - 8)
        descriptors, end = unit3_world_descriptors(data, ctx)
        desc = dict(context=ctx, descriptors=descriptors, end=end)
    except (ValueError, KeyError) as error:
        desc = dict(error=str(error))
    worlds = None
    if desc.get('descriptors'):
        parents = {int(row['parent_token'], 16) for row in x['beacons']}
        try:
            worlds = find_world_components(data, *x['global_units'][6], parents, bodykeys, desc['descriptors'])
        except ValueError as error:
            worlds = dict(error=str(error))
    return dict(extraction=x, player=player, components=components, descriptors=desc, worlds=worlds)

def readmap(path):
    b = path.read_bytes()
    v, flag, n = struct.unpack_from('<BBI', b)
    assert v == 5
    ids = struct.unpack_from('<' + str(n) + 'I', b, 6)
    p = 6 + 4 * n
    nf = struct.unpack_from('<I', b, p)[0]
    p += 4
    assert nf == 2
    faces = []
    for face in range(nf):
        width, height, count = struct.unpack_from('<III', b, p)
        p += 12
        assert width * height == count and width and height
        off = p
        values = struct.unpack_from('<' + str(count) + 'I', b, p)
        p += 4 * count
        maskcount = struct.unpack_from('<I', b, p)[0]
        p += 4
        assert maskcount == count
        maskoff = p
        p += maskcount
        faces.append(dict(width=width, height=height, offset=off, values=values, maskoffset=maskoff, mask=list(b[maskoff:p])))
    assert p == len(b)
    return dict(version=v, flag=flag, catalog=ids, faces=faces)

def lookup(m, t, i, j):
    u = (i + 0.5) / 49152 - 0.5
    v = (j + 0.5) / 49152 - 0.5
    if t in (2, 3):
        t = int(t != 2)
        u = -u
        v = -v
    face = m['faces'][t]
    w, h = (face['width'], face['height'])
    a = min(w - 1, max(0, math.floor(min(1, max(0, u + 0.5)) * w)))
    b = min(h - 1, max(0, math.floor((1 - min(1, max(0, v + 0.5))) * h)))
    return (face['values'][b * w + a], (t, a, b), face['offset'] + 4 * (b * w + a))

def enumerate_cells(cx, cy, r=150):
    out = []
    for qy in range(math.floor((cy - r) / 100) - 1, math.floor((cy + r) / 100) + 2):
        for qx in range(math.floor((cx - r) / 100) - 1, math.floor((cx + r) / 100) + 2):
            dx = max(qx * 100 - cx, 0, cx - (qx + 1) * 100)
            dy = max(qy * 100 - cy, 0, cy - (qy + 1) * 100)
            d2 = dx * dx + dy * dy
            if d2 < r * r:
                out.append((qx, qy, d2))
    return out

def project(output):
    maps = {body: readmap(output / name) for body, name in [(259487, 'kreet.biom'), (385246, 'feynman v.biom'), (386266, 'carinae iii-a.biom')]}
    rows = []
    inputs = []
    for label in ['HIST-0035', 'HIST-0267', 'Kreet25', 'Kreet39']:
        path = output / (label + '-r3.json')
        x = json.loads(path.read_text())
        inputs.append(pin(path)[1])
        for b in x['extraction']['beacons']:
            body = b['proposed_body_formid']
            names = [n['text'] for n in b['name_for_comparison']]
            name = names[0] if names else 'UNNAMED'
            if body is None and x.get('worlds', {}):
                joined = [v for v in x['worlds'].get('rows', []) if v['world'] == b['parent_token']]
                if len(joined) == 1 and len(b['points']) == 1 and (int(joined[0]['body'], 16) == b['points'][0]['body_formid']):
                    body = int(joined[0]['body'], 16)
            if body not in maps or (label.startswith('HIST') and name not in ['Carinae III-a Rc Fe', 'Feynman V Cu Co Ni IL', 'Feynman V Cu IL F']):
                continue
            wp = b.get('workshop')
            assert wp and wp['delta_hex'] == '000000000000000000000000'
            C = b['local_xyz']
            frame = b['initial_flag']
            site = grid_cell(*b['points'][0]['pair'])
            desc = None
            world = None
            if x.get('worlds', {}) and 'rows' in x['worlds']:
                matches = [a for a in x['worlds']['rows'] if a['world'] == b['parent_token']]
                if len(matches) == 1:
                    world = matches[0]
                if world:
                    matches = [a for a in x['descriptors']['descriptors'] if a['world_token'] == world['secondary'] and a['body'] == world['body']]
                    if len(matches) == 1:
                        desc = matches[0]
            if frame == 11:
                assert desc is not None
                t = desc['tag']
                base = [desc['x'], desc['y']]
                if t in (2, 3):
                    base = [49151 - v for v in base]
            elif frame == 43:
                t, *base = site
                assert t in (0, 1)
            else:
                raise ValueError('UNQUALIFIED_FRAME')
            cells = []
            m = maps[body]
            for qx, qy, d2 in enumerate_cells(*C[:2]):
                i = base[0] + qx
                j = base[1] + qy
                assert 0 <= i < 49152 and 0 <= j < 49152, 'SEAM_NOT_TESTED_HERE'
                fid, pixel, off = lookup(m, t, i, j)
                cells.append(dict(q=[qx, qy], cell=[t, i, j], biome=f'{fid:08x}', pixel=pixel, map_byte_offset=off, min_distance_squared=d2))
            q = [split_local(v)[0] for v in C[:2]]
            actual = [t, base[0] + q[0], base[1] + q[1]]
            for c in cells:
                tt, i, j = c['cell']
                assert tt in (0, 1)
                face = m['faces'][tt]
                assert face['width'] == face['height'] == 256
                col = i // 192
                row = 255 - j // 192
                assert list(c['pixel']) == [tt, col, row]
                raw = (output / ('kreet.biom' if body == 259487 else 'feynman v.biom' if body == 385246 else 'carinae iii-a.biom')).read_bytes()
                assert int.from_bytes(raw[c['map_byte_offset']:c['map_byte_offset'] + 4], 'little') == int(c['biome'], 16)
            margin = min((abs(math.sqrt(c['min_distance_squared']) - 150) for c in cells))
            for qy in range(math.floor((C[1] - 150) / 100) - 1, math.floor((C[1] + 150) / 100) + 2):
                for qx in range(math.floor((C[0] - 150) / 100) - 1, math.floor((C[0] + 150) / 100) + 2):
                    dx = max(qx * 100 - C[0], 0, C[0] - (qx + 1) * 100)
                    dy = max(qy * 100 - C[1], 0, C[1] - (qy + 1) * 100)
                    margin = min(margin, abs(math.hypot(dx, dy) - 150))
            assert margin > 0.001
            row = dict(sample=label, save=x['source'], decoded_sha256=x['metrics']['decoded_sha256'], name=name, token=b['token'], parent=b['parent_token'], record_offset=b['record']['offset'], xyz_offset=b['xyz_offset'], body=f'{body:08x}', frame=f'{frame:02x}', center=C, workshop=wp, site=list(site), world=world, descriptor=desc, base=[t, *base], center_cell=actual, cells=cells, biomes=sorted({c['biome'] for c in cells}), numeric_boundary_margin=margin, coverage='CONDITIONAL_SAVED_FRAME_ORDINARY_BASE_BIOME')
            rows.append(row)
            print(label, name, 'base', row['base'], 'center', actual, 'cells', len(cells), 'biomes', row['biomes'], 'margin', margin)
    checks = {}
    disk = enumerate_cells(150, 150, 150)
    checks['enclosed_cell_included'] = (1, 1) in [(x, y) for x, y, d in disk]
    checks['enclosed_cell_no_circle_boundary'] = max((math.hypot(x - 150, y - 150) for x in (100, 200) for y in (100, 200))) < 150
    checks['tangent_cell_excluded'] = not any((x == 3 and y == 1 for x, y, d in disk))
    checks['negative_floor_included'] = any((x == -2 for x, y, d in enumerate_cells(-0.1, 0)))
    checks['strict_small_cap_included'] = any((x == 2 and y == 0 for x, y, d in enumerate_cells(50.00001, 50)))
    checks['strict_small_gap_excluded'] = not any((x == 2 and y == 0 for x, y, d in enumerate_cells(49.99999, 50)))
    for body, m in maps.items():
        for t in (0, 1):
            for i, j in [(0, 0), (191, 191), (192, 192), (49151, 49151), (25124, 32448)]:
                a = lookup(m, t, i, j)
                tt, xx, yy = a[1]
                checks[f'raster-{body:x}-{t}-{i}-{j}'] = xx == i // 192 and yy == 255 - j // 192
        for t, normal in [(2, 0), (3, 1)]:
            checks[f'reflection-{body:x}-{t}'] = lookup(m, t, 120, 456)[0] == lookup(m, normal, 49031, 48695)[0]
    assert all(checks.values()), checks
    return dict(rows=rows, checks=checks, input_receipt_sha256=inputs)

def verify_oracle(model, extractions):

    def table(name):
        path = ROOT / 'docs/experiments/outpost-biomes' / name
        with path.open(encoding='utf8', newline='') as stream:
            return list(csv.DictReader(stream))
    assert all(model['checks'].values())
    rows = {(r['sample'], r['token']): r for r in model['rows']}
    cases = [r for r in table('cases.csv') if (r['sample'], r['token']) in rows]
    assert len(cases) == len(rows) == 9
    expected_cells = set()
    for r in table('cells.csv'):
        if (r['sample'], r['token']) not in rows:
            continue
        expected_cells.add((r['sample'], r['token'], *[int(r[k]) for k in ('local_qx', 'local_qy', 'tag', 'fine_I', 'fine_J')], r['biome'], *[int(r[k]) for k in ('face', 'pixel_column', 'pixel_row', 'map_member_byte_offset')]))
    actual_cells = set()
    for expected in cases:
        key = (expected['sample'], expected['token'])
        r = rows[key]
        assert r['base'] == json.loads(expected['selected_base'])
        assert r['center_cell'] == json.loads(expected['center_cell'])
        assert r['record_offset'] == int(expected['record_decoded_offset'])
        assert r['center'] == json.loads(expected['center_xyz'])
        assert r['frame'] == expected['frame'] and r['parent'] == expected['parent']
        if expected['descriptor_key']:
            assert r['descriptor']['offset'] == int(expected['descriptor_decoded_offset'])
            assert expected['descriptor_key'] in r['descriptor'].values()
            assert r['world']['offset'] == int(expected['world_decoded_offset'])
        else:
            assert r['descriptor'] is None
        observed = {tuple(c['q']) for c in r['cells']}
        x, y = map(Fraction, r['center'][:2])
        exact = set()
        for i in range(math.floor((x - 150) / 100), math.floor((x + 150) / 100) + 1):
            for j in range(math.floor((y - 150) / 100), math.floor((y + 150) / 100) + 1):
                dx = max(i * 100 - x, 0, x - (i + 1) * 100)
                dy = max(j * 100 - y, 0, y - (j + 1) * 100)
                if dx ** 2 + dy ** 2 < 22500:
                    exact.add((i, j))
        assert exact == observed
        for c in r['cells']:
            actual_cells.add((*key, *c['q'], *c['cell'], c['biome'], *c['pixel'], c['map_byte_offset']))
    assert actual_cells == expected_cells
    a, b, c = (extractions[label]['extraction'] for label in ('Save37', 'Save38', 'Kreet39'))
    assert [len(x['beacons']) for x in (a, b, c)] == [0, 0, 1]
    assert c['beacons'][0]['token'] == '841421'
    old, new = (extractions[label]['extraction']['beacons'] for label in ('Kreet25', 'Save26'))
    for r in new:
        wp = r['workshop']
        prior, = [o for o in old if o['workshop']['identifier98_hex'] == wp['identifier98_hex']]
        delta = struct.unpack('<3f', bytes.fromhex(wp['delta_hex']))
        assert struct.pack('<3f', *(x + y for x, y in zip(r['local_xyz'], delta))) == bytes.fromhex(prior['xyz_hex'])
        assert r['points'][0]['pair_hex'] == prior['points'][0]['pair_hex']
    assert '140d4ae40' in extractions['Kreet25']['components']['error']
    neg, = [r for r in extractions['HIST-0267']['extraction']['beacons'] if r['token'] == '84ede9']
    anchor = grid_cell(*neg['points'][0]['pair'])
    assert anchor[1] == 13152 and neg['initial_flag'] == 43
    assert anchor[1] + math.floor(neg['local_xyz'][0] / 100) == 13151
    x, y = [extractions[label]['player']['xyz'] for label in ('Save38', 'Kreet39')]
    require(struct.pack('<2f', *x[:2]) == struct.pack('<2f', *y[:2]) and abs(x[2] - y[2]) == 1.52587890625e-05, 'PLAYER_POSITION_CONTROL')
    return dict(cases=len(cases), cells=len(actual_cells), negative_x=13151)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--member', nargs=2, action='append', required=True, metavar=('ID', 'PATH'))
    parser.add_argument('--esm', required=True, type=Path)
    parser.add_argument('--planet-data', required=True, type=Path)
    parser.add_argument('--output-directory', required=True, type=Path)
    args = parser.parse_args()
    require(sys.flags.isolated and sys.dont_write_bytecode and __debug__, 'USE_PYTHON_I_B')
    paths = {int(number): Path(path).resolve(strict=True) for number, path in args.member}
    require(paths.keys() == MEMBERS.keys() and len(set(paths.values())) == len(args.member), 'GEOGRAPHY_SELECTION')
    output = args.output_directory.resolve()
    require(output.parent.is_dir(), 'OUTPUT_PARENT')
    disk_guard(output.parent)
    require(pin(args.esm) == ESM, 'GEOGRAPHY_ESM')
    pins = member_pins()
    output.mkdir()
    try:
        extract_maps(args.planet_data, output)
        catalog = spatial_catalog(args.esm)
        extractions = {}
        for number, label in MEMBERS.items():
            with decode_member(number, paths[number], output, pins) as (data, metrics):
                row = extract_save(data, catalog, number)
                metrics = {key: value for key, value in metrics.items() if key != 'seconds'}
                row.update(source=dict(sha256=pins[f'B4-F{number:03}'][1]), metrics=metrics)
                extractions[label] = row
            disk_guard(output)
            write(output / f'{label}-r3.json', row)
        model = project(output)
        require('descriptors' not in extractions['HIST-0035']['descriptors']
                and extractions['HIST-0035']['descriptors'].get('error'),
                'HIST0035_DESCRIPTOR_AMBIGUITY')
        checks = verify_oracle(model, extractions)
        lab = fixed_lab(args.esm, extractions['Save37']['player'], model)
        require(pin(args.esm) == ESM and pin(args.planet_data) == BA2, 'GEOGRAPHY_SOURCE_CHANGED')
        write(output / 'result.json', dict(model=model, oracle=checks, lab=lab))
    except Exception as error:
        write(output / 'failure.json', dict(error=type(error).__name__, detail=str(error)))
        raise
if __name__ == '__main__':
    main()
