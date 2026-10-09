"""SPDX-License-Identifier: GPL-3.0-or-later
SOR-EXP-0013 offline numerical audit, original project code, stdlib only.
Reads frozen EXP0012 manifests/catalog, then original and archived saves and
installed ESM. Re-extracts associations without names/network JSON. Writes
exclusive ignored receipts/selected numeric CSV; decoder removes own scratch.
No target execution, database changes, network, save edits or Git operations.
Analytical spherical equations are not a bit-exact engine implementation.
"""
import argparse
import csv
import json
import math
from pathlib import Path
import struct
import zlib

from inventory_historical_saves import ROOT, identity, guard
from inspect_outpost_definitions import esm_records, subrecords
from outpost_planetary_location import extract, associations, body_catalog
from stream_save import decoded_save
from validate_mature_outposts import directory
from outpost_record_framing import iter_records


def spherical(longitude, latitude):
    if not all(math.isfinite(v) for v in (longitude, latitude)):
        raise ValueError('NONFINITE')
    if not -math.pi / 2 <= latitude <= math.pi / 2:
        raise ValueError('LATITUDE_RANGE')
    c = math.cos(latitude)
    return c * math.cos(longitude), c * math.sin(longitude), math.sin(latitude)


def angles(x, y, z):
    if not all(math.isfinite(v) for v in (x, y, z)) or (x == y == z == 0):
        raise ValueError('INVALID_DIRECTION')
    return math.atan2(y, x), math.atan2(z, math.hypot(x, y))


def audit_pair(raw):
    if len(raw) != 16:
        raise ValueError('PAIR_SIZE')
    lon, lat = struct.unpack('<2d', raw)
    v = spherical(lon, lat)
    a, b = angles(*v)
    error = max(abs(math.remainder(a-lon, 2*math.pi)), abs(b-lat))
    return dict(longitude_rad=lon, latitude_rad=lat,
                longitude_deg=math.degrees(lon), latitude_deg=math.degrees(lat),
                direction_x=v[0], direction_y=v[1], direction_z=v[2],
                roundtrip_error_rad=error, norm_error=abs(math.hypot(*v)-1),
                latitude_first_radians_valid=abs(lon) <= math.pi/2,
                normalized_signed_pair_valid=max(abs(lon), abs(lat)) <= 1,
                big_endian_pair=list(struct.unpack('>2d', raw)),
                float32_words=list(struct.unpack('<4f', raw)))


def fixed_points(esm):
    """PNDT pre-BDST CNAM only; repeated fields retained, selected payloads.
    Disk order latitude,longitude,WRLD is justified separately by native loader.
    Source offsets exist only for uncompressed, uniquely located subrecords.
    """
    wanted = {0x3f5a1: 0x1251b, 0x5e2b6: 0x27cfa2, 0x3f59a: 0x2cfc4a}
    out = []
    for rec, fs in esm_records(esm, {b'PNDT'}, repeated=True):
        if rec['formid'] not in wanted:
            continue
        with esm.open('rb') as f:
            f.seek(rec['offset']); h = f.read(24)
            n = struct.unpack_from('<I', h, 4)[0]
            if n > 16*1024*1024:
                raise ValueError('FIXED_PAYLOAD_BOUND')
            payload = f.read(n)
        if rec['flags'] & 0x40000:
            size = struct.unpack_from('<I', payload)[0]
            if size > 16*1024*1024:
                raise ValueError('FIXED_DECODED_BOUND')
            decoder = zlib.decompressobj()
            raw = decoder.decompress(payload[4:], size+1)
            if len(raw) != size or not decoder.eof or decoder.unused_data or decoder.unconsumed_tail:
                raise ValueError('FIXED_DECODED_CLOSURE')
            payload = raw
        assert list(subrecords(payload)) == fs
        for tag, data in fs:
            if tag == b'BDST':
                break
            if tag != b'CNAM':
                continue
            if len(data) % 20:
                raise ValueError('FIXED_CNAM_STRIDE')
            marker = b'CNAM' + struct.pack('<H', len(data)) + data
            relative = payload.find(marker)
            if relative < 0 or payload.find(marker, relative+1) >= 0:
                raise ValueError('FIXED_CNAM_LOCATOR_AMBIGUOUS')
            for p in range(0, len(data), 20):
                lat, lon, world = struct.unpack_from('<ddI', data, p)
                if world != wanted[rec['formid']]:
                    continue
                raw = struct.pack('<2d', lon, lat)
                out.append(dict(body_formid=f'{rec["formid"]:08X}',
                    world_formid=f'{world:08X}', record_file_offset=rec['offset'],
                    pair_file_offset=(rec['offset']+24+relative+6+p if not rec['flags'] & 0x40000 else None),
                    pair_record_decoded_offset=relative+6+p,
                    disk_latitude_longitude_hex=data[p:p+16].hex(), **audit_pair(raw)))
    if len(out) != 3:
        raise ValueError('FIXED_CASE_MISSING_OR_AMBIGUOUS')
    return out


def write(path, data):
    with path.open('x', encoding='utf-8', newline='\n') as f:
        json.dump(data, f, indent=2, allow_nan=False); f.write('\n')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--run', required=True)
    ap.add_argument('--frozen', type=Path, required=True)
    ap.add_argument('--catalog', type=Path, required=True)
    a = ap.parse_args()
    if not a.run.replace('-', '').isalnum():
        raise ValueError('RUN_NAME')
    out = ROOT / '.local-work/surface-anchor' / a.run
    out.mkdir(exist_ok=False); guard(out)
    catalog = json.loads(a.catalog.read_text()); frozen = json.loads(a.frozen.read_text())
    esm = Path(catalog['source']['path'])
    before = {str(p): identity(p) for p in (a.frozen, a.catalog, esm)}
    if before[str(esm)]['sha256'] != catalog['source']['sha256']:
        raise ValueError('ESM_HASH')
    cases, receipts, pairs = [], [], []
    by_pair, by_id = body_catalog(catalog['records'])
    for s in frozen:
        label = s['label']; manifest = s['source']
        for role in ('source', 'copy'):
            p = Path(manifest[role]['path']); actual = identity(p)
            if actual['sha256'] != manifest[role]['sha256']:
                raise ValueError('SAVE_HASH')
            before[str(p)] = actual
        with decoded_save(manifest['copy']['path'], out/'scratch') as (b, metrics):
            if metrics['decoded_sha256'] != s['metrics']['decoded_sha256']:
                raise ValueError('DECODED_HASH')
            result = extract(b, catalog['records'])
            if label == 'HIST-0245':
                # EXP0012 independently checked player parent, not a name match.
                parent = '41251b'; d = directory(b)
                player = next((r for r in iter_records(b, *d['regions']['region_R3'], d['words'][9])
                               if r['token'] == '400014'), None)
                if player is None or player['offset'] != 1519861 or player['refs'][0] != parent:
                    raise ValueError('SAVE2_PLAYER_PARENT')
                _, ps = associations(b, *result['global_units'][6], parent, by_pair, by_id)
                candidates = [dict(token='400014', parent_token=parent, points=ps,
                                   saved_disabled=None, local_xyz=None)]
            else:
                candidates = result['beacons']
            cases.append(dict(label=label, beacons=len(result['beacons']),
                              point_count=sum(len(r['points']) for r in candidates)))
            for r in candidates:
                for pt in r['points']:
                    q = pt['offset']; raw = bytes(b[q+6:q+22])
                    if list(struct.unpack('<2d', raw)) != pt['pair']:
                        raise ValueError('PAIR_REREAD')
                    row = dict(sample=label, token=r['token'], parent=r['parent_token'],
                               body_formid=f'{pt["body_formid"]:08X}',
                               kind=pt['raw_kind'], parent_decoded_offset=q,
                               pair_decoded_offset=q+6, pair_hex=raw.hex(),
                               saved_disabled=r['saved_disabled'], **audit_pair(raw))
                    pairs.append(row)
                    receipts.append(dict(sample=label, token=r['token'],
                                         local_xyz=r['local_xyz'], **pt))
        guard(out)
    fixed = fixed_points(esm)
    lodge = next(p for p in pairs if p['sample']=='HIST-0245')
    city = next(p for p in fixed if p['world_formid']=='0001251B')
    if (lodge['longitude_rad'], lodge['latitude_rad']) != (city['longitude_rad'], city['latitude_rad']):
        raise ValueError('NEW_ATLANTIS_PAIR_MISMATCH')
    controlled = [p['pair_hex'] for p in pairs if p['sample'] in ('S1', 'S1C', 'L2C')]
    if len(controlled) != 3 or len(set(controlled)) != 1:
        raise ValueError('SAME_SITE_REPEATABILITY')
    write(out/'results.json', dict(cases=cases, pairs=pairs, fixed=fixed, receipts=receipts,
                                  same_site_bit_identical=True, new_atlantis_bit_identical=True))
    # Selected authored numbers only; no raw asset/payload or personal name.
    keys = [k for k in pairs[0] if k not in ('big_endian_pair', 'float32_words')]
    with (out/'matrix.csv').open('x', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=keys, extrasaction='ignore'); w.writeheader(); w.writerows(pairs)
    after = {p: identity(Path(p)) for p in before}
    if after != before:
        raise ValueError('INPUT_CHANGED')
    write(out/'preservation.json', dict(before=before, after=after))
    write(out/'tools.json', dict(scripts=[identity(p) for p in Path(__file__).parent.glob('*.py')]))
    print(dict(cases=cases, saved_pairs=len(pairs), fixed=len(fixed),
               max_roundtrip_error=max(p['roundtrip_error_rad'] for p in pairs+fixed)))


if __name__ == '__main__':
    main()
