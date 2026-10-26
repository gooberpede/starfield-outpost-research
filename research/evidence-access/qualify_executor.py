# SPDX-License-Identifier: GPL-3.0-or-later
"""Disposable Windows retirement fault matrix; never executes on real sources.

Creates tiny synthetic archives via the owned Stage B builder. Writes fixtures,
approval controls, transaction journals and retained case receipts below ignored
Cargo/Stage B roots. Synthetic approvals explicitly bind only replica roots.
The separate replica command handles real-byte consumer reproduction.
"""
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from unittest.mock import patch
import uuid
import shutil

import executor as x

a, e = x.a, x.e
REJECTIONS = []


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(e.encode(value))
    return e.pin(path)


def snapshot(base):
    paths = [a.ROOT / p for p in x.methods()] + [Path(__file__), Path(__file__).with_name('replica_executor.py')]
    rows = []
    for p in paths:
        target = base / 'executed-methods' / p.relative_to(a.ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(p, target)
        rows.append(dict(path=str(p), sha256=e.pin(p), snapshot=str(target)))
    save(base / 'executed-methods.json', dict(rows=rows, python=sys.version, executable=sys.executable,
                                            executable_sha256=e.pin(sys.executable), git=x.git_identity()))
    return rows


def unchanged(rows):
    assert all(e.pin(r['path']) == r['sha256'] == e.pin(r['snapshot']) for r in rows)


def approve(tx, path):
    return save(path, dict(schema=1, operation=x.OPERATION, binding=tx.binding,
                          expires_utc=(dt.datetime.now(dt.timezone.utc) + dt.timedelta(hours=8)).isoformat(),
                          exclusive_ownership=True, maintainer_approval='SEPARATE EXPLICIT GO'))


def controls(root, store, base, rows=None):
    with store.authenticated(True) as (entry, _, _):
        rows = entry['rows'] if rows is None else rows
        planned = []
        for row in rows:
            st = (root / row['path']).stat()
            planned.append(dict(path=row['path'], member=row['path'], owner=entry['owner'],
                                index_sha256=store.index_sha, bytes=row['bytes'], sha256=row['sha256'],
                                device=st.st_dev, file_id=st.st_ino))
    holds = []
    for name in sorted(x.HOLDS):
        p = root / name
        p.parent.mkdir(parents=True, exist_ok=True)
        if not p.exists():
            p.write_bytes(b'held-version')
        holds.append(dict(path=name, bytes=p.stat().st_size, sha256=e.pin(p)))
    plan = dict(schema='sor-cargo-retirement/1', authority='DELETION NOT AUTHORIZED',
                index_sha256=store.index_sha, archive_sha256=store.archive_sha, rows=planned)
    recovery = dict(state='RESTORED-TESTED', members=len(rows), index_sha256=store.index_sha,
                    archive_sha256=store.archive_sha, manifest_sha256=store.manifest_sha)
    before = [dict(path=r['path'], bytes=r['bytes'], sha256=r['sha256']) for r in rows] + holds
    shadow = a.migrate(before, [r['path'] for r in rows], store, x.digest(before))
    ps = save(base / 'plan.json', plan)
    rs = save(base / 'recovery.json', recovery)
    ss = save(base / 'shadow.json', shadow)
    tx = x.Transaction(root, store, base / 'plan.json', ps, base / 'recovery.json', rs,
                       base / 'shadow.json', ss, base / 'tx')
    approval = base / 'approval.json'
    sha = approve(tx, approval)
    return tx, approval, sha


def fixture(base, name):
    folder = e.LOCAL / ('retirement-' + base.name) / name
    root = folder / 'sources'
    rows = []
    for i, prefix in enumerate(x.PREFIXES):
        p = root / prefix / 'payload.txt'
        p.parent.mkdir(parents=True)
        p.write_bytes(('synthetic-%d' % i).encode() * 100)
        rows.append(dict(path=p.relative_to(root).as_posix(), bytes=p.stat().st_size, sha256=e.pin(p)))
    built = e.build(root, rows, folder / 'archive')
    store = a.Store(folder / 'archive/index.json', built['index_sha256'], built['archive_sha256'], built['manifest_sha256'])
    return controls(root, store, base / name)


def rejected(fn):
    try:
        fn()
    except (a.Error, OSError, ValueError, KeyError, TypeError, IndexError) as exc:
        REJECTIONS.append(repr(exc))
        return
    raise AssertionError('Expected fail-closed result')


def routine_probe(tx):
    baseline = tx.folder / 'baseline.json'
    return tx.verify(e.pin(baseline) if baseline.exists() else '0' * 64)


def main():
    e.space(128 * 1024 * 1024)
    base = x.LOCAL / ('qualification-' + uuid.uuid4().hex)
    base.mkdir(parents=True)
    source_pins = snapshot(base)
    results = []

    def case(name, fn):
        REJECTIONS.clear()
        try:
            detail = fn()
            results.append(dict(case=name, status='PASS', detail=detail, rejected=list(REJECTIONS)))
        except Exception as ex:
            results.append(dict(case=name, status='FAIL', error=repr(ex)))
        save(base / 'results.json', results)

    def normal():
        tx, ap, sha = fixture(base, 'normal')
        rejected(lambda: routine_probe(tx))
        result = tx.execute(ap, sha)
        assert result['state'] == 'COMMITTED'
        assert tx.verify(result['baseline_sha256'])['routine_member_hashes'] == 0
        rejected(lambda: tx.execute(ap, sha))
        return result
    case('exact normal retirement; before/after baseline; double activation', normal)

    for event in ('intent', 'deleted', 'baseline-before', 'baseline-after'):
        def interrupted(event=event):
            tx, ap, sha = fixture(base, 'stop-' + event)
            def fault(ev, name):
                if ev == event:
                    raise a.Error('Injected interruption')
            rejected(lambda: tx.execute(ap, sha, fault))
            rejected(lambda: routine_probe(tx))
            if event == 'baseline-after':
                assert 'not committed' in REJECTIONS[-1]
            # Recreate manager from externally held inputs, not in-memory state.
            tx2 = x.Transaction(tx.root, tx.store, *sum(([p, h] for p, h in tx.controls), []), tx.folder)
            result = tx2.execute(ap, sha)
            assert result['state'] == 'COMMITTED'
            return tx2.verify(result['baseline_sha256'])
        case('restart/replay after ' + event, interrupted)

    for kind in ('source', 'inode', 'extra', 'missing', 'hardlink', 'plan', 'recovery', 'shadow',
                 'index', 'archive', 'inventory', 'approval', 'stale', 'protected', 'unknown-cleanup', 'missing-hold', 'readonly', 'empty-directory'):
        def tamper(kind=kind):
            tx, ap, sha = fixture(base, 'tamper-' + kind)
            all_rows = json.loads(tx.controls[0][0].read_text())['rows']
            row = all_rows[0]
            source = tx.root / row['path']
            if kind == 'source':
                source.write_bytes(b'bad')
            elif kind == 'inode':
                data = source.read_bytes()
                source.rename(source.with_suffix('.old'))
                source.write_bytes(data)
                source.with_suffix('.old').unlink()
            elif kind == 'extra':
                source.with_name('unknown.bin').write_bytes(b'?')
            elif kind == 'empty-directory':
                source.with_name('unknown-empty').mkdir()
            elif kind == 'missing':
                source.unlink()
            elif kind == 'missing-hold':
                (tx.root / sorted(x.HOLDS)[0]).unlink()
            elif kind == 'readonly':
                source.chmod(0o444)
            elif kind == 'hardlink':
                os.link(source, tx.root / 'alias')
            elif kind in ('plan', 'recovery', 'shadow'):
                tx.controls[('plan', 'recovery', 'shadow').index(kind)][0].write_bytes(b'{}')
            elif kind == 'index':
                tx.store.index.write_bytes(b'{}')
            elif kind == 'archive':
                _, archive, _ = e.load(tx.store.index, tx.store.index_sha)
                archive.write_bytes(b'bad')
            elif kind == 'inventory':
                tx.store.manifest_sha = '0' * 64
            elif kind == 'approval':
                ap.write_bytes(b'{}')
            elif kind == 'stale':
                doc = json.loads(ap.read_text())
                doc['expires_utc'] = '2000-01-01T00:00:00+00:00'
                sha = save(ap, doc)
            elif kind == 'protected':
                rejected(lambda: x.scope(['.local-work/protected/save.sfs']))
                return 'Non-Cargo path rejected before filesystem access'
            else:
                tx.folder.mkdir()
                (tx.folder / 'unknown.sfs').write_bytes(b'unknown')
            before_sources = {r['path']: e.pin(tx.root / r['path']) if (tx.root / r['path']).exists() else None for r in all_rows}
            rejected(lambda: tx.execute(ap, sha))
            assert not (tx.folder / 'baseline.json').exists()
            after_sources = {r['path']: e.pin(tx.root / r['path']) if (tx.root / r['path']).exists() else None for r in all_rows}
            assert before_sources == after_sources, 'Admission failure removed or altered a source'
        case('reject ' + kind, tamper)

    def disk():
        tx, ap, sha = fixture(base, 'disk')
        with patch.object(e, 'space', side_effect=a.Error('disk guard')):
            rejected(lambda: tx.execute(ap, sha))
        assert all((tx.root / p['path']).exists() for p in json.loads(tx.controls[0][0].read_text())['rows'])
    case('disk guard before journal or delete', disk)

    def race():
        tx, ap, sha = fixture(base, 'race')
        attempted = []
        def fault(ev, name):
            if ev == 'locked':
                rejected(lambda: (tx.root / name).write_bytes(b'concurrent mutation'))
                rejected(lambda: (tx.root / name).unlink())
                rejected(lambda: (tx.root / name).parent.rename((tx.root / name).parent.with_name('moved')))
                attempted.append(name)
        result = tx.execute(ap, sha, fault)
        assert len(attempted) == 5
        tx.verify(result['baseline_sha256'])
        return attempted
    case('actual Windows concurrent write/delete/ancestor rename denied', race)

    def torn():
        tx, ap, sha = fixture(base, 'torn')
        rejected(lambda: tx.execute(ap, sha, lambda ev, name: (_ for _ in ()).throw(a.Error('stop')) if ev == 'deleted' else None))
        with (tx.folder / 'journal.jsonl').open('ab') as f:
            f.write(b'{"torn":')
        rejected(lambda: tx.execute(ap, sha))
        rejected(lambda: routine_probe(tx))
        return 'RECOVERY_REQUIRED; torn tail preserved, no automatic truncation'
    case('interrupted journal write blocks safe commitment', torn)

    def baseline_write():
        tx, ap, sha = fixture(base, 'baseline-writing')
        def fault(ev, name):
            if ev == 'baseline-writing':
                raise PermissionError('simulated publication IO failure')
        rejected(lambda: tx.execute(ap, sha, fault))
        rejected(lambda: tx.execute(ap, sha))
        rejected(lambda: routine_probe(tx))
        return 'Complete retired archive retained; unpublished baseline requires explicit reconciliation'
    case('baseline IO failure with unknown temporary file blocks', baseline_write)

    def lost():
        tx, ap, sha = fixture(base, 'archive-loss')
        def fault(ev, name):
            if ev == 'deleted':
                raise a.Error('stop after one deletion')
        rejected(lambda: tx.execute(ap, sha, fault))
        _, archive, _ = e.load(tx.store.index, tx.store.index_sha)
        archive.unlink()
        rejected(lambda: tx.execute(ap, sha))
        rejected(lambda: routine_probe(tx))
        return 'RECOVERY_REQUIRED; one removed synthetic payload irrecoverable without external copy'
    case('genuine single-archive loss cannot restore or commit', lost)

    def junction():
        tx, ap, sha = fixture(base, 'junction')
        source = tx.root / '.local-work/c1-cargo'
        other = tx.root / 'outside'
        source.rename(other)
        cmd = subprocess.run(['cmd', '/c', 'mklink', '/J', str(source), str(other)], capture_output=True)
        assert cmd.returncode == 0
        rejected(lambda: tx.execute(ap, sha))
    case('reparse namespace escape rejected', junction)

    def abrupt():
        tx, ap, sha = fixture(base, 'abrupt')
        config = dict(root=str(tx.root), index=str(tx.store.index), index_sha=tx.store.index_sha,
                      archive_sha=tx.store.archive_sha, manifest_sha=tx.store.manifest_sha,
                      controls=[(str(p), h) for p, h in tx.controls], folder=str(tx.folder), ap=str(ap), sha=sha)
        save(base / 'child.json', config)
        child = subprocess.run([sys.executable, '-B', __file__, '--child', str(base / 'child.json')], capture_output=True)
        assert child.returncode == 73, child.stderr
        rejected(lambda: routine_probe(tx))
        result = tx.execute(ap, sha)
        assert result['state'] == 'COMMITTED'
        return tx.verify(result['baseline_sha256'])
    case('abrupt process exit after delete and fresh process replay', abrupt)

    def hardlink_race():
        tx, ap, sha = fixture(base, 'hardlink-race')
        original = []
        def fault(ev, name):
            if ev == 'locked':
                original.append(tx.root / name)
                os.link(tx.root / name, tx.root / 'concurrent-alias')
        rejected(lambda: tx.execute(ap, sha, fault))
        assert original[0].exists()
        assert not (tx.folder / 'baseline.json').exists()
        return 'Disposition cancellation preserves original after a new hardlink'
    case('actual hardlink race cancels disposition and blocks', hardlink_race)

    def pending_link():
        tx, ap, sha = fixture(base, 'pending-link')
        attempts = []
        def fault(ev, name):
            if ev == 'pending-delete':
                rejected(lambda: os.link(tx.root / name, tx.root / 'alias'))
                attempts.append(name)
        tx.execute(ap, sha, fault)
        assert len(attempts) == 5
        return 'NTFS blocks new link through delete-pending original'
    case('actual link admission after disposition denied', pending_link)

    def journal_race():
        tx, ap, sha = fixture(base, 'journal-race')
        attempts = []
        def fault(ev, name):
            if ev == 'locked':
                rejected(lambda: (tx.folder / 'journal.jsonl').write_bytes(b'{}\n'))
                rejected(lambda: (tx.folder / 'journal.jsonl').unlink())
                attempts.append(name)
        result = tx.execute(ap, sha, fault)
        assert len(attempts) == 5
        return tx.verify(result['baseline_sha256'])
    case('actual journal write/replace denied throughout execution', journal_race)

    def method_change():
        tx, ap, sha = fixture(base, 'method-change')
        with patch.object(x, 'methods', return_value={'changed': '0' * 64}):
            rejected(lambda: tx.execute(ap, sha))
    case('transitive method change invalidates approval', method_change)

    def future_head():
        tx, ap, sha = fixture(base, 'future-head')
        result = tx.execute(ap, sha)
        with patch.object(x, 'git_identity', return_value=dict(head='later-unrelated-head', repo_index_sha256='later-index')):
            tx2 = x.Transaction(tx.root, tx.store, *sum(([p, h] for p, h in tx.controls), []), tx.folder)
            assert tx2.verify(result['baseline_sha256'])['state'] == 'COMMITTED'
    case('routine pinned baseline survives unrelated later HEAD/index', future_head)

    unchanged(source_pins)
    print(json.dumps(dict(directory=str(base), passed=sum(r['status'] == 'PASS' for r in results), total=len(results)), indent=2))
    return 1 if any(r['status'] != 'PASS' for r in results) else 0


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--child':
        cfg = json.loads(Path(sys.argv[2]).read_text())
        st = a.Store(cfg['index'], cfg['index_sha'], cfg['archive_sha'], cfg['manifest_sha'])
        tx = x.Transaction(Path(cfg['root']), st, *sum(([Path(p), h] for p, h in cfg['controls']), []), Path(cfg['folder']))
        tx.execute(Path(cfg['ap']), cfg['sha'], lambda ev, name: os._exit(73) if ev == 'deleted' else None)
    else:
        raise SystemExit(main())
