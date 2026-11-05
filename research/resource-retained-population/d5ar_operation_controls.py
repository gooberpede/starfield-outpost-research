# SPDX-License-Identifier: GPL-3.0-or-later
"""Build/run owned operation-request diagnostic controls, stdlib only.

Reads D5AR fixed-buffer helper/fixture and installed MSVC/SDK; writes fresh ignored
build/logs and source-bound receipt. Runs only its own fixture, never engine
instructions, game, saves, database, install, network or Git operations. The
observed operation relation is not a current-outpost or native area certificate.
"""
import os
import sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE','') not in ('','0'):
    raise RuntimeError('Use pinned Python -E -B without optimization')

import json
from pathlib import Path
import subprocess
from d5ad_baseline import ROOT, guard, sha


def main():
    out=Path(sys.argv[1]).resolve()
    if not out.is_relative_to(ROOT / '.local-work/d5ar') or out.exists():
        raise ValueError('Fresh ignored D5AR output required')
    if any(p.is_symlink() or p.is_junction() for p in (out,*out.parents)):
        raise ValueError('No reparse outputs')
    before=guard();out.mkdir(parents=True)
    source=ROOT / 'runtime/outpost-geometry-snapshot'
    sources=(source / 'identity.h',source / 'operation.h',source / 'operation_fixture.cpp',Path(__file__))
    source_pins={str(p.relative_to(ROOT)):sha(p) for p in sources}
    vc=Path('C:/Program Files/Microsoft Visual Studio/18/Community/VC/Auxiliary/Build/vcvars64.bat')
    script=out / 'compile.cmd'
    script.write_text('@echo off\ncall "'+str(vc)+'" >nul\nif errorlevel 1 exit /b %errorlevel%\n'
        +'cl /nologo /std:c++20 /EHsc /W4 /WX /MT /O2 /Brepro /Fe:"'+str(out / 'operation-fixture.exe')
        +'" "'+str(source / 'operation_fixture.cpp')+'" /link /INCREMENTAL:NO /Brepro\nexit /b %errorlevel%\n',
        encoding='utf8',newline='\r\n')
    result=subprocess.run(['cmd.exe','/d','/c',str(script)],cwd=out,capture_output=True)
    (out / 'compile-stdout.log').write_bytes(result.stdout);(out / 'compile-stderr.log').write_bytes(result.stderr)
    if result.returncode:raise RuntimeError('Operation fixture compile failed; retain logs')
    execution=subprocess.run([str(out / 'operation-fixture.exe')],capture_output=True)
    (out / 'stdout.log').write_bytes(execution.stdout);(out / 'stderr.log').write_bytes(execution.stderr)
    if execution.returncode:raise RuntimeError('Operation fixture failed; retain logs')
    value=json.loads(execution.stdout)
    if value!={'status':'PASS','controls':20,'scope':'owned_operation_diagnostics_only'}:
        raise ValueError('Operation fixture result differs')
    if {str(p.relative_to(ROOT)):sha(p) for p in sources}!=source_pins:
        raise ValueError('Executed operation source changed')
    value.update(inputs=source_pins,
        exe_sha256=sha(out / 'operation-fixture.exe'),interpreter_sha256=sha(sys.executable),
        compiler_setup_sha256=sha(vc),floors_before=before,floors_after=guard())
    with (out / 'qualification.json').open('x',encoding='utf8',newline='\n') as stream:stream.write(json.dumps(value,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',controls=20,path=str(out / 'qualification.json'))))


if __name__=='__main__':main()
