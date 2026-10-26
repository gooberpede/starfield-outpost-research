# SPDX-License-Identifier: GPL-3.0-or-later
"""Exact authorized archive retirement and baseline publication on Windows.

Reads externally pinned approval, proposal, recovery, shadow and archive objects.
Writes only a fresh transaction directory, its append-only journal and baseline.
Only execute() removes originals, through authenticated open file handles. CLI
execution requires a separately supplied approval digest; this brief is no GO.
Uses project-owned access/retirement/Stage A/B code and installed Python stdlib.
"""
import argparse
import contextlib
import datetime as dt
import hashlib
import json
import msvcrt
import os
from pathlib import Path
import subprocess
import sys

import access as a
import retirement

e = a.e
LOCAL = a.ROOT / '.local-work/cargo-retirement'
PREFIXES = tuple('.local-work/' + x + '/' for x in (
    'c1-cargo', 'c2-transit', 'c2-transport', 'c3-fuel', 'c2-prose-spacing'))
HOLDS = {'.local-work/' + x + '/package.py' for x in ('c2-transit', 'c2-transport', 'c3-fuel')}
# Read-only census, 2026-10-26: these six historical empty directories are
# outside the file-derived ancestry. They are retained, never deletion targets.
EMPTY_DIRECTORIES = {'.local-work/' + x + '/scratch' for x in ('c1-cargo', 'c2-transport', 'c3-fuel')} | {
    '.local-work/' + x + '/ghidra-cache/User-ghidra/fscache2/new' for x in ('c2-transit', 'c2-transport', 'c3-fuel')}
OPERATION = 'RETIRE EXACT CARGO ALLOWLIST AND ACTIVATE ARCHIVE BASELINE'


def digest(value):
    return hashlib.sha256(e.encode(value)).hexdigest()


def git_identity():
    return dict(head=subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=a.ROOT).decode().strip(),
                repo_index_sha256=e.pin(a.ROOT / '.git/index'))


def runtime_identity():
    return dict(executable=str(Path(sys.executable).resolve()),
                executable_sha256=e.pin(sys.executable), version=sys.version)


def git_guard_paths():
    """Lock the current loose HEAD/ref and index without changing Git metadata."""
    folder = a.ROOT / '.git'
    head = (folder / 'HEAD').read_text().strip()
    paths = [folder / 'HEAD', folder / 'index']
    if head.startswith('ref: '):
        ref = head[5:]
        e.safe_name(ref)
        reference = folder / ref
        if not reference.is_file():
            raise a.Error('Resource retirement requires an existing lockable loose branch ref')
        paths.append(reference)
    return paths


def scope(names, prefixes=PREFIXES, holds=HOLDS):
    e.names_valid(list(names))
    if not names or any(not n.startswith(prefixes) or n in holds for n in names):
        raise a.Error('Non-Cargo or held source in exact retirement scope')


@contextlib.contextmanager
def ancestors(paths):
    """Hold existing directories against rename/delete during the transaction.

    Denying directory DELETE sharing closes the ancestor replacement race under
    the declared exclusive operator ownership; file content locks are separate.
    """
    handles = []
    try:
        dirs = {p for path in paths for p in Path(path).absolute().parents}
        for directory in sorted(dirs, key=str):
            e.canonical(directory)
            h = e.K.CreateFileW(str(directory), 0x80, 3, None, 3, 0x02200000, None)
            if h == e.w.HANDLE(-1).value:
                raise e.c.WinError(e.c.get_last_error())
            handles.append(h)
            e.canonical(directory)
        yield
    finally:
        for h in reversed(handles):
            e.K.CloseHandle(h)


def census(root, names, holds, prefixes=PREFIXES, empty_directories=EMPTY_DIRECTORIES, excluded=()):
    """Enumerate the declared namespaces; reject every unknown node."""
    excluded_names = {r['path'] for r in excluded}
    expected = set(names) | {r['path'] for r in holds} | excluded_names
    found = set()
    allowed_dirs = {p.parent for name in expected for p in (Path(root) / name, *(Path(root) / name).parents)
                    if p.is_relative_to(root)}
    allowed_dirs |= {p for n in empty_directories for p in (Path(root) / n, *(Path(root) / n).parents)
                     if p.is_relative_to(root)}
    for prefix in prefixes:
        folder = e.canonical(Path(root) / prefix.rstrip('/'), root)
        if not folder.exists():
            continue
        stack = [folder]
        while stack:
            for p in stack.pop().iterdir():
                e.canonical(p, root)
                if p.is_dir():
                    if p not in allowed_dirs:
                        raise a.Error('Unexpected empty or nonmember directory')
                    stack.append(p)
                elif p.is_file():
                    name = p.relative_to(root).as_posix()
                    if name not in expected:
                        raise a.Error('Unexpected Cargo directory contents: ' + name)
                    found.add(name)
                else:
                    raise a.Error('Unsupported source node')
    for row in excluded:
        path = e.canonical(Path(root) / row['path'], root)
        st = path.stat()
        if (row['path'] not in found or st.st_nlink != 1 or any(
                getattr(st, field) != row[key] for field, key in (
                    ('st_size', 'bytes'), ('st_ino', 'file_id'), ('st_dev', 'device'), ('st_mtime_ns', 'mtime_ns')))):
            raise a.Error('Protected exclusion namespace changed')
    return found - excluded_names


def checked(stream, info, row, identity=True):
    info = standard(stream)
    st = os.fstat(stream.fileno())
    stream.seek(0)
    if (info.links != 1 or info.pending or info.directory or info.length != row['bytes'] or
            hashlib.file_digest(stream, 'sha256').hexdigest() != row['sha256'] or
            (row.get('mtime_ns') is not None and st.st_mtime_ns != row['mtime_ns']) or
            (row.get('allocated_bytes') is not None and info.allocation != row['allocated_bytes']) or
            (identity and (st.st_ino != row['file_id'] or st.st_dev != row['device']))):
        raise a.Error('Source content or file identity mismatch: ' + row['path'])


def standard(stream):
    info = e.Standard()
    if not e.K.GetFileInformationByHandleEx(msvcrt.get_osfhandle(stream.fileno()), 1,
                                           e.c.byref(info), e.c.sizeof(info)):
        raise e.c.WinError(e.c.get_last_error())
    return info


def disposition(stream, remove):
    flag = e.c.c_ubyte(remove)
    if not e.K.SetFileInformationByHandle(msvcrt.get_osfhandle(stream.fileno()), 4,
                                          e.c.byref(flag), e.c.sizeof(flag)):
        raise e.c.WinError(e.c.get_last_error())


def methods():
    paths = [Path(__file__), Path(a.__file__), Path(retirement.__file__), Path(e.__file__), Path(e.prototype.__file__)]
    return {p.relative_to(a.ROOT).as_posix(): e.pin(p) for p in paths}


def system_methods():
    paths = sorted((a.ROOT / 'research/resources-evidence-consolidation').glob('*.py'))
    paths += [a.ROOT / 'research' / name / 'protection.py' for name in (
        'resource-carinae-source-context', 'resource-tungsten-acquisition')]
    return {p.relative_to(a.ROOT).as_posix(): e.pin(p) for p in paths}


class Journal:
    """Hash-chained, fsynced JSON-lines; a torn/invalid tail requires recovery."""
    def __init__(self, path, binding, writable=False, boundary=LOCAL):
        self.path, self.binding = Path(path), digest(binding)
        self.events = []
        self.tail = '0' * 64
        self.path = e.canonical(self.path, boundary)
        h = e.K.CreateFileW(str(self.path), 0xC0000000 if writable else 0x80000000,
                           1, None, 4 if writable else 3, 0x00200000, None)
        if h == e.w.HANDLE(-1).value:
            raise e.c.WinError(e.c.get_last_error())
        fd = msvcrt.open_osfhandle(h, (os.O_RDWR if writable else os.O_RDONLY) | os.O_BINARY)
        self.stream = os.fdopen(fd, 'r+b' if writable else 'rb')
        try:
            info = standard(self.stream)
            if info.links != 1 or info.directory:
                raise a.Error('Unsupported journal identity')
            e.stream_check(self.path)
            raw = self.stream.read()
            if raw:
                self.load(raw)
            self.validate()
        except BaseException:
            self.close()
            raise

    def close(self):
        self.stream.close()

    def load(self, raw):
        if raw:
            if not raw.endswith(b'\n'):
                raise a.Error('RECOVERY_REQUIRED: interrupted journal write')
            for line in raw.splitlines():
                item = json.loads(line)
                h = item.pop('hash')
                if (item['previous'] != self.tail or item['binding'] != self.binding or
                        item['ordinal'] != len(self.events) or digest(item) != h):
                    raise a.Error('RECOVERY_REQUIRED: journal chain mismatch')
                self.events.append(item)
                self.tail = h

    def validate(self):
        self.state, self.pending, self.completed = None, None, []
        self.completed_set = set()
        for item in self.events:
            self.transition(item)

    def transition(self, item):
        """Validate each new transition once; replay still validates the full chain."""
        event, name = item['event'], item['path']
        if event == 'PREPARED' and self.state is None:
            self.state = 'PREPARED'
        elif event == 'INTENT' and self.state in ('PREPARED', 'RETIRING') and self.pending is None and name not in self.completed_set:
            self.pending, self.state = name, 'RETIRING'
        elif event == 'DONE' and self.pending == name and self.state == 'RETIRING':
            self.completed.append(name)
            self.completed_set.add(name)
            self.pending = None
        elif event == 'RETIRED_PENDING_BASELINE' and self.state == 'RETIRING' and self.pending is None:
            self.state = event
        elif event == 'COMMITTED' and self.state == 'RETIRED_PENDING_BASELINE':
            self.state = event
        else:
            raise a.Error('RECOVERY_REQUIRED: illegal journal transition')

    def append(self, event, path=None):
        e.space(4 * 1024 * 1024)
        item = dict(binding=self.binding, ordinal=len(self.events), previous=self.tail, event=event, path=path)
        h = digest(item)
        raw = json.dumps(dict(item, hash=h), sort_keys=True).encode() + b'\n'
        self.stream.seek(0, 2)
        start = self.stream.tell()
        self.stream.write(raw)
        self.stream.flush()
        os.fsync(self.stream.fileno())
        self.stream.seek(start)
        if self.stream.read() != raw:
            raise a.Error('RECOVERY_REQUIRED: journal readback failed')
        self.events.append(item)
        self.tail = h
        self.transition(item)


class Transaction:
    """Caller-pinned controls; no candidate file supplies its own trust root."""
    def __init__(self, root, store, plan, plan_sha, recovery, recovery_sha, shadow, shadow_sha, folder,
                 profile=None):
        self.root = e.canonical(root)
        self.store = store
        self.controls = [(Path(plan), plan_sha), (Path(recovery), recovery_sha), (Path(shadow), shadow_sha)]
        self.profile = profile
        self.control_limit = 64 * 1024 * 1024 if profile is None else 128 * 1024 * 1024
        self.operation = OPERATION if profile is None else 'RETIRE EXACT RESOURCES PRODUCTION POWER ALLOWLIST AND ACTIVATE ARCHIVE BASELINE'
        self.boundary = LOCAL if profile is None else a.ROOT / '.local-work/resources-evidence-consolidation'
        self.prefixes = PREFIXES if profile is None else tuple(profile['prefixes'])
        self.hold_names = HOLDS if profile is None else set(profile['holds'])
        self.empty_directories = EMPTY_DIRECTORIES if profile is None else set(profile['empty_directories'])
        self.excluded = () if profile is None else profile['excluded']
        if profile is not None:
            if set(profile) != {'owner', 'prefixes', 'holds', 'empty_directories', 'excluded'} or profile['owner'] != store.owner or store.owner != 'resources-production':
                raise a.Error('Unsupported explicit system profile')
            e.names_valid([p.rstrip('/') for p in self.prefixes])
            if any(not p.startswith('.local-work/') or not p.endswith('/') or len(p.split('/')) != 3 for p in self.prefixes):
                raise a.Error('Unsafe system namespace profile')
            protected_names = profile['holds'] + [r['path'] for r in self.excluded]
            e.names_valid(protected_names)
            e.names_valid(profile['empty_directories'])
            if any(not n.startswith(self.prefixes) for n in protected_names + profile['empty_directories']):
                raise a.Error('Protected/empty path outside system profile')
        self.folder = e.canonical(folder, self.boundary)
        if self.folder == self.boundary or self.folder.is_relative_to(self.root / '.local-work/c1-cargo'):
            raise a.Error('Unsafe transaction workspace')
        self.binding = dict(root=str(self.root), plan_sha256=plan_sha, recovery_sha256=recovery_sha,
                            shadow_sha256=shadow_sha, index=str(store.index), index_sha256=store.index_sha,
                            archive_sha256=store.archive_sha, manifest_sha256=store.manifest_sha,
                            transaction=str(self.folder), empty_directories=sorted(self.empty_directories),
                            methods=methods(), **git_identity())
        if profile is not None:
            self.binding['profile'] = profile
            self.binding['system_methods'] = system_methods()
            self.binding['runtime'] = runtime_identity()

    def census(self, names, holds):
        if set(names) & {r['path'] for r in self.excluded}:
            raise a.Error('Protected exclusion in retirement allowlist')
        return census(self.root, names, holds, self.prefixes, self.empty_directories, self.excluded)

    def read_controls(self):
        return [e.authenticate(p, h, limit=self.control_limit) for p, h in self.controls]

    @contextlib.contextmanager
    def validated(self):
        with contextlib.ExitStack() as stack:
            for path, sha in self.controls:
                stack.enter_context(e.locked(path))
            plan, recovery, shadow = self.read_controls()
            entry, archive, members = stack.enter_context(self.store.authenticated(True))
            rows = plan['rows']
            names = [r['path'] for r in rows]
            scope(names, self.prefixes, self.hold_names)
            if (plan.get('schema') != 'sor-cargo-retirement/1' or plan.get('authority') != 'DELETION NOT AUTHORIZED' or
                    plan.get('index_sha256') != self.store.index_sha or plan.get('archive_sha256') != self.store.archive_sha or
                    set(names) != {r['path'] for r in entry['rows']} or
                    recovery.get('state') != 'RESTORED-TESTED' or recovery.get('members') != len(rows) or
                    any(recovery.get(k) != getattr(self.store, v) for k, v in (
                        ('index_sha256', 'index_sha'), ('archive_sha256', 'archive_sha'), ('manifest_sha256', 'manifest_sha')))):
                raise a.Error('Proposal/recovery/archive membership mismatch')
            before = a.rollback(shadow, shadow['before_sha256'])
            expected = a.migrate(before, names, self.store, shadow['before_sha256'])
            if shadow != expected:
                raise a.Error('Shadow baseline substitution')
            retired_names = set(names)
            holds = [r for r in before if r['path'] not in retired_names]
            if set(r['path'] for r in holds) != self.hold_names:
                raise a.Error('Exact profile loose holds required')
            for row in rows:
                if (any(row[k] != members[row['path']][k] for k in ('sha256', 'bytes')) or
                        row.get('member') != row['path'] or row.get('owner') != entry['owner'] or
                        row.get('index_sha256') != self.store.index_sha):
                    raise a.Error('Substituted allowlist row')
            yield rows, holds, shadow, archive

    def approval(self, path, sha):
        doc = e.authenticate(path, sha)
        if (set(doc) != {'schema', 'operation', 'binding', 'expires_utc', 'exclusive_ownership', 'maintainer_approval'} or
                doc['schema'] != 1 or doc['operation'] != self.operation or doc['binding'] != self.binding or
                doc['exclusive_ownership'] is not True or doc['maintainer_approval'] != 'SEPARATE EXPLICIT GO' or
                methods() != self.binding['methods'] or
                (self.profile is not None and system_methods() != self.binding['system_methods']) or
                (self.profile is not None and runtime_identity() != self.binding['runtime']) or
                dt.datetime.fromisoformat(doc['expires_utc']) <= dt.datetime.now(dt.timezone.utc) or
                git_identity() != {k: self.binding[k] for k in ('head', 'repo_index_sha256')}):
            raise a.Error('Absent, bogus or stale external authorization')
        return doc

    def execute(self, approval_path, approval_sha, fault=lambda event, path: None):
        """Separately authorized exact deletion; fault callbacks qualify disposable data.

        Fault callback is for qualification. No automatic rollback recreates
        originals. Missing intent sources may be reconciled only from a valid
        prefix and authenticated complete archive; unexplained absence blocks.
        """
        fs = e.c.create_unicode_buffer(32)
        if not e.K.GetVolumeInformationW(str(self.root.anchor), None, 0, None, None, None, fs, len(fs)):
            raise e.c.WinError(e.c.get_last_error())
        if fs.value != 'NTFS':
            raise a.Error('Unqualified filesystem deletion semantics; NTFS required')
        e.space(8 * 1024 * 1024)
        self.folder.mkdir(parents=True, exist_ok=True)
        lock = self.folder / 'RUNNING'
        # The kernel releases this exclusive handle on abrupt process exit.
        h = e.K.CreateFileW(str(lock), 0xC0000000, 0, None, 4, 0x00200000, None)
        if h == e.w.HANDLE(-1).value:
            raise e.c.WinError(e.c.get_last_error())
        try:
            with contextlib.ExitStack() as stack:
                stack.enter_context(e.locked(approval_path))
                approval = self.approval(approval_path, approval_sha)
                if self.profile is not None:
                    locked_paths = [a.ROOT / name for name in {**methods(), **system_methods()}]
                    locked_paths += git_guard_paths() + [Path(approval_path), Path(sys.executable)]
                    stack.enter_context(ancestors(locked_paths))
                    for path in locked_paths:
                        stack.enter_context(e.locked(path))
                    # Close the validation-to-lock race before any source action.
                    approval = self.approval(approval_path, approval_sha)
                rows, holds, shadow, archive = stack.enter_context(self.validated())
                paths = [self.root / r['path'] for r in rows + holds + list(self.excluded)]
                stack.enter_context(ancestors(paths + [self.folder / 'journal.jsonl', archive, self.store.index]))
                if set(p.name for p in self.folder.iterdir()) - {'RUNNING', 'journal.jsonl', 'baseline.json'}:
                    raise a.Error('Unknown transaction artifact; manual recovery required')
                log = Journal(self.folder / 'journal.jsonl', self.binding, writable=True, boundary=self.boundary)
                stack.callback(log.close)
                if log.state == 'COMMITTED':
                    raise a.Error('Already activated; use verify, never double activation')
                names = [r['path'] for r in rows]
                if log.completed != names[:len(log.completed)] or (log.pending and log.pending != names[len(log.completed)]):
                    raise a.Error('RECOVERY_REQUIRED: journal not exact allowlist prefix')
                present = self.census(names, holds)
                # Excluded historical saves/containers are namespace-protected
                # without opening their payloads for hashing or archival use.
                for excluded in self.excluded:
                    stream, info = stack.enter_context(e.locked(self.root / excluded['path']))
                    stat = os.fstat(stream.fileno())
                    if any(actual != excluded[key] for actual, key in (
                            (info.length, 'bytes'), (stat.st_ino, 'file_id'),
                            (stat.st_dev, 'device'), (stat.st_mtime_ns, 'mtime_ns'))):
                        raise a.Error('Protected exclusion identity changed before lock')
                if not {r['path'] for r in holds} <= present:
                    raise a.Error('Missing protected loose hold before retirement')
                allowed_missing = set(log.completed) | ({log.pending} if log.pending else set())
                if set(names) - present - allowed_missing or set(log.completed) & present:
                    raise a.Error('RECOVERY_REQUIRED: unexplained source presence/absence')
                locked = {}
                if self.profile is not None:
                    for row in rows:
                        if row['path'] in present:
                            with e.locked(self.root / row['path']) as (source, info):
                                checked(source, info, row)
                for row in (rows + holds if self.profile is None else holds):
                    if row['path'] in present:
                        f, info = stack.enter_context(e.locked(self.root / row['path'], delete=row['path'] in names))
                        checked(f, info, row, row['path'] in names)
                        locked[row['path']] = (f, info)
                e.space(8 * 1024 * 1024)
                if log.state is None:
                    if (self.folder / 'baseline.json').exists():
                        raise a.Error('Unjournaled baseline')
                    log.append('PREPARED')
                for row in rows[len(log.completed):]:
                    name = row['path']
                    if self.profile is None:
                        self.approval(approval_path, approval_sha)
                    elif dt.datetime.fromisoformat(approval['expires_utc']) <= dt.datetime.now(dt.timezone.utc):
                        raise a.Error('External approval expired; preserve journal')
                    # Locked archive/index/control objects cannot be replaced.
                    # Cargo reauthenticates per removal; resources retain the
                    # continuously locked, fully authenticated archive object.
                    if self.profile is None:
                        self.store.verify(False)
                    e.space(8 * 1024 * 1024)
                    # Open and verify before a new INTENT. Otherwise an external
                    # disappearance could be mistaken for our interrupted deletion.
                    with contextlib.ExitStack() as one_source:
                        current = None
                        if self.profile is not None and name in present:
                            fault('source-before-lock', name)
                            current = one_source.enter_context(e.locked(self.root / name, delete=True))
                            checked(current[0], current[1], row)
                        if log.pending is None:
                            log.append('INTENT', name)
                        fault('intent', name)
                        if current is not None:
                            f, info = current
                            self.remove_one(row, f, info, fault)
                        elif name in locked:
                            f, info = locked.pop(name)
                            self.remove_one(row, f, info, fault)
                    fault('deleted', name)
                    log.append('DONE', name)
                if log.state != 'RETIRED_PENDING_BASELINE':
                    log.append('RETIRED_PENDING_BASELINE')
                if self.census(names, holds) != {r['path'] for r in holds}:
                    raise a.Error('RECOVERY_REQUIRED: post-retirement population')
                self.store.verify(True)
                baseline = dict(schema='sor-cargo-active/1', binding=self.binding, before_sha256=shadow['before_sha256'],
                                rows=shadow['after'], retired=len(rows), journal_prefix=log.tail)
                destination = self.folder / 'baseline.json'
                fault('baseline-before', None)
                if destination.exists():
                    if e.authenticate(destination, digest(baseline)) != baseline:
                        raise a.Error('RECOVERY_REQUIRED: baseline conflict')
                else:
                    # Flush bytes, then same-volume write-through publication.
                    temporary = self.folder / 'baseline.writing'
                    with temporary.open('xb') as f:
                        f.write(e.encode(baseline))
                        f.flush()
                        os.fsync(f.fileno())
                    fault('baseline-writing', None)
                    if not e.K.MoveFileExW(str(temporary), str(destination), 8):
                        raise e.c.WinError(e.c.get_last_error())
                fault('baseline-after', None)
                log.append('COMMITTED')
                log.stream.seek(0)
                journal_sha = hashlib.file_digest(log.stream, 'sha256').hexdigest()
                return dict(state=log.state, retired=len(rows), baseline_sha256=digest(baseline), journal_sha256=journal_sha)
        finally:
            e.K.CloseHandle(h)

    def remove_one(self, row, stream, info, fault):
        """Retain the qualified same-handle checks and pending-link cancellation."""
        name = row['path']
        checked(stream, info, row)
        fault('locked', name)
        disposition(stream, True)
        fault('pending-delete', name)
        pending = standard(stream)
        if pending.links != 0 or not pending.pending:
            disposition(stream, False)
            if standard(stream).pending:
                raise a.Error('RECOVERY_REQUIRED: could not cancel disposition')
            raise a.Error('Concurrent hardlink alias; disposition cancelled')
        stream.close()
        if (self.root / name).exists():
            raise a.Error('RECOVERY_REQUIRED: deletion still pending')

    def verify(self, expected_baseline=None, include_members=False):
        """Routine committed check: archive/index and holds, no member hashes.

        Before a transaction use the existing preparer. Partial/missing journals
        never excuse missing loose sources. This does not change global policy.
        """
        if expected_baseline is None:
            raise a.Error('Independently retained committed baseline digest required')
        document = e.authenticate(self.folder / 'baseline.json', expected_baseline)
        binding = document['binding']
        stable = set(self.binding) - {'head', 'repo_index_sha256', 'methods', 'system_methods', 'runtime'}
        if any(binding[k] != self.binding[k] for k in stable):
            raise a.Error('Baseline scope/identity changed')
        log = Journal(self.folder / 'journal.jsonl', binding, boundary=self.boundary)
        try:
            return self._verify(document, binding, log, include_members)
        finally:
            log.close()

    def _verify(self, document, binding, log, include_members=False):
        if log.state != 'COMMITTED':
            raise a.Error('RECOVERY_REQUIRED: baseline transaction not committed')
        plan, _, shadow = self.read_controls()
        names = [r['path'] for r in plan['rows']]
        scope(names, self.prefixes, self.hold_names)
        if log.completed != names or log.pending:
            raise a.Error('Incomplete retired population')
        retired_names = set(names)
        holds = [r for r in shadow['before'] if r['path'] not in retired_names]
        baseline = dict(schema='sor-cargo-active/1', binding=binding, before_sha256=shadow['before_sha256'],
                        rows=shadow['after'], retired=len(names), journal_prefix=log.events[-1]['previous'])
        if document != baseline:
            raise a.Error('Baseline content mismatch')
        with self.store.authenticated(False) as (entry, archive, members):
            if self.census(names, holds) != {r['path'] for r in holds}:
                raise a.Error('Unexpected post-commit loose population')
            e.inspect(self.root, holds)
        result = dict(state='COMMITTED', retired=len(names), routine_member_hashes=0, routine_objects=2 + len(holds),
                      baseline_sha256=digest(baseline))
        if include_members:
            result['_archive_rows'] = entry['rows']
        return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation', choices=('verify', 'execute'))
    for name in ('root', 'plan', 'recovery', 'shadow', 'folder'):
        parser.add_argument('--' + name, type=Path, required=True)
    for name in ('plan', 'recovery', 'shadow'):
        parser.add_argument('--' + name + '-sha256', required=True)
    parser.add_argument('--approval', type=Path)
    parser.add_argument('--approval-sha256')
    parser.add_argument('--baseline-sha256')
    args = parser.parse_args()
    tx = Transaction(args.root, a.Store(), args.plan, args.plan_sha256, args.recovery, args.recovery_sha256,
                     args.shadow, args.shadow_sha256, args.folder)
    if args.operation == 'execute':
        if not args.approval or not args.approval_sha256:
            parser.error('Separate explicit maintainer approval and externally retained hash required')
        result = tx.execute(args.approval, args.approval_sha256)
    else:
        result = tx.verify(args.baseline_sha256)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
