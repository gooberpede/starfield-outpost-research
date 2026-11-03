# SPDX-License-Identifier: GPL-3.0-or-later
"""Prepare an unapproved D5AL operational bundle without deployment.

SOR-P-0002 lineage: D5AI plan/bundle pinning and D5AJ checkpoint source lock.
Reads frozen approved plan, original native ZIP, owned sources and new card.
Writes exclusive ignored staging files, source snapshots, locks and manifest.
No save, game, Vortex, database, controller request, approval or network writes.
Requires installed Python -E -B and both caller-available disk floors. Preserve
all outputs, including failed preparations; never replace an existing bundle.
"""
import sys
import os
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):
    raise RuntimeError('Use Python -E -B')

import argparse
import copy
import hashlib
import json
from pathlib import Path
import zipfile

from d5ae_baseline import ROOT, guard, sha
import d5al_operations as operations

ORIGINAL = ROOT / '.local-work/d5ai/vortex-package01/SorConstructionWinner-0.7.0.zip'
ZIP_HASH = '9b81fac5b62fc97ad2582dc48e9717d138643b6fa1a1e78fe8eb6912f31f830c'
DLL_HASH = '9df5a04ef770887b402dca7c61ee3af52f6046711fcd4e997b66922055bbe67c'
FILENAME = 'SorConstructionWinner-0.7.0-D5AL-B-r1.zip'
CARD = ROOT / 'docs/experiments/resource-retained-population/run-card-d5al-episode-b.md'


def fresh(path, value):
    with path.open('x', encoding='utf8', newline='\n') as stream:
        stream.write(json.dumps(value, indent=2) + '\n')


def members(path):
    with zipfile.ZipFile(path) as archive:
        rows = []
        seen = set()
        for info in archive.infolist():
            if info.filename.casefold() in seen:
                raise ValueError('Duplicate package member')
            seen.add(info.filename.casefold())
            data = archive.read(info)
            rows.append(dict(name=info.filename, bytes=len(data), sha256=hashlib.sha256(data).hexdigest(),
                             date_time=info.date_time, compression=info.compress_type,
                             crc=info.CRC, external_attr=info.external_attr,
                             extra_hex=info.extra.hex(), comment_hex=info.comment.hex()))
        return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('out', type=Path)
    args = parser.parse_args()
    out = args.out.resolve()
    if not out.is_relative_to(ROOT / '.local-work/d5al'):
        raise ValueError('Fresh task-local staging required')
    free = guard()
    old_path = ROOT / '.local-work/d5ai/final-plans05/episode-b-plan.json'
    old = json.loads(old_path.read_bytes())
    # Do not silently rebaseline any frozen source or producer identity.
    for name, expected in old['package_pins'].items():
        if sha(name) != expected:
            raise ValueError('Frozen package input changed: ' + name)
    if sha(ORIGINAL) != ZIP_HASH or old['dll_sha256'] != DLL_HASH:
        raise ValueError('Qualified native package mismatch')
    out.mkdir(parents=True, exist_ok=False)
    candidate = out / FILENAME
    with candidate.open('xb') as stream:
        stream.write(ORIGINAL.read_bytes())
    if sha(candidate) != ZIP_HASH or candidate.read_bytes() != ORIGINAL.read_bytes():
        raise ValueError('Filename alias must retain exact archive bytes')
    before, after = members(ORIGINAL), members(candidate)
    if before != after:
        raise ValueError('Package member or metadata mismatch')
    dll_rows = [r for r in after if r['name'].lower().endswith('/sorconstructionwinner.dll')]
    if len(dll_rows) != 1 or dll_rows[0]['sha256'] != DLL_HASH:
        raise ValueError('Installed-shaped native DLL mismatch')
    # No Vortex path is written. A same-named prior import would be ambiguous.
    vortex = Path('C:/Users/User/AppData/Roaming/Vortex/downloads/starfield')
    collisions = list(vortex.glob(FILENAME + '*')) if vortex.exists() else []
    mods = Path('C:/Users/User/AppData/Roaming/Vortex/starfield/mods')
    collisions += list(mods.glob(Path(FILENAME).stem + '*')) if mods.exists() else []
    downloads = Path('C:/Users/User/Downloads')
    collisions += list(downloads.glob(FILENAME + '*'))
    if collisions:
        raise ValueError('Archive alias already present in Vortex: ' + str(collisions))
    source_dir = ROOT / 'research/resource-retained-population'
    lock_sources = {source_dir / n for n in ('d5aj_checkpoint.py', 'd5aj_reduce.py', 'd5aj_scope.py',
                    'd5ai_geometry.py', 'd5ai_lifetime.py', 'd5ae_baseline.py')}
    lock_sources.update(ROOT / 'runtime/construction-winner' / n for n in
                        ('read_capture.py', 'reduce_v3.py', 'reduce_v4.py', 'd5ai_read_geometry.py', 'd5ai_read_lifetime.py'))
    aj_lock = out / 'd5aj-source-lock.json'
    fresh(aj_lock, dict(schema='sor-d5aj-source-lock/1', repository_root=str(ROOT),
                        dll_sha256=DLL_HASH, interpreter_sha256=sha(sys.executable),
                        sources={str(p): sha(p) for p in sorted(lock_sources)}))
    required = operations.required_sources() | lock_sources | {Path(p).resolve() for p in old['package_pins']}
    ak_lock = out / 'd5al-source-lock.json'
    fresh(ak_lock, dict(schema='sor-d5al-operational-lock/1', interpreter=sys.executable,
                        interpreter_sha256=sha(sys.executable), dll_sha256=DLL_HASH,
                        sources={str(p): sha(p) for p in sorted(required)}))
    plan = copy.deepcopy(old)
    plan.update(state='PREPARED_NOT_AUTHORIZED', run_card_path=str(CARD), run_card_sha256=sha(CARD),
                d5al_source_lock=str(ak_lock), d5al_source_lock_sha256=sha(ak_lock),
                d5aj_source_lock=str(aj_lock), d5aj_source_lock_sha256=sha(aj_lock),
                package_zip=str(candidate), package_zip_sha256=sha(candidate), package_filename=FILENAME,
                install_archive=str(candidate), install_archive_sha256=sha(candidate),
                native_version='0.7.0', checkpoint_method='sor-d5aj-source-grid/1')
    import d5al_content
    plan.update(timestamp_policy=d5al_content.POLICY,
                episode_b_adapter_pins={str(p): sha(p) for p in d5al_content.ADAPTERS},
                trusted_stop_sha256=sha(Path(__file__).with_name('d5al_stop.py')))
    baseline_path = ROOT / '.local-work/d5al/baseline01/manifest.json'
    identity_path = ROOT / '.local-work/d5x/live/session-4da7b6b6ed99fb240b3fd380ad5000e0ba4a39d73301dbff5be919e688e28af6/identity.json'
    identity = json.loads(identity_path.read_bytes())
    plan.update(d5al_baseline=str(baseline_path), d5al_baseline_sha256=sha(baseline_path),
                d5ak_a_process=dict(creation_filetime=identity['creation_filetime'], nonce=identity['nonce'], identity_sha256=sha(identity_path)))
    plan['package_pins'].update({str(p): sha(p) for p in required | lock_sources})
    # Keep legacy checkpoint pins for reproducibility; new commands explicitly
    # select the separately named D5AJ lock and never reinterpret old outputs.
    operations.source_pins(plan)
    plan_path = out / 'episode-b-plan.json'
    fresh(plan_path, plan)
    sources = set(required) | lock_sources | {Path(p) for p in old['package_pins'] if Path(p).is_relative_to(ROOT)}
    for path in sorted(sources | {CARD}):
        if not path.is_relative_to(ROOT):
            continue
        target = out / 'source-snapshot' / path.relative_to(ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open('xb') as stream:
            stream.write(path.read_bytes())
    files = {p.relative_to(out).as_posix(): dict(bytes=p.stat().st_size, sha256=sha(p))
             for p in sorted(out.rglob('*')) if p.is_file()}
    fresh(out / 'manifest.json', dict(schema='sor-d5al-bundle/1', authority='NONE',
          original_plan=dict(path=str(old_path), sha256=sha(old_path)),
          original_card=dict(path=old['run_card_path'], sha256=old['run_card_sha256']),
          new_card=dict(path=str(CARD), sha256=sha(CARD)), new_plan=dict(path=str(plan_path), sha256=sha(plan_path)),
          native_version='0.7.0', dll_sha256=DLL_HASH, zip_sha256=sha(candidate), filename=FILENAME,
          original_zip=str(ORIGINAL), byte_identical_archive=True,
          member_metadata_and_content_equal=before == after, members=after,
          operational_changes='New source locks, controller/checkpoint coupling and prospective card outside the unchanged native archive.',
          free=free, vortex_checked=[str(vortex), str(mods), str(downloads)], vortex_collisions=[], files=files,
          manifest_self_hash='Excluded to avoid recursive content identity; delivery manifest pins this file.'))
    print(json.dumps(dict(plan=str(plan_path), package=str(candidate), sha256=sha(candidate))))


if __name__ == '__main__':
    main()
