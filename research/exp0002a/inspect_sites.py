# SPDX-License-Identifier: GPL-3.0-or-later
"""Bounded offline PE evidence; no execution or analysis-database access.

Reads the explicitly supplied, hash-pinned retail PE and original EXP0002 PE
helpers (CPython standard library only). Writes a create-new LOCAL-ONLY JSON
under .local-work/exp0002a. Up to 32 windows of 32 bytes; records address domains
and E8 rel32 targets where requested sites actually begin with E8. This does
not disassemble, prove function boundaries, or establish runtime semantics.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import struct
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'research/exp0002'))
from prepare import GAME_HASH, pe_layout, file_offset


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--game', type=Path, required=True)
    p.add_argument('--output', required=True)
    p.add_argument('rvas', nargs='+', type=lambda s: int(s, 0))
    a = p.parse_args()
    if not 1 <= len(a.rvas) <= 32:
        p.error('1 to 32 sites required')
    if Path(a.output).name != a.output or not a.output.endswith('.json'):
        p.error('simple JSON basename required')
    data = a.game.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    if digest != GAME_HASH:
        raise ValueError('Wrong executable hash; no evidence exported')
    base, size, sections = pe_layout(data)
    rows = []
    for rva in a.rvas:
        pos = file_offset(sections, rva, 32)
        raw = data[pos:pos+32]
        row = dict(rva=hex(rva), static_va=hex(base+rva),
                   file_offset=hex(pos), size=32, hex=raw.hex(),
                   sha256=hashlib.sha256(raw).hexdigest())
        if raw[0] == 0xe8:
            target = rva + 5 + struct.unpack_from('<i', raw, 1)[0]
            row['e8_rel32_target_rva'] = hex(target)
        rows.append(row)
    result = dict(classification='LOCAL-ONLY', utc=datetime.now(timezone.utc).isoformat(),
                  game_sha256=digest, game_size=len(data), preferred_base=hex(base),
                  image_size=size, sites=rows)
    root = ROOT / '.local-work/exp0002a'
    if root.resolve() != root.absolute():
        raise ValueError('Redirected evidence directory')
    root.mkdir(parents=True, exist_ok=True)
    with (root/a.output).open('x', encoding='utf-8', newline='\n') as f:
        json.dump(result, f, indent=2)
        f.write('\n')
        f.flush()
        os.fsync(f.fileno())
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
