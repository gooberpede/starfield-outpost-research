# SPDX-License-Identifier: GPL-3.0-or-later
"""Finite offline evidence/accounting checks; reads/writes/effects in README.md."""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import struct
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'research/s1-storage'))
from catalog import pin
from inventory_historical_saves import guard


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--run', required=True)
    a = ap.parse_args()
    assert a.run.isalnum()
    guard()
    w = ROOT / '.local-work/c3-fuel'
    checks = []

    def check(label, condition):
        assert condition, label
        checks.append(label)

    baseline = json.loads((w / 'baseline.json').read_text())
    for p in baseline['protected']:
        check('protected unchanged: ' + p['path'], pin(p['path']) == p)
    for key in ('index', 'brief'):
        check(key + ' unchanged', pin(baseline[key]['path']) == baseline[key])
    head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT,
                                  env=dict(os.environ, GIT_OPTIONAL_LOCKS='0')).decode().strip()
    check('HEAD unchanged', head == baseline['head'])
    defs = json.loads((w / 'definitions01.json').read_text())
    check('fresh main ESM identity', pin(defs['source']['path']) == defs['source'])
    byid = {r['formid']: r for r in defs['rows']}

    def field(fid, name):
        return bytes.fromhex(next(v for k, v in byid[fid]['fields'] if k == name))

    check('actual fuel recipe IRES/count', struct.unpack('<III', field(0x214c92, 'FVPA')) == (0x57f5, 5, 0))
    check('null output still consumes', field(0x214c92, 'CNAM') == bytes(4))
    check('cargo resource AV/recipe/interval bindings',
          [int.from_bytes(field(0x21e6ff, k), 'little') for k in ('NAM1', 'NAM2', 'NAM3')]
          == [0x21e6fe, 0x214c92, 0x217854])
    f32 = lambda x: struct.unpack('<f', struct.pack('<f', x))[0]
    interval = f32(struct.unpack('<f', field(0x217854, 'FLTV'))[0] * 3600)
    check('fuel base interval exactly 108 binary32', interval == 108)
    check('whole recipes: 0/4/5/12 supply, request3',
          [min(3, n // 5) for n in (0, 4, 5, 12)] == [0, 0, 1, 2])
    check('split source threshold 4+1', (4 + 1) // 5 == 1)
    check('partial elapsed fuel debit leaves2', 12 - 5 * min(math.trunc(360 / interval), 12 // 5) == 2)
    check('modifier-compatible interval', f32(interval * f32(.95)) == 102.5999984741211)
    elapsed = f32(f32(900 / 15) * 1)
    check('declared wait chunk elapsed60', elapsed == 60)
    remaining = interval
    cycles = 0
    for _ in range(20):
        remaining = f32(remaining - elapsed)
        if remaining <= 0:
            cycles += 1
            remaining = interval
    check('case1 ten fuel cycles /150 remaining', cycles == 10 and 20 * 10 - cycles * 5 == 150)
    check('case1 ten extractors each one request', 10 * math.trunc(elapsed / 36) == 10)
    check('case1 calendar18000UT', 20 * elapsed * 15 == 18000)
    check('single-item saturation75', min(200, 75) == 75)
    check('case2 sequential partial unload retained15 then5', (20 - min(20, 100 - 95)) - 10 == 5)
    ticks = lambda s: int(f32(max(f32(f32(s / 3600) * 15), f32(.03333333507180214)) * f32(41.66666793823242)))
    check('cached ground15 timer5/2/5', [ticks(s) for s in (30, 15, 30)] == [5, 2, 5])
    check('one-shot rearm now1102/1105', (1100 + ticks(15), 1100 + ticks(30)) == (1102, 1105))
    exports = {p.name: p.read_text(encoding='utf8') for p in (w / 'native').glob('*.request.tsv')}
    e = exports['001.request.tsv']
    for s in ('140f7f3b0\tMOV DL,0x1', '140f7f3d3\tCALL 0x140f7d6a0',
              '140f7d4c2\tCMP dword ptr [RSP + 0x24],0x2',
              '140f7d4c7\tJZ 0x140f7d4f4', '140f7d831\tCALL 0x140f7f6f0'):
        check('decisive instruction: ' + s.split('\t')[0], s in e)
    check('concrete source removal virtual458', '0x458]' in e)
    check('Papyrus readiness mode0', 'FUN_140f7d120(param_3,0,param_3,param_4)' in exports['003.request.tsv'])
    scripts = json.loads((w / 'scripts01.json').read_text())
    check('five installed PEX and five sources', len(scripts) == 10 and sum('decoded' in r for r in scripts.values()) == 5)
    methods = {}
    for name, r in scripts.items():
        if 'decoded' in r:
            for obj in r['decoded']['objects']:
                for state, fs in obj['states']:
                    for method, body in fs:
                        methods[(obj['name'], method)] = body
    body = json.dumps(methods[('SQ_OutpostCargoLinkScript', 'CargoLinkCanProduce')])
    check('either-pad method calls reverse links and predicate', all(x in body for x in ('GetRefsLinkedToMe', 'CanProduceForWorkshop', 'HasKeyword')))
    check('ready method has no removal operation', 'RemoveItem' not in body and 'RemoveAllItems' not in body)
    saved = json.loads((w / 'save01.json').read_text())
    check('saved source unchanged', pin(saved['source']['path']) == saved['source'])
    check('bounded saved coverage', saved['records'] == 205557 and len(saved['edges']) == 246 and len(saved['rows']) == 944)
    rows = {r['identity']: r for r in saved['rows'].values()}
    for fid, count in (('ff04fb23', 1), ('ff050483', 150), ('ff036b0f', 15), ('ff036b11', 15)):
        inv = rows['DYNAMIC:' + fid]['inventory']
        check('physical He3 source ' + fid,
              inv['status'] == 'DECODED_EMPTY_STACK_EXTRA_SUBSET'
              and inv['rows'][0]['item'] == 'starfield.esm:00558e'
              and inv['rows'][0]['stacks'][0]['count'] == count)
    edges = set(map(tuple, saved['edges']))
    for source, target in (('ff0428f5', 'ff04fb23'), ('ff04fb23', 'ff04fad9'),
                           ('ff036b0f', 'ff050483'), ('ff036b11', 'ff050483'), ('ff050483', 'ff02b86b')):
        check('actual source edge ' + source + ' -> ' + target,
              ('DYNAMIC:' + source, 'DYNAMIC:' + target) in edges)
    for fid, eligible in (('ff0217b5', 0), ('ff04fad9', 1), ('ff020ce1', 0), ('ff02b86b', 0)):
        p = next(p for p in saved['producer_rows'] if p['row']['reference_identities'][0] == 'DYNAMIC:' + fid)
        values = struct.unpack('<iiBff', bytes.fromhex(p['row']['payload_hex']))
        check('actual pad producer payload ' + fid,
              p['resource'] == 'starfield.esm:21e6ff' and values == (0, 1, eligible, 30.271221160888672, 102.5999984741211))
    out = dict(checks=checks, count=len(checks), head=head, tool=pin(__file__),
               limits='Finite evidence/accounting checks; no native/VM execution or historical voyage proof')
    (w / (a.run + '.json')).open('x', encoding='utf8', newline='\n').write(json.dumps(out, indent=2) + '\n')
    guard()
    print('PASS', len(checks), 'finite checks')


if __name__ == '__main__':
    main()
