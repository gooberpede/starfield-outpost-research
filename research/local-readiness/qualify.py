# SPDX-License-Identifier: GPL-3.0-or-later
"""Offline original qualification coordinator. Reads existing pinned exports,
owned source/fixture receipts and Git metadata; executes owned disposable tests.
Writes exclusive ignored receipts only. No target/process/deployment/control,
save/configuration/analysis DB/Git changes or network. CPython stdlib only.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'runtime/session-tools'))
from common import guard, fresh, sha


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out',type=Path,required=True)
    a=ap.parse_args();guard();a.out.mkdir(parents=True,exist_ok=False)
    initial=dict(head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip(),index=sha(ROOT/'.git/index'))
    pins={}
    for name in ('sources.csv','region-sources.csv'):
        p=ROOT/'docs/experiments/native-availability-map'/name
        for r in csv.DictReader(p.open(encoding='utf8')):
            source=ROOT/r['path'];assert sha(source)==r['sha256'],source
            pins[r['path']]=r['sha256']
    suites=[('availability',['-m','unittest','discover','-s','save-analysis/scripts','-p','test_resource_availability*.py','-v']),
            ('spatial',['-m','unittest','discover','-s','save-analysis/scripts','-p','test_resource_spatial.py','-v']),
            ('session',['-m','unittest','discover','-s','runtime/session-tools','-p','test_*.py','-v'])]
    results={}
    for label,args in suites:
        r=subprocess.run([sys.executable,'-B',*args],cwd=ROOT,capture_output=True)
        (a.out/(label+'.txt')).write_bytes(r.stdout+r.stderr)
        results[label]=dict(exit_code=r.returncode,log_sha256=sha(a.out/(label+'.txt')))
        assert r.returncode==0,label
    assert sha(ROOT/'.git/index')==initial['index']
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip()==initial['head']
    fresh(a.out/'qualification.json',dict(status='PASS',scope='OFFLINE_ONLY_NO_NATIVE_EQUIVALENCE',identity=initial,sources=pins,suites=results,disk=guard(),script_sha256=sha(__file__)))
    print(json.dumps(dict(status='PASS',source_pins=len(pins),suites=results)))


if __name__=='__main__':main()
