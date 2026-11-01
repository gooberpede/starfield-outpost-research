# SPDX-License-Identifier: GPL-3.0-or-later
"""Build the pinned SFSE DLL and exercise it only in disposable native hosts.

Reads task source, existing identity receipt and installed MSVC/MASM/SDK. Writes
only a fresh .local-work/d5x build directory, compiled binaries, source snapshots,
command logs and raw synthetic receipts. No dependency downloads, game, saves,
deployment, configuration, analysis-database or Git mutations. Native fixtures
may terminate only their own disposable process in declared crash controls.
"""
import os
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
import importlib.util
import zipfile
import struct

ROOT = Path(__file__).resolve().parents[2]
SRC = Path(__file__).parent
VC = Path('C:/Program Files/Microsoft Visual Studio/18/Community/VC/Auxiliary/Build/vcvars64.bat')
CASES = ('normal mask-zero conflicting-mask unexpected-mask descriptor-change temporary-descriptor unrelated-conversion post-reset-old-provider schedule-old-first schedule-fresh-first reset-closeout edge corner null-cell overlap-reset orphan-sample bad-read bad-source bad-descriptor source-absent selection-only '
         'visited map-hit skip-sample nested interrupt in-flight-loss missing-lookup missing-descriptor '
         'missing-generator missing-sample prior-unknown ready-only descriptor-collision reused-pointer '
         'reset clear destroy erase concurrent competing loss-one loss-many saturation timing stop-under-production '
         'representative burst reserve-fail unknown-birth later-bypass write-fault flush-fault ack-fault disk-fault ack-write-fault crash-before crash-after crash-sample sequence-wrap guard-mismatch p1-noaccess-lookup p1-retire-lookup p1-reset-lookup p1-unpublished p1-constructor-exception').split()


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def guard():
    free = {drive: shutil.disk_usage(drive).free for drive in ('C:/', 'D:/')}
    assert min(free.values()) >= 40_000_000_000, free
    return free


def main():
    queue_capacity=int(os.environ.get("SOR_QUEUE_CAPACITY","32768"))
    assert queue_capacity in (1024,8192,32768)
    label = sys.argv[1]
    selected_cases = sys.argv[2:] or CASES
    assert set(selected_cases) <= set(CASES)
    assert re.fullmatch('[a-z0-9-]+', label)
    out = ROOT / '.local-work/d5x' / label
    out.mkdir(exist_ok=False)
    free = guard()
    identity = json.loads((ROOT / '.local-work/d5x/identity04/identity.json').read_text())
    assert all(sha(name) == digest for name, digest in identity['installed'].items())
    spec = importlib.util.spec_from_file_location('owned_pe_reader', ROOT / 'runtime/retained-population/build.py')
    pe = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(pe)
    image = (pe.GAME / 'Starfield.exe').read_bytes()
    emitter_page = bytearray(4096)
    emitter_ranges = [(0x988240, 23), (0x988330, 65), (0x988760, 103), (0x988ab0, 166)]
    emitter_pins = []
    for rva, count in emitter_ranges:
        raw = pe.pe_read(image, rva, count)
        emitter_page[rva - 0x988000:rva - 0x988000 + count] = raw
        emitter_pins.append(dict(rva=rva, size=count, sha256=hashlib.sha256(raw).hexdigest()))
    generated = out / 'emitters.generated.h'
    generated.write_text('#pragma once\ninline constexpr char emitter_expected_hash[]="' + hashlib.sha256(emitter_page).hexdigest() + '";\n', encoding='utf8', newline='\n')
    (out / 'emitter-input.bin').write_bytes(emitter_page)
    sites = [(0x79f860,7),(0x79fa90,8),(0x79fca3,9),(0x79fccb,5),(0x79feaf,5),(0x79ff18,5),(0x79b8e8,5),
             (0x79ddf0,5),(0x79d910,5),(0x975030,8),(0x9829b0,5),(0x982b70,5),(0x79dec4,5),(0x78d6f4,5),(0x9830cd,12),(0x983177,11),(0x79ff3e,5),(0x79ff59,11)]
    header = '#pragma once\nnamespace winner {\ninline constexpr uint32_t game_version=(1u<<24)|(16u<<16)|(244u<<4);\n'
    for key, value in [('game',pe.GAME_HASH),('sfse',pe.SFSE_HASH),('esm',identity['installed'][str(pe.GAME / 'Data/Starfield.esm')]),('planet',identity['installed'][str(pe.GAME / 'Data/Starfield - PlanetData.ba2')])]:
        header += f'inline constexpr char {key}_hash[]="{value}";\n'
    header += 'struct Site {uint64_t rva;unsigned length;const char* hash;};inline Site sites[]={\n'
    targets = []
    for index, (rva, size) in enumerate(sites):
        window = pe.pe_read(image, rva, 32)
        digest = hashlib.sha256(window).hexdigest()
        if index<14: assert digest == identity['sites'][f'0x{rva:x}']['raw_sha256']
        header += f'{{{rva},{size},"{digest}"}},\n'
        if index in (3,4,5,6,12,13,16):
            assert window[0] == 0xe8
            targets.append(rva + 5 + struct.unpack_from('<i',window,1)[0])
    assert targets == [0x3499f0,0x78d660,0x79b520,0x2339340,0x2c45a0,0x96f5c0,0x22cc0d0]
    header += '};struct Target {uint64_t rva;const char* hash;};inline Target target_guards[]={\n'
    for rva in targets:
        header += f'{{{rva},"{hashlib.sha256(pe.pe_read(image,rva,32)).hexdigest()}"}},\n'
    header += '};}\n'
    (out / 'identity.generated.h').write_text(header, encoding='utf8', newline='\n')
    inputs = {str(p): sha(p) for p in SRC.iterdir() if p.is_file()}
    for name in ('core.h', 'win_support.h', 'third_party/sfse/PluginAPI.h', 'third_party/sfse/LICENSE.txt'):
        p = ROOT / 'runtime/exp0002' / name
        inputs[str(p)] = sha(p)
    snapshot = out / 'sources'
    for name in inputs:
        p = Path(name)
        dest = snapshot / p.relative_to(ROOT)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(p.read_bytes())
    commands = [f'call "{VC}"', 'if errorlevel 1 exit /b 1', 'where cl', 'where link', 'where ml64',
                f'ml64 /nologo /c /Fobridges.obj "{SRC / "bridges.asm"}"',
                f'ml64 /nologo /c /Fofixture-asm.obj "{SRC / "fixture.asm"}"',
                f'cl /Bv /nologo /std:c++20 /EHsc /W4 /O2 /MD /DSOR_QUEUE_CAPACITY={queue_capacity} /I"{out}" "{SRC / "transport.cpp"}" "{SRC / "fixture.cpp"}" "{SRC / "plugin.cpp"}" bridges.obj fixture-asm.obj /LD /Fe:SorConstructionWinner.dll /link /Brepro /INCREMENTAL:NO bcrypt.lib',
                f'cl /nologo /std:c++20 /EHsc /W4 /O2 /MD "{SRC / "host.cpp"}" /Fe:sor-d5x-fixture.exe /link /Brepro /INCREMENTAL:NO',
                'dumpbin /DEPENDENTS SorConstructionWinner.dll']
    script = out / 'build.cmd'
    script.write_text('@echo off\n' + '\nif errorlevel 1 exit /b 1\n'.join(commands) + '\n', encoding='utf8', newline='\r\n')
    def run(command, name, expected=0):
        guard()
        result = subprocess.run(command, cwd=out, capture_output=True)
        (out / (name + '.log')).write_bytes(result.stdout + result.stderr)
        return dict(command=command, actual=result.returncode, expected=expected, pass_exit=result.returncode == expected)
    compilation = run(['cmd', '/d', '/c', str(script)], 'build')
    results = []
    if compilation['pass_exit']:
        package = out / 'SorConstructionWinner-disposable.zip'
        with zipfile.ZipFile(package, 'x', zipfile.ZIP_DEFLATED) as archive:
            for name in ('SorConstructionWinner.dll', 'sor-d5x-fixture.exe'):
                archive.write(out / name, name)
            archive.write(SRC / 'read_capture.py', 'read_capture.py')
            archive.write(SRC / 'reduce_v3.py', 'reduce_v3.py')
            archive.write(SRC / 'reduce_v4.py', 'reduce_v4.py')
            archive.write(SRC / 'worker_health.py', 'worker_health.py')
            archive.write(SRC / 'controller.py', 'controller.py')
            archive.write(out / 'emitter-input.bin', 'emitter-input.bin')
            archive.write(ROOT / 'runtime/exp0002/third_party/sfse/LICENSE.txt', 'SFSE-PluginAPI-MIT.txt')
            archive.write(ROOT / 'LICENSE', 'COPYING')
        with zipfile.ZipFile(out / 'SorConstructionWinner-D5X-review.zip', 'x', zipfile.ZIP_DEFLATED) as archive:
            archive.write(out / 'SorConstructionWinner.dll', 'Data/SFSE/Plugins/SorConstructionWinner.dll')
            archive.write(ROOT / 'runtime/exp0002/third_party/sfse/LICENSE.txt', 'SFSE-PluginAPI-MIT.txt')
            archive.write(ROOT / 'LICENSE', 'COPYING')
        extracted = out / 'package-runtime'
        extracted.mkdir()
        with zipfile.ZipFile(package) as archive:
            archive.extractall(extracted)
        assert all(sha(extracted / name) == sha(out / name) for name in ('SorConstructionWinner.dll', 'sor-d5x-fixture.exe','emitter-input.bin'))
        def qualify(case):
            expected = {'crash-before': 71, 'crash-after': 72, 'crash-sample': 73}.get(case, 0)
            result = run([str(extracted / 'sor-d5x-fixture.exe'), str(extracted / 'SorConstructionWinner.dll'), str(out / case), case], case, expected)
            return dict(case=case, **result)
        with ThreadPoolExecutor(max_workers=8) as pool:
            results = list(pool.map(qualify, selected_cases))
    result = dict(schema='sor-d5x-disposable-build/1', authority='OFFLINE_ONLY', sfse_entry=True, queue_capacity=queue_capacity,
                  inputs=inputs, installed=identity['installed'], emitter_pins=emitter_pins, initial_free=free, final_free=guard(), compilation=compilation, cases=results,
                  source_unchanged=all(sha(name) == digest for name, digest in inputs.items()),
                  outputs={str(p.relative_to(out)): sha(p) for p in out.rglob('*') if p.is_file()})
    (out / 'build.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf8', newline='\n')
    assert all(sha(name) == digest for name, digest in identity['installed'].items())
    print(json.dumps(dict(out=str(out), compilation=compilation['actual'], cases=len(results), failures=[row for row in results if not row['pass_exit']], source_unchanged=result['source_unchanged']), indent=2))
    return 0 if compilation['pass_exit'] and result['source_unchanged'] and all(row['pass_exit'] for row in results) else 1


if __name__ == '__main__':
    raise SystemExit(main())
