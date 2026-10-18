# SPDX-License-Identifier: GPL-3.0-or-later
"""Finite installed C2 source audit; stdlib and owned S1/ESM readers only.
Reads installed ESM/Misc.ba2/ContentResources.zip and local five PEX/five PSC
members. Writes one new ignored JSON receipt; never extracts/executes assets.
No original, analysis-project, target process, save, configuration or Git effect.
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
from catalog import pin
from inspect_outpost_definitions import esm_records
from inventory_historical_saves import guard


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--run', required=True)
    a = ap.parse_args()
    assert a.run.isalnum()
    guard()
    work = ROOT / '.local-work/c2-transport'
    game = Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield')
    paths = [game / 'Data/Starfield.esm', game / 'Data/Starfield - Misc.ba2',
             game / 'Tools/ContentResources.zip']
    before = [pin(p) for p in paths]
    definitions = []
    wanted = {b'GLOB', b'GMST', b'PACK', b'QUST', b'GBFM', b'NPC_', b'ACTI', b'PERK', b'AVIF', b'DFOB'}
    for r, fs in esm_records(paths[0], wanted, repeated=True):
        edid = next((v.rstrip(b'\0').decode() for k, v in fs if k == b'EDID'), '')
        if (r['formid'] in (0x2cb0, 0x255cc6, 0x219042, 0x495e, 0x39, 0x23826f, 0x2407e8, 0x2b344) or
                (r['type'] == 'PERK' and any(k == b'DATA' and len(v) == 3 and v[0] == 0xaa for k, v in fs)) or
                'cargolink' in edid.lower()):
            definitions.append(dict(r, edid=edid, fields=[(k.decode(), v.hex()) for k, v in fs]))
    stems = ('outpostcargolinkmarkerscript', 'sq_outpostcargolinkscript',
             'sq_outpostcargolinkshipscript',
             'pf_sq_outpostcargolinktravel_002457b0', 'pf_sq_outpostcargolinktravel_00255cc4')
    pex = []
    with paths[1].open('rb') as f:
        assert struct.unpack('<4sI4s', f.read(12)) == (b'BTDX', 2, b'GNRL')
        n, names = struct.unpack('<IQ', f.read(12))
        f.seek(32)
        entries = [struct.unpack('<I4sIIQIII', f.read(36)) for _ in range(n)]
        f.seek(names)
        filenames = [f.read(int.from_bytes(f.read(2), 'little')).decode() for _ in range(n)]
        for stem in stems:
            matches = [i for i, s in enumerate(filenames)
                       if s.lower().endswith('/' + stem + '.pex')]
            assert len(matches) == 1
            i = matches[0]
            _, _, _, _, off, packed, size, _ = entries[i]
            f.seek(off)
            b = f.read(packed or size)
            if packed:
                b = zlib.decompress(b)
            assert len(b) == size and b == (work / (stem + '.pex')).read_bytes()
            pex.append(dict(member=filenames[i], archive_offset=off, local=pin(work / (stem + '.pex'))))
    scripts = []
    with zipfile.ZipFile(paths[2]) as z:
        for name in ('OutpostCargoLinkMarkerScript', 'SQ_OutpostCargoLinkScript',
                     'SQ_OutpostCargoLinkShipScript',
                     'Fragments/Packages/PF_SQ_OutpostCargoLinkTravel_002457B0',
                     'Fragments/Packages/PF_SQ_OutpostCargoLinkTravel_00255CC4'):
            member = 'Scripts/Source/' + name + '.psc'
            local = work / (name.rsplit('/', 1)[-1] + '.psc')
            assert z.read(member) == local.read_bytes()
            scripts.append(dict(member=member, local=pin(local)))
    assert [pin(p) for p in paths] == before
    result = dict(inputs=before, definitions=definitions, pex=pex,
                  scripts=scripts, tool=pin(__file__), protected_unchanged=True)
    with (work / (a.run + '.json')).open('x', encoding='utf8', newline='\n') as out:
        json.dump(result, out, indent=2)
        out.write('\n')
    guard()
    print('PASS', len(definitions), 'selected definitions; five PEX and five PSC archive comparisons')


if __name__ == '__main__':
    main()
