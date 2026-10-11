"""SPDX-License-Identifier: GPL-3.0-or-later
Versioned saved-position research reproducer; preserves EXP0021 source/fixtures.
Reads explicit sor-position/1 JSON; stdout only. Stdlib/project modules, no target,
save, database, network or expected-output reads. Native provenance and scope:
docs/experiments/position-resumption/algorithm.md. Qualified site cells remain
upstream inputs; missing cells produce UNKNOWN rather than angular guesses.
"""
import argparse
import copy
import json
from pathlib import Path
import struct

from audit_activated_grid import hierarchy, offset
from beacon_terrain_projection import f32
from durable_position_model import reconstruct

N = 49152


def reflect_packed(tag, x, y):
    """14096fb40 unpack / 14096fa90 pack: involution between domains."""
    return (tag, N-1-x, N-1-y) if tag in (2, 3) else (tag, x, y)


def reproduce(data):
    # Delegate frozen schema/identity/binary32 checks, never output expectations.
    # A missing upstream site is accepted only as a partial representation.
    if type(data.get('frame')) is not int or data['frame'] not in (0x0b, 0x2b):
        raise ValueError('UNSUPPORTED_OR_DISABLED_SAVED_FRAME')
    partial = data['frame'] == 0x2b and data.get('site_cell') is None
    validated = copy.deepcopy(data)
    if partial:
        validated['frame'] = 0x0b
    old = reconstruct(validated)
    c = old['center']
    # Native MXCSR FTZ/DAZ was not captured. Normal inputs can have subnormal
    # products; fail explicitly rather than assume a processor mode.
    if any(0 < abs(v) < 2**-126 / f32(.01) for v in c[:2]):
        raise ValueError('SCALE_SUBNORMAL_ENVIRONMENT_UNQUALIFIED')
    origin = old['trace']['origin']
    packed = tuple(origin[k] for k in ('tag', 'x', 'y'))
    native_origin = reflect_packed(*packed)
    site = data['site_cell']
    if data['frame'] == 0x2b and site is not None and site[0] not in (0, 1):
        raise ValueError('SITE_CELL_DOMAIN_UNQUALIFIED')
    base = tuple(site) if data['frame'] == 0x2b and site is not None else native_origin
    cell = None if partial else offset(*base, *old['trace']['floor'])
    native_cell = None if cell is None else dict(tag=cell[0], xy=list(cell[1:]),
        hierarchy_xy=[list(hierarchy(i)) for i in cell[1:]],
        domain='native-index-hierarchy')
    return dict(schema='sor-position-result/2', status='OFFLINE-SCOPED-RECONSTRUCTION',
        preconditions=['Caller-qualified ordinary activator / Workshop keyword / extra-bc branch',
                       'Round-to-nearest binary32 arithmetic; supported normal/zero domain'],
        identity=old['identity'], source=old['source'], body=old['body'],
        saved_frame=data['frame'], center_hex=old['center_hex'], center=c,
        residual=old['residual'], residual_hex=struct.pack('<3f', *old['residual']).hex(),
        native_cell=native_cell,
        packed_cell=None if cell is None else list(reflect_packed(*cell)),
        selected_base=None if partial else list(base),
        source_origin=dict(packed=list(packed), native=list(native_origin)),
        trace=dict(compensation=old['trace']['compensation'],
            selected_base='site' if data['frame'] == 0x2b else 'source-world',
            floor=old['trace']['floor'], grid_resolution=N, local_cell_span=100),
        stages=dict(body='INDEPENDENTLY-CORROBORATED', center='STATICALLY-RECOVERED',
            frame_branch='STATICALLY-RECOVERED',
            saved_site_base='UNKNOWN' if partial else
                ('MODEL-PREDICTED' if data['frame'] == 0x2b else 'STATICALLY-RECOVERED'),
            cell_arithmetic='UNKNOWN' if partial else 'STATICALLY-RECOVERED',
            cell='UNKNOWN' if partial else
                ('MODEL-PREDICTED' if data['frame'] == 0x2b else 'STATICALLY-RECOVERED'),
            angular_quantizer='UNKNOWN', future_loaded_frame='UNKNOWN',
            fresh_native_end_to_end='UNKNOWN'),
        unknowns=(['qualified_site_cell'] if partial else []) +
            ['arbitrary_angle_native_quantization', 'future_loaded_edge_and_epoch',
             'fresh_same_invocation_native_center_and_grid'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    args = parser.parse_args()
    print(json.dumps(reproduce(json.loads(args.input.read_text(encoding='utf8'))),
                     indent=2, allow_nan=False))


if __name__ == '__main__':
    main()
