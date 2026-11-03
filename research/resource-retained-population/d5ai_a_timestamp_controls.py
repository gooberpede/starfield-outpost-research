# SPDX-License-Identifier: GPL-3.0-or-later
"""Qualify Episode A timestamp guards on owned files and labeled protocol models.

Writes fresh ignored fixtures/receipts, touches only those fixture timestamps and
contents, and runs this task's Python CLI for help/optimization/authority refusals.
No game, native host, save original, deployment, process intervention or network.
File-guard/phase positives use real owned bytes; fabricated preflight/postflight
objects are explicit models, never real protected audits or live observations.
"""
import sys
if not __debug__ or sys.flags.optimize:
    raise RuntimeError('Use Python -E -B')

import argparse
import copy
import json
import os
from pathlib import Path
import subprocess
from types import SimpleNamespace

import d5ai_a_operations as ops
import d5ai_a_episode as episode


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('out', type=Path)
    args = parser.parse_args()
    out = args.out.resolve()
    ops.require(out.is_relative_to(ops.ROOT / '.local-work/d5ai-a'), 'Task-local controls required')
    ops.guard()
    out.mkdir(exist_ok=False)
    tests = []

    def check(name, condition):
        tests.append(dict(name=name, passed=bool(condition)))
        if not condition:
            raise AssertionError(name)

    def refuse(name, fn, kind=(ValueError, AssertionError, OSError)):
        try:
            fn()
        except kind:
            check(name, True)
        else:
            check(name, False)

    fixture = out / 'guard.dat'
    fixture.write_bytes(b'original bytes!!')
    row = dict(bytes=fixture.stat().st_size, mtime_ns=fixture.stat().st_mtime_ns)
    digest = ops.sha(fixture)
    check('unchanged-large-guard-fast-path', ops.content_guard(fixture, row, digest) is None)
    os.utime(fixture, ns=(row['mtime_ns'], row['mtime_ns'] + 2_000_000_000))
    result = ops.content_guard(fixture, row, digest)
    check('actual-timestamp-only-file-accepted-and-hashed', result['timestamp_changed'] and result['content_sha256_verified'] == digest)
    fixture.write_bytes(b'changed bytes!!!')
    os.utime(fixture, ns=(row['mtime_ns'], row['mtime_ns'] + 4_000_000_000))
    refuse('same-size-changed-bytes-with-new-time-refused', lambda: ops.content_guard(fixture, row, digest))
    os.utime(fixture, ns=(row['mtime_ns'], row['mtime_ns']))
    refuse('configuration-changed-content-original-time-refused', lambda: ops.content_guard(fixture, row, digest, True))
    fixture.write_bytes(b'x')
    refuse('size-change-refused', lambda: ops.content_guard(fixture, row, digest))
    refuse('missing-file-refused', lambda: ops.content_guard(out / 'absent', row, digest))
    refuse('missing-independent-hash-refused', lambda: ops.content_guard(fixture, row, None))
    fixture.write_bytes(b'original bytes!!')
    saved_sha = ops.sha
    reads = 0

    def changing_time(path):
        nonlocal reads
        value = saved_sha(path)
        reads += 1
        stat = Path(path).stat()
        os.utime(path, ns=(stat.st_atime_ns, stat.st_mtime_ns + 2_000_000_000))
        return value

    ops.sha = changing_time
    try:
        refuse('unstable-equal-content-yields-pending-not-abort',
               lambda: ops.content_guard(fixture, row, digest, True), ops.TimestampPending)
        check('unstable-read-bounded-to-two-checks', reads == 2)
    finally:
        ops.sha = saved_sha

    plan = ops.original.read_json(ops.ROOT / '.local-work/d5ai/final-plans05/episode-a-plan.json')
    plan.update(timestamp_policy=ops.POLICY,
                episode_a_adapter_pins={str(p): ops.sha(p) for p in sorted(ops.ADAPTERS)})
    live, remote, plugins = (out / n for n in ('live-saves', 'remote-saves', 'plugins'))
    for p in (live, remote, plugins):
        p.mkdir()
    save_name = plan['save52_name']
    (live / save_name).write_bytes(b'owned namespace model')
    config, definition, installed, sfse, dll = [out / 'config.ini', out / 'definition.esm',
                                              out / 'installed.exe', out / 'sfse.dll', plugins / 'SorConstructionWinner.dll']
    for p in (config, definition, installed, sfse, dll):
        p.write_bytes(b'owned file guard model')
    def metadata(p):
        return dict(bytes=p.stat().st_size, mtime_ns=p.stat().st_mtime_ns)
    policy = ops.original.legacy().policy_module()
    before = dict(protection=dict(save_policy_sha256=policy.policy_hash(policy.load_policy()),
                                 live_path=str(live), protected_live={save_name: dict(bytes=(live / save_name).stat().st_size)},
                                 config={str(config): ops.sha(config)}, definitions={str(definition): ops.sha(definition)},
                                 file_guards={str(p): metadata(p) for p in (config, definition)},
                                 installed={str(installed): dict(metadata(installed), sha256=ops.sha(installed))}),
                  remote_protected_sizes={str(remote): {}})
    plan.update(sfse_path=str(sfse), sfse_sha256=ops.sha(sfse), deployed_dll=str(dll), dll_sha256=ops.sha(dll))
    for p in (config, definition, installed):
        stat = p.stat()
        os.utime(p, ns=(stat.st_atime_ns, stat.st_mtime_ns + 2_000_000_000))
    phase = ops.lightweight(plan, before)
    check('actual-phase-three-file-types-timestamp-only-pass', phase['state'] == 'PASS_LIGHTWEIGHT' and len(phase['timestamp_changes']) == 3)
    target = episode.EpisodeAController.__new__(episode.EpisodeAController)
    target.plan = plan
    target.validate_phase(before)
    check('actual-controller-dispatch-reaches-new-phase', target.phase_result['timestamp_policy'] == ops.POLICY)
    for p, label in ((config, 'config'), (definition, 'definition'), (installed, 'installed')):
        old = p.read_bytes()
        p.write_bytes(b'changed file guard mdl!')
        stat = p.stat()
        os.utime(p, ns=(stat.st_atime_ns, stat.st_mtime_ns + 4_000_000_000))
        refuse('actual-phase-content-refusal-' + label, lambda: ops.lightweight(plan, before))
        p.write_bytes(old)
    bad = copy.deepcopy(plan)
    bad['episode'] = 'B'
    refuse('episode-b-scope-refused', lambda: ops.lightweight(bad, before))
    bad = copy.deepcopy(plan)
    bad['episode_a_adapter_pins'][str(Path(ops.__file__).resolve())] = '0' * 64
    refuse('adapter-source-drift-refused', lambda: ops.lightweight(bad, before))
    bad_before = copy.deepcopy(before)
    bad_before['protection']['save_policy_sha256'] = '0' * 64
    refuse('policy-change-refused', lambda: ops.lightweight(plan, bad_before))
    bad_before = copy.deepcopy(before)
    del bad_before['protection']['file_guards'][str(config)]
    refuse('incomplete-roster-refused', lambda: ops.lightweight(plan, bad_before))
    (live / 'unknown.sfs').write_bytes(b'unknown')
    refuse('unclassified-save-refused', lambda: ops.lightweight(plan, before))
    (live / 'unknown.sfs').rename(live / 'unknown-preserved.bin')
    # The unsupported file remains outside this model's measured save namespace.
    (live / 'unknown-preserved.bin').rename(out / 'unknown-preserved.bin')
    (plugins / 'SorOther.dll').write_bytes(b'owned competing model')
    refuse('competing-plugin-refused', lambda: ops.lightweight(plan, before))

    baseline = dict(save_policy_sha256='p' * 64, protected_live={'save': dict(bytes=4, sha256='s' * 64)},
                    backups={'save': [dict(path='backup', sha256='b' * 64, kind='LOOSE_BACKUP',
                                           metadata=dict(bytes=4, mtime_ns=1))]},
                    archive_guard={'archive': dict(bytes=12, mtime_ns=1)},
                    archive_content_sha256={'archive': 'a' * 64},
                    definitions={'definition': 'd' * 64}, config={'config': 'c' * 64},
                    restore_rehearsal_sha256='r' * 64,
                    installed={'installed': dict(bytes=4, mtime_ns=1, sha256='i' * 64)},
                    file_guards={'definition': dict(bytes=4, mtime_ns=1), 'config': dict(bytes=4, mtime_ns=1)})
    after = copy.deepcopy(baseline)
    after['backups']['save'][0]['metadata']['mtime_ns'] = 2
    for group in ('archive_guard', 'installed', 'file_guards'):
        for value in after[group].values():
            value['mtime_ns'] = 2
    preserved = copy.deepcopy(baseline), copy.deepcopy(after)
    comparison = ops.compare_protection(baseline, after)
    check('typed-postflight-time-only-pass', comparison['equal'] and len(comparison['timestamp_changes']) == 5)
    check('comparison-does-not-mutate-inputs', (baseline, after) == preserved)
    for group, key in (('archive_content_sha256', 'archive'), ('definitions', 'definition'), ('config', 'config')):
        changed = copy.deepcopy(after)
        changed[group][key] = '0' * 64
        refuse('postflight-content-refusal-' + group, lambda changed=changed: ops.compare_protection(baseline, changed))
    for label, edit in (
            ('backup-hash', lambda v: v['backups']['save'][0].update(sha256='0' * 64)),
            ('backup-path', lambda v: v['backups']['save'][0].update(path='other')),
            ('backup-size', lambda v: v['backups']['save'][0]['metadata'].update(bytes=5)),
            ('archive-unknown-metadata', lambda v: v['archive_guard']['archive'].update(unknown=3)),
            ('installed-hash', lambda v: v['installed']['installed'].update(sha256='0' * 64)),
            ('protected-hash', lambda v: v['protected_live']['save'].update(sha256='0' * 64))):
        changed = copy.deepcopy(after)
        edit(changed)
        refuse('postflight-' + label + '-refused', lambda changed=changed: ops.compare_protection(baseline, changed))

    # Execute the real adapter's private-module postflight routing. Native raw
    # readers run on an existing completed owned capture; process/preservation
    # premises are explicit models. Retail finalization is expected to refuse
    # this non-retail session, independently of the tested content comparator.
    archive = out / 'modeled-audit-archive.dat'
    archive.write_bytes(b'owned audit archive')
    first, second = copy.deepcopy(baseline), copy.deepcopy(after)
    for value in (first, second):
        value['archive_guard'] = {str(archive): dict(bytes=archive.stat().st_size,
                                                    mtime_ns=1 if value is first else 2)}
        value['archive_content_sha256'] = {str(archive): ops.sha(archive)}
    native = ops.ROOT / '.local-work/d5ai-recorder/build16/d5ai-retained'
    identity = ops.original.read_json(native / 'identity.json')
    post_plan = copy.deepcopy(plan)
    post_plan.update(dll_sha256=identity['dll_sha256'], deployed_dll=str(out / 'absent-postflight.dll'),
                     plan_sha256='b' * 64)
    admission = dict(protection=first, remote_protected_sizes={}, receipt_sha256='a' * 64)
    saved_verify, saved_legacy = ops.original.verify_plan, ops.original.legacy
    base_compare = saved_legacy().compare_protection

    def factory():
        return SimpleNamespace(verify_plan=lambda value: None,
                               original_process_gone=lambda value: 'MODELED_COMPLETED_OWNED_HOST',
                               full=lambda path: copy.deepcopy(second),
                               compare_protection=base_compare, remote_sizes=lambda value: {})

    ops.original.verify_plan = lambda value: None
    ops.original.legacy = factory
    try:
        value = ops.postflight(post_plan, admission, native, {}, out)
        check('adapter-private-postflight-actually-invokes-content-comparator',
              not value['protection_errors'] and value['protection_comparisons'][0]['equal'])
        check('modeled-nonretail-postflight-not-reported-real-pass', value['status'] == 'PARTIAL_POSTFLIGHT')
        second['backups']['save'][0]['sha256'] = '0' * 64
        value = ops.postflight(post_plan, admission, native, {}, out)
        check('adapter-private-postflight-content-failure-remains-protection-error',
              bool(value['protection_errors']) and not value['protection_comparisons'])
    finally:
        ops.original.verify_plan, ops.original.legacy = saved_verify, saved_legacy

    cli = Path(episode.__file__).resolve()
    command = subprocess.run([sys.executable, '-E', '-B', str(cli), '--help'], capture_output=True)
    check('actual-cli-help', command.returncode == 0 and b'geometry-poll' in command.stdout)
    command = subprocess.run([sys.executable, '-O', '-B', str(cli), '--help'], capture_output=True)
    check('actual-cli-optimization-refused-before-operation', command.returncode != 0 and b'Use Python -E -B' in command.stderr)
    plan_path = out / 'wrong-episode-plan.json'
    bad = dict(plan, episode='B')
    plan_path.write_text(json.dumps(bad), encoding='utf8')
    receipt = out / 'wrong-episode-result.json'
    command = [sys.executable, '-E', '-B', str(cli), 'start', '--plan', str(plan_path),
               '--plan-sha256', ops.sha(plan_path), '--preflight', str(out / 'not-read'),
               '--preflight-sha256', '0' * 64, '--approval', str(out / 'not-read-approval'),
               '--approval-sha256', '0' * 64, '--session', str(out / 'not-contacted'), '--out', str(receipt)]
    run = subprocess.run(command, capture_output=True)
    check('actual-cli-b-refused-before-session-or-authority-read', run.returncode != 0 and
          json.loads(receipt.read_bytes())['state'] == 'CHECK_ERROR' and b'Only the approved Episode A' in run.stderr)
    (out / 'cli-stdout.txt').write_bytes(run.stdout)
    (out / 'cli-stderr.txt').write_bytes(run.stderr)
    sources = {str(p): ops.sha(p) for p in sorted(ops.ADAPTERS | {Path(__file__).resolve()})}
    result = dict(schema='sor-d5ai-a-timestamp-controls/1', tests=tests, passed=len(tests), sources=sources,
                  scope='Actual owned file/phase reads and CLI refusals; postflight/full-audit operands and process-independent controller dispatch are explicit models. No real preflight or native/retail execution.')
    ops.fresh(out / 'receipt.json', result)
    print(json.dumps(dict(passed=len(tests))))


if __name__ == '__main__':
    main()
