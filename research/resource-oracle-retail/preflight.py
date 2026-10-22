# SPDX-License-Identifier: GPL-3.0-or-later
"""Read-only identity/definition/static-guard launch checks; fresh local receipt.

Does not launch game or debugger, install anything, edit configuration or saves.
Build and qualification must already be complete. User Cloud/READY attestations
are recorded separately from machine-verified checks. No network or Git writes.
"""
import argparse
import csv
import datetime
import json
from pathlib import Path
import shutil
import struct
from collect import LOCAL, ROOT, pin, write

GAME = Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield')


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--build', type=Path, required=True)
    ap.add_argument('--qualification', type=Path, required=True)
    ap.add_argument('--name', default='identity-preflight')
    a = ap.parse_args()
    assert a.name and all(c in 'abcdefghijklmnopqrstuvwxyz0123456789-' for c in a.name)
    assert not (LOCAL / (a.name + '.json')).exists()
    build = a.build.resolve()
    assert build.is_relative_to(LOCAL)
    q = json.loads(a.qualification.read_text())
    assert q['unit'] and len(q['cases']) == 13 and all(r['passed'] for r in q['cases'])
    old = json.loads((ROOT / '.local-work/resource-oracle-collector/qualification-c1d01/qualification.json').read_text())
    # Keep the full unchanged 19-case receipt as primary evidence, not just a count.
    inputs = json.loads((LOCAL / 'protected-preflight.json').read_text())['pins']
    for row in inputs:
        assert pin(row['path']) == row['sha256'], row['path']
    assert pin(GAME / 'Starfield.exe') == '7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28'
    assert pin(GAME / 'Data/Starfield.esm') == '1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7'
    definitions = {str(p): dict(bytes=p.stat().st_size, sha256=pin(p)) for p in (GAME / 'Data').iterdir()
                   if p.suffix.lower() in ('.esm', '.esp', '.esl')}
    config = {}
    for folder in (GAME, Path('C:/Users/User/Documents/My Games/Starfield'), Path('C:/Users/User/AppData/Local/Starfield')):
        for p in folder.iterdir():
            if p.is_file() and (p.suffix.lower() == '.ini' or p.name.lower() in ('plugins.txt', 'loadorder.txt')):
                config[str(p)] = pin(p)
    # Exact primary export pins for source-to-register correspondence.
    sources = list(csv.DictReader((ROOT / 'docs/experiments/resource-ui-oracle/sources.csv').open()))[:38]
    for row in sources:
        assert pin(ROOT / row['path']) == row['sha256'], row['path']
    b = (GAME / 'Starfield.exe').read_bytes()
    nt = struct.unpack_from('<I', b, 0x3c)[0]
    count, optional = struct.unpack_from('<H', b, nt+6)[0], struct.unpack_from('<H', b, nt+20)[0]
    sections = [struct.unpack_from('<8sIIIIIIHHI', b, nt+24+optional+i*40) for i in range(count)]

    def at(rva, n):
        for s in sections:
            if s[2] <= rva and rva+n <= s[2]+s[3]:
                offset = s[4]+rva-s[2]
                return b[offset:offset+n]
        raise ValueError('unmapped RVA')

    guards = {hex(rva): at(rva, 16).hex() for rva in (0x21b26bc, 0x21e0bf4, 0x21f6b58, 0x15796fc)}
    for site, dest in ((0x21b26bc, 0x21e07d0), (0x21e0bf4, 0x12ed2a0)):
        code = at(site, 5)
        assert code[0] == 0xe8 and site+5+struct.unpack_from('<i', code, 1)[0] == dest
    assert at(0x21f6b58, 4) == bytes.fromhex('488b5108')
    # bm001: MOVZX EBX,AL (not a byte-sized MOV BL,AL).
    assert at(0x15796fc, 3) == bytes.fromhex('0fb6d8')
    space = {d: shutil.disk_usage(d).free for d in ('C:/', 'D:/')}
    assert min(space.values()) >= 40_000_000_000
    value = dict(status='CHECKED_NOT_YET_ADMITTED', utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                 controller_sha256=pin(build / 'sor-c1d-controller.exe'), guards=guards,
                 definitions=definitions, config=config, source_pins=sources, protected_count=len(inputs), space=space,
                 qualification_sha256=pin(a.qualification), inherited_qualification=old,
                 load_map='Installed/config inventory only; actual runtime plugin load map not observed. Runtime FormIDs retained as such; no effective-override equivalence claim.',
                 plugin_files='Starfield.esm main baseline exact; active config frozen including unstarred ResourceGenerationTest.esp. No configuration change.')
    write(LOCAL / (a.name + '.json'), value)
    print('identity/static guards/definitions checked', len(definitions), 'protected', len(inputs), space)


if __name__ == '__main__':
    main()
