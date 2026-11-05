# SPDX-License-Identifier: GPL-3.0-or-later
"""Build/run the original owned C++ writer in disposable offline fixture hosts.

Reads D5AR source and installed MSVC/Windows SDK; writes fresh ignored build/logs,
synthetic snapshots and exact receipt. Executes only own compiled fixture, never
SFSE or Starfield. No install, download, save/database/configuration/Git mutation.
Stops on compiler, floor, parser/hash/canonicalization or fixture mismatch.
"""
import os
import sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):
    raise RuntimeError('Use pinned Python -E -B without optimization')

import json
from pathlib import Path
import subprocess
import d5ar_snapshot as snapshot


def main():
    root = Path(__file__).resolve().parents[2]
    out = Path(sys.argv[1]).resolve()
    snapshot.guard()
    snapshot.require(out.is_relative_to(root / '.local-work/d5ar') and not out.exists(), 'Fresh D5AR output required')
    snapshot.require(not any(p.is_symlink() or p.is_junction() for p in (out, *out.parents)), 'No reparse outputs')
    out.mkdir(parents=True)
    source = root / 'runtime/outpost-geometry-snapshot'
    sources = [source / n for n in ('writer.h', 'writer.cpp', 'writer_fixture.cpp', 'capture_fixture.h', 'capture.h', 'identity.h',
                                    'operation.h', 'selection.h', 'source_lifetime.h', 'startup.h', 'startup_fixture.h', 'binding.h', 'binding_fixture.h')]
    sources += [Path(__file__), Path(snapshot.__file__), Path(snapshot.geometry.__file__)]
    source_pins = {str(p.relative_to(root)): snapshot.digest(p.read_bytes()) for p in sources}
    vc = Path('C:/Program Files/Microsoft Visual Studio/18/Community/VC/Auxiliary/Build/vcvars64.bat')
    script = out / 'compile.cmd'
    script.write_text('@echo off\ncall "' + str(vc) + '" >nul\nif errorlevel 1 exit /b %errorlevel%\n' +
        'cl /nologo /std:c++20 /EHsc /W4 /WX /MT /O2 /Brepro /Fe:"' + str(out / 'writer-fixture.exe') +
        '" "' + str(source / 'writer.cpp') + '" "' + str(source / 'writer_fixture.cpp') +
        '" /link /INCREMENTAL:NO /Brepro\nexit /b %errorlevel%\n', encoding='utf8', newline='\r\n')
    compile_result = subprocess.run(['cmd.exe', '/d', '/c', str(script)], cwd=out, capture_output=True)
    (out / 'compile-stdout.log').write_bytes(compile_result.stdout)
    (out / 'compile-stderr.log').write_bytes(compile_result.stderr)
    snapshot.require(compile_result.returncode == 0, 'Native writer compile failed; retain logs')
    modes = ['normal', 'refused', 'bad-hash', 'bad-date', 'bad-path-date', 'bad-point', 'duplicate', 'missing-dir', 'capture-core', 'startup-core', 'binding-core']
    checks = []
    for mode in modes:
        directory = out / mode
        directory.mkdir()
        result = subprocess.run([str(out / 'writer-fixture.exe'), str(directory), mode], capture_output=True)
        (directory / 'stdout.log').write_bytes(result.stdout)
        (directory / 'stderr.log').write_bytes(result.stderr)
        snapshot.require(result.returncode == 0 and b'PASS' in result.stdout, 'Native writer fixture failed: ' + mode)
        files = list(directory.glob('*.snapshot.json'))
        snapshot.require(len(files) == (1 if mode in ('normal', 'refused') else 0), 'Unexpected complete artifact')
        for path in files:
            value = snapshot.load(path)
            snapshot.require(path.read_bytes() == snapshot.encoded(value) + b'\n', 'Independent canonical JSON/hash mismatch')
            snapshot.require(value['status'] == ('REFUSED' if mode == 'refused' else 'COPIED_UNQUALIFIED'), 'Native refusal lost')
            snapshot.require(len(value['sources']) == 2 and value['sources'][1]['geometry'] is None, 'Unknown holder lost or fabricated')
            geometry = value['sources'][0]['geometry']
            snapshot.require(geometry['capture']['point_total'] == 2 and geometry['source'] is None and geometry['frame'] is None,
                             'Native geometry exactness/qualification mismatch')
            snapshot.require(geometry['population'][0]['regions'][0]['header'].endswith('abcdef'), 'Raw padding lost')
        checks.append(dict(mode=mode, result='PASS', stdout=result.stdout.decode().strip()))
    snapshot.require({str(p.relative_to(root)): snapshot.digest(p.read_bytes()) for p in sources} == source_pins,
                     'Executed writer source changed during qualification')
    receipt = dict(status='PASS', native_writer_only=True, plugin_execution=False, checks=checks,
                   inputs=source_pins,
                   exe_sha256=snapshot.digest((out / 'writer-fixture.exe').read_bytes()),
                   compiler_setup_sha256=snapshot.digest(vc.read_bytes()), floors=snapshot.guard())
    (out / 'qualification.json').write_bytes(snapshot.encoded(receipt) + b'\n')
    print(json.dumps(dict(status='PASS', modes=len(modes), receipt=str(out / 'qualification.json'))))


if __name__ == '__main__':
    main()
