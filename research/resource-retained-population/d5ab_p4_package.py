# SPDX-License-Identifier: GPL-3.0-or-later
"""Freeze an offline-only P4 bundle; never install or enable its DLL.

Reads unchanged Final04/Repro02 build receipts, generated pins, current tools
and existing P4 qualification receipts. Writes exclusive ignored staging copies,
candidate ZIP, plan, manifest and exact source/receipt inventories. No game,
save/configuration/database/Git mutation, network or new dependency.
Owned build/export/provenance methods are reused under SOR-P-0002.
"""

import sys

# Safety checks below require assertions, including when imported as a helper.
if not __debug__ or sys.flags.optimize != 0:
    raise RuntimeError('Python optimization is forbidden; invoke with -E -B and no -O/-OO')
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import shutil
import zipfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'runtime/session-tools'))
from common import fresh, guard, sha, read


def main():
    out = (ROOT / sys.argv[1]).resolve()
    assert out.is_relative_to(ROOT / '.local-work/d5ab')
    out.mkdir(parents=True, exist_ok=False)
    guard()
    build = (ROOT / sys.argv[2]).resolve() if len(sys.argv) > 2 else ROOT / '.local-work/d5x/p3-native-final04'
    reproduction = (ROOT / sys.argv[3]).resolve() if len(sys.argv) > 3 else ROOT / '.local-work/d5x/p3-repro02'
    assert build.is_relative_to(ROOT / '.local-work/d5x')
    assert reproduction.is_relative_to(ROOT / '.local-work/d5x')
    native = read(build / 'build.json')
    assert native['source_unchanged'] and native['compilation']['pass_exit']
    assert all(row['pass_exit'] for row in native['cases'])
    for path, digest in native['inputs'].items():
        assert sha(path) == digest, path
    for path, digest in native['outputs'].items():
        assert sha(build / path) == digest, path
    dll = build / 'package-runtime/SorConstructionWinner.dll'
    assert sha(dll) == sha(reproduction / 'package-runtime/SorConstructionWinner.dll')
    assert sha(dll) == sha(ROOT / '.local-work/d5x/p3-native-final04/package-runtime/SorConstructionWinner.dll')
    header = (build / 'identity.generated.h').read_text(encoding='utf8')
    site_block = header.split('inline Site sites[]={')[1].split('};')[0]
    sites = [dict(index=i, rva=int(rva), length=int(length), guard_sha256=digest)
             for i, (rva, length, digest) in enumerate(re.findall(r'\{(\d+),(\d+),"([0-9a-f]{64})"\}', site_block))]
    assert len(sites) == 18 and sites[2]['length'] == 13
    pins = dict(re.findall(r'char (\w+)_hash\[\]="([0-9a-f]{64})"', header))
    # Read exact executable windows through the existing owned PE reader.
    spec = importlib.util.spec_from_file_location('p4_pe', ROOT / 'runtime/retained-population/build.py')
    pe = importlib.util.module_from_spec(spec); spec.loader.exec_module(pe)
    image = (pe.GAME / 'Starfield.exe').read_bytes()
    assert hashlib.sha256(image).hexdigest() == pins['game']
    for row in sites:
        assert hashlib.sha256(pe.pe_read(image, row['rva'], 32)).hexdigest() == row['guard_sha256']
    target_block = header.split('inline Target target_guards[]={')[1].split('};')[0]
    targets = [dict(rva=int(rva), guard_sha256=digest) for rva, digest in
               re.findall(r'\{(\d+),"([0-9a-f]{64})"\}', target_block)]
    assert len(targets) == 7
    for row in targets:
        assert hashlib.sha256(pe.pe_read(image, row['rva'], 32)).hexdigest() == row['guard_sha256']
    candidate = out / 'candidate'; candidate.mkdir()
    shutil.copyfile(dll, candidate / dll.name)
    notice = ROOT / 'runtime/exp0002/third_party/sfse/LICENSE.txt'
    shutil.copyfile(notice, candidate / 'SFSE-PluginAPI-LICENSE.txt')
    zip_path = out / 'candidate-NOT-AUTHORIZED.zip'
    with zipfile.ZipFile(zip_path, 'x', compression=zipfile.ZIP_DEFLATED) as z:
        z.write(dll, 'Data/SFSE/Plugins/' + dll.name)
        z.write(notice, 'SFSE-PluginAPI-LICENSE.txt')
    tool_paths = [ROOT / 'runtime/construction-winner' / name for name in
                 ('p4_controller.py','controller.py','worker_health.py','read_capture.py','reduce_v3.py','reduce_v4.py')]
    operations = ROOT / 'research/resource-retained-population/d5ab_p4_operations.py'
    support = tool_paths + list((ROOT / 'runtime/session-tools').glob('*.py')) + [operations]
    support += list((ROOT / 'research/resource-retained-population').glob('d5ab_p4_*.py'))
    support += [ROOT / 'runtime/retained-population/protect.py',
                ROOT / 'runtime/retained-population/build.py',
                ROOT / 'research/resource-retained-population/prepare_native.py']
    support += list((ROOT / 'research/resource-carinae-source-context').glob('*.py'))
    support += [ROOT / 'research/resource-carinae-source-context/save_policy.json']
    for folder in ('resource-query-reachability', 'resources-evidence-consolidation',
                   'evidence-access', 'evidence-archive-discovery',
                   'evidence-archive', 'evidence-archive-stage-b', 'cargo-evidence-cutover'):
        support += list((ROOT / 'research' / folder).glob('*.py'))
    closure = None
    if len(sys.argv) > 4:
        closure_path = (ROOT / sys.argv[4]).resolve()
        assert closure_path.is_relative_to(ROOT / '.local-work/d5ab')
        closure = read(closure_path)
        assert closure['passed'] and closure['executed_modules']
        for name, digest in closure['executed_modules'].items():
            path = (ROOT / name).resolve()
            assert path.is_relative_to(ROOT) and path.suffix == '.py'
            assert sha(path) == digest
            support.append(path)
    support = sorted(set(support))
    source_pins = {str(path): sha(path) for path in support}
    for path in support:
        dest = out / 'review-tools' / path.relative_to(ROOT)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, dest)
    package_pins = source_pins | {str(candidate / dll.name):sha(dll), str(zip_path):sha(zip_path),
                                  str(Path(sys.executable)):sha(sys.executable)}
    plan = dict(schema='sor-d5ab-p4-plan/1', state='PREPARED_NOT_AUTHORIZED',
        python_executable=sys.executable, python_sha256=sha(sys.executable),
        python_flags=['-E','-B'], optimization='REFUSE_BEFORE_OPERATIONAL_IMPORTS',
        process_image=str(pe.GAME / 'Starfield.exe'), game_sha256=pins['game'],
        sfse_path=str(pe.GAME / 'sfse_1_16_244.dll'), sfse_sha256=pins['sfse'],
        dll_sha256=sha(dll), deployed_dll=str(pe.GAME / 'Data/SFSE/Plugins' / dll.name),
        live_root=str(ROOT / '.local-work/d5x/live'), sites=sites, call_targets=targets,
        operations_sha256=sha(operations), package_pins=package_pins,
        launch_pins={str(pe.GAME / name):digest for name, digest in (
            ('Starfield.exe', pins['game']),
            ('sfse_1_16_244.dll', pins['sfse']),
            ('sfse_loader.exe', '16916c2ec47e31774e3d550609a1844fcb368b03060c03511891564b7f5f7526'),
            ('Data/Starfield.esm', pins['esm']),
            ('Data/Starfield - PlanetData.ba2', pins['planet']))},
        phase_pins={str(path):sha(path) for path in (operations,
            ROOT / 'runtime/session-tools/common.py',
            ROOT / 'research/resource-carinae-source-context/save_policy.py')},
        controller_pins={str(path):sha(path) for path in tool_paths})
    fresh(out / 'plan.json', plan)
    manifest = dict(schema='sor-d5ab-p4-offline-package/1', authority='NOT_AUTHORIZED_FOR_B2',
        execution_root=str(ROOT), execution_rule='Run canonical repository tools only after pin checks; review-tools are frozen snapshots.',
        native_build=str(build / 'build.json'), native_build_sha256=sha(build / 'build.json'),
        reproduction_sha256=sha(reproduction / 'build.json'),
        build_input_pins=native['inputs'],
        compiled_source_pins={path:digest for path,digest in native['inputs'].items()
                             if Path(path).suffix.lower() in ('.h','.cpp','.asm')},
        source_pins=source_pins,
        dependency_closure=None if closure is None else dict(path=str(closure_path),sha256=sha(closure_path)),
        executable='Starfield 1.16.244.0', sfse='0.2.21', schema_version='sor-d5x/4',
        plan_sha256=sha(out / 'plan.json'), dll_sha256=sha(dll), zip_sha256=sha(zip_path),
        files={p.relative_to(out).as_posix():dict(bytes=p.stat().st_size,sha256=sha(p))
               for p in sorted(out.rglob('*')) if p.is_file()},
        rights='Owned source SOR-P-0002; unchanged approved SFSE header/notices; no game bytes included.',
        exclusions='Game/assets/saves/native exports/databases/raw/private evidence remain local; no publication clearance.')
    fresh(out / 'manifest.json', manifest)
    print(json.dumps(dict(out=str(out), files=len(manifest['files']), dll_sha256=sha(dll), plan_sha256=sha(out / 'plan.json'))))


if __name__ == '__main__':
    main()
