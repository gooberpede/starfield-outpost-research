# SPDX-License-Identifier: GPL-3.0-or-later
"""Identity-bound read-only thread liveness, with disposable qualification mode.

--qualify creates only its own Python thread and fresh ignored receipts. --watch
is a FUTURE LIVE OPERATION, NOT AUTHORIZED by D5AB: it reads an approved session,
opens a query/synchronization handle, and writes a private health receipt. It does
not attach a debugger, pause/inject/modify/terminate a process, send STOP, read game
memory, scan saves, install anything or use the network. The retained handle
prevents TID reuse from silently selecting another worker.
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
import os
from pathlib import Path
import threading
import time

K = C.WinDLL('kernel32', use_last_error=True)
K.OpenThread.argtypes = [W.DWORD, W.BOOL, W.DWORD]
K.OpenThread.restype = W.HANDLE
K.CloseHandle.argtypes = [W.HANDLE]
K.GetProcessIdOfThread.argtypes = [W.HANDLE]
K.GetProcessIdOfThread.restype = W.DWORD
K.GetThreadTimes.argtypes = [W.HANDLE, C.POINTER(W.FILETIME), C.POINTER(W.FILETIME), C.POINTER(W.FILETIME), C.POINTER(W.FILETIME)]
K.WaitForSingleObject.argtypes = [W.HANDLE, W.DWORD]
K.WaitForSingleObject.restype = W.DWORD
K.GetDiskFreeSpaceExW.argtypes=[W.LPCWSTR,C.POINTER(C.c_ulonglong),C.c_void_p,C.c_void_p]
QUERY_SYNC = 0x800 | 0x100000
SESSION_KEYS = ('schema', 'pid', 'creation_filetime', 'nonce', 'dll_sha256')


def created(handle):
    values = [W.FILETIME() for _ in range(4)]
    if not K.GetThreadTimes(handle, *(C.byref(v) for v in values)):
        raise OSError(C.get_last_error(), 'GetThreadTimes failed')
    return values[0].dwLowDateTime | values[0].dwHighDateTime << 32


class WorkerLease:
    def __init__(self, ready, expected):
        self.handle = None
        assert all(ready.get(k) == expected[k] for k in SESSION_KEYS)
        assert ready['schema'] in ('sor-d5x/3', 'sor-d5x/4') and ready['ready'] is True and ready['hooks'] == 18
        self.expected = dict(expected)
        self.tid, self.creation = ready['worker_thread_id'], ready['worker_creation_filetime']
        assert isinstance(self.tid, int) and self.tid > 0 and isinstance(self.creation, int) and self.creation > 0
        handle = K.OpenThread(QUERY_SYNC, False, self.tid)
        if not handle:
            raise OSError(C.get_last_error(), 'Cannot acquire worker query/synchronization handle')
        try:
            if K.GetProcessIdOfThread(handle) != ready['pid']:
                raise AssertionError('Worker belongs to another process')
            assert created(handle) == self.creation
            self.handle = handle
            assert self.alive(), 'Worker already exited before admission'
        except BaseException:
            self.handle = None
            K.CloseHandle(handle)
            raise

    def alive(self):
        assert self.handle
        state = K.WaitForSingleObject(self.handle, 0)
        if state == 258:
            return True
        if state == 0:
            return False
        raise OSError(C.get_last_error(), 'Worker wait query failed')

    def verify_ack(self, ack, challenge):
        assert all(ack.get(k) == self.expected[k] for k in SESSION_KEYS)
        assert ack['worker_thread_id'] == self.tid and ack['worker_creation_filetime'] == self.creation
        assert ack['request_nonce'] == challenge and len(challenge) == 32
        assert all(c in '0123456789abcdef' for c in challenge)
        assert ack['hooks_intact'] and ack['capture_active'] and ack.get('output_faults', 0) == 0
        assert self.alive(), 'ACK cannot revive an exited worker'

    def close(self):
        if self.handle:
            if not K.CloseHandle(self.handle):
                raise AssertionError('CloseHandle failed')
            self.handle = None


def read_json(path):
    with Path(path).open('rb') as stream:
        data = stream.read(65537)
    assert len(data) <= 65536
    return json.loads(data)


def disk_guard():
    for drive in ('C:/','D:/'):
        available=C.c_ulonglong()
        if not K.GetDiskFreeSpaceExW(drive,C.byref(available),None,None):
            raise OSError(C.get_last_error(),'Disk query failed')
        assert available.value>=40_000_000_000,'Disk floor failed'


def exclusive(path, value):
    disk_guard()
    with Path(path).open('x', encoding='utf8', newline='\n') as stream:
        json.dump(value, stream, indent=2)
        stream.write('\n')
        stream.flush()
        os.fsync(stream.fileno())


def qualify(out):
    out = Path(out).resolve()
    root = Path(__file__).resolve().parents[2] / '.local-work/d5ab'
    assert out.is_relative_to(root)
    disk_guard()
    out.mkdir(parents=True, exist_ok=False)
    release = threading.Event()
    thread = threading.Thread(target=lambda: release.wait(30))
    thread.start()
    handle = K.OpenThread(QUERY_SYNC, False, thread.native_id)
    assert handle
    expected = dict(schema='sor-d5x/3', pid=os.getpid(), creation_filetime=1, nonce='a' * 64, dll_sha256='b' * 64)
    ready = dict(expected, ready=True, hooks=18, worker_thread_id=thread.native_id, worker_creation_filetime=created(handle))
    K.CloseHandle(handle)
    results = []
    lease = None
    try:
        lease = WorkerLease(ready, expected)
        assert lease.alive()
        results.append('live-original-worker')
        for key, value in (('pid', os.getpid() + 1), ('worker_creation_filetime', ready['worker_creation_filetime'] + 1),
                           ('worker_thread_id', 0), ('nonce', 'c' * 64), ('schema', 'sor-d5x/2')):
            bad = dict(ready, **{key: value})
            try:
                wrong = WorkerLease(bad, expected)
            except (AssertionError, OSError):
                results.append('reject-' + key)
            else:
                wrong.close()
                raise AssertionError('Incorrect worker identity accepted')
        ack = dict(ready, request_nonce='1' * 32, hooks_intact=True, capture_active=True, output_faults=0)
        lease.verify_ack(ack, '1' * 32)
        try:
            lease.verify_ack(dict(ack, worker_creation_filetime=ready['worker_creation_filetime'] + 1), '1' * 32)
        except AssertionError:
            results.append('reject-reused-tid-creation')
        else:
            raise AssertionError('Reused TID identity accepted')
        release.set()
        thread.join(5)
        assert not thread.is_alive() and not lease.alive()
        results.append('detect-actual-exit')
        try:
            lease.verify_ack(ack, '1' * 32)
        except AssertionError:
            results.append('reject-stale-ack-after-exit')
        else:
            raise AssertionError('Stale ACK revived worker')
    finally:
        release.set()
        thread.join(5)
        if lease:
            lease.close()
    receipt = dict(schema='sor-d5ab-worker-health-tests/1', passed=True, cases=results,
                   script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                   effect='Own disposable Python thread only; no game process.')
    exclusive(out / 'receipt.json', receipt)
    print(json.dumps(receipt))


def watch(session, expected_path, expected_sha256, out):
    # Execution is reserved for a separately approved B2 control plan.
    disk_guard()
    with Path(expected_path).open('rb') as stream:expected_bytes=stream.read(65537)
    assert len(expected_bytes)<=65536
    assert hashlib.sha256(expected_bytes).hexdigest() == expected_sha256
    expected = json.loads(expected_bytes)
    session, out = Path(session).resolve(), Path(out).resolve()
    assert not out.exists()
    ready = read_json(session / 'ready.json')
    lease = WorkerLease(ready, expected)
    try:
        exclusive(out, dict(state='BOUND_LIVE', controller_pid=os.getpid(), expected=expected,
                            worker_thread_id=lease.tid, worker_creation_filetime=lease.creation))
        while lease.alive():
            disk_guard()
            time.sleep(0.25)
        exclusive(out.with_name(out.name + '.exit.json'), dict(state='EXPECTED_STOP_EXIT' if (session / 'STOP').is_file() else 'UNEXPECTED_WORKER_EXIT', expected=expected))
    finally:
        lease.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--qualify', type=Path)
    parser.add_argument('--watch', type=Path)
    parser.add_argument('--expected', type=Path)
    parser.add_argument('--expected-sha256')
    parser.add_argument('--out', type=Path)
    args = parser.parse_args()
    if args.qualify:
        qualify(args.qualify)
    else:
        assert args.watch and args.expected and args.expected_sha256 and args.out
        watch(args.watch, args.expected, args.expected_sha256, args.out)
