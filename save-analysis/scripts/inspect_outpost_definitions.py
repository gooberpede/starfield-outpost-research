"""SPDX-License-Identifier: GPL-3.0-or-later
Original read-only ESM reader for beacon ACTI definitions and placed templates.
SOR-S-0128: installed Bethesda data; no external implementation. Stdlib only.
Reads two explicitly supplied ESM files, verifies pre/post SHA-256, performs two
bounded record walks, writes only exclusive ignored numeric/catalog JSON.
No game, xEdit, save or analysis-project effects. No raw assets are exported.
"""
from pathlib import Path
import argparse
import json
import struct
import zlib
from inventory_historical_saves import ROOT, identity, guard


def subrecords(b):
    p = 0
    while p < len(b):
        if p + 6 > len(b):
            raise ValueError('ESM_SUBHEADER_TRUNCATED')
        tag, n = b[p:p+4], struct.unpack_from('<H', b, p+4)[0]
        p += 6
        if tag == b'XXXX':
            if n != 4 or p + 10 > len(b):
                raise ValueError('ESM_EXTENDED_SIZE_INVALID')
            n = struct.unpack_from('<I', b, p)[0]
            tag = b[p+4:p+8]
            p += 10
        if n > len(b) - p:
            raise ValueError('ESM_SUBRECORD_BOUNDS')
        yield tag, b[p:p+n]
        p += n


def esm_records(path, wanted, *, repeated=False):
    """24-byte headers/groups; group end stack rejects nested overflow.
    Only requested record types are read/decompressed. Payload <=16 MiB.
    Default dict retains the last repeated field (legacy behavior); repeated=True
    returns the ordered field list for component-sensitive research.
    """
    with path.open('rb') as f:
        total = path.stat().st_size
        p, stack = 0, [total]
        while p < total:
            while p == stack[-1] and len(stack) > 1:
                stack.pop()
            if p + 24 > stack[-1]:
                raise ValueError('ESM_HEADER_GROUP_BOUNDS')
            f.seek(p)
            h = f.read(24)
            tag = h[:4]
            n, flags, fid = struct.unpack_from('<III', h, 4)
            end = p + (n if tag == b'GRUP' else 24 + n)
            if end > stack[-1] or end < p + 24:
                raise ValueError('ESM_RECORD_GROUP_BOUNDS')
            if tag == b'GRUP':
                stack.append(end)
                p += 24
                continue
            if tag in wanted:
                if n > 16 * 1024 * 1024:
                    raise ValueError('ESM_PAYLOAD_RESOURCE_BOUND')
                b = f.read(n)
                if flags & 0x40000:
                    if len(b) < 4:
                        raise ValueError('ESM_COMPRESSED_HEADER')
                    size = struct.unpack_from('<I', b)[0]
                    if size > 16 * 1024 * 1024:
                        raise ValueError('ESM_DECODED_RESOURCE_BOUND')
                    decoder = zlib.decompressobj()
                    raw = decoder.decompress(b[4:], size + 1)
                    if len(raw) != size or not decoder.eof or decoder.unused_data or decoder.unconsumed_tail:
                        raise ValueError('ESM_COMPRESSED_CLOSURE')
                    b = raw
                fields = list(subrecords(b))
                yield dict(offset=p, type=tag.decode(), formid=fid, flags=flags), (fields if repeated else dict(fields))
            p = end
        if p != total or any(e != total for e in stack[1:]):
            raise ValueError('ESM_FILE_CLOSURE')


def inspect(path):
    before = identity(path)
    definitions, templates = [], []
    for r, fields in esm_records(path, {b'TES4', b'ACTI'}):
        # MAST repeats: dict would lose older masters; self slot is independently
        # visible in record IDs. Catalog does not certify save-era load order.
        if r['type'] == 'ACTI':
            edid = fields.get(b'EDID', b'').rstrip(b'\0').decode('utf-8', errors='strict')
            if edid.startswith('OutpostBeaconActivator'):
                kw = fields.get(b'KWDA', b'')
                if len(kw) % 4:
                    raise ValueError('ESM_KEYWORD_ARRAY_BOUNDS')
                definitions.append(dict(**r, editor_id=edid, keywords=list(struct.unpack(f'<{len(kw)//4}I', kw))))
    bases = {r['formid'] for r in definitions}
    for r, fields in esm_records(path, {b'REFR'}):
        name = fields.get(b'NAME')
        if name and len(name) == 4:
            base = struct.unpack('<I', name)[0]
            if base in bases:
                templates.append(dict(**r, base_formid=base, explicit_owner=(
                    int.from_bytes(fields[b'XOWN'], 'little') if b'XOWN' in fields else None)))
    if identity(path) != before:
        raise ValueError('ESM_CHANGED_DURING_READ')
    return dict(source=before, definitions=definitions, templates=templates,
                coverage='two complete header/group walks; selected ACTI/REFR subrecords only; no override merger')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--run', required=True)
    ap.add_argument('--data', type=Path, required=True)
    args = ap.parse_args()
    if not args.run.replace('-', '').isalnum():
        raise ValueError('run name')
    out = ROOT / '.local-work/membership-completion' / args.run
    out.mkdir(exist_ok=False)
    guard(out)
    result = {name: inspect(args.data / name) for name in ('Starfield.esm', 'SFBGS050.esm')}
    with (out / 'definitions.json').open('x', encoding='utf-8', newline='\n') as f:
        json.dump(result, f, indent=2)
        f.write('\n')
    print({k: dict(definitions=len(v['definitions']), templates=len(v['templates'])) for k, v in result.items()})


if __name__ == '__main__':
    main()
