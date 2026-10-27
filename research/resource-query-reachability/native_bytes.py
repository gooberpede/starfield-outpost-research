# SPDX-License-Identifier: GPL-3.0-or-later
"""Read the pinned installed PE; write an exclusive local native-byte receipt.

Uses only Python stdlib. No target, database, installed-input or Git writes.
The caller supplies a fresh ignored output path. VAs use the preferred PE base.
Vtable labels come from the D5H read-only Ghidra symbol export, not RTTI guesses.
"""
import hashlib
import json
from pathlib import Path
import struct
import sys

EXE = Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield/Starfield.exe')
EXPECTED = '7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28'
TABLES = {'GridEdgeXCell': 0x144b67e28, 'GridCornerCell': 0x144b67e70,
          'GridFillCell': 0x144b67eb8, 'GridEdgeYCell': 0x144b67f00,
          'Grid': 0x144b67f48, 'MultiFilesGrid': 0x144b3e0b8}


def main():
    output = Path(sys.argv[1]).resolve()
    root = Path(__file__).resolve().parents[2]
    assert output.is_relative_to(root / '.local-work') and not output.exists()
    with EXE.open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
        assert digest == EXPECTED
        stream.seek(0x3c)
        pe = struct.unpack('<I', stream.read(4))[0]
        stream.seek(pe)
        header = stream.read(24)
        assert header[:4] == b'PE\0\0'
        count = struct.unpack_from('<H', header, 6)[0]
        optional_size = struct.unpack_from('<H', header, 20)[0]
        optional = stream.read(optional_size)
        assert struct.unpack_from('<H', optional)[0] == 0x20b
        base = struct.unpack_from('<Q', optional, 24)[0]
        assert base == 0x140000000
        sections = [stream.read(40) for _ in range(count)]

        def read(va, size):
            rva = va - base
            matches = []
            for section in sections:
                _, start, raw_size, raw = struct.unpack_from('<IIII', section, 8)
                if start <= rva and rva + size <= start + raw_size:
                    matches.append(raw + rva - start)
            assert len(matches) == 1
            stream.seek(matches[0])
            data = stream.read(size)
            assert len(data) == size
            return data, matches[0]

        tables = {}
        for name, va in TABLES.items():
            size = 0x90 if name == 'MultiFilesGrid' else 0x48 if name == 'Grid' else 0x40
            data, offset = read(va, size)
            tables[name] = dict(va=hex(va), file_offset=offset,
                sha256=hashlib.sha256(data).hexdigest(),
                slots={hex(i): hex(struct.unpack_from('<Q', data, i)[0])
                       for i in range(0, len(data), 8)})
        constants = {}
        for va in (0x144f046a8, 0x144f04718, 0x144f052c0, 0x144f04668,
                   0x144f04770, 0x144f047a0, 0x144f04210):
            data, offset = read(va, 8)
            constants[hex(va)] = dict(file_offset=offset, hex_bytes=data.hex(), value=struct.unpack('<d', data)[0])
        receipt = dict(exe=str(EXE), exe_sha256=digest, preferred_base=hex(base), tables=tables,
                       constants=constants)
        receipt['math_wrapper_window'] = read(0x14374dcd2, 64)[0].hex()
        receipt['sine_constants'] = {hex(va): list(struct.unpack('<4d', read(va, 32)[0]))
            for va in range(0x14882ecc0, 0x14882f180, 0x40)}
        receipt['wrapper_shift'] = list(struct.unpack('<4d', read(0x144f07280, 32)[0]))
        def string(va):
            data = read(va, 256)[0]
            return data.split(b'\0')[0].decode('ascii')
        imports_rva = struct.unpack_from('<I', optional, 120)[0]
        imports = {}
        for descriptor in range(256):
            fields = struct.unpack('<5I', read(base + imports_rva + descriptor * 20, 20)[0])
            original, _, _, name, first = fields
            if not any(fields):
                break
            for index in range(4096):
                lookup = struct.unpack('<Q', read(base + (original or first) + index * 8, 8)[0])[0]
                if not lookup:
                    break
                address = base + first + index * 8
                if address in (0x143a40570, 0x143a40648):
                    imports[hex(address)] = dict(dll=string(base + name), function=string(base + lookup + 2))
        assert len(imports) == 2
        receipt['scalar_math_imports'] = imports
    with output.open('x', encoding='utf8', newline='\n') as stream:
        json.dump(receipt, stream, indent=2)
        stream.write('\n')
    print(json.dumps(tables, indent=2))


if __name__ == '__main__':
    main()
