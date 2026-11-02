# SPDX-License-Identifier: GPL-3.0-or-later
"""Exercise reconnect STOP after actual owned READY metadata fails strict parsing.

Launches only the exact disposable host/DLL16; reads query-only worker/process
identity. Writes fresh ignored captures and corrupt/restored fixture metadata.
Rejects malformed persisted ownership rather than inventing an owner. No game,
save, deployment, network, process memory access or process termination. Failure
requests fixture STOP and preserves all files. No retail authority is asserted.
"""
from pathlib import Path
import json
import subprocess
import sys
import time

from d5ai_episode import ROOT, CONTROL_PATHS, strict_session_json, sha
from d5ai_native_controller_qualify import OwnedEpisodeController
from worker_health import disk_guard


def main():
    build, out = (Path(p).resolve() for p in sys.argv[1:3])
    if not out.is_relative_to(ROOT / '.local-work/d5ai-recorder'):
        raise ValueError('Fresh task-local output required')
    disk_guard()
    out.mkdir(exist_ok=False)
    session = out / 'session'
    image, dll = (build / 'package-runtime' / leaf for leaf in ('sor-d5x-fixture.exe', 'SorConstructionWinner.dll'))
    inputs = {str(p): sha(p) for p in ({image, dll, Path(__file__),
              Path(__file__).with_name('d5ai_native_controller_qualify.py'),
              Path(__file__).with_name('d5ai_operations.py')} | CONTROL_PATHS)}
    logs = [(out / leaf).open('wb') for leaf in ('host.stdout', 'host.stderr')]
    process = subprocess.Popen([str(image), str(dll), str(session), 'd5ai-controller-host'], stdout=logs[0], stderr=logs[1])
    result, controller = dict(schema='sor-d5ai-actual-strict-stop/1', inputs=inputs), None

    def wait_file(leaf):
        while not (session / leaf).exists():
            if process.poll() is not None:
                raise RuntimeError('Host ended before ' + leaf)
            time.sleep(.01)

    try:
        wait_file('ready.json')
        wait_file('fixture-controller-ready.json')
        identity = strict_session_json(session / 'identity.json')
        plan = dict(process_image=str(image), dll=str(dll))
        controller = OwnedEpisodeController(session, identity, plan, {}, {}, 'start')
        owner = controller.state['owner']
        controller.close()
        controller = None
        state_path = session / 'p4-state.json'
        state = state_path.read_bytes()
        changed = state.rstrip()[:-1] + b',"owner":' + json.dumps(owner).encode() + b'}\n'
        (out / 'state.original').write_bytes(state)
        (out / 'state.duplicate').write_bytes(changed)
        state_path.write_bytes(changed)
        try:
            OwnedEpisodeController(session, identity, plan, {}, {}, 'stop')
        except ValueError as error:
            assert str(error) == 'Duplicate session JSON key: owner'
        else:
            raise AssertionError('STOP invented ownership from malformed state')
        state_path.write_bytes(state)
        ready_path = session / 'ready.json'
        ready = ready_path.read_bytes()
        changed = ready.rstrip()[:-1] + b',"ready":true}\n'
        (out / 'ready.original').write_bytes(ready)
        (out / 'ready.duplicate').write_bytes(changed)
        ready_path.write_bytes(changed)
        try:
            OwnedEpisodeController(session, identity, plan, {}, {}, 'poll')
        except ValueError as error:
            assert str(error) == 'Duplicate session JSON key: ready'
        else:
            raise AssertionError('Malformed READY became live health')
        controller = OwnedEpisodeController(session, identity, plan, {}, {}, 'stop')
        assert controller.state['owner'] == owner and controller.lease is None
        stopped = controller.request_stop('known owned STOP despite malformed READY; no health claim')
        assert stopped['state'] == 'STOP_REQUESTED'
        assert ready_path.read_bytes() == changed
        (session / 'fixture-controller-done').write_bytes(b'finite STOP qualification complete\n')
        process.wait()
        assert process.returncode == 0
        assert controller.terminal()['state'] == 'RETIRED_PENDING_POSTFLIGHT'
        ready_path.write_bytes(ready)
        result.update(status='PASS', exit=0, malformed_ownership_refused=True, malformed_READY_health_refused=True,
                      existing_owner_preserved=True, actual_owned_STOP_with_malformed_READY=True,
                      scope='Actual owned process and STOP; fixture-only target validator, no retail authority')
    except BaseException as error:
        result.update(status='FAIL', error=repr(error))
        raise
    finally:
        if controller is not None:
            try:
                controller.request_stop('owned strict-STOP test closeout')
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
