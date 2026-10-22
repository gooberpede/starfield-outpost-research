# SPDX-License-Identifier: GPL-3.0-or-later
"""Synthetic-only launcher and durable C1B receipt writer.

Reads exact owned build/manifest and controller stdout; writes fresh local run.
Creates only the controller, which creates only its sibling disposable target.
No game, attachment, saves, config, DB, network, downloads or Git writes.
"""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import queue
import shutil
import subprocess
import sys
import threading
import time
import uuid

ROOT = Path(__file__).resolve().parents[2]
LOCAL = ROOT / '.local-work/resource-oracle-collector'
spec = importlib.util.spec_from_file_location('c1b_receipt', ROOT/'research/resource-ui-oracle/receipt_probe.py')
receipt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(receipt)


def pin(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write(path, value):
    with Path(path).open('x', encoding='utf8', newline='\n') as f:
        json.dump(value, f, indent=2, sort_keys=True)
        f.write('\n'); f.flush(); os.fsync(f.fileno())


def collect(build, output, mode='good', fault='none', limit=256, target=None):
    build, output = Path(build).resolve(), Path(output).resolve()
    assert build.is_relative_to(LOCAL.resolve()) and output.is_relative_to(LOCAL.resolve())
    assert not any(p.is_symlink() or (p.exists() and p.lstat().st_file_attributes & 0x400)
                   for x in (build, output) for p in (x, *list(x.parents)[:-1]))
    manifest = json.loads((build/'build.json').read_text())
    assert manifest['exit_code'] == 0
    exe, controller = build/'sor-c1c-target.exe', build/'sor-c1c-controller.exe'
    assert target is None or Path(target).resolve() == exe
    for p in (exe, controller):
        assert pin(p) == manifest['files'][str(p)]
    assert 0 < limit <= 256
    assert mode in ('good', 'zero', 'threads', 'bad-pointer', 'bad-count', 'overflow',
                    'budget', 'truncated', 'truncated-resource', 'crash-before', 'crash-after')
    assert fault in ('none', 'interrupt', 'drop', 'malformed', 'ackfail', 'preack-stop')
    assert min(shutil.disk_usage(d).free for d in ('C:/', 'D:/')) >= 40_000_000_000
    output.mkdir(parents=True, exist_ok=False)
    command = [str(controller), '--synthetic-only', pin(exe), mode, fault, str(limit)]
    config = dict(schema='sor-resource-oracle/1+c1c-synthetic-1', nonce=str(uuid.uuid4()),
                  synthetic=True, command=command, mode=mode, fault=fault, limit=limit,
                  exe_sha256=pin(exe), controller_sha256=pin(controller),
                  sources={str(p.relative_to(ROOT)): pin(p) for p in sorted(Path(__file__).parent.glob('*')) if p.is_file()},
                  transport_sha256=pin(ROOT/'research/resource-ui-oracle/receipt_probe.py'),
                  monotonic='perf_counter_ns', clock=time.get_clock_info('perf_counter')._asdict()
                  if hasattr(time.get_clock_info('perf_counter'), '_asdict') else str(time.get_clock_info('perf_counter')))
    write(output/'config.json', config)
    log, losses, acks = [], [], []
    native_session = None
    p = subprocess.Popen(command, cwd=build, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, text=True, encoding='utf8')
    incoming = queue.Queue()

    def reader():
        for line in p.stdout:
            incoming.put(line)
        incoming.put(None)

    thread = threading.Thread(target=reader, daemon=True); thread.start()
    try:
        while True:
            # Fixture-only liveness watchdog: these deterministic programs need no operator input.
            line = incoming.get(timeout=30)
            if line is None:
                break
            row = json.loads(line); row['received_ns'] = time.perf_counter_ns(); log.append(row)
            if row['kind'] == 'SESSION':
                assert native_session is None and row['exe_sha256'] == pin(exe)
                native_session = row
            if row['kind'] != 'SAMPLE':
                continue
            for population in row['populations'].values():
                if population['status'] == 'COMPLETE':
                    copied = bytes.fromhex(population['raw_pointer_bytes'])
                    copied += b''.join(bytes.fromhex(m['raw']) for m in population['members'])
                    population['payload_sha256'] = hashlib.sha256(copied).hexdigest()
                else:
                    population['payload_sha256'] = None
            assert native_session is not None and row['pid'] == native_session['pid']
            assert row['capture'] == len([r for r in log if r['kind'] == 'SAMPLE'])
            path = output / f"capture-{row['capture']:04d}.bin"
            valid = all(v['status'] == 'COMPLETE' for v in row['populations'].values())
            row['read_status'] = 'COMPLETE' if valid else 'INCOMPLETE'
            if not valid:
                losses.append(dict(capture=row['capture'], reason='INCOMPLETE native population'))
            try:
                if fault == 'drop' and row['capture'] == 2:
                    raise ValueError('injected event loss before serialization')
                rows = [dict(kind='SESSION', config_sha256=pin(output/'config.json'), **{k:v for k,v in native_session.items() if k != 'kind'}),
                        row, dict(kind='END', capture=row['capture'], complete=valid)]
                if fault == 'malformed' and row['capture'] == 1:
                    path.write_bytes(receipt.frame(1, rows[0])[:-1])
                    receipt.decode(path.read_bytes())
                if fault == 'preack-stop' and row['capture'] == 1:
                    path.write_bytes(receipt.frame(1, rows[0])+receipt.frame(2, row))
                    raise ValueError('injected STOP before END/flush/readback acknowledgement')
                ack = receipt.persist(path, rows)
                # Failed ACK is an injected fault at the external acknowledgement boundary;
                # persisted payload may still be usable offline, but session acquisition fails.
                if fault == 'ackfail' and row['capture'] == 1:
                    raise ValueError('injected durable acknowledgement rejection')
                actual = json.loads(path.with_suffix('.ack.json').read_text())
                assert actual == ack and actual['sha256'] == pin(path)
                assert receipt.decode(path.read_bytes())[1] == row
                acks.append(dict(capture=row['capture'], **ack))
                response = f"ACK {row['capture']}\n" if valid else 'STOP\n'
            except (ValueError, OSError, AssertionError) as error:
                losses.append(dict(capture=row['capture'], reason=str(error)))
                response = 'STOP\n'
            p.stdin.write(response); p.stdin.flush()
        code = p.wait(timeout=10)
        stderr = p.stderr.read()
    except BaseException as error:
        losses.append(dict(reason=repr(error)))
        p.kill(); code = p.wait(timeout=10); stderr = p.stderr.read()
    finally:
        p.stdin.close(); p.stdout.close(); p.stderr.close()
    exits = [r for r in log if r['kind'] == 'EXIT']
    captures = [r for r in log if r['kind'] == 'SAMPLE']
    if code or not exits or exits[-1]['captures'] != len(captures) or len(acks) != len(captures):
        losses.append(dict(reason='controller/terminal/capture/ACK accounting'))
    if not captures:
        losses.append(dict(reason='no acknowledged native sample'))
    result = dict(command=command, controller_exit=code, stderr=stderr, losses=losses,
                  acquisition='PASS' if not losses else 'FAIL', captures=len(captures), acknowledgements=acks,
                  target_exit=exits[-1] if exits else None,
                  evidence_files={f.name: pin(f) for f in sorted(output.iterdir()) if f.is_file()})
    write(output/'events.json', log); write(output/'result.json', result)
    print(output.name, result['acquisition'], len(captures), 'ack', len(acks), 'exit', exits[-1]['code'] if exits else None)
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--synthetic-only', required=True, action='store_true')
    ap.add_argument('--build', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--target', type=Path)
    ap.add_argument('--mode', default='good')
    ap.add_argument('--fault', default='none')
    ap.add_argument('--stop-after', type=int, default=256)
    a = ap.parse_args()
    r = collect(a.build, a.output, a.mode, a.fault, a.stop_after, a.target)
    return 0 if r['acquisition'] == 'PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())
