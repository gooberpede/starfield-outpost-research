# SPDX-License-Identifier: GPL-3.0-or-later
"""Bounded CR2 offline census; run from repository cwd with installed CPython.

Reads installed ESM with owned inspect_outpost_definitions.esm_records (conceptual
reuse of research/e1-extractors/production-definitions.py); stdlib only. Hashes
before/after, checks both-drive guard, writes exclusive ignored JSON. Includes
all NPC/PERK/SPEL/MGEF/KYWD/AVIF records so template and non-crew perk leads are
not silently excluded. No game, save, database, Git or network mutations.
Game-derived field payloads remain LOCAL-ONLY; this is not an importer.
"""
from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'save-analysis/scripts'))
from inspect_outpost_definitions import esm_records
from inventory_historical_saves import guard


def pin(path):
    with path.open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    return dict(path=str(path), bytes=path.stat().st_size, sha256=digest)


if __name__ == '__main__':
    guard()
    path = Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield/Data/Starfield.esm')
    before = pin(path)
    assert before['sha256'] == '1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7'
    rows = []
    for header, fields in esm_records(path, {b'NPC_', b'PERK', b'SPEL', b'MGEF', b'KYWD', b'AVIF'}, repeated=True):
        rows.append(dict(**header, edid=next((v.rstrip(b'\0').decode('utf8') for k, v in fields if k == b'EDID'), ''),
                         fields=[(k.decode(), v.hex()) for k, v in fields]))
    assert before == pin(path)
    out = ROOT / '.local-work/cr2-skills/definitions01.json'
    with out.open('x', encoding='utf8', newline='\n') as stream:
        json.dump(dict(source=before, records=rows), stream, indent=2)
        stream.write('\n')
    guard()
    print('PASS fresh records', len(rows), 'source unchanged')
