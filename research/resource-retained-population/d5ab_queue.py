# SPDX-License-Identifier: GPL-3.0-or-later
"""Compile and run the production queue in three disposable offline hosts.

Reads owned observer/stress sources and installed MSVC/SDK; writes a fresh ignored
directory, commands, compiler logs, executables and measured JSON receipts. Uses
no SFSE header, game code, network, deployment, saves, database or Git mutation.
Finite bounds apply to engineering tests only. CPython standard library only.
"""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
VC = Path('C:/Program Files/Microsoft Visual Studio/18/Community/VC/Auxiliary/Build/vcvars64.bat')


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    out = (ROOT / sys.argv[1]).resolve()
    assert out.is_relative_to(ROOT / '.local-work/d5ab')
    out.mkdir(parents=True, exist_ok=False)
    free = {d: shutil.disk_usage(d).free for d in ('C:/', 'D:/')}
    assert min(free.values()) >= 40_000_000_000
    src = ROOT / 'runtime/construction-winner/queue_stress.cpp'
    per_producer=int(sys.argv[2]) if len(sys.argv)>2 else 3000
    assert per_producer in (3000,8000)
    run_src=out/'queue_stress.generated.cpp'
    text=src.read_text().replace('i<3000','i<'+str(per_producer)).replace('U(p)*3000','U(p)*'+str(per_producer))
    text=text.replace('sequence+drops==12000','sequence+drops=='+str(4*per_producer)).replace('capacity<12000','capacity<'+str(4*per_producer))
    text=text.replace('burst_offered\\\":12000','burst_offered\\\":'+str(4*per_producer))
    run_src.write_text(text,encoding='utf8',newline='\n')
    inputs = {str(p): sha(p) for p in (src, src.with_name('observer.h'), VC,run_src)}
    commands = [f'call "{VC}"', 'if errorlevel 1 exit /b 1']
    for capacity in (1024, 8192, 32768):
        commands += [f'cl /nologo /std:c++20 /EHsc /W4 /O2 /MD /DSOR_QUEUE_CAPACITY={capacity} /I"{src.parent}" "{run_src}" /Fe:queue-{capacity}.exe /Fo:queue-{capacity}.obj /link /Brepro /INCREMENTAL:NO',
                     'if errorlevel 1 exit /b 1']
    script = out / 'build.cmd'
    script.write_text('@echo off\n' + '\n'.join(commands) + '\n', encoding='utf8', newline='\r\n')
    build = subprocess.run(['cmd', '/d', '/c', str(script)], cwd=out, capture_output=True)
    (out / 'build.log').write_bytes(build.stdout + build.stderr)
    assert build.returncode == 0, build.returncode
    results = []
    for capacity in (1024, 8192, 32768):
        exe = out / f'queue-{capacity}.exe'
        for repeat in range(3):
            run = subprocess.run([str(exe)], cwd=out, capture_output=True)
            (out / f'{capacity}-{repeat}.stdout').write_bytes(run.stdout)
            (out / f'{capacity}-{repeat}.stderr').write_bytes(run.stderr)
            assert run.returncode == 0, (capacity, repeat, run.stderr)
            result = json.loads(run.stdout)
            assert result['capacity'] == capacity and result['passed']
            assert result['burst_offered']==4*per_producer
            results.append(dict(result, repeat=repeat, executable_sha256=sha(exe)))
    assert all(sha(p) == h for p, h in inputs.items())
    receipt = dict(schema='sor-d5ab-queue-tests/1', inputs=inputs, initial_free=free,
                   results=results, source_unchanged=True,
                   final_free={d: shutil.disk_usage(d).free for d in free})
    (out / 'receipt.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf8', newline='\n')
    print(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()
