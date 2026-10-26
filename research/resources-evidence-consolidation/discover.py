# SPDX-License-Identifier: GPL-3.0-or-later
"""Read system metadata and established pins; write fresh local discovery receipts.

Uses project-owned Stage A classification and Stage B locked source checks.
Requires installed CPython 3.14 and Windows. No deletion, baseline activation,
save-payload reads, target operations, external dependencies or Git mutation.
"""
from collections import Counter, defaultdict
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / '.local-work/resources-evidence-consolidation'
sys.path.insert(0, str(ROOT / 'research/evidence-archive-stage-b'))
import engine as e
sys.path.insert(0, str(ROOT / 'research/evidence-archive-discovery'))
import inventory
from scope import held


def write(name, value):
    data = e.encode(value)
    e.space(len(data) * 2 + 1024 * 1024)
    with (OUT / name).open('xb') as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT).decode().strip()


def run():
    initial_free = e.space()
    OUT.mkdir(parents=True, exist_ok=True)
    write('baseline.json', dict(head=git('rev-parse', 'HEAD'),
          index_sha256=e.pin(ROOT / '.git/index'), status=git('status', '--short'),
          free=initial_free))
    a = ROOT / '.local-work/evidence-archive-discovery'
    summary = json.loads((a / 'inventory-summary03.json').read_text())
    assert e.pin(a / 'inventory03.sqlite') == summary['inventory_sha256']
    prior = ROOT / '.local-work/resource-predictability-contrast/audit-before.json'
    assert e.pin(prior) == 'a243c67c0e451aac21cbb5fcb671c9e94ad2b3806406d0fdec1b2626f153ab9b'
    pins = json.loads(prior.read_text())['pins']
    norm = lambda p: os.path.normcase(os.path.normpath(str(p)))
    expected = {norm(p): v for p, v in pins.items()}
    db = sqlite3.connect(f'file:{(a / "inventory03.sqlite").as_posix()}?mode=ro', uri=True)
    old = {r[0]: dict(zip(('path', 'directory', 'area', 'bytes', 'allocation_estimate',
          'device', 'file_id', 'links', 'extension', 'role', 'uncertainty',
          'original_pin', 'mtime_ns'), r)) for r in db.execute('select * from files')}
    owners_path = a / 'candidate-owners-scoped02.sqlite'
    owners = sqlite3.connect(f'file:{owners_path.as_posix()}?mode=ro', uri=True)
    selected = {r[0] for r in owners.execute("select path from candidate where scheme_a='resources-production'")}
    assert len(selected) == 134140
    tops = sorted({p.split('/')[1] for p in selected})
    write('intake.json', dict(stage_a_inventory_sha256=summary['inventory_sha256'],
          scoped_owners_sha256=e.pin(owners_path), prior_sha256=e.pin(prior),
          stage_a_count=len(selected), stage_a_bytes=sum(old[p]['bytes'] for p in selected),
          system_directories=tops, inherited_methods={str(p.relative_to(ROOT)): e.pin(p)
          for p in (Path(__file__), Path(e.__file__), Path(inventory.__file__),
                    ROOT / 'research/evidence-archive-discovery/scope.py')}))
    rows, exclusions, errors = [], [], []
    seen = set()
    for top in tops:
        stack = [ROOT / '.local-work' / top]
        while stack:
            folder = stack.pop()
            try:
                e.canonical(folder, ROOT)
                entries = list(os.scandir(folder))
            except (OSError, e.Error) as exc:
                errors.append(dict(path=str(folder), error=str(exc)))
                continue
            for entry in entries:
                p = Path(entry.path)
                rel = p.relative_to(ROOT).as_posix()
                st = p.lstat()
                if st.st_file_attributes & 0x400:
                    errors.append(dict(path=rel, error='REPARSE; not followed'))
                    continue
                if entry.is_dir(follow_symlinks=False):
                    stack.append(p)
                    continue
                reason = held(rel, top, p.suffix.lower())
                row = dict(path=rel, bytes=st.st_size, device=st.st_dev,
                           file_id=st.st_ino, mtime_ns=st.st_mtime_ns,
                           owner='resources-production', original_pin=expected.get(norm(p)),
                           stage_a_member=rel in selected, role=inventory.role(rel, norm(p) in expected)[0])
                if reason:
                    exclusions.append(dict(row, reason=reason))
                    continue
                if st.st_nlink != 1:
                    errors.append(dict(path=rel, error='HARDLINK'))
                    continue
                if norm(p) in seen:
                    errors.append(dict(path=rel, error='ALIAS'))
                    continue
                seen.add(norm(p))
                rows.append(row)
    e.names_valid([r['path'] for r in rows])
    write('namespace.json', dict(rows=rows, exclusions=exclusions, errors=errors,
          missing_stage_a=sorted(selected - {r['path'] for r in rows}),
          added_since_stage_a=sorted(r['path'] for r in rows if not r['stage_a_member'])))
    if errors:
        raise e.Error('Unsafe namespace; inspect durable discovery errors')
    # Verify established scientific pins before proposing any archival admission.
    start = time.perf_counter()
    checked, conflicts = [], []
    for i, row in enumerate(r for r in rows if r['original_pin']):
        with e.locked(ROOT / row['path']) as (stream, info):
            actual = hashlib.file_digest(stream, 'sha256').hexdigest()
            checked.append(dict(path=row['path'], sha256=actual, bytes=info.length,
                                allocated_bytes=info.allocation))
            if actual != row['original_pin']:
                conflicts.append(dict(path=row['path'], expected=row['original_pin'], actual=actual))
        if i % 5000 == 0:
            print(f'Established pins verified: {i + 1}; conflicts: {len(conflicts)}', flush=True)
            e.space()
    counts = Counter(r['path'].split('/')[1] for r in rows)
    write('pin-verification.json', dict(checked=checked, conflicts=conflicts,
          seconds=time.perf_counter()-start, bytes_read=sum(r['bytes'] for r in checked)))
    result = dict(state='INTEGRITY-STOP' if conflicts else 'DISCOVERED',
          eligible_files=len(rows), eligible_bytes=sum(r['bytes'] for r in rows),
          exclusions=len(exclusions), stage_a_files=len(selected),
          added_files=sum(not r['stage_a_member'] for r in rows),
          missing_stage_a_files=len(selected - {r['path'] for r in rows}),
          recurring_inventory_candidate_total=len(pins), system_pin_overlap=len(checked),
          mismatches=len(conflicts), verification_seconds=time.perf_counter()-start,
          system_directories=dict(counts), free=e.space())
    write('discovery.json', result)
    print(json.dumps(result, indent=2), flush=True)


if __name__ == '__main__':
    run()
