# SPDX-License-Identifier: GPL-3.0-or-later
"""Prepare identity-bound B2 control; execution needs a later explicit GO.

Reads pinned admission/approval/plan, READY, ACK, worker and process query handles.
Writes only session-local state, exclusive checkpoint receipts, request and STOP.
No launch, injection, memory read, deployment, unload, process kill or save access.
Live health checks metadata only; full raw authentication belongs to postflight.
Owned P2 controller/worker methods are adapted under SOR-P-0002.
"""

import sys

# Safety checks below require assertions, including when imported as a helper.
if not __debug__ or sys.flags.optimize != 0:
    raise RuntimeError('Python optimization is forbidden; invoke with -E -B and no -O/-OO')
import argparse
import ctypes as C
from ctypes import wintypes as W
import hashlib
import json
import msvcrt
import os
from pathlib import Path
import secrets

from worker_health import K, WorkerLease, disk_guard, read_json
from controller import loss_counts

ROOT = Path(__file__).resolve().parents[2]
LIVE = ROOT / '.local-work/d5x/live'
K.OpenProcess.argtypes = [W.DWORD, W.BOOL, W.DWORD]
K.OpenProcess.restype = W.HANDLE
K.GetProcessTimes.argtypes = K.GetThreadTimes.argtypes
K.QueryFullProcessImageNameW.argtypes = [W.HANDLE, W.DWORD, W.LPWSTR, C.POINTER(W.DWORD)]


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def clean_path(path):
    path = Path(path).absolute()
    for ancestor in (path, *path.parents):
        if ancestor.exists():
            assert not ancestor.is_symlink() and not ancestor.is_junction(), str(ancestor)
    assert path.resolve() == path
    return path


def write_new(path, value):
    """Persist an exclusive receipt without making emergency STOP depend on disk queries."""
    with Path(path).open('x', encoding='utf8', newline='\n') as stream:
        json.dump(value, stream, indent=2)
        stream.write('\n')
        stream.flush()
        os.fsync(stream.fileno())


def pinned_json(path, digest):
    data = Path(path).read_bytes()
    assert hashlib.sha256(data).hexdigest() == digest
    return json.loads(data)


def telemetry_counts(ack, prior=None):
    """Validate sampled loss metadata separately from raw byte authentication."""
    counts = loss_counts(ack)
    keys = ('loss_generation', 'first_loss_sampled_admission', 'last_loss_sampled_admission')
    assert all(type(ack[k]) is int and 0 <= ack[k] < 2 ** 64 for k in keys)
    assert type(ack['loss_bounds_uncertain']) is bool
    first, last = (ack[k] for k in keys[1:])
    assert ack['loss_generation'] == counts[0]
    if counts[0]:
        assert ack['loss_bounds_uncertain'] or 0 < first <= last
    else:
        assert first == last == 0 and not ack['loss_bounds_uncertain']
    if prior is not None:
        assert all(a >= b for a, b in zip(counts, loss_counts(prior)))
        assert ack['flushed'] >= prior['flushed']
        assert ack['loss_generation'] >= prior['loss_generation']
        assert not prior['loss_bounds_uncertain'] or ack['loss_bounds_uncertain']
        if prior['first_loss_sampled_admission']:
            assert 0 < first <= prior['first_loss_sampled_admission']
        assert last >= prior['last_loss_sampled_admission']
    return counts


def process_identity(identity, image, allow_exited=False):
    handle = K.OpenProcess(0x1000 | 0x100000, False, identity['pid'])
    if not handle:
        if allow_exited and C.get_last_error() == 87:
            return 'PROCESS_UNAVAILABLE_PENDING_POSTFLIGHT'
        raise OSError(C.get_last_error(), 'Cannot bind process query/synchronization handle')
    try:
        values = [W.FILETIME() for _ in range(4)]
        if not K.GetProcessTimes(handle, *(C.byref(v) for v in values)):
            raise AssertionError('GetProcessTimes failed')
        birth = values[0].dwLowDateTime | values[0].dwHighDateTime << 32
        assert birth == identity['creation_filetime']
        running = K.WaitForSingleObject(handle, 0) == 258
        assert running or allow_exited, 'Process already exited'
        if not running:
            return 'PROCESS_EXITED'
        buffer = C.create_unicode_buffer(32768)
        size = W.DWORD(len(buffer))
        if not K.QueryFullProcessImageNameW(handle, 0, buffer, C.byref(size)):
            raise AssertionError('Process image query failed')
        assert Path(buffer.value).resolve() == Path(image).resolve(), 'Wrong process image path'
        return 'PROCESS_ALIVE' if running else 'PROCESS_EXITED'
    finally:
        K.CloseHandle(handle)


class SessionController:
    """One writer at a time; persisted state survives operator disconnects.

    RetailController adds exact retail admission. Disposable qualification uses
    a test subclass with a fixture-only validator; the CLI exposes retail only.
    """
    def __init__(self, session, expected, plan, admission, approval, action):
        self.session = clean_path(session)
        self.expected, self.plan = dict(expected), dict(plan)
        self.lock = self.lease = None
        self.identity_hash = sha(self.session / 'identity.json')
        assert read_json(self.session / 'identity.json') == expected
        self.validate_target(admission, approval)
        if action != 'stop':
            self.validate_phase(admission)
        if action == 'start':
            assert self.session.name not in admission.get('existing_sessions', [])
            assert str(self.session) not in admission.get('existing_sessions', [])
        self.process_state = process_identity(expected, plan['process_image'], action in ('poll', 'stop'))
        try:
            self.lock = (self.session / 'p4-controller.lock').open('a+b')
            self.lock.seek(0)
            msvcrt.locking(self.lock.fileno(), msvcrt.LK_NBLCK, 1)
            ready = read_json(self.session / 'ready.json')
            assert all(ready.get(k) == v for k, v in expected.items())
            if action not in ('poll', 'stop') or not (self.session / 'terminal.json').exists():
                try:
                    self.lease = WorkerLease(ready, expected)
                except (OSError, AssertionError):
                    if action not in ('poll', 'stop'):
                        raise
                    # No unavailable or exited lease is treated as a live ACK.
                    self.lease = None
            self.state_path = self.session / 'p4-state.json'
            if action == 'start':
                disk_guard()
                assert not self.state_path.exists() and not (self.session / 'STOP').exists()
                self.state = dict(identity_sha256=self.identity_hash, owner=secrets.token_hex(16),
                                  challenge=None, stop=None, last_ack=None, telemetry_fault=False)
                write_new(self.state_path, self.state)
            else:
                self.state = read_json(self.state_path)
                assert self.state['identity_sha256'] == self.identity_hash
                assert len(self.state['owner']) == 32
        except BaseException:
            self.close()
            raise

    def validate_target(self, admission, approval):
        raise NotImplementedError

    def validate_phase(self, admission):
        pass

    def save(self):
        pending = self.session / ('p4-state-' + secrets.token_hex(16) + '.pending')
        write_new(pending, self.state)
        os.replace(pending, self.state_path)

    def request(self):
        disk_guard()
        assert self.lease.alive() and self.state['stop'] is None
        # Repeating an unfinished request preserves its identity across reconnect.
        if self.state['challenge'] is None:
            self.state['challenge'] = secrets.token_hex(16)
            self.save()
        nonce = self.state['challenge']
        request = self.session / 'request.txt'
        if request.exists() and request.read_bytes() == nonce.encode('ascii'):
            return dict(state='REQUESTED', nonce=nonce)
        pending = self.session / ('p4-request-' + secrets.token_hex(16) + '.pending')
        with pending.open('xb') as stream:
            stream.write(nonce.encode('ascii'))
            stream.flush()
            os.fsync(stream.fileno())
        try:
            os.replace(pending, request)
        except PermissionError:
            # Retain this exact nonce and the complete pending bytes. A sharing
            # race is retryable publication, never permission to choose a new one.
            return dict(state='REQUEST_PUBLICATION_PENDING', nonce=nonce, pending=str(pending))
        return dict(state='REQUESTED', nonce=nonce)

    def poll(self):
        disk_guard()
        if self.lease is None or not self.lease.alive():
            return self.terminal()
        if self.state['stop'] is not None:
            return dict(state='STOP_PENDING', raw_verified=False)
        nonce = self.state['challenge']
        if nonce is None:
            return dict(state='ALIVE_UNCHALLENGED', raw_verified=False)
        path = self.session / ('ack-' + nonce + '.json')
        if not path.exists():
            return dict(state='ALIVE_ACK_PENDING', raw_verified=False)
        ack = read_json(path)
        self.lease.verify_ack(ack, nonce)
        assert all(ack.get(k) == v for k, v in self.expected.items())
        assert ack['hooks_intact'] is True and ack['capture_active'] is True
        assert ack['counter_overflow'] is False and ack['output_fault'] == 'none'
        assert type(ack['output_faults']) is int and ack['output_faults'] == 0
        assert type(ack['flushed']) is int and ack['flushed'] >= 0
        assert type(ack['acknowledged']) is int and ack['acknowledged'] == ack['flushed']
        assert type(ack['loss_bounds_uncertain']) is bool
        telemetry_ok = True
        try:
            counts = telemetry_counts(ack, self.state['last_ack'])
        except (AssertionError, KeyError, TypeError):
            telemetry_ok = False
            self.state['telemetry_fault'] = True
        self.state['last_ack'] = ack
        self.state['challenge'] = None
        self.save()
        state = ('TELEMETRY_INCONSISTENT' if not telemetry_ok or self.state['telemetry_fault']
                 else 'ALIVE_LOSS' if counts[0] or ack['loss_bounds_uncertain'] else 'HEALTHY_ACK')
        return dict(state=state, ack=ack, raw_verified=False,
                    scientific_firstness_qualified=False)

    def request_stop(self, reason):
        # No disk, DLL, guard or READY recheck here. An admitted owner can stop
        # after those checks fail. The worker leaves resident forwarding wrappers.
        if self.state['stop'] is None:
            self.state['stop'] = dict(identity_sha256=self.identity_hash,
                                      owner=self.state['owner'], stop_nonce=secrets.token_hex(16), reason=reason)
            self.save()
        payload = (json.dumps(self.state['stop'], sort_keys=True) + '\n').encode()
        path = self.session / 'STOP'
        if path.exists():
            assert path.read_bytes() == payload, 'Foreign STOP is never owned finalization'
        else:
            with path.open('xb') as stream:
                stream.write(payload)
                stream.flush()
                os.fsync(stream.fileno())
        return dict(state='STOP_REQUESTED', stop=self.state['stop'])

    def terminal(self):
        path = self.session / 'terminal.json'
        if not path.exists():
            return dict(state='EXIT_INCOMPLETE', raw_verified=False)
        value = read_json(path)
        assert all(value.get(k) == v for k, v in self.expected.items())
        if value['failed'] or value['output_faults'] or value['output_fault'] != 'none':
            state = 'EXIT_FAULT'
        elif self.state['stop'] is None:
            state = 'EXIT_UNOWNED_STOP'
        else:
            payload = (json.dumps(self.state['stop'], sort_keys=True) + '\n').encode()
            if (self.session / 'STOP').read_bytes() != payload:
                state = 'EXIT_UNOWNED_STOP'
            else:
                assert value['resident_inert'] is True
                state = 'RETIRED_PENDING_POSTFLIGHT'
        return dict(state=state, terminal=value, raw_verified=False,
                    scientific_firstness_qualified=False)

    def close(self):
        if self.lease:
            self.lease.close()
            self.lease = None
        if self.lock:
            self.lock.close()
            self.lock = None


class RetailController(SessionController):
    def validate_phase(self, admission):
        import importlib.util
        path = ROOT / 'research/resource-retained-population/d5ab_p4_operations.py'
        assert sha(path) == self.plan['operations_sha256']
        spec = importlib.util.spec_from_file_location('p4_operations', path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        module.lightweight(self.plan, admission)

    def validate_target(self, admission, approval):
        assert self.session.parent == LIVE and self.session.name == 'session-' + self.expected['nonce']
        assert self.expected['schema'] == 'sor-d5x/4' and self.expected['retail'] is True
        assert self.expected['host_sha256'] == self.plan['game_sha256']
        assert self.expected['sfse_sha256'] == self.plan['sfse_sha256']
        assert self.expected['dll_sha256'] == self.plan['dll_sha256']
        assert Path(self.plan['process_image']).name == 'Starfield.exe'
        assert len(self.expected['sites']) == len(self.plan['sites']) == 18
        for observed, pinned in zip(self.expected['sites'], self.plan['sites']):
            assert observed['index'] == pinned['index'] and observed['rva'] == pinned['rva']
            assert observed['guard_sha256'] == pinned['guard_sha256']
            assert observed['va'] == self.expected['module_base'] + pinned['rva']
        assert admission['state'] == 'PASS_OFFLINE_PREFLIGHT'
        assert admission['plan_sha256'] == self.plan['plan_sha256']
        assert approval['authority'] == 'B2_EXPLICIT_MAINTAINER_GO'
        assert approval['plan_sha256'] == self.plan['plan_sha256']
        assert approval['preflight_sha256'] == admission['receipt_sha256']
        assert approval['session'] == str(self.session)
        assert approval['identity_sha256'] == self.identity_hash
        assert approval['one_process_one_load_one_direct_travel'] is True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['start', 'request', 'poll', 'stop'])
    parser.add_argument('--session', required=True, type=Path)
    for name in ('plan', 'preflight', 'approval'):
        parser.add_argument('--' + name, required=True, type=Path)
        parser.add_argument('--' + name + '-sha256', required=True)
    parser.add_argument('--out', required=True, type=Path)
    parser.add_argument('--reason', default='maintainer-directed STOP')
    args = parser.parse_args()
    try:
        execute(args)
    except BaseException as error:
        try:
            write_new(args.out, dict(state='CHECK_ERROR', action=args.action,
                                     error=repr(error), raw_verified=False,
                                     scientific_firstness_qualified=False))
        except OSError:
            pass
        raise


def execute(args):
    plan = pinned_json(args.plan, args.plan_sha256)
    plan['plan_sha256'] = args.plan_sha256
    preflight = pinned_json(args.preflight, args.preflight_sha256)
    preflight['receipt_sha256'] = args.preflight_sha256
    approval = pinned_json(args.approval, args.approval_sha256)
    required = {'p4_controller.py', 'controller.py', 'worker_health.py',
                'read_capture.py', 'reduce_v3.py', 'reduce_v4.py'}
    assert {Path(path).name for path in plan['controller_pins']} == required
    for path, digest in plan['controller_pins'].items():
        assert Path(path).resolve() == Path(__file__).resolve().parent / Path(path).name
        assert sha(path) == digest
    if args.action != 'stop':
        disk_guard()
    expected = read_json(args.session / 'identity.json')
    controller = RetailController(args.session, expected, plan, preflight, approval, args.action)
    try:
        result = (dict(state='BOUND_READY', raw_verified=False) if args.action == 'start'
                  else controller.request() if args.action == 'request'
                  else controller.poll() if args.action == 'poll'
                  else controller.request_stop(args.reason))
        result.update(identity_sha256=controller.identity_hash, owner=controller.state['owner'],
                      plan_sha256=args.plan_sha256, approval_sha256=args.approval_sha256)
        write_new(args.out, result)
        print(json.dumps(result))
    finally:
        controller.close()


if __name__ == '__main__':
    main()
