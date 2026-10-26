# SPDX-License-Identifier: GPL-3.0-or-later
"""Focused system-profile tests on fresh synthetic sources and controls only.

Reuses Cargo transaction/control fixtures under SOR-P-0002. Writes local test
archives and journals; only synthetic fixture sources may be removed. No real
evidence retirement, baseline activation, save, target, network or Git effects.
"""
import datetime as dt
import json
from pathlib import Path
import sys
import time
import uuid
import importlib.util
import os
from unittest.mock import patch
import copy
import hashlib

from prepare import ROOT, OUT, OWNER, a, e
import executor as x
import cutover as c
import resources_preservation as preservation
import staging as working


def run():
    base = OUT / ('qualification-' + uuid.uuid4().hex)
    base.mkdir(parents=True)
    results = []

    def save(path, value):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(e.encode(value))
        return e.pin(path)

    def fixture(name, protected=False):
        folder = e.LOCAL / base.name / name
        root = folder / 'source'
        prefix = '.local-work/resource-system-fixture/'
        rows = []
        for i in range(8):
            path = root / prefix / f'payload{i}.txt'
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(('synthetic-' + str(i)).encode())
            rows.append(dict(path=path.relative_to(root).as_posix(), bytes=path.stat().st_size,
                             sha256=e.pin(path), owner=OWNER))
        build = e.build(root, rows, folder / 'archive', owner=OWNER)
        store = a.Store(folder / 'archive/index.json', build['index_sha256'],
                        build['archive_sha256'], build['manifest_sha256'], OWNER)
        planned = []
        for row in rows:
            st = (root / row['path']).stat()
            with e.locked(root / row['path']) as (_, info):
                allocation = info.allocation
            planned.append(dict(row, member=row['path'], file_id=st.st_ino, device=st.st_dev,
                                mtime_ns=st.st_mtime_ns, allocated_bytes=allocation,
                                index_sha256=store.index_sha))
        plan = dict(schema='sor-cargo-retirement/1', authority='DELETION NOT AUTHORIZED',
                    index_sha256=store.index_sha, archive_sha256=store.archive_sha, rows=planned)
        recovery = dict(state='RESTORED-TESTED', members=len(rows), index_sha256=store.index_sha,
                        archive_sha256=store.archive_sha, manifest_sha256=store.manifest_sha)
        before = [{k: r[k] for k in ('path', 'bytes', 'sha256')} for r in rows]
        shadow = a.migrate(before, [r['path'] for r in rows], store, x.digest(before))
        location = base / name
        controls = []
        for filename, value in (('plan.json', plan), ('recovery.json', recovery), ('shadow.json', shadow)):
            path = location / filename
            controls += [path, save(path, value)]
        excluded = []
        if protected:
            path = root / prefix / 'protected.sfs'
            path.write_bytes(b'synthetic fixture; not a game save')
            st = path.stat()
            excluded.append(dict(path=path.relative_to(root).as_posix(), bytes=st.st_size,
                                 device=st.st_dev, file_id=st.st_ino, mtime_ns=st.st_mtime_ns))
        profile = dict(owner=OWNER, prefixes=[prefix], holds=[], empty_directories=[], excluded=excluded)
        tx = x.Transaction(root, store, *controls, location / 'tx', profile=profile)
        approval = location / 'synthetic-approval.json'
        digest = save(approval, dict(schema=1, operation=tx.operation, binding=tx.binding,
                      expires_utc=(dt.datetime.now(dt.timezone.utc)+dt.timedelta(hours=8)).isoformat(),
                      exclusive_ownership=True, maintainer_approval='SEPARATE EXPLICIT GO'))
        return tx, approval, digest, planned

    def case(name, fn):
        start = time.perf_counter()
        try:
            fn()
            result = dict(name=name, status='PASS', seconds=time.perf_counter()-start)
        except BaseException as exc:
            result = dict(name=name, status='FAIL', error=repr(exc), seconds=time.perf_counter()-start)
        results.append(result)
        save(base / f'case{len(results):02d}.json', result)

    def rejected(fn):
        try:
            fn()
        except (e.Error, OSError, KeyError, ValueError):
            return
        raise AssertionError('Expected rejection')

    def commit():
        tx, approval, digest, rows = fixture('commit')
        result = tx.execute(approval, digest)
        assert result['retired'] == 8
        assert tx.verify(result['baseline_sha256'])['state'] == 'COMMITTED'
        assert not any((tx.root / r['path']).exists() for r in rows)
    case('resource profile exact retirement and routine activation on synthetic inputs', commit)

    def resume():
        tx, approval, digest, rows = fixture('resume')
        def fault(event, name):
            if event == 'deleted':
                raise e.Error('Synthetic interruption after disposition')
        rejected(lambda: tx.execute(approval, digest, fault))
        result = tx.execute(approval, digest)
        assert tx.verify(result['baseline_sha256'])['state'] == 'COMMITTED'
    case('resource profile resumes authenticated INTENT after synthetic interruption', resume)

    def changed():
        tx, approval, digest, rows = fixture('changed')
        (tx.root / rows[-1]['path']).write_bytes(b'changed')
        rejected(lambda: tx.execute(approval, digest))
        assert all((tx.root / row['path']).exists() for row in rows)
    case('preflight rejects changed last source before any removal', changed)

    def late_change():
        tx, approval, digest, rows = fixture('late-change')
        def fault(event, name):
            if event == 'source-before-lock':
                (tx.root / name).write_bytes(b'late-change')
        rejected(lambda: tx.execute(approval, digest, fault))
        assert all((tx.root / row['path']).exists() for row in rows)
    case('locked source verification rejects changes before a new INTENT', late_change)

    def missing():
        tx, approval, digest, rows = fixture('missing')
        (tx.root / rows[0]['path']).unlink()
        rejected(lambda: tx.execute(approval, digest))
        assert all((tx.root / row['path']).exists() for row in rows[1:])
    case('unexplained absence cannot be resumed', missing)

    def exclusion():
        tx, approval, digest, _ = fixture('exclusion', protected=True)
        path = tx.root / tx.excluded[0]['path']
        def fault(event, name):
            if event == 'intent':
                rejected(lambda: path.write_bytes(b'forbidden synthetic mutation'))
        result = tx.execute(approval, digest, fault)
        assert path.read_bytes() == b'synthetic fixture; not a game save'
        assert tx.verify(result['baseline_sha256'])['state'] == 'COMMITTED'
    case('protected exclusion remains unchanged and locked through retirement', exclusion)

    def owner():
        tx, _, _, _ = fixture('owner')
        wrong = a.Store(tx.store.index, tx.store.index_sha, tx.store.archive_sha, tx.store.manifest_sha)
        rejected(wrong.verify)
        assert tx.store.verify()['members'] == 8
        rejected(lambda: x.scope(['.local-work/other/path'], tx.prefixes, tx.hold_names))
    case('explicit owner and namespace reject default Cargo or outside member', owner)

    def locator():
        tx, approval, digest, rows = fixture('locator')
        tx.execute(approval, digest)
        located = tx.store.locate(rows[0]['path'], source_root=tx.root)
        assert not located['loose'] and located['owner'] == OWNER
        path = tx.root / rows[0]['path']
        path.write_bytes(b'unexpected surviving source')
        rejected(lambda: tx.store.locate(rows[0]['path'], source_root=tx.root))
    case('resource locator uses archive after retirement and rejects conflicting loose bytes', locator)

    def identity_race():
        tx, approval, digest, rows = fixture('identity-race')
        initial = x.git_identity()
        altered = dict(initial, head='unapproved-head')
        with patch.object(x, 'git_identity', side_effect=[initial, altered]):
            rejected(lambda: tx.execute(approval, digest))
        assert all((tx.root / row['path']).exists() for row in rows)
    case('approval is revalidated after method and Git locks before retirement', identity_race)

    def runtime():
        tx, approval, digest, rows = fixture('runtime')
        altered = dict(x.runtime_identity(), executable_sha256='0' * 64)
        with patch.object(x, 'runtime_identity', return_value=altered):
            rejected(lambda: tx.execute(approval, digest))
        assert all((tx.root / row['path']).exists() for row in rows)
    case('changed execution runtime identity refuses the approved batch', runtime)

    def timestamp():
        tx, approval, digest, rows = fixture('timestamp')
        path = tx.root / rows[-1]['path']
        st = path.stat()
        os.utime(path, ns=(st.st_atime_ns, st.st_mtime_ns + 2_000_000_000))
        assert e.pin(path) == rows[-1]['sha256']
        rejected(lambda: tx.execute(approval, digest))
        assert all((tx.root / row['path']).exists() for row in rows)
    case('metadata-only timestamp change blocks before any retirement', timestamp)

    def allocation():
        tx, _, _, rows = fixture('allocation')
        plan = json.loads(tx.controls[0][0].read_text())
        plan['rows'][-1]['allocated_bytes'] += 4096
        path = tx.folder.parent / 'wrong-allocation-plan.json'
        digest = save(path, plan)
        revised = x.Transaction(tx.root, tx.store, path, digest,
                    *sum(([p, h] for p, h in tx.controls[1:]), []), tx.folder, profile=tx.profile)
        approval = tx.folder.parent / 'wrong-allocation-approval.json'
        digest = save(approval, dict(schema=1, operation=revised.operation, binding=revised.binding,
                      expires_utc=(dt.datetime.now(dt.timezone.utc)+dt.timedelta(hours=8)).isoformat(),
                      exclusive_ownership=True, maintainer_approval='SEPARATE EXPLICIT GO'))
        rejected(lambda: revised.execute(approval, digest))
        assert all((tx.root / row['path']).exists() for row in rows)
    case('allocation mismatch blocks with unchanged source content and identity', allocation)

    def control_limit():
        tx, _, _, _ = fixture('control-limit')
        path = tx.folder.parent / 'padded-recovery.json'
        raw = tx.controls[1][0].read_bytes()
        length = 70 * 1024 * 1024
        e.space(250 * 1024 * 1024)
        with path.open('xb') as stream:
            stream.write(raw)
            remaining = length - len(raw)
            while remaining:
                block = b' ' * min(remaining, 1024 * 1024)
                stream.write(block)
                remaining -= len(block)
        digest = e.pin(path)
        def size_refused(fn):
            try:
                fn()
            except e.Error as exc:
                assert 'Control document size bound' in str(exc)
            else:
                raise AssertionError('Expected exact control-size rejection')
        size_refused(lambda: e.authenticate(path, digest))
        revised = x.Transaction(tx.root, tx.store, *tx.controls[0], path, digest,
                                *tx.controls[2], tx.folder, profile=tx.profile)
        assert revised.control_limit == 128 * 1024 * 1024
        assert revised.read_controls()[1] == json.loads(raw)
        try:
            e.authenticate(path, '0' * 64, limit=revised.control_limit)
        except e.Error as exc:
            assert 'Independent control digest mismatch' in str(exc)
        else:
            raise AssertionError('Wrong control digest accepted')
        oversized = tx.folder.parent / 'oversized-control.json'
        with oversized.open('xb') as stream:
            stream.truncate(revised.control_limit + 1)
        size_refused(lambda: e.authenticate(oversized, '0' * 64, limit=revised.control_limit))
        save(tx.folder.parent / 'control-limit-proof.json', dict(valid_padded_bytes=length,
             valid_padded_sha256=digest, inherited_limit=64*1024*1024,
             resource_limit=revised.control_limit, oversized_bytes=revised.control_limit+1,
             disposition='Both exclusively created synthetic padding files removed after qualified checks; small original recovery and exact recipe retained'))
        for synthetic in (path, oversized):
            e.canonical(synthetic, base)
            with e.locked(synthetic, delete=True) as (stream, info):
                x.disposition(stream, True)
            assert not synthetic.exists()
    case('resource 128 MiB control cap accepts large authenticated JSON and preserves Cargo/default and upper-bound rejection', control_limit)

    def staging():
        tx, _, _, rows = fixture('staging')
        destination = a.RESOURCE_STAGING / base.name / 'lease'
        result = tx.store.restore(destination)
        assert result['files'] == 8
        assert a.lease_rows(destination, result['lease_sha256'])['owner'] == OWNER
        a.cleanup(destination, result['lease_sha256'])
        assert not destination.exists()
        original = e.prototype.shutil.disk_usage
        def low_c(path):
            value = original(path)
            if path == 'C:/':
                return type('Usage', (), dict(free=40_500_000_000))()
            return value
        with patch.object(e.prototype.shutil, 'disk_usage', low_c):
            rejected(lambda: a.workspace_space(destination, 1024*1024*1024))
        rejected(lambda: a.output(Path('C:/Users/User/Downloads/unapproved-lease')))
        rejected(lambda: tx.store.restore(a.RESOURCE_STAGING))
    case('authorized C staging restores and cleans exact lease while preserving target-volume reserve and boundary guards', staging)

    def partial_recovery():
        tx, _, _, rows = fixture('partial-recovery')
        full = tx.store.restore(a.RESOURCE_STAGING / base.name / 'alternate-full')
        partial = tx.folder.parent / 'full-restore01.partial-owned-fixture'
        partial.mkdir()
        for row in rows[:2]:
            source = tx.root / row['path']
            target = partial / row['path']
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(source.read_bytes())
        prefix = partial / rows[2]['path']
        prefix.write_bytes((tx.root / rows[2]['path']).read_bytes()[:5])
        st = partial.stat()
        result = working.seal_partial(partial, (st.st_dev, st.st_ino), full,
                   tx.folder.parent / 'recovered', tx.folder.parent / 'quarantine', tx.store)
        assert result['files'] == 2 and len(result['preserved_diagnostics']) == 1
        assert (tx.folder.parent / 'quarantine' / rows[2]['path']).read_bytes() == (tx.root / rows[2]['path']).read_bytes()[:5]
        a.cleanup(result['destination'], result['lease_sha256'])
        a.cleanup(full['destination'], full['lease_sha256'])
        assert all((tx.root / row['path']).exists() for row in rows)
    case('superseded working subset is proven and cleaned while incomplete prefix and originals survive', partial_recovery)

    def partial_reject():
        tx, _, _, rows = fixture('partial-reject')
        full = tx.store.restore(a.RESOURCE_STAGING / base.name / 'reject-alternate-full')
        partial = tx.folder.parent / 'full-restore01.partial-rejected-fixture'
        partial.mkdir()
        unknown = partial / 'unknown.bin'
        unknown.write_bytes(b'unknown synthetic bytes')
        st = partial.stat()
        rejected(lambda: working.seal_partial(partial, (st.st_dev, st.st_ino), full,
                   tx.folder.parent / 'rejected', tx.folder.parent / 'quarantine', tx.store))
        assert unknown.read_bytes() == b'unknown synthetic bytes'
        a.cleanup(full['destination'], full['lease_sha256'])
    case('unknown partial content refuses promotion or cleanup and is preserved', partial_reject)

    def merged_owner():
        tx, _, _, _ = fixture('merged-owner')
        cargo = e.authenticate(e.ARCHIVES / 'index.json', a.INDEX_SHA)
        resource = e.authenticate(tx.store.index, tx.store.index_sha)
        entry = resource['archives'][OWNER]
        archive = tx.store.index.parent / entry['archive']
        copy_path = e.ARCHIVES / (base.name + '-synthetic.tar.zst')
        copy_path.write_bytes(archive.read_bytes())
        entry['archive'] = copy_path.name
        cargo['archives'][OWNER] = entry
        path = e.ARCHIVES / (base.name + '-merged.json')
        e.record(path, cargo)
        digest = e.pin(path)
        assert a.Store(path, digest).verify(False)['members'] == 1051
        assert a.Store(path, digest, tx.store.archive_sha, tx.store.manifest_sha, OWNER).verify()['members'] == 8
    case('multi-owner index preserves Cargo cross-references and explicit selection', merged_owner)

    def configuration(tx, result):
        control_path = tx.folder.parent / 'controls.json'
        controls = dict(controls=[dict(path=str(p), sha256=h) for p, h in tx.controls], profile=tx.profile)
        digest = save(control_path, controls)
        selection = dict(schema='sor-resources-active-selection/1', owner=OWNER, state='ACTIVE',
                         baseline_sha256=result['baseline_sha256'], journal_sha256=result['journal_sha256'],
                         index=dict(path=str(tx.store.index), sha256=tx.store.index_sha),
                         archive_sha256=tx.store.archive_sha, manifest_sha256=tx.store.manifest_sha,
                         controls_sha256=digest, retired_members=8)
        return dict(schema='sor-resources-selection-proposal/1', authority='NOT AUTHORIZED',
                    source_root=str(tx.root), transaction=str(tx.folder),
                    controls=dict(path=str(control_path), sha256=digest), selection=selection,
                    selection_sha256=x.digest(selection), execution_binding_sha256=x.digest(tx.binding))

    def activation():
        tx, approval, digest, rows = fixture('activation')
        shadow = e.authenticate(*tx.controls[2])
        predicted, predicted_journal = c.expected_completion(tx, shadow, [r['path'] for r in rows])
        result = tx.execute(approval, digest)
        assert result['baseline_sha256'] == predicted and result['journal_sha256'] == predicted_journal
        config = configuration(tx, result)
        target = tx.folder.parent / 'active.json'
        def fault(event):
            if event == 'selection-writing':
                raise e.Error('Synthetic interruption before selection publication')
        rejected(lambda: c.activate(config, tx, fault, target))
        assert not target.exists() and target.with_suffix('.json.writing').exists()
        c.activate(config, tx, destination=target)
        c.activate(config, tx, destination=target)
        assert c.verify_active_selection(target, config)[0]['state'] == 'COMMITTED'
        after = target.with_name('active-after-publication.json')
        def after_fault(event):
            if event == 'selection-published':
                raise e.Error('Synthetic interruption after selection publication')
        rejected(lambda: c.activate(config, tx, after_fault, after))
        assert after.exists() and c.verify_active_selection(after, config)[0]['state'] == 'COMMITTED'
        c.activate(config, tx, destination=after)
        return tx, rows, config, target
    case('predicted complete hashes and interrupted activation resume exactly', lambda: activation())

    def readers():
        tx, approval, digest, rows = fixture('readers')
        result = tx.execute(approval, digest)
        config = configuration(tx, result)
        target = tx.folder.parent / 'active.json'
        c.activate(config, tx, destination=target)
        inputs = [dict(path=str(tx.root / rows[0]['path']), sha256=rows[0]['sha256'], match=True)]
        live = tx.folder.parent / 'nonexistent-active-save-namespace'
        for name in ('resource-carinae-source-context', 'resource-tungsten-acquisition'):
            sys.path.insert(0, str(ROOT / 'research' / name))
            spec = importlib.util.spec_from_file_location('test_' + name.replace('-', '_'), ROOT / 'research' / name / 'protection.py')
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            with patch.object(preservation, 'SELECTION', target), patch.object(preservation, 'trusted_configuration', return_value=config), \
                 patch.object(module, 'snapshot', return_value={}), patch.object(module, 'compare', return_value=dict(ok=True)), \
                 patch.object(module, 'partition', return_value={}):
                result = module.audit_rows(inputs, live, {}, include_archive_pins=True)
                assert result['changes'] == [] and len(result['_archive_pins']) == 8
                wrong = copy.deepcopy(inputs)
                wrong[0]['sha256'] = '0' * 64
                assert module.audit_rows(wrong, live, {})['changes']
                for path in (target, Path(config['controls']['path']), tx.store.index, tx.folder / 'journal.jsonl'):
                    raw = path.read_bytes()
                    path.write_bytes(raw + b' ')
                    rejected(lambda: module.audit_rows(inputs, live, {}))
                    path.write_bytes(raw)
    case('both active preservation readers enforce pins and reject substituted selection/control/index/journal', readers)

    def scale():
        # Actual full-cardinality metadata and transition replay; durability is
        # separately exercised by the real small journals and Cargo regressions.
        names = [f'.local-work/resource-system-fixture/{i:06d}.bin' for i in range(134140)]
        e.names_valid(names)
        log = object.__new__(x.Journal)
        log.events = [dict(event='PREPARED', path=None)]
        for name in names:
            log.events.extend((dict(event='INTENT', path=name), dict(event='DONE', path=name)))
        log.events += [dict(event='RETIRED_PENDING_BASELINE', path=None), dict(event='COMMITTED', path=None)]
        log.validate()
        assert log.state == 'COMMITTED' and log.completed == names and log.pending is None
        rejected(lambda: log.transition(dict(event='INTENT', path=names[0])))
    case('134140-member metadata and complete journal-state replay', scale)
    save(base / 'results.json', dict(results=results, methods=x.methods(),
         script_sha256=e.pin(Path(__file__)), free=e.space()))
    print(json.dumps(dict(directory=str(base), passed=sum(r['status']=='PASS' for r in results), total=len(results))), flush=True)
    if any(r['status'] != 'PASS' for r in results):
        raise SystemExit(1)


if __name__ == '__main__':
    run()
