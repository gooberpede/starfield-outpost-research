# SPDX-License-Identifier: GPL-3.0-or-later
"""Read pinned installed SFSE export/import/disassembly for preload-order audit.

Runs installed Microsoft dumpbin on the fixed 116,216-byte DLL as data only;
never loads or executes SFSE or Starfield. Writes fresh ignored textual exports
and a hash-bound receipt. No database, save, configuration, install, network or
Git mutation. Uses the owned D5AR disk guard under SOR-P-0002. Original native
facts remain local; no SFSE implementation is incorporated into project code.
Stop on input/source drift, tool failure or either caller-available drive floor.
Preserve all logs; no cleanup deletes or replaces existing artifacts.
"""
import os
import sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):
    raise RuntimeError('Use pinned Python -E -B without optimization')

import hashlib
import json
from pathlib import Path
import subprocess

import d5ar_native_inventory as inherited

DLL = Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield/sfse_1_16_244.dll')
PIN = '28c5bda41d9959c885efcb6e889de69e92767c80a1a66842d711d215f722f82b'
TOOL = Path('C:/Program Files/Microsoft Visual Studio/18/Community/VC/Tools/MSVC/14.51.36231/bin/Hostx64/x64/dumpbin.exe')


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    before = inherited.disk_floor()
    if len(sys.argv) != 2:
        raise ValueError('One fresh ignored output directory required')
    out = Path(sys.argv[1]).absolute()
    if not out.resolve().is_relative_to(inherited.ROOT / '.local-work/d5ar') or out.exists():
        raise ValueError('Fresh ignored D5AR output required')
    if any(p.is_symlink() or p.is_junction() for p in (out, *out.parents)):
        raise ValueError('No reparse output')
    sources = {str(p): sha(p) for p in (Path(__file__).resolve(), Path(inherited.__file__).resolve())}
    if sha(DLL) != PIN or DLL.stat().st_size != 116216:
        raise ValueError('Pinned SFSE image differs')
    tool_hash = sha(TOOL)
    out.mkdir()
    logs = []
    for name, option in (('exports', '/EXPORTS'), ('imports', '/IMPORTS'), ('instructions', '/DISASM:NOBYTES')):
        result = subprocess.run([str(TOOL), option, str(DLL)], capture_output=True)
        for suffix, data in (('txt', result.stdout), ('stderr.txt', result.stderr)):
            path = out / (name + '.' + suffix)
            with path.open('xb') as stream:
                stream.write(data)
            logs.append(dict(path=str(path), bytes=len(data), sha256=sha(path)))
        if result.returncode:
            raise ValueError('Read-only dumpbin failed; preserve logs')
    if sha(DLL) != PIN or sha(TOOL) != tool_hash or any(sha(p) != digest for p, digest in sources.items()):
        raise ValueError('Input or method changed')
    receipt = dict(status='EXPORTED_REQUIRES_SEMANTIC_REVIEW', native_execution=False,
                   source_sha256=sources, image_sha256=PIN, tool=dict(path=str(TOOL), sha256=tool_hash),
                   outputs=logs, floors_before=before, floors_after=inherited.disk_floor())
    with (out / 'receipt.json').open('xb') as stream:
        stream.write(json.dumps(receipt, sort_keys=True, separators=(',', ':')).encode('ascii') + b'\n')
    print(json.dumps(dict(status=receipt['status'], receipt=str(out / 'receipt.json'))))


if __name__ == '__main__':
    main()
