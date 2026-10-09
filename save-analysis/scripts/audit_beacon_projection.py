"""SPDX-License-Identifier: GPL-3.0-or-later
SOR-EXP-0015: audit selected extraction receipts against the native-derived grid.
Reads JSON receipts and selected fixed-city CSV; writes a NEW local directory.
Stdlib only. Does not read/change saves, executable, game or analysis database.
Prerequisite: research_two_outpost_anchors.py receipts. No names/network inputs.
Results establish grid-centre consistency, NOT exact individual beacon angles.
"""
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
import shutil

from beacon_terrain_projection import to_square, grid_centre, split_local


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit(pair, xyz=None):
    # Defaults independently recovered from native settings/initialization.
    tag, u, v = to_square(*pair)
    n = 16 * 12 * 256
    i, j = round((u+.5)*n-.5), round((v+.5)*n-.5)
    predicted = grid_centre(tag, i, j, native=True)
    row = dict(tag=tag, i=i, j=j,
               square_residual_x=(u+.5)*n-i-.5,
               square_residual_y=(v+.5)*n-j-.5,
               longitude_rad=pair[0], latitude_rad=pair[1],
               longitude_error_rad=math.remainder(predicted[0]-pair[0], 2*math.pi),
               latitude_error_rad=predicted[1]-pair[1])
    if xyz is not None:
        qx, rx = split_local(xyz[0])
        qy, ry = split_local(xyz[1])
        row.update(local_x=xyz[0], local_y=xyz[1], local_z=xyz[2],
                   local_grid_x=qx, local_grid_y=qy, residual_x=rx, residual_y=ry,
                   candidate_origin_i=i-qx, candidate_origin_j=j-qy)
    return row


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--receipts', type=Path, required=True)
    parser.add_argument('--fixed', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    inputs = [args.receipts.resolve(), args.fixed.resolve()]
    before = {str(p): digest(p) for p in inputs}
    output = args.output.resolve()
    ancestor = output.parent
    while not ancestor.exists():
        ancestor = ancestor.parent
    if shutil.disk_usage(ancestor).free < 40_000_000_000:
        raise RuntimeError('40GB_FREE_SPACE_GUARD')
    if output.exists():
        raise FileExistsError(output)
    rows = []
    counts = {}
    for sample in json.loads(args.receipts.read_text(encoding='utf-8')):
        counts[sample['label']] = len(sample['extraction']['beacons'])
        for beacon in sample['extraction']['beacons']:
            for point in beacon['points']:
                rows.append(dict(sample=sample['label'], kind='beacon-site',
                                 token=beacon['token'], parent=beacon['parent_token'],
                                 body=f"{point['body_formid']:08X}",
                                 **audit(point['pair'], beacon['local_xyz'])))
    with args.fixed.open(encoding='utf-8', newline='') as stream:
        for city in csv.DictReader(stream):
            pair = [float(city[k]) for k in ('longitude_rad', 'latitude_rad')]
            rows.append(dict(sample='fixed-ESM', kind='fixed-site',
                             token=city['world_formid'], parent='',
                             body=city['body_formid'], **audit(pair)))
    after = {str(p): digest(p) for p in inputs}
    if before != after:
        raise RuntimeError('INPUT_CHANGED')
    output.mkdir(parents=True)
    fields = list(dict.fromkeys(key for row in rows for key in row))
    with (output/'matrix.csv').open('x', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)
    beacon_rows = [r for r in rows if r['kind'] == 'beacon-site']
    summary = dict(inputs_before=before, inputs_after=after, beacon_counts=counts,
                   grid_n=49152, beacon_pair_rows=len(beacon_rows),
                   max_longitude_error_rad=max(abs(r['longitude_error_rad']) for r in beacon_rows),
                   max_latitude_error_rad=max(abs(r['latitude_error_rad']) for r in beacon_rows),
                   conclusion='GRID-CENTRE CONSISTENCY ONLY; EXACT BEACON TRANSFORM OPEN')
    (output/'summary.json').write_text(json.dumps(summary, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
