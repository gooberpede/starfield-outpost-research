# SPDX-License-Identifier: GPL-3.0-or-later
"""S2 evidence binding, scalar traces and protected-input/regression checks.

Reads baseline, existing native/save receipts, owned sources and Git read-only.
Writes one fresh ignored receipt; --tables writes authored source/function
metadata CSVs. No game/native invocation, original/save/database/Git mutation or
network. CPython -B, stdlib and existing project modules; both-drive 40 GB guard.
No production logistics model or independent runtime oracle is implemented.
"""
import argparse
import csv
from fractions import Fraction
import json
import math
from pathlib import Path
import re
import struct
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'research/s1-storage'))
from catalog import pin
from inventory_historical_saves import guard


def f32(v):
    return struct.unpack('<f', struct.pack('<f', v))[0]


def fit(c, w, mass, q):
    free = f32(c - w)
    return 0 if free < mass else min(q, math.floor(f32(free / mass)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--run', required=True)
    ap.add_argument('--tables', action='store_true')
    args = ap.parse_args()
    assert args.run.isalnum()
    guard()
    base = ROOT / '.local-work/s2-links'
    out = base / (args.run + '.json')
    assert not out.exists()
    baseline = json.loads((base / 'baseline.json').read_text(encoding='utf8'))
    checks, sources = [], []

    def check(ok, label):
        assert ok, label
        checks.append(label)

    for p in baseline['protected'] + [baseline['index'], baseline['brief']]:
        check(pin(p['path']) == p, 'protected/pre ' + p['path'])
        sources.append(p)
    for p in baseline['starting_untracked'].values():
        check(pin(p['path']) == p, 'unrelated/supplied untracked preserved ' + p['path'])
    check(subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT).decode().strip()
          == baseline['head'], 'HEAD unchanged')
    db = Path('D:/ReverseEngineering/Starfield/GhidraProject')
    check({str(p) for p in db.rglob('*') if p.is_file()} ==
          {p['path'] for p in baseline['protected'] if 'GhidraProject' in p['path']},
          'database file inventory unchanged')
    saved = json.loads((base / 'saved01.json').read_text(encoding='utf8'))
    check(saved['all_supported_edges_equal'] and saved['edge_count'] == 246,
          'fresh protected original reproduces supported edge envelope')
    check(len(saved['selected_rows']) == 18 and len(saved['joined_edges']) == 9,
          '18 selected endpoint inventories, nine real owner-joined edges')
    check(all(e['common_explicit_owners'] for e in saved['joined_edges']),
          'selected edge endpoints have common explicit Workshop owner')
    for row in saved['selected_rows'].values():
        check(row['inventory']['status'] == 'DECODED_EMPTY_STACK_EXTRA_SUBSET',
              'qualified inventory ' + str(row['record_offset']))
        for p in row['producer_rows']:
            raw = bytes.fromhex(p['row']['payload_hex'])
            check(len(raw) == 17, 'producer wire body17 ' + str(p['row']['offset']))
            pending, iterations, eligible, remaining, interval = struct.unpack('<iiBff', raw)
            check(pending >= 0 and iterations > 0 and eligible in (0, 1)
                  and math.isfinite(remaining) and interval > 0,
                  'selected ordinary producer wire values, not output measurement')
    for p in saved['priors'] + [saved['source'], saved['tool']]:
        check(pin(p['path']) == p, 'save receipt input/tool pinned ' + p['path'])
        sources.append(p)
    for operands, expected in [((75, 70, .5, 10), 10), ((75, 74, .5, 10), 2),
                                ((75, 75, .5, 10), 0), ((75, 74.75, .5, 10), 0),
                                ((75, 73, .5, 8), 4), ((75, 60, .5, 20), 20)]:
        check(fit(*operands) == expected, 'fixed scalar fit ' + repr(operands))
    # Fork in traces: B fits2, A W73 fits4 (not6), so residual4.
    check(Fraction(75 - 74) / Fraction('.5') == 2 and
          Fraction(75 - 73) / Fraction('.5') == 4, 'independent rational fork capacities')
    check(f32(74.5 + f32(3 * .5)) == 76, 'whole production batch can cross C75')
    check(f32(f32(20 * .5) + f32(75 - 60)) == 25 < 75 and
          f32(60 + f32(2 * 20 * .5)) == 80, 'mixed planning counterexample, no reservations')
    check(math.trunc(f32(50 / 36)) == 1 and f32(5 - 10) == -5,
          'large elapsed/countdown paths differ from phase preserving cycles')
    native = {}
    exports = sorted((ROOT / '.local-work/recon').glob('s2-links-*.tsv'))
    for p in exports:
        t = p.read_text(encoding='utf8')
        check('SHA256\t' + baseline['protected'][0]['sha256'] in t,
              'native executable identity ' + p.name)
        native[p.stem.rsplit('-', 1)[1]] = t
        sources.extend([pin(p), pin(str(p) + '.log')])
    anchors = {
        '09': ['140f85585\tVSUBSS XMM7,XMM6,XMM0',
               '140f85592\tVROUNDSS XMM2,XMM2,XMM1,0x1',
               '140f85642\tADD qword ptr [R13 + 0x8],0x40',
               '140f8568f\tVADDSS XMM2,XMM1,XMM7',
               '140f85693\tVCOMISS XMM2,XMM6'],
        '10': ['BSTEventSource<TESObjectLoadedEvent>::vftable',
               'BSTEventSource<TESContainerChangedEvent>::vftable',
               '140f8c68a\tCMP dword ptr [RBX + -0x8],EAX',
               '140f8c6ae\tMOV dword ptr [RBX],0x0'],
        '01': ['140f7f1e0', 'FUN_1428ccc40', '140f84ede'],
        '02': ['140f82c30', 'FUN_140f82820', 'FUN_140f80af0'],
        '03': ['140f7d510', '140f7df8f', 'FUN_140b64fc0'],
        '08': ['FUN_140b9a340', '0x145916510', 'FUN_140b994d0', '0x145916518'],
        '11': ['140b41a30', '140f515a0', '140f50880'],
        '13': ['FUNCTION\t140f8a020', 'FUN_140b756c0', 'FUN_140346030',
               'FUNCTION\t140481010', 'FUNCTION\t140f8b570'],
    }
    for n, tokens in anchors.items():
        for token in tokens:
            check(token in native[n], 'native evidence anchor ' + n + ' ' + token)
    regressions = []
    for name in ['test_workshop_inventory.py', 'test_outpost_record_framing.py',
                 'test_stream_save.py', 'test_extractor_resources.py']:
        r = subprocess.run([sys.executable, '-B', '-m', 'unittest', 'discover',
                            '-s', 'save-analysis/scripts', '-p', name], cwd=ROOT,
                           capture_output=True, text=True)
        regressions.append(dict(command=name, returncode=r.returncode,
                                stdout=r.stdout, stderr=r.stderr))
        check(r.returncode == 0, 'regression ' + name)
        sources.append(pin(ROOT / 'save-analysis/scripts' / name))
    failures = []
    for n in range(1, 14):
        p = base / f'export{n:02}.log'
        if p.exists():
            t = p.read_text(encoding='utf8', errors='replace')
            failures.append(dict(export=n, script_error=('ERROR' in t or 'Exception' in t),
                                 log=pin(p)))
    for p in baseline['protected'] + [baseline['index'], baseline['brief']]:
        check(pin(p['path']) == p, 'protected/post ' + p['path'])
    for p in [base / 'saved01.json', ROOT / 'research/s2-links/saved_examples.py',
              Path(__file__), ROOT / 'ghidra/scripts/OutpostRecon.java',
              ROOT / 'ghidra/scripts/Invoke-OutpostRecon.ps1',
              ROOT / '.local-work/recon/scripts/OutpostContainerScript.psc',
              ROOT / '.local-work/s1-capacity/calculations03.json']:
        sources.append(pin(p))
    result = dict(checks=checks, regressions=regressions, sources=sources,
                  export_acquisition_errors=failures,
                  retained_failures=['WindowsApps python alias inaccessible; explicit installed interpreter used',
                                     'First saved join expected >=10 though nine fixed pairs selected; replaced arbitrary count with exact expected pair set',
                                     'Invalid guessed instruction windows in exports06/07/08/10; completed preceding functions retained, verified windows09/12 used'],
                  limits=['Scalar/locator checks are not native replay or RUNTIME evidence',
                          'No complete simulator, no actual current effective inventories'])
    with out.open('x', encoding='utf8', newline='\n') as f:
        json.dump(result, f, indent=2)
        f.write('\n')
    if args.tables:
        dest = ROOT / 'docs/experiments/local-output-links'
        with (dest / 'sources.csv').open('w', encoding='utf8', newline='') as f:
            w = csv.writer(f, lineterminator='\n')
            w.writerow(['path', 'bytes', 'sha256', 'classification'])
            for p in {p['path']: p for p in sources}.values():
                w.writerow([p['path'], p['bytes'], p['sha256'],
                            'Metadata REVIEW-REQUIRED; original/native/save payload LOCAL-ONLY'])
        wanted = {'140f81200', '140f81a90', '140f80af0', '140f82820', '140f82c30',
                  '140f84d70', '140f84fc0', '140f84c40', '140f7d510', '140f7d6a0',
                  '140f7ef20', '140f7f1e0', '140f7dfa0', '140f8c580', '140f7ee40',
                  '140f83020', '140f7e530', '140f7e6f0', '140f7ea10', '140f515a0',
                  '140f50880', '140f82160', '142077ac0', '1428ccc40', '140f83450',
                  '1421ad290', '1421ad550', '140f843e0', '140f894c0', '140f84470',
                  '140f85760', '140f8a020', '140481010', '140f8b570'}
        found = {}
        for p in exports:
            t = p.read_text(encoding='utf8')
            for m in re.finditer(r'^FUNCTION\t([0-9a-f]+)\t([^\n]+)\n(.*?)(?=^FUNCTION\t|\Z)', t, re.M | re.S):
                if m[1] in wanted and 'DECOMPILED\ttrue' in m[3]:
                    found[m[1]] = p
        assert set(found) == wanted, wanted - set(found)
        with (dest / 'functions.csv').open('w', encoding='utf8', newline='') as f:
            w = csv.writer(f, lineterminator='\n')
            w.writerow(['key', 'static_va', 'rva', 'original_name', 'source', 'scope', 'limits'])
            for i, (va, p) in enumerate(sorted(found.items()), 1):
                w.writerow([f'S2-{i:03}', '0x' + va, hex(int(va, 16) - 0x140000000),
                            'FUN_' + va, p.relative_to(ROOT).as_posix(),
                            'STATIC; analyst contracts in native.md/lifecycle.md; image base0x140000000',
                            'Instruction listings may cap600; full decompilation; no invocation/safe ABI'])
    guard()
    print('PASS', len(checks), 'checks;', len(regressions), 'regression suites')


if __name__ == '__main__':
    main()
