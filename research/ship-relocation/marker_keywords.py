# SPDX-License-Identifier: GPL-3.0-or-later
"""Read-only installed ESM marker/keyword audit, stdout selected identity JSON.

Explicit ESM input only; no process/database/save/network or original writes.
Stdlib/project reader, full header walks for FURN/KYWD, pre/post file hash and
both-drive40GB guard. Raw payload/assets stay local; selected names are evidence
identity, not proof of native settings or radius. Capture stdout as new receipt.
"""
import argparse
import hashlib
import json
from pathlib import Path
import struct
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'save-analysis/scripts'))
from inspect_outpost_definitions import esm_records
from inventory_historical_saves import guard


def main(path):
    guard()
    def digest():
        with path.open('rb') as stream:
            return hashlib.file_digest(stream, 'sha256').hexdigest()
    before = digest()
    if before != '1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7':
        raise ValueError('pinned_esm_hash')
    markers, keywords = [], {}
    for record, fields in esm_records(path, {b'FURN', b'KYWD'}):
        name = fields.get(b'EDID', b'').rstrip(b'\0').decode('utf8')
        if record['type'] == 'KYWD':
            keywords[record['formid']] = dict(editor_id=name, offset=record['offset'])
        elif 'ShipLandingMarker' in name or ('LandingPad' in name and ('40m' in name or '80m' in name)):
            raw = fields.get(b'KWDA', b'')
            if len(raw) % 4:
                raise ValueError('KWDA_length')
            markers.append(dict(**record, editor_id=name,
                                keyword_ids=list(struct.unpack('<'+'I'*(len(raw)//4), raw))))
    for row in markers:
        row['keywords'] = [{**keywords.get(i, {'editor_id': 'UNRESOLVED'}), 'formid': f'{i:08X}'}
                           for i in row['keyword_ids']]
    if digest() != before:
        raise ValueError('esm_changed')
    print(json.dumps(dict(source=str(path), sha256=before, markers=markers,
                         limits='Static installed definitions, not runtime winning overrides or native global keyword mapping'), indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('esm', type=Path)
    main(parser.parse_args().esm)
