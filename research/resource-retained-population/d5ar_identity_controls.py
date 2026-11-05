# SPDX-License-Identifier: GPL-3.0-or-later
"""Build and execute owned source-diagnostic controls, without target access.

Reads D5AR helper/fixture and installed MSVC/SDK; writes fresh ignored build,
logs and hash-bound receipt. No game, native game-instruction execution, save,
database, install, network or Git operation. This validates exact bytes and
failure handling of a checked-reader helper, not a native source lifetime lease.
"""
import os
import sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):
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
    before=guard()
    out.mkdir(parents=True)
    source=ROOT / 'runtime/outpost-geometry-snapshot'
    vc=Path('C:/Program Files/Microsoft Visual Studio/18/Community/VC/Auxiliary/Build/vcvars64.bat')
    script=out / 'compile.cmd'
    script.write_text('@echo off\ncall "'+str(vc)+'" >nul\nif errorlevel 1 exit /b %errorlevel%\n'
        +'cl /nologo /std:c++20 /EHsc /W4 /WX /MT /O2 /Brepro /Fe:"'+str(out / 'identity-fixture.exe')
        +'" "'+str(source / 'identity_fixture.cpp')+'" /link /INCREMENTAL:NO /Brepro\nexit /b %errorlevel%\n',
        encoding='utf8',newline='\r\n')
    result=subprocess.run(['cmd.exe','/d','/c',str(script)],cwd=out,capture_output=True)
    (out / 'compile-stdout.log').write_bytes(result.stdout)
    (out / 'compile-stderr.log').write_bytes(result.stderr)
    if result.returncode:
        raise RuntimeError('Identity fixture compile failed; retain logs')
    execution=subprocess.run([str(out / 'identity-fixture.exe')],capture_output=True)
    (out / 'stdout.log').write_bytes(execution.stdout)
    (out / 'stderr.log').write_bytes(execution.stderr)
    if execution.returncode:
        raise RuntimeError('Identity fixture failed; retain logs')
    value=json.loads(execution.stdout)
    if value!={'status':'PASS','controls':25,'scope':'owned_diagnostic_reader_only'}:
        raise ValueError('Identity fixture result differs')
    value.update(inputs={str(p.relative_to(ROOT)):sha(p) for p in
        (source / 'identity.h',source / 'identity_fixture.cpp',Path(__file__))},
        exe_sha256=sha(out / 'identity-fixture.exe'),interpreter_sha256=sha(sys.executable),
        compiler_setup_sha256=sha(vc),floors_before=before,floors_after=guard())
    with (out / 'qualification.json').open('x',encoding='utf8',newline='\n') as stream:
        stream.write(json.dumps(value,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',controls=25,path=str(out / 'qualification.json'))))


if __name__=='__main__':
    main()
