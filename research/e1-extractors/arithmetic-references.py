# SPDX-License-Identifier: GPL-3.0-or-later
"""Original exact-byte definition locator for the E1 extra-production question.
Reads the pinned main ESM with the owned strict reader; writes an exclusive
ignored receipt. Requires CPython stdlib, repository cwd and disk guards. A
header preflight excludes entire types with >16MiB encoded payloads rather
than weakening the reader's bound. Exact matches are locators, not typed proof.
No game, process, save, analysis project, index or network effects.
This preserves and makes reproducible the earlier inline investigation method.
"""
from pathlib import Path
import argparse
import hashlib
import json
import struct
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'save-analysis/scripts'))
from inspect_outpost_definitions import esm_records
from inventory_historical_saves import guard


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--run', required=True)
    args = parser.parse_args()
    assert args.run.isalnum()
    guard()
    path = Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield/Data/Starfield.esm')
    before = digest(path)
    assert before == '1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7'
    kinds, excluded = set(), set()
    with path.open('rb') as stream:
        total, pos = path.stat().st_size, 0
        while pos < total:
            stream.seek(pos)
            header = stream.read(24)
            assert len(header) == 24
            tag = header[:4]
            size = struct.unpack_from('<I', header, 4)[0]
            if tag == b'GRUP':
                pos += 24
            else:
                kinds.add(tag)
                if size > 16*1024*1024:
                    excluded.add(tag)
                pos += 24+size
        assert pos == total
    patterns = {value: struct.pack('<I', value) for value in (0x4ce2a, 0x4ce2b, 0x4ce2c, 0x4ce2d)}
    hits, count = [], 0
    for header, fields in esm_records(path, kinds-excluded, repeated=True):
        count += 1
        matches = []
        for tag, value in fields:
            for target, needle in patterns.items():
                at = value.find(needle)
                if at >= 0:
                    matches.append(dict(tag=tag.decode(), target=hex(target), at=at,
                                        hex=value.hex() if len(value) < 3000 else None))
        if matches:
            edid = next((v.rstrip(b'\0').decode('utf8') for k, v in fields if k == b'EDID'), '')
            hits.append(dict(**header, edid=edid, matches=matches))
    assert digest(path) == before
    guard()
    result = dict(source=str(path), sha256=before, records=count,
                  excluded=sorted(tag.decode() for tag in excluded), hits=hits,
                  coverage='All header types except resource-bound excluded types; exact four-byte locators, not typed semantic matches.')
    dest = ROOT/'.local-work/e1-arithmetic'/('special-references'+args.run+'.json')
    with dest.open('x', encoding='utf8', newline='\n') as stream:
        json.dump(result, stream, indent=2)
        stream.write('\n')
    print('PASS', count, 'records;', len(hits), 'candidate records; excluded', result['excluded'])


if __name__ == '__main__':
    main()
