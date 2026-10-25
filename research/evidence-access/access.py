# SPDX-License-Identifier: GPL-3.0-or-later
"""Explicit archive access and shadow baselines; no real retirement operation.

Reuses owned Stage B locked Windows handles and Stage A strict streaming decoder.
Reads only caller-authenticated objects. Writes fresh disposable leases/control
receipts beneath .local-work/cargo-evidence-cutover; no network or target effect.
"""
import argparse
import contextlib
import hashlib
import json
import os
import ntpath
from pathlib import Path
import sys
import time
import uuid

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'research/evidence-archive-stage-b'))
import engine as e

LOCAL = ROOT / '.local-work/cargo-evidence-cutover'
INDEX = e.ARCHIVES / 'index.json'
INDEX_SHA = '5500892dbc247c642b83336ee619ca34d40fae8967ccfda95c5394e7ceff7e3b'
ARCHIVE_SHA = 'ebda740f0092b93f1dc9f32120db365223f465a6d374ce8e98933e8041eb1da7'
MANIFEST_SHA = 'f46605615abca2ff026f46aad6f51162a554c4383e89b79048899e4fb6e39a7a'
Error = e.Error


def output(path):
    return e.canonical(path, LOCAL)


def write(path, value):
    path = output(path)
    e.space(len(e.encode(value)) * 2 + 1024 * 1024)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as stream:
        stream.write(e.encode(value))
        stream.flush()
        os.fsync(stream.fileno())


class Store:
    """Trust roots are supplied externally, never learned from an unknown index."""
    def __init__(self, index=INDEX, index_sha=INDEX_SHA,
                 archive_sha=ARCHIVE_SHA, manifest_sha=MANIFEST_SHA):
        self.index = Path(index)
        self.index_sha = index_sha
        self.archive_sha = archive_sha
        self.manifest_sha = manifest_sha

    @contextlib.contextmanager
    def authenticated(self, deep=False):
        with e.locked(self.index):
            entry, archive, members = e.load(self.index, self.index_sha)
            if (entry['archive_sha256'] != self.archive_sha or
                    entry['manifest_sha256'] != self.manifest_sha):
                raise Error('Wrong externally pinned archive version')
            with e.locked(archive) as (stream, info):
                if (info.length != entry['archive_bytes'] or
                        hashlib.file_digest(stream, 'sha256').hexdigest() != self.archive_sha):
                    raise Error('Archive identity mismatch')
                if deep:
                    e.prototype.stream_members(archive, 'tar.zst', members)
                yield entry, archive, members

    def verify(self, deep=True):
        start = time.perf_counter()
        with self.authenticated(deep) as (entry, archive, members):
            return dict(schema=1, index_sha256=self.index_sha,
                        archive_sha256=self.archive_sha, manifest_sha256=self.manifest_sha,
                        members=len(entry['rows']), deep=deep,
                        routine_objects=2, routine_bytes=self.index.stat().st_size + archive.stat().st_size,
                        member_hashes=len(members) if deep else 0,
                        seconds=time.perf_counter() - start)

    def locate(self, original, source_root=ROOT):
        e.safe_name(original)
        with self.authenticated() as (entry, archive, members):
            rows = [r for r in entry['rows'] if r['path'] == original]
            if len(rows) != 1:
                raise Error('Missing or ambiguous exact original path')
            row = rows[0]
            source = e.canonical(Path(source_root) / original, source_root)
            # A changed loose file is an error, never silently hidden by archive fallback.
            if source.exists():
                e.inspect(source_root, [row])
                location = str(source)
            else:
                location = str(archive)
            return dict(original=original, location=location, member=original,
                        owner=entry['owner'], sha256=row['sha256'], bytes=row['bytes'],
                        loose=source.exists(), index_sha256=self.index_sha,
                        archive_sha256=self.archive_sha)

    def restore(self, destination, selected=None, experiment=None, fault=None):
        destination = output(destination)
        if destination.exists():
            raise Error('Refuse restore overwrite')
        if selected is not None and experiment is not None:
            raise Error('Choose member set or experiment')
        with self.authenticated(True) as (entry, archive, members):
            available = {r['path']: r for r in entry['rows']}
            if experiment is not None:
                if experiment not in ('c1-cargo', 'c2-transit', 'c2-transport', 'c3-fuel', 'c2-prose-spacing'):
                    raise Error('Unknown exact Cargo experiment')
                selected = [n for n in available if n.startswith('.local-work/' + experiment + '/')]
            selected = list(available) if selected is None else list(selected)
            e.names_valid(selected)
            if not selected or not set(selected) <= set(available):
                raise Error('Empty selection or orphaned member')
            rows = [available[n] for n in sorted(selected)]
            e.space(sum(r['bytes'] for r in rows) + len(rows) * 32768 + 32 * 1024 * 1024)
            partial = destination.with_name(destination.name + '.partial-' + uuid.uuid4().hex)
            partial.mkdir(parents=True)
            class Sink:
                def __init__(self, path):
                    path.parent.mkdir(parents=True, exist_ok=True)
                    self.stream = path.open('xb')
                def write(self, data):
                    return self.stream.write(data)
                def close(self):
                    self.stream.flush()
                    os.fsync(self.stream.fileno())
                    self.stream.close()
            class Discard:
                def write(self, data):
                    pass
                def close(self):
                    pass
            chosen = set(selected)
            def sink(name):
                return Sink(output(partial / name)) if name in chosen else Discard()
            e.prototype.stream_members(archive, 'tar.zst', members, sink)
            e.inspect(partial, rows)
            lease = dict(schema=1, state='OPEN', token=uuid.uuid4().hex,
                         index_sha256=self.index_sha, archive_sha256=self.archive_sha,
                         index=str(self.index), manifest_sha256=self.manifest_sha,
                         destination=str(destination), rows=rows,
                         lifecycle='Disposable scientific working copy; never a permanent preservation pin')
            write(partial / 'LEASE.json', lease)
            if fault == 'process-exit':
                os._exit(73)
            if fault:
                raise Error('Injected interruption; partial lease quarantined')
            # Stage B publisher only accepts its own roots: use its unchanged Windows API.
            if not e.K.MoveFileExW(str(partial), str(destination), 8):
                raise e.c.WinError(e.c.get_last_error())
            return dict(destination=str(destination), lease_sha256=e.pin(destination / 'LEASE.json'),
                        files=len(rows), bytes=sum(r['bytes'] for r in rows))


def lease_rows(destination, lease_sha):
    destination = output(destination)
    lease = e.authenticate(destination / 'LEASE.json', lease_sha)
    if (lease.get('schema') != 1 or lease.get('state') != 'OPEN' or
            lease.get('destination') != str(destination)):
        raise Error('Invalid or interrupted lease')
    e.names_valid([r['path'] for r in lease['rows']])
    store = Store(lease['index'], lease['index_sha256'], lease['archive_sha256'], lease['manifest_sha256'])
    with store.authenticated(True) as (entry, archive, members):
        for row in lease['rows']:
            if row['path'] not in members or any(row[k] != members[row['path']][k] for k in ('sha256', 'bytes')):
                raise Error('Lease member outside authenticated inventory')
    e.inspect(destination, lease['rows'])
    return lease


def cleanup(destination, lease_sha):
    """Only unchanged exact lease members; refuse unknown files or unsafe nodes."""
    destination = output(destination)
    lease = lease_rows(destination, lease_sha)
    expected = {r['path'] for r in lease['rows']} | {'LEASE.json'}
    actual = set()
    directories = []
    stack = [destination]
    while stack:
        folder = stack.pop()
        directories.append(folder)
        for node in folder.iterdir():
            e.canonical(node, destination)
            if node.is_dir():
                stack.append(node)
            else:
                actual.add(node.relative_to(destination).as_posix())
    if actual != expected:
        raise Error('Unregistered consumer outputs; preserve lease for explicit reconciliation')
    for name in sorted(expected - {'LEASE.json'}):
        (destination / name).unlink()
    (destination / 'LEASE.json').unlink()
    for directory in sorted(directories, key=lambda p: len(p.parts), reverse=True):
        directory.rmdir()


def consumer_paths(parser, experiment, default):
    """Opt-in input lease for maintained payload readers; output is always separate."""
    parser.add_argument('--evidence-lease', type=Path)
    parser.add_argument('--lease-sha256')
    parser.add_argument('--output-directory', type=Path)
    args = parser.parse_args()
    if not args.evidence_lease:
        if args.lease_sha256 or args.output_directory:
            parser.error('Lease digest/output require an explicit evidence lease')
        return args, default, default
    if not args.lease_sha256 or not args.output_directory:
        parser.error('Lease mode requires independent lease digest and fresh output directory')
    lease = lease_rows(args.evidence_lease, args.lease_sha256)
    prefix = '.local-work/' + experiment + '/'
    if not any(r['path'].startswith(prefix) for r in lease['rows']):
        raise Error('Experiment absent from lease')
    destination = output(args.output_directory)
    if destination.exists() or destination.is_relative_to(output(args.evidence_lease)):
        raise Error('Consumer output must be fresh and separate from lease')
    e.space(32 * 1024 * 1024)
    destination.mkdir(parents=True)
    return args, Path(args.evidence_lease) / '.local-work' / experiment, destination


def migrate(before, retired, store, expected_before):
    """Pure versioned shadow transformation; preserves the original full baseline."""
    if hashlib.sha256(e.encode(before)).hexdigest() != expected_before:
        raise Error('Wrong baseline')
    identities = [ntpath.normcase(ntpath.normpath(r['path'])) for r in before]
    if len(identities) != len(set(identities)):
        raise Error('Duplicate baseline identity')
    e.names_valid(retired)
    with store.authenticated(True) as (entry, archive, members):
        member_rows = {r['path']: r for r in entry['rows']}
        prior = {r['path']: r for r in before}
        if not set(retired) <= set(prior) or not set(retired) <= set(member_rows):
            raise Error('Silent omission or orphaned member')
        for name in retired:
            if any(prior[name][k] != member_rows[name][k] for k in ('sha256', 'bytes')):
                raise Error('Baseline member mismatch')
        archive_path = archive.relative_to(ROOT).as_posix()
        index_path = store.index.relative_to(ROOT).as_posix()
        kept = [r for r in before if r['path'] not in set(retired)]
        kept_names = {r['path'] for r in kept}
        # Existing archive/index rows are replaced exactly once, not appended twice.
        objects = [dict(path=archive_path, sha256=store.archive_sha, bytes=archive.stat().st_size),
                   dict(path=index_path, sha256=store.index_sha, bytes=store.index.stat().st_size)]
        for row in objects:
            if row['path'] in kept_names:
                old = prior[row['path']]
                if any(old[k] != row[k] for k in ('sha256', 'bytes')):
                    raise Error('Existing archive object mismatch')
        after = [r for r in kept if r['path'] not in {x['path'] for x in objects}] + objects
        return dict(schema='sor-preservation-shadow/1', state='PROPOSED-INACTIVE',
                    before_sha256=expected_before, before=before, after=after,
                    retired=sorted(retired), index_sha256=store.index_sha,
                    archive_sha256=store.archive_sha,
                    removed_rows=len(retired), routine_member_checks=0)


def rollback(shadow, expected_before):
    before = shadow['before']
    if (shadow['schema'] != 'sor-preservation-shadow/1' or shadow['state'] != 'PROPOSED-INACTIVE' or
            shadow['before_sha256'] != expected_before or
            hashlib.sha256(e.encode(before)).hexdigest() != expected_before):
        raise Error('Invalid shadow/recovery state')
    return before


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation', choices=['locate', 'verify', 'restore', 'cleanup'])
    parser.add_argument('--index', type=Path, default=INDEX)
    parser.add_argument('--index-sha256', default=INDEX_SHA)
    parser.add_argument('--archive-sha256', default=ARCHIVE_SHA)
    parser.add_argument('--manifest-sha256', default=MANIFEST_SHA)
    parser.add_argument('--member', action='append')
    parser.add_argument('--experiment')
    parser.add_argument('--destination', type=Path)
    parser.add_argument('--lease-sha256')
    parser.add_argument('--routine', action='store_true')
    args = parser.parse_args()
    store = Store(args.index, args.index_sha256, args.archive_sha256, args.manifest_sha256)
    if args.operation == 'verify':
        result = store.verify(not args.routine)
    elif args.operation == 'locate':
        if not args.member or len(args.member) != 1:
            parser.error('Locate requires one exact --member')
        result = store.locate(args.member[0])
    elif args.operation == 'restore':
        if not args.destination:
            parser.error('Restore requires --destination')
        result = store.restore(args.destination, args.member, args.experiment)
    else:
        if not args.destination or not args.lease_sha256:
            parser.error('Cleanup requires destination and externally retained lease digest')
        cleanup(args.destination, args.lease_sha256)
        result = dict(state='DISPOSABLE-LEASE-REMOVED')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
