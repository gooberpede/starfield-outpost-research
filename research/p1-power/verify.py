# SPDX-License-Identifier: GPL-3.0-or-later
"""P1 integrity/reference audit. Stdlib and owned disk guard only.
Reads final local receipts, native exports, stopped database, protected inputs,
authored text, HEAD/index. Writes one exclusive ignored JSON receipt and source
metadata CSV with --pins. No game/native invocation or Git/database mutation.
Byte/table checks do not independently prove native semantics.
"""
import argparse
import ast
import csv
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / '.local-work/p1-power'
sys.path.insert(0, str(ROOT / 'save-analysis/scripts'))
from inventory_historical_saves import guard


def sha(p):
    with p.open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--run', required=True)
    ap.add_argument('--pins', action='store_true')
    a = ap.parse_args()
    assert a.run.isalnum()
    out = BASE / (a.run + '.json')
    assert not out.exists()
    guard()
    checks = []
    pins = {}

    def check(ok, label):
        assert ok, label
        checks.append(label)

    def pin(p):
        p = Path(p)
        pins[str(p)] = dict(path=str(p), bytes=p.stat().st_size, sha256=sha(p))
        return pins[str(p)]

    def verify_pin(row):
        check(pin(row['path'])['sha256'] == row['sha256'], 'input identity ' + str(row['path']))

    seed = json.loads((BASE / 'baseline.json').read_text())
    check(subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip() == seed['head'], 'HEAD preserved')
    verify_pin(seed['index'])
    for row in seed['files']:
        verify_pin(row)
    exe = Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield/Starfield.exe')
    exe_hash = pin(exe)['sha256']
    check(exe_hash == '7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28', 'retail executable identity')
    cat = json.loads((BASE/'definitions03.json').read_text())
    for row in [cat['source'],cat['cache'],cat['tool'],*cat['sources']]:
        if isinstance(row,dict) and 'path' in row:
            verify_pin(row)
    graph = json.loads((BASE/'saved/graph03.json').read_text())
    verify_pin(graph['tool'])
    for row in graph['inputs']:
        verify_pin(row)
        j = json.loads(Path(row['path']).read_text())
        verify_pin(j['source'])
        verify_pin(j['tool'])
        check(j['source_unchanged'], 'original save pre/post ' + j['sample'])
    db = json.loads((BASE/'db-before.json').read_text())
    for path, expected in db.items():
        check(sha(Path(path)) == expected, 'database unchanged ' + path)
    check((BASE/'native/stop').exists(), 'read-only session stopped')
    for request in sorted((BASE/'native').glob('*.request')):
        check(request.with_name(request.name+'.done').exists(), 'native request completed '+request.name)
        p = request.with_name(request.name+'.tsv')
        t = p.read_text()
        check('SHA256\t'+exe_hash in t and 'BASE\t140000000' in t, 'native identity '+request.name)
        check('DECOMPILED\tfalse' not in t, 'no failed decompile '+request.name)
        pin(p)
    additions = json.loads((BASE/'register-additions.json').read_text())
    rows = list(csv.DictReader((ROOT/'docs/experiments/native-availability-map/functions.csv').open(encoding='utf8')))
    for row in additions:
        check(row in rows, 'native registry row '+row['key'])
        check(int(row['static_va'],16)-0x140000000 == int(row['rva'],16), 'VA/RVA '+row['key'])
        check('FUNCTION\t'+row['static_va'][2:]+'\t' in (ROOT/row['source']).read_text(), 'function export '+row['key'])
        prose = ' '.join(row[k] for k in ['alias','decisive_window','inputs','outputs','prerequisites','effects','edges','confidence_basis','interface','limits'])
        check(not re.search(r'\b(?:retail|version|stride|word|operation|mask|offset)(?=[0-9])|\bat(?=(?:0x)?[0-9a-f]{9}\b)|ExtraFlags(?=[0-9])', prose, re.I), 'registry notation spacing '+row['key'])
    for p in (ROOT/'research/p1-power').glob('*.py'):
        ast.parse(p.read_text(encoding='utf8'))
        checks.append('Python AST '+p.name)
        pin(p)
    docs = list((ROOT/'docs/experiments/power').glob('*'))
    for p in docs:
        if not p.is_file():
            continue
        t = p.read_text(encoding='utf8')
        check(not p.read_bytes().startswith(b'\xef\xbb\xbf') and b'\r' not in p.read_bytes(), 'UTF8 LF '+p.name)
        check(all(x.rstrip()==x for x in t.splitlines()), 'whitespace '+p.name)
        check(not re.search(r'\b(?:STATIC|SAVE|RUNTIME|UNKNOWN|PASS|FAIL)(?:[0-9]|0x)',t), 'fused label audit '+p.name)
        if p.suffix=='.md':
            check(t.count('```')%2==0, 'fences '+p.name)
            for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',t):
                name=target.split('#')[0].strip('<>')
                if name and not re.match(r'[A-Za-z]+:',name):
                    check((p.parent/name).resolve().exists(),'link '+p.name+' '+target)
    subprocess.run(['git','diff','--check'],cwd=ROOT,check=True,capture_output=True)
    checks.append('git diff --check')
    for p in [BASE/'definitions03.json',BASE/'definitionVerification02.json',BASE/'saved/graph03.json',BASE/'power-perks01.json',BASE/'power-perks-recheck01.json',BASE/'planetScriptLocator01.json',BASE/'native/session.log',BASE/'native/E2ReadSession.java',ROOT/'ghidra/scripts/OutpostRecon.java',ROOT/'research/e3-fabricators/catalog.py',ROOT/'research/e2-organic/catalog.py']:
        pin(p)
    for n in ['static-exhaustion-23.tsv','active-outpost-static-30.tsv','static-exhaustion-08.tsv','e1-stacking-08.tsv']:
        pin(ROOT/'.local-work/recon'/n)
    if a.pins:
        s=io.StringIO(newline='')
        w=csv.writer(s,lineterminator='\n')
        w.writerow(['path','bytes','sha256','eligibility'])
        for row in sorted(pins.values(),key=lambda x:x['path']):
            path=Path(row['path'])
            try:
                label=path.relative_to(ROOT).as_posix()
            except ValueError:
                label=row['path']
            w.writerow([label,row['bytes'],row['sha256'],'LOCAL-ONLY original; metadata REVIEW-REQUIRED'])
        (ROOT/'docs/experiments/power/sources.csv').write_text(s.getvalue(),encoding='utf8',newline='\n')
    out.write_text(json.dumps(dict(checks=checks,pins=list(pins.values()),database_files=len(db),native_new_rows=len(additions),tool=pin(Path(__file__)),limits=['No new runtime values; hashes do not prove semantics; independent interpretation review required']),indent=2)+'\n',encoding='utf8',newline='\n')
    print('PASS',len(checks),'checks;',len(pins),'pins;',len(additions),'native rows')


if __name__ == '__main__':
    main()
