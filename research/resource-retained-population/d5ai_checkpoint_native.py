# SPDX-License-Identifier: GPL-3.0-or-later
"""Request a fresh post-capture ACK from an explicitly owned disposable host.

Launches only the supplied task-local compiled fixture/DLL with fixed retained
scenario. Publishes one challenge in its new private session; reads native output
and validates a completed durable prefix. No Starfield, debugger, process memory,
save, deployment, network or Git operation. Writes new ignored receipts only.
The host exits through its own declared STOP. On failure retain all evidence;
no unrelated process is stopped. Stdlib only; installed Python -E -B required.
"""
import sys
if not __debug__ or sys.flags.optimize:
    raise RuntimeError('Use Python -E -B')

import argparse
import json
import os
from pathlib import Path
import secrets
import subprocess
import time

from d5ae_baseline import guard, sha
import d5ai_checkpoint as checkpoint


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('build', type=Path)
    parser.add_argument('out', type=Path)
    parser.add_argument('--dll-sha256', required=True)
    args = parser.parse_args()
    guard()
    root = checkpoint.reducer.ROOT
    if (not args.out.resolve().is_relative_to(root / '.local-work/d5ai') or
            not args.build.resolve().is_relative_to(root / '.local-work/d5ai-recorder')):
        raise ValueError('Explicit task-local build and fresh output required')
    package = args.build / 'package-runtime'
    dll, host = package / 'SorConstructionWinner.dll', package / 'sor-d5x-fixture.exe'
    if sha(dll) != args.dll_sha256:
        raise ValueError('Compiled candidate changed')
    args.out.mkdir(exist_ok=False)
    session = args.out / 'native-session'
    command = [str(host.resolve()), str(dll.resolve()), str(session.resolve()), 'd5ai-retained']
    log = (args.out / 'host.log').open('xb')
    process = subprocess.Popen(command, stdout=log, stderr=subprocess.STDOUT, creationflags=subprocess.CREATE_NO_WINDOW)
    nonce = secrets.token_hex(16)
    result = dict(command=command, pid=process.pid, dll_sha256=sha(dll), host_sha256=sha(host),
                  nonce=nonce, method_sha256=sha(__file__), native_prefix=None, failure=None)
    try:
        while not (session / 'geometry-1.json').exists():
            if process.poll() is not None:
                raise RuntimeError('Disposable host did not publish its first geometry receipt')
            time.sleep(0.001)
        pending = session / ('checkpoint-' + nonce + '.pending')
        with pending.open('xb') as stream:
            stream.write(nonce.encode('ascii'))
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(pending, session / 'request.txt')
        ack = session / ('ack-' + nonce + '.json')
        while not ack.exists():
            if process.poll() is not None:
                raise RuntimeError('No fresh post-capture native challenge ACK')
            time.sleep(0.001)
        result['terminal_present_before_prefix_check'] = (session / 'terminal.json').exists()
        result['native_prefix'] = checkpoint.inspect_prefix(session, args.dll_sha256, 1, nonce,
                                                          checkpoint.reducer.read_capture.TARGET, 0x5e0de)
        if result['native_prefix']['state'] != 'BASELINE_PREFIX_QUALIFIED':
            raise ValueError('Actual native prefix did not qualify')
    except Exception as error:
        result['failure'] = type(error).__name__ + ': ' + str(error)
    finally:
        try:
            result['exit'] = process.wait(timeout=60)
        except subprocess.TimeoutExpired:
            result['exit'] = 'STILL_RUNNING_OWNED_HOST'
            result['failure'] = result['failure'] or 'Host failed its own declared STOP; preserve PID for owned recovery'
        log.close()
        result['checkpoint_sha256'] = sha(checkpoint.__file__)
        (args.out / 'receipt.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf8', newline='\n')
    if result['failure'] or result['exit'] != 0:
        raise RuntimeError(result['failure'] or 'Native host exit failed')
    print(json.dumps(dict(state=result['native_prefix']['state'], terminal_present_before_check=result['terminal_present_before_prefix_check'], exit=result['exit'])))


if __name__ == '__main__':
    main()
