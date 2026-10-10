"""SPDX-License-Identifier: GPL-3.0-or-later
EXP0021 deterministic saved-position research model, schema sor-position/1.
Reads one explicit JSON input on CLI; writes JSON to stdout only. Stdlib and
existing project arithmetic; no saves, native calls, expected-output files or
target effects. Source basis/coverage: docs/experiments/engine-oracle/algorithm.md.
"""
import argparse
import json
import math
import re
import struct
from pathlib import Path

from audit_activated_grid import offset
from beacon_terrain_projection import f32, split_local
from planet_world_key import qualified_grid

EXE_SHA = '7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28'


def vector(text):
    if not isinstance(text, str) or not re.fullmatch('[0-9a-f]{24}', text):
        raise ValueError('FLOAT32_LE_HEX_REQUIRED')
    result = struct.unpack('<3f', bytes.fromhex(text))
    if not all(math.isfinite(x) and (x == 0 or abs(x) >= 2**-126) for x in result):
        raise ValueError('NONFINITE_OR_SUBNORMAL_UNSUPPORTED')
    return result


def center(position, delta):
    """Native helper's vector-wide zero bypass preserves signed-zero input bits."""
    if all(x == 0 for x in delta):
        return tuple(position), 'zero-vector-copy'
    result = tuple(f32(p+d) for p, d in zip(position, delta))
    if not all(math.isfinite(x) and (x == 0 or abs(x) >= 2**-126) for x in result):
        raise ValueError('CENTER_ARITHMETIC_UNSUPPORTED')
    return result, 'float32-add-all-components'


def reconstruct(data):
    required = {'schema', 'exe_sha256', 'source', 'identity', 'frame', 'position_hex',
                'compensation_hex', 'descriptor', 'site_cell'}
    if set(data) != required:
        raise ValueError('INPUT_FIELDS_MISSING_OR_UNEXPECTED')
    if data['schema'] != 'sor-position/1' or data['exe_sha256'] != EXE_SHA:
        raise ValueError('UNSUPPORTED_SCHEMA_OR_EXECUTABLE')
    source = data['source']
    if set(source) != {'sample', 'decoded_sha256', 'record_offset', 'evidence'}:
        raise ValueError('SOURCE_PROVENANCE_REQUIRED')
    if (not isinstance(source['decoded_sha256'], str) or
        not re.fullmatch('[0-9a-f]{64}', source['decoded_sha256']) or
        type(source['record_offset']) is not int or source['record_offset'] < 0 or
        not source['sample'] or not source['evidence']):
        raise ValueError('INVALID_SOURCE_PROVENANCE')
    ident = data['identity']
    if set(ident) != {'body', 'saved_reference', 'parent', 'secondary', 'workshop_id'}:
        raise ValueError('IDENTITY_FIELDS_REQUIRED')
    for k, width in [('body',8), ('saved_reference',6), ('parent',6), ('secondary',6), ('workshop_id',16)]:
        if not isinstance(ident[k],str) or not re.fullmatch('[0-9a-fA-F]{'+str(width)+'}',ident[k]):
            raise ValueError('INVALID_IDENTITY_'+k)
    descriptor = data['descriptor']
    if set(descriptor) != {'key','body','world_token','system_id','body_index'}:
        raise ValueError('DESCRIPTOR_FIELDS_REQUIRED')
    if descriptor['body'] != ident['body'] or descriptor['world_token'] != ident['secondary']:
        raise ValueError('DESCRIPTOR_IDENTITY_MISMATCH')
    if not isinstance(descriptor['key'],str) or not re.fullmatch('[0-9a-f]{16}',descriptor['key']):
        raise ValueError('WORLD_KEY_HEX_REQUIRED')
    origin = qualified_grid(int(descriptor['key'],16))
    if (origin['system_id'],origin['body_index']) != (descriptor['system_id'],descriptor['body_index']):
        raise ValueError('INSTALLED_BODY_IDENTITY_MISMATCH')
    frame = data['frame']
    if type(frame) is not int or frame not in (0x0b,0x2b):
        raise ValueError('UNSUPPORTED_OR_DISABLED_SAVED_FRAME')
    site = data['site_cell']
    if site is not None:
        if (not isinstance(site,list) or len(site)!=3 or any(type(x) is not int for x in site)
            or site[0] not in range(4) or any(not 0<=x<49152 for x in site[1:])):
            raise ValueError('INVALID_SITE_CELL')
    if frame & 0x20 and site is None:
        raise ValueError('MISSING_SITE_CELL')
    p, d = vector(data['position_hex']), vector(data['compensation_hex'])
    c, branch = center(p,d)
    # Restrict integer-conversion and arithmetic domains rather than model
    # SSE indefinite integers or overflow without native qualification.
    if max(abs(c[0]),abs(c[1])) >= 2**24:
        raise ValueError('LOCAL_INTEGER_DOMAIN_UNSUPPORTED')
    base = tuple(site) if frame & 0x20 else tuple(origin[k] for k in ('tag','x','y'))
    qx,rx = split_local(c[0]); qy,ry = split_local(c[1])
    cell = offset(*base,qx,qy)
    return dict(schema='sor-position-result/1', status='STATIC/REPRODUCER',
                identity=ident.copy(), source=source.copy(),
                center_hex=struct.pack('<3f',*c).hex(), center=list(c),
                body=ident['body'], cell=list(cell), residual=[rx,ry,c[2]],
                trace=dict(compensation=branch, selected_base='site' if frame&0x20 else 'source-world',
                           base=list(base), floor=[qx,qy], origin=origin,
                           grid_resolution=49152, local_cell_span=100,
                           orientation='saved axes preserved; seam tag transitions only'),
                limitations=['No future loaded-frame prediction',
                             'No continuous geographical coordinates',
                             'Site cell is an upstream qualified discrete input; angular quantizer not bit-exact here'])


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('input',type=Path)
    args=p.parse_args()
    print(json.dumps(reconstruct(json.loads(args.input.read_text(encoding='utf8'))),indent=2,allow_nan=False))


if __name__ == '__main__':
    main()
