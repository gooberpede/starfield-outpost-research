# SPDX-License-Identifier: GPL-3.0-or-later
"""Original bounded E1 arithmetic definition reader.
Reads pinned installed main ESM through the owned strict stdlib record reader;
writes one exclusive ignored JSON inventory. Requires repository cwd, CPython,
installed input and C:/D: disk guards. No game, save, project, index or network
effects. Retains selected definition fields locally, not assets in Git.
"""
from pathlib import Path
import argparse
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'save-analysis/scripts'))
from inspect_outpost_definitions import esm_records
from inventory_historical_saves import guard


def pin(path):
    with path.open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    return dict(path=str(path), size=path.stat().st_size, sha256=digest)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--run', default='01')
    args = parser.parse_args()
    assert args.run.isalnum()
    guard()
    path = Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield/Data/Starfield.esm')
    before = pin(path)
    assert before['sha256'] == '1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7'
    selected = {0x05ef19, 0x20a062, 0x20a04a, 0x06ac84, 0x27ab66,
                0x57c7, 0x05ef53, 0x556e, 0x8407, 0x8408, 0x04ce2e}
    records = []
    counts = {}
    wanted = {b'CONT', b'IRES', b'COBJ', b'GLOB', b'AVIF', b'DFOB', b'LVLI', b'KYWD'}
    for header, fields in esm_records(path, wanted, repeated=True):
        kind = header['type']
        counts[kind] = counts.get(kind, 0) + 1
        edid = next((v.rstrip(b'\0').decode('utf8') for k, v in fields if k == b'EDID'), '')
        keep = (header['formid'] in selected or kind in {'IRES', 'AVIF', 'DFOB'}
                or (kind == 'GLOB' and ('production' in edid.lower()
                    or edid in {'TimeScale', 'GameHour', 'GameDaysPassed', 'GameDay', 'GameMonth', 'GameYear'}))
                or (kind == 'LVLI' and any(b'\x2e\xce\x04\x00' in v for _, v in fields)))
        if keep:
            records.append(dict(**header, edid=edid,
                                fields=[(k.decode(), v.hex()) for k, v in fields]))
    recipe_ids = set()
    for record in records:
        if record['type'] == 'IRES':
            fields = dict(record['fields'])
            if int.from_bytes(bytes.fromhex(fields.get('NAM1', '00000000')), 'little') in {0x5ef18, 0x5ed85, 0x5ef1e}:
                recipe_ids.add(int.from_bytes(bytes.fromhex(fields['NAM2']), 'little'))
    retained = {record['formid'] for record in records}
    for header, fields in esm_records(path, {b'COBJ'}, repeated=True):
        if header['formid'] in recipe_ids - retained:
            edid = next((v.rstrip(b'\0').decode('utf8') for k, v in fields if k == b'EDID'), '')
            records.append(dict(**header, edid=edid,
                                fields=[(k.decode(), v.hex()) for k, v in fields]))
    assert pin(path) == before
    out = ROOT/'.local-work/e1-arithmetic'/('definitions'+args.run+'.json')
    with out.open('x', encoding='utf8', newline='\n') as stream:
        json.dump(dict(source=before, counts=counts, records=records), stream, indent=2)
        stream.write('\n')
    guard()
    print('PASS pinned definition inventory', counts, 'selected', len(records))


if __name__ == '__main__':
    main()
