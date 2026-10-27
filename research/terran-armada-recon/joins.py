# SPDX-License-Identifier: GPL-3.0-or-later
"""D5J targeted identity, ancestry and installed override sanity checks.

Reads installed plugin headers plus bounded selected records, metadata and loose
script paths. Writes one exclusive ignored JSON. No game or configuration writes.
Not a runtime loader implementation; plugin availability differs from activation.
Uses the owned ESM reader and the sibling task helper, with stdlib only.
"""
import json
import argparse
import struct
from scan import DATA, OUT, ROOT, esm_records, pin


def main(out=OUT):
    out = __import__('pathlib').Path(out).resolve()
    assert out.is_relative_to(ROOT / '.local-work') and out.is_dir()
    wanted = {b'ACTI', b'REFR', b'QUST', b'PCBN', b'PCCN', b'PCMT', b'LCTN', b'LCRT', b'PNDT', b'AVIF', b'CONT', b'COBJ'}
    target = {0x0202cdd7, 0x0202cdd9, 0x0202cdda, 0x0202cdd8, 0x0202cddb, 0x0202cddc,
              0x0001b060, 0x0001b6ca, 0x0001b51a, 0x003e8651, 0x0002271f, 0x002c60e9,
              0x0037c675, 0x0207e613, 0x0207e614, 0x0207e615, 0x0031986f, 0x00271128}
    rows = []
    for name in ('Starfield.esm', 'SFBGS050.esm'):
        for rec, fields in esm_records(DATA / name, wanted, repeated=True):
            ed = next((v.rstrip(b'\0').decode() for k, v in fields if k == b'EDID'), '')
            if rec['formid'] in target or rec['type'] == 'PNDT' and any(t in ed.lower() for t in ('nemeriaiv-a', 'strixi', 'ternioniii')):
                rows.append(dict(file=name, **rec, edid=ed, fields=[(k.decode(), v.hex()) for k, v in fields]))
    # Complete header walks: retain only overrides of this DLC's own namespace.
    overrides, headers, ancestry = [], [], {}
    for path in sorted(DATA.glob('*')):
        if path.suffix.lower() not in ('.esm', '.esp'):
            continue
        master_fields = next(esm_records(path, {b'TES4'}, repeated=True))[1]
        masters = [v.rstrip(b'\0').decode().lower() for k, v in master_fields if k == b'MAST']
        headers.append(dict(file=path.name, sha256=pin(path), masters=masters))
        dlc_index = masters.index('sfbgs050.esm') if 'sfbgs050.esm' in masters else None
        stack = [(path.stat().st_size, None, None)]
        with path.open('rb') as f:
            p = 0
            while p < stack[0][0]:
                while p == stack[-1][0] and len(stack) > 1:
                    stack.pop()
                assert p + 24 <= stack[-1][0]
                f.seek(p)
                h = f.read(24)
                tag = h[:4]
                n, flags, fid = struct.unpack_from('<III', h, 4)
                end = p + (n if tag == b'GRUP' else 24 + n)
                assert p + 24 <= end <= stack[-1][0]
                if tag == b'GRUP':
                    stack.append((end, f'0x{flags:08x}', fid))
                    p += 24
                else:
                    if dlc_index is not None and fid >> 24 == dlc_index:
                        overrides.append(dict(file=path.name, type=tag.decode(), raw_formid=f'0x{fid:08x}', local_id=f'0x{fid & 0xffffff:06x}', offset=p))
                    if path.name.lower() == 'sfbgs050.esm' and fid in (0x0202b254, 0x0202b255, 0x0202b256):
                        ancestry[f'0x{fid:08x}'] = stack[1:]
                    p = end
            assert p == stack[0][0]
    loose = []
    for path in (DATA / 'Scripts').rglob('*.pex') if (DATA / 'Scripts').exists() else []:
        if any(t in path.name.lower() for t in ('mqoutpost', 'outpostbeacon')):
            loose.append(dict(path=str(path), sha256=pin(path)))
    config = {}
    for path in (ROOT / '.git/index', DATA.parent / 'Starfield.exe',
                 DATA / 'Starfield - PlanetData.ba2',
                 __import__('pathlib').Path('C:/Users/User/AppData/Local/Starfield/Plugins.txt'),
                 __import__('pathlib').Path('C:/Users/User/AppData/Local/Starfield/loadorder.txt'),
                 __import__('pathlib').Path('C:/Users/User/AppData/Local/Starfield/ContentCatalog.txt')):
        config[str(path)] = dict(bytes=path.stat().st_size, sha256=pin(path))
    with (out / 'joins.json').open('x', encoding='utf8', newline='\n') as f:
        json.dump(dict(records=rows, headers=headers, dlc_overrides=overrides,
                       ancestry=ancestry, loose_scripts=loose, config=config), f, indent=2)
        f.write('\n')
    print('Selected joins', len(rows), 'plugin headers', len(headers), 'DLC overrides', len(overrides), 'loose scripts', len(loose))


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out', type=__import__('pathlib').Path, default=OUT)
    main(ap.parse_args().out)
