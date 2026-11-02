# SPDX-License-Identifier: GPL-3.0-or-later
"""Freeze an explicitly supplied offline D5AI review bundle, without deployment.

Reads exact build inputs/outputs, separately prepared episode plans, frozen
prediction/review records and explicit receipts. Copies authored source snapshots,
the candidate DLL and existing approved notices into a fresh ignored directory.
Retains raw evidence at its original private path with hash references. No game,
save, analysis project, Git/index/ref, network, installation or approval action.
Canonical repository tools remain the execution root; copied tools are for review.
Owned P4 package/provenance methods are adapted under SOR-P-0002.
"""
import argparse
import json
from pathlib import Path
import shutil
import sys

from d5ae_baseline import guard, sha
from d5ai_geometry import load

ROOT = Path(__file__).resolve().parents[2]


def require(value, message):
    if not value:
        raise ValueError(message)


def fresh(path, value):
    with path.open('x', encoding='utf8', newline='\n') as stream:
        stream.write(json.dumps(value, indent=2, allow_nan=False) + '\n')


def main():
    if not __debug__ or sys.flags.optimize:
        raise RuntimeError('Use installed Python -E -B')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build', type=Path, required=True)
    parser.add_argument('--plan-a', type=Path, required=True)
    parser.add_argument('--plan-b', type=Path, required=True)
    parser.add_argument('--freeze', type=Path, required=True)
    parser.add_argument('--receipt', type=Path, action='append', required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    guard()
    require(args.out.resolve().is_relative_to(ROOT / '.local-work/d5ai'), 'Fresh task-local bundle required')
    require(args.build.resolve().is_relative_to(ROOT / '.local-work/d5ai-recorder'), 'Explicit task candidate required')
    build = load(args.build / 'build.json')
    require(build['source_unchanged'] is True and all(c['pass_exit'] for c in build['cases']),
            'Native build qualification incomplete')
    for path, digest in build['inputs'].items():
        require(sha(path) == digest, 'Build input changed: ' + path)
    for path, digest in build['outputs'].items():
        require(sha(args.build / path) == digest, 'Build output changed: ' + path)
    dll = args.build / 'package-runtime/SorConstructionWinner.dll'
    plans = [load(args.plan_a), load(args.plan_b)]
    for episode, plan in zip(('A', 'B'), plans):
        require(plan['schema'] == 'sor-d5ai-plan/1' and plan['episode'] == episode and
                plan['state'] == 'PREPARED_NOT_AUTHORIZED' and plan['dll_sha256'] == sha(dll),
                'Exact unapproved episode plan required')
        for group in ('controller_pins', 'phase_pins', 'package_pins'):
            for path, digest in plan[group].items():
                require(sha(path) == digest, 'Plan input changed: ' + path)
    freeze = load(args.freeze)
    require(freeze['schema'] == 'sor-d5ai-prediction-freeze/1' and
            freeze['measurement_review'] == 'ACCEPT' and freeze['phase_b_results_accessed'] is False,
            'Independent prospective measurement review/freeze required')
    for path, digest in freeze['pins'].items():
        require(sha(path) == digest, 'Frozen prediction input changed: ' + path)
    args.out.mkdir(exist_ok=False)
    sources = set()
    for plan in plans:
        for group in ('controller_pins', 'phase_pins', 'package_pins'):
            sources.update(Path(p).resolve() for p in plan[group] if Path(p).suffix.lower() in ('.py', '.json', '.md'))
    sources.update(ROOT.glob('research/resource-retained-population/d5ai_*.py'))
    sources.update(ROOT.glob('research/resource-retained-population/d5ai-*'))
    sources.add(ROOT / 'research/resource-retained-population/ExploreD5AIManager.java')
    sources.update(ROOT.glob('runtime/construction-winner/d5ai_*'))
    sources.update(ROOT.glob('docs/experiments/resource-retained-population/d5ai-*'))
    sources.update(ROOT.glob('docs/experiments/resource-retained-population/run-card-d5ai-*'))
    source_pins = {}
    for source in sorted(sources):
        require(source.is_relative_to(ROOT) and source.is_file(), 'Unexpected source outside repository')
        require(not source.is_relative_to(ROOT / '.local-work'), 'Raw/private files are references, not source snapshots')
        destination = args.out / 'review-sources' / source.relative_to(ROOT)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        require(sha(source) == sha(destination), 'Source copy mismatch')
        source_pins[str(source)] = sha(source)
    # Derived compiled sources are essential: the unchanged historical base is
    # insufficient to reproduce this candidate's source-informed adaptations.
    compiled = {}
    for number, (name, digest) in enumerate(sorted(build['inputs'].items())):
        source = Path(name)
        if source.suffix.lower() not in ('.h', '.cpp', '.asm', '.inc'):
            continue
        destination = args.out / 'compiled-inputs' / f'{number:04d}-{source.name}'
        destination.parent.mkdir(exist_ok=True)
        shutil.copyfile(source, destination)
        require(sha(destination) == digest, 'Compiled source copy mismatch')
        compiled[name] = dict(sha256=digest, snapshot=destination.relative_to(args.out).as_posix())
    candidate = args.out / 'candidate-NOT-AUTHORIZED'
    candidate.mkdir()
    shutil.copyfile(dll, candidate / dll.name)
    notice = ROOT / 'runtime/exp0002/third_party/sfse/LICENSE.txt'
    shutil.copyfile(notice, candidate / 'SFSE-PluginAPI-LICENSE.txt')
    references = [args.build / 'build.json', args.plan_a, args.plan_b, args.freeze, *args.receipt]
    receipts = {str(p.resolve()): dict(sha256=sha(p), bytes=p.stat().st_size) for p in references}
    for number, source in enumerate(references):
        destination = args.out / 'review-receipts' / f'{number:04d}-{source.name}'
        destination.parent.mkdir(exist_ok=True)
        shutil.copyfile(source, destination)
        require(sha(destination) == sha(source), 'Receipt copy mismatch')
    guard()
    manifest = dict(schema='sor-d5ai-offline-bundle/1', state='NOT_AUTHORIZED_FOR_EITHER_EPISODE',
                    execution_root=str(ROOT), execution_rule='Canonical tools only after exact pin checks; copies are review snapshots.',
                    dll_sha256=sha(dll), source_pins=source_pins, compiled_inputs=compiled,
                    receipt_references=receipts, prediction_freeze_sha256=sha(args.freeze),
                    method_sha256=sha(__file__), interpreter_sha256=sha(sys.executable),
                    files={str(p.relative_to(args.out).as_posix()): dict(sha256=sha(p), bytes=p.stat().st_size)
                           for p in sorted(args.out.rglob('*')) if p.is_file()},
                    limitations='No retail result, procedural-exception acceptance, publication clearance or live authority.')
    fresh(args.out / 'manifest.json', manifest)
    print(json.dumps(dict(files=len(manifest['files']), manifest_sha256=sha(args.out / 'manifest.json'))))


if __name__ == '__main__':
    main()
