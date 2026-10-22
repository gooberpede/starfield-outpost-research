# SPDX-License-Identifier: GPL-3.0-or-later
"""Offline MSVC build. Reads owned sources/installed SDK; writes fresh local build.

No download/install, target execution, game/config/save access or Git mutation.
The generated command file calls only installed vcvars64 and cl/link.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
SRC = Path(__file__).resolve().parent
LOCAL = ROOT / '.local-work/resource-oracle-collector'
VC = Path('C:/Program Files/Microsoft Visual Studio/18/Community/VC/Auxiliary/Build/vcvars64.bat')


def pin(path):
    with Path(path).open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--name', required=True)
    name = ap.parse_args().name
    assert name and all(c in 'abcdefghijklmnopqrstuvwxyz0123456789-' for c in name)
    assert min(shutil.disk_usage(d).free for d in ('C:/', 'D:/')) >= 40_000_000_000
    out = LOCAL / name
    out.mkdir(parents=True, exist_ok=False)
    commands = [f'call "{VC}"', 'if errorlevel 1 exit /b 1']
    for unit, exe in [('target', 'sor-c1c-target'), ('controller', 'sor-c1c-controller')]:
        commands += [f'cl /Bv /nologo /std:c++20 /EHsc /W4 /Od /MT "{SRC / (unit+".cpp")}" /Fe:{exe}.exe /link /INCREMENTAL:NO',
                     'if errorlevel 1 exit /b 1']
    commands += ['exit /b 0']
    script = out / 'build.cmd'
    script.write_text('@echo off\n'+'\n'.join(commands)+'\n', encoding='utf8', newline='\r\n')
    p = subprocess.run(['cmd', '/d', '/c', str(script)], cwd=out, capture_output=True)
    (out / 'build.log').write_bytes(p.stdout+p.stderr)
    tools = list((VC.parents[2]/'Tools/MSVC').glob('*/bin/Hostx64/x64/cl.exe'))
    tools += list((VC.parents[2]/'Tools/MSVC').glob('*/bin/Hostx64/x64/link.exe'))
    sdk = Path('C:/Program Files (x86)/Windows Kits/10/Include')
    for header in ('windows.h','winnt.h','debugapi.h','processthreadsapi.h'):
        tools += list(sdk.glob('*/um/'+header))
    manifest = dict(exit_code=p.returncode, python=sys.version, command=['cmd', '/d', '/c', str(script)],
                    files={str(f): pin(f) for f in [VC, *SRC.glob('*.cpp'), SRC/'fixture.h', Path(__file__),
                                                   *tools, *out.glob('*')] if f.is_file()})
    (out / 'build.json').write_text(json.dumps(manifest, indent=2)+'\n', encoding='utf8', newline='\n')
    print(out, p.returncode)
    print((p.stdout+p.stderr).decode(errors='replace')[-4000:])
    return p.returncode


if __name__ == '__main__':
    raise SystemExit(main())
