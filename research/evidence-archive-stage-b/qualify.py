# SPDX-License-Identifier: GPL-3.0-or-later
"""Disposable Windows fault injection; never touches authentic evidence.

Creates fresh synthetic fixtures under the Stage B local root. Some tests delete
only their own fixture files using the proposed executor. Leaves failures intact.
"""
import hashlib
import contextlib
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import time
from unittest.mock import patch
import uuid

import engine as e


def main():
    e.space(128*1024*1024)
    base = e.LOCAL / ('qualification-' + uuid.uuid4().hex)
    base.mkdir()
    results = []

    def case(name, function):
        before = e.space(32*1024*1024)
        try:
            function()
            results.append(dict(name=name, status='PASS', before_free=before, after_free=e.space()))
        except BaseException as exc:
            results.append(dict(name=name, status='FAIL', error=repr(exc)))
        e.record(base/'results.json', results, replace=True)

    def rejected(function):
        try:
            function()
        except (e.Error, OSError, ValueError, KeyError, tarfile.TarError):
            return
        raise AssertionError('Expected rejection')

    def fixture(name):
        folder = base/name
        root = folder/'sources'
        root.mkdir(parents=True)
        rows = []
        for filename, data in (('a.txt', b'alpha'*100), ('nested/b.txt', b'beta'*100), ('zero', b'')):
            p = root/filename
            p.parent.mkdir(exist_ok=True)
            p.write_bytes(data)
            rows.append(dict(path=filename, bytes=len(data), sha256=hashlib.sha256(data).hexdigest()))
        return folder, root, e.inspect(root, rows)

    folder, root, rows = fixture('good')
    result = e.build(root, rows, folder/'transaction')
    index = folder/'transaction/index.json'
    anchor = result['index_sha256']

    def equivalent():
        e.restore(index, anchor, folder/'restored')
        assert e.inspect(folder/'restored', rows) == rows
    case('full restore equality and empty member', equivalent)
    case('wrong independent index anchor', lambda: rejected(lambda: e.restore(index, '0'*64, folder/'bad')))
    case('existing restore destination', lambda: rejected(lambda: e.restore(index, anchor, folder/'restored')))
    case('existing build destination', lambda: rejected(lambda: e.build(root, rows, folder/'transaction')))
    case('restore interrupted before publication', lambda: rejected(lambda: e.restore(index, anchor, folder/'interrupted', True)))
    case('interrupted restore not published', lambda: assert_false((folder/'interrupted').exists()))
    case('authenticated recovery', lambda: assert_equal(e.recover(folder/'transaction', anchor)['state'], 'VERIFIED'))
    case('unanchored recovery quarantine', lambda: assert_equal(e.recover(folder/'transaction')['state'], 'QUARANTINED'))
    def hard_exit():
        f, r, rr = fixture('process-exit')
        e.record(f/'rows.json',rr)
        command = 'import json,pathlib,engine as e; e.build(pathlib.Path('+repr(str(r))+'),json.loads(pathlib.Path('+repr(str(f/'rows.json'))+').read_text()),pathlib.Path('+repr(str(f/'transaction'))+'),"process-exit")'
        process = subprocess.run([sys.executable,'-B','-c',command],cwd=Path(__file__).parent,capture_output=True)
        assert process.returncode == 73, process.stderr
        assert not (f/'transaction/index.json').exists()
        assert e.recover(f/'transaction')['state']=='QUARANTINED'
        e.build(r,rr,f/'retry')
    case('abrupt process exit without finally and safe fresh retry', hard_exit)
    for fault in ('creation','before-publication','after-publication'):
        def interrupted(fault=fault):
            f, r, rr = fixture(fault)
            rejected(lambda: e.build(r, rr, f/'transaction', fault))
            assert not (f/'transaction/index.json').exists()
            assert e.recover(f/'transaction')['state'] == 'QUARANTINED'
            e.build(r, rr, f/'retry')
        case('crash ' + fault + ' and fresh retry', interrupted)
    for name in ('../escape','C:/absolute','a:b','a/../b','a\\b','a.','CON','aux.txt','/absolute','a//b'):
        case('unsafe path ' + repr(name), lambda name=name: rejected(lambda: e.safe_name(name)))
    for names in (['a','A'], ['a','a/b'], ['e\u0301','\u00e9']):
        case('alias collision ' + repr(names), lambda names=names: rejected(lambda: e.names_valid(names)))

    def byte_change():
        f, r, rr = fixture('byte-change')
        (r/'a.txt').write_bytes(b'X'*500)
        rejected(lambda: e.build(r, rr, f/'transaction'))
    case('changed bytes without journal change', byte_change)

    def missing():
        f, r, rr = fixture('missing')
        (r/'a.txt').unlink()
        rejected(lambda: e.build(r, rr, f/'transaction'))
    case('missing original source', missing)

    def hardlink():
        f, r, rr = fixture('hardlink')
        os.link(r/'a.txt', r/'alias')
        rejected(lambda: e.inspect(r, rr))
    case('hardlink excluded', hardlink)

    def ads():
        f, r, rr = fixture('ads')
        Path(str(r/'a.txt')+':hidden').write_bytes(b'hidden')
        rejected(lambda: e.inspect(r, rr))
    case('alternate data stream excluded', ads)

    def junction():
        f, r, rr = fixture('junction')
        alias = f/'junction'
        process = subprocess.run(['cmd','/c','mklink','/J',str(alias),str(r)], capture_output=True)
        if process.returncode:
            raise AssertionError(process.stderr.decode(errors='replace'))
        rejected(lambda: e.inspect(alias, rr))
    case('actual Windows junction excluded', junction)

    def disk():
        with patch.object(e.prototype.shutil, 'disk_usage', return_value=shutil._ntuple_diskusage(1,1,1)):
            rejected(lambda: e.space(1))
    case('both-drive capacity guard failure', disk)

    for variant in ('tamper-index','corrupt-archive','missing-archive','truncated-archive'):
        def corrupt(variant=variant):
            f, r, rr = fixture(variant)
            result = e.build(r, rr, f/'transaction')
            idx = f/'transaction/index.json'
            arc = f/'transaction/cargo-transport-fuel.tar.zst'
            if variant == 'tamper-index':
                idx.write_bytes(idx.read_bytes()+b' ')
            elif variant == 'missing-archive':
                arc.unlink()
            elif variant == 'truncated-archive':
                arc.write_bytes(arc.read_bytes()[:20])
            else:
                raw = bytearray(arc.read_bytes())
                raw[len(raw)//2] ^= 1
                arc.write_bytes(raw)
            rejected(lambda: e.restore(idx, result['index_sha256'], f/'restore'))
        case(variant, corrupt)

    def replaced_pair():
        f, r, rr = fixture('replacement')
        (r/'a.txt').write_bytes(b'changed'*70)
        rr[0].update(bytes=490, sha256=hashlib.sha256(b'changed'*70).hexdigest())
        other = e.build(r, rr, f/'transaction')
        rejected(lambda: e.restore(f/'transaction/index.json', anchor, f/'restore'))
    case('self-consistent archive/index substitution', replaced_pair)

    def malicious_tar():
        p = base/'malicious.tar.zst'
        with tarfile.open(p, 'w:zst') as tar:
            item = tarfile.TarInfo('../escape')
            item.size = 1
            tar.addfile(item, io.BytesIO(b'x'))
        rejected(lambda: e.prototype.stream_members(p, 'tar.zst', {'a':dict(bytes=1,sha256=hashlib.sha256(b'x').hexdigest())}))
    case('actual malicious tar traversal', malicious_tar)

    def malicious_link():
        p = base/'link.tar.zst'
        with tarfile.open(p, 'w:zst') as tar:
            item = tarfile.TarInfo('a')
            item.type = tarfile.SYMTYPE
            item.linkname = 'elsewhere'
            tar.addfile(item)
        rejected(lambda: e.prototype.stream_members(p, 'tar.zst', {'a':dict(bytes=0,sha256=hashlib.sha256(b'').hexdigest())}))
    case('actual tar symlink', malicious_link)

    def retirement():
        f, r, rr = fixture('retirement')
        result = e.build(r, rr, f/'transaction')
        idx = f/'transaction/index.json'
        anc = result['index_sha256']
        e.restore(idx, anc, f/'recovery')
        manifest = f/'manifest.json'
        e.record(manifest, dict(schema=1,index_sha256=anc,rows=rr))
        approved = e.pin(manifest)
        rejected(lambda: e.retire(r,idx,anc,manifest,'0'*64,execute=True))
        assert e.retire(r,idx,anc,manifest,approved)['deleted'] == 0
        rejected(lambda: e.retire(r,idx,anc,manifest,approved,execute=True,fault=0))
        assert not (r/rr[0]['path']).exists()
        assert (r/rr[1]['path']).exists()
        # A missing source never becomes proof of our deletion from a journal.
        rejected(lambda: e.retire(r,idx,anc,manifest,approved,execute=True))
        restored = f/'recovery'/rr[0]['path']
        (r/rr[0]['path']).write_bytes(restored.read_bytes())
        assert e.retire(r,idx,anc,manifest,approved,execute=True)['state'] == 'COMPLETED'
        assert not any((r/row['path']).exists() for row in rr)
        # Full rollback onto a fresh root; original simulation data remains absent.
        e.restore(idx,anc,f/'rollback')
        assert e.inspect(f/'rollback',rr) == rr
    case('dry run, wrong approval, partial deletion, fail-closed retry, rollback and completion', retirement)

    def nonmember():
        manifest = folder/'invalid-manifest.json'
        e.record(manifest, dict(schema=1,index_sha256=anchor,rows=[dict(path='outside',bytes=0,sha256='0'*64,allocated_bytes=0)]))
        rejected(lambda: e.retire(root,index,anchor,manifest,e.pin(manifest),execute=True))
    case('nonmember deletion allowlist', nonmember)
    for variant in ('duplicate-owner','unicode-owner-alias','unresolved-reference','archive-traversal','invalid-schema'):
        def bad_central(variant=variant):
            f,r,rr = fixture(variant)
            res = e.build(r,rr,f/'transaction')
            idx = f/'transaction/index.json'
            data = json.loads(idx.read_text())
            if variant == 'duplicate-owner':
                other = dict(data['archives']['cargo-transport-fuel'],owner='other-system')
                data['archives']['other-system'] = other
            elif variant == 'unicode-owner-alias':
                data['archives']['cargo-transport-fuel']['rows'][0]['path'] = '\u00e9'
                other = dict(data['archives']['cargo-transport-fuel'],owner='other-system',
                             rows=[dict(rr[0],path='e\u0301')])
                data['archives']['other-system'] = other
            elif variant == 'unresolved-reference':
                data['cross_references'] = [dict(owner='cargo-transport-fuel',path='absent',consumer_system='governance')]
            elif variant == 'archive-traversal':
                data['archives']['cargo-transport-fuel']['archive'] = '../outside.tar.zst'
            else:
                data['schema'] = 500
            idx.write_bytes(e.encode(data))
            rejected(lambda: e.restore(idx,e.pin(idx),f/'restore'))
        case('central index ' + variant,bad_central)
    def changed_retire():
        f,r,rr = fixture('changed-retire')
        res = e.build(r,rr,f/'transaction')
        plan = f/'manifest.json'
        e.record(plan,dict(schema=1,index_sha256=res['index_sha256'],rows=rr))
        (r/'nested/b.txt').write_bytes(b'X'*400)
        rejected(lambda: e.retire(r,f/'transaction/index.json',res['index_sha256'],plan,e.pin(plan),execute=True))
        assert (r/'a.txt').exists()
    case('changed source aborts entire retirement preflight before first removal',changed_retire)
    def vanished():
        f,r,rr = fixture('vanished')
        res = e.build(r,rr,f/'transaction')
        plan = f/'manifest.json'
        e.record(plan,dict(schema=1,index_sha256=res['index_sha256'],rows=rr))
        real = e.verified
        count = 0
        @contextlib.contextmanager
        def injection(*args):
            nonlocal count
            count += 1
            with real(*args) as value:
                if count == 3:
                    (r/rr[1]['path']).unlink()
                yield value
        with patch.object(e,'verified',injection):
            rejected(lambda: e.retire(r,f/'transaction/index.json',res['index_sha256'],plan,e.pin(plan),execute=True))
        log = json.loads((f/'retirement.json').read_text())
        assert log['state'] != 'COMPLETED' and rr[1]['path'] not in log['completed']
    case('source vanishes after preflight: stop partial retirement',vanished)
    def retirement_space():
        f,r,rr = fixture('retirement-space')
        res = e.build(r,rr,f/'transaction')
        plan = f/'manifest.json'
        e.record(plan,dict(schema=1,index_sha256=res['index_sha256'],rows=rr))
        with patch.object(e.prototype.shutil,'disk_usage',return_value=shutil._ntuple_diskusage(100_000_000_000,59_999_500_000,40_000_500_000)):
            rejected(lambda: e.retire(r,f/'transaction/index.json',res['index_sha256'],plan,e.pin(plan),execute=True))
        assert not (f/'retirement.json').exists()
        assert all((r/row['path']).exists() for row in rr)
    case('retirement journal reservation fails above bare minimum without writes',retirement_space)
    summary = e.ROOT/'.local-work/evidence-archive-discovery/cargo-pilot-summary04.json'
    for hold in json.loads(summary.read_text())['historical_method_version_holds']:
        def wrong_version(hold=hold):
            f,r,rr = fixture('version-' + Path(hold['path']).parent.name)
            data = (e.ROOT/hold['path']).read_bytes()
            current = hashlib.sha256(data).hexdigest()
            assert current == hold['current_sha256']
            (r/'method.py').write_bytes(data)
            old = next(x['sha256'] for x in hold['historical_expectations'] if x['sha256'] != current)
            rejected(lambda: e.build(r,[dict(path='method.py',bytes=len(data),sha256=old)],f/'transaction'))
            e.build(r,[dict(path='method.py',bytes=len(data),sha256=current)],f/'accepted-current')
        case('reject historical expectation for current ' + hold['path'],wrong_version)
    e.record(base/'summary.json', dict(tests=len(results), passed=sum(r['status']=='PASS' for r in results),
              failed=[r for r in results if r['status']!='PASS'], free=e.space(),
              methods={p.name:e.pin(p) for p in Path(__file__).parent.glob('*.py')}))
    print(json.dumps(dict(directory=str(base), tests=len(results), failed=[r for r in results if r['status']!='PASS']),indent=2))
    if any(r['status']!='PASS' for r in results):
        raise SystemExit(1)


def assert_equal(a, b):
    assert a == b, (a,b)


def assert_false(a):
    assert not a


if __name__ == '__main__':
    main()
