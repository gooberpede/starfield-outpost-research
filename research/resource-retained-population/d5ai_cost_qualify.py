# SPDX-License-Identifier: GPL-3.0-or-later
"""Measure the exact retained producer objects in an independent owned host.

Reads current pinned headers, generated native input and build objects. Writes
fresh ignored source copies, build logs, executable and measured cost receipt.
Runs only its own process. Supplied logical lock fields isolate copy costs; this
is not a native-lock, worker-throughput or retail-frequency oracle.
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
    source = Path(__file__).parent / 'd5ai-cost-driver.cpp'
    header = ROOT / 'runtime/construction-winner/d5ai_geometry.h'
    retained = build / 'sources'
    object_names = ('transport.obj', 'bridges.obj', 'd5ai-bridge.obj')
    pins = {str(p): sha(p) for p in [source, header, Path(__file__), *[build / name for name in object_names]]}
    (output / source.name).write_bytes(source.read_bytes())
    # The include tree is the exact source snapshot of this selected candidate.
    candidate = next(retained.rglob('d5ai_geometry.h')).parent
    if sha(candidate / 'd5ai_geometry.h') != sha(header):
        raise ValueError('Current header differs from the tested producer')
    include = output / 'runtime/construction-winner'
    include.mkdir(parents=True)
    for name in ('d5ai_lifetime.h', 'd5ai_geometry.h', 'observer.h', 'patch.h', 'd5ai_population.generated.h'):
        (include / name).write_bytes((candidate / name).read_bytes())
    support = output / 'runtime/exp0002'
    support.mkdir()
    for name in ('win_support.h', 'core.h'):
        (support / name).write_bytes((retained / 'runtime/exp0002' / name).read_bytes())
    command = ('@echo off\ncall "' + str(VC) + '"\nif errorlevel 1 exit /b 1\n'
               'cl /nologo /std:c++20 /EHsc /W4 /O2 /MD /I"' + str(include) + '" d5ai-cost-driver.cpp ' +
               ' '.join('"' + str(build / name) + '"' for name in object_names) +
               ' /Fe:d5ai-cost.exe /link /Brepro /INCREMENTAL:NO bcrypt.lib\n')
    script = output / 'build.cmd'
    script.write_text(command, encoding='utf8', newline='\r\n')
    compile_result = subprocess.run(['cmd', '/d', '/c', str(script)], cwd=output, capture_output=True)
    (output / 'compile.log').write_bytes(compile_result.stdout + compile_result.stderr)
    result = dict(schema='sor-d5ai-exact-object-cost/1', inputs=pins, compilation=compile_result.returncode, free=guard())
    if compile_result.returncode == 0:
        run = subprocess.run([str(output / 'd5ai-cost.exe')], cwd=output, capture_output=True)
        (output / 'run.stdout').write_bytes(run.stdout)
        (output / 'run.stderr').write_bytes(run.stderr)
        result['exit'] = run.returncode
        if run.returncode == 0:
            result['measurements'] = json.loads(run.stdout)
        result['executable_sha256'] = sha(output / 'd5ai-cost.exe')
    result['sources_unchanged'] = all(sha(p) == digest for p, digest in pins.items())
    result['status'] = 'PASS' if result['compilation'] == 0 and result.get('exit') == 0 and result['sources_unchanged'] else 'FAIL'
    (output / 'qualification.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf8', newline='\n')
    print(json.dumps(result))
    return 0 if result['status'] == 'PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())
