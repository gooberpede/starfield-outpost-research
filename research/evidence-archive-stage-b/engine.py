# SPDX-License-Identifier: GPL-3.0-or-later
"""Bounded Windows archival transactions, using owned Stage A path/tar validation.

Reads caller-pinned loose sources and archives; writes only fresh task outputs.
Retirement is a separate explicit operation, qualified on disposable inputs only.
Requires installed CPython 3.14 and its stdlib; no target or network operations.
"""
import contextlib
import ctypes as c
from ctypes import wintypes as w
import hashlib
import io
import json
import msvcrt
import os
from pathlib import Path
import stat
import sys
import tarfile
import time
import uuid

ROOT = Path(__file__).resolve().parents[2]
LOCAL = ROOT / '.local-work/evidence-archive-stage-b'
ARCHIVES = ROOT / '.local-work/research-archives'
sys.path.insert(0, str(ROOT / 'research/evidence-archive-discovery'))
import archive as prototype

# Reuse the strict decoder without weakening the historical module on disk.
prototype.SPACE = ROOT / '.local-work'
Error = prototype.ArchiveError
pin = prototype.pin
safe_name = prototype.safe_name
names_valid = prototype.names_valid
space = prototype.space
MANIFEST = 'ARCHIVE-MEMBERS.json'
K = c.WinDLL('kernel32', use_last_error=True)
K.CreateFileW.argtypes = [w.LPCWSTR, w.DWORD, w.DWORD, c.c_void_p, w.DWORD, w.DWORD, w.HANDLE]
K.CreateFileW.restype = w.HANDLE
K.CloseHandle.argtypes = [w.HANDLE]
K.GetFileInformationByHandleEx.argtypes = [w.HANDLE, c.c_int, c.c_void_p, w.DWORD]
K.SetFileInformationByHandle.argtypes = [w.HANDLE, c.c_int, c.c_void_p, w.DWORD]
K.MoveFileExW.argtypes = [w.LPCWSTR, w.LPCWSTR, w.DWORD]


class Standard(c.Structure):
    _fields_ = [('allocation', c.c_longlong), ('length', c.c_longlong),
                ('links', w.DWORD), ('pending', c.c_ubyte), ('directory', c.c_ubyte)]


class Streams(c.Structure):
    _fields_ = [('size', c.c_longlong), ('name', w.WCHAR * 296)]


K.FindFirstStreamW.argtypes = [w.LPCWSTR, c.c_int, c.c_void_p, w.DWORD]
K.FindFirstStreamW.restype = w.HANDLE
K.FindNextStreamW.argtypes = [w.HANDLE, c.c_void_p]
K.FindClose.argtypes = [w.HANDLE]


def canonical(path, boundary=None):
    path = Path(path).absolute()
    if boundary and not path.is_relative_to(Path(boundary).absolute()):
        raise Error('Outside declared boundary')
    for node in (path, *path.parents):
        if node.exists() or node.is_symlink():
            if node.lstat().st_file_attributes & 0x400:
                raise Error('Reparse path or ancestor')
    if path.resolve() != path:
        raise Error('Path alias or noncanonical spelling')
    return path


def output(path):
    path = canonical(path)
    if not any(path.is_relative_to(p) for p in (LOCAL, ARCHIVES)):
        raise Error('Outside task output roots')
    return path


def stream_check(path):
    info = Streams()
    handle = K.FindFirstStreamW(str(path), 0, c.byref(info), 0)
    if handle == w.HANDLE(-1).value:
        raise c.WinError(c.get_last_error())
    try:
        while True:
            if info.name != '::$DATA':
                raise Error('Alternate data stream excluded')
            if not K.FindNextStreamW(handle, c.byref(info)):
                if c.get_last_error() != 38:
                    raise c.WinError(c.get_last_error())
                break
    finally:
        K.FindClose(handle)


@contextlib.contextmanager
def locked(path, delete=False):
    """Deny concurrent write/delete sharing; hash and delete the same file handle."""
    path = canonical(path)
    handle = K.CreateFileW(str(path), 0x80000000 | (0x10000 if delete else 0),
                           1, None, 3, 0x00200000, None)
    if handle == w.HANDLE(-1).value:
        raise c.WinError(c.get_last_error())
    try:
        info = Standard()
        if not K.GetFileInformationByHandleEx(handle, 1, c.byref(info), c.sizeof(info)):
            raise c.WinError(c.get_last_error())
        if info.links != 1 or info.directory:
            raise Error('Hardlink or nonregular source excluded')
        stream_check(path)
        fd = msvcrt.open_osfhandle(handle, os.O_RDONLY | os.O_BINARY)
    except BaseException:
        K.CloseHandle(handle)
        raise
    with os.fdopen(fd, 'rb') as f:
        if not stat.S_ISREG(os.fstat(f.fileno()).st_mode):
            raise Error('Not a regular file')
        yield f, info


def encode(value):
    return (json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False) + '\n').encode('utf8')


def durable(path, data, replace=False):
    space(len(data)*2 + 1024*1024)
    path = output(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not replace:
        raise Error('Refuse existing output')
    temporary = path.with_name(path.name + '.writing-' + uuid.uuid4().hex)
    with temporary.open('xb') as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())
    publish(temporary,path,replace)


def publish(source, target, replace=False):
    """Request Windows write-through namespace publication on the same volume.

    fsync covers file data beforehand. Device/controller honesty and actual
    power-loss survival are outside the disposable process-interruption tests.
    """
    source, target = output(source), output(target)
    if source.drive != target.drive or (target.exists() and not replace):
        raise Error('Publication must be same-volume and no-clobber')
    if not K.MoveFileExW(str(source),str(target),8 | (1 if replace else 0)):
        raise c.WinError(c.get_last_error())


def record(path, value, replace=False):
    durable(path, encode(value), replace)


def authenticate(path, expected, limit=64 * 1024 * 1024):
    with locked(path) as (f, info):
        if info.length > limit:
            raise Error('Control document size bound')
        raw = f.read()
    if hashlib.sha256(raw).hexdigest() != expected:
        raise Error('Independent control digest mismatch')
    return json.loads(raw)


def inspect(root, rows):
    names_valid([r['path'] for r in rows])
    result = []
    for row in rows:
        path = canonical(Path(root) / str(safe_name(row['path'])), root)
        with locked(path) as (f, info):
            digest = hashlib.file_digest(f, 'sha256').hexdigest()
            if digest != row['sha256'] or info.length != row['bytes']:
                raise Error('Frozen source mismatch: ' + row['path'])
            result.append(dict(row, verified_sha256=digest, allocated_bytes=info.allocation))
    return result


def expected_members(rows):
    manifest = encode(rows)
    members = {r['path']: dict(sha256=r['sha256'], bytes=r['bytes']) for r in rows}
    members[MANIFEST] = dict(sha256=hashlib.sha256(manifest).hexdigest(), bytes=len(manifest))
    return members, manifest


def checkpoint(folder, state, **values):
    record(Path(folder) / 'journal.json', dict(state=state, **values), replace=True)


def build(root, rows, folder, fault=None, index_path=None, cross_references=None,
          owner='cargo-transport-fuel'):
    """Fresh transaction only; interrupted artifacts are never implicitly trusted."""
    folder = output(folder)
    if folder.exists():
        raise Error('Fresh transaction required; use recovery inspection after interruption')
    total = sum(r['bytes'] for r in rows)
    capacity = space(total * 4 + len(rows) * 32768 + 32 * 1024 * 1024)
    # Every included source is hashed under its own lock below. Preserve the
    # Cargo prepass; the larger system uses its separately frozen admission.
    if owner == 'cargo-transport-fuel':
        inspect(root, rows)
    else:
        names_valid([r['path'] for r in rows])
    folder.mkdir(parents=True)
    checkpoint(folder, 'PREPARED', source_manifest_sha256=hashlib.sha256(encode(rows)).hexdigest())
    members, manifest = expected_members(rows)
    safe_name(owner)
    if '/' in owner:
        raise Error('Owner must be one path component')
    partial = folder / (owner + '.tar.zst.partial')
    start = time.perf_counter()
    with partial.open('xb') as target:
        with tarfile.open(fileobj=target, mode='w:zst', format=tarfile.PAX_FORMAT, level=3) as tar:
            for ordinal, row in enumerate(sorted(rows, key=lambda r: r['path'])):
                with locked(Path(root) / row['path']) as (source, info):
                    if info.length != row['bytes']:
                        raise Error('Changed source size')
                    digest = hashlib.file_digest(source, 'sha256').hexdigest()
                    if digest != row['sha256']:
                        raise Error('Changed source bytes')
                    source.seek(0)
                    item = tarfile.TarInfo(row['path'])
                    item.size = row['bytes']
                    item.mode = 0o600
                    tar.addfile(item, source)
                if fault == 'creation' and ordinal == 0:
                    raise Error('Injected creation interruption')
                if fault == 'process-exit' and ordinal == 0:
                    os._exit(73)
                if owner != 'cargo-transport-fuel' and (ordinal + 1) % 5000 == 0:
                    checkpoint(folder, 'PACKING', admitted=ordinal + 1,
                               total=len(rows), free=space())
                    print('Packed', ordinal + 1, 'of', len(rows), flush=True)
            item = tarfile.TarInfo(MANIFEST)
            item.size = len(manifest)
            item.mode = 0o600
            tar.addfile(item, io.BytesIO(manifest))
        target.flush()
        os.fsync(target.fileno())
    creation_seconds = time.perf_counter() - start
    verification_start = time.perf_counter()
    prototype.stream_members(partial, 'tar.zst', members)
    digest = pin(partial)
    if fault == 'before-publication':
        raise Error('Injected prepublication interruption')
    archive = partial.with_suffix('')
    publish(partial,archive)
    if fault == 'after-publication':
        raise Error('Injected postpublication interruption')
    index_path = output(index_path or folder/'index.json')
    index = dict(owner=owner, state='VERIFIED',
                 archive=archive.relative_to(index_path.parent).as_posix(), archive_sha256=digest, archive_bytes=archive.stat().st_size,
                 manifest_sha256=hashlib.sha256(manifest).hexdigest(), rows=rows,
                 exclusions='See frozen retain-loose inventory and decision card')
    central = dict(schema=2, archives={owner:index}, cross_references=cross_references or [])
    record(index_path, central)
    anchor = pin(index_path)
    checkpoint(folder, 'VERIFIED', index_sha256=anchor)
    return dict(index_sha256=anchor, archive_sha256=digest, manifest_sha256=index['manifest_sha256'],
                source_files=len(rows), archive_members=len(members), source_bytes=total,
                archive_bytes=index['archive_bytes'], index_bytes=index_path.stat().st_size,
                creation_seconds=creation_seconds, verification_seconds=time.perf_counter()-verification_start,
                before_free=capacity, after_free=space())


def load(index_path, anchor, owner='cargo-transport-fuel'):
    index_path = output(index_path)
    central = authenticate(index_path, anchor)
    if central.get('schema') != 2 or set(central) != {'schema','archives','cross_references'}:
        raise Error('Unsupported central index schema')
    originals = []
    for archive_owner, entry in central['archives'].items():
        if archive_owner != entry['owner']:
            raise Error('Archive owner mismatch')
        for row in entry['rows']:
            originals.append(row['path'])
    names_valid(originals)
    for ref in central['cross_references']:
        referenced_owner = central['archives'].get(ref['owner'])
        if referenced_owner is None or ref['path'] not in {r['path'] for r in referenced_owner['rows']}:
            raise Error('Unresolved cross-system reference')
    j = central['archives'][owner]
    if j.get('owner') != owner or j.get('state') != 'VERIFIED':
        raise Error('Unsupported index identity or state')
    rows = j['rows']
    if not rows or len(rows) > 300000:
        raise Error('Index cardinality')
    names_valid([r['path'] for r in rows])
    if any(r['bytes'] < 0 or len(r['sha256']) != 64 for r in rows):
        raise Error('Invalid member expectation')
    members, manifest = expected_members(rows)
    if hashlib.sha256(manifest).hexdigest() != j['manifest_sha256']:
        raise Error('Manifest mismatch')
    safe_name(j['archive'])
    archive = output(index_path.parent / j['archive'])
    canonical(archive,index_path.parent)
    return j, archive, members


@contextlib.contextmanager
def verified(index_path, anchor, owner='cargo-transport-fuel'):
    # Hold both objects against replacement for the complete operation.
    with locked(index_path):
        j, archive, members = load(index_path, anchor, owner)
        with locked(archive) as (f, info):
            if info.length != j['archive_bytes'] or hashlib.file_digest(f, 'sha256').hexdigest() != j['archive_sha256']:
                raise Error('Archive identity mismatch')
            prototype.stream_members(archive, 'tar.zst', members)
            yield j, archive, members


def restore(index_path, anchor, destination, fault=False, owner='cargo-transport-fuel'):
    start = time.perf_counter()
    destination = output(destination)
    if destination.exists():
        raise Error('Restore destination exists')
    with verified(index_path, anchor, owner) as (j, archive, members):
        capacity = space(sum(r['bytes'] for r in members.values()) + len(members)*32768 + 32*1024*1024)
        partial = destination.with_name(destination.name + '.partial-' + uuid.uuid4().hex)
        partial.mkdir(parents=True)
        def sink(name):
            p = output(partial / safe_name(name))
            p.parent.mkdir(parents=True, exist_ok=True)
            stream = p.open('xb')
            class Flushed:
                def write(self, data):
                    return stream.write(data)
                def close(self):
                    try:
                        stream.flush()
                        os.fsync(stream.fileno())
                    finally:
                        stream.close()
            return Flushed()
        prototype.stream_members(archive, 'tar.zst', members, sink)
        # A separate reread verifies all restored bytes and regular-file safety.
        for name, row in members.items():
            with locked(partial / name) as (f, info):
                if info.length != row['bytes'] or hashlib.file_digest(f, 'sha256').hexdigest() != row['sha256']:
                    raise Error('Restored reread mismatch')
        if fault:
            raise Error('Injected restore interruption')
        publish(partial,destination)
    return dict(files=len(members), payload_bytes=sum(r['bytes'] for r in members.values()),
                wall_seconds=time.perf_counter()-start, before_free=capacity, after_free=space(),
                destination=str(destination), all_reread_equal=True)


def recover(folder, anchor=None):
    folder = output(folder)
    # Journal is diagnostic, never an authenticity oracle.
    if not anchor:
        return dict(state='QUARANTINED', reason='Independent index anchor required; start a fresh transaction')
    with verified(folder/'index.json', anchor):
        return dict(state='VERIFIED', reason='Reauthenticated index, archive and every member; no implicit deletion')


def retire(root, index_path, anchor, manifest_path, approved_manifest, *, execute=False, fault=None):
    """Explicit allowlist only, with per-file reauthentication and write-ahead state.

    Real operation requires separate human approval; never call from pilot build.
    Missing sources stop retry even when a journal reports retirement intent.
    Exclusive-writer ownership of ancestor directories is a required precondition.
    """
    manifest_path = output(manifest_path)
    plan = authenticate(manifest_path, approved_manifest)
    if plan.get('schema') != 1 or plan.get('index_sha256') != anchor:
        raise Error('Manifest/index binding')
    journal_path = manifest_path.parent / 'retirement.json'
    log = dict(manifest_sha256=approved_manifest, pending=[], completed=[], state='AWAITING-APPROVAL')
    if journal_path.exists():
        log = json.loads(journal_path.read_text())
        if log['manifest_sha256'] != approved_manifest:
            raise Error('Retirement resume identity mismatch')
    names_valid([r['path'] for r in plan['rows']])
    with verified(index_path, anchor) as (index, archive, members):
        for row in plan['rows']:
            if row['path'] not in members or any(row[k] != members[row['path']][k] for k in ('sha256','bytes')):
                raise Error('Allowlist outside authenticated membership')
    # Authenticate all still-present sources before the first removal.
    for row in plan['rows']:
        p = canonical(Path(root)/safe_name(row['path']), root)
        if p.exists():
            inspect(root, [row])
        else:
            raise Error('Unexpected missing source')
    if not execute:
        return dict(state='AWAITING-APPROVAL', files=len(plan['rows']), deleted=0,
                    expected_allocated_bytes=sum(r['allocated_bytes'] for r in plan['rows']))
    for ordinal, row in enumerate(plan['rows']):
        space(len(encode(log))*2 + len(encode(plan))*2 + 2*1024*1024)
        # Reverify immediately before each removal, even on resume.
        with verified(index_path, anchor):
            p = canonical(Path(root)/row['path'], root)
            if row['path'] not in log['pending']:
                log['pending'].append(row['path'])
                log['state'] = 'RETIRING'
                record(journal_path, log, replace=True)
            if p.exists():
                with locked(p, delete=True) as (f, info):
                    if info.length != row['bytes'] or hashlib.file_digest(f, 'sha256').hexdigest() != row['sha256']:
                        raise Error('Changed source immediately before retirement')
                    disposition = c.c_ubyte(1)
                    if not K.SetFileInformationByHandle(msvcrt.get_osfhandle(f.fileno()), 4,
                                                       c.byref(disposition), c.sizeof(disposition)):
                        raise c.WinError(c.get_last_error())
            else:
                raise Error('Source disappeared immediately before retirement')
            if fault == ordinal:
                raise Error('Injected interruption after deletion, before completion checkpoint')
            if row['path'] not in log['completed']:
                log['completed'].append(row['path'])
            record(journal_path, log, replace=True)
    with verified(index_path, anchor):
        if any((Path(root)/r['path']).exists() for r in plan['rows']):
            raise Error('Postflight source remains')
    log['state'] = 'COMPLETED'
    record(journal_path, log, replace=True)
    return log


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation', choices=['restore','dry-run','retire'])
    parser.add_argument('--index', type=Path, required=True)
    parser.add_argument('--index-sha256', required=True)
    parser.add_argument('--destination', type=Path)
    parser.add_argument('--manifest', type=Path)
    parser.add_argument('--approved-manifest-sha256')
    parser.add_argument('--execute-retirement', action='store_true')
    args = parser.parse_args()
    if args.operation == 'restore':
        if not args.destination:
            parser.error('Explicit fresh destination required')
        result = restore(args.index,args.index_sha256,args.destination)
    else:
        if not args.manifest or not args.approved_manifest_sha256:
            parser.error('Exact manifest and independent digest required')
        if args.operation == 'retire' and not args.execute_retirement:
            parser.error('Separate human authorization and explicit execution switch required')
        result = retire(ROOT,args.index,args.index_sha256,args.manifest,args.approved_manifest_sha256,
                        execute=args.operation=='retire')
    print(json.dumps(result,indent=2))
