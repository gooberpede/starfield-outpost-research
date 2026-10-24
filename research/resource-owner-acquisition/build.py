# SPDX-License-Identifier: GPL-3.0-or-later
"""Build D4D with installed MSVC/SDK; no execution, downloads or target effects.

Reads owned D4D and inherited D4A headers and installed toolchain. Writes a fresh
ignored build, log and SHA-256 manifest. Python stdlib only.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[2]
SRC = Path(__file__).resolve().parent
LOCAL = ROOT / '.local-work/resource-owner-acquisition'
VC = Path('C:/Program Files/Microsoft Visual Studio/18/Community/VC/Auxiliary/Build/vcvars64.bat')


def pin(p):
    with Path(p).open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--name', required=True)
    a = ap.parse_args()
    assert a.name and all(c in 'abcdefghijklmnopqrstuvwxyz0123456789-' for c in a.name)
    assert min(shutil.disk_usage(d).free for d in ('C:/', 'D:/')) >= 40_000_000_000
    out = LOCAL / a.name
    out.mkdir(parents=True, exist_ok=False)
    commands = [f'call "{VC}"', 'if errorlevel 1 exit /b 1']
    names = ('fixture_updater_entry', 'fixture_callback_return', 'fixture_update_return',
             'fixture_transfer', 'fixture_accept', 'fixture_reject', 'diagnostic_entry',
             'diagnostic_call', 'diagnostic_return', 'map_loop', 'map_cleanup', 'map_return', 'map_wrapper_return', 'candidate_ready')
    exports = ' '.join('/EXPORT:' + n for n in names)
    for asm in ('fixture', 'fixture-consumer'):
        commands += [f'ml64 /nologo /c /Fo{asm}-asm.obj "{SRC / (asm + ".asm")}"', 'if errorlevel 1 exit /b 1']
    commands += [f'cl /nologo /std:c++20 /EHsc /W4 /Od /MT "{SRC / "fixture.cpp"}" "{SRC / "fixture-map.cpp"}" fixture-asm.obj fixture-consumer-asm.obj /Fe:sor-d4d-fixture.exe /link {exports} /INCREMENTAL:NO',
                 'if errorlevel 1 exit /b 1']
    for name, flag in (('fixture-controller', '/DRETAIL_FIXTURE'), ('controller', '')):
        commands += [f'cl /Bv /nologo /std:c++20 /EHsc /W4 /Od /MT {flag} "{SRC / "controller.cpp"}" /Fe:sor-d4d-{name}.exe /link /INCREMENTAL:NO', 'if errorlevel 1 exit /b 1']
    script = out / 'build.cmd'
    script.write_text('@echo off\n' + '\n'.join(commands) + '\n', encoding='utf8', newline='\r\n')
    p = subprocess.run(['cmd', '/d', '/c', str(script)], cwd=out, capture_output=True)
    (out / 'build.log').write_bytes(p.stdout + p.stderr)
    inputs = [VC, *SRC.glob('*'), *(SRC.parent / 'resource-tungsten-acquisition').glob('*.h'),
              SRC.parent / 'resource-tungsten-acquisition/sample.inc']
    files = [f for f in inputs + list(out.glob('*')) if f.is_file()]
    (out / 'build.json').write_text(json.dumps(dict(exit_code=p.returncode,
        files={str(f): pin(f) for f in files}), indent=2) + '\n', encoding='utf8', newline='\n')
    print(out, p.returncode)
    print((p.stdout + p.stderr).decode(errors='replace')[-3000:])
    return p.returncode


if __name__ == '__main__':
    raise SystemExit(main())
