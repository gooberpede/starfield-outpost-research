# SPDX-License-Identifier: GPL-3.0-or-later
"""Prepare one non-save archive using the existing Stage A/B and access tooling.

Reads frozen namespace, established pins and explicitly named source members.
Writes local admission, archive, proposed index and disposable restoration only.
No real retirement, baseline activation, save access, network or target effects.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import os
from pathlib import Path
import sys
import time

from discover import ROOT, OUT, write
sys.path.insert(0, str(ROOT / 'research/evidence-access'))
import access as a
e = a.e
OWNER = 'resources-production'
ACTIVE_HOLDS = {'.local-work/resource-carinae-source-context/protected-before.json',
                '.local-work/resource-carinae/sync-paths-preflight02.json'}
ARCHIVE_FOLDER = e.ARCHIVES / 'resources-production-preparation01'
PROPOSED_INDEX = e.ARCHIVES / 'index-resources-proposed01.json'


def admit():
    namespace = json.loads((OUT / 'namespace.json').read_text())
    verification = json.loads((OUT / 'pin-verification.json').read_text())
    if verification['conflicts'] or namespace['errors'] or namespace['missing_stage_a']:
        raise e.Error('Discovery integrity stop; no archival admission')
    checked = {r['path']: r for r in verification['checked']}
    candidates = json.loads((ROOT / '.local-work/evidence-archive-discovery/expected-sample-pin-candidates03.json').read_text())
    ledgers = {ref['ledger']: ref['ledger_sha256'] for refs in candidates.values() for ref in refs}
    for name, digest in ledgers.items():
        if e.pin(ROOT / name) != digest:
            raise e.Error('Historical ledger changed: ' + name)
    norm = lambda p: os.path.normcase(os.path.normpath(str(p)))
    start = time.perf_counter()

    def one(row):
        p = e.canonical(ROOT / row['path'], ROOT)
        st = p.stat()
        if any(getattr(st, k) != row[v] for k, v in (
                ('st_ino', 'file_id'), ('st_dev', 'device'), ('st_size', 'bytes'), ('st_mtime_ns', 'mtime_ns'))):
            raise e.Error('Changed discovered source: ' + row['path'])
        prior = checked.get(row['path'])
        if prior is None:
            with e.locked(p) as (stream, info):
                digest = hashlib.file_digest(stream, 'sha256').hexdigest()
                allocation = info.allocation
        else:
            digest, allocation = prior['sha256'], prior['allocated_bytes']
        refs = candidates.get(norm(p), [])
        conflicts = [ref for ref in refs if ref['sha256'] != digest]
        # Conflicting executed versions remain loose, as in the Cargo baseline.
        return dict(path=row['path'], sha256=digest, bytes=row['bytes'],
                    owner=OWNER, file_id=row['file_id'], device=row['device'],
                    allocated_bytes=allocation, role=row['role'],
                    recurring_pin=bool(row['original_pin']), historical_expectations=refs,
                    disposition=('HELD-ACTIVE-PRESERVATION' if row['path'] in ACTIVE_HOLDS
                                 else 'HELD-VERSION-CONFLICT' if conflicts else 'PROPOSED-ARCHIVE-ONLY'))

    rows = []
    with ThreadPoolExecutor(max_workers=8) as pool:
        for i, row in enumerate(pool.map(one, namespace['rows'])):
            rows.append(row)
            if (i + 1) % 10000 == 0:
                print('Admission:', i + 1, flush=True)
                e.space()
    write('admission.json', dict(rows=rows, namespace_sha256=e.pin(OUT / 'namespace.json'),
          pins_sha256=e.pin(OUT / 'pin-verification.json'), seconds=time.perf_counter()-start,
          authenticated_ledger_hashes=ledgers))
    # Keep compact member metadata to stay within the inherited control limit.
    members = [{k: r[k] for k in ('path', 'sha256', 'bytes', 'owner')}
               for r in rows if r['disposition'] == 'PROPOSED-ARCHIVE-ONLY']
    holds = [r for r in rows if r['disposition'] != 'PROPOSED-ARCHIVE-ONLY']
    write('members.json', members)
    write('holds.json', holds)
    print(json.dumps(dict(members=len(members), holds=len(holds),
          member_bytes=sum(r['bytes'] for r in members), manifest_bytes=len(e.encode(members)))), flush=True)


def build():
    rows = json.loads((OUT / 'members.json').read_text())
    result = e.build(ROOT, rows, ARCHIVE_FOLDER, index_path=PROPOSED_INDEX, owner=OWNER)
    write('build.json', result)
    cargo = e.authenticate(e.ARCHIVES / 'index.json', a.INDEX_SHA)
    proposed = e.authenticate(PROPOSED_INDEX, result['index_sha256'])
    if set(cargo['archives']) & set(proposed['archives']):
        raise e.Error('Duplicate archive owner')
    proposed['archives'].update(cargo['archives'])
    proposed['cross_references'].extend(cargo['cross_references'])
    path = e.ARCHIVES / 'index-resources-merged-proposed01.json'
    e.record(path, proposed)
    write('proposed-central-index.json', dict(path=str(path), sha256=e.pin(path),
          state='PROPOSED-INACTIVE', prior_cargo_index_sha256=a.INDEX_SHA))


def restore():
    build = json.loads((OUT / 'build.json').read_text())
    index = json.loads((OUT / 'proposed-central-index.json').read_text())
    store = a.Store(index['path'], index['sha256'], build['archive_sha256'], build['manifest_sha256'], OWNER)
    result = store.restore(OUT / 'full-restore01')
    write('restore.json', result)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('phase', choices=('admit', 'build', 'restore'))
    args = parser.parse_args()
    globals()[args.phase]()
