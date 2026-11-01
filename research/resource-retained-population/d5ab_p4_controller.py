# SPDX-License-Identifier: GPL-3.0-or-later
"""Qualify the P4 controller with the unchanged actual disposable DLL worker.

Reads an existing P3 build and owned controller/consumer sources. Writes only
fresh ignored P4 fixture sessions and receipts. Deliberate faults affect the
self-created host only. No retail process, deployment, saves or network access.
Synthetic receipt damage is labeled and original bytes retained separately.
"""

import sys

# Safety checks below require assertions, including when imported as a helper.
if not __debug__ or sys.flags.optimize != 0:
    raise RuntimeError('Python optimization is forbidden; invoke with -E -B and no -O/-OO')
import json
import os
from pathlib import Path
import subprocess
import time
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'runtime/construction-winner'
sys.path.insert(0, str(SRC))
from p4_controller import SessionController, RetailController, sha, write_new, LIVE
from worker_health import read_json, disk_guard
from read_capture import inspect


class FixtureController(SessionController):
    def validate_target(self, admission, approval):
        assert self.expected['retail'] is False
        assert self.session.is_relative_to(ROOT / '.local-work/d5x')
        assert Path(self.plan['process_image']).name == 'sor-d5x-fixture.exe'


def wait(predicate, seconds=180):
    end = time.monotonic() + seconds
    while time.monotonic() < end:
        value = predicate()
        if value:
            return value
        time.sleep(0.01)
    raise AssertionError('Disposable test stimulus did not finish; not a live cutoff')


def main():
    build, label = Path(sys.argv[1]).resolve(), sys.argv[2]
    assert label.replace('-', '').isalnum()
    disk_guard()
    out = ROOT / '.local-work/d5ab' / label
    sessions = ROOT / '.local-work/d5x' / label
    out.mkdir(exist_ok=False)
    sessions.mkdir(exist_ok=False)
    source_paths = [Path(__file__), *[SRC / p for p in ('p4_controller.py', 'controller.py', 'worker_health.py',
                                                     'read_capture.py', 'reduce_v3.py', 'reduce_v4.py')]]
    inputs = {str(p): sha(p) for p in source_paths}
    for p in source_paths:
        target = out / 'sources' / p.relative_to(ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(p.read_bytes())
    package = build / 'package-runtime'
    plan = dict(process_image=str(package / 'sor-d5x-fixture.exe'))
    cases = ('normal reconnect retry publish-race slow duplicate-owner wrong-image stale-identity retained-session postexit '
             'telemetry-generation telemetry-causes telemetry-regression telemetry-retained bad-ack bad-ack-bool bad-ack-count '
             'stop-disk-failure foreign-stop write raw-flush ack-flush ack-write disk guard exit missing-terminal loss').split()
    if len(sys.argv) > 3:
        cases = sys.argv[3:]
    results = []
    for case in cases:
        disk_guard()
        session = sessions / case
        log = (out / (case + '.log')).open('xb')
        command = [plan['process_image'], str(package / 'SorConstructionWinner.dll'), str(session), 'controller-host']
        process = subprocess.Popen(command, stdout=log, stderr=subprocess.STDOUT)
        controller = None
        row = dict(case=case, command=command, passed=False)
        try:
            wait(lambda: (session / 'host-online.json').exists())
            expected = read_json(session / 'identity.json')
            assert expected['pid'] == process.pid and expected['dll_sha256'] == sha(package / 'SorConstructionWinner.dll')
            controller = FixtureController(session, expected, plan, {}, {}, 'start')
            def fresh():
                controller.request()
                def ready():
                    value = controller.poll()
                    if value['state'] == 'ALIVE_ACK_PENDING':
                        controller.request()
                        return None
                    return value
                return wait(ready)
            assert fresh()['state'] == 'HEALTHY_ACK'
            states = ['HEALTHY_ACK']
            def stimulate(action):
                pending = session / ('fixture-' + action + '.pending')
                pending.write_bytes(action.encode())
                pending.rename(session / 'fixture-command.txt')
                wait(lambda: (session / ('command-' + action + '.json')).exists())
            if case == 'reconnect':
                owner = controller.state['owner']
                controller.close()
                controller = FixtureController(session, expected, plan, {}, {}, 'request')
                assert controller.state['owner'] == owner
                assert fresh()['state'] == 'HEALTHY_ACK'
                states.append('RECONNECTED_SAME_OWNER')
            elif case == 'retry':
                nonce = controller.request()['nonce']
                assert controller.request()['nonce'] == nonce
                controller.close()
                controller = FixtureController(session, expected, plan, {}, {}, 'request')
                assert controller.request()['nonce'] == nonce
                assert wait(lambda: value if (value := controller.poll())['state'] != 'ALIVE_ACK_PENDING' else None)['state'] == 'HEALTHY_ACK'
                states.append('RETRY_SAME_NONCE_AFTER_RECONNECT')
            elif case == 'slow':
                stimulate('pause')
                time.sleep(0.15)
                controller.request()
                assert controller.poll()['state'] == 'ALIVE_ACK_PENDING'
                time.sleep(1.1)
                assert controller.poll()['state'] == 'ALIVE_ACK_PENDING'
                assert wait(lambda: value if (value := controller.poll())['state'] != 'ALIVE_ACK_PENDING' else None)['state'] == 'HEALTHY_ACK'
                states.append('SLOW_WORKER_REMAINS_ALIVE')
            elif case == 'publish-race':
                original_replace = os.replace
                def race(source, destination):
                    if Path(destination).name == 'request.txt':
                        raise PermissionError('modeled sharing race at publication')
                    return original_replace(source, destination)
                with patch('p4_controller.os.replace', side_effect=race):
                    pending = controller.request()
                    assert pending['state'] == 'REQUEST_PUBLICATION_PENDING'
                assert controller.request()['nonce'] == pending['nonce']
                assert wait(lambda: value if (value := controller.poll())['state'] != 'ALIVE_ACK_PENDING' else None)['state'] == 'HEALTHY_ACK'
                states.append('PUBLICATION_RACE_RETRIES_IDENTICAL_NONCE')
            elif case in ('duplicate-owner', 'wrong-image', 'stale-identity', 'retained-session'):
                bad_expected, bad_plan = dict(expected), dict(plan)
                admission = {}
                action = 'request'
                if case == 'wrong-image':
                    bad_plan['process_image'] = str(SRC / 'sor-d5x-fixture.exe')
                elif case == 'stale-identity':
                    bad_expected['creation_filetime'] += 1
                elif case == 'retained-session':
                    admission = dict(existing_sessions=[session.name])
                    action = 'start'
                try:
                    duplicate = FixtureController(session, bad_expected, bad_plan, admission, {}, action)
                except (AssertionError, OSError):
                    states.append('REJECTED_' + case)
                else:
                    duplicate.close()
                    raise AssertionError('Incorrect admission or simultaneous owner accepted')
            elif case.startswith(('telemetry-', 'bad-ack')):
                controller.request()
                path = session / ('ack-' + controller.state['challenge'] + '.json')
                wait(path.exists)
                original = path.read_bytes()
                (out / (case + '-original-ack.json')).write_bytes(original)
                ack = json.loads(original)
                if case == 'telemetry-generation':
                    ack['loss_generation'] += 1
                elif case == 'telemetry-causes':
                    ack['queue_full'] += 1
                elif case == 'telemetry-regression':
                    controller.state['last_ack'] = dict(ack, drops=1, queue_full=1, loss_generation=1)
                elif case == 'telemetry-retained':
                    original_loss = json.loads((build / 'stop-under-production/flush.jsonl').read_bytes().splitlines()[2])
                    keys = ('drops', 'queue_full', 'contention_exhausted', 'reentrant_losses', 'loss_generation',
                            'first_loss_sampled_admission', 'last_loss_sampled_admission', 'loss_bounds_uncertain')
                    ack.update({key: original_loss[key] for key in keys})
                    row['replayed_actual_sample'] = dict(source=str(build / 'stop-under-production/flush.jsonl'),
                                                        sha256=sha(build / 'stop-under-production/flush.jsonl'), line=3,
                                                        tuple={key: original_loss[key] for key in keys})
                elif case == 'bad-ack-bool':
                    ack['hooks_intact'] = 'true'
                elif case == 'bad-ack-count':
                    ack['acknowledged'] = True
                else:
                    ack['request_nonce'] = 'f' * 32
                write_new(out / (case + '-modeled-ack.json'), ack)
                # The current worker supplies the real identity/challenge and
                # stays unchanged. Inject damaged metadata at the consumer read
                # boundary instead of racing a native published receipt handle.
                real_read = read_json
                with patch('p4_controller.read_json', side_effect=lambda p: ack if Path(p) == path else real_read(p)):
                    if case.startswith('bad-ack'):
                        try:
                            controller.poll()
                        except AssertionError:
                            states.append('ACK_IDENTITY_REJECTED')
                        else:
                            raise AssertionError('Wrong challenge accepted')
                    else:
                        response = controller.poll()
                        assert response['state'] == 'TELEMETRY_INCONSISTENT'
                        assert response['scientific_firstness_qualified'] is False
                if case.startswith('telemetry-'):
                    assert fresh()['state'] == 'TELEMETRY_INCONSISTENT'
                    states.append('TELEMETRY_FAULT_STICKY_NO_FIRSTNESS')
            elif case == 'stop-disk-failure':
                with patch('p4_controller.disk_guard', side_effect=AssertionError('simulated caller disk floor failure')):
                    try:
                        controller.request()
                    except AssertionError:
                        states.append('REQUEST_DISK_REFUSED')
                    else:
                        raise AssertionError('Request bypassed disk floor')
                    assert controller.request_stop('offline floor control')['state'] == 'STOP_REQUESTED'
                    assert controller.request_stop('retry STOP')['state'] == 'STOP_REQUESTED'
                states.append('STOP_BYPASSES_DISK_SAME_BYTES')
            elif case == 'foreign-stop':
                (session / 'STOP').write_bytes(b'foreign stop')
                try:
                    controller.request_stop('control')
                except AssertionError:
                    states.append('FOREIGN_STOP_REJECTED')
                else:
                    raise AssertionError('Foreign STOP accepted')
            elif case in ('write', 'raw-flush', 'ack-flush', 'ack-write', 'disk', 'guard', 'exit', 'missing-terminal', 'loss'):
                stimulate(case)
                if case == 'loss':
                    assert fresh()['state'] == 'ALIVE_LOSS'
                    states.append('LOSS_REPORTED_NO_FIRSTNESS')
            if case not in ('foreign-stop', 'write', 'raw-flush', 'ack-flush', 'ack-write', 'disk', 'guard', 'exit') and controller.state['stop'] is None:
                controller.request_stop('offline qualification STOP')
            final = wait(lambda: value if (value := controller.poll())['state'] in
                         ('EXIT_FAULT', 'EXIT_INCOMPLETE', 'EXIT_UNOWNED_STOP', 'RETIRED_PENDING_POSTFLIGHT') else None)
            wanted = ('EXIT_FAULT' if case in ('write', 'raw-flush', 'ack-flush', 'ack-write', 'disk', 'guard')
                      else 'EXIT_INCOMPLETE' if case in ('exit', 'missing-terminal')
                      else 'RETIRED_PENDING_POSTFLIGHT')
            if case == 'foreign-stop':
                # Refusal is decisive; foreign STOP has no successful owned closeout.
                wanted = 'EXIT_UNOWNED_STOP'
            assert final['state'] == wanted, (case, final, wanted)
            assert final['raw_verified'] is False
            assert process.wait(timeout=20) == 0
            if case == 'postexit':
                controller.close()
                controller = FixtureController(session, expected, plan, {}, {}, 'poll')
                assert controller.poll()['state'] == 'RETIRED_PENDING_POSTFLIGHT'
                assert controller.process_state in ('PROCESS_EXITED', 'PROCESS_UNAVAILABLE_PENDING_POSTFLIGHT')
                states.append('POSTEXIT_RECONNECT_PENDING_POSTFLIGHT')
            states.append(final['state'])
            reduced = inspect(session, expected['dll_sha256'])
            row['offline_consumer'] = {k: reduced[k] for k in ('complete_session', 'durable_records', 'damage')}
            row.update(passed=True, states=states)
        except BaseException as error:
            import traceback
            row['error'] = repr(error)
            row['traceback'] = traceback.format_exc()
        finally:
            if controller:
                controller.close()
            if process.poll() is None and session.exists() and not (session / 'STOP').exists():
                (session / 'STOP').write_bytes(b'offline fixture cleanup')
            try:
                row['exit'] = process.wait(timeout=25)
            except subprocess.TimeoutExpired:
                row['cleanup'] = 'Self-created host still alive; no kill performed'
            log.close()
            row['files'] = {str(p.relative_to(session)): sha(p) for p in session.rglob('*') if p.is_file()}
            results.append(row)
            unchanged = all(sha(p) == digest for p, digest in inputs.items())
            write = dict(schema='sor-d5ab-p4-controller-qualification/1', inputs=inputs, build=str(build),
                         dll_sha256=sha(package / 'SorConstructionWinner.dll'), results=results,
                         source_unchanged=unchanged,
                         passed=unchanged and all(r['passed'] for r in results))
            (out / 'receipt.json').write_text(json.dumps(write, indent=2) + '\n', encoding='utf8', newline='\n')
        assert row['passed'], row
        assert unchanged, 'Test/adapter/consumer source changed during execution'
    print(json.dumps(dict(cases=len(results), passed=True, out=str(out))))


if __name__ == '__main__':
    if sys.argv[1] == '--parallel':
        from concurrent.futures import ThreadPoolExecutor
        build, label = sys.argv[2:4]
        out = ROOT / '.local-work/d5ab' / label
        out.mkdir(exist_ok=False)
        cases = ('normal reconnect retry publish-race slow duplicate-owner wrong-image stale-identity retained-session postexit '
                 'telemetry-generation telemetry-causes telemetry-regression telemetry-retained bad-ack bad-ack-bool bad-ack-count '
                 'stop-disk-failure foreign-stop write raw-flush ack-flush ack-write disk guard exit missing-terminal loss').split()
        def run(case):
            result = subprocess.run([sys.executable, '-E', '-B', str(Path(__file__)), build, label + '-' + case, case], capture_output=True)
            (out / (case + '.stdout')).write_bytes(result.stdout)
            (out / (case + '.stderr')).write_bytes(result.stderr)
            receipt = ROOT / '.local-work/d5ab' / (label + '-' + case) / 'receipt.json'
            return dict(case=case, exit=result.returncode, receipt=str(receipt),
                        receipt_sha256=sha(receipt) if receipt.exists() else None)
        with ThreadPoolExecutor(max_workers=8) as pool:
            results = list(pool.map(run, cases))
        write_new(out / 'receipt.json', dict(results=results, passed=all(r['exit'] == 0 for r in results)))
        print(json.dumps(results))
        assert all(r['exit'] == 0 for r in results)
    else:
        main()
