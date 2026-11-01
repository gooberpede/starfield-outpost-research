# SPDX-License-Identifier: GPL-3.0-or-later
"""Control an explicitly selected disposable recorder session, never a game.

Reads identity, READY, challenge ACK, framed raw/flush data and terminal receipts.
Writes an exclusive controller journal, lock, request and authenticated STOP files
only in that session. Uses installed Windows query/synchronization APIs and stdlib.
No launch, attachment, memory access, injection, unload, kill or automatic recovery.
The caller owns finite offline test stimuli; polling delay never retires capture.
"""

import sys

# Safety checks below require assertions, including when imported as a helper.
if not __debug__ or sys.flags.optimize != 0:
    raise RuntimeError('Python optimization is forbidden; invoke with -E -B and no -O/-OO')
import hashlib
import json
import msvcrt
import os
from pathlib import Path
import secrets
import struct
import zlib

from worker_health import WorkerLease, read_json, disk_guard, exclusive, K
from ctypes import wintypes as W

K.OpenProcess.argtypes = [W.DWORD, W.BOOL, W.DWORD]
K.OpenProcess.restype = W.HANDLE
K.GetProcessTimes.argtypes = K.GetThreadTimes.argtypes
LOSS_KEYS = ('drops', 'queue_full', 'contention_exhausted', 'reentrant_losses')


def loss_counts(receipt):
    values = tuple(receipt[key] for key in LOSS_KEYS)
    assert all(type(value) is int and 0 <= value < 2 ** 64 for value in values)
    assert values[0] == sum(values[1:])
    return values


class Controller:
    def __init__(self, session, expected):
        self.session = Path(session).resolve()
        self.expected = dict(expected)
        self.lease = None
        self.lock = None
        self.challenge = None
        self.stop = None
        self.last_ack = None
        identity = read_json(self.session / 'identity.json')
        assert identity == expected and identity['retail'] is False
        root = Path(__file__).resolve().parents[2] / '.local-work/d5x'
        assert self.session.is_relative_to(root), 'Disposable sessions only'
        self.identity_hash = hashlib.sha256((self.session / 'identity.json').read_bytes()).hexdigest()
        process = K.OpenProcess(0x1000 | 0x100000, False, identity['pid'])
        assert process
        try:
            values = [W.FILETIME() for _ in range(4)]
            import ctypes
            if not K.GetProcessTimes(process, *(ctypes.byref(v) for v in values)):
                raise AssertionError('GetProcessTimes failed')
            birth = values[0].dwLowDateTime | values[0].dwHighDateTime << 32
            assert birth == identity['creation_filetime']
            if K.WaitForSingleObject(process, 0) != 258:
                raise AssertionError('Expected live disposable process')
        finally:
            K.CloseHandle(process)
        try:
            disk_guard()
            self.lock = (self.session / 'controller.lock').open('a+b')
            self.lock.seek(0)
            msvcrt.locking(self.lock.fileno(), msvcrt.LK_NBLCK, 1)
            self.lease = WorkerLease(read_json(self.session / 'ready.json'), expected)
            self.owner = secrets.token_hex(16)
            exclusive(self.session / ('controller-' + self.owner + '.json'),
                      dict(owner=self.owner, controller_pid=os.getpid(), identity_sha256=self.identity_hash))
        except BaseException:
            self.close()
            raise

    def request(self):
        assert not self.challenge and not self.stop and self.lease.alive()
        self.challenge = secrets.token_hex(16)
        pending = self.session / ('request-' + self.challenge + '.pending')
        disk_guard()
        with pending.open('xb') as stream:
            stream.write(self.challenge.encode('ascii'))
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(pending, self.session / 'request.txt')
        return self.challenge

    def prefix(self, ack):
        """Authenticate the challenged durable prefix without requiring idle writers."""
        count = ack['flushed']
        assert type(count) is int and count >= 0 and ack['acknowledged'] == count
        raw = (self.session / 'events.bin').read_bytes()[:count * 328]
        assert len(raw) == count * 328
        for index in range(count):
            frame = raw[index * 328:(index + 1) * 328]
            magic, size, sequence, crc = struct.unpack_from('<4I', frame)
            actual = struct.unpack_from('<Q', frame, 16)[0]
            expected = self.expected.get('sequence_origin', 0) + index + 1
            assert magic == 0x31505253 and size == 312
            assert actual == expected and sequence == (expected & 0xffffffff)
            assert zlib.crc32(frame[16:]) == crc
        matches = []
        for line in (self.session / 'flush.jsonl').read_bytes().splitlines(keepends=True):
            if not line.endswith(b'\n'):
                break
            receipt = json.loads(line)
            if receipt['records'] == count:
                matches.append(receipt)
        assert len(matches) == 1
        receipt = matches[0]
        assert receipt['identity_sha256'] == self.identity_hash
        assert receipt['bytes'] == len(raw) and receipt['prefix_crc32'] == zlib.crc32(raw)
        loss_counts(receipt)
        return receipt

    def poll(self):
        disk_guard()
        if not self.lease.alive():
            terminal_path = self.session / 'terminal.json'
            if not terminal_path.exists():
                return 'EXIT_INCOMPLETE'
            terminal = read_json(terminal_path)
            assert all(terminal.get(k) == v for k, v in self.expected.items())
            if terminal['failed'] or terminal['output_faults'] or terminal['output_fault'] != 'none':
                return 'EXIT_FAULT'
            if self.stop is None or (self.session / 'STOP').read_bytes() != self.stop:
                return 'EXIT_UNOWNED_STOP'
            totals = [terminal[k] for k in ('written', 'flushed', 'acknowledged')]
            if len(set(totals)) != 1 or terminal['enqueued'] != totals[0] + self.expected.get('sequence_origin', 0):
                return 'EXIT_INCOMPLETE'
            try:
                self.prefix(dict(flushed=totals[0], acknowledged=totals[0]))
                from read_capture import inspect
                complete = inspect(self.session, self.expected['dll_sha256'])['complete_session']
            except (AssertionError, ValueError, KeyError, TypeError, OSError, struct.error):
                complete = False
            if not complete:
                return 'EXIT_INCOMPLETE'
            return 'STOPPED_LOSS' if terminal['drops'] else 'STOPPED_COMPLETE'
        if self.stop:
            return 'STOP_PENDING'
        if self.challenge:
            path = self.session / ('ack-' + self.challenge + '.json')
            if not path.exists():
                return 'ALIVE_ACK_PENDING'
            ack = read_json(path)
            self.lease.verify_ack(ack, self.challenge)
            counts = loss_counts(ack)
            prefix = self.prefix(ack)
            assert all(current >= durable for current, durable in zip(counts, loss_counts(prefix)))
            if self.last_ack:
                assert all(current >= prior for current, prior in zip(counts, loss_counts(self.last_ack)))
            assert type(ack['loss_bounds_uncertain']) is bool
            assert ack['counter_overflow'] is False and ack['output_fault'] == 'none'
            assert type(ack['output_faults']) is int and ack['output_faults'] == 0
            self.last_ack = ack
            self.challenge = None
            return 'ALIVE_LOSS' if counts[0] or ack['loss_bounds_uncertain'] else 'HEALTHY'
        return 'ALIVE_UNCHALLENGED'

    def request_stop(self, reason='operator STOP'):
        assert not self.stop and self.lease.alive()
        payload = dict(identity_sha256=self.identity_hash, owner=self.owner,
                       stop_nonce=secrets.token_hex(16), reason=reason)
        self.stop = (json.dumps(payload, sort_keys=True) + '\n').encode()
        disk_guard()
        with (self.session / 'STOP').open('xb') as stream:
            stream.write(self.stop)
            stream.flush()
            os.fsync(stream.fileno())
        return payload

    def close(self):
        if self.lease:
            self.lease.close()
            self.lease = None
        if self.lock:
            self.lock.close()
            self.lock = None
