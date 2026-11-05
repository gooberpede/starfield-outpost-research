# SPDX-License-Identifier: GPL-3.0-or-later
"""Recover the A0-anchored main-file source BIOM, conditionally.

Reads the authenticated A0 archive and the pinned installed PlanetData BA2.
Uses owned B1 BA2 framing and RG1 map lookup (SOR-P-0002). Writes only a fresh
ignored receipt; never loads or writes a save, game, profile or analysis DB.
"""
import os
import sys

if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):
    raise RuntimeError('Use pinned Python -E -B without optimization')

import hashlib
import json
import struct
import zipfile
import zlib
from pathlib import Path

from d5ad_baseline import ROOT, guard, sha
from d5al_baseline import ANCHORS, ARCHIVE

sys.path.insert(0, str(ROOT / 'research/resource-geometry'))
from context import map_lookup, read_map


def need(condition, reason):
    if not condition:
        raise ValueError(reason)


def main():
    before = guard()
    sources = {str(Path(module.__file__).resolve()): sha(module.__file__)
               for module in tuple(sys.modules.values()) if getattr(module, '__file__', None) and
               Path(module.__file__).suffix == '.py' and Path(module.__file__).resolve().is_relative_to(ROOT)}
    out = Path(sys.argv[1]).absolute()
    need(out.resolve().is_relative_to(ROOT / '.local-work/d5ar') and out.parent.is_dir() and not out.exists(),
         'Fresh ignored output required')
    need(not any(p.is_symlink() or p.is_junction() for p in (out, *out.parents)), 'No reparse output')
    a0 = ARCHIVE / 'episode-a.zip'
    keys = ROOT / '.local-work/d5ar/key-inputs01.json'
    need(sha(a0) == ANCHORS[a0], 'A0 archive changed')
    need(sha(keys) == '1ca87c0e8a4ffe1c6aa37561ddc97d83ba8e62c2e5c40bf6d3bde60f99d43ca6', 'Key receipt changed')
    with zipfile.ZipFile(a0) as zipped:
        pre = json.loads(zipped.read('notes/preflight01/receipt.json'))['protection']
        post = json.loads(zipped.read('notes/postflight01/receipt.json'))
    need(post['status'] == 'PASS_POSTFLIGHT' and not post['protection_errors'], 'A0 postflight not qualified')
    post_installed = any(row['equal'] and 'installed' in row['fields'] for row in post['protection_comparisons'])
    archives = [(Path(name), pin) for name, pin in pre['installed'].items()
                if Path(name).name.lower() == 'starfield - planetdata.ba2']
    need(len(archives) == 1, 'A0 archive roster changed')
    archive, installed = archives[0]
    pin = installed['sha256']
    size = archive.stat().st_size
    need(size == installed['bytes'] and sha(archive) == pin, 'Installed archive content changed')
    member = 'planetdata/biomemaps/feynman v.biom'
    with archive.open('rb') as stream:
        magic, version, kind, count, names = struct.unpack('<4sI4sIQ', stream.read(24))
        need((magic, version, kind) == (b'BTDX', 2, b'GNRL') and 32 + 36 * count <= names < size,
             'Unsupported archive framing')
        stream.seek(names)
        indices = []
        for index in range(count):
            length, = struct.unpack('<H', stream.read(2))
            raw_name = stream.read(length)
            need(len(raw_name) == length, 'Short archive name')
            if raw_name.decode('utf8').lower().replace('\\', '/') == member:
                indices.append(index)
        need(len(indices) == 1, 'Ambiguous main archive member')
        stream.seek(32 + 36 * indices[0])
        _, _, _, _, offset, packed, unpacked, _ = struct.unpack('<I4sIIQIII', stream.read(36))
        need(unpacked == 655414 and 32 + 36 * count <= offset <= names - (packed or unpacked),
             'Unsupported member extent')
        stream.seek(offset)
        payload = stream.read(packed or unpacked)
    if packed:
        decoder = zlib.decompressobj()
        payload = decoder.decompress(payload, unpacked + 1)
        need(decoder.eof and not decoder.unused_data and not decoder.unconsumed_tail, 'Incomplete member')
    need(len(payload) == unpacked, 'Short member')
    key = json.loads(keys.read_bytes())
    chart, x, y, _ = key['source'].split(':')
    chart, x, y = int(chart), int(x), int(y)
    raster = read_map(payload)
    biome = map_lookup(raster, chart, x, y)
    col, row = x // 192, 255 - y // 192
    need(chart == 0 and key['body'] == '0005e0de' and biome == 0x145440 and
         struct.unpack_from('<I', payload, 34 + 4 * (256 * row + col))[0] == biome,
         'A0-derived anchor, body or independent raster address differs')
    inputs = {str(a0): ANCHORS[a0], str(archive): pin, str(keys): sha(keys)}
    need(all(sha(path) == digest for path, digest in (inputs | sources).items()), 'Input or source changed')
    receipt = dict(status='PASS_CONDITIONAL_MAIN_RASTER_BIOME', source=key['source'], body=key['body'],
                   member=member, member_index=indices[0], member_sha256=hashlib.sha256(payload).hexdigest(),
                   pixel=[chart, col, row], biome=f'{biome:08x}', inputs=inputs, source_sha256=sources,
                   premises=['Manager ready map resolves this pinned main archive member',
                             'Stable ordinary active descriptor at source BIOM selection'],
                   historical_runtime_biome_observed=False, a0_postflight_compared_installed=post_installed,
                   floors_before=before, floors_after=guard())
    with out.open('x', encoding='utf8', newline='\n') as stream:
        json.dump(receipt, stream, indent=2)
        stream.write('\n')
    print(json.dumps({name: receipt[name] for name in ('status', 'pixel', 'biome')}))


if __name__ == '__main__':
    main()
