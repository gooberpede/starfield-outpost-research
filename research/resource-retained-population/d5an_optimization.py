# SPDX-License-Identifier: GPL-3.0-or-later
"""Exercise early optimization refusal for every authored D5AN Python module.

Invokes only refusal paths with -O, -OO or inherited PYTHONOPTIMIZE=1 and --help.
Reads source/AST; writes one fresh local JSON receipt. No success-path fixture,
game, deployment, save, database, dependency, network or Git operations occur.
The existing owned D5AM early-guard AST check is reused under SOR-P-0002.
"""
import os
import sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE','0') not in ('','0'):
    raise RuntimeError('Python optimization is forbidden; invoke with -E -B')
import argparse
import json
from pathlib import Path
import subprocess
from concurrent.futures import ThreadPoolExecutor
from d5am_optimization_matrix import early_guard
from d5am_lock_qualify import ROOT,guard,sha

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('out',type=Path)
    args=parser.parse_args();out=args.out.resolve()
    if not out.is_relative_to(ROOT/'.local-work/d5an') or out.exists():raise ValueError('Fresh task-local receipt required')
    free=guard();paths=sorted(p for folder in ('runtime/construction-winner','research/resource-retained-population') for p in (ROOT/folder).glob('d5an_*.py'))
    pins={str(p):sha(p) for p in paths}
    def run(item):
        path,mode=item;env=dict(os.environ);command=[sys.executable,'-E','-B']
        if mode=='ENV':env['PYTHONOPTIMIZE']='1'
        else:command.append(mode)
        command.extend([str(path),'--help']);value=subprocess.run(command,capture_output=True,env=env)
        diagnostic=value.stderr.lower()
        return dict(path=str(path),mode=mode,exit=value.returncode,passed=value.returncode!=0 and early_guard(path) and any(marker in diagnostic for marker in (b'optimization',b'without pythonoptimize')),stderr=value.stderr.decode('utf8',errors='replace'))
    with ThreadPoolExecutor(max_workers=4) as pool:checks=list(pool.map(run,[(p,m) for p in paths for m in ('-O','-OO','ENV')]))
    unchanged=all(sha(p)==h for p,h in pins.items());passed=unchanged and bool(paths) and all(c['passed'] for c in checks)
    result=dict(schema='sor-d5an-optimization/1',result='PASS' if passed else 'FAIL',sources=pins,source_unchanged=unchanged,checks=checks,initial_free=free,final_free=guard())
    with out.open('x',encoding='utf8',newline='\n') as stream:json.dump(result,stream,indent=2);stream.write('\n')
    print(json.dumps(dict(result=result['result'],modules=len(paths),checks=len(checks))))
    if not passed:raise RuntimeError('Optimization refusal failure')

if __name__=='__main__':main()
