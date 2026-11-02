# SPDX-License-Identifier: GPL-3.0-or-later
"""Qualify the typed lifetime entries and exception journal using independent calls.

Reads an exact retained native context fixture object and matching derived
headers. Writes a fresh ignored include tree, sources, build logs, executable
and receipt. Executes only its own host with owned function/relay mutations.
No game, debugger, external process, save, network or database operations.
"""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
from d5ae_baseline import guard

ROOT = Path(__file__).resolve().parents[2]
VC = Path('C:/Program Files/Microsoft Visual Studio/18/Community/VC/Auxiliary/Build/vcvars64.bat')


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    build, output = (Path(p).resolve() for p in sys.argv[1:3])
    if not output.is_relative_to(ROOT / '.local-work/d5ai-recorder'):
        raise ValueError('Fresh task-local output required')
    guard()
    output.mkdir(exist_ok=False)
    candidate = next((build / 'sources').rglob('d5ai_lifetime.h')).parent
    source = Path(__file__).parent / 'd5ai-lifetime-driver.cpp'
    obj = build / 'd5ai-context-fixture.obj'
    pins = {str(p): sha(p) for p in (source, obj, Path(__file__), candidate / 'd5ai_lifetime.h', candidate / 'observer.h')}
    include = output / 'runtime/construction-winner'
    include.mkdir(parents=True)
    for name in ('d5ai_lifetime.h', 'observer.h', 'patch.h'):
        (include / name).write_bytes((candidate / name).read_bytes())
    support = output / 'runtime/exp0002'
    support.mkdir()
    for name in ('win_support.h', 'core.h'):
        (support / name).write_bytes((build / 'sources/runtime/exp0002' / name).read_bytes())
    (output / source.name).write_bytes(source.read_bytes())
    command = ('@echo off\ncall "' + str(VC) + '"\nif errorlevel 1 exit /b 1\n'
               'cl /nologo /std:c++20 /EHsc /W4 /O2 /MD /I"' + str(include) + '" d5ai-lifetime-driver.cpp "' + str(obj) +
               '" /Fe:d5ai-lifetime.exe /link /Brepro /INCREMENTAL:NO bcrypt.lib\n')
    script = output / 'build.cmd'
    script.write_text(command, encoding='utf8', newline='\r\n')
    compiled = subprocess.run(['cmd', '/d', '/c', str(script)], cwd=output, capture_output=True)
    (output / 'compile.log').write_bytes(compiled.stdout + compiled.stderr)
    result = dict(schema='sor-d5ai-lifetime-native/1', inputs=pins, compilation=compiled.returncode, free=guard())
    if compiled.returncode == 0:
        run = subprocess.run([str(output / 'd5ai-lifetime.exe')], cwd=output, capture_output=True)
        (output / 'run.stdout').write_bytes(run.stdout)
        (output / 'run.stderr').write_bytes(run.stderr)
        result['exit'] = run.returncode
        if run.returncode == 0:
            result['oracle'] = json.loads(run.stdout)
        result['executable_sha256'] = sha(output / 'd5ai-lifetime.exe')
    result['sources_unchanged'] = all(sha(p) == digest for p, digest in pins.items())
    result['status'] = 'PASS' if result['compilation'] == 0 and result.get('exit') == 0 and result['sources_unchanged'] else 'FAIL'
    (output / 'qualification.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf8', newline='\n')
    print(json.dumps(result))
    return 0 if result['status'] == 'PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())
