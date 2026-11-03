# SPDX-License-Identifier: GPL-3.0-or-later
"""D5AK actual disposable-worker integration and bounded adverse controls.

SOR-P-0002 adaptation of d5ai_native_controller_qualify.py. Executes only the
existing owned fixture host and unchanged 0.7.0 DLL; never Starfield. Reads the
exact prospective source-locked plan. Fixture target/phase validators replace
retail admission and preservation only, explicitly retaining actual process,
ownership, lock, worker, challenge, geometry, checkpoint and STOP mechanisms.
Writes new ignored fixture evidence and receipts. No saves/deployment/network.
"""
import sys
if not __debug__ or sys.flags.optimize:
    raise RuntimeError('Use the pinned Python interpreter with -E -B')

import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import shutil
import time
from types import SimpleNamespace

import d5ak_episode as episode
import d5ak_operations as operations
from d5ai_episode import ROOT, require, sha, read_json, poll_geometry
from d5ai_read_lifetime import validate_identity, read_prefix
from d5ai_read_geometry import read_session
from d5ai_operations import worker_json
from worker_health import disk_guard


def closeout():
    """Test modeled operations dispatch and actual native loss/archive paths."""
    build, plan_path, source, out = (Path(p).resolve() for p in sys.argv[2:6])
    require(out.is_relative_to(ROOT / '.local-work/d5ak') and not out.is_relative_to(source),
            'Fresh fixture closeout outside source required')
    disk_guard()
    out.mkdir(exist_ok=False)
    plan = read_json(plan_path)
    operations.source_pins(plan)
    checks = []
    from common import fresh, inventory

    # These are component routing controls with explicitly modeled full-audit
    # premises. They cannot establish a full retail preservation postflight.
    owned_guard = out / 'owned-archive-guard'
    owned_guard.write_bytes(b'owned modeled archive content')
    modeled = dict(protection=dict(archive_guard={str(owned_guard): {}}),
                   steam_cloud='historical', operator_confirmation_basis='historical')
    saved = (operations.verify_plan, operations.original.preflight, operations.content.postflight)
    calls = []
    try:
        operations.verify_plan = lambda value: calls.append(('verify', value))
        def preflight(value, digest, destination):
            calls.append(('preflight', value, digest, destination))
            return copy.deepcopy(modeled)
        operations.original.preflight = preflight
        value = operations.preflight(plan, sha(plan_path), out)
        require('steam_cloud' not in value and 'operator_confirmation_basis' not in value and
                value['protection']['archive_content_sha256'][str(owned_guard)] == sha(owned_guard) and
                value['d5ak_source_lock_sha256'] == plan['d5ak_source_lock_sha256'] and
                calls == [('verify', plan), ('preflight', plan, sha(plan_path), out)],
                'Modeled preflight routing or current/historical distinction failed')
        checks.append(dict(name='new preflight routes full audit and positively hashes archives', basis='MODELED full-audit premise; actual wrapper/content hash', passed=True))
        before, approval = dict(modeled_before=True), dict(modeled_approval=True)
        def postflight(value, initial, session, authority, destination):
            require((value, initial, session, authority, destination) == (plan, before, source, approval, out),
                    'Postflight arguments changed')
            return dict(status='MODELED_COMPONENT_RETURN_NO_RETAIL_CLAIM')
        operations.content.postflight = postflight
        result = operations.postflight(plan, before, source, approval, out)
        require(result['status'] == 'MODELED_COMPONENT_RETURN_NO_RETAIL_CLAIM', 'Postflight dispatch failed')
        checks.append(dict(name='new postflight routes exact content-protection finalization', basis='MODELED finalization and full-audit premises; actual wrapper', passed=True))
        def rejected(value):
            raise ValueError('modeled source-lock refusal')
        operations.verify_plan = rejected
        for name, action in (
                ('preflight', lambda: operations.preflight(plan, sha(plan_path), out)),
                ('postflight', lambda: operations.postflight(plan, before, source, approval, out))):
            try:
                action()
            except ValueError:
                checks.append(dict(name=name + ' source refusal before modeled effect', basis='MODELED verification failure; actual dispatch order', passed=True))
            else:
                raise RuntimeError('Source refusal was swallowed')
    finally:
        operations.verify_plan, operations.original.preflight, operations.content.postflight = saved

    # Actual native fault: the existing owned host retires its own worker through
    # its prequalified scenario. No process is terminated by this script.
    image, dll = (build / 'package-runtime' / name for name in ('sor-d5x-fixture.exe', 'SorConstructionWinner.dll'))
    require(sha(dll) == plan['dll_sha256'], 'Native fault fixture DLL mismatch')
    failed_session = out / 'unexpected-worker-exit'
    with (out / 'unexpected-worker.log').open('xb') as log:
        child = subprocess.Popen([str(image), str(dll), str(failed_session), 'd5ai-worker-exit'],
                                 stdout=log, stderr=subprocess.STDOUT, creationflags=subprocess.CREATE_NO_WINDOW)
        child.wait()
    require(child.returncode == 0 and not (failed_session / 'terminal.json').exists(),
            'Native unexpected-worker scenario did not preserve its expected missing terminal')
    identity = read_json(failed_session / 'identity.json')
    from worker_health import WorkerLease
    try:
        lease = WorkerLease(episode.original.strict_session_json(failed_session / 'ready.json'), identity)
    except (OSError, AssertionError):
        checks.append(dict(name='actual exited native worker cannot acquire live lease', basis='ACTUAL owned worker scenario/process/thread query', passed=True))
    else:
        lease.close()
        raise RuntimeError('Exited worker acquired a live lease')
    stopped = episode.EpisodeAController.__new__(episode.EpisodeAController)
    stopped.session, stopped.expected, stopped.lease = failed_session, identity, None
    require(stopped.poll()['state'] == 'EXIT_INCOMPLETE', 'Missing terminal invented a clean shutdown')
    checks.append(dict(name='actual missing terminal returns EXIT_INCOMPLETE', basis='ACTUAL native evidence; unadmitted no-lease poll', passed=True))

    # Authenticate and seal the complete existing native integration session.
    archive_path = ROOT / 'runtime/session-tools/archive.py'
    spec = importlib.util.spec_from_file_location('d5ak_owned_archive', archive_path)
    archive = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(archive)
    source_before = inventory(source)
    source_identity = read_json(source / 'identity.json')
    require(source_identity['retail'] is False, 'Fixture archive only')
    process_state = operations.original.legacy().original_process_gone(source_identity)
    require(process_state in ('GONE', 'EXITED', 'ORIGINAL_GONE_PID_REUSED'), 'Actual source process not gone')
    core = episode.checkpoint.reducer.read_capture.inspect(source, plan['dll_sha256'])
    geometry = read_session(source)
    terminal = worker_json(source / 'terminal.json')
    lifetime = read_prefix(source, terminal)
    require(core['complete_session'] and not geometry['errors'] and len(geometry['snapshots']) == 2,
            'Complete actual fixture evidence required')
    for snapshot in geometry['snapshots']:
        episode.checkpoint.reducer.d5ai_read_lifetime.qualify_snapshot(snapshot, lifetime)
    state = read_json(source / 'p4-state.json')
    stop = state['stop']
    require(state['identity_sha256'] == sha(source / 'identity.json') and
            stop['identity_sha256'] == state['identity_sha256'] and stop['owner'] == state['owner'] and
            (source / 'STOP').read_bytes() == (json.dumps(stop, sort_keys=True) + '\n').encode() and
            not state['telemetry_fault'] and terminal['resident_inert'], 'Owned STOP mismatch')
    controller_receipt = read_json(source.parent / 'qualification.json')
    require(controller_receipt['status'] == 'PASS' and controller_receipt['stop']['stop'] == stop,
            'Actual native controller receipt mismatch')
    companion = out / 'companion'
    companion.mkdir()
    fresh(companion / 'core.json', core)
    fresh(companion / 'geometry.json', geometry)
    fresh(companion / 'lifetime.json', lifetime)
    fresh(companion / 'owned-stop.json', stop)
    for name in ('qualification.json', 'baseline-certificate.json', 'comparison.json'):
        with (companion / ('actual-' + name)).open('xb') as stream:
            stream.write((source.parent / name).read_bytes())
    post = companion / 'fixture-postflight.json'
    fresh(post, dict(action='postflight', process_state=process_state, session=str(source),
                     status='PARTIAL_POSTFLIGHT', no_full_protection_audit=True,
                     no_retail_approval=True, scope='Actual fixture capture/STOP/exit authentication only'))
    roots = dict(capture=dict(path=str(source), kind='raw-capture'),
                 companion=dict(path=str(companion), kind='private-receipt'))
    fresh(out / 'roots.json', roots)
    reason = 'owned offline fixture; no full retail protection postflight'
    seal = archive.seal(roots, post, sha(post), reason)
    require(seal['status'] == 'PARTIAL', 'Fixture cannot imply retail postflight')
    exact = {'capture/' + name: row for name, row in source_before.items()}
    exact.update({'companion/' + name: row for name, row in inventory(companion).items()})
    require(exact == seal['files'], 'Archive omitted fixture evidence')
    fresh(out / 'seal.json', seal)
    destination = out / 'native-integration-lossless.zip'
    created = archive.create(out / 'seal.json', sha(out / 'seal.json'), destination)
    fresh(out / 'create.json', created)
    verified = archive.verify(destination, seal, sha(destination))
    fresh(out / 'verify.json', verified)
    require(inventory(source) == source_before and archive.collect(roots) == seal['files'], 'Source changed during archive')
    checks.append(dict(name='actual lossless seal/create/every-member stream verification', basis='ACTUAL exited native fixture; partial fixture postflight explicitly labeled', passed=True))
    fresh(out / 'qualification.json', dict(status='PASS', checks=checks,
          source_session=str(source), source_files=len(source_before), members=len(seal['files']),
          archive_sha256=sha(destination), process_state=process_state,
          original_tree='PRESERVED', full_retail_postflight='NOT TESTED',
          source_plan_sha256=sha(plan_path), final_free=disk_guard()))
    print(json.dumps(dict(status='PASS', checks=len(checks), members=len(seal['files']))))


class OwnedEpisodeController(episode.EpisodeAController):
    """Use real source pins; restrict all process actions to the owned host."""
    def validate_target(self, admission, approval):
        operations.source_pins(self.plan)
        require(self.expected['retail'] is False, 'Retail fixture forbidden')
        require(self.session.is_relative_to(ROOT / '.local-work/d5ak'), 'Task-local fixture required')
        require(Path(self.plan['process_image']).name == 'sor-d5x-fixture.exe', 'Owned fixture required')
        require(sha(self.plan['process_image']) == self.expected['host_sha256'], 'Host identity changed')
        require(sha(self.plan['dll']) == self.expected['dll_sha256'] == self.plan['dll_sha256'], 'DLL changed')
        validate_identity(self.expected)

    def validate_phase(self, admission):
        operations.source_pins(self.plan)
        disk_guard()


class OwnedFrozenFallback(episode.original.EpisodeController):
    """Exercise frozen STOP with only its exact trusted controller closure."""
    def validate_target(self, admission, approval):
        episode.original.verify_controller_pins(self.plan)
        require(self.expected['retail'] is False and
                self.session.is_relative_to(ROOT / '.local-work/d5ak') and
                Path(self.plan['process_image']).name == 'sor-d5x-fixture.exe',
                'Only the owned fallback fixture is permitted')
        require(sha(self.plan['process_image']) == self.expected['host_sha256'] and
                sha(self.plan['dll']) == self.expected['dll_sha256'], 'Fallback fixture identity mismatch')


def main():
    build, plan_path, out = (Path(p).resolve() for p in sys.argv[1:4])
    require(out.is_relative_to(ROOT / '.local-work/d5ak'), 'Fresh D5AK fixture output required')
    disk_guard()
    out.mkdir(exist_ok=False)
    plan_hash = sha(plan_path)
    plan = read_json(plan_path)
    operations.source_pins(plan)
    image = build / 'package-runtime/sor-d5x-fixture.exe'
    dll = build / 'package-runtime/SorConstructionWinner.dll'
    plan.update(process_image=str(image), dll=str(dll), plan_sha256=plan_hash)
    session = out / 'session'
    inputs = {str(p): sha(p) for p in (image, dll, plan_path, Path(__file__))}
    logs = [(out / name).open('xb') for name in ('host.stdout', 'host.stderr')]
    process = subprocess.Popen([str(image), str(dll), str(session), 'd5ai-controller-host'],
                               stdout=logs[0], stderr=logs[1], creationflags=subprocess.CREATE_NO_WINDOW)
    controller, states, checks = None, [], []
    result = dict(schema='sor-d5ak-integration-controls/1', inputs=inputs,
                  plan_sha256=plan_hash,
                  scope='Actual owned native worker with fixture admission; no retail protection rehearsal or live authority')

    def wait_file(name):
        while not (session / name).exists():
            if process.poll() is not None:
                raise RuntimeError('Owned host ended before ' + name)
            time.sleep(.01)

    def refuses(name, action):
        try:
            action()
        except (ValueError, KeyError):
            checks.append(dict(name=name, passed=True))
        else:
            raise RuntimeError('Missing refusal: ' + name)

    def fresh_health():
        controller.request()
        while True:
            value = controller.poll()
            if value['state'] == 'HEALTHY_ACK':
                return value
            require(value['state'] == 'ALIVE_ACK_PENDING', 'Unexpected actual worker health: ' + value['state'])
            time.sleep(.01)

    try:
        wait_file('ready.json')
        wait_file('fixture-controller-ready.json')
        identity = read_json(session / 'identity.json')
        controller = OwnedEpisodeController(session, identity, plan, {}, {}, 'start')
        refuses('A1 before A0 cannot arm', lambda: episode.arm_once(controller, 'A1'))
        for request, label in ((1, 'A0'), (2, 'A1')):
            while True:
                value = episode.arm_once(controller, label)
                states.append(value['state'])
                if value['state'] == 'GEOMETRY_ARMED':
                    break
                require(process.poll() is None, 'Host exited during arm handshake')
                time.sleep(.02)
            require(value['geometry_request']['arm_ack']['geometry_armed'] == request, 'Wrong one-shot arm ACK')
            (session / ('fixture-query-' + str(request))).write_bytes(b'one owned query\n')
            wait_file('geometry-request-' + str(request) + '.json')
            require(poll_geometry(controller)['state'] == 'GEOMETRY_CAPTURE_RECEIPT', 'Missing capture receipt')
            consumed = episode.arm_once(controller, label)
            require(consumed['state'] == 'GEOMETRY_ALREADY_CONSUMED' and
                    controller.state['geometry_last_request'] == request, 'Consumed arm was repeated')
            checks.append(dict(name=label + ' native arm ACK/query/consumed-label refusal', passed=True))
            if request == 1:
                health = fresh_health()
                nonce = health['ack']['request_nonce']
                args = SimpleNamespace(session=session, snapshot=1, nonce=nonce,
                                       target=episode.checkpoint.reducer.read_capture.TARGET,
                                       owner_formid='0005e0de', plan_sha256=plan_hash)
                cert = episode.qualify(args, plan)
                require(cert['state'] == 'BASELINE_PREFIX_QUALIFIED', 'Actual native prefix failed')
                require(not (session / 'terminal.json').exists(), 'Prefix only tested after terminal')
                again = episode.qualify(args, plan)
                require(again == cert, 'Repeated read-only interpretation differs')
                (out / 'baseline-certificate.json').write_text(json.dumps(cert, indent=2) + '\n', encoding='utf8', newline='\n')
                checks.append(dict(name='actual preterminal source-locked D5AJ checkpoint and identical read-only requalification', passed=True))
                for field, wrong in (('target', 'foreign-source'), ('owner_formid', '00000001')):
                    bad_args = copy.copy(args)
                    setattr(bad_args, field, wrong)
                    refuses('checkpoint rejects overridden ' + field,
                            lambda bad_args=bad_args: episode.qualify(bad_args, plan))
                    bad_compare = SimpleNamespace(session=session, target=bad_args.target,
                                                  owner_formid=bad_args.owner_formid,
                                                  before_snapshot=1, after_snapshot=2, plan_sha256=plan_hash)
                    refuses('comparison rejects overridden ' + field,
                            lambda bad_compare=bad_compare: episode.compare_session(bad_compare, plan))
                for field in ('state', 'identity_sha256', 'plan_sha256', 'snapshot_id', 'snapshot_sha256', 'method'):
                    bad = copy.deepcopy(cert)
                    bad[field] = 'foreign'
                    refuses('departure rejects wrong certificate ' + field,
                            lambda bad=bad: episode.departure_check(controller, bad, plan_hash))
                for branch, field in (('source', 'key'), ('source', 'body_formid'), ('frame', 'owner_formid')):
                    bad = copy.deepcopy(cert)
                    bad['envelope'][branch][field] = 'foreign'
                    refuses('departure rejects different-source certificate ' + branch + '.' + field,
                            lambda bad=bad: episode.departure_check(controller, bad, plan_hash))
                bad = copy.deepcopy(cert)
                bad['proof']['owner_context']['owner_formid'] = '00000001'
                refuses('departure rejects different proof owner', lambda: episode.departure_check(controller, bad, plan_hash))
                held = episode.departure_check(controller, cert, plan_hash)
                require(held['state'] == 'HOLD_DEPARTURE' and not held['automatic_stop'], 'Pending current health did not hold')
                checks.append(dict(name='healthy unchallenged departure HOLD preserves worker', passed=True))
                controller.request()
                while True:
                    value = episode.departure_check(controller, cert, plan_hash)
                    if value['state'] == 'BASELINE_AND_CURRENT_HEALTH_QUALIFIED':
                        break
                    require(value['state'] == 'HOLD_DEPARTURE' and process.poll() is None, 'Unexpected departure failure')
                    time.sleep(.01)
                owner = controller.state['owner']
                controller.close()
                controller = OwnedEpisodeController(session, identity, plan, {}, {}, 'request')
                require(controller.state['owner'] == owner and controller.state['d5ak_arms'] == {'A0': 1}, 'Reconnect lost owner or arm history')
                checks.append(dict(name='actual current challenge departure gate and reconnect persistence', passed=True))
        refuses('A0 cannot be rearmed after A1', lambda: episode.arm_once(controller, 'A0'))
        # The frozen STOP entry verifies only its original minimal controller
        # closure. A broken scientific lock must not remove that recovery route.
        fallback_plan = copy.deepcopy(plan)
        fallback_plan['d5aj_source_lock_sha256'] = '0' * 64
        refuses('new entry rejects altered scientific lock', lambda: operations.source_pins(fallback_plan))
        episode.original.verify_controller_pins(fallback_plan)
        bad_control = copy.deepcopy(fallback_plan)
        bad_control['controller_pins'][next(iter(bad_control['controller_pins']))] = '0' * 64
        refuses('frozen STOP refuses altered original controller source pin',
                lambda: episode.original.verify_controller_pins(bad_control))
        controller.close()
        controller = OwnedFrozenFallback(session, identity, fallback_plan, {}, {}, 'stop')
        result['stop'] = controller.request_stop('finite owned D5AK qualification via trusted frozen STOP fallback')
        checks.append(dict(name='actual frozen owned STOP succeeds despite refused D5AJ scientific lock', passed=True))
        controller.close()
        controller = None
        (session / 'fixture-controller-done').write_bytes(b'done\n')
        process.wait()
        require(process.returncode == 0, 'Host failed normal owned shutdown')
        terminal = worker_json(session / 'terminal.json')
        raw = read_session(session)
        lifetime = read_prefix(session, terminal)
        require(not raw['errors'] and len(raw['snapshots']) == 2 and lifetime['complete'], 'Incomplete actual fixture capture')
        require(terminal['geometry_completed'] == 2 and terminal['lifetime_drops'] == 0, 'Native recorder failure')
        compare_args = SimpleNamespace(session=session, target=args.target, owner_formid='0005e0de',
                                       before_snapshot=1, after_snapshot=2, plan_sha256=plan_hash)
        compared = episode.compare_session(compare_args, plan)
        require(compared['state'] == 'COMPARISON_REPORTED', 'Source-locked stopped comparison missing')
        (out / 'comparison.json').write_text(json.dumps(compared, indent=2) + '\n', encoding='utf8', newline='\n')
        checks.append(dict(name='actual stopped A0/A1 geometry/lifetime/availability comparison dispatch', passed=True))
        # Mutate only fresh disposable copies of the actual captured native
        # bytes. Each oracle runs the same source-locked checkpoint dispatch.
        def tamper(path):
            data = bytearray(path.read_bytes())
            data[0] ^= 1
            path.write_bytes(data)

        def edit_receipt(folder, name, field, value):
            path = folder / name
            row = episode.original.strict_session_json(path)
            row[field] = value
            path.write_text(json.dumps(row) + '\n', encoding='utf8', newline='\n')

        adverse = (
            ('missing-baseline', lambda folder: (folder / 'geometry-1.bin').unlink()),
            ('partial-baseline', lambda folder: edit_receipt(folder, 'geometry-1.json', 'flushed', False)),
            ('core-corruption', lambda folder: tamper(folder / 'events.bin')),
            ('lifetime-corruption', lambda folder: tamper(folder / 'lifetimes.bin')),
            ('geometry-corruption', lambda folder: tamper(folder / 'geometry-1.bin')),
            ('lost-core', lambda folder: (folder / 'events.bin').write_bytes(b'')),
            ('lost-lifetime', lambda folder: (folder / 'lifetimes.bin').unlink()),
            ('lifetime-loss-counter', lambda folder: edit_receipt(folder, 'ack-' + nonce + '.json', 'lifetime_drops', 1)),
            ('core-loss-counter', lambda folder: edit_receipt(folder, 'ack-' + nonce + '.json', 'drops', 1)),
        )
        for name, mutation in adverse:
            folder = out / name
            shutil.copytree(session, folder)
            mutation(folder)
            bad_args = copy.copy(args)
            bad_args.session = folder
            refuses('actual native copied bytes: ' + name, lambda bad_args=bad_args: episode.qualify(bad_args, plan))
        result.update(status='PASS', exit=process.returncode, snapshots=2,
                      lifetime_prefix_sha256=lifetime['raw_prefix_sha256'])
    except BaseException as error:
        result.update(status='FAIL', error=repr(error))
        raise
    finally:
        if controller is not None:
            try:
                controller.request_stop('owned D5AK fixture failure closeout')
            finally:
                controller.close()
        if session.exists() and process.poll() is None:
            # Disposable host-only cleanup, never a live Starfield STOP.
            if not (session / 'STOP').exists():
                (session / 'STOP').write_bytes(b'owned failed fixture STOP\n')
            (session / 'fixture-controller-done').touch(exist_ok=True)
            process.wait()
        for log in logs:
            log.close()
        result.update(checks=checks, states=states,
                      inputs_unchanged=all(sha(p) == digest for p, digest in inputs.items()))
        (out / 'qualification.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf8', newline='\n')
    print(json.dumps(dict(status=result['status'], checks=len(checks), snapshots=result['snapshots'])))


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'closeout':
        closeout()
    else:
        main()
