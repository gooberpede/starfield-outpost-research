# SPDX-License-Identifier: GPL-3.0-or-later
"""Strict location-only adapter over custodian-provisioned decoded operands.

Pure functions plus JSON CLI. Reads only the named candidate table; stdout only.
This is not a save parser. The trusted custodian must independently authenticate
the table's lineage; schema success cannot establish engine-effective geometry.
No third-party dependencies, target access or writes.
"""
import json
import math
import re
import struct
import sys

EXE = '7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28'
ESM = '1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7'
PLANET = '2fb1fff5d8fc074718bf05022c099f3c87ef70e00050229b368ae7d680fbe5d5'
# Observed PNDT identities from installed.py under the three pinned inputs.
BODIES = {'Kreet': '0003f59f', 'Vectera': '0003f59e', 'Jemison': '0003f5a1'}


def exact(obj, keys):
    if type(obj) is not dict or set(obj) != set(keys.split()):
        raise ValueError('SCHEMA_FIELDS')


def hexword(value, count):
    if type(value) is not str or re.fullmatch('[0-9a-f]{%d}' % count, value) is None:
        raise ValueError('HEX_ENCODING')
    return value


def integer(value, low, high):
    if type(value) is not int or not low <= value <= high:
        raise ValueError('INTEGER_DOMAIN')
    return value


def f32(value, count):
    raw = bytes.fromhex(hexword(value, count * 8))
    values = struct.unpack('<' + 'f' * count, raw)
    if not all(math.isfinite(x) for x in values):
        raise ValueError('NONFINITE_BINARY32')
    return values


def loads(data):
    def pairs(items):
        out = {}
        for key, value in items:
            if key in out:
                raise ValueError('DUPLICATE_JSON_FIELD')
            out[key] = value
        return out
    return json.loads(data, object_pairs_hook=pairs,
                      parse_constant=lambda _: (_ for _ in ()).throw(ValueError('NONFINITE_JSON')))


def validate(row):
    exact(row, 'schema trial body body_formid workshop beacon_token position_le compensation_le frame chart descriptor effective receipt')
    if row['schema'] != 'sor-blind-location/1' or type(row['body']) is not str or row['body'] not in BODIES:
        raise ValueError('LOCATION_VERSION_OR_BODY')
    hexword(row['trial'], 32)
    hexword(row['body_formid'], 8)
    if row['body_formid'] != BODIES[row['body']]:
        raise ValueError('INSTALLED_BODY_IDENTITY')
    hexword(row['workshop'], 16)
    hexword(row['beacon_token'], 6)
    hexword(row['receipt'], 64)
    f32(row['position_le'], 3)
    f32(row['compensation_le'], 3)
    if type(row['frame']) is not int or row['frame'] not in (0x0b, 0x2b):
        raise ValueError('UNKNOWN_SAVED_FRAME')
    integer(row['chart'], 0, 1)
    if type(row['descriptor']) is not list or len(row['descriptor']) != 2:
        raise ValueError('DESCRIPTOR_ARITY')
    for v in row['descriptor']:
        integer(v, 0, 49151)
        if v % 96:
            raise ValueError('DESCRIPTOR_ALIGNMENT')
    # No approved generic saved-to-effective conversion exists yet. Refuse a
    # caller's assertion that this adapter has qualified it.
    if row['effective'] != 'UNKNOWN':
        raise ValueError('UNQUALIFIED_EFFECTIVE_CENTRE')
    return row


def extract(table, trial, workshop):
    exact(table, 'schema exe esm planet receipt rows')
    if table['schema'] != 'sor-blind-location-table/1' or (table['exe'], table['esm'], table['planet']) != (EXE, ESM, PLANET):
        raise ValueError('UNKNOWN_INSTALLED_INPUTS')
    hexword(table['receipt'], 64)
    if type(table['rows']) is not list:
        raise ValueError('TABLE_ROWS')
    # Reject forbidden fields in every row, including unselected candidates.
    for row in table['rows']:
        exact(row, 'body body_formid workshop beacon_token position_le compensation_le frame chart descriptor')
        validate(dict(row, schema='sor-blind-location/1', trial=trial,
                      effective='UNKNOWN', receipt=table['receipt']))
    selected = [r for r in table['rows'] if r['workshop'] == workshop]
    if len(selected) != 1:
        raise ValueError('WORKSHOP_NOT_UNIQUE')
    return validate(dict(selected[0], schema='sor-blind-location/1', trial=trial,
                         effective='UNKNOWN', receipt=table['receipt']))


if __name__ == '__main__':
    with open(sys.argv[1], encoding='utf8') as stream:
        result = extract(loads(stream.read()), sys.argv[2], sys.argv[3])
    print(json.dumps(result, sort_keys=True, separators=(',', ':'), allow_nan=False))
