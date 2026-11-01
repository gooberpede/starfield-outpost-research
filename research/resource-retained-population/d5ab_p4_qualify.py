# SPDX-License-Identifier: GPL-3.0-or-later
"""Exercise P4 protection/archival procedures with disposable evidence.

Reads unchanged P3 positive raw evidence, owned phase/archive/policy functions.
Writes fresh ignored copies, mutated negative controls, ZIPs and test receipts.
No protected original write, game, deployment, network or dependency download.
Actual archive disk guards run; protection adverse cases use synthetic inputs.
"""

import sys

# Safety checks below require assertions, including when imported as a helper.
if not __debug__ or sys.flags.optimize != 0:
    raise RuntimeError('Python optimization is forbidden; invoke with -E -B and no -O/-OO')
import copy
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'runtime/session-tools'))
sys.path.insert(0, str(ROOT / 'runtime/construction-winner'))
import archive
from common import fresh, guard, sha
from read_capture import inspect
import d5ab_p4_operations as ops


def main():
    out = (ROOT / sys.argv[1]).resolve()
    assert out.is_relative_to(ROOT / '.local-work/d5ab')
    out.mkdir(parents=True, exist_ok=False)
    guard()
    rows = []
    def check(name, value):
        rows.append(dict(case=name, passed=bool(value)))
        assert value, name
    def rejects(name, call):
        try:
            call()
        except (AssertionError, OSError, ValueError, zipfile.BadZipFile):
            check(name, True)
        else:
            check(name, False)
    raw = out / 'raw'
    source = ROOT / '.local-work/d5x/p3-native-final04/p3-positive-bypass'
    originals = {p.name: sha(p) for p in source.iterdir() if p.is_file()}
    shutil.copytree(source, raw)
    dll = sha(ROOT / '.local-work/d5x/p3-native-final04/package-runtime/SorConstructionWinner.dll')
    result = inspect(raw, dll)
    check('actual-final04-positive-chain', result['complete_session'] and len(result['chains']) == 1)
    companions = out / 'companions'
    companions.mkdir()
    post = companions / 'postflight.json'
    fresh(post, dict(action='postflight', process_state='EXITED', session=str(raw),
                     status='PASS_POSTFLIGHT', scope='Disposable archived P3 replay, no B2'))
    roots = {'raw': dict(path=str(raw), kind='raw-capture'),
             'receipts': dict(path=str(companions), kind='private-receipt')}
    seal_value = archive.seal(roots, post, sha(post))
    seal = out / 'seal.json'
    fresh(seal, seal_value)
    zipped = out / 'capture.zip'
    receipt = archive.create(seal, sha(seal), zipped)
    check('actual-archive-create-verify', receipt['status'] == 'VERIFIED_EVERY_MEMBER')
    verified = archive.verify(zipped, seal_value, sha(zipped))
    check('independent-stream-verification', verified['status'] == 'VERIFIED_EVERY_MEMBER')
    restored = out / 'reconstruction'
    restored.mkdir()
    with zipfile.ZipFile(zipped) as z:
        for name, row in seal_value['files'].items():
            target = restored / name
            target.parent.mkdir(parents=True, exist_ok=True)
            with z.open(name) as src, target.open('xb') as dst:
                shutil.copyfileobj(src, dst)
            check('reconstruct-' + name, sha(target) == row['sha256'])
    check('reconstructed-reader-equality', inspect(restored / 'raw', dll) == result)
    damaged = out / 'damaged.zip'
    payload = bytearray(zipped.read_bytes())
    payload[len(payload) // 2] ^= 255
    damaged.write_bytes(payload)
    rejects('damaged-archive-pin-refused', lambda: archive.verify(damaged, seal_value, sha(zipped)))
    truncated = out / 'truncated.zip'
    truncated.write_bytes(zipped.read_bytes()[:-30])
    rejects('truncated-archive-refused', lambda: archive.verify(truncated, seal_value))
    terminal = raw / 'terminal.json'
    terminal.write_bytes(b'{}')
    rejects('changed-sealed-source-refused', lambda: archive.create(seal, sha(seal), out / 'changed-source.zip'))
    check('original-capture-preserved', originals == {p.name: sha(p) for p in source.iterdir() if p.is_file()})

    # Exercise the exact lightweight function against disposable native-name files.
    module = ops.policy_module()
    saves = out / 'saves'
    remote = out / 'remote'
    saves.mkdir(); remote.mkdir()
    name = 'Save1_ABCD1234M41_000000_20261031010000_1_1_4.sfs'
    (saves / name).write_bytes(b'disposable; not a game save')
    policy = module.load_policy()
    config = out / 'test.ini'; config.write_bytes(b'fixture')
    definition = out / 'definition.esm'; definition.write_bytes(b'definition fixture')
    installed = out / 'installed.asset'; installed.write_bytes(b'A' * (1024 * 1024))
    sfse = out / 'sfse.dll'; sfse.write_bytes(b'fixture')
    plugins = out / 'Plugins'; plugins.mkdir()
    deployed = plugins / 'SorConstructionWinner.dll'; deployed.write_bytes(b'fixture')
    protection = dict(save_policy_sha256=module.policy_hash(policy),
        protected_live=module.snapshot(saves, policy), live_path=str(saves),
        config={str(config):sha(config)}, definitions={str(definition):sha(definition)},
        file_guards={str(p):dict(bytes=p.stat().st_size, mtime_ns=p.stat().st_mtime_ns)
                     for p in (config, definition)},
        installed={str(installed):dict(bytes=installed.stat().st_size,
                   mtime_ns=installed.stat().st_mtime_ns, sha256=sha(installed))})
    preflight = dict(protection=protection, remote_protected_sizes={str(remote):{}})
    plan = dict(sfse_path=str(sfse), sfse_sha256=sha(sfse), deployed_dll=str(deployed), dll_sha256=sha(deployed))
    plan['phase_pins'] = {str(ROOT / name):sha(ROOT / name) for name in (
        'runtime/session-tools/common.py',
        'research/resource-carinae-source-context/save_policy.py',
        'research/resource-retained-population/d5ab_p4_operations.py')}
    check('lightweight-native-grammar-positive', ops.lightweight(plan, preflight)['state'] == 'PASS_LIGHTWEIGHT')
    # Configuration content is checked even when all metadata still matches.
    # Existing tool/DLL pin checks remain; save and installed-asset payloads must
    # not join this small configuration-content read path.
    hash_reads = []
    real_sha = ops.sha
    def observe_hash(path):
        path = Path(path).resolve()
        assert not path.is_relative_to(saves.resolve())
        assert not path.is_relative_to(remote.resolve())
        assert path != installed.resolve()
        assert path != definition.resolve()
        hash_reads.append(dict(path=str(path), bytes=path.stat().st_size))
        return real_sha(path)
    with patch.object(ops, 'sha', side_effect=observe_hash):
        normal = ops.lightweight(plan, preflight)
    check('configuration-always-hashed-with-unchanged-metadata',
          normal['configuration_content_rehashed'] is True and
          normal['configuration_timestamp_changes'] == [] and
          sum(row['path'] == str(config.resolve()) for row in hash_reads) == 1)
    check('lightweight-hashes-no-save-or-installed-asset-payload',
          all(row['path'] != str(installed.resolve()) and
              row['path'] != str(definition.resolve()) and
              not Path(row['path']).is_relative_to(saves.resolve()) and
              not Path(row['path']).is_relative_to(remote.resolve()) for row in hash_reads))
    config_stat = config.stat()
    os.utime(config, ns=(config_stat.st_atime_ns, config_stat.st_mtime_ns + 1_000_000_000))
    timestamp_only = ops.lightweight(plan, preflight)
    check('configuration-timestamp-only-change-accepted',
          timestamp_only['state'] == 'PASS_LIGHTWEIGHT' and
          timestamp_only['configuration_timestamp_changes'] == [str(config)] and
          sha(config) == protection['config'][str(config)])
    config.write_bytes(b'changed')
    os.utime(config, ns=(config_stat.st_atime_ns, config_stat.st_mtime_ns))
    check('changed-config-retains-original-size-and-mtime',
          config.stat().st_size == config_stat.st_size and
          config.stat().st_mtime_ns == config_stat.st_mtime_ns)
    rejects('configuration-same-size-restored-mtime-content-change-refused',
            lambda: ops.lightweight(plan, preflight))
    config.write_bytes(b'fixture')
    os.utime(config, ns=(config_stat.st_atime_ns, config_stat.st_mtime_ns))
    config.unlink()
    rejects('missing-configuration-file-refused', lambda: ops.lightweight(plan, preflight))
    config.write_bytes(b'fixture')
    os.utime(config, ns=(config_stat.st_atime_ns, config_stat.st_mtime_ns))
    for label, digest in (('absent', None), ('empty', ''), ('wrong', '0' * 64)):
        missing_pin = copy.deepcopy(preflight)
        if label == 'absent':
            missing_pin['protection']['config'].pop(str(config))
        else:
            missing_pin['protection']['config'][str(config)] = digest
        rejects('configuration-' + label + '-pin-refused',
                lambda value=missing_pin: ops.lightweight(plan, value))
    null_pin = copy.deepcopy(preflight)
    null_pin['protection']['config'][str(config)] = None
    rejects('configuration-null-pin-refused', lambda: ops.lightweight(plan, null_pin))
    ambiguous = copy.deepcopy(preflight)
    ambiguous['protection']['definitions'][str(config)] = sha(config)
    rejects('ambiguous-config-definition-roster-refused', lambda: ops.lightweight(plan, ambiguous))
    incomplete = copy.deepcopy(preflight)
    incomplete['protection']['file_guards'].pop(str(config))
    rejects('configuration-missing-size-guard-refused', lambda: ops.lightweight(plan, incomplete))
    definition_stat = definition.stat()
    os.utime(definition, ns=(definition_stat.st_atime_ns, definition_stat.st_mtime_ns + 1_000_000_000))
    rejects('definition-timestamp-change-still-refused', lambda: ops.lightweight(plan, preflight))
    os.utime(definition, ns=(definition_stat.st_atime_ns, definition_stat.st_mtime_ns))
    installed_stat = installed.stat()
    os.utime(installed, ns=(installed_stat.st_atime_ns, installed_stat.st_mtime_ns + 1_000_000_000))
    rejects('installed-asset-timestamp-change-still-refused', lambda: ops.lightweight(plan, preflight))
    os.utime(installed, ns=(installed_stat.st_atime_ns, installed_stat.st_mtime_ns))
    # A real disposable directory junction tests ancestor rejection without
    # requiring file-symlink privileges. Remove only the junction entry afterward.
    real_config = out / 'real-config'; real_config.mkdir()
    (real_config / config.name).write_bytes(b'fixture')
    junction = out / 'linked-config'
    made = subprocess.run(['cmd', '/d', '/c', 'mklink', '/J', str(junction), str(real_config)],
                          capture_output=True)
    (out / 'junction.stdout').write_bytes(made.stdout)
    (out / 'junction.stderr').write_bytes(made.stderr)
    check('disposable-configuration-junction-created', made.returncode == 0 and junction.is_junction())
    try:
        linked = junction / config.name
        reparse = copy.deepcopy(preflight)
        reparse['protection']['config'] = {str(linked):sha(real_config / config.name)}
        reparse['protection']['file_guards'].pop(str(config))
        reparse['protection']['file_guards'][str(linked)] = dict(
            bytes=linked.stat().st_size, mtime_ns=linked.stat().st_mtime_ns)
        rejects('configuration-junction-ancestor-refused', lambda: ops.lightweight(plan, reparse))
    finally:
        assert junction.resolve().is_relative_to(out) and junction.is_relative_to(out)
        os.rmdir(junction)
    check('junction-removal-preserves-target', not junction.exists() and (real_config / config.name).is_file())
    real_is_symlink = Path.is_symlink
    with patch.object(Path, 'is_symlink', lambda path: path == config or real_is_symlink(path)):
        rejects('configuration-file-symlink-refused-modeled', lambda: ops.lightweight(plan, preflight))
    bad = copy.deepcopy(plan)
    bad['phase_pins'][str(ROOT / 'runtime/session-tools/common.py')] = '0' * 64
    rejects('lightweight-helper-drift-refused', lambda: ops.lightweight(bad, preflight))
    auto = saves / 'Exitsave0_ABCD1234M41_000000_20261031010000_1_1_4.sfs'
    auto.write_bytes(b'new transient')
    check('transient-addition-diagnostic', ops.lightweight(plan, preflight)['state'] == 'PASS_LIGHTWEIGHT')
    (saves / 'unknown.sfs').write_bytes(b'unknown')
    rejects('unknown-save-refused', lambda: ops.lightweight(plan, preflight))
    (saves / 'unknown.sfs').unlink()
    (remote / name).write_bytes(b'new protected remote')
    rejects('remote-addition-refused', lambda: ops.lightweight(plan, preflight))
    (remote / name).unlink()
    (saves / name).write_bytes(b'changed size')
    rejects('protected-size-change-refused', lambda: ops.lightweight(plan, preflight))
    (saves / name).write_bytes(b'disposable; not a game save')
    deployed.write_bytes(b'changed')
    rejects('deployed-mismatch-refused', lambda: ops.lightweight(plan, preflight))
    deployed.write_bytes(b'fixture')
    (plugins / 'SorOther.dll').write_bytes(b'fixture')
    rejects('competing-observer-refused', lambda: ops.lightweight(plan, preflight))
    (plugins / 'SorOther.dll').unlink()
    config.write_bytes(b'changed')
    rejects('config-change-refused', lambda: ops.lightweight(plan, preflight))
    # Full comparison must detect content change, not only the lighter size gate.
    before = {key: 'stable' for key in ('save_policy_sha256','protected_live','backups',
              'definitions','config','archive_guard','restore_rehearsal_sha256')}
    check('full-protection-comparison-positive', ops.compare_protection(before, copy.deepcopy(before))['equal'])
    after = copy.deepcopy(before); after['protected_live'] = 'different-hash'
    rejects('full-protected-content-change-refused', lambda: ops.compare_protection(before, after))
    check('full-no-game-check', ops.no_game() is None)
    import p4_controller
    identity = json.loads((source / 'identity.json').read_bytes())
    identity.update(retail=True, host_sha256='game', sfse_sha256='sfse', module_base=4096)
    pins = [dict(index=i, rva=i * 32, guard_sha256='fixture') for i in range(18)]
    identity['sites'] = [dict(row, va=4096 + row['rva']) for row in pins]
    session = out / ('session-' + identity['nonce']); session.mkdir()
    fresh(session / 'identity.json', identity)
    identity_hash = sha(session / 'identity.json')
    synthetic_plan = dict(game_sha256='game', sfse_sha256='sfse', dll_sha256=dll,
                          process_image='Starfield.exe', sites=pins, plan_sha256='plan')
    admission = dict(state='PASS_OFFLINE_PREFLIGHT', plan_sha256='plan',
                     receipt_sha256='preflight', existing_sessions=[])
    approval = dict(authority='B2_EXPLICIT_MAINTAINER_GO', plan_sha256='plan',
                    preflight_sha256='preflight', session=str(session),
                    identity_sha256=identity_hash, one_process_one_load_one_direct_travel=True)
    state = dict(identity_sha256=identity_hash, owner='b' * 32, telemetry_fault=False,
                 stop=dict(identity_sha256=identity_hash, owner='b' * 32, stop_nonce='c' * 32))
    fresh(session / 'p4-state.json', state)
    (session / 'STOP').write_bytes((json.dumps(state['stop'], sort_keys=True) + '\n').encode())
    fresh(session / 'terminal.json', dict(identity, resident_inert=True))
    with patch.object(p4_controller, 'LIVE', out):
        check('owned-postflight-binding-positive', bool(ops.finalization(synthetic_plan, admission, session, approval)))
        wrong = dict(approval, identity_sha256='wrong')
        rejects('postflight-wrong-approval-refused', lambda: ops.finalization(synthetic_plan, admission, session, wrong))
        stale = dict(admission, existing_sessions=[session.name])
        rejects('postflight-old-session-refused', lambda: ops.finalization(synthetic_plan, stale, session, approval))
        (session / 'STOP').write_bytes(b'foreign STOP')
        rejects('postflight-foreign-stop-refused', lambda: ops.finalization(synthetic_plan, admission, session, approval))
        (session / 'STOP').write_bytes((json.dumps(state['stop'], sort_keys=True) + '\n').encode())
        state['telemetry_fault'] = True
        (session / 'p4-state.json').write_text(json.dumps(state), encoding='utf8')
        rejects('postflight-telemetry-fault-refused', lambda: ops.finalization(synthetic_plan, admission, session, approval))
    bad_plan = out / 'bad-plan.json'; fresh(bad_plan, {})
    command = [sys.executable, '-E', '-B', str(Path(ops.__file__)), 'preflight',
               '--plan', str(bad_plan), '--plan-sha256', '0' * 64,
               '--out', str(out / 'failed-preflight')]
    failed = subprocess.run(command, capture_output=True)
    (out / 'failed-preflight.stderr').write_bytes(failed.stderr)
    check('cli-failure-durable-receipt', failed.returncode != 0 and
          json.loads((out / 'failed-preflight/receipt.json').read_bytes())['state'] == 'CHECK_ERROR')
    launch = out / 'launch-pins'; launch.mkdir()
    for name in ('Starfield.exe', 'sfse_loader.exe', 'sfse_1_16_244.dll',
                 'Starfield.esm', 'Starfield - PlanetData.ba2'):
        (launch / name).write_bytes(b'Disposable pin bytes; not a game/tool binary')
    launch_plan = dict(schema='sor-d5ab-p4-plan/1', package_pins={},
                       operations_sha256=sha(ops.__file__),
                       launch_pins={str(p):sha(p) for p in launch.iterdir()})
    check('all-five-prelaunch-pins-positive', ops.verify_plan(launch_plan) is None)
    (launch / 'sfse_loader.exe').write_bytes(b'changed disposable loader')
    rejects('changed-prelaunch-loader-refused', lambda: ops.verify_plan(launch_plan))
    receipt = dict(schema='sor-d5ab-p4-procedure-tests/1', passed=all(r['passed'] for r in rows),
        rows=rows, driver_sha256=sha(__file__), operations_sha256=sha(ops.__file__),
        archive_sha256=sha(archive.__file__), raw_source=str(source), original_hashes=originals,
        lightweight_hash_reads=hash_reads,
        seal_sha256=sha(seal), zip_sha256=sha(zipped),
        scope='Offline disposable controls; synthetic approval fields test validators only and authorize no retail operation')
    fresh(out / 'receipt.json', receipt)
    print(json.dumps(dict(passed=receipt['passed'], tests=len(rows), out=str(out))))


if __name__ == '__main__':
    main()
