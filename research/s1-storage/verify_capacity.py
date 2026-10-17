# SPDX-License-Identifier: GPL-3.0-or-later
"""S1 capacity qualification. Reads protected baseline, calculation/native
receipts and four existing owned regressions. Writes fresh ignored JSON and
optional authored hash ledger. Stdlib/owned readers only; no original, database,
game, configuration, dependency, network or Git mutation. CPython -B, repo cwd.
"""
import argparse
import csv
from fractions import Fraction
import json
from pathlib import Path
import struct
import subprocess
import sys
from catalog import ROOT, pin
from inventory_historical_saves import guard


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--run', required=True)
    ap.add_argument('--tables', action='store_true')
    ap.add_argument('--text-only', action='store_true', help='validate authored text without scientific input reads')
    a = ap.parse_args()
    assert a.run.isalnum()
    if a.text_only:
        from text_validation import audit_authored_text
        audit_authored_text(ROOT, a.run)
        return
    guard()
    base = ROOT / '.local-work/s1-capacity'
    out = base / (a.run + '.json')
    assert not out.exists()
    baseline = json.loads((base / 'baseline.json').read_text())
    checks, sources = [], []
    def check(ok, text):
        assert ok, text
        checks.append(text)
    for p in baseline['protected'] + [baseline['index'], baseline['brief']]:
        check(pin(p['path'])['sha256'] == p['sha256'], 'protected unchanged ' + p['path'])
        sources.append(pin(p['path']))
    check(subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT).decode().strip() == baseline['head'], 'HEAD unchanged')
    db = Path('D:/ReverseEngineering/Starfield/GhidraProject')
    check({str(p) for p in db.rglob('*') if p.is_file()} == {p['path'] for p in baseline['protected'] if 'GhidraProject' in p['path']}, 'database file inventory unchanged')
    calc = json.loads((base / 'calculations03.json').read_text())
    for p in calc['inputs'] + [calc['esm'], calc['cache'], calc['tool']]:
        check(pin(p['path']) == p, 'calculation input pinned ' + p['path'])
        sources.append(p)
    ex = {r['reference']: r for r in calc['examples']}
    check(len(ex) == 9 and calc['reread_records'] == 113, 'nine examples, 113 physically reread definitions/filter lists')
    # Independent expected binary32 bit results, not recalculated via capacity.py.
    expected = {'DYNAMIC:ff018b64': '00009642', 'DYNAMIC:ff018b66': '00009642',
                'DYNAMIC:ff01c792': '00000000', 'DYNAMIC:ff018b73': '00009643',
                'DYNAMIC:ff02c339': '9999ab42', 'DYNAMIC:ff018b61': '67669642'}
    for ref, bits in expected.items():
        check(struct.pack('<f', ex[ref]['occupied_binary32']).hex() == bits, 'independent expected weight bits ' + ref)
    # Rational arithmetic independently checks readable exact-decimal receipts.
    check(Fraction(41) * Fraction('1.8') + 3 * 4 == Fraction('85.8'), 'mixed decimal calculation 85.8; binary32 result deliberately distinct')
    check(Fraction(150) / 2 == 75 and Fraction(94) * Fraction('.8') > 75, 'exact decimal boundary and over-nominal controls')
    check(all(not r['saved_carryweight_values'] and 'e1' not in r['extra_types'] for r in ex.values()), 'closed selected extras have no saved CarryWeight or E1; runtime remains unknown')
    check(ex['DYNAMIC:ff01c792']['nominal_fit'] == 150 and ex['DYNAMIC:ff01ac54']['nominal_fit'] == 375, 'empty controls prospective fit includes binary32 division')
    check(all(ex[ref]['nominal_fit'] == 0 for ref in expected if ref != 'DYNAMIC:ff01c792'), 'boundary examples admit zero named positive-weight items under fallback')
    native = {}
    for p in sorted((ROOT / '.local-work/recon').glob('s1-capacity-*.tsv')):
        t = p.read_text()
        check('SHA256\t' + baseline['protected'][0]['sha256'] in t, 'native executable pin ' + p.name)
        native[p.stem.rsplit('-', 1)[1]] = t
        sources.append(pin(p))
        sources.append(pin(str(p) + '.log'))
    for n, tokens in {'01': ['140b65155\tCALL 0x140b70a80', '140b6517a\tMOV dword ptr [RSP + 0x60],EBX'],
                      '04': ['140b696fa\tCALL qword ptr [RAX + 0x4c8]', '140645e11\tMOV dword ptr [RSI + 0x3c],0xbf800000'],
                      '08': ['140b69c10\tVMOVAPS XMM0,XMM2'],
                      '16': ['140f85592\tVROUNDSS XMM2,XMM2,XMM1,0x1'],
                      '07': ['141eb0c37\tMOV dword ptr [RBP + 0x2e8],EAX']}.items():
        for token in tokens:
            check(token in native[n], 'checked instruction ' + token)
    regressions = []
    for name in ['test_workshop_inventory.py', 'test_outpost_record_framing.py', 'test_stream_save.py', 'test_extractor_resources.py']:
        r = subprocess.run([sys.executable, '-B', '-m', 'unittest', 'discover', '-s', 'save-analysis/scripts', '-p', name], cwd=ROOT, capture_output=True, text=True)
        regressions.append(dict(command=name, returncode=r.returncode, stdout=r.stdout, stderr=r.stderr))
        check(r.returncode == 0, 'regression ' + name)
        sources.append(pin(ROOT / 'save-analysis/scripts' / name))
    for p in ['capacity.py', 'verify_capacity.py']:
        sources.append(pin(ROOT / 'research/s1-storage' / p))
    for p in [base / 'calculations03.json', ROOT / 'ghidra/scripts/OutpostRecon.java', ROOT / 'ghidra/scripts/Invoke-OutpostRecon.ps1']:
        sources.append(pin(p))
    for p in baseline['protected']:
        check(pin(p['path']) == p, 'postflight protected ' + p['path'])
    guard()
    out.write_text(json.dumps(dict(checks=checks, regressions=regressions, sources=sources,
                                   limits=['No native execution or actual live acceptance measurement', 'Hashes/guard/regressions verify integrity and reader framing, not semantic truth'],
                                   prior_failed_paths=['c05/c06 invalid range-window selectors; later selectors omitted', 'interior address guesses are NO_FUNCTION_AT, not absence evidence']), indent=2) + '\n', encoding='utf8', newline='\n')
    if a.tables:
        with (ROOT / 'docs/experiments/storage/capacity-sources.csv').open('w', encoding='utf8', newline='') as f:
            w = csv.writer(f, lineterminator='\n')
            w.writerow(['path', 'bytes', 'sha256', 'classification'])
            for p in {p['path']: p for p in sources}.values():
                w.writerow([p['path'], p['bytes'], p['sha256'], 'Metadata REVIEW-REQUIRED; original/native/save payload LOCAL-ONLY'])
    print('PASS', len(checks), 'checks;', len(regressions), 'regression suites')


if __name__ == '__main__':
    main()
