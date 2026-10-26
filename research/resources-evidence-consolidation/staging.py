# SPDX-License-Identifier: GPL-3.0-or-later
"""Temporary C restore and proof-bound reconciliation of owned D working copies.

Uses the existing authenticated Store and exact lease cleanup. No archive is
copied to C. Reconciliation requires a stopped task-owned writer and a complete
verified alternate lease; unknown or changed members stop it. Incomplete prefixes
and worker metadata are preserved separately. Original evidence is never moved,
deleted or overwritten; this module operates only within the task workspaces.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import uuid

from cutover import ROOT, OUT, store, save, e, a


def restore_c():
    destination = a.RESOURCE_STAGING / 'resources-production-full01'
    with store().authenticated(False) as (entry, archive, members):
        reserve = sum(r['bytes'] for r in entry['rows']) + len(entry['rows'])*32768 + 32*1024*1024
    save(OUT / 'restore-c-preflight.json', dict(destination=str(destination),
         reserve_bytes=reserve, free=a.workspace_space(destination, reserve),
         authority='Temporary staging only; authoritative archive remains on D'))
    result = store().restore(destination)
    save(OUT / 'restore-c.json', result)
    print(json.dumps(result), flush=True)


def seal_partial(partial, identity, full_receipt, destination, quarantine, selected_store):
    """Recover a verified subset lease, preserving every incomplete prefix.

    The caller must prove its writer stopped and the full alternate lease was
    physically verified before calling. Its exact control is reauthenticated
    here; only actually used prefix sources need a fresh payload reread.
    """
    partial = e.canonical(partial, OUT)
    destination = e.canonical(destination, OUT)
    quarantine = e.canonical(quarantine, OUT)
    if (partial == OUT or '.partial-' not in partial.name or destination.exists() or
            destination == OUT or quarantine.exists() or destination.is_relative_to(partial) or
            quarantine.is_relative_to(partial)):
        raise e.Error('Fresh owned partial/recovery destinations required')
    st = partial.stat()
    if (st.st_dev, st.st_ino) != tuple(identity):
        raise e.Error('Owned partial directory identity changed')
    full_root = a.output(full_receipt['destination'])
    full = e.authenticate(full_root / 'LEASE.json', full_receipt['lease_sha256'])
    if (full.get('schema') != 1 or full.get('state') != 'OPEN' or
            full.get('destination') != str(full_root)):
        raise e.Error('Completed alternate lease control required')
    with selected_store.authenticated(False) as (entry, archive, members):
        expected = {r['path']: r for r in entry['rows']}
        full_rows = {r['path']: r for r in full['rows']}
        if (len(full_rows) != len(full['rows']) or full_rows != expected or
                full['index_sha256'] != selected_store.index_sha or
                full['archive_sha256'] != selected_store.archive_sha or
                full['manifest_sha256'] != selected_store.manifest_sha):
            raise e.Error('A complete matching alternate lease is required')
    completed, preserved = [], []
    observed = set()
    allowed_directories = {parent.as_posix() for name in expected for parent in Path(name).parents if str(parent) != '.'}
    for folder, dirs, files in os.walk(partial, followlinks=False):
        e.canonical(folder, partial)
        for name in dirs:
            child = e.canonical(Path(folder) / name, partial)
            if child.relative_to(partial).as_posix() not in allowed_directories:
                raise e.Error('Unknown working directory')
        for name in files:
            path = e.canonical(Path(folder) / name, partial)
            relative = path.relative_to(partial).as_posix()
            if relative in observed:
                raise e.Error('Duplicate working member')
            observed.add(relative)
            with e.locked(path) as (stream, info):
                digest = hashlib.file_digest(stream, 'sha256').hexdigest()
                length = info.length
            if relative == 'LEASE.json':
                preserved.append(dict(path=relative, bytes=length, sha256=digest, reason='Worker control retained as diagnostic'))
                continue
            row = expected.get(relative)
            if row is None or length > row['bytes']:
                raise e.Error('Unknown or oversized working member')
            if length == row['bytes'] and digest == row['sha256']:
                completed.append(row)
                continue
            if length == row['bytes']:
                raise e.Error('Changed complete working member')
            with e.locked(full_root / relative) as (source, info):
                if info.length != row['bytes'] or hashlib.file_digest(source, 'sha256').hexdigest() != row['sha256']:
                    raise e.Error('Used alternate source changed after full verification')
                source.seek(0)
                prefix = hashlib.sha256()
                remaining = length
                while remaining:
                    block = source.read(min(remaining, 1024*1024))
                    if not block:
                        raise e.Error('Incomplete alternate source')
                    prefix.update(block)
                    remaining -= len(block)
            if prefix.hexdigest() != digest:
                raise e.Error('Working prefix differs from verified alternate')
            preserved.append(dict(path=relative, bytes=length, sha256=digest, reason='Incomplete matching task-generated prefix'))
    if not completed:
        raise e.Error('No complete working members to recover')
    # No original has been changed: these exact moves preserve diagnostics from
    # the task-owned stopped writer outside the newly authenticated subset lease.
    for row in preserved:
        source = e.canonical(partial / row['path'], partial)
        target = e.canonical(quarantine / row['path'], OUT)
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists() or e.pin(source) != row['sha256']:
            raise e.Error('Working diagnostic changed before preservation')
        if not e.K.MoveFileExW(str(source), str(target), 8):
            raise e.c.WinError(e.c.get_last_error())
    lease = dict(schema=1, state='OPEN', token=uuid.uuid4().hex,
                 index_sha256=selected_store.index_sha, archive_sha256=selected_store.archive_sha,
                 index=str(selected_store.index), manifest_sha256=selected_store.manifest_sha,
                 owner=entry['owner'], destination=str(destination), rows=completed,
                 lifecycle='Verified subset recovered from a superseded task working copy; originals untouched')
    a.write(partial / 'LEASE.json', lease)
    lease_sha = e.pin(partial / 'LEASE.json')
    if not e.K.MoveFileExW(str(partial), str(destination), 8):
        raise e.c.WinError(e.c.get_last_error())
    return dict(destination=str(destination), lease_sha256=lease_sha,
                files=len(completed), bytes=sum(r['bytes'] for r in completed),
                preserved_diagnostics=preserved, original_evidence_changed=0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation', choices=('restore-c',))
    parser.parse_args()
    restore_c()
