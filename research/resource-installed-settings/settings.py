# SPDX-License-Identifier: GPL-3.0-or-later
"""Offline installed GMST audit; stdlib and the owned ESM reader only.

Reads pinned EXE, installed plugins/configuration and prior native provenance.
Writes a fresh local JSON; never loads a plugin or changes game/analysis state.
Installed files are a bounded audit, not a reconstructed historical load order.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import struct
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'save-analysis/scripts'))
from inspect_outpost_definitions import esm_records

CLASSES = ('Common', 'Uncommon', 'Rare', 'Exotic', 'Unique', 'Special')
IDS = (0x2d40c0, 0x226b0c, 0x226b0e, 0x226b0d, 0x2f031c, 0x2d40ce)
CONSTANTS = (0x144f04250, 0x144f041cc, 0x144f040c0, 0x144f03eec, None, 0x144f04250)

def pin(path):
    with Path(path).open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()

def bits(value):
    return f'0x{struct.unpack("<I", struct.pack("<f", value))[0]:08x}'

def parse_setting(header, fields, rarity):
    if type(rarity) is not int or not 0 <= rarity < 6:
        raise ValueError('unsupported setting rarity')
    fields = dict(fields)
    expected = 'fInactiveResourceChanceMult'+CLASSES[rarity]
    if header['type'] != 'GMST' or header['formid'] != IDS[rarity]:
        raise ValueError('GMST record identity mismatch')
    if fields.get(b'EDID') != expected.encode()+b'\0' or len(fields.get(b'DATA', b'')) != 4:
        raise ValueError('GMST name or binary32 DATA mismatch')
    raw = fields[b'DATA']
    if not math.isfinite(struct.unpack('<f', raw)[0]):
        raise ValueError('nonfinite GMST DATA')
    return dict(rarity=rarity, name=expected, formid=f'0x{IDS[rarity]:08x}',
                record_header_file_offset=header['offset'], installed_le_bytes=raw.hex(),
                installed_bits=f'0x{int.from_bytes(raw, "little"):08x}',
                installed_value=struct.unpack('<f', raw)[0])

def resolve(rarity, mask, settings, branch='ordinary'):
    if type(rarity) is not int or not 0 <= rarity <= 6:
        raise ValueError('unsupported rarity')
    if type(mask) is not int or not 0 <= mask <= 15:
        raise ValueError('unsupported ordinary mask')
    if branch == 'everywhere' and rarity == 6:
        return 1.0
    if branch != 'ordinary':
        raise ValueError('unsupported selection branch')
    if mask != 8 and rarity <= mask:
        return 1.0
    if rarity == 6:
        return 0.0
    if set(settings) != set(range(6)):
        raise ValueError('complete rarity settings required')
    if any(type(v) not in (int,float) or not math.isfinite(v) for v in settings.values()):
        raise ValueError('finite numeric settings required')
    return settings[rarity]

def audit():
    game = Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield')
    exe = game/'Starfield.exe'
    assert pin(exe) == '7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28'
    assert pin(game/'Data/Starfield.esm') == '1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7'
    plugins = sorted(p for p in (game/'Data').iterdir() if p.suffix.lower() in ('.esm','.esp','.esl'))
    config = []
    for folder in (game, Path('C:/Users/User/Documents/My Games/Starfield'), Path('C:/Users/User/AppData/Local/Starfield')):
        config.extend(p for p in folder.iterdir() if p.is_file() and (p.suffix.lower()=='.ini' or p.name.lower() in ('plugins.txt','loadorder.txt')))
    paths = [exe, *plugins, *config]
    before = {str(p):pin(p) for p in paths}
    blob = exe.read_bytes()
    nt = struct.unpack_from('<I', blob, 60)[0]
    count = struct.unpack_from('<H', blob, nt+6)[0]
    opt = struct.unpack_from('<H', blob, nt+20)[0]
    sections = [struct.unpack_from('<8sIIIIIIHHI', blob, nt+24+opt+i*40) for i in range(count)]
    def offset(va):
        rva = va-0x140000000
        s = next(s for s in sections if s[2] <= rva and rva+4 <= s[2]+s[3])
        return s[4]+rva-s[2]
    rows, candidates, walked = {}, [], {}
    names = {'fInactiveResourceChanceMult'+c for c in CLASSES}
    for plugin in plugins:
        walked[plugin.name] = 0
        for h, fs in esm_records(plugin, {b'GMST'}, repeated=True):
            walked[plugin.name] += 1
            fields = dict(fs)
            name = fields.get(b'EDID',b'').rstrip(b'\0').decode('utf8')
            if name in names or h['formid'] in IDS:
                candidates.append(dict(file=plugin.name, formid=f'0x{h["formid"]:08x}', name=name,
                                       offset=h['offset'], data=fields.get(b'DATA',b'').hex()))
            if plugin.name == 'Starfield.esm' and name in names:
                rarity = CLASSES.index(name.removeprefix('fInactiveResourceChanceMult'))
                assert rarity not in rows
                rows[rarity] = parse_setting(h, fs, rarity)
    assert set(rows) == set(range(6))
    for rarity, row in rows.items():
        va = CONSTANTS[rarity]
        raw = blob[offset(va):offset(va)+4] if va else b'\0'*4
        row.update(default_le_bytes=raw.hex(), default_bits=f'0x{int.from_bytes(raw,"little"):08x}',
                   default_value=struct.unpack('<f',raw)[0], constant_static_va=hex(va) if va else None,
                   constant_file_offset=offset(va) if va else None,
                   initializer_static_va=hex(0x140051240+rarity*0x30),
                   setting_payload_static_va=hex(0x145e901b8+rarity*0x20),
                   differs=raw.hex()!=row['installed_le_bytes'])
    config_mentions = [dict(file=str(p), line=i, setting=name) for p in config
                       for i,line in enumerate(p.read_text(encoding='utf-8-sig',errors='replace').splitlines(),1)
                       for name in names if name.lower() in line.lower()]
    assert before == {str(p):pin(p) for p in paths}
    return dict(schema='sor-c1h-settings/1', settings=list(rows.values()), pins=before,
                gmst_records_walked=walked, candidates=candidates, config_mentions=config_mentions,
                resolution='Installed main ESM values; audit candidates retained, historical load order and console/INI writers UNKNOWN')

if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output', type=Path, required=True)
    a = ap.parse_args()
    assert a.output.resolve().is_relative_to(ROOT/'.local-work/resource-installed-settings')
    result = audit()
    with a.output.open('x',encoding='utf8',newline='\n') as f:
        json.dump(result,f,indent=2); f.write('\n')
    print('settings',len(result['settings']),'files',len(result['pins']),'candidates',len(result['candidates']))
