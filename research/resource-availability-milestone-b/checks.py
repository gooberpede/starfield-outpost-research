# SPDX-License-Identifier: GPL-3.0-or-later
"""Run focused owned stdlib tests; save exclusive local receipt.
Reads test sources; subprocesses are CPython unittest only. No target effects.
Also writes review exporter adapted from owned original; no external code.
"""
import argparse, hashlib, json, subprocess, sys
from pathlib import Path
root=Path(__file__).resolve().parents[2]
original=root/'research/resource-availability/export-review-package.py'
s=original.read_text().replace("base=root/'.local-work/resource-availability'", "base=root/'.local-work/resource-availability-milestone-b'")
s=s.replace("'.local-work/diffs/resource-availability-'+label+'-'+args.run+'.diff'", "'.local-work/diffs/resource-availability-milestone-b-'+args.run+'-'+label+'.diff'")
exporter=Path(__file__).with_name('export-review-package.py')
if not exporter.exists(): exporter.write_text(s,encoding='utf8',newline='\n')
ap=argparse.ArgumentParser();ap.add_argument('--run',required=True);args=ap.parse_args()
if not args.run.replace('-','').isalnum(): raise ValueError('RUN_NAME')
out=[]
for pattern in ('test_resource_availability*.py','test_resource_spatial.py','test_extractor_resources.py','test_workshop_origin.py','test_outpost_record_framing.py'):
    command=[sys.executable,'-B','-m','unittest','discover','-s','save-analysis/scripts','-p',pattern]
    r=subprocess.run(command,cwd=root,capture_output=True,text=True)
    out.append(dict(command=command,returncode=r.returncode,stdout=r.stdout,stderr=r.stderr))
with (root/('.local-work/resource-availability-milestone-b/tests-'+args.run+'.json')).open('x',encoding='utf8') as f:
    json.dump(dict(tests=out,exporter_origin=str(original),origin_sha256=hashlib.sha256(original.read_bytes()).hexdigest()),f,indent=2)
for r in out: print(r['command'][-1],r['returncode'],r['stderr'])
assert all(r['returncode']==0 and 'Ran 0 tests' not in r['stderr'] for r in out)
