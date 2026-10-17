# SPDX-License-Identifier: GPL-3.0-or-later
"""Audit follow-up evidence/inputs and all modified documentation; stdlib only.

Reads stopped native exports, original save/definition/executable pins, database
hash baseline, Git read-only inventory and authored text. Writes exclusive local
JSON and, with --pins, authored metadata CSV. Does not stage, run targets,
modify originals/databases or use network. Hashes do not prove interpretation.
"""
import argparse
import ast
import csv
import io
import json
import re
import subprocess
from pathlib import Path

from saved_instances import ROOT, pin, guard
from followup import replay, generation_walk


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, stderr=subprocess.PIPE)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--run', required=True)
    ap.add_argument('--pins', action='store_true'); args = ap.parse_args()
    assert args.run.isalnum()
    base = ROOT / '.local-work/p1-order'
    out = base / (args.run+'.json'); assert not out.exists()
    checks, pins, notes = [], {}, []
    def check(ok, label):
        assert ok, label
        checks.append(label)
    def add(path):
        p = Path(path); r = pin(p); pins[str(p)] = r; return r
    def verify(row):
        check(add(row['path'])['sha256'] == row['sha256'], 'pin '+row['path'])
    guard()
    baseline = json.loads((base/'baseline.json').read_text())
    check(git('rev-parse', 'HEAD').decode().strip() == baseline['head'], 'HEAD unchanged')
    verify(baseline['index'])
    for row in baseline['files']:
        relative = Path(row['path']).relative_to(ROOT)
        check(add(base/'baseline-tree'/relative)['sha256'] == row['sha256'],
              'follow-up baseline copy '+str(relative))
    db = json.loads((base/'db-before.json').read_text())
    for p, sha in db.items():
        check(add(p)['sha256'] == sha, 'database unchanged '+p)
    check((base/'native-r2/stop').exists(), 'native session stopped')
    for folder, requests in [('native', range(1, 10)), ('native-r2', [12])]:
        for n in requests:
            p = base/folder/f'{n:03}.request.tsv'
            check(p.with_suffix('.done').exists(), 'request done '+str(p))
            t = p.read_text()
            check('SHA256\t7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28' in t
                  and 'BASE\t140000000' in t, 'native identity '+str(p))
            check('DECOMPILED\tfalse' not in t, 'native no failed decompile '+str(p))
            add(p)
    for p in [base/'native/010.request.tsv', base/'native/session.log',
              base/'native-r2/session.log', base/'native/E2ReadSession.java',
              ROOT/'ghidra/scripts/OutpostRecon.java', base/'register-additions.json',
              base/'export.py', base/'baseline.json', base/'db-before.json']:
        add(p)
    notes.append('010 request stopped at invalid window instruction; 011 never executed; '
                 'fresh readOnly/noanalysis session 012 recovered required complete functions. '
                 'No completion marker invented for failed request.')
    j = json.loads((base/'saved/inspection02.json').read_text())
    verify(j['tool']); add(base/'saved/inspection02.json')
    for s, fixture in zip(j['samples'], j['fixtures']):
        verify(s['source']); verify(s['prior'])
        check(s['source_unchanged'], 'original pre/post '+s['sample'])
        check(replay(s) == fixture, 'actual tree replay exact '+s['sample'])
        switches = [r for r in s['rows'] if r['kind'] == 'SWITCH']
        expected = (86, 8) if s['sample'] == 'HIST-0036' else (62, 12)
        check((len(switches), sum(r['open_difference'] for r in switches)) == expected,
              'switch saved masks '+s['sample'])
        check(not any(r['default_difference'] for r in switches),
              'switch default-difference coverage '+s['sample'])
    cycle = dict(a=['b', 'c', 'd'], b=['a', 'd'], c=['a'], d=['a', 'b'])
    check(generation_walk(cycle, 'a') == ['a','d','b','c'], 'pending promotion control')
    check(generation_walk(cycle, 'a', True) == ['a','b','d','c'], 'recursive control')
    # Rehash the original P1 protected sources too; no replacement of prior receipts.
    old = json.loads((ROOT/'.local-work/p1-power/verification06.json').read_text())
    for row in old['pins']:
        if not Path(row['path']).is_relative_to(ROOT) or '/saved/instances' in row['path'].replace('\\','/'):
            verify(row)
    additions = json.loads((base/'register-additions.json').read_text())
    rows = list(csv.DictReader((ROOT/'docs/experiments/native-availability-map/functions.csv').open(encoding='utf8')))
    for row in additions:
        check(row in rows, 'register row '+row['key'])
        check(int(row['static_va'],16)-0x140000000 == int(row['rva'],16), 'VA/RVA '+row['key'])
        check('FUNCTION\t'+row['static_va'][2:]+'\t' in (ROOT/row['source']).read_text(),
              'primary function export '+row['key'])
    for p in (ROOT/'research/p1-power').glob('*.py'):
        ast.parse(p.read_text(encoding='utf8')); add(p)
        checks.append('AST '+p.name)
    if args.pins:
        stream = io.StringIO(newline=''); w = csv.writer(stream, lineterminator='\n')
        w.writerow(['path','bytes','sha256','eligibility'])
        for r in sorted(pins.values(), key=lambda r:r['path']):
            p = Path(r['path'])
            label = p.relative_to(ROOT).as_posix() if p.is_relative_to(ROOT) else str(p)
            w.writerow([label,r['bytes'],r['sha256'],'LOCAL-ONLY original; metadata REVIEW-REQUIRED'])
        (ROOT/'docs/experiments/power/followup-sources.csv').write_text(stream.getvalue(), encoding='utf8', newline='\n')
    # Entire modified documentation inventory, not only power/ or a new-row slice.
    names = sorted(set(git('diff','HEAD','--name-only','-z').decode().split('\0')[:-1]
        + git('ls-files','--others','--exclude-standard','-z').decode().split('\0')[:-1]))
    documentation = []
    for name in names:
        p = ROOT/name
        if p.suffix not in ('.md','.csv'):
            continue
        data = p.read_bytes(); t = data.decode('utf8')
        documentation.append(name)
        check(not data.startswith(b'\xef\xbb\xbf') and '\ufffd' not in t, 'encoding '+name)
        # Supplied briefs are preserved byte-for-byte, not normalized authored text.
        supplied = 'docs/implementation-briefs/' in name
        if not supplied:
            check(b'\r' not in data, 'LF '+name)
            check(all(line.rstrip() == line for line in t.splitlines()), 'whitespace '+name)
        # Audit new/changed lines against HEAD for legacy docs, whole new documents.
        try:
            oldtext = git('show','HEAD:'+name).decode('utf8')
        except subprocess.CalledProcessError:
            oldtext = ''
        corrupt = [line for line in t.splitlines()
                   if re.search('[\u00c3\u00c2]|\u00e2[\u0080-\u2122]', line)]
        check(all(line in oldtext.splitlines() for line in corrupt), 'no new mojibake '+name)
        if corrupt:
            notes.append(dict(preexisting_encoding_lines=name, count=len(corrupt),
                              disposition='Byte-identical historical HEAD lines retained; no new corruption'))
        added_lines = [line for line in t.splitlines() if line not in oldtext.splitlines()]
        prose = '\n'.join(added_lines)
        bad = re.findall(r'\b(?:retail|version|stride|word|operation|mask|offset)(?=[0-9])|\bat(?=(?:0x)?[0-9a-f]{9}\b)|ExtraFlags(?=[0-9])', prose, re.I)
        bad += re.findall(r'\b(?:STATIC|SAVE|RUNTIME|UNKNOWN|PASS|FAIL)(?=[0-9])', prose)
        check(not bad, 'notation/prose '+name)
        if p.suffix == '.md':
            check(t.count('```')%2 == 0, 'fences '+name)
            for link in re.findall(r'\[[^\]]*\]\(([^)]+)\)', t):
                file = link.split('#')[0].strip('<>')
                if file and not re.match(r'[A-Za-z]+:',file):
                    check((p.parent/file).resolve().exists(), 'link '+name+' '+link)
    subprocess.run(['git','diff','--check'],cwd=ROOT,check=True,capture_output=True)
    checks.append('git diff --check')
    verify(baseline['index']); guard()
    out.write_text(json.dumps(dict(checks=checks, pins=list(pins.values()),
        documentation_audited=documentation, database_files=len(db),
        native_new_rows=len(additions), notes=notes,
        limits=['Integrity/fixture checks do not prove native semantics or live equivalence',
                'Manual prose reading supplements patterns; original briefs preserved']),indent=2)+'\n',encoding='utf8',newline='\n')
    print('PASS',len(checks),'checks;',len(documentation),'documents;',len(pins),'pins')


if __name__ == '__main__':
    main()
