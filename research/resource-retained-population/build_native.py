# SPDX-License-Identifier: GPL-3.0-or-later
"""Build native-shaped disposable qualification with the actual native reader.

Reads owned debugger/adapter sources and installed MSVC/SDK/MASM; writes a fresh
task-local build, commands, logs and input/tool pins. Executes build tools only.
No downloads, retail process, save, analysis or Git mutations.
"""
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
from build import ROOT, SRC, LOCAL, VC, pin, controller_source


def main():
    label = sys.argv[1]
    assert re.fullmatch('[a-z0-9-]+', label)
    assert min(shutil.disk_usage(d).free for d in ('C:/', 'D:/')) >= 40000000000
    out = LOCAL/label
    out.mkdir(exist_ok=False)
    inherited = ROOT/'research/resource-combined-acquisition/controller.cpp'
    generated = out/'controller.cpp'
    generated.write_text(controller_source(inherited), encoding='utf8', newline='\n')
    names = ['native_'+n for n in 'visited lookup query mask append complete init reset destroy erase grid_clear source_init grid_init source_retire'.split()]
    exports = names+['after_'+n for n in names]+['native_inner_return','native_outer_return','native_outer_return2']
    flags = '/Bv /nologo /std:c++20 /EHsc /W4 /Od /MT'
    commands = [f'call "{VC}"', 'if errorlevel 1 exit /b 1','where cl','where link','where ml64',
        f'ml64 /nologo /c /Fonative-asm.obj "{SRC/"native-fixture.asm"}"','if errorlevel 1 exit /b 1',
        f'cl {flags} "{SRC/"native-fixture.cpp"}" native-asm.obj /Fe:sor-d5l-native-fixture.exe /link '+
        ' '.join('/EXPORT:'+n for n in exports)+' /INCREMENTAL:NO','if errorlevel 1 exit /b 1',
        f'cl {flags} /DNATIVE_ABI /DRETAIL_FIXTURE /I"{inherited.parent}" /I"{SRC}" "{generated}" /Fe:sor-d5l-native-fixture-controller.exe /link /INCREMENTAL:NO',
        'if errorlevel 1 exit /b 1',
        f'cl {flags} /DNATIVE_ABI /DRETAIL_FIXTURE /DD5L_RETAIL_TARGET /I"{inherited.parent}" /I"{SRC}" "{generated}" /Fe:sor-d5l-native-controller.exe /link /INCREMENTAL:NO',
        'if errorlevel 1 exit /b 1']
    script = out/'build.cmd'
    script.write_text('@echo off\n'+'\n'.join(commands)+'\n',encoding='utf8',newline='\r\n')
    x = subprocess.run(['cmd','/d','/c',str(script)],cwd=out,capture_output=True)
    (out/'build.log').write_bytes(x.stdout+x.stderr)
    files = {VC,inherited,*[p for p in SRC.glob('*') if p.suffix in ('.cpp','.h','.inc','.asm','.py','.java')]}
    pending = [generated, SRC/'native-fixture.cpp']
    seen = set()
    while pending:
        p = pending.pop().resolve()
        if p in seen:
            continue
        seen.add(p)
        for n in re.findall(r'#include\s+"([^"]+)"',p.read_text()):
            found = next((q.resolve() for q in (p.parent/n,inherited.parent/n,SRC/n) if q.is_file()), None)
            assert found, (p,n)
            pending.append(found)
    files |= seen | {p for p in out.glob('*') if p.is_file()}
    snapshots = {}
    for p in sorted(files):
        if p.is_relative_to(ROOT) and p.suffix in ('.cpp','.h','.inc','.asm','.py','.java'):
            snapshot=out/'source-snapshot'/p.relative_to(ROOT);snapshot.parent.mkdir(parents=True,exist_ok=True);snapshot.write_bytes(p.read_bytes())
            snapshots[str(p)]=dict(path=str(snapshot),sha256=pin(snapshot))
    for line in (x.stdout+x.stderr).decode(errors='replace').splitlines():
        p = Path(line.strip())
        if p.name.lower() in ('cl.exe','link.exe','ml64.exe') and p.is_file():
            files.add(p)
    (out/'build.json').write_text(json.dumps(dict(exit_code=x.returncode,files={str(p):pin(p) for p in sorted(files)},source_snapshots=snapshots),indent=2)+'\n',encoding='utf8',newline='\n')
    print(x.returncode,(x.stdout+x.stderr).decode(errors='replace')[-4000:])
    return x.returncode


if __name__ == '__main__':
    raise SystemExit(main())
