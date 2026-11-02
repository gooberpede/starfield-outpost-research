# SPDX-License-Identifier: GPL-3.0-or-later
"""Read bounded vtable words directly from the pinned installed PE.

Original stdlib PE section walk, independent of Ghidra's virtual-call typing.
Reads Starfield.exe only; writes one fresh ignored JSON. No execution of game
bytes, database, save, network or Git operation. Stops on hash, range or disk
failure. Addresses are preferred static VAs at base 0x140000000.
"""
from pathlib import Path
import hashlib
import json
import struct
import sys

from d5ae_baseline import guard

ROOT = Path(__file__).resolve().parents[2]


def main():
    if not __debug__ or sys.flags.optimize:
        raise RuntimeError('Use Python -E -B')
    guard()
    path = Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield/Starfield.exe')
    data = path.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    if digest != '7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28':
        raise ValueError('PE identity mismatch')
    pe = struct.unpack_from('<I', data, 0x3c)[0]
    if data[pe:pe+4] != b'PE\0\0':
        raise ValueError('PE header')
    count = struct.unpack_from('<H', data, pe+6)[0]
    optional = struct.unpack_from('<H', data, pe+20)[0]
    base = struct.unpack_from('<Q', data, pe+24+24)[0]
    if base != 0x140000000:
        raise ValueError('Unexpected preferred base')
    sections = []
    for i in range(count):
        at = pe+24+optional+i*40
        virtual_size, rva, raw_size, raw = struct.unpack_from('<IIII', data, at+8)
        sections.append((rva, raw_size, raw))
    rows = []
    for value in sys.argv[2:]:
        va = int(value, 16)
        for slot in (0x28, 0x38, 0x40, 0x88, 0x90):
            rva = va+slot-base
            mapped = [(raw+rva-start) for start, size, raw in sections if start <= rva and rva+8 <= start+size]
            if len(mapped) != 1:
                raise ValueError('Ambiguous/unbacked static address')
            target = struct.unpack_from('<Q', data, mapped[0])[0]
            rows.append(dict(table=hex(va), slot=hex(slot), file_offset=hex(mapped[0]), target=hex(target)))
    out = (ROOT/'.local-work/d5ag'/sys.argv[1]).resolve()
    if not out.is_relative_to(ROOT/'.local-work/d5ag') or out.exists():
        raise ValueError('Fresh task-local output required')
    out.write_text(json.dumps(dict(pe_sha256=digest, preferred_base=hex(base), rows=rows,
                                   method_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()),
                              indent=2)+'\n', encoding='utf8', newline='\n')
    print(json.dumps(rows))


if __name__ == '__main__':
    main()
