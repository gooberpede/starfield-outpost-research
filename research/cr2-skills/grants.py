# SPDX-License-Identifier: GPL-3.0-or-later
"""Reproduce CR2's compiled crew-quest grant census; offline/read-only.

Reads pinned Misc.ba2, local quest-record and source-discovery inventories and
owned CR1 PEX reader (itself adapted from C2). Decodes PEX as data, never runs it.
Writes exclusive ignored --output JSON; archive/quest/PEX fields stay local.
Requires installed CPython, repository cwd, existing baseline/definitions and
both-drive guard. No target, original, database, index or network effects.
"""
from pathlib import Path
import argparse
import collections
import contextlib
import hashlib
import io
import json
import struct
import sys
import zlib

ROOT = Path(__file__).resolve().parents[2]
WORK = ROOT / '.local-work/cr2-skills'
sys.path[:0] = [str(ROOT / 'save-analysis/scripts'), str(ROOT / '.local-work/cr1-crew')]
from pex_probe import P
from inventory_historical_saves import guard


def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', required=True)
    args = ap.parse_args()
    output = Path(args.output).resolve()
    assert output.is_relative_to(WORK.resolve())
    guard()
    source = json.loads((WORK / 'grant-source01.json').read_text())
    selected = [n for n in source if '/QF_CREW_' in n]
    quests = json.loads((WORK / 'quests-lists01.json').read_text())['records']
    archive = Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield/Data/Starfield - Misc.ba2')
    expected = next(p['sha256'] for p in json.loads((WORK / 'baseline.json').read_text())['protected'] if Path(p['path']) == archive)
    assert sha(archive) == expected
    members, grants = {}, []
    with archive.open('rb') as stream:
        _, _, kind, count, names = struct.unpack('<4sI4sIQ', stream.read(24))
        assert kind == b'GNRL'
        stream.seek(32)
        index = [struct.unpack('<I4sIIQIII', stream.read(36)) for _ in range(count)]
        stream.seek(names)
        paths = [stream.read(int.from_bytes(stream.read(2), 'little')).decode() for _ in range(count)]
        for name in selected:
            target = name.replace('/Source', '')[:-4] + '.pex'
            position = next(i for i, p in enumerate(paths) if p.lower().replace('\\', '/') == target.lower())
            offset, packed, unpacked = index[position][4:7]
            stream.seek(offset)
            data = stream.read(packed or unpacked)
            if packed:
                data = zlib.decompress(data)
            assert len(data) == unpacked
            with contextlib.redirect_stdout(io.StringIO()):
                decoded = P(data).parse()
            fid = int(Path(name).stem.rsplit('_', 1)[-1], 16)
            quest = next(q for q in quests if q['formid'] == fid)
            vmad = bytes.fromhex(dict(quest['fields'])['VMAD'])
            members[target] = dict(sha256=hashlib.sha256(data).hexdigest(), bytes=len(data),
                                   archive_offset=offset, decoded=decoded, quest=f'{fid:08x}', quest_offset=quest['offset'])
            for obj in decoded['objects']:
                for state, functions in obj['states']:
                    for name, body in functions:
                        for op in body['ops']:
                            if op['op'] != 23 or op['args'][0][1].lower() != 'addperk':
                                continue
                            variable = op['args'][-1][0][1]
                            prop = next(p[0] for p in obj['properties'] if p[3] == variable)
                            needle = struct.pack('<H', len(prop)) + prop.encode() + b'\x01\x01'
                            start = vmad.lower().find(needle.lower())
                            assert start >= 0, (quest['edid'], prop)
                            value = vmad[start + len(needle):start + len(needle) + 8]
                            perk = int.from_bytes(value[4:], 'little')
                            grants.append(dict(member=target, function=name, op_offset=op['offset'], property=prop,
                                               perk=f'{perk:08x}', quest=f'{fid:08x}', vmad_property_offset=start,
                                               receiver=op['args'][1], args=op['args'][-1]))
    assert sha(archive) == expected
    output.open('x', encoding='utf8').write(json.dumps(dict(members=members, grants=grants), indent=2) + '\n')
    guard()
    print('PASS', len(members), 'closed PEX members;', len(grants), 'compiled AddPerk calls')


if __name__ == '__main__':
    main()
