# SPDX-License-Identifier: GPL-3.0-or-later
"""Finite C1 installed-source/definition check, CPython -B stdlib/owned readers.
Reads existing E2 index, selected physical ESM records, installed development ZIP
and Interface BA2. Writes exclusive ignored JSON and only WorkshopTargetMenu.swf
to ignored C1 work area. No original/game/DB/config/save/Git/network mutation.
Archive payload and all game-derived fields remain local. Not a general extractor.
"""
import argparse
import json
from pathlib import Path
import struct
import sys
import zipfile
import zlib

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'research/s1-storage'))
from catalog import pin, field
from inventory_historical_saves import guard
from inspect_outpost_definitions import subrecords

guard()
ap = argparse.ArgumentParser()
ap.add_argument('--run', required=True)
args = ap.parse_args()
assert args.run.isalnum()
base = ROOT / '.local-work/c1-cargo'
cache = ROOT / '.local-work/e2-organic/inventory02.json'
j = json.loads(cache.read_text())
esm = Path(j['source']['path'])
assert pin(esm) == j['source']
selected = [r for r in j['records'] if
            any(x in r['edid'].lower() for x in ('cargolink', 'linkoutpostcargo',
                                                'isotopiccoolant', 'supercooledmagnet'))]
assemblies = ROOT / '.local-work/s1-storage/assemblies01.json'
aj = json.loads(assemblies.read_text())
assert aj['source'] == j['source']
for r in aj['actis']:
    if r['formid'] in ('002a6c3f', '00219523', '002508aa'):
        selected.append(dict(r, formid=int(r['formid'], 16), type='ACTI',
                             edid=field(r, 'EDID').rstrip(b'\0').decode()))
for r in aj['children']:
    if r.get('packin') == 'OutpostPI_CargoLink01LandingPad' and r['formid'] in (
            '00219172','00219170','00218230','0021916d','0021916c','0021916b'):
        selected.append(dict(r, formid=int(r['formid'],16), type='REFR', edid=''))
with esm.open('rb') as f:
    for r in selected:
        f.seek(r['offset'])
        h = f.read(24)
        n, flags, fid = struct.unpack_from('<III', h, 4)
        assert fid == r['formid'] and h[:4].decode() == r['type']
        b = f.read(n)
        if flags & 0x40000:
            size = int.from_bytes(b[:4], 'little')
            b = zlib.decompress(b[4:])
            assert len(b) == size
        assert [(k.decode(), v.hex()) for k, v in subrecords(b)] == [tuple(x) for x in r['fields']]
zpath = Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield/Tools/ContentResources.zip')
zip_pin = pin(zpath)
scripts = []
with zipfile.ZipFile(zpath) as z:
    for name in ('OutpostCargoLinkMenuScript', 'OutpostCargoLinkMarkerScript',
                 'OutpostCargoLinkPackinScript', 'SQ_OutpostCargoLinkScript'):
        member = 'Scripts/Source/' + name + '.psc'
        b = z.read(member)
        local = ROOT / '.local-work/recon/scripts' / (name + '.psc')
        assert b == local.read_bytes()
        scripts.append(dict(member=member, local=pin(local)))
archive = Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield/Data/Starfield - Interface.ba2')
archive_pin = pin(archive)
with archive.open('rb') as f:
    magic, version, kind, n, names = struct.unpack('<4sI4sIQ', f.read(24))
    assert (magic, version, kind) == (b'BTDX', 2, b'GNRL')
    f.seek(32)
    entries = [struct.unpack('<I4sIIQIII', f.read(36)) for _ in range(n)]
    f.seek(names)
    filenames = [f.read(int.from_bytes(f.read(2), 'little')).decode() for _ in range(n)]
    matches = [i for i, name in enumerate(filenames) if name.lower().endswith('/workshoptargetmenu.swf')]
    assert len(matches) == 1
    i = matches[0]
    _, _, _, _, off, packed, unpacked, _ = entries[i]
    f.seek(off)
    b = f.read(packed or unpacked)
    if packed:
        b = zlib.decompress(b)
    assert len(b) == unpacked
    swf = base / 'WorkshopTargetMenu.swf'
    if swf.exists():
        assert swf.read_bytes() == b
    else:
        with swf.open('xb') as out:
            out.write(b)
assert pin(esm) == j['source'] and pin(zpath) == zip_pin and pin(archive) == archive_pin
result = dict(esm=pin(esm), cache=pin(cache), assemblies=pin(assemblies), zip=zip_pin, scripts=scripts,
              archive=archive_pin, member=filenames[i], swf=pin(swf),
              definitions=selected, tool=pin(__file__))
with (base / (args.run + '.json')).open('x', encoding='utf8', newline='\n') as f:
    json.dump(result, f, indent=2)
    f.write('\n')
guard()
print('PASS', len(selected), 'physical ESM rereads; four exact ZIP sources; one menu asset')
