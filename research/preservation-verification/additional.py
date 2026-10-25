# SPDX-License-Identifier: GPL-3.0-or-later
"""Supplementary disposable adversarial checks; never edits existing evidence.

Uses the qualified fixture builder. All expectations are frozen before execution.
No performance rerun or change to the original W1/W2 denominator. Writes a fresh
local supplement directory and reads current Git changes without index/ref writes.
"""
import hashlib
import json
from pathlib import Path
import shutil
import struct
import subprocess

import journal
import prototype as p
from qualify import make

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / '.local-work/preservation-verification/supplement01'


def write(name,value):
    with (OUT / name).open('x',encoding='utf8',newline='\n') as f:
        json.dump(value,f,indent=2)
        f.write('\n')


def check(root,anchor,mode,expected,inject=None):
    try:
        p.verify(root,anchor,mode=mode,inject=inject)
        result,detail='ALLOW',''
    except (p.IntegrityError,journal.JournalError,OSError,ValueError) as exc:
        result,detail='DETECT',type(exc).__name__+': '+str(exc)
    return dict(mode=mode,expected=expected,observed=result,passed=result==expected,detail=detail)


def main():
    OUT.mkdir(exist_ok=False)
    expectations={'wrong-root':'DETECT','full-interruption':'DETECT',
        'concurrent-journaled-write':'DETECT','concurrent-full-detection':'DETECT',
        'ordinary-git-output':'ALLOW','unavailable-journal':'DETECT','fallback-full':'ALLOW',
        'unsupported-journal-record':'DETECT','baseline-construction-race':'DETECT'}
    write('freeze.json',expectations)
    rows=[]
    for mode in ('full','journal-conditional'):
        original=OUT / ('original-'+mode)
        setup=make(original)
        wrong=OUT / ('wrong-'+mode)
        make(wrong)
        # Copy a disposable manifest only; preserve both original manifests.
        original_bytes=(original / 'baseline.sqlite').read_bytes()
        with (wrong / 'foreign.sqlite').open('xb') as f:
            f.write(original_bytes)
        (wrong / 'baseline.sqlite').rename(wrong / 'own-baseline.sqlite')
        (wrong / 'foreign.sqlite').rename(wrong / 'baseline.sqlite')
        rows.append(dict(case='wrong-root',**check(wrong,setup['anchor'],mode,'DETECT')))
        if mode=='full':
            def interrupt(path):
                raise InterruptedError('Injected full scan interruption')
            rows.append(dict(case='full-interruption',**check(original,setup['anchor'],mode,'DETECT',interrupt)))
        changed=False
        def concurrent(path):
            nonlocal changed
            if not changed and path.parent.name=='scientific':
                leaf=next((original / 'historical').rglob('*.dat'))
                leaf.write_bytes(b'z'*1024)
                changed=True
        case='concurrent-journaled-write' if mode=='journal-conditional' else 'concurrent-full-detection'
        rows.append(dict(case=case,**check(original,setup['anchor'],mode,expectations[case],concurrent)))
    root=OUT / 'recovery'
    setup=make(root)
    baseline_before=hashlib.sha256((root / 'baseline.sqlite').read_bytes()).hexdigest()
    old=journal.read_since
    try:
        def fail(volume,cursor):
            raise journal.JournalError('Injected inaccessible journal')
        journal.read_since=fail
        rows.append(dict(case='unavailable-journal',**check(root,setup['anchor'],'journal-conditional','DETECT')))
    finally:
        journal.read_since=old
    rows.append(dict(case='fallback-full',**check(root,setup['anchor'],'full','ALLOW')))
    assert hashlib.sha256((root / 'baseline.sqlite').read_bytes()).hexdigest()==baseline_before
    # Actual authorized navigation edits should exist by this supplemental check.
    changes=subprocess.check_output(['git','diff','--name-only'],cwd=ROOT,text=True).splitlines()
    if not changes:
        raise RuntimeError('Normal tracked Git change control not established')
    rows.append(dict(case='ordinary-git-output',tracked_changes=changes,
                     **check(root,setup['anchor'],'journal-conditional','ALLOW')))
    try:
        journal.decode(struct.pack('<qIHH',0,64,3,0)+b'\0'*56)
        detected=False
    except journal.JournalError:
        detected=True
    rows.append(dict(case='unsupported-journal-record',expected='DETECT',observed='DETECT' if detected else 'ALLOW',passed=detected))
    racing=OUT / 'baseline-race'
    make(racing)
    (racing / 'baseline.sqlite').rename(racing / 'preserved-first-baseline.sqlite')
    original_sha=p.sha
    triggered=False
    def race_sha(data):
        nonlocal triggered
        value=original_sha(data)
        if not triggered:
            (racing / 'historical/00/00000.dat').write_bytes(b'q'*1024)
            triggered=True
        return value
    try:
        p.sha=race_sha
        try:
            p.baseline(racing)
            detected=False
        except p.IntegrityError:
            detected=True
    finally:
        p.sha=original_sha
    rows.append(dict(case='baseline-construction-race',expected='DETECT',observed='DETECT' if detected else 'ALLOW',passed=detected))
    write('tests.json',rows)
    if not all(row['passed'] for row in rows):
        raise RuntimeError('Supplemental failure; preserve receipts for correction')
    print(json.dumps(dict(tests=len(rows),passed=True,non_destructive_fallback=True)))


if __name__=='__main__':
    main()
