# SPDX-License-Identifier: GPL-3.0-or-later
"""LO1 finite offline verification; effects/prerequisites in adjacent README.
Original assertions over primary exported operations and installed metadata.
Reuses owned disk/text validators; no native/AS execution or source mutation.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import struct
import subprocess
import sys

R = Path.cwd()
W = R / '.local-work/lo1-locations'
sys.path.insert(0, str(R / 'save-analysis/scripts'))
from inventory_historical_saves import guard
sys.path.insert(0, str(R / 'research/s1-storage'))
from text_validation import validate_authored


def pin(p):
    p = Path(p)
    with p.open('rb') as f:
        return dict(path=str(p), bytes=p.stat().st_size,
                    sha256=hashlib.file_digest(f, 'sha256').hexdigest())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--run', required=True)
    a = ap.parse_args()
    assert re.fullmatch('[A-Za-z0-9-]+', a.run)
    out = W / ('verification-' + a.run + '.json')
    assert not out.exists()
    guard()
    checks = []

    def check(label, truth):
        assert truth, label
        checks.append(label)

    base = json.loads((W / 'baseline.json').read_text())
    for p in base['protected']:
        check('protected:' + p['path'], pin(p['path']) == p)
    check('brief', pin(base['brief']['path']) == base['brief'])
    check('HEAD', subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode().strip() == base['head'])
    check('index', pin(R / '.git/index') == base['index'])

    def native(n, va, *tokens):
        s = (W / 'native' / (n + '.request.tsv')).read_text()
        check(n + ':image', 'SHA256\t' + base['protected'][2]['sha256'] in s
              and 'BASE\t140000000' in s)
        parts = re.split(r'(?m)^FUNCTION\t', s)
        body = next(p for p in parts[1:] if p.startswith(va + '\t'))
        body = re.split(r'(?m)^(?:FUNCTION|REFERENCE_TARGET|DATA_WINDOW|WINDOW)\t', body)[0]
        check(n + ':' + va + ':decomp', 'DECOMPILED\ttrue' in body)
        for token in tokens:
            check(n + ':' + va + ':' + token, token in body)
        return body

    collect = native('027', '141360e80', 'FUN_140f3bfc0', 'FUN_14047fce0',
                     'FUN_140347170', 'FUN_141976dc0', 'VCVTTSS2SI R12D,XMM0',
                     'FUN_14136ac90', 'DAT_145f0ba80')
    check('long collector complete instructions', 'INSTRUCTION_LIMIT_REACHED' not in collect)
    native('016', '141976dc0', 'param_1 + 0x1f0', 'FUN_1419af700')
    native('016', '1419776f0', 'pfVar8[1] + *pfVar8 + pfVar8[2]', 'fVar12 + fVar11')
    native('012', '140f3bfc0', 'DAT_145f0c6d0', 'param_1 + 0x68')
    native('023', '1401595f0', '145f0c688', '144c266e0')
    native('023', '1409e6c20', 'param_1[9] = 0', 'BGSDefaultObject::vftable')
    native('005', '14135d890', '"$NONE"', '0xffffffff', 'lVar9 + 0xd8',
           'lVar9 + 0xa0', 'FUN_140aba950', 'lVar15 + 0x158', 'FUN_14172bc70')
    native('006', '140aba950', 'param_1 + 0xc0', 'DAT_145eacec8',
           'DAT_145e8fb68', 'DAT_145e8fb10')
    metadata = native('027', '14135f0e0', 'FUN_140786690', 'FUN_140910af0',
                      'lVar15 + 0xa9', 'DAT_145e85bf8', 'DAT_145e85c58',
                      'FUN_141369b80')
    check('long metadata complete instructions', 'INSTRUCTION_LIMIT_REACHED' not in metadata)
    native('016', '140aab770', 'param_1 + 9', '*param_1 = (ulonglong)uVar6')
    native('012', '140ab8030', '0x41544144', 'FUN_140aab770', 'param_1 + 0x14')
    native('026', '140ab9f80', 'param_1 + 0xa0', 'FUN_1402b9480')
    native('021', '1416aab70', '"focusedBodyID"', '"childInfoA"')
    native('021', '14136cf60', '"uBodyID"', '"fCoordsX"', '"fCoordsY"')
    native('008', '1413630c0', 'FUN_142be45c0', 'vminss_avx', 'local_164')

    ui = json.loads((W / 'ui01.json').read_text())
    prior = json.loads((R / '.local-work/sd3-stored/02.json').read_text())
    check('fresh nonexecuting parse equals SD3 compiled receipt', ui == prior)
    selected = [190, 585, 586, 726, 741, 742, 859, 862, 1005, 1170, 1171,
                1173, 1175, 1247, 1248, 1257, 1261, 1263, 1264, 1268,
                1270, 1271, 1279, 1285, 1286, 1288]

    def method(mid):
        m = next(m for m in ui['methods'] if m['method'] == mid)
        check('ABC decoded:' + str(mid), m['decoded_bytes'] == m['code_bytes']
              and not any(i[1] == 'UNKNOWN_STOP' for i in m['instructions']))
        return m['instructions']

    ms = {i: method(i) for i in selected}

    def tokens(mid, *values):
        data = json.dumps(ms[mid])
        for value in values:
            check('ABC:' + str(mid) + ':' + value, value in data)

    tokens(1279, 'SetFilterComparitor', 'InitializeEntries', 'entryCount', 'MaxOutposts')
    check('outpost filter null', ms[1279][4][1] == '0x20')
    tokens(1270, 'iCargoLinks', 'iCrewCount', 'iPowerGenerated', 'iPowerRequired',
           'fBuildLimit', 'framesLoaded', 'round', 'gotoAndStop', 'fProductionPerMin')
    tokens(1285, 'sSystemName', 'sBodyName', 'sFactionName', 'iFactionType',
           'uSystemMinLevel', 'uSystemChallengeLevel')
    tokens(1268, 'uSystemID', 'SetHoveredSystem', 'uBodyID', 'dispatchEvent')
    tokens(1264, 'focusedBodyID', 'SetBodyHighlight')
    tokens(726, 'sunRadiusPercent', 'scanned', 'color', 'childInfoA')
    tokens(1173, 'fCoordsX', 'fCoordsY')
    tokens(1171, 'VericalLine_mc', 'HorizontalLine_mc')

    assets = json.loads((W / 'assets01.json').read_text())
    check('movie source pin', assets['input_sha256'] == pin(W / 'LocationsPage.swf')['sha256']
          == '3977612bf4f8285ac6dfed149a8ce01c23ac8ccc5e8c1673be40434978c4998d')
    check('Locations meter frames100', assets['sprites']['149']['frames'] == 100
          and any(h['name'] == 'BuildLimitMeter_mc' and h['character'] == 149
                  and h['owner'] == 152 for h in assets['bindings']))
    labels = [r['label'] for r in assets['sprites']['154']['labels']]
    check('actual faction art labels', labels == ['BlackFleet', 'FreestarCollective',
          'HouseVaruun', 'RyujinIndustries', 'UnitedColonies', 'Constellation', 'None'])
    check('additional helper labels lack matching clip labels',
          all(s not in labels for s in ['TrackersAlliance', 'TerranArmada', 'Creations']))

    defs = json.loads((W / 'controls02.json').read_text())
    by = {r['formid']: r for r in defs['records']}

    def field(fid, key):
        return next(bytes.fromhex(v) for k, v in by[fid]['fields'] if k == key)

    check('finite source14', len(by) == 14)
    check('Narion definition owner and level', int.from_bytes(field(0x615b0, 'DATA')[:4], 'little')
          == 0x638e5 and field(0x615b0, 'DATA')[5] == 1)
    check('Schrodinger definition owner and level', field(0x61547, 'DATA')[:4] == bytes(4)
          and field(0x61547, 'DATA')[5] == 65)
    check('faction keyword separate from FACT', by[0x638e5]['type'] == 'FACT'
          and by[0x546df]['type'] == 'KYWD'
          and int.from_bytes(field(0x638e5, 'DNAM'), 'little') == 0x546df
          and int.from_bytes(field(0x137e5c, 'DATA'), 'little') == 0x546df)
    check('decorate keyword actual DFOB', int.from_bytes(field(0x3e4f4a, 'DATA'), 'little')
          == 0x3e4f4b and field(0x3e4f4b, 'EDID') == b'WorkshopUseDecorateTextKeyword\0')
    strings = json.loads((W / 'localization02.json').read_text())
    check('English source name controls', strings['strings']['0000a898'] == 'Kreet'
          and strings['strings']['0000a9b2'] == 'Narion'
          and strings['strings']['0000a4a0'] == 'Schrodinger II'
          and strings['strings']['00006d04'] == 'Freestar Collective')
    check('localization preserved', pin(strings['source']['path']) == strings['source'])

    # Independent physical PE translation: instruction guards and configuration strings.
    exe = Path(base['protected'][2]['path']).read_bytes()
    pe = struct.unpack_from('<I', exe, 0x3c)[0]
    nsec = struct.unpack_from('<H', exe, pe + 6)[0]
    opt = struct.unpack_from('<H', exe, pe + 20)[0]
    sections = [struct.unpack_from('<IIII', exe, pe + 24 + opt + 40*i + 8)
                for i in range(nsec)]

    def raw(va, n):
        rva = va - 0x140000000
        _, start, size, off = next(s for s in sections if s[1] <= rva < s[1]+s[2])
        check('PE physical range:' + hex(va), rva+n <= start+size)
        return exe[off+rva-start:off+rva-start+n]

    check('physical maximum conversion', raw(0x141361a2a, 4) == bytes.fromhex('c57a2ce0'))
    for va, value in [(0x1400255c4, 11), (0x1400255f4, 21),
                      (0x140025624, 31), (0x140025654, 51)]:
        check('physical threshold:' + hex(va), raw(va, 6) == b'\x41\xb8'+struct.pack('<I', value))
    check('physical exclusion default name', raw(0x144c266e0, 180).split(b'\0')[0]
          == b'WorkshopUseDecorateTextKeyword_DO')
    check('physical Freestar default name', raw(0x144c08bd0, 100).split(b'\0')[0]
          == b'FactionFreestar_DO')

    for p in sorted((R / 'docs/experiments/locations-outpost').glob('*.md')):
        b = p.read_bytes()
        validate_authored(b, str(p))
        check('authored UTF8/LF:' + p.name, b'\r' not in b and not b.startswith(b'\xef\xbb\xbf'))
        s = b.decode()
        check('prose spacing:' + p.name, not re.search(r'\b(?:the|and|from|with)[A-Z][a-z]', s))
        for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', s):
            name = target.split('#')[0].strip('<>')
            if name and not re.match(r'[A-Za-z]+:', name):
                check('link:' + p.name + ':' + name, (p.parent / name).resolve().exists())
    guard()
    receipt = dict(result='PASS', checks=checks, count=len(checks),
                   scope='STATIC identity/selected operations and metadata; no live/renderer oracle',
                   verifier=pin(Path(__file__)), head=base['head'], index=base['index'])
    out.open('x', encoding='utf8', newline='\n').write(json.dumps(receipt, indent=2)+'\n')
    print('PASS', len(checks), 'checks;', out)


if __name__ == '__main__':
    main()
