# SPDX-License-Identifier: GPL-3.0-or-later
"""Explicit future native attachment transport; NOT authorized by Phase A.

Requires a separately approved run card/GO and hash-bound admission receipt.
Reads that receipt, build/source pins and target PID. Runs the native controller,
persists SRO1 snapshots/ACKs plus a flushed event journal in a fresh ignored
directory. STOP may terminate the target under the future crash-tolerant policy.
No game launch, save/configuration/database writes, network or Git operations.
"""
import argparse
import json
import os
from pathlib import Path
import queue
import shutil
import subprocess
import threading
import importlib.util
from build import ROOT, LOCAL, pin


def load(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


transport = load('d5e_pump_transport', 'research/resource-oracle-retail/collect.py')
verifier = load('d5e_pump_decoder', 'research/resource-tungsten-acquisition/qualify.py')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--retail-pilot', action='store_true', required=True)
    parser.add_argument('--admission', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    admission, output = args.admission.resolve(), args.output.resolve()
    assert admission.is_relative_to(LOCAL) and output.is_relative_to(LOCAL)
    gate = json.loads(admission.read_text())
    assert gate['status'] == 'GO' and gate['phase'] == 'B' and gate['source'] == '0:37536:20928:0029d20e'
    # A JSON flag never supplies human authorization. The separately reviewed
    # run card controls its creation and admission checks before this command.
    for field in ('run_card', 'preflight', 'build_manifest'):
        assert pin(gate[field]['path']) == gate[field]['sha256']
    manifest = json.loads(Path(gate['build_manifest']['path']).read_text())
    assert manifest['exit_code'] == 0
    for path, digest in manifest['files'].items():
        assert pin(path) == digest, path
    controller = Path(gate['build_manifest']['path']).parent / 'sor-d5e-native-controller.exe'
    assert pin(controller) == manifest['files'][str(controller)]
    assert min(shutil.disk_usage(d).free for d in ('C:/', 'D:/')) >= 40_000_000_000
    return pump([str(controller), '--retail-pilot', str(gate['pid'])], output, gate, pin(admission), False)


def pump(command, output, gate, admission_hash, synthetic, test_failure=None):
    """Shared bounded external transport, also exercised by disposable fixtures."""
    output.mkdir(exist_ok=False)
    transport.write(output / 'admission.json', gate)
    assert test_failure is None or synthetic
    if test_failure == 'pre-arm-stop':
        (output / 'STOP').write_bytes(b'fixture cancellation\n')
    stderr = (output / 'stderr.txt').open('xb')
    process = subprocess.Popen(command,
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=stderr, text=True)
    try:
        return _events(process, output, admission_hash, synthetic, test_failure)
    except BaseException as error:
        try:
            transport.write(output / 'transport-failure.json', dict(reason=type(error).__name__,
                detail=str(error), coverage='GAP', controller_pid=process.pid))
        except OSError:
            pass
        raise
    finally:
        # The controller owns kill-on-debugger-exit. Retiring it after transport
        # failure intentionally disposes the research target under the card.
        if process.poll() is None:
            process.terminate()
        process.wait(timeout=15)
        process.stdin.close()
        process.stdout.close()
        stderr.close()


def _events(process, output, admission_hash, synthetic, test_failure):
    incoming = queue.Queue(maxsize=32)
    def reader():
        for line in process.stdout:
            incoming.put(line)
        incoming.put(None)
    threading.Thread(target=reader, daemon=True).start()
    session, number, stopping = None, 0, False
    with (output / 'events.jsonl').open('x', encoding='utf8', newline='\n') as journal:
        while True:
            try:
                line = incoming.get(timeout=1)
            except queue.Empty:
                if test_failure == 'idle-collector-loss':
                    raise RuntimeError('synthetic idle collector failure')
                if test_failure == 'idle-pipe-loss':
                    process.stdin.close()
                    test_failure = None
                # An idle STOP is an intentional abort and may precede a queued
                # sample; that race yields a declared GAP, never a forged ACK.
                if not stopping and ((output / 'STOP').exists() or min(shutil.disk_usage(d).free for d in ('C:/', 'D:/')) < 40_000_000_000):
                    process.stdin.write('STOP\n');process.stdin.flush();stopping=True
                continue
            if line is None:
                break
            row = json.loads(line)
            journal.write(json.dumps(row) + '\n');journal.flush();os.fsync(journal.fileno())
            if row['kind'] == 'SESSION':
                assert session is None and row['synthetic'] is synthetic
                session = row
            if row['kind'] in ('SAMPLE', 'ARM_BARRIER'):
                assert session
                number += 1
                envelope = [dict(session, admission_sha256=admission_hash),
                    dict(kind='SAMPLE', event=row), dict(kind='END', complete=row.get('native_read_complete', True))]
                path = output / f'capture-{number:06d}.bin'
                transport.persist(path, envelope, synthetic=synthetic)
                assert verifier.independent(path) == envelope
                if stopping:
                    continue
                if row['kind'] == 'ARM_BARRIER':
                    if (output / 'STOP').exists():
                        answer = 'STOP'
                        stopping = True
                    else:
                        answer = 'ARM_ACK'
                        transport.write(output / 'READY.json', dict(admission_sha256=admission_hash,
                            barrier_sha256=pin(path), session=session, state='ARMED_BEFORE_OPERATOR_LOAD'))
                else:
                    suffix = ' STOP' if (output / 'STOP').exists() else ''
                    answer = f'ACK {row["capture"]}{suffix}'
                    stopping = bool(suffix)
                process.stdin.write(answer + '\n');process.stdin.flush()
    code = process.wait(timeout=15)
    transport.write(output / 'controller-exit.json', dict(exit_code=code, requested_stop=stopping))
    return code


if __name__ == '__main__':
    raise SystemExit(main())
