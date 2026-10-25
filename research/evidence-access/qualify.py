# SPDX-License-Identifier: GPL-3.0-or-later
"""Adversarial tests on fresh disposable fixtures only; preserves every result.

Uses stdlib, owned Stage B synthetic packager and Windows APIs. Modifies/deletes
only self-created synthetic files, never real Cargo members or protected inputs.
"""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from unittest.mock import patch
import uuid

import access as a
import retirement as r


def main():
    a.e.space(128 * 1024 * 1024)
    label = uuid.uuid4().hex
    base = a.LOCAL / ('qualification-' + label)
    source_base = a.e.LOCAL / ('access-fixtures-' + label)
    base.mkdir(parents=True)
    source_base.mkdir()
    results = []

    def case(name, fn):
        try:
            fn()
            results.append(dict(name=name, status='PASS'))
        except Exception as exc:
            results.append(dict(name=name, status='FAIL', error=repr(exc)))
        a.write(base / ('case-%02d.json' % len(results)), results[-1])

    def rejected(fn):
        try:
            fn()
        except (a.Error, OSError, ValueError, KeyError, TypeError):
            return
        raise AssertionError('Expected fail-closed rejection')

    def fixture(name):
        folder = source_base / name
        root = folder / 'sources'
        root.mkdir(parents=True)
        rows = []
        for n, data in (('.local-work/c1-cargo/a', b'alpha' * 200),
                        ('.local-work/c1-cargo/sub/b', b'beta'),
                        ('.local-work/c2-transport/zero', b'')):
            p = root / n
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(data)
            rows.append(dict(path=n, sha256=hashlib.sha256(data).hexdigest(), bytes=len(data)))
        built = a.e.build(root, rows, folder / 'archive')
        store = a.Store(folder / 'archive/index.json', built['index_sha256'],
                        built['archive_sha256'], built['manifest_sha256'])
        return root, rows, store

    root, rows, store = fixture('good')
    names = [x['path'] for x in rows]
    case('deep archive and embedded inventory', lambda: store.verify())
    case('routine hashes zero members', lambda: equal(store.verify(False)['member_hashes'], 0))
    case('locate exact loose identity', lambda: equal(store.locate(names[0], root)['loose'], True))
    case('missing member rejected', lambda: rejected(lambda: store.locate('unknown', root)))
    case('wrong original spelling rejected', lambda: rejected(lambda: store.locate(names[0].upper(), root)))
    case('wrong external index', lambda: rejected(lambda: a.Store(store.index, '0'*64).verify()))
    case('wrong external archive', lambda: rejected(lambda: a.Store(store.index, store.index_sha, '0'*64).verify()))
    case('wrong external inventory', lambda: rejected(lambda: a.Store(store.index, store.index_sha, store.archive_sha, '0'*64).verify()))
    receipt = store.restore(base / 'selected', [names[0]])
    case('selected bytes and no extra extraction', lambda: equal(len(a.lease_rows(base/'selected', receipt['lease_sha256'])['rows']), 1))
    case('restore overwrite rejected', lambda: rejected(lambda: store.restore(base/'selected')))
    case('orphaned selection rejected', lambda: rejected(lambda: store.restore(base/'orphan', ['unknown'])) )
    case('duplicate selection rejected', lambda: rejected(lambda: store.restore(base/'dup', [names[0], names[0]])))
    case('interrupted restore never publishes', lambda: rejected(lambda: store.restore(base/'interrupted', fault=True)))
    case('interrupted restore absent', lambda: equal((base/'interrupted').exists(), False))
    case('fresh restart after restore interruption', lambda: store.restore(base/'retry', experiment='c1-cargo'))
    case('cleanup wrong authority rejected', lambda: rejected(lambda: a.cleanup(base/'selected', '0'*64)))
    case('exact disposable cleanup', lambda: a.cleanup(base/'selected', receipt['lease_sha256']))

    for n, data in (('corrupt', b'bad'), ('truncated', b'')):
        def altered(n=n, data=data):
            rt, rr, st = fixture(n)
            _, archive, _ = a.e.load(st.index, st.index_sha)
            archive.write_bytes(data)
            rejected(lambda: st.verify(False))
        case(n + ' archive rejected', altered)

    def missing_archive():
        rt, rr, st = fixture('missing')
        _, archive, _ = a.e.load(st.index, st.index_sha)
        archive.unlink()
        rejected(lambda: st.verify())
    case('missing archive rejected', missing_archive)

    def changed_source():
        rt, rr, st = fixture('stale')
        (rt/rr[0]['path']).write_bytes(b'changed')
        rejected(lambda: st.locate(rr[0]['path'], rt))
    case('changed loose source cannot fall back', changed_source)

    def archive_fallback():
        rt, rr, st = fixture('fallback')
        (rt/rr[0]['path']).unlink()
        equal(st.locate(rr[0]['path'], rt)['loose'], False)
    case('exact archive fallback after synthetic absence', archive_fallback)

    def substitution():
        rt, rr, st = fixture('substitution')
        doc = json.loads(st.index.read_text())
        doc['archives']['cargo-transport-fuel']['rows'][0]['sha256'] = '0'*64
        st.index.write_bytes(a.e.encode(doc))
        rejected(lambda: st.verify())
    case('altered alternate index rejected', substitution)

    before = [dict(path=x['path'], sha256=x['sha256'], bytes=x['bytes']) for x in rows]
    expected = hashlib.sha256(a.e.encode(before)).hexdigest()
    shadow = a.migrate(before, names, store, expected)
    case('all routine member rows replaced by two objects', lambda: equal((len(shadow['after']), shadow['routine_member_checks']), (2, 0)))
    case('exact rollback to prior baseline', lambda: equal(a.rollback(shadow, expected), before))
    case('wrong baseline refused', lambda: rejected(lambda: a.migrate(before, names, store, '0'*64)))
    case('orphaned baseline member refused', lambda: rejected(lambda: a.migrate(before, ['unknown'], store, expected)))
    def duplicate_objects():
        extra = before + shadow['after']
        ss = a.migrate(extra, names, store, hashlib.sha256(a.e.encode(extra)).hexdigest())
        equal(len(ss['after']), 2)
    case('no double counting preexisting archive objects', duplicate_objects)
    case('invalid rollback state refused', lambda: rejected(lambda: a.rollback(dict(shadow, state='COMPLETED'), expected)))
    case('substituted rollback trust root refused', lambda: rejected(lambda: a.rollback(shadow, '0'*64)))
    def no_member_reads():
        with patch.object(a.e, 'inspect', side_effect=AssertionError('Loose member read')):
            equal(store.verify(False)['member_hashes'], 0)
        equal(set(names) & {r['path'] for r in shadow['after']}, set())
    case('retired set absent from routine loop', no_member_reads)

    recovered = store.restore(base/'recovery')
    plan = dict(schema='sor-cargo-retirement/1', authority='DELETION NOT AUTHORIZED',
                index_sha256=store.index_sha, archive_sha256=store.archive_sha,
                rows=[dict(x, member=x['path'], owner='cargo-transport-fuel', index_sha256=store.index_sha) for x in rows])
    pp, rp = base/'plan.json', base/'recovery.json'
    a.write(pp, plan)
    a.write(rp, dict(state='RESTORED-TESTED', index_sha256=store.index_sha,
                     archive_sha256=store.archive_sha, manifest_sha256=store.manifest_sha, members=len(rows),
                     restore=recovered))
    def prepare(**kw):
        return r.prepare(store, root, pp, a.e.pin(pp), rp, a.e.pin(rp), **kw)
    case('exact preparation deletes zero', lambda: equal(prepare()['deleted'], 0))
    case('changed allowlist authority refused', lambda: rejected(lambda: r.prepare(store, root, pp, '0'*64, rp, a.e.pin(rp))))
    case('missing recovery refused', lambda: rejected(lambda: r.prepare(store, root, pp, a.e.pin(pp), base/'absent', '0'*64)))
    for state, pending, completed in (('RETIRING', [names[0]], []), ('COMPLETED', [], names), ('PREPARED', [], [names[0]])):
        case('ambiguous journal ' + state + str(len(completed)), lambda state=state, pending=pending, completed=completed:
             rejected(lambda: prepare(journal=dict(state=state, pending=pending, completed=completed, plan_sha256=a.e.pin(pp)))))
    case('restart prepared empty journal', lambda: prepare(journal=dict(state='PREPARED', pending=[], completed=[], plan_sha256=a.e.pin(pp))))
    def disk():
        with patch.object(a.e.prototype.shutil, 'disk_usage', return_value=type('D', (), dict(free=39_999_999_999))()):
            rejected(prepare)
    case('insufficient free space both-drive guard', disk)
    def stale_preparation():
        p = root/names[0]
        original = p.read_bytes()
        p.write_bytes(b'changed')
        try:
            rejected(prepare)
        finally:
            p.write_bytes(original)
    case('stale source refuses retirement preparation', stale_preparation)
    def absent_preparation():
        p = root/names[0]
        original = p.read_bytes()
        p.unlink()
        try:
            rejected(prepare)
        finally:
            p.write_bytes(original)
    case('missing source refuses retirement preparation', absent_preparation)
    def abrupt_restore():
        target = base/'abrupt'
        command = ('from pathlib import Path; import access as a; s=a.Store(' +
                   repr(str(store.index)) + ',' + repr(store.index_sha) + ',' + repr(store.archive_sha) + ',' +
                   repr(store.manifest_sha) + '); s.restore(Path(' + repr(str(target)) + '),fault="process-exit")')
        process = subprocess.run([sys.executable,'-B','-c',command], cwd=Path(__file__).parent, capture_output=True)
        assert process.returncode == 73, process.stderr
        equal(target.exists(), False)
        store.restore(base/'abrupt-retry')
    case('power-loss-like abrupt restore and fresh restart', abrupt_restore)
    def hardlink():
        rt, rr, st = fixture('hardlink')
        os.link(rt/rr[0]['path'], rt/'alias')
        rejected(lambda: st.locate(rr[0]['path'], rt))
    case('real hardlink source rejected', hardlink)
    def junction():
        alias = base/'junction'
        p = subprocess.run(['cmd','/c','mklink','/J',str(alias),str(root)],capture_output=True)
        assert p.returncode == 0, p.stderr
        rejected(lambda: store.locate(names[0], alias))
    case('real junction ancestor rejected', junction)
    def cleanup_unknown():
        rec = store.restore(base/'extra')
        (base/'extra/unregistered').write_bytes(b'keep')
        rejected(lambda: a.cleanup(base/'extra', rec['lease_sha256']))
    case('cleanup refuses consumer-created unknown files', cleanup_unknown)
    def modified_lease():
        rec = store.restore(base/'modified')
        (base/'modified'/names[0]).write_bytes(b'changed')
        rejected(lambda: a.cleanup(base/'modified', rec['lease_sha256']))
    case('cleanup refuses modified restored bytes', modified_lease)
    for name in ('../escape', 'a:b', 'A/../b', 'CON', 'a\\b'):
        case('unsafe original ' + name, lambda name=name: rejected(lambda: store.locate(name, root)))
    a.write(base/'results.json', dict(results=results, passed=sum(x['status']=='PASS' for x in results),
                                     total=len(results), source_fixture=str(source_base)))
    print(json.dumps(dict(receipt=str(base/'results.json'), failed=[x for x in results if x['status']!='PASS']), indent=2))
    return int(any(x['status']!='PASS' for x in results))


def equal(left, right):
    assert left == right, (left, right)


if __name__ == '__main__':
    sys.exit(main())
