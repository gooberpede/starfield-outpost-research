# SPDX-License-Identifier: GPL-3.0-or-later
"""Run only offline decoders and frozen tests; write local regression receipt.

Reads named existing synthetic runs and unchanged owned modules. Writes decoder
JSON beside those inputs and regression.json under the ignored task root. No
native execution, game access, dependencies, Git mutation or input-byte writes.
"""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'.local-work/x87-preservation'
commands=[]
for run,expected in [('diagnostic-04','loss'),('corrected-02','preserved')]:
    for condition in ('minimal','adversarial'):
        commands.append(['research/x87-preservation/verify.py',
                         f'.local-work/x87-preservation/{run}/{condition}/states.bin','--expect',expected])
    commands.append(['research/internal-observation-qualification/verify.py',
                     f'.local-work/x87-preservation/{run}/adversarial/geometry.bin'])
commands.append(['-m','unittest','discover','-s','save-analysis/scripts','-p','test_resource_spatial.py'])
rows=[]
for command in commands:
    proc=subprocess.run([sys.executable,'-B',*command],cwd=ROOT,capture_output=True)
    rows.append(dict(command=command,exit_code=proc.returncode,
                     stdout=proc.stdout.decode(errors='replace'),stderr=proc.stderr.decode(errors='replace')))
receipt=dict(checks=rows,all_exit_zero=all(r['exit_code']==0 for r in rows),
             script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
(OUT/'regression.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf8',newline='\n')
print(json.dumps(dict(commands=len(rows),all_exit_zero=receipt['all_exit_zero'])))
assert receipt['all_exit_zero']
