# SPDX-License-Identifier: GPL-3.0-or-later
"""Exercise the actual DLL worker/controller only in disposable offline hosts.

Reads a selected P2 build, owned source and synthetic receipts; writes fresh
ignored `.local-work/d5x` and `.local-work/d5ab` outputs. No game, saves, live process,
deployment, downloads or Git writes. Engineering waits are finite test bounds;
controller state has no elapsed-time failure policy. Preserves failures verbatim.
"""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'runtime/construction-winner'
sys.path.insert(0, str(SRC))
from controller import Controller
from worker_health import read_json, exclusive, disk_guard


def wait(predicate, seconds=180):
    end = time.monotonic() + seconds
    while time.monotonic() < end:
        result = predicate()
        if result:
            return result
        time.sleep(0.01)
    raise AssertionError('Finite offline test stimulus did not complete')


def main():
    build = Path(sys.argv[1]).resolve()
    label = sys.argv[2]
    inputs = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in [Path(__file__), SRC / 'controller.py', SRC / 'worker_health.py',
                        SRC / 'read_capture.py', SRC / 'reduce_v3.py']}
    assert label.replace('-', '').isalnum()
    out = ROOT / '.local-work/d5ab' / label
    out.mkdir(exist_ok=False)
    for name in inputs:
        snapshot = out / 'sources' / name
        snapshot.parent.mkdir(parents=True, exist_ok=True)
        snapshot.write_bytes((ROOT / name).read_bytes())
    sessions = ROOT / '.local-work/d5x' / label
    sessions.mkdir(exist_ok=False)
    package = build / 'package-runtime'
    results = []
    scenarios = sys.argv[3:] or ['normal', 'delay', 'disconnect', 'controller-death', 'identity', 'write', 'raw-flush',
                 'ack-flush', 'ack-write', 'disk', 'exit', 'guard', 'missing-terminal',
                 'loss', 'unowned-stop', 'damaged-ack', 'stale-ack', 'closed-raw-tail', 'closed-ack-tail', 'closed-duplicate-ack',
                 'loss-denial', 'negative-loss', 'string-loss', 'boolean-loss', 'loss-cause-mismatch', 'regressing-loss']
    for scenario in scenarios:
        disk_guard()
        session = sessions / scenario
        log = (out / (scenario + '.log')).open('xb')
        command = [str(package / 'sor-d5x-fixture.exe'), str(package / 'SorConstructionWinner.dll'),
                   str(session), 'controller-host']
        process = subprocess.Popen(command, stdout=log, stderr=subprocess.STDOUT)
        controller = None
        record = dict(case=scenario, command=command, pass_test=False)
        try:
            wait(lambda: (session / 'host-online.json').exists())
            expected = read_json(session / 'identity.json')
            assert expected['pid'] == process.pid
            assert expected['dll_sha256'] == hashlib.sha256((package / 'SorConstructionWinner.dll').read_bytes()).hexdigest()
            controller = Controller(session, expected)
            def fresh():
                controller.request()
                return wait(lambda: (state if (state := controller.poll()) != 'ALIVE_ACK_PENDING' else None))
            assert fresh() == 'HEALTHY'
            states = ['HEALTHY']
            def stimulate(action):
                pending = session / ('fixture-' + action + '.pending')
                with pending.open('xb') as stream:
                    stream.write(action.encode())
                    stream.flush()
                    import os
                    os.fsync(stream.fileno())
                pending.rename(session / 'fixture-command.txt')
                wait(lambda: (session / ('command-' + action + '.json')).exists())
            if scenario == 'controller-death':
                controller.close()
                child = subprocess.Popen([sys.executable, '-B', str(Path(__file__)), '--child', str(session)])
                wait(lambda: (session / 'child-controller-bound.json').exists())
                try:
                    duplicate = Controller(session, expected)
                except OSError:
                    states.append('ACTIVE_CHILD_OWNER_REJECTED')
                else:
                    duplicate.close()
                    raise AssertionError('Child lock ignored')
                (session / 'child-exit.txt').write_bytes(b'exit child controller only')
                assert child.wait(timeout=15) == 23
                controller = Controller(session, expected)
                assert fresh() == 'HEALTHY'
                states.append('CONTROLLER_CRASH_RESTART_HEALTHY')
            elif scenario == 'disconnect':
                try:
                    duplicate = Controller(session, expected)
                except OSError:
                    states.append('DUPLICATE_CONTROLLER_REJECTED')
                else:
                    duplicate.close()
                    raise AssertionError('Duplicate controller acquired lock')
                controller.close()
                time.sleep(0.1)
                controller = Controller(session, expected)
                assert fresh() == 'HEALTHY'
                states.append('RECONNECTED_HEALTHY')
            elif scenario == 'identity':
                for key, value in [('nonce', 'c' * 64), ('creation_filetime', expected['creation_filetime'] + 1), ('pid', expected['pid'] + 1)]:
                    try:
                        invalid = Controller(session, dict(expected, **{key: value}))
                    except AssertionError:
                        states.append('REJECTED_' + key)
                    else:
                        invalid.close()
                        raise AssertionError('Stale identity accepted')
            elif scenario == 'delay':
                stimulate('pause')
                time.sleep(0.15)
                controller.request()
                states.append(controller.poll())
                assert states[-1] == 'ALIVE_ACK_PENDING'
                time.sleep(1.1)
                states.append(controller.poll())
                assert states[-1] == 'ALIVE_ACK_PENDING'
                states.append(wait(lambda: (state if (state := controller.poll()) != 'ALIVE_ACK_PENDING' else None)))
                assert states[-1] == 'HEALTHY'
            elif scenario in ('damaged-ack', 'stale-ack', 'loss-denial', 'negative-loss', 'string-loss', 'boolean-loss', 'loss-cause-mismatch', 'regressing-loss'):
                if scenario in ('loss-denial', 'regressing-loss'):
                    stimulate('loss')
                    if scenario == 'regressing-loss':
                        assert fresh() == 'ALIVE_LOSS'
                        (out / 'original-last-ack.json').write_text(json.dumps(controller.last_ack), encoding='utf8')
                        # Model a prior larger authenticated counter without changing
                        # the actual worker or its open flush stream.
                        controller.last_ack = dict(controller.last_ack, drops=2, contention_exhausted=2)
                        states.append('MODELED_PRIOR_LOSS_MAXIMUM')
                controller.request()
                path = session / ('ack-' + controller.challenge + '.json')
                wait(path.exists)
                ack = read_json(path)
                (out / 'original-challenge.json').write_bytes(path.read_bytes())
                if scenario == 'stale-ack':
                    ack['request_nonce'] = '0' * 32
                elif scenario == 'damaged-ack':
                    ack['flushed'] += 1
                elif scenario == 'loss-denial':
                    ack.update(drops=0, queue_full=0, contention_exhausted=0, reentrant_losses=0)
                elif scenario == 'regressing-loss':
                    pass
                elif scenario == 'loss-cause-mismatch':
                    ack['queue_full'] += 1
                else:
                    ack['drops'] = {'negative-loss': -1, 'string-loss': '0', 'boolean-loss': False}[scenario]
                path.write_text(json.dumps(ack), encoding='utf8')
                try:
                    controller.poll()
                except AssertionError:
                    states.append('ACK_REJECTED')
                else:
                    raise AssertionError('Damaged ACK accepted')
            elif scenario == 'unowned-stop':
                (session / 'STOP').write_bytes(b'foreign STOP\n')
            elif scenario in ('write', 'raw-flush', 'ack-flush', 'ack-write', 'disk', 'exit', 'guard', 'missing-terminal', 'loss'):
                stimulate(scenario)
                if scenario == 'loss':
                    assert fresh() == 'ALIVE_LOSS'
                    states.append('ALIVE_LOSS')
            if scenario not in ('write', 'raw-flush', 'ack-flush', 'ack-write', 'disk', 'exit', 'guard', 'unowned-stop'):
                controller.request_stop()
            final = wait(lambda: (state if (state := controller.poll()).startswith(('EXIT_', 'STOPPED_')) else None))
            wanted = ('EXIT_FAULT' if scenario in ('write', 'raw-flush', 'ack-flush', 'ack-write', 'disk', 'guard')
                      else 'EXIT_INCOMPLETE' if scenario in ('exit', 'missing-terminal')
                      else 'EXIT_UNOWNED_STOP' if scenario == 'unowned-stop'
                      else 'STOPPED_LOSS' if scenario in ('loss', 'loss-denial', 'regressing-loss') else 'STOPPED_COMPLETE')
            assert final == wanted, (scenario, final, wanted)
            assert process.wait(timeout=20) == 0
            states.append(final)
            from read_capture import inspect
            reduction = inspect(session, expected['dll_sha256'])
            record['readback'] = {key: reduction[key] for key in ('complete_session', 'durable_records', 'parsed_records', 'raw_bytes', 'damage')}
            if scenario.startswith('closed-'):
                original = out / 'closed-original'
                original.mkdir()
                for name in ('identity.json', 'ready.json', 'terminal.json', 'events.bin', 'flush.jsonl'):
                    (original / name).write_bytes((session / name).read_bytes())
                record['pre_damage'] = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in original.iterdir()}
                if scenario == 'closed-raw-tail':
                    with (session / 'events.bin').open('ab') as stream:
                        stream.write(b'x')
                elif scenario == 'closed-ack-tail':
                    with (session / 'flush.jsonl').open('ab') as stream:
                        stream.write(b'{')
                else:
                    first = (session / 'flush.jsonl').read_bytes().splitlines(keepends=True)[0]
                    with (session / 'flush.jsonl').open('ab') as stream:
                        stream.write(first)
                assert controller.poll() == 'EXIT_INCOMPLETE'
                states.append('CLOSED_DAMAGE_REJECTED')
            record.update(pass_test=True, states=states)
        except BaseException as error:
            record['error'] = repr(error)
            raise
        finally:
            if controller:
                controller.close()
            # Recovery is restricted to this self-created host's STOP protocol.
            if process.poll() is None and session.exists() and not (session / 'STOP').exists():
                (session / 'STOP').write_bytes(b'offline test cleanup STOP\n')
            try:
                record['exit'] = process.wait(timeout=25)
            except subprocess.TimeoutExpired:
                record['cleanup'] = 'Host still running; no termination performed'
            log.close()
            record['files'] = {str(p.relative_to(session)): hashlib.sha256(p.read_bytes()).hexdigest()
                               for p in session.rglob('*') if p.is_file()}
            results.append(record)
            unchanged = all(hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest
                            for name, digest in inputs.items())
            (out / 'receipt.json').write_text(json.dumps(dict(results=results, build=str(build),
                inputs=inputs, source_unchanged=unchanged,
                passed=unchanged and all(r['pass_test'] for r in results)), indent=2) + '\n', encoding='utf8', newline='\n')
            assert unchanged, 'Controller/consumer/test source changed during execution'
    print(json.dumps(dict(cases=len(results), passed=all(r['pass_test'] for r in results))))


if __name__ == '__main__':
    if sys.argv[1] == '--parallel':
        from concurrent.futures import ThreadPoolExecutor
        build, label = sys.argv[2:4]
        out = ROOT / '.local-work/d5ab' / label
        out.mkdir(exist_ok=False)
        cases = 'normal delay disconnect controller-death identity write raw-flush ack-flush ack-write disk exit guard missing-terminal loss unowned-stop damaged-ack stale-ack closed-raw-tail closed-ack-tail closed-duplicate-ack loss-denial negative-loss string-loss boolean-loss loss-cause-mismatch regressing-loss'.split()
        def run(case):
            result = subprocess.run([sys.executable, '-B', str(Path(__file__)), build, label + '-' + case, case], capture_output=True)
            (out / (case + '.stdout')).write_bytes(result.stdout)
            (out / (case + '.stderr')).write_bytes(result.stderr)
            receipt = ROOT / '.local-work/d5ab' / (label + '-' + case) / 'receipt.json'
            return dict(case=case, exit=result.returncode, receipt=str(receipt),
                        receipt_sha256=hashlib.sha256(receipt.read_bytes()).hexdigest() if receipt.exists() else None)
        with ThreadPoolExecutor(max_workers=4) as pool:
            results = list(pool.map(run, cases))
        (out / 'receipt.json').write_text(json.dumps(dict(results=results, passed=all(r['exit'] == 0 for r in results)), indent=2) + '\n', encoding='utf8', newline='\n')
        print(json.dumps(results))
        assert all(r['exit'] == 0 for r in results)
    elif sys.argv[1] == '--child':
        import os
        session = Path(sys.argv[2])
        lease = Controller(session, read_json(session / 'identity.json'))
        exclusive(session / 'child-controller-bound.json', dict(pid=os.getpid()))
        wait(lambda: (session / 'child-exit.txt').exists())
        os._exit(23)
    else:
        main()
