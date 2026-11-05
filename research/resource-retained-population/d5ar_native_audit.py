# SPDX-License-Identifier: GPL-3.0-or-later
"""Independently compare retained native export instructions to the pinned PE.

Reads explicit ignored export directories and the installed EXE. Writes one
fresh ignored numeric/hash receipt. No game/native execution, database opening,
save/configuration or original-evidence writes; no outside implementation.
"""
import os
import sys
if sys.flags.optimize or not __debug__ or os.environ.get('PYTHONOPTIMIZE', '0') not in ('', '0'):
    raise RuntimeError('Optimization forbidden; invoke pinned Python -E -B')
import hashlib
import json
from pathlib import Path
import re
import struct
from d5ar_native_inventory import ROOT, EXE, PIN, disk_floor


def main():
    output = Path(sys.argv[1]).resolve()
    if not output.is_relative_to(ROOT / '.local-work') or output.exists():
        raise ValueError('Fresh ignored output required')
    before = disk_floor()
    image = EXE.read_bytes()
    if hashlib.sha256(image).hexdigest() != PIN:
        raise ValueError('Installed PE changed')
    pe = struct.unpack_from('<I', image, 0x3c)[0]
    optional = struct.unpack_from('<H', image, pe + 20)[0]
    sections = [struct.unpack_from('<IIII', image, pe + 24 + optional + n * 40 + 8)
                for n in range(struct.unpack_from('<H', image, pe + 6)[0])]
    rows = []
    for argument in sys.argv[2:]:
        source = Path(argument).resolve()
        if not source.is_relative_to(ROOT / '.local-work'):
            raise ValueError('Ignored export directory required')
        receipt = json.loads((source / 'result.json').read_bytes())
        if not (receipt.get('copy_core_preserved') or receipt.get('copy_preserved')):
            raise ValueError('Copied-core preservation missing')
        raw = (source / 'native.tsv').read_bytes()
        digest = hashlib.sha256(raw).hexdigest()
        if digest != receipt['native_sha256']:
            raise ValueError('Native export hash differs')
        text = raw.decode('utf8')
        if not text.startswith('SHA256\t' + PIN + '\n') or not text.endswith('END\n'):
            raise ValueError('Native export identity/completeness')
        verified, byte_count = set(), 0
        for address, encoded in re.findall(r'^BYTES\t([0-9a-f]+)\t([0-9a-f]+)$', text, re.M):
            data = bytes.fromhex(encoded)
            rva = int(address, 16) - 0x140000000
            actual = None
            for _, start, length, offset in sections:
                if start <= rva and rva + len(data) <= start + length:
                    actual = image[offset + rva - start:offset + rva - start + len(data)]
                    break
            if actual != data:
                raise ValueError('Original instruction mismatch at ' + address)
            verified.add(address)
            byte_count += len(data)
        instructions = re.findall(r'^([0-9a-f]{9})\t[^\n]+$', text, re.M)
        if not verified or any(address not in verified for address in instructions):
            raise ValueError('Instruction coverage incomplete')
        rows.append(dict(export=str(source), sha256=digest, instruction_addresses=len(verified),
                         instruction_bytes=byte_count, preserved_copy=True))
    result = dict(schema='sor-d5ar-native-byte-audit/1', status='PASS', rows=rows,
                  exe_sha256=PIN, source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  free_before=before, free_after=disk_floor(), scope='Byte authentication, not semantic acceptance')
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('x', encoding='utf8', newline='\n') as stream:
        json.dump(result, stream, indent=2)
        stream.write('\n')
    print(output, len(rows))


if __name__ == '__main__':
    main()
