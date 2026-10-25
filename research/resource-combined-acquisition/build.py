# SPDX-License-Identifier: GPL-3.0-or-later
"""Build only: combined D5B controller and fixtures with installed MSVC/SDK.

Reads sources/toolchain; writes a fresh ignored build. No target execution,
download, configuration, saves, database or Git mutation. Adapted from owned
C1G build.py at e684cd4; this command does not execute targets or tests.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[2]
SRC = Path(__file__).resolve().parent
LOCAL = ROOT / '.local-work/resource-combined-acquisition'
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
    exports = ' '.join('/EXPORT:' + n for n in ('fixture_entry', 'fixture_resource_call', 'fixture_resource_return', 'fixture_cell_return', 'fixture_chance', 'fixture_biom', 'fixture_query', 'fixture_component', 'fixture_mask_call', 'fixture_mask_return', 'fixture_candidate', 'fixture_resolved', 'fixture_terminal', 'fixture_provider'))
    exports += ' ' + ' '.join('/EXPORT:con_fixture_' + n for n in ('updater_entry','accept','reject','transfer','update_return','callback_return'))
    for name in ('producer','consumer'):
        commands += [f'ml64 /nologo /c /Fo{name}-asm.obj "{SRC / (name + ".asm")}"', 'if errorlevel 1 exit /b 1']
    commands += [f'cl /Bv /nologo /std:c++20 /EHsc /W4 /Od /MT "{SRC / "producer.cpp"}" "{SRC / "consumer.cpp"}" producer-asm.obj consumer-asm.obj /Fe:sor-d5b-fixture.exe /link {exports} /INCREMENTAL:NO', 'if errorlevel 1 exit /b 1',
                 f'cl /nologo /std:c++20 /EHsc /W4 /Od /MT /DRETAIL_FIXTURE "{SRC / "controller.cpp"}" /Fe:sor-d5b-fixture-controller.exe /link /INCREMENTAL:NO','if errorlevel 1 exit /b 1']
    commands += [f'cl /nologo /std:c++20 /EHsc /W4 /Od /MT "{SRC / "controller.cpp"}" /Fe:sor-d5b-controller.exe /link /INCREMENTAL:NO', 'if errorlevel 1 exit /b 1']
    script = out / 'build.cmd'
    script.write_text('@echo off\n' + '\n'.join(commands) + '\n', encoding='utf8', newline='\r\n')
    p = subprocess.run(['cmd', '/d', '/c', str(script)], cwd=out, capture_output=True)
    (out / 'build.log').write_bytes(p.stdout + p.stderr)
    files = [VC, *SRC.glob('*'), *out.glob('*')]
    for family in ('resource-selection-context','resource-tungsten-acquisition','resource-oracle-retail','resource-feynman-d5','resource-ui-oracle'):
        files += [p for p in (ROOT / 'research' / family).glob('*') if p.is_file()]
    (out / 'build.json').write_text(json.dumps(dict(exit_code=p.returncode, files={str(f): pin(f) for f in files if f.is_file()}), indent=2) + '\n', encoding='utf8', newline='\n')
    print(out, p.returncode)
    print((p.stdout + p.stderr).decode(errors='replace')[-4000:])
    return p.returncode


if __name__ == '__main__':
    raise SystemExit(main())
