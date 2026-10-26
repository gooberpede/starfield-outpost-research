# SPDX-License-Identifier: GPL-3.0-or-later
"""Read-only real identity audit and disposable 1,051-member retirement replay.

Reads original Cargo sources and the accepted archive/index/controls. Copies the
archive and index into a disposable Stage B tree, retires only restored replicas,
and replays the two maintained consumers through a second authenticated lease.
Writes ignored audit receipts; never issues approval for the repository root.
"""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import uuid

import executor as x
from qualify_executor import controls, save, snapshot, unchanged

a, e = x.a, x.e
PLAN_SHA = 'b809a65f25560bec838873bfbb50c1e945a478a627129c24f837ec437b88e75d'
RECOVERY_SHA = '7d1ddeb5d169b35178d2632d3cdc54843e426c8a4ad159d0520967c12c194b63'
PRIOR = a.LOCAL / 'real04'


def inspect_real():
    store = a.Store()
    plan = e.authenticate(PRIOR / 'deletion-allowlist.json', PLAN_SHA)
    shadow = json.loads((PRIOR / 'shadow-baseline.json').read_text())
    with store.authenticated(True) as (entry, archive, members):
        assert len(plan['rows']) == 1051
        assert {r['path'] for r in plan['rows']} == {r['path'] for r in entry['rows']}
        holds = [r for r in shadow['before'] if r['path'] not in {n['path'] for n in plan['rows']}]
        assert {r['path'] for r in holds} == x.HOLDS
        assert x.census(a.ROOT, [r['path'] for r in plan['rows']], holds) == {r['path'] for r in plan['rows'] + holds}
        e.inspect(a.ROOT, plan['rows'] + holds)
        ledger = []
        for row in plan['rows'] + holds:
            with e.locked(a.ROOT / row['path']) as (f, info):
                x.checked(f, info, row, row in plan['rows'])
                st = __import__('os').fstat(f.fileno())
                ledger.append(dict(path=row['path'], sha256=row['sha256'], bytes=info.length,
                                   file_id=st.st_ino, device=st.st_dev, held=row in holds))
    prepared = __import__('retirement').prepare(store, a.ROOT, PRIOR / 'deletion-allowlist.json', PLAN_SHA,
                                               PRIOR / 'recovery.json', RECOVERY_SHA)
    return dict(git=x.git_identity(), archive=store.verify(), plan_sha256=PLAN_SHA,
                recovery_sha256=RECOVERY_SHA, shadow_sha256=e.pin(PRIOR / 'shadow-baseline.json'),
                ledger=ledger, ledger_sha256=x.digest(ledger), prepare=prepared, free=e.space())


def main():
    e.space(256 * 1024 * 1024)
    base = x.LOCAL / ('replica-' + uuid.uuid4().hex)
    base.mkdir(parents=True)
    source_pins = snapshot(base)
    before = inspect_real()
    save(base / 'real-before.json', before)
    print('Real population and trust roots authenticated; creating disposable replica.', flush=True)
    copied = e.LOCAL / base.name
    copied.mkdir()
    index = json.loads(a.INDEX.read_text())
    archive_name = index['archives']['cargo-transport-fuel']['archive']
    (copied / archive_name).parent.mkdir(parents=True)
    shutil.copyfile(a.INDEX, copied / 'index.json')
    shutil.copyfile(a.INDEX.parent / archive_name, copied / archive_name)
    st = a.Store(copied / 'index.json')
    replica_base = a.LOCAL / base.name
    replica = replica_base / 'originals'
    restored = st.restore(replica)
    for name in x.HOLDS:
        shutil.copyfile(a.ROOT / name, replica / name)
    tx, ap, sha = controls(replica, st, base / 'controls')
    assert tx.root != a.ROOT and tx.root.is_relative_to(replica_base)
    rejected = __import__('qualify_executor').rejected
    rejected(lambda: tx.verify('0' * 64))
    result = tx.execute(ap, sha)
    assert not any((replica / r['path']).exists() for r in json.loads(tx.controls[0][0].read_text())['rows'])
    save(base / 'retirement.json', result)
    save(base / 'routine.json', tx.verify(result['baseline_sha256']))
    print('All 1051 disposable originals absent; restoring authenticated consumer lease.', flush=True)
    lease = replica_base / 'consumer-lease'
    receipt = st.restore(lease)
    trials = []
    for script, experiment, expected_file in (
            ('research/c1-cargo/menu_abc.py', 'c1-cargo', 'menuabc03.json'),
            ('research/c2-transport/pex.py', 'c2-transport', 'pex01.json')):
        output = replica_base / (experiment + '-output')
        cmd = [sys.executable, '-B', script, '--run', 'replay', '--evidence-lease', str(lease),
               '--lease-sha256', receipt['lease_sha256'], '--output-directory', str(output)]
        run = subprocess.run(cmd, cwd=a.ROOT, capture_output=True, text=True)
        expected = json.loads((lease / '.local-work' / experiment / expected_file).read_text())
        actual = json.loads((output / 'replay.json').read_text()) if run.returncode == 0 else None
        trials.append(dict(script=script, command=cmd, returncode=run.returncode, stderr=run.stderr,
                           equal=actual == expected, expected_sha256=e.pin(lease / '.local-work' / experiment / expected_file),
                           output_sha256=e.pin(output / 'replay.json') if actual is not None else None))
        save(base / 'consumers.json', trials)
        assert run.returncode == 0 and actual == expected
    a.cleanup(lease, receipt['lease_sha256'])
    assert not lease.exists()
    save(base / 'lease-cleanup.json', dict(receipt=receipt, absent=True,
                                         original_replica_lease='Retired payloads absent; stale metadata retained as audit receipt'))
    after = inspect_real()
    save(base / 'real-after.json', after)
    assert before['ledger'] == after['ledger'] and before['git'] == after['git']
    unchanged(source_pins)
    save(base / 'summary.json', dict(real_sources_unchanged=1054, replica_retired=1051,
                                    real_deleted=0, real_baseline_activated=False, consumers=2,
                                    temporary_consumer_lease_absent=True, result=result, before_free=before['free'], after_free=after['free']))
    print(json.dumps(dict(directory=str(base), result='PASS'), indent=2))


if __name__ == '__main__':
    main()
