"""SPDX-License-Identifier: GPL-3.0-or-later
EXP0020 original selected saved-frame audit. Reads frozen center extraction and
qualified world-component/descriptor CSVs; writes selected numerical joins and
hash receipts to a NEW ignored directory. Stdlib/project modules only, 40GB guard.
No save, target, database, network or Git writes. No continuous angular claim.
Native basis: 1418325a0/141833b20 and 140ad3ed0, pinned retail1.16.244.0;
see EXP0020 trace notes for branch coverage and limitations.
"""
import argparse
import csv
import json
from pathlib import Path

from audit_activated_grid import offset
from audit_beacon_projection import audit
from audit_durable_center import table
from beacon_terrain_projection import split_local
from inventory_historical_saves import guard, identity
from residual_ambiguity import countermodel


def selected_grid(origin, site, frame, center):
    """Compare two saved frames in the same indexed chart.

    Mask20 clear: XYZ uses the generated source world's origin. Mask20 set:
    the applicable overlay's site supplies the base; the loader may translate
    into the active source world. Return the invariant indexed representation,
    not the exact runtime edge/XYZ selected in an unobserved load.
    """
    if frame & 0x10:
        raise ValueError('DISABLED_REFERENCE')
    if frame not in (0x0b, 0x2b):
        raise ValueError('UNQUALIFIED_SAVED_FRAME')
    base = site if frame & 0x20 else origin
    if base is None:
        raise ValueError('MISSING_SELECTED_BASE')
    qx, rx = split_local(center[0])
    qy, ry = split_local(center[1])
    tag, x, y = offset(*base, qx, qy)
    return dict(tag=tag, x=x, y=y, local_floor_x=qx, local_floor_y=qy,
                residual_x=rx, residual_y=ry,
                selected_base='site' if frame & 0x20 else 'source-world')


def main():
    parser = argparse.ArgumentParser()
    for name in ('samples', 'components', 'descriptors', 'output'):
        parser.add_argument('--'+name, type=Path, required=True)
    args = parser.parse_args()
    guard(args.output.parent)
    inputs = [args.samples, args.components, args.descriptors]
    before = [identity(p) for p in inputs]
    samples = json.loads(args.samples.read_text(encoding='utf8'))
    with args.components.open(encoding='utf8', newline='') as f:
        components = list(csv.DictReader(f))
    with args.descriptors.open(encoding='utf8', newline='') as f:
        descriptors = list(csv.DictReader(f))
    rows = []
    selected_labels = {r['sample'] for r in components}
    for sample in samples:
        label = sample['label']
        if label not in selected_labels:
            continue
        for beacon in sample['rows']:
            if beacon['role'] != 'beacon':
                continue
            parent = beacon['prefix']['parent_token']
            matches = [r for r in components if r['sample'] == label and r['world'] == parent]
            if len(matches) != 1:
                raise ValueError('PARENT_COMPONENT_NOT_UNIQUE')
            component = matches[0]
            matches = [r for r in descriptors if r['sample'] == label and
                       r['world_token'] == component['secondary']]
            if len(matches) != 1 or matches[0]['body'] != component['body']:
                raise ValueError('SECONDARY_DESCRIPTOR_NOT_UNIQUE_OR_BODY_MISMATCH')
            descriptor = matches[0]
            origin = tuple(int(descriptor[k]) for k in ('tag', 'x', 'y'))
            points = beacon['association']['points']
            if any(f"{p['body_formid']:08X}" != component['body'] for p in points):
                raise ValueError('SITE_COMPONENT_BODY_MISMATCH')
            sites = {tuple(audit(p['pair'])[k] for k in ('tag', 'i', 'j')) for p in points}
            if len(sites) > 1:
                raise ValueError('SITE_NOT_UNIQUE')
            site = next(iter(sites)) if sites else None
            frame = beacon['initial_frame_flag']
            if frame not in (0x0b, 0x2b, 0x3b):
                raise ValueError('UNQUALIFIED_SAVED_FRAME')
            result = {} if frame & 0x10 else selected_grid(origin, site, frame, beacon['center'])
            rows.append(dict(sample=label, token=beacon['prefix']['self_token'],
                             parent=parent, secondary=component['secondary'],
                             body=component['body'], frame=hex(frame),
                             disabled=bool(frame & 0x10), center_hex=beacon['center_hex'],
                             origin_tag=origin[0], origin_x=origin[1], origin_y=origin[2],
                             site_tag=None if site is None else site[0],
                             site_x=None if site is None else site[1],
                             site_y=None if site is None else site[2], **result))
    if before != [identity(p) for p in inputs]:
        raise ValueError('INPUT_CHANGED')
    # Workshop identifier is the independent cross-save identity, not FormID.
    controls = {}
    for sample in samples:
        if sample['label'] not in ('Save25', 'Save26'):
            continue
        for b in sample['rows']:
            if b['role'] == 'beacon':
                key = b['workshop']['identifier98_hex']
                row = next(r for r in rows if r['sample'] == sample['label'] and
                           r['token'] == b['prefix']['self_token'])
                controls.setdefault(key, []).append(tuple(row.get(k) for k in
                    ('body', 'center_hex', 'tag', 'x', 'y', 'residual_x', 'residual_y')))
    if len(controls) != 2 or any(len(v) != 2 or v[0] != v[1] for v in controls.values()):
        raise ValueError('CONTROLLED_DURABLE_FRAME_INVARIANCE')
    args.output.mkdir(exist_ok=False)
    table(args.output/'saved-center-frame.csv', rows)
    countermodels = []
    for row in rows:
        if row['disabled']:
            continue
        values = [countermodel(*(row[k] for k in ('tag','x','y','residual_x','residual_y')),
                               epsilon=e) for e in (0,.05)]
        countermodels.append(dict(sample=row['sample'], token=row['token'],
            body=row['body'], linear_lon=values[0][0], linear_lat=values[0][1],
            warped_lon=values[1][0], warped_lat=values[1][1],
            difference_lon=values[1][0]-values[0][0],
            difference_lat=values[1][1]-values[0][1],
            status='UNVALIDATED_COUNTERMODELS_NOT_GEOGRAPHIC_ESTIMATES'))
    table(args.output/'residual-countermodels.csv', countermodels)
    receipt = dict(inputs=before, selected_beacons=len(rows),
                   disabled=sum(r['disabled'] for r in rows), controlled_invariant=2,
                   scope='Saved indexed frame plus surviving local residual; continuous chart mapping unvalidated')
    (args.output/'receipt.json').write_text(json.dumps(receipt, indent=2)+'\n', encoding='utf8')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
