# SPDX-License-Identifier: GPL-3.0-or-later
"""Run R3 disposable controls; never build a retail candidate.

Reads unchanged production sources, prior R1 DLL/host pins and owned R3 fixture.
Writes a fresh ignored child, counterfactual header, compiled Windows hosts,
raw test JSONL/logs and reductions. Runs installed MSVC and disposable hosts only.
Uses CPython stdlib and existing owned readers. No game, deployment, original
evidence mutation, save/configuration operation, download or Git write.
"""
import json
from pathlib import Path
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'runtime/retained-population'))
from build import sha, guard, VC
from read_capture import inspect


def write(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n', encoding='utf8', newline='\n')


def main():
    label = sys.argv[1]
    assert re.fullmatch('[a-z0-9-]+', label)
    out = ROOT / '.local-work/d5p-r3' / label
    out.mkdir(parents=True, exist_ok=False)
    original = ROOT / 'runtime/retained-population/observer.h'
    fixture = Path(__file__).with_name('d5p-r3-context.cpp')
    source_hashes = {str(p): sha(p) for p in (original, fixture, Path(__file__), VC)}
    start = guard()
    # A single explicit removal, never a production repair or deployable source.
    text = original.read_text(encoding='utf8')
    old = '&&predicate(n<=256,GridCoverageLimit)'
    assert text.count(old) == 1
    variant = out / 'uncapped-observer.h'
    variant.write_text(text.replace(old, ''), encoding='utf8', newline='\n')
    builds = {}
    for mode, header in (('production', original), ('counterfactual', variant)):
        directory = out / mode
        directory.mkdir()
        wrapper = directory / 'main.cpp'
        wrapper.write_text('#define SOR_R3_UNCAPPED ' + str(int(mode == 'counterfactual')) + '\n' +
                           '#define SOR_OBSERVER_HEADER "' + header.as_posix() + '"\n' +
                           '#include "' + fixture.as_posix() + '"\n', encoding='utf8', newline='\n')
        command = directory / 'compile.cmd'
        command.write_text('@echo off\ncall "' + str(VC) + '"\nif errorlevel 1 exit /b 1\n' +
                           'cl /Bv /nologo /std:c++20 /EHsc /W4 /O2 /MD main.cpp /Fe:context.exe /link /Brepro /INCREMENTAL:NO\n',
                           encoding='utf8', newline='\r\n')
        hashes = []
        for repeat in range(2):
            result = subprocess.run(['cmd', '/d', '/c', str(command)], cwd=directory, capture_output=True)
            (directory / f'compile{repeat}.log').write_bytes(result.stdout + result.stderr)
            assert result.returncode == 0, result.stdout.decode(errors='replace')
            hashes.append(sha(directory / 'context.exe'))
        assert hashes[0] == hashes[1], 'same-path rebuild differs'
        result = subprocess.run([str(directory / 'context.exe'), str(directory / 'cases.jsonl')], capture_output=True)
        (directory / 'run.log').write_bytes(result.stdout + result.stderr)
        assert result.returncode == 0, (mode, result.returncode)
        rows = [json.loads(line) for line in (directory / 'cases.jsonl').read_text().splitlines()]
        assert sum('case' in row for row in rows) == 41
        assert sum('timing_count' in row for row in rows) == 5
        builds[mode] = dict(exe_sha256=hashes[0], reproducible=True, rows=rows,
                            header_sha256=sha(header), wrapper_sha256=sha(wrapper))
    r1 = ROOT / '.local-work/d5p/r1-build04'
    prior = json.loads((r1 / 'build.json').read_text())
    dll_hash = sha(r1 / 'SorRetainedPopulation.dll')
    assert dll_hash == prior['dll_sha256'] == '503464d3670ff00422303c10652b036cd0bc891d3f8f7cba9a22d9d396fb5667'
    assert sha(r1 / 'sor-d5p-fixture.exe') == prior['host_sha256']
    cases = ('normal', 'context-reasons', 'nested', 'concurrent', 'aba', 'reset', 'clear', 'retire',
             'loss-one', 'loss-many', 'retry-one', 'retry-many', 'loss-cross', 'loss-fence',
             'loss-rebuild', 'in-flight-loss', 'hook-stress', 'stress', 'crash-before', 'crash-after',
             'late-disk-fault', 'late-write-fault', 'late-flush-fault', 'late-ack-fault', 'late-ack-write-fault')
    def run(name):
        guard()
        result = subprocess.run([str(r1 / 'sor-d5p-fixture.exe'), str(r1 / 'SorRetainedPopulation.dll'), str(out / name), name], capture_output=True)
        (out / (name + '.log')).write_bytes(result.stdout + result.stderr)
        assert result.returncode == {'crash-before': 71, 'crash-after': 72}.get(name, 0), (name, result.returncode)
        reduction = inspect(out / name, dll_hash)
        if name in ('loss-one', 'loss-many', 'retry-one', 'retry-many'):
            assert reduction['known_ordinary_drops'] == (1 if name.endswith('one') else 37)
            assert reduction['loss_diagnostics']['failed'] is False
        if name in ('loss-cross', 'loss-fence', 'in-flight-loss', 'crash-before', 'aba', 'reset', 'clear', 'retire'):
            assert not reduction['complete_chains'], name
        elif name != 'context-reasons':
            assert reduction['complete_chains'], name
        if name.startswith('late-'):
            assert reduction['loss_diagnostics']['failed'] and reduction['independently_verified_durable_records'] >= 9
        return name, reduction
    with ThreadPoolExecutor(max_workers=4) as pool:
        regressions = dict(pool.map(run, cases))
    write(out / 'dll-regressions.json', regressions)
    assert source_hashes == {p: sha(p) for p in source_hashes}
    write(out / 'qualification.json', dict(authority='R3_OFFLINE_ONLY_NO_CANDIDATE',
          initial_free=start, final_free=guard(), sources=source_hashes, builds=builds,
          dll_sha256=dll_hash, host_sha256=prior['host_sha256'], dll_cases=list(regressions),
          limits='Counterfactual is altered source-path evidence, not the production DLL or retail qualification.'))
    print(out)


if __name__ == '__main__':
    main()
