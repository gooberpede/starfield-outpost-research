# SPDX-License-Identifier: GPL-3.0-or-later
"""L2 evidence correspondence verification; CPython stdlib/project methods.

Run from the repository root with -B and --run NEW. Reads ignored L2 native,
definition/menu/save receipts, pinned game/archive/save originals, HEAD/index
and owned framing methods. Independently decompresses each selected saved input
in memory to check exact primary float bytes and BF masks. Writes one exclusive
ignored JSON receipt. No game/ActionScript/native execution, save/database edits,
network, dependency install, staging or other Git mutation. Both-drive guard.
Checks establish correspondence/integrity, not an independent semantic oracle.
"""
from pathlib import Path
import argparse
import hashlib
import json
import struct
import subprocess
import sys

ROOT = Path.cwd()
WORK = ROOT / '.local-work/l2-budget'
sys.path[:0] = [str(ROOT / 'save-analysis/scripts')]
from inventory_historical_saves import guard, framing, transform
from outpost_record_framing import Reader


def pin(path):
    path = Path(path)
    with path.open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    return dict(path=str(path), bytes=path.stat().st_size, sha256=digest)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--run', required=True)
    args = parser.parse_args()
    assert args.run.isalnum()
    guard()
    checks = []
    pins = {}

    def check(condition, description):
        if not condition:
            raise AssertionError(description)
        checks.append(description)

    def read(name):
        path = WORK / name
        pins[str(path)] = pin(path)
        return json.loads(path.read_text(encoding='utf8'))

    baseline = read('baseline.json')
    for expected in baseline['protected']:
        actual = pin(expected['path'])
        check(actual == expected, 'protected unchanged: ' + expected['path'])
        pins[actual['path']] = actual
    check(subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode().strip() == baseline['head'],
          'HEAD unchanged')
    check(pin(ROOT / '.git/index') == baseline['index'], 'index unchanged')
    check(pin(baseline['brief']['path']) == baseline['brief'], 'supplied brief unchanged')

    native = {}
    for path in sorted((WORK / 'native').glob('*.request.tsv')):
        text = path.read_text(encoding='utf8')
        pins[str(path)] = pin(path)
        check('SHA256\t7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28\n' in text
              and 'BASE\t140000000\n' in text, path.name + ': imported EXE/base')
        check(path.with_suffix('').with_suffix('.request.done').exists(), path.name + ': completed request')
        native[path.name[:3]] = text
    for n, needles in {
        '003': ['WorkshopBudgetMultiplier_DO', 'WorkshopBudgetBaseline_DO',
                'fBudgetBaseCost:Workshop', 'fBudgetBaseline:Workshop',
                '140d9c070\tMOV EDX,0xdd', '140d9c07d\tMOV qword ptr [RBX + 0x450],RAX'],
        '005': ['140f4c814\tVMOVSS XMM6,dword ptr [0x145f0cdb0]',
                '140f4c95c\tVMULSS XMM0,XMM7,XMM6',
                '140f4c9d1\tVADDSS XMM6,XMM0,XMM6',
                '140f4cac7\tVSUBSS XMM1,XMM0,XMM6',
                '140f4cbe2\tVDIVSS XMM0,XMM0,XMM7'],
        '006': ['FUN_140f4c980(fVar12,plVar8)', '1421de838\tCALL qword ptr [RAX + 0x1d0]',
                '1421de841\tCALL 0x140f4ca70', 'fVar34 + fVar37 <= fVar33'],
        '007': ['140f40274\tCMP byte ptr [RSI + 0x620],0x0',
                '140f4027d\tMOV byte ptr [RDI + 0xc3],0x1e', 'FUN_140f6e260'],
        '011': ['param_2 + 700', 'ActorValueInfo::vftable'],
        '014': ['140f33500\tCALL qword ptr [RAX + 0x1d0]',
                '140f33506\tVMOVSS dword ptr [RSI + 0x78],XMM0'],
        '017': ['FUNCTION\t1419aec20', 'FUNCTION\t1419aeff0', 'FUNCTION\t140f50660',
                'FUNCTION\t140f50880', 'OutpostPackinCollisionPrimitiveKeyword_DO'],
        '018': ['FUNCTION\t14038a200', '1421baa65\tJMP 0x1421f2cb0'],
        '020': ['1421b2370\tCMP byte ptr [R8 + 0x193],0x2',
                '1421b2e4f\tCMP byte ptr [R8 + 0x193],0x2'],
        '021': ['case 0x1e:', 'PTR_s_Cannot_place_item__The_workshop__145912f18'],
        '025': ['case', 'uVar9 = 0x10', 'uVar9 = 0x1f', 'piVar7[1] = piVar7[1] | uVar9']
    }.items():
        for needle in needles:
            check(needle in native[n], n + ': ' + needle)

    settings = read('settings01.json')
    check(settings['constants'] == {'0x144f044e8': 1.0, '0x144f04980': 4.0,
                                    '0x144f04f28': 2500.0}, 'compiled constant operands')
    for row in settings['configs']:
        check(pin(row['source']['path']) == row['source'], 'configuration source unchanged')
    definitions = read('definitions01.json')
    check(pin(definitions['source']['path']) == definitions['source'], 'definition source unchanged')
    by = {r['formid']: r for r in definitions['records']}
    for formid in (0xba33d, 0xba33e, 0xba33f, 0xba340):
        check(dict(by[formid]['fields'])['DATA'] == '00000000', 'main GMST zero: ' + hex(formid))
    check(dict(by[0x319871]['fields'])['DATA'] == '72983100', 'baseline DFOB points to actual AVIF')
    check(dict(by[0x319872]['fields'])['NAM0'] == '00000000', 'baseline AV default zero')
    examples = read('examples01.json')
    check(len(examples['records']) == 9, 'nine exact physical example records')
    check(pin(examples['screenshot']['path']) == examples['screenshot'], 'supplied screenshot unchanged')

    expected = dict(S1=7, S1C=7, S2=8, S2C=8, S3=10, S3C=10, S4=10, S4C=10,
                    S5=10, S5C=10, S6=10, S6C=10, S7=9, S7C=9, exit=9)
    observed = {}
    for path in sorted(WORK.glob('save-*.json')):
        j = read(path.name)
        check(pin(j['source']['path']) == j['source'], j['label'] + ': saved source pin')
        raw = Path(j['source']['path']).read_bytes()
        _, spans = framing(raw)
        data = transform(raw, spans, True)
        check(j['source_unchanged'], j['label'] + ': scanner post-read pin')
        values = []
        for beacon in j['beacons']:
            extra = beacon['extras']
            check(extra['status'] == 'COUNT_CLOSED', j['label'] + ': closed beacon extra list')
            for row in extra['extras']:
                if row['type'] != 'bf':
                    continue
                cursor = Reader(data, row['offset'] + 1, row['end'])
                check(data[row['offset']] == 0xbf, j['label'] + ': primary BF tag')
                for section in row['sections']:
                    count = cursor.count()
                    check(count == len(section['avs']), j['label'] + ': primary AV count')
                    mask = cursor.take((section['bits'] * count + 7) // 8)
                    selected = iter(section['values'])
                    for bit in range(count * section['bits']):
                        if not mask[bit // 8] & (1 << (bit % 8)):
                            continue
                        v = next(selected)
                        check(cursor.p == v['offset'] and v['av'] == section['avs'][bit // section['bits']],
                              j['label'] + ': independently walked masked float offset')
                        value = struct.unpack('<f', cursor.take(4))[0]
                        check(value == v['value'], j['label'] + ': primary float bytes')
                        if v['av'] == 'starfield.esm:000399':
                            check(section['bits'] == 1 and v['bit'] == 0,
                                  j['label'] + ': budget in base section')
                            values.append(value)
                check(cursor.p == row['end'], j['label'] + ': BF exact byte closure')
        if j['label'] in expected:
            check(values == [expected[j['label']]], j['label'] + ': expected controlled budget')
            observed[j['label']] = values[0]
        elif j['label'] in ('S0', 'S0C'):
            check(not j['beacons'], j['label'] + ': no sampled beacon; not fabricated budget zero')
        else:
            check(len(values) == len(j['beacons']), j['label'] + ': explicit budgets on detected beacons')
    check(set(observed) == set(expected), 'all 15 positive Kreet controls covered')

    ui = read('ui-source01.json')
    check(pin(ui['archive']['path']) == ui['archive'], 'Interface archive unchanged')
    check(pin(ui['selected'][0]['output']['path']) == ui['selected'][0]['output'], 'single selected SWF unchanged')
    abc = read('menu01.json')
    check(all(m['decoded_bytes'] == m['code_bytes'] and
              all(x[1] != 'UNKNOWN_STOP' for x in m['instructions']) for m in abc['methods']),
          'all selected ABC bodies fully framed without unknown opcode')
    meter = next(m for m in abc['methods'] if m['method'] == 621)
    check(meter['binding'].endswith('OnStatusDataUpdate') and
          [26, 'getproperty', 'fBuildLimit'] in meter['instructions'] and
          [30, 'callproperty', '22:::round', 1] in meter['instructions'] and
          [34, 'callpropvoid', 'gotoAndStop', 1] in meter['instructions'], 'exact meter consumer')
    timeline = read('timeline01.json')
    check(timeline['binding']['character'] == timeline['meter']['id'] == 118 and
          timeline['meter']['frames'] == timeline['show_frames'] == 100,
          'actual named meter resolves to 100-frame sprite')
    check(7 + 1 == observed['S2'] and 8 + 2 == observed['S3'] and
          observed['S6'] == observed['S5'] and observed['S7'] == observed['S6'] - 1,
          'add/delete/move model agrees with real controlled saved values')
    guard()
    out = WORK / (args.run + '.json')
    with out.open('x', encoding='utf8', newline='\n') as stream:
        json.dump(dict(checks=checks, check_count=len(checks), pins=list(pins.values()),
                       verifier=pin(__file__), limits='Correspondence and integrity only; no live oracle or publication clearance'),
                  stream, indent=2)
        stream.write('\n')
    print('PASS', len(checks), 'checks', out)


if __name__ == '__main__':
    main()
