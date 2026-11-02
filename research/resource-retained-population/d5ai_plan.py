# SPDX-License-Identifier: GPL-3.0-or-later
"""Prepare two offline, unapproved episode plans for an exact native candidate.

Adapts owned P4 package pinning under SOR-P-0002. Reads build/source receipts,
installed launch-input hashes and authored cards. Writes fresh ignored JSON only.
No launch, deployment, save mutation, approval, network or Git/index/ref action.
Canonical source paths remain the execution root; no copied tool is executed.
"""
import argparse
import json
from pathlib import Path
import re
import sys

from d5ae_baseline import guard, sha
from d5ai_geometry import load
from d5ai_episode import CONTROL_PATHS, ROOT, RUNTIME, SCHEMA, scope_for_episode
from d5ai_operations import PHASES
from d5ai_recorder_build import retail_guard_rows


def fresh(path, value):
    with path.open('x', encoding='utf8', newline='\n') as stream:
        stream.write(json.dumps(value, indent=2) + '\n')


def support_paths():
    paths = set(CONTROL_PATHS) | set(PHASES)
    paths.update(ROOT.glob('research/resource-retained-population/d5ai_*.py'))
    paths.update(ROOT.glob('research/resource-retained-population/d5ab_p4_*.py'))
    paths.update(ROOT.glob('runtime/session-tools/*.py'))
    paths.update(ROOT.glob('research/resource-carinae-source-context/*.py'))
    paths.add(ROOT / 'research/resource-carinae-source-context/save_policy.json')
    paths.update(ROOT / name for name in ('runtime/retained-population/protect.py',
                 'runtime/retained-population/build.py',
                 'runtime/retained-population/export_review.py',
                 'research/resource-retained-population/d5ae_baseline.py',
                 'research/resource-retained-population/d5ad_baseline.py',
                 'research/resource-retained-population/prepare_native.py'))
    for folder in ('resource-query-reachability', 'resources-evidence-consolidation',
                   'evidence-access', 'evidence-archive-discovery', 'evidence-archive',
                   'evidence-archive-stage-b', 'cargo-evidence-cutover'):
        paths.update((ROOT / 'research' / folder).glob('*.py'))
    return sorted(paths)


def main():
    if not __debug__ or sys.flags.optimize:
        raise RuntimeError('Use installed Python -E -B')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('build', type=Path)
    parser.add_argument('out', type=Path)
    args = parser.parse_args()
    guard()
    if not args.out.resolve().is_relative_to(ROOT / '.local-work/d5ai'):
        raise ValueError('Fresh task-local plan directory required')
    build = load(args.build / 'build.json')
    if build['source_unchanged'] is not True or not all(c['pass_exit'] for c in build['cases']):
        raise ValueError('Exact native qualification required')
    for path, digest in build['inputs'].items():
        if sha(path) != digest:
            raise ValueError('Build input changed: ' + path)
    dll = args.build / 'package-runtime/SorConstructionWinner.dll'
    if sha(dll) not in build['outputs'].values():
        raise ValueError('Candidate DLL/build mismatch')
    header = (args.build / 'identity.generated.h').read_text(encoding='utf8')
    pins = dict(re.findall(r'char (\w+)_hash\[\]="([0-9a-f]{64})"', header))
    site_block = header.split('inline Site sites[]={')[1].split('};')[0]
    sites = [dict(index=i, rva=int(rva), length=int(length), guard_sha256=digest)
             for i, (rva, length, digest) in enumerate(re.findall(r'\{(\d+),(\d+),"([0-9a-f]{64})"\}', site_block))]
    target_block = header.split('inline Target target_guards[]={')[1].split('};')[0]
    targets = [dict(rva=int(rva), guard_sha256=digest) for rva, digest in
               re.findall(r'\{(\d+),"([0-9a-f]{64})"\}', target_block)]
    if len(sites) != 18 or len(targets) != 7 or sites[2]['length'] != 13:
        raise ValueError('Incomplete native base guards')
    game = Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield')
    launch = {str(game / name): digest for name, digest in (
        ('Starfield.exe', pins['game']), ('sfse_1_16_244.dll', pins['sfse']),
        ('sfse_loader.exe', '16916c2ec47e31774e3d550609a1844fcb368b03060c03511891564b7f5f7526'),
        ('Data/Starfield.esm', pins['esm']), ('Data/Starfield - PlanetData.ba2', pins['planet']))}
    for path, digest in launch.items():
        guard()
        if sha(path) != digest:
            raise ValueError('Pinned launch input changed: ' + path)
    source_pins = {str(p): sha(p) for p in support_paths()}
    package_pins = source_pins | {str(dll.resolve()): sha(dll), str(Path(sys.executable)): sha(sys.executable)}
    args.out.mkdir(exist_ok=False)
    lock_sources = {ROOT / 'research/resource-retained-population' / name for name in
                    ('d5ai_checkpoint.py', 'd5ai_reduce.py', 'd5ai_geometry.py', 'd5ai_lifetime.py', 'd5ae_baseline.py')}
    lock_sources.update(RUNTIME / name for name in
                        ('read_capture.py', 'reduce_v3.py', 'reduce_v4.py', 'd5ai_read_geometry.py', 'd5ai_read_lifetime.py'))
    lock_path = args.out / 'checkpoint-source-lock.json'
    fresh(lock_path, dict(schema='sor-d5ai-source-lock/1', repository_root=str(ROOT),
                          dll_sha256=sha(dll), interpreter_sha256=sha(sys.executable),
                          sources={str(p): sha(p) for p in sorted(lock_sources)}))
    save_name = 'Save52_BA75E3CDM43616F205472616E_580743_20260818064541_319_15_4.sfs'
    for episode in ('A', 'B'):
        card = ROOT / f'docs/experiments/resource-retained-population/run-card-d5ai-episode-{episode.lower()}.md'
        plan = dict(schema=SCHEMA, state='PREPARED_NOT_AUTHORIZED', episode=episode,
                    scope=scope_for_episode(episode), run_card_path=str(card), run_card_sha256=sha(card),
                    save52_name=save_name, save52_sha256='6b4a10084c7e752c31fd2de121a00850aaa2bf1decd700b437d7dccfcdbc82e8',
                    python_executable=sys.executable, python_sha256=sha(sys.executable), python_flags=['-E', '-B'],
                    optimization='REFUSE_BEFORE_OPERATIONAL_IMPORTS', process_image=str(game / 'Starfield.exe'),
                    game_sha256=pins['game'], sfse_path=str(game / 'sfse_1_16_244.dll'), sfse_sha256=pins['sfse'],
                    dll_sha256=sha(dll), deployed_dll=str(game / 'Data/SFSE/Plugins/SorConstructionWinner.dll'),
                    live_root=str(ROOT / '.local-work/d5x/live'), sites=sites, call_targets=targets,
                    operations_sha256=sha(ROOT / 'research/resource-retained-population/d5ai_operations.py'),
                    package_pins=package_pins, launch_pins=launch,
                    phase_pins={str(p): sha(p) for p in sorted(PHASES)},
                    controller_pins={str(p): sha(p) for p in sorted(CONTROL_PATHS)},
                    checkpoint_source_lock_path=str(lock_path.resolve()), checkpoint_source_lock_sha256=sha(lock_path))
        plan.update(retail_guard_rows(args.build))
        fresh(args.out / f'episode-{episode.lower()}-plan.json', plan)
    fresh(args.out / 'manifest.json', dict(schema='sor-d5ai-episode-plans/1', authority='NONE',
          build_sha256=sha(args.build / 'build.json'), method_sha256=sha(__file__),
          files={p.name: sha(p) for p in sorted(args.out.iterdir()) if p.is_file()}))
    print('Prepared separate Episode A/B plans; neither episode is authorized.')


if __name__ == '__main__':
    main()
