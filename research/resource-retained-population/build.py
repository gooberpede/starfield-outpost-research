# SPDX-License-Identifier: GPL-3.0-or-later
"""Build only the disposable D5L experiment using installed MSVC.

Reads owned D5B utilities/includes and local sources. Writes a fresh ignored
build, commands, logs and source/tool pins. No target execution, installation,
download, protected input or Git mutation. Uses existing MSVC/Windows SDK.
"""
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
SRC = Path(__file__).resolve().parent
LOCAL = ROOT/'.local-work/resource-retained-population'
VC = Path('C:/Program Files/Microsoft Visual Studio/18/Community/VC/Auxiliary/Build/vcvars64.bat')


def pin(p):
    with Path(p).open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def main():
    label = sys.argv[1]
    if not re.fullmatch('[a-z0-9-]+', label):
        raise ValueError('Fresh task label required')
    if min(shutil.disk_usage(d).free for d in ('C:/', 'D:/')) < 40000000000:
        raise ValueError('Disk floor')
    out = LOCAL/label
    out.mkdir(exist_ok=False)
    inherited = ROOT/'research/resource-combined-acquisition/controller.cpp'
    generated = out/'controller.cpp'
    generated.write_text(inherited.read_text().split('struct Thread {')[0] +
                         (SRC/'controller-tail.inc').read_text(), encoding='utf8', newline='\n')
    names = ('owner_init source_init provider_entry visited lookup inserted query mask completed '
             'owner_reset owner_destroy provider_exit').split()
    exports = ' '.join('/EXPORT:'+n for n in names)
    flags = '/Bv /nologo /std:c++20 /EHsc /W4 /Od /MT'
    commands = [f'call "{VC}"', 'if errorlevel 1 exit /b 1', 'where cl', 'where link',
                f'cl {flags} "{SRC/"fixture.cpp"}" /Fe:sor-d5l-fixture.exe /link {exports} /INCREMENTAL:NO',
                'if errorlevel 1 exit /b 1',
                f'cl {flags} /DRETAIL_FIXTURE /I"{inherited.parent}" "{generated}" /Fe:sor-d5l-controller.exe /link /INCREMENTAL:NO',
                'if errorlevel 1 exit /b 1']
    script = out/'build.cmd'
    script.write_text('@echo off\n'+'\n'.join(commands)+'\n', encoding='utf8', newline='\r\n')
    x = subprocess.run(['cmd', '/d', '/c', str(script)], cwd=out, capture_output=True)
    (out/'build.log').write_bytes(x.stdout+x.stderr)
    files = {VC, inherited, *[p for p in SRC.glob('*') if p.is_file()]}
    pending = [generated, SRC/'fixture.cpp']
    seen = set()
    while pending:
        p = pending.pop().resolve()
        if p in seen:
            continue
        seen.add(p)
        for name in re.findall(r'#include\s+"([^"]+)"', p.read_text()):
            found = next((q.resolve() for q in (p.parent/name, inherited.parent/name) if q.is_file()), None)
            if found is None:
                raise ValueError('Missing include: '+name)
            pending.append(found)
    files |= seen | {p for p in out.glob('*') if p.is_file()}
    for line in (x.stdout+x.stderr).decode(errors='replace').splitlines():
        p = Path(line.strip())
        if p.name.lower() in ('cl.exe', 'link.exe') and p.is_file():
            files.add(p)
    (out/'build.json').write_text(json.dumps(dict(exit_code=x.returncode,
        files={str(p):pin(p) for p in sorted(files)}), indent=2)+'\n', encoding='utf8', newline='\n')
    print(x.returncode, (x.stdout+x.stderr).decode(errors='replace')[-2000:])
    return x.returncode


if __name__ == '__main__':
    raise SystemExit(main())
