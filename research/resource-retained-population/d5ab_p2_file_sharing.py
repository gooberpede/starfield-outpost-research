# SPDX-License-Identifier: GPL-3.0-or-later
"""Discriminate command-file sharing in one actual disposable recorder host.

Reads an explicit offline build and owned sources; writes fresh ignored receipts
under `.local-work/d5ab` and `.local-work/d5x`. Holds DELETE access to its own
synthetic command while atomically publishing it. No game, saves, deployment,
downloads, debugger, process termination, Git writes or native source changes.
"""
import ctypes as C
from ctypes import wintypes as W
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'runtime/construction-winner'
sys.path.insert(0, str(SRC))
from controller import Controller
from worker_health import K, read_json, disk_guard
from d5ab_p2_controller import wait

K.CreateFileW.argtypes = [W.LPCWSTR, W.DWORD, W.DWORD, C.c_void_p, W.DWORD, W.DWORD, W.HANDLE]
K.CreateFileW.restype = W.HANDLE
INVALID = C.c_void_p(-1).value


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    build = Path(sys.argv[1]).resolve()
    label = sys.argv[2]
    assert build.is_relative_to(ROOT / '.local-work/d5x') and label.replace('-', '').isalnum()
    out = ROOT / '.local-work/d5ab' / label
    session = ROOT / '.local-work/d5x' / label
    out.mkdir(exist_ok=False)
    inputs = {str(p.relative_to(ROOT)): sha(p) for p in (Path(__file__),
              Path(__file__).with_name('d5ab_p2_controller.py'), SRC / 'controller.py',
              SRC / 'worker_health.py', SRC / 'read_capture.py', SRC / 'reduce_v3.py')}
    package = build / 'package-runtime'
    disk_guard()
    log = (out / 'host.log').open('xb')
    process = subprocess.Popen([str(package / 'sor-d5x-fixture.exe'),
        str(package / 'SorConstructionWinner.dll'), str(session), 'controller-host'], stdout=log, stderr=subprocess.STDOUT)
    controller = handle = None
    receipt = dict(passed=False, inputs=inputs, build=str(build))
    try:
        wait(lambda: (session / 'host-online.json').exists())
        expected = read_json(session / 'identity.json')
        assert expected['pid'] == process.pid and expected['dll_sha256'] == sha(package / 'SorConstructionWinner.dll')
        controller = Controller(session, expected)
        controller.request()
        assert wait(lambda: (state if (state := controller.poll()) != 'ALIVE_ACK_PENDING' else None)) == 'HEALTHY'
        pending = session / 'sharing.pending'
        with pending.open('xb') as stream:
            stream.write(b'loss')
            stream.flush()
            os.fsync(stream.fileno())
        handle = K.CreateFileW(str(pending), 0x10000, 7, None, 3, 0x80, None)
        assert handle != INVALID
        # The previous share-read-only input contract is incompatible with a
        # concurrent DELETE-access publication handle. Record the actual error.
        old_probe = K.CreateFileW(str(pending), 0x80000000, 1, None, 3, 0x80, None)
        error = C.get_last_error()
        receipt.update(old_policy_open_error=error, old_policy_open_rejected=old_probe == INVALID)
        if old_probe != INVALID:
            K.CloseHandle(old_probe)
        assert old_probe == INVALID and error == 32
        pending.rename(session / 'fixture-command.txt')
        wait(lambda: (session / 'command-loss.json').exists())
        K.CloseHandle(handle)
        handle = None
        controller.request()
        assert wait(lambda: (state if (state := controller.poll()) != 'ALIVE_ACK_PENDING' else None)) == 'ALIVE_LOSS'
        controller.request_stop()
        assert wait(lambda: (state if (state := controller.poll()).startswith(('EXIT_', 'STOPPED_')) else None)) == 'STOPPED_LOSS'
        assert process.wait(timeout=20) == 0
        receipt.update(passed=True, final_state='STOPPED_LOSS',
            scope='One deterministic file-sharing interoperability control; historical open error remains UNKNOWN.')
    except BaseException as error:
        receipt['error'] = repr(error)
        raise
    finally:
        if handle and handle != INVALID:
            K.CloseHandle(handle)
        if controller:
            controller.close()
        if process.poll() is None and session.exists() and not (session / 'STOP').exists():
            (session / 'STOP').write_bytes(b'offline sharing test cleanup STOP\n')
        try:
            receipt['exit'] = process.wait(timeout=40)
        except subprocess.TimeoutExpired:
            receipt['cleanup'] = 'Host still running; no termination performed'
        log.close()
        receipt['source_unchanged'] = all(sha(ROOT / name) == digest for name, digest in inputs.items())
        receipt['files'] = {str(p.relative_to(session)): sha(p) for p in session.rglob('*') if p.is_file()}
        (out / 'receipt.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf8', newline='\n')
    assert receipt['passed'] and receipt['source_unchanged']
    print(json.dumps({key: receipt[key] for key in ('passed', 'old_policy_open_error', 'final_state')}))


if __name__ == '__main__':
    main()
