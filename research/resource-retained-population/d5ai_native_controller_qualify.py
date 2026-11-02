# SPDX-License-Identifier: GPL-3.0-or-later
"""Execute actual owned worker arming, query, reconnect and STOP controls.

Launches only the selected disposable qualification host and exact candidate DLL.
The fixture-only Episode subclass preserves worker/process/lock/STOP mechanisms;
its target validator positively restricts the owned host instead of retail.
Writes fresh ignored captures/receipts only. No game, saves, deployment, network,
process memory access or process termination. Failure requests owned STOP.
"""
from pathlib import Path
import json
import subprocess
import sys
import time

from d5ai_episode import EpisodeController, ROOT, CONTROL_PATHS, sha, read_json, arm, poll_geometry
from d5ai_read_lifetime import validate_identity, read_prefix
from d5ai_read_geometry import read_session
from worker_health import disk_guard
from d5ai_operations import worker_json


class OwnedEpisodeController(EpisodeController):
    def validate_target(self, admission, approval):
        assert self.expected['retail'] is False
        assert self.session.is_relative_to(ROOT / '.local-work/d5ai-recorder')
        assert Path(self.plan['process_image']).name == 'sor-d5x-fixture.exe'
        assert sha(self.plan['process_image']) == self.expected['host_sha256']
        assert sha(self.plan['dll']) == self.expected['dll_sha256']
        assert self.expected['geometry_schema'] == 'sor-d5ai-raw/2'
        assert len(self.expected['geometry_sites']) == 3 and len(self.expected['context_sites']) == 2
        validate_identity(self.expected)

    def validate_phase(self, admission):
        pass


def main():
    build, out = (Path(p).resolve() for p in sys.argv[1:3])
    if not out.is_relative_to(ROOT / '.local-work/d5ai-recorder'):
        raise ValueError('Fresh task-local output required')
    disk_guard()
    out.mkdir(exist_ok=False)
    session = out / 'session'
    image = build / 'package-runtime/sor-d5x-fixture.exe'
    dll = build / 'package-runtime/SorConstructionWinner.dll'
    inputs = {str(p): sha(p) for p in ({image,dll,Path(__file__),Path(__file__).with_name('d5ai_operations.py')} | CONTROL_PATHS)}
    logs = [(out / name).open('wb') for name in ('host.stdout', 'host.stderr')]
    process = subprocess.Popen([str(image), str(dll), str(session), 'd5ai-controller-host'], stdout=logs[0], stderr=logs[1])
    controller, states = None, []
    result = dict(schema='sor-d5ai-actual-controller/1', inputs=inputs, scope='Owned Episode subclass target validator; actual process/worker/arm/query/reconnect/STOP, no retail authority')

    def wait_file(name):
        while not (session / name).exists():
            if process.poll() is not None:
                raise RuntimeError('Owned host ended before ' + name)
            time.sleep(.01)

    try:
        wait_file('ready.json')
        wait_file('fixture-controller-ready.json')
        identity = read_json(session / 'identity.json')
        plan = dict(process_image=str(image), dll=str(dll))
        controller = OwnedEpisodeController(session, identity, plan, {}, {}, 'start')
        for request in (1, 2):
            while True:
                value = arm(controller, 'owned-checkpoint-' + str(request))
                states.append(value['state'])
                if value['state'] == 'GEOMETRY_ARMED':
                    break
                if process.poll() is not None:
                    raise RuntimeError('Host exited during arm handshake')
                time.sleep(.02)
            ack = value['geometry_request']['arm_ack']
            assert ack['geometry_armed'] == request and ack['lifetime_failed'] is False
            assert ack['lifetime_unlogged_cutoff_ticks'] == 0
            (session / ('fixture-query-' + str(request))).write_bytes(b'one owned query\n')
            wait_file('geometry-request-' + str(request) + '.json')
            assert poll_geometry(controller)['state'] == 'GEOMETRY_CAPTURE_RECEIPT'
            if request == 1:
                owner = controller.state['owner']
                controller.close()
                controller = OwnedEpisodeController(session, identity, plan, {}, {}, 'request')
                assert controller.state['owner'] == owner and controller.state['geometry_last_request'] == 1
        stop = controller.request_stop('finite owned two-query controller qualification')
        result['stop'] = stop
        controller.close()
        controller = None
        (session / 'fixture-controller-done').write_bytes(b'done\n')
        process.wait()
        assert process.returncode == 0
        terminal = worker_json(session / 'terminal.json')
        raw = read_session(session)
        lifetime = read_prefix(session, terminal)
        assert not raw['errors'] and len(raw['snapshots']) == 2 and lifetime['complete']
        assert terminal['geometry_completed'] == 2 and terminal['lifetime_drops'] == 0
        result.update(status='PASS', exit=process.returncode, snapshots=2, states=states,
                      reconnect_owner_preserved=True, lifetime_prefix_sha256=lifetime['raw_prefix_sha256'])
    except BaseException as error:
        result.update(status='FAIL', error=repr(error), states=states)
        raise
    finally:
        if controller is not None:
            try:
                controller.request_stop('owned test failure closeout')
            finally:
                controller.close()
        if session.exists() and process.poll() is None:
            if not (session / 'STOP').exists():
                (session / 'STOP').write_bytes(b'owned failed fixture STOP\n')
            (session / 'fixture-controller-done').touch(exist_ok=True)
            process.wait()
        for log in logs:
            log.close()
        result['inputs_unchanged'] = all(sha(p) == digest for p, digest in inputs.items())
        (out / 'qualification.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf8', newline='\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
