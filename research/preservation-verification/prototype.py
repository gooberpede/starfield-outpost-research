# SPDX-License-Identifier: GPL-3.0-or-later
"""Isolated disposable-only verifier; no project policy activation.

Reads a frozen SQLite baseline, NTFS metadata and fixture bytes. Only baseline()
writes, exclusively under a caller-provided disposable directory. Verification
returns measurements or raises: it never repairs inputs or advances checkpoints.
Full mode is the safe default. Journal mode requires an explicit conditional
threat-model choice and cannot attest current historical bytes against bit rot.
"""
import hashlib
import json
from pathlib import Path
import sqlite3
import time
import zipfile

import journal

MARKER = 'SOR_DISPOSABLE_PRESERVATION_FIXTURE'


class IntegrityError(RuntimeError):
    pass


def sha(data):
    return hashlib.sha256(data).hexdigest()


def fixture_guard(root):
    root = Path(root).absolute()
    if not (root / MARKER).is_file() or root.is_symlink():
        raise IntegrityError('Explicit disposable fixture required')
    for p in (root, *root.parents):
        if p.lstat().st_file_attributes & 0x400:
            raise IntegrityError('Reparse ancestor')
    return root


def baseline(root):
    """Freeze synthetic leaf hashes, directories and critical inputs exactly once."""
    root = fixture_guard(root)
    target = root / 'baseline.sqlite'
    if target.exists():
        raise IntegrityError('Refuse baseline overwrite')
    cursor = journal.query(root.drive)
    db = sqlite3.connect(':memory:')
    db.execute('create table pins(path text primary key, digest text, bytes integer, frn text unique, category text)')
    count = nbytes = 0
    for kind in ('historical', 'scientific', 'critical'):
        folder = root / kind
        for p in [folder, *sorted(folder.rglob('*'))]:
            volume, frn = journal.identity(p)
            if p.is_file():
                data = p.read_bytes()
                digest, size = sha(data), len(data)
                count += 1
                nbytes += size
            else:
                digest, size = None, 0
            db.execute('insert into pins values(?,?,?,?,?)', (p.relative_to(root).as_posix(), digest, size, str(frn), kind))
    config = dict(root=str(root), identity=journal.identity(root), volume=root.drive,
                  cursor=cursor, schema=1)
    activity, _, _ = journal.read_since(root.drive,cursor)
    for frn,parent,usn,reason in activity:
        if db.execute("select path from pins where category='historical' and frn in (?,?) limit 1",
                      (str(frn),str(parent))).fetchone():
            raise IntegrityError('Historical mutation during baseline construction')
    db.execute('create table config(value text)')
    db.execute('insert into config values(?)', (json.dumps(config),))
    db.commit()
    data = db.serialize()
    db.close()
    with target.open('xb') as f:
        f.write(data)
    return dict(anchor=sha(data), payload_hashes=count, payload_bytes=nbytes,
                manifest_bytes=len(data), cursor=config['cursor'])


def verify(root, anchor, *, mode='full', inject=None):
    """Fail closed on any error; count payload and control-plane costs separately.

    legacy mode models D5G's two historical intake passes plus one post pass.
    Full and journal modes represent one pre/post pair; all fresh scientific and
    critical input hashes run twice. Fault callbacks exist only for qualification.
    """
    start = time.perf_counter()
    cpu = time.process_time()
    root = fixture_guard(root)
    if mode not in ('full', 'legacy', 'journal-conditional'):
        raise IntegrityError('Unknown mode')
    raw = (root / 'baseline.sqlite').read_bytes()
    if sha(raw) != anchor:
        raise IntegrityError('Baseline digest mismatch')
    db = sqlite3.connect(':memory:')
    try:
        db.deserialize(raw)
        cfg = json.loads(db.execute('select value from config').fetchone()[0])
        if cfg['schema'] != 1 or cfg['root'] != str(root) or tuple(cfg['identity']) != journal.identity(root):
            raise IntegrityError('Wrong baseline/root identity')
        control_seconds = time.perf_counter()-start
        counts = {k: dict(enumerations=0, logical_pin_visits=0, opens=0, hash_invocations=0, bytes_hashed=0, unique_files=0)
                  for k in ('historical', 'scientific', 'critical')}
        seen = {k: set() for k in counts}
        journal_rows = journal_bytes = 0
        historical_seconds = 0

        def historical_gate():
            nonlocal journal_rows, journal_bytes, historical_seconds
            gate_start = time.perf_counter()
            rows, size, checkpoint = journal.read_since(cfg['volume'], cfg['cursor'])
            journal_rows += len(rows)
            journal_bytes += size
            for frn, parent, usn, reason in rows:
                hit = db.execute("select path from pins where category='historical' and frn in (?,?) limit 1",
                                 (str(frn), str(parent))).fetchone()
                if hit:
                    raise IntegrityError('Journaled historical mutation: ' + hit[0])
            historical_seconds += time.perf_counter()-gate_start

        def scan(kind,namespace=True):
            nonlocal historical_seconds
            kind_start = time.perf_counter()
            expected = list(db.execute('select path,digest,bytes,frn from pins where category=?', (kind,)))
            if namespace:
                actual = [root / kind, *sorted((root / kind).rglob('*'))]
                counts[kind]['enumerations'] += len(actual)
                if {p.relative_to(root).as_posix() for p in actual} != {row[0] for row in expected}:
                    raise IntegrityError('Unexpected/missing path')
            for path, digest, size, frn in expected:
                counts[kind]['logical_pin_visits'] += 1
                p = root / path
                if str(journal.identity(p)[1]) != frn:
                    raise IntegrityError('Replaced file/directory identity: ' + path)
                if digest is None:
                    continue
                if inject:
                    inject(p)
                data = p.read_bytes()
                counts[kind]['opens'] += 1
                counts[kind]['hash_invocations'] += 1
                counts[kind]['bytes_hashed'] += len(data)
                seen[kind].add(path)
                if len(data) != size or sha(data) != digest:
                    raise IntegrityError('Payload identity mismatch: ' + path)
                if p.suffix == '.zip':
                    with zipfile.ZipFile(p) as archive:
                        if archive.testzip() is not None:
                            raise IntegrityError('Invalid archive')
            if kind == 'historical':
                historical_seconds += time.perf_counter()-kind_start
        if mode == 'journal-conditional':
            historical_gate()
        if mode == 'legacy':
            scan('historical',False)
        for phase in ('before','after'):
            for kind in counts:
                if kind == 'historical' and mode == 'journal-conditional':
                    continue
                scan(kind,namespace=(kind != 'historical' or mode != 'legacy' or phase == 'before'))
        if mode == 'journal-conditional':
            historical_gate()
        for kind in counts:
            counts[kind]['unique_files'] = len(seen[kind])
        return dict(mode=mode, counts=counts, control_bytes_hashed=len(raw),
                    control_hash_invocations=1, journal_rows=journal_rows, journal_bytes=journal_bytes,
                    wall_seconds=time.perf_counter()-start, cpu_seconds=time.process_time()-cpu,
                    historical_wall_seconds=historical_seconds+control_seconds,
                    current_historical_bytes_verified=(mode != 'journal-conditional'),
                    readable_historical_byte_coverage=(mode != 'journal-conditional'))
    finally:
        db.close()
