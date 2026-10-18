# SPDX-License-Identifier: GPL-3.0-or-later
"""Finite C2 evidence receipt/pin and arithmetic checks; see README.md.

Reads ignored acquired evidence, protected inputs and Git HEAD/index only.
Writes one exclusive ignored JSON receipt. No target execution or mutation.
"""
import argparse
import hashlib
import json
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
    w = ROOT / '.local-work/c2-transport'
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
    sources = json.loads((w / 'sources03.json').read_text())
    check('five installed PEX and five source members matched',
          len(sources['pex']) == len(sources['scripts']) == 5 and sources['protected_unchanged'])
    for p in sources['inputs']:
        check('archive/input pin: ' + p['path'], pin(p['path']) == p)
    for row in sources['pex'] + sources['scripts']:
        check('member pin: ' + row['member'], pin(row['local']['path']) == row['local'])
    pex = json.loads((w / 'pex01.json').read_text())
    check('PEX closure/control receipt', pex['controls'] == dict(
        invalid_inputs_rejected=15, branch_targets_in_bounds=True))
    for name, row in pex.items():
        if name != 'controls':
            check('decoded PEX pin: ' + name,
                  hashlib.sha256((w / (name + '.pex')).read_bytes()).hexdigest() == row['sha256'])
    saved = json.loads((w / 'save02.json').read_text())
    check('saved source unchanged', pin(saved['source']['path']) == saved['source'])
    check('finite save coverage', saved['records'] == 205557 and len(saved['edges']) == 246
          and len(saved['ships']) == 24 and len(saved['rows']) == 929)
    rows = saved['rows']
    ships = [rows[t] for t in saved['ships']]
    check('selected ship bases', all(r['base'] in ('starfield.esm:255cc6', 'starfield.esm:219042') for r in ships))
    closed = [r for r in ships if r['inventory'].get('status') == 'DECODED_EMPTY_STACK_EXTRA_SUBSET']
    check('19 closed / 11 stocked / 8 empty / 5 gaps', len(closed) == 19
          and sum(r['inventory']['item_count'] > 0 for r in closed) == 11
          and sum(r['inventory']['item_count'] == 0 for r in closed) == 8)
    check('principal explicit empty', rows['82dc37']['inventory']['item_count'] == 0)
    byid = {r['identity']: r for r in rows.values()}
    for identity, count in (('DYNAMIC:ff019341', 2), ('DYNAMIC:ff01c5b7', 1), ('DYNAMIC:ff047b8b', 1)):
        check('positive hold: ' + identity, byid[identity]['inventory']['item_count'] == count)
    # PE section translation: preferred VA is not a file offset.
    constants = {}
    with Path(baseline['protected'][0]['path']).open('rb') as f:
        f.seek(0x3c)
        pe = int.from_bytes(f.read(4), 'little')
        f.seek(pe + 6)
        n = int.from_bytes(f.read(2), 'little')
        f.seek(pe + 20)
        opt = int.from_bytes(f.read(2), 'little')
        f.seek(pe + 24 + opt)
        sections = []
        for _ in range(n):
            vs, va, rs, rp = struct.unpack_from('<4I', f.read(40), 8)
            sections.append((va, max(vs, rs), rp))
        for addr, expected in ((0x144f03fb4, '8988083d'), (0x144f04be4, 'abaa2642'),
                               (0x144f04e90, '00007a44'), (0x144f04768, '00000040'),
                               (0x144f04980, '00008040')):
            rva = addr - 0x140000000
            va, _, rp = next(s for s in sections if s[0] <= rva < s[0] + s[1])
            f.seek(rp + rva - va)
            b = f.read(4)
            check('native float bytes: ' + hex(addr), b.hex() == expected)
            constants[hex(addr)] = struct.unpack('<f', b)[0]
    f32 = lambda v: struct.unpack('<f', struct.pack('<f', v))[0]
    def ticks(seconds, ground):
        h = f32(f32(seconds / 3600) * ground)
        return int(f32(max(h, constants['0x144f03fb4']) * constants['0x144f04be4']))
    check('ground15 load5/takeoff2', (ticks(30, 15), ticks(15, 15)) == (5, 2))
    check('fallback30 load10/takeoff5', (ticks(30, 30), ticks(15, 30)) == (10, 5))
    check('minimum request one tick', ticks(0, 15) == 1)
    check('hypothetical wait jump rearms now', 1100 + ticks(15, 15) == 1102)
    # Finite arithmetic identity, not an execution model of the native planner.
    stages = [(100, 280, 40, 0, 0), (0, 280, 40, 0, 100),
              (0, 300, 40, 0, 80), (0, 300, 0, 0, 120), (0, 300, 0, 120, 0)]
    check('worked journey conserved420', all(sum(s) == 420 for s in stages))
    check('worked partial admission20/retention80', min(100, 300 - 280) == 20 and 100 - 20 == 80)
    check('mixed priority example two possible fits', 2 * 2 + 1 == 5 and 4 + 2 > 5)
    result = dict(checks=checks, count=len(checks), constants=constants, head=head,
                  tool=pin(__file__), limits='Receipt consistency, pins and finite arithmetic; no VM/native execution or historical voyage proof')
    with (w / (a.run + '.json')).open('x', encoding='utf8', newline='\n') as out:
        json.dump(result, out, indent=2)
        out.write('\n')
    guard()
    print('PASS', len(checks), 'C2 mechanical checks')


if __name__ == '__main__':
    main()
