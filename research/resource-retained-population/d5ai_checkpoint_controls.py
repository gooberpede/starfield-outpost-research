# SPDX-License-Identifier: GPL-3.0-or-later
"""Qualify durable baseline checkpoints on native output and disposable derivatives.

Reads one explicit stopped native fixture and its built DLL, then creates local
copies for negative controls and exclusive receipts. Never contacts a process or
changes original captures, saves, databases, network or Git. Copied files may be
truncated or removed only under the fresh task-local output. Stdlib only.
Actual live worker health remains the independently tested controller's job.
"""
import sys
if not __debug__ or sys.flags.optimize:
    raise RuntimeError('Use Python -E -B')

import argparse
import copy
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

from d5ae_baseline import guard, sha
import d5ai_checkpoint as checkpoint


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('build', type=Path)
    parser.add_argument('out', type=Path)
    parser.add_argument('--native-checkpoint', type=Path, required=True)
    args = parser.parse_args()
    guard()
    root = checkpoint.reducer.ROOT
    if not args.out.resolve().is_relative_to(root / '.local-work/d5ai'):
        raise ValueError('Task-local output required')
    args.out.mkdir(exist_ok=False)
    digest = sha(args.build / 'SorConstructionWinner.dll')
    expected_build = checkpoint.reducer.load(args.build / 'build.json')
    if (digest not in expected_build['outputs'].values() or expected_build['source_unchanged'] is not True or
            not all(row['pass_exit'] for row in expected_build['cases'])):
        raise ValueError('Build/DLL correspondence failed')
    native = checkpoint.reducer.load(args.native_checkpoint)
    if (native['failure'] is not None or native['exit'] != 0 or native['dll_sha256'] != digest or
            native['native_prefix']['state'] != 'BASELINE_PREFIX_QUALIFIED'):
        raise ValueError('Actual fresh native checkpoint did not qualify')
    session = Path(native['command'][2])
    nonce = native['nonce']
    inspect = lambda p: checkpoint.inspect_prefix(p, digest, 1, nonce, checkpoint.reducer.read_capture.TARGET, 0x5e0de)
    tests = []

    def check(name, condition):
        tests.append(dict(name=name, passed=bool(condition)))
        if not condition:
            raise AssertionError(name)

    positive = inspect(session)
    check('native-durable-baseline', positive['state'] == 'BASELINE_PREFIX_QUALIFIED')
    check('no-finalization-or-departure-upgrade', positive['complete_session'] is False and positive['permission_to_depart'] is False and positive['live_worker_verified'] is False)
    for label in ('stale-count', 'wrong-nonce', 'wrong-identity', 'drop', 'boolean-count',
                  'truncated-prefix', 'changed-prefix', 'missing-whole-snapshot', 'false-completion',
                  'duplicate-key', 'contradictory-frequency', 'unacknowledged-tail'):
        destination = args.out / label
        shutil.copytree(session, destination)
        if not destination.resolve().is_relative_to(args.out.resolve()):
            raise ValueError('Controlled-copy boundary failed')
        ack_path = destination / ('ack-' + nonce + '.json')
        ack = checkpoint.load_ack(ack_path)
        if label == 'stale-count': ack['geometry_completed'] = 0
        elif label == 'wrong-nonce': ack['request_nonce'] = 'b' * 32
        elif label == 'wrong-identity': ack['dll_sha256'] = '0' * 64
        elif label == 'drop': ack['drops'] = 1
        elif label == 'boolean-count': ack['drops'] = False
        elif label == 'truncated-prefix':
            path = destination / 'events.bin'
            path.write_bytes(path.read_bytes()[:ack['flushed'] * 328 - 1])
        elif label == 'changed-prefix':
            path = destination / 'events.bin'
            raw = bytearray(path.read_bytes())
            raw[100] ^= 1
            path.write_bytes(raw)
        elif label == 'missing-whole-snapshot':
            (destination / 'geometry-1.bin').unlink()
            (destination / 'geometry-1.json').unlink()
        elif label == 'false-completion':
            path = destination / 'geometry-1.json'
            value = checkpoint.reducer.load(path)
            value['flushed'] = False
            path.write_text(json.dumps(value) + '\n', encoding='utf8', newline='\n')
        elif label == 'unacknowledged-tail':
            path = destination / 'events.bin'
            with path.open('ab') as stream:
                stream.write(b'\x01\x02\x03')
        payload = json.dumps(ack)
        if label == 'duplicate-key': payload = payload[:-1] + ',"geometry_completed":1}'
        elif label == 'contradictory-frequency': payload = payload[:-1] + ',"qpc_frequency":1}'
        ack_path.write_text(payload + '\n', encoding='utf8', newline='\n')
        try:
            actual = inspect(destination)
        except (ValueError, OSError, KeyError, TypeError):
            check(label, label != 'unacknowledged-tail')
        else:
            check(label, label == 'unacknowledged-tail' and actual['state'] == 'BASELINE_PREFIX_QUALIFIED')
    source_paths = [Path(checkpoint.__file__), Path(checkpoint.reducer.__file__),
                    Path(checkpoint.reducer.__file__).with_name('d5ai_geometry.py'),
                    Path(checkpoint.reducer.__file__).with_name('d5ai_lifetime.py'),
                    Path(checkpoint.reducer.__file__).with_name('d5ae_baseline.py')]
    source_paths += [root / 'runtime/construction-winner' / n for n in
                     ('read_capture.py', 'reduce_v3.py', 'reduce_v4.py', 'd5ai_read_geometry.py', 'd5ai_read_lifetime.py')]
    lock = dict(schema='sor-d5ai-source-lock/1', repository_root=str(root), dll_sha256=digest,
                interpreter_sha256=sha(sys.executable), sources={str(p.resolve()): sha(p) for p in source_paths})
    lock_path = args.out / 'source-lock.json'
    lock_path.write_text(json.dumps(lock, indent=2) + '\n', encoding='utf8', newline='\n')
    command = [sys.executable, '-E', '-B', checkpoint.__file__, str(session), '--dll-sha256', digest,
               '--snapshot', '1', '--nonce', nonce, '--source-lock', str(lock_path),
               '--source-lock-sha256', sha(lock_path), '--out', str(args.out / 'cli-positive.json')]
    run = subprocess.run(command, capture_output=True)
    (args.out / 'cli.log').write_bytes(run.stdout + run.stderr)
    check('actual-source-bound-cli', run.returncode == 0)
    bad = copy.deepcopy(lock)
    bad['sources'][str(Path(checkpoint.__file__).resolve())] = '0' * 64
    bad_path = args.out / 'bad-lock.json'
    bad_path.write_text(json.dumps(bad) + '\n', encoding='utf8', newline='\n')
    try:
        checkpoint.verify_source_lock(bad_path, sha(bad_path), digest)
    except ValueError:
        check('source-drift-refused', True)
    else:
        check('source-drift-refused', False)
    wrong_root = copy.deepcopy(lock)
    wrong_root['repository_root'] = str(root / '.local-work')
    root_path = args.out / 'bad-root-lock.json'
    root_path.write_text(json.dumps(wrong_root) + '\n', encoding='utf8', newline='\n')
    try:
        checkpoint.verify_source_lock(root_path, sha(root_path), digest)
    except ValueError:
        check('foreign-output-root-refused', True)
    else:
        check('foreign-output-root-refused', False)
    result = dict(tests=tests, passed=len(tests), command=command, native_prefix=positive,
                  method_sha256=sha(__file__), checkpoint_sha256=sha(checkpoint.__file__),
                  build_sha256=sha(args.build / 'build.json'), source_lock_sha256=sha(lock_path),
                  native_checkpoint_sha256=sha(args.native_checkpoint))
    (args.out / 'receipt.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf8', newline='\n')
    for method in (Path(__file__), Path(checkpoint.__file__)):
        (args.out / method.name).write_bytes(method.read_bytes())
    print(json.dumps(dict(passed=len(tests))))


if __name__ == '__main__':
    main()
