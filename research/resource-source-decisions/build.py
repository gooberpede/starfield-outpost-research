# SPDX-License-Identifier: GPL-3.0-or-later
"""Build disposable D5E probes from the owned D5B debugger utilities.

Reads repository sources and installed MSVC. Writes a new ignored build directory,
generated controller translation unit, build commands, log and hashes. Executes
only MSVC/SDK build tools, no fixture or retail process, download or Git writes.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import re

ROOT = Path(__file__).resolve().parents[2]
SRC = Path(__file__).resolve().parent
LOCAL = ROOT / '.local-work/resource-source-decisions'
VC = Path('C:/Program Files/Microsoft Visual Studio/18/Community/VC/Auxiliary/Build/vcvars64.bat')


def pin(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--name', required=True)
    args = parser.parse_args()
    assert args.name and all(c in 'abcdefghijklmnopqrstuvwxyz0123456789-' for c in args.name)
    assert min(shutil.disk_usage(d).free for d in ('C:/', 'D:/')) >= 40_000_000_000
    out = LOCAL / args.name
    out.mkdir(parents=True, exist_ok=False)
    inherited = ROOT / 'research/resource-combined-acquisition/controller.cpp'
    prefix = inherited.read_text(encoding='utf8').split('struct Thread {')[0]
    generated = out / 'controller.cpp'
    generated.write_text(prefix + (SRC / 'controller-tail.inc').read_text(), encoding='utf8', newline='\n')
    flags = '/Bv /nologo /std:c++20 /EHsc /W4 /Od /MT'
    exports = ' '.join('/EXPORT:decision_' + n for n in ('visited', 'lookup', 'mask', 'terminal'))
    commands = [f'call "{VC}"', 'if errorlevel 1 exit /b 1', 'where cl', 'where link',
        f'cl {flags} "{SRC / "fixture.cpp"}" /Fe:sor-d5e-fixture.exe /link {exports} /INCREMENTAL:NO',
        'if errorlevel 1 exit /b 1',
        f'cl {flags} /DRETAIL_FIXTURE /I"{inherited.parent}" "{generated}" /Fe:sor-d5e-controller.exe /link /INCREMENTAL:NO',
        'if errorlevel 1 exit /b 1',
        f'cl {flags} /I"{inherited.parent}" /I"{SRC}" "{generated}" /Fe:sor-d5e-native-controller.exe /link /INCREMENTAL:NO',
        'if errorlevel 1 exit /b 1']
    script = out / 'build.cmd'
    script.write_text('@echo off\n' + '\n'.join(commands) + '\n', encoding='utf8', newline='\r\n')
    proc = subprocess.run(['cmd', '/d', '/c', str(script)], cwd=out, capture_output=True)
    (out / 'build.log').write_bytes(proc.stdout + proc.stderr)
    inputs = [VC, inherited, *SRC.glob('*')]
    for directory in ('resource-tungsten-acquisition', 'resource-oracle-retail', 'resource-ui-oracle', 'resource-combined-acquisition'):
        inputs += [p for p in (ROOT / 'research' / directory).glob('*') if p.is_file()]
    files = [*inputs, *[p for p in out.glob('*') if p.is_file()]]
    # Bind every quoted transitive include; the generated translation unit uses
    # the D5B and current source include roots explicitly passed to MSVC.
    pending = [generated, SRC / 'fixture.cpp']
    seen = set()
    while pending:
        path = pending.pop().resolve()
        if path in seen:
            continue
        seen.add(path)
        for include in re.findall(r'#include\s+"([^"]+)"', path.read_text(encoding='utf8')):
            candidates = [path.parent / include, inherited.parent / include, SRC / include]
            dependency = next((p.resolve() for p in candidates if p.is_file()), None)
            assert dependency is not None, (path, include)
            pending.append(dependency)
    files += list(seen)
    for line in (proc.stdout + proc.stderr).decode(errors='replace').splitlines():
        candidate = Path(line.strip())
        if candidate.name.lower() in ('cl.exe', 'link.exe') and candidate.is_file():
            files.append(candidate)
    (out / 'build.json').write_text(json.dumps(dict(exit_code=proc.returncode,
        files={str(p): pin(p) for p in files}), indent=2) + '\n', encoding='utf8', newline='\n')
    print(out, proc.returncode)
    print((proc.stdout + proc.stderr).decode(errors='replace')[-3000:])
    return proc.returncode


if __name__ == '__main__':
    raise SystemExit(main())
