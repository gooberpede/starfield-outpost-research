# SPDX-License-Identifier: GPL-3.0-or-later
"""Custodian-only bridge from existing sor-position/1 extracted save operands.

Reuses unchanged durable_position_v2's identity, branch-aware compensation and
frame arithmetic. This is an extracted-input adapter, not a universal raw-save
parser. Reads an explicit JSON array in CLI mode; writes filtered JSON stdout.
No raw save, game/process, configuration, database or network effects. Stdlib and
owned save-analysis modules; their original source/fixture bytes remain intact.
"""
import hashlib
import json
from pathlib import Path
import sys

from bridge import BODIES, validate

ROOT = Path(__file__).resolve().parents[2]


def adapt(inputs, trial, workshop):
    sys.path.insert(0, str(ROOT/'save-analysis/scripts'))
    from durable_position_v2 import reproduce
    selected = [row for row in inputs if row.get('identity', {}).get('workshop_id', '').lower() == workshop]
    if len(selected) != 1:
        raise ValueError('WORKSHOP_NOT_UNIQUE')
    row = selected[0]
    result = reproduce(row)
    body = result['body'].lower()
    names = [name for name, fid in BODIES.items() if fid == body]
    if len(names) != 1:
        raise ValueError('BODY_OUTSIDE_CANDIDATE_SCOPE')
    base = result['selected_base']
    if base is None:
        raise ValueError('MISSING_QUALIFIED_SITE_CELL')
    # The source-world/site base is a conditional descriptor input. Neither
    # native_cell nor saved center becomes an observed effective native query.
    filtered = dict(schema='sor-blind-location/1', trial=trial, body=names[0],
        body_formid=body, workshop=workshop, beacon_token=row['identity']['saved_reference'].lower(),
        position_le=row['position_hex'], compensation_le=row['compensation_hex'],
        frame=row['frame'], chart=base[0], descriptor=base[1:], effective='UNKNOWN',
        receipt=hashlib.sha256(json.dumps(row, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()).hexdigest())
    return dict(location=validate(filtered), saved_reconstruction=result,
                transfer_only='location', effective_workshop_query='UNKNOWN')


if __name__ == '__main__':
    from bridge import loads
    with open(sys.argv[1], encoding='utf8') as stream:
        rows = loads(stream.read())
    # Only the allowlisted location crosses the boundary; the custodian keeps
    # the full reconstruction in its private area if it is needed for review.
    print(json.dumps(adapt(rows, sys.argv[2], sys.argv[3])['location'], sort_keys=True, allow_nan=False))
