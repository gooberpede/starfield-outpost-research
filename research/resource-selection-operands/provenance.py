# SPDX-License-Identifier: GPL-3.0-or-later
"""Bounded OFFLINE PE/installed-definition provenance. Reads pinned EXE/main ESM,
owned record reader and supplied screenshots; writes fresh ignored JSON. No
target, save/config/analysis/Git writes, downloads or third-party incorporation.
Offsets are compressed-file record headers or PE file offsets as labelled.
"""
import argparse
import hashlib
import json
from pathlib import Path
import struct
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'save-analysis/scripts'))
from inspect_outpost_definitions import esm_records


def pin(path):
    with path.open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output', required=True, type=Path)
    a = ap.parse_args()
    assert a.output.resolve().is_relative_to(ROOT/'.local-work/resource-selection-operands')
    assert not a.output.exists()
    game = Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield')
    exe, esm = game/'Starfield.exe', game/'Data/Starfield.esm'
    before = {str(p):pin(p) for p in (exe, esm)}
    assert before[str(exe)] == '7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28'
    assert before[str(esm)] == '1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7'
    b = exe.read_bytes()
    nt = struct.unpack_from('<I', b, 60)[0]
    count = struct.unpack_from('<H', b, nt+6)[0]
    opt = struct.unpack_from('<H', b, nt+20)[0]
    sections = [struct.unpack_from('<8sIIIIIIHHI', b, nt+24+opt+i*40) for i in range(count)]
    def offset(va, n):
        rva = va-0x140000000
        for s in sections:
            if s[2] <= rva and rva+n <= s[2]+s[3]:
                return s[4]+rva-s[2]
        raise ValueError('unmapped VA')
    def data(va, n):
        at = offset(va, n)
        return b[at:at+n]
    defaults = []
    for rarity, va in enumerate((0x144f04250, 0x144f041cc, 0x144f040c0, 0x144f03eec, None, 0x144f04250)):
        raw = data(va, 4) if va else b'\0'*4
        table = struct.unpack('<I', data(0x14079c454+rarity*4, 4))[0]+0x140000000
        defaults.append(dict(rarity=rarity, constant_static_va=va, constant_file_offset=offset(va, 4) if va else None,
                             bits=raw.hex(), value=struct.unpack('<f', raw)[0],
                             setting_payload_static_va=0x145e901b8+rarity*0x20,
                             ordinary_switch_destination_static_va=table))
    records, gmst_count = [], 0
    for h, fields in esm_records(esm, {b'GMST', b'RSGD'}, repeated=True):
        edid = next((v.rstrip(b'\0').decode('utf8') for k,v in fields if k == b'EDID'), '')
        if h['type'] == 'GMST':
            gmst_count += 1
        if ('InactiveResourceChanceMult' in edid or
                edid in ('CanyonsDefaultRes', 'FrozenBarrenDefaultRes03', 'DesertRocksDefaultRes')):
            records.append(dict(**h, editor_id=edid, offset_domain='original ESM file record header',
                                fields=[(k.decode(),v.hex()) for k,v in fields]))
    screenshots = [dict(path=str(p.relative_to(ROOT)), sha256=pin(p), bytes=p.stat().st_size)
                   for p in sorted((ROOT/'.local-work/screengrabs').glob('ch-feynman-v-rsgd*.PNG'))]
    assert len(screenshots) == 7
    assert before == {str(p):pin(p) for p in (exe, esm)}
    out = dict(inputs=before, defaults=defaults, selected_main_records=records,
               main_gmst_records_walked=gmst_count, screenshots=screenshots,
               coverage='main ESM only, no runtime override merge or INI-loader assertion',
               guards={hex(va):data(va,16).hex() for va in (0x14079b520,0x14079be20,0x14079a59e,0x14079ff1d)})
    with a.output.open('x', encoding='utf8', newline='\n') as f:
        json.dump(out, f, indent=2)
        f.write('\n')
    print('defaults', defaults, 'selected records', [(r['type'], r['editor_id'], hex(r['formid'])) for r in records], 'GMST', gmst_count)


if __name__ == '__main__':
    main()
