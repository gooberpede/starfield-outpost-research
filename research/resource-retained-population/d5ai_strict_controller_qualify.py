# SPDX-License-Identifier: GPL-3.0-or-later
"""Reject duplicate JSON on actual owned READY, ACK, state and terminal paths.

Runs only the exact disposable DLL16/host. Saves original and corrupted metadata
bytes in fresh ignored outputs, restores each original after its negative test,
and preserves actual owned STOP. No retail authority, game, save, deployment,
network, process memory access or process termination. STOP on identity, source,
worker or disk guard failure; request owned STOP in cleanup and retain all files.
This fixture-only target validator does not qualify retail occurrence or approval.
"""
from pathlib import Path
import json
import subprocess
import sys
import time

from d5ai_episode import ROOT, CONTROL_PATHS, strict_session_json, SessionController, sha
from d5ai_native_controller_qualify import OwnedEpisodeController
from worker_health import disk_guard
import p4_controller as historical_p4


def main():
    build, out = (Path(p).resolve() for p in sys.argv[1:3])
    if not out.is_relative_to(ROOT / '.local-work/d5ai-recorder'):
        raise ValueError('Fresh task-local output required')
    disk_guard()
    out.mkdir(exist_ok=False)
    session = out / 'session'
    image = build / 'package-runtime/sor-d5x-fixture.exe'
    dll = build / 'package-runtime/SorConstructionWinner.dll'
    inputs = {str(p): sha(p) for p in ({image, dll, Path(__file__),
              Path(__file__).with_name('d5ai_native_controller_qualify.py'),
              Path(__file__).with_name('d5ai_operations.py')} | CONTROL_PATHS)}
    logs = [(out / leaf).open('wb') for leaf in ('host.stdout', 'host.stderr')]
    process = subprocess.Popen([str(image), str(dll), str(session), 'd5ai-controller-host'], stdout=logs[0], stderr=logs[1])
    checks, controller = [], None
    result = dict(schema='sor-d5ai-actual-strict-controller/1', inputs=inputs,
                  scope='Actual owned worker files and private inherited methods; fixture-only target validation, no retail authority')

    def wait_file(leaf):
        while not (session / leaf).exists():
            if process.poll() is not None:
                raise RuntimeError('Host ended before ' + leaf)
            time.sleep(.01)

    def corrupt(path, key):
        raw = path.read_bytes()
        parsed = json.loads(raw)
        changed = raw.rstrip()[:-1] + b',' + json.dumps(key).encode() + b':' + json.dumps(parsed[key]).encode() + b'}\n'
        (out / (path.name + '.original')).write_bytes(raw)
        (out / (path.name + '.duplicate')).write_bytes(changed)
        path.write_bytes(changed)
        return raw

    def refuses(name, action):
        try:
            action()
        except ValueError as error:
            if 'Duplicate session JSON key:' not in str(error):
                raise
            checks.append(dict(name=name, passed=True, error=str(error)))
        else:
            raise AssertionError('Duplicate metadata was accepted: ' + name)

    try:
        wait_file('ready.json')
        wait_file('fixture-controller-ready.json')
        identity = strict_session_json(session / 'identity.json')
        plan = dict(process_image=str(image), dll=str(dll))
        controller = OwnedEpisodeController(session, identity, plan, {}, {}, 'start')
        owner = controller.state['owner']
        for method in ('__init__', 'poll', 'terminal'):
            assert getattr(SessionController, method).__globals__['read_json'] is strict_session_json
        assert historical_p4.SessionController.poll.__globals__['read_json'] is historical_p4.read_json
        assert historical_p4.read_json is not strict_session_json
        checks.append(dict(name='private single-parse methods; historical globals untouched', passed=True))
        controller.close()
        controller = None
        path = session / 'ready.json'
        original = corrupt(path, 'ready')
        refuses('actual constructor READY duplicate', lambda: OwnedEpisodeController(session, identity, plan, {}, {}, 'request'))
        path.write_bytes(original)
        controller = OwnedEpisodeController(session, identity, plan, {}, {}, 'request')
        assert controller.state['owner'] == owner
        controller.close()
        controller = None
        path = session / 'p4-state.json'
        original = corrupt(path, 'owner')
        refuses('actual constructor persisted-state duplicate', lambda: OwnedEpisodeController(session, identity, plan, {}, {}, 'request'))
        path.write_bytes(original)
        controller = OwnedEpisodeController(session, identity, plan, {}, {}, 'request')
        assert controller.state['owner'] == owner
        challenge = controller.request()['nonce']
        path = session / ('ack-' + challenge + '.json')
        wait_file(path.name)
        original = corrupt(path, 'geometry_failed')
        refuses('actual fresh ACK duplicate', controller.poll)
        assert controller.state['challenge'] == challenge
        # The already admitted owner does not reread READY/ACK/state to stop.
        stop = controller.request_stop('strict JSON negative control; preserve owned STOP after ACK refusal')
        assert stop['state'] == 'STOP_REQUESTED'
        checks.append(dict(name='owned STOP available immediately after ACK refusal', passed=True))
        path.write_bytes(original)
        (session / 'fixture-controller-done').write_bytes(b'finite metadata controls complete\n')
        process.wait()
        assert process.returncode == 0
        wait_file('terminal.json')
        path = session / 'terminal.json'
        original = corrupt(path, 'lifetime_failed')
        refuses('actual terminal duplicate', controller.terminal)
        assert controller.request_stop('repeat already-owned STOP')['state'] == 'STOP_REQUESTED'
        checks.append(dict(name='owned STOP available despite malformed terminal', passed=True))
        path.write_bytes(original)
        assert controller.terminal()['state'] == 'RETIRED_PENDING_POSTFLIGHT'
        checks.append(dict(name='restored actual terminal authenticates owned finalization', passed=True))
        result.update(status='PASS', exit=0, checks=checks)
    except BaseException as error:
        result.update(status='FAIL', error=repr(error), checks=checks)
        raise
    finally:
        if controller is not None:
            try:
                controller.request_stop('owned strict-controller test closeout')
            finally:
                controller.close()
        if session.exists() and process.poll() is None:
            if not (session / 'STOP').exists():
                (session / 'STOP').write_bytes(b'owned disposable failure STOP\n')
            (session / 'fixture-controller-done').touch(exist_ok=True)
            process.wait()
        for log in logs:
            log.close()
        result['inputs_unchanged'] = all(sha(p) == digest for p, digest in inputs.items())
        (out / 'qualification.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf8', newline='\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'inputs'}))


if __name__ == '__main__':
    main()
