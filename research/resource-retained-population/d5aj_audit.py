# SPDX-License-Identifier: GPL-3.0-or-later
"""Authenticate immutable Episode A inputs and derive a diagnostic event census.

Reads existing sealed local evidence, installed executable, protected research
Save52, original methods and Git identity. Writes a fresh ignored output directory.
Uses owned D5AI readers and D5AE guards under SOR-P-0002; stdlib only. No target,
save, database, controller, configuration, network or Git mutation. Diagnostic
joins are not qualified source continuity. Invoke installed Python -E -B.
"""
import sys
if not __debug__ or sys.flags.optimize:
    raise RuntimeError('Use Python -E -B')
import argparse
from collections import Counter
import json
from pathlib import Path
import subprocess
import zipfile

from d5ae_baseline import ROOT, guard, sha
import d5ai_reduce as old

SESSION = ROOT / '.local-work/d5x/live/session-2f305e35afac69b4faca3025a30c7e6f0c04aeaefd579c387d464ef3c4981571'
DLL = '9df5a04ef770887b402dca7c61ee3af52f6046711fcd4e997b66922055bbe67c'
NONCE = '8ef67521dc0fbaa4e2178aed3e987aa1'


def write(path, value):
    with Path(path).open('x', encoding='utf8', newline='\n') as stream:
        stream.write(json.dumps(value, indent=2) + '\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('out', type=Path)
    args = parser.parse_args()
    if not args.out.resolve().is_relative_to(ROOT / '.local-work/d5aj'):
        raise ValueError('Fresh D5AJ output required')
    free = guard()
    args.out.mkdir(parents=True, exist_ok=False)
    base = ROOT / '.local-work/d5ai-a/archive01'
    seal_path = base / 'seal.json'
    archive = base / 'episode-a-attempt01.zip'
    if sha(seal_path) != 'b6f4c0906072cb7d54af7d26ae8bd4f559bd6b64d68382cda12e92dee43384c2' or sha(archive) != '194aa78d3517c3c7c3ad2959fcf9c7011a044d36cc076ecd05a94a47f3627497':
        raise ValueError('Immutable archive/seal mismatch')
    seal = old.load(seal_path)
    verified = {}
    import hashlib
    with zipfile.ZipFile(archive) as zipped:
        if set(zipped.namelist()) != set(seal['files']) | {'SOR-MANIFEST.json'}:
            raise ValueError('Archive path inventory mismatch')
        for name, pin in seal['files'].items():
            root, rel = name.split('/', 1)
            original = Path(seal['roots'][root]['path']) / rel
            data = zipped.read(name)
            if len(data) != pin['size'] or hashlib.sha256(data).hexdigest() != pin['sha256'] or sha(original) != pin['sha256']:
                raise ValueError('Archive/original mismatch: ' + name)
            verified[str(original)] = dict(bytes=len(data), sha256=pin['sha256'])
    policy = old.load(ROOT / 'research/resource-carinae-source-context/save_policy.json')
    save_name = next(n for n in policy['designated'] if n.startswith('Save52_'))
    save = ROOT / '.local-work/savegames' / save_name
    exe = Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield/Starfield.exe')
    if sha(save) != '6b4a10084c7e752c31fd2de121a00850aaa2bf1decd700b437d7dccfcdbc82e8' or sha(exe) != '7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28':
        raise ValueError('Protected sample/executable mismatch')
    approved = old.load(ROOT / '.local-work/d5ai-a/plan-a02.json')
    approved_sources = {}
    for name, expected in approved['package_pins'].items():
        if sha(name) != expected:
            raise ValueError('Original approved package source mismatch: ' + name)
        approved_sources[name] = expected
    package = ROOT / '.local-work/d5ai/vortex-package01/SorConstructionWinner-0.7.0.zip'
    if sha(package) != '9b81fac5b62fc97ad2582dc48e9717d138643b6fa1a1e78fe8eb6912f31f830c':
        raise ValueError('Approved package ZIP mismatch')
    import d5ai_checkpoint
    d5ai_checkpoint.verify_source_lock(approved['checkpoint_source_lock_path'], approved['checkpoint_source_lock_sha256'], DLL)
    preflight = old.load(ROOT / '.local-work/d5ai-a/preflight02/receipt.json')
    backup_rows = preflight['protection']['backups'][save_name]
    backups = []
    for row in backup_rows:
        if row['kind'] != 'LOOSE_BACKUP' or sha(row['path']) != row['sha256'] or row['sha256'] != sha(save):
            raise ValueError('Independent Save52 backup mismatch')
        backups.append(row)
    methods = [p for p in (ROOT / 'research/resource-retained-population').glob('d5ai*.py')]
    methods += list((ROOT / 'runtime/construction-winner').glob('*'))
    methods += [ROOT / 'docs/experiments/resource-retained-population' / n for n in ('d5ai-predictions.md', 'd5ai-prediction-text-v1.md', 'd5ai-a-report.md', 'run-card-d5ai-episode-a.md')]
    pins = {str(p): sha(p) for p in methods if p.is_file()}
    git = lambda *a: subprocess.check_output(['git', *a], cwd=ROOT).decode().strip()
    write(args.out / 'preservation.json', dict(head=git('rev-parse', 'HEAD'), index_sha256=sha(ROOT / '.git/index'), status=git('status', '--short'), free=free,
          archive_sha256=sha(archive), seal_sha256=sha(seal_path), verified=verified, frozen_methods=pins,
          approved_sources=approved_sources, package=dict(path=str(package), sha256=sha(package)), save52_backups=backups,
          save=dict(path=str(save), sha256=sha(save)), exe=dict(path=str(exe), sha256=sha(exe)), method_sha256=sha(__file__),
          interpreter=dict(path=sys.executable, sha256=sha(sys.executable), version=sys.version)))
    report = old.inspect(SESSION, DLL, old.read_capture.TARGET)
    sidecar = old.d5ai_read_geometry.read_session(SESSION)
    snapshot = sidecar['snapshots'][0]
    events = report['events']
    h = snapshot['header']
    holders = []
    for ordinal, holder in enumerate(snapshot['holders'], 1):
        births = [e for e in events if e['kind'] == 14 and e['source'] == holder['source_pointer'] and e['ticks'] < h['ticks_begin']]
        birth = max(births, key=lambda e: (e['ticks'], e['sequence'])) if births else None
        pubs = [e for e in events if e['kind'] == 15 and e['source'] == holder['source_pointer'] and birth and birth['ticks'] < e['ticks'] < h['ticks_begin']]
        try:
            old.source_identity(events, holder['source_pointer'], h)
            refusal = None
        except ValueError as error:
            refusal = str(error)
        generations = [e for e in events if e['kind'] == 6 and e['d'] == holder['holder_pointer'] + 8]
        holders.append(dict(ordinal=ordinal, holder=holder, birth=birth, publications=pubs,
                            key=None if birth is None else old.read_capture.source_key(birth),
                            generations=generations, historical_refusal=refusal))
    # Keep complete decoded evidence local, including adverse and non-target history.
    write(args.out / 'events.json', events)
    write(args.out / 'snapshot.json', snapshot)
    write(args.out / 'lifetime.json', report['lifetime'])
    write(args.out / 'holders.json', holders)
    write(args.out / 'census.json', dict(records=len(events), kinds=dict(Counter(e['kind'] for e in events)),
          fences=[e for e in events if e['kind'] in (10, 11)], header=h,
          original_refused=report['refused'], original_observations=report['observations'],
          geometry_errors=sidecar['errors'], lifetime_coverage=old.d5ai_read_lifetime.qualify_snapshot(snapshot, report['lifetime']),
          core_sha256=report['lifecycle_raw_sha256'], method_sha256=sha(__file__)))
    print(json.dumps(dict(records=len(events), holders=len(holders), original_refused=report['refused'], free=free)))


if __name__ == '__main__':
    main()
