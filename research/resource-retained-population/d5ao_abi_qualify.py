# SPDX-License-Identifier: GPL-3.0-or-later
"""Link an independent hostile caller to the exact D5AM candidate bridge object.

Reads one retained candidate object and authored drivers. Writes a fresh D5AM
receipt/build tree and executes only its own disposable ABI/unwind host. No
game, saves, deployment, external process, network or analysis database access.
"""
import os
import sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE','0') not in ('','0'):
    raise RuntimeError('Python optimization is forbidden; invoke with -E -B')
from pathlib import Path
import json
import subprocess
from d5am_lock_qualify import guard,sha,VC,ROOT

def main():
    build=Path(sys.argv[1]).resolve();out=Path(sys.argv[2]).resolve()
    if not out.is_relative_to(ROOT/'.local-work/d5ao'):
        raise ValueError('Fresh task-local output required')
    initial=guard();out.mkdir(exist_ok=False)
    source=Path(__file__).parent
    inputs=[build/'d5am-causality.obj',source/'d5an-abi-driver.cpp',source/'d5am-abi-driver.asm',Path(__file__),VC,build/'candidate/runtime/construction-winner/d5an_counter.h']
    pins={str(p):sha(p) for p in inputs}
    for p in inputs[:3]:
        (out/p.name).write_bytes(p.read_bytes())
    commands=[f'call "{VC}"','ml64 /nologo /c /Focaller.obj d5am-abi-driver.asm',
              f'cl /nologo /I"{build/"candidate/runtime/construction-winner"}" /std:c++20 /EHsc /W4 /O2 /MD d5an-abi-driver.cpp caller.obj d5am-causality.obj /Fe:d5am-abi.exe /link /Brepro /INCREMENTAL:NO']
    cmd=out/'build.cmd';cmd.write_text('@echo off\n'+'\nif errorlevel 1 exit /b 1\n'.join(commands)+'\n',encoding='utf8',newline='\r\n')
    compiled=subprocess.run(['cmd','/d','/c',str(cmd)],cwd=out,capture_output=True)
    (out/'build.log').write_bytes(compiled.stdout+compiled.stderr)
    receipt=dict(schema='sor-d5an-exact-object-abi/1',inputs=pins,compilation=compiled.returncode,initial_free=initial)
    if not compiled.returncode:
        run=subprocess.run([str(out/'d5am-abi.exe')],cwd=out,capture_output=True)
        (out/'run.stdout').write_bytes(run.stdout);(out/'run.stderr').write_bytes(run.stderr)
        receipt['exit']=run.returncode
        if not run.returncode:
            receipt['oracle']=json.loads(run.stdout)
        receipt['executable_sha256']=sha(out/'d5am-abi.exe')
    receipt['source_unchanged']=all(sha(p)==h for p,h in pins.items());receipt['final_free']=guard()
    receipt['status']='PASS' if not receipt['compilation'] and receipt.get('exit')==0 and receipt['source_unchanged'] else 'FAIL'
    (out/'qualification.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf8',newline='\n')
    print(json.dumps(receipt))
    if receipt['status']!='PASS':
        raise RuntimeError('Exact-object ABI/unwind qualification failed')

if __name__=='__main__':
    main()
