# SPDX-License-Identifier: GPL-3.0-or-later
"""Link an independent ABI and unwind caller against an exact retained bridge object.

Reads the selected offline build's `d5ai-bridge.obj` and owned separate driver,
installed compiler/MASM/SDK. Writes only a fresh ignored directory with source
copies, command/compiler logs, disposable executable and receipt. Runs only that
owned executable, which patches its own linked test call site. No game, saves,
debugger, remote process, deployment, network or analysis-project operation.
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
    if not __debug__ or sys.flags.optimize:
        raise RuntimeError('Use installed Python -E -B')
    build, output = (Path(p).resolve() for p in sys.argv[1:3])
    if not output.is_relative_to(ROOT / '.local-work/d5ai-recorder'):
        raise ValueError('Fresh task-local output required')
    guard()
    output.mkdir(exist_ok=False)
    source = Path(__file__).parent
    inputs = [build / 'd5ai-bridge.obj', source / 'd5ai-abi-driver.cpp', source / 'd5ai-abi-driver.asm', Path(__file__), VC]
    pins = {str(p): sha(p) for p in inputs}
    for p in inputs[:3]:
        (output / p.name).write_bytes(p.read_bytes())
    command = ('@echo off\ncall "' + str(VC) + '"\nif errorlevel 1 exit /b 1\n'
               'ml64 /nologo /c /Foindependent-caller.obj d5ai-abi-driver.asm\nif errorlevel 1 exit /b 1\n'
               'cl /nologo /std:c++20 /EHsc /W4 /O2 /MD d5ai-abi-driver.cpp independent-caller.obj d5ai-bridge.obj /Fe:d5ai-abi.exe /link /Brepro /INCREMENTAL:NO\n')
    script = output / 'build.cmd'
    script.write_text(command, encoding='utf8', newline='\r\n')
    compile_result = subprocess.run(['cmd', '/d', '/c', str(script)], cwd=output, capture_output=True)
    (output / 'compile.log').write_bytes(compile_result.stdout + compile_result.stderr)
    result = dict(schema='sor-d5ai-exact-object-abi/1', inputs=pins, compilation=compile_result.returncode,
                  candidate_object_sha256=sha(build / 'd5ai-bridge.obj'), free=guard())
    if compile_result.returncode == 0:
        run = subprocess.run([str(output / 'd5ai-abi.exe')], cwd=output, capture_output=True)
        (output / 'run.stdout').write_bytes(run.stdout)
        (output / 'run.stderr').write_bytes(run.stderr)
        result['exit'] = run.returncode
        if run.returncode == 0:
            result['oracle'] = json.loads(run.stdout)
        result['executable_sha256'] = sha(output / 'd5ai-abi.exe')
    result['sources_unchanged'] = all(sha(p) == digest for p, digest in pins.items())
    result['status'] = ('PASS' if result['compilation'] == 0 and result.get('exit') == 0 and
                        result['sources_unchanged'] else 'FAIL')
    (output / 'qualification.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf8', newline='\n')
    print(json.dumps(result))
    return 0 if result['status'] == 'PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())
