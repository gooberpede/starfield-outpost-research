# SPDX-License-Identifier: GPL-3.0-or-later
"""Bounded offline D5J inspection using owned ESM/PEX readers at starting HEAD.

Reads installed SFBGS050 definitions and selected BA2 script/string members.
Writes selected raw records and decoded scripts ONLY beneath ignored local work.
No VM/game execution, installation, save, configuration or database writes.
Stdlib only; existing reader provenance and limits are documented in methods.md.
"""
import hashlib
import argparse
import json
from pathlib import Path
import shutil
import struct
import sys
import zlib

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / '.local-work/terran-armada-recon'
DATA = Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield/Data')
sys.path.insert(0, str(ROOT / 'save-analysis/scripts'))
from inspect_outpost_definitions import esm_records
sys.path.insert(0, str(ROOT / 'research/c2-transport'))
from pex import P


def pin(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def members(path, predicate):
    with path.open('rb') as f:
        magic, version, kind, count, names_at = struct.unpack('<4sI4sIQ', f.read(24))
        assert (magic, version, kind) == (b'BTDX', 2, b'GNRL') and count < 100000
        f.seek(32)
        entries = [struct.unpack('<I4sIIQIII', f.read(36)) for _ in range(count)]
        f.seek(names_at)
        names = [f.read(int.from_bytes(f.read(2), 'little')).decode() for _ in entries]
        assert len(set(names)) == len(names)
        for name, entry in zip(names, entries):
            if not predicate(name):
                continue
            at, packed, size = entry[4:7]
            assert size <= 5000000 and at + (packed or size) <= path.stat().st_size
            f.seek(at)
            data = f.read(packed or size)
            if packed:
                decoder = zlib.decompressobj()
                data = decoder.decompress(data, size + 1)
                assert decoder.eof and not decoder.unused_data and not decoder.unconsumed_tail
            assert len(data) == size
            yield name, data


def main(out=OUT):
    out = Path(out).resolve()
    assert out.is_relative_to(ROOT / '.local-work')
    out.mkdir(parents=True, exist_ok=True)
    assert not (out / 'installed.json').exists()
    assert min(shutil.disk_usage(d).free for d in ('C:/', 'D:/')) >= 40000000000
    esm, ba2 = DATA / 'SFBGS050.esm', DATA / 'SFBGS050 - Main.ba2'
    before = {str(p): pin(p) for p in (esm, ba2)}
    catalog, records = [], {}
    wanted = {x.encode() for x in ('TES4', 'QUST', 'ACTI', 'LCTN', 'WRLD', 'CELL',
                                  'REFR', 'COBJ', 'FLST', 'KYWD', 'GBFM', 'OMOD', 'FURN')}
    for rec, fields in esm_records(esm, wanted, repeated=True):
        edid = next((v.rstrip(b'\0').decode(errors='strict') for k, v in fields if k == b'EDID'), '')
        key = f"{rec['formid']:08x}"
        catalog.append(dict(**rec, edid=edid))
        records[key] = dict(**rec, edid=edid, fields=[(k.decode(), v.hex()) for k, v in fields])
    selected = {k: v for k, v in records.items() if any(t in v['edid'].lower()
                for t in ('outpost', 'xtech'))}
    quests = {k: v for k, v in selected.items() if v['type'] == 'QUST'}
    # Direct reference edges to the three beacon bases and all quest-bound forms.
    targets = {0x02038ac8, 0x02038ac9, 0x02038aca}
    for q in quests.values():
        for tag, value in q['fields']:
            b = bytes.fromhex(value)
            if tag in ('ALFR', 'ALUA', 'ALRT', 'ALFL', 'ALFA') and len(b) == 4:
                targets.add(int.from_bytes(b, 'little'))
    for key, rec in records.items():
        fs = {k: bytes.fromhex(v) for k, v in rec['fields']}
        if rec['formid'] in targets or (rec['type'] == 'REFR' and int.from_bytes(fs.get('NAME', b''), 'little') in targets):
            selected[key] = rec
    scripts = {}
    for name, b in members(ba2, lambda n: n.endswith('.pex') and ('mqoutpost' in n.lower() or 'xtech' in n.lower()) or n == 'strings/sfbgs050_en.strings'):
        item = dict(sha256=hashlib.sha256(b).hexdigest(), bytes=len(b))
        if name.endswith('.pex'):
            item['decoded'] = P(b).parse()
            with (out / Path(name).name).open('xb') as f:
                f.write(b)
        else:
            count, size = struct.unpack_from('<II', b)
            assert 8 + count * 8 + size == len(b)
            base = 8 + count * 8
            strings = {}
            for i in range(count):
                sid, off = struct.unpack_from('<II', b, 8 + i * 8)
                end = b.index(0, base + off)
                strings[sid] = b[base + off:end].decode('utf8')
            item['strings'] = strings
        scripts[name] = item
    assert before == {str(p): pin(p) for p in (esm, ba2)}
    result = dict(inputs=before, catalog=catalog, records=selected, scripts=scripts)
    with (out / 'installed.json').open('x', encoding='utf8', newline='\n') as f:
        json.dump(result, f, indent=2)
        f.write('\n')
    print('Closed records:', len(catalog), 'selected:', len(selected), 'members:', len(scripts))


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out', type=Path, default=OUT)
    main(ap.parse_args().out)
