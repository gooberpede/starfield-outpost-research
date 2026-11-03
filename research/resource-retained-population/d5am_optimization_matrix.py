# SPDX-License-Identifier: GPL-3.0-or-later
"""Check every new D5AM Python entrypoint refuses optimization before its CLI.

Reads authored source/AST and invokes only -O, -OO or explicitly inherited
PYTHONOPTIMIZE refusal paths with --help. Writes an exclusive D5AM-local JSON
receipt and diagnostics. Stdlib only; no successful experimental/live command,
native build, process intervention, save, database, network or Git mutation.
Sources are hashed before/after; an entrypoint without an early guard fails.
"""
import os
import sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE','') not in ('','0'):
    raise RuntimeError('Python optimization is forbidden; invoke with -E -B')

import ast
import json
from pathlib import Path
import re
import subprocess
from d5ad_baseline import guard,sha

ROOT=Path(__file__).resolve().parents[2]


def entrypoint(path):
    tree=ast.parse(path.read_text(encoding='utf8'))
    for node in tree.body:
        if isinstance(node,ast.If) and isinstance(node.test,ast.Compare):
            value=node.test
            if isinstance(value.left,ast.Name) and value.left.id=='__name__' and any(isinstance(c,ast.Constant) and c.value=='__main__' for c in value.comparators):
                return True
    return False


def early_guard(path):
    """Only os/sys imports may precede the ordinary optimization refusal."""
    for node in ast.parse(path.read_text(encoding='utf8')).body:
        if isinstance(node,ast.Expr) and isinstance(node.value,ast.Constant) and isinstance(node.value.value,str):
            continue
        if isinstance(node,ast.Import) and all(name.name in ('os','sys') for name in node.names):
            continue
        if isinstance(node,ast.If):
            test=ast.unparse(node.test)
            return '__debug__' in test and 'optimize' in test and 'PYTHONOPTIMIZE' in test and any(isinstance(n,ast.Raise) for n in ast.walk(node))
        return False
    return False


def main():
    if len(sys.argv)!=2 or not re.fullmatch('[a-z0-9-]+',sys.argv[1]):
        raise ValueError('Fresh bounded label required')
    out=ROOT/'.local-work/d5am'/(sys.argv[1]+'.json')
    if any(p.is_symlink() or p.is_junction() for p in (out,*out.parents)) or out.exists():
        raise ValueError('Fresh non-reparse output required')
    free=guard()
    paths=sorted(p for directory in ('research/resource-retained-population','runtime/construction-winner')
                 for p in (ROOT/directory).glob('d5am_*.py') if entrypoint(p))
    pins={str(p.relative_to(ROOT)):sha(p) for p in paths}
    checks=[]
    for path in paths:
        for flags,env in ((['-E','-B','-O'],None),(['-E','-B','-OO'],None),
                           (['-E','-B'],dict(os.environ,PYTHONOPTIMIZE='1'))):
            command=[sys.executable,*flags,str(path),'--help']
            result=subprocess.run(command,capture_output=True,text=True,env=env)
            diagnostic=result.stderr.lower()
            passed=result.returncode!=0 and early_guard(path) and any(marker in diagnostic for marker in ('optimization','without pythonoptimize'))
            checks.append(dict(path=str(path.relative_to(ROOT)),flags=flags,inherited_env=env is not None,
                               exit=result.returncode,passed=passed,stdout=result.stdout,stderr=result.stderr))
    unchanged=all(sha(ROOT/p)==pin for p,pin in pins.items())
    passed=bool(paths) and unchanged and all(c['passed'] for c in checks)
    with out.open('x',encoding='utf8',newline='\n') as stream:
        json.dump(dict(schema='sor-d5am-optimization/1',state='PASS' if passed else 'FAIL',
                       sources=pins,source_unchanged=unchanged,checks=checks,method_sha256=sha(__file__),
                       initial_free=free,final_free=guard(),
                       scope='Early optimization-refusal CLIs only; no native/operational success-path qualification.'),stream,indent=2)
        stream.write('\n')
    print(json.dumps(dict(state='PASS' if passed else 'FAIL',entries=len(paths),checks=len(checks),out=str(out))))
    if not passed:
        raise SystemExit(1)


if __name__=='__main__':
    main()
