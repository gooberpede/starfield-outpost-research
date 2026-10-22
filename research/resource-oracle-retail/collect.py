# SPDX-License-Identifier: GPL-3.0-or-later
"""Explicit retail launcher, external durable transport, no arbitrary live timeout.

Reads fresh preflight/build pins; launches only the separate pinned retail
controller. Writes raw native receipts only to fresh ignored local output.
STOP file requests declared controlled disposal; otherwise natural process exit.
No save/configuration writes, installation, network or Git mutation.
Owned C1C transport orchestration adapted at 60ce35a; C1B framing reused.
"""
import argparse
import datetime
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import queue
import shutil
import subprocess
import threading
import time

ROOT = Path(__file__).resolve().parents[2]
LOCAL = ROOT / '.local-work/resource-oracle-retail'
spec = importlib.util.spec_from_file_location('c1b', ROOT / 'research/resource-ui-oracle/receipt_probe.py')
receipt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(receipt)


def pin(p):
    with Path(p).open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def write(p, value):
    with p.open('x', encoding='utf8', newline='\n') as f:
        json.dump(value, f, indent=2)
        f.write('\n')
        f.flush()
        os.fsync(f.fileno())


def persist(path, rows, synthetic=False):
    # Same C1B frame/decoder, explicit retail ACK domain rather than synthetic=True.
    raw = b''.join(receipt.frame(i+1, row) for i, row in enumerate(rows))
    with path.open('xb') as f:
        f.write(raw)
        f.flush()
        os.fsync(f.fileno())
    actual = path.read_bytes()
    assert actual == raw and receipt.decode(actual) == rows
    ack = dict(bytes=len(raw), sha256=pin(path), records=len(rows), synthetic=synthetic,
               status='DURABLE_READBACK')
    write(path.with_suffix('.ack.json'), ack)
    assert json.loads(path.with_suffix('.ack.json').read_text()) == ack
    return ack


def preserve_sample(output, session, row, synthetic=False):
    complete = all(v['status'] == 'COMPLETE' for v in row['populations'].values())
    for key in ('refresh_payload', 'produced'):
        if key in row:
            complete &= row[key]['status'] == 'COMPLETE'
    path = output / f'capture-{row["capture"]:05d}.bin'
    ack = persist(path, [session, row, dict(kind='END', complete=complete)], synthetic)
    payload = row.get('refresh_payload', {})
    useful = (row['identity'] == 'BOUND' and row.get('refresh_payload_site_ancestry') == 'BOUND_TRANSFER'
              and payload.get('status') == 'COMPLETE'
              and any(m['runtime_formid'] == 0x57d4 for m in payload['members'])
              and any(p['runtime_formid'] == 0x57d4 and p['provenance']['status'] == 'COMPLETE' and p['provenance']['main_file_identity']
                      for p in row.get('payload_file_provenance', [])))
    return ack, useful


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--retail-pilot', required=True, action='store_true')
    ap.add_argument('--build', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--pid', type=int, required=True)
    ap.add_argument('--launch', type=Path, default=LOCAL / 'steam-launch.json')
    ap.add_argument('--gate', type=Path, default=LOCAL / 'launch-gate.json')
    a = ap.parse_args()
    build, output = a.build.resolve(), a.output.resolve()
    assert build.is_relative_to(LOCAL) and output.is_relative_to(LOCAL) and not output.exists()
    for p in (build, output):
        for q in (p, *p.parents):
            assert not q.exists() or not q.lstat().st_file_attributes & 0x400
    manifest = json.loads((build / 'build.json').read_text())
    assert manifest['exit_code'] == 0
    exe = build / 'sor-c1d-controller.exe'
    assert pin(exe) == manifest['files'][str(exe)]
    # Every source compiled into this binary must still match.
    for name, digest in manifest['files'].items():
        if name.endswith(('.cpp', '.h')):
            assert pin(name) == digest, name
    pre = json.loads((LOCAL / 'preflight-saves.json').read_text())
    assert pre['live'] == pre['backup'] and pre['cloud_disabled']
    from saves import SAVES
    # Hash-bound full audit belongs before launch and after exit. During main-menu
    # attachment use names/sizes only; do not repeat a full live save scan.
    for folder in (SAVES, Path(pre['backup_path'])):
        paths = [p for p in folder.rglob('*') if p.is_file()]
        assert all(not p.lstat().st_file_attributes & 0x400 for p in paths)
        assert {p.relative_to(folder).as_posix(): p.stat().st_size for p in paths} == {n: r['bytes'] for n, r in pre['live'].items()}
    assert min(shutil.disk_usage(d).free for d in ('C:/', 'D:/')) >= 40_000_000_000
    assert a.gate.resolve().is_relative_to(LOCAL)
    gate = json.loads(a.gate.read_text())
    assert gate['status'] == 'GO' and gate['controller_sha256'] == pin(exe)
    if 'collector_sha256' in gate:
        assert gate['collector_sha256'] == pin(__file__)
    output.mkdir(parents=True)
    assert a.launch.resolve().is_relative_to(LOCAL)
    launch = json.loads(a.launch.read_text())
    process = json.loads(subprocess.check_output(['powershell', '-NoProfile', '-Command',
        f'Get-Process -Id {a.pid} | Select-Object Id,Path,@{{n="StartUtc";e={{$_.StartTime.ToUniversalTime().ToString("o")}}}} | ConvertTo-Json'], text=True))
    assert process['Id'] == a.pid and process['Path'].lower() == str(Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield/Starfield.exe')).lower()
    assert process['StartUtc'] > launch['utc']
    command = [str(exe), '--retail-pilot', str(a.pid)]
    config = dict(command=command, utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  synthetic=False, build_sha256=pin(build / 'build.json'),
                  save_preflight_sha256=pin(LOCAL / 'preflight-saves.json'), gate=gate, process=process, steam_launch=launch,
                  source_sha256=pin(__file__), transport_sha256=pin(ROOT / 'research/resource-ui-oracle/receipt_probe.py'))
    write(output / 'config.json', config)
    p = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         stderr=(output / 'stderr.txt').open('xb'), cwd=ROOT,
                         text=True, encoding='utf8')
    incoming = queue.Queue()

    def reader():
        for line in p.stdout:
            incoming.put(line)
        incoming.put(None)

    threading.Thread(target=reader, daemon=True).start()
    session = None
    captures = acks = 0
    stopped = False
    events = (output / 'events.jsonl').open('x', encoding='utf8', newline='\n')
    try:
        while True:
            if not stopped and ((output / 'STOP').exists() or min(shutil.disk_usage(d).free for d in ('C:/', 'D:/')) < 40_000_000_000):
                p.stdin.write('STOP\n')
                p.stdin.flush()
                stopped = True
            try:
                line = incoming.get(timeout=1)
            except queue.Empty:
                continue
            if line is None:
                break
            row = json.loads(line)
            row['received_ns'] = time.perf_counter_ns()
            events.write(json.dumps(row) + '\n')
            events.flush()
            os.fsync(events.fileno())
            if row['kind'] == 'SESSION':
                assert session is None
                session = row
            if row['kind'] != 'SAMPLE':
                continue
            captures += 1
            assert session and row['capture'] == captures
            ack, useful = preserve_sample(output, session, row)
            acks += 1
            # Complete copied data may still have unbound runtime identity.
            if not stopped:
                if useful:
                    stopped = True
                p.stdin.write(f'ACK {captures} STOP\n' if useful else f'ACK {captures}\n')
                p.stdin.flush()
    finally:
        events.close()
    code = p.wait()
    write(output / 'result.json', dict(controller_exit=code, captures=captures, acknowledgements=acks,
          scientific='REQUIRES_INDEPENDENT_IDENTITY_AND_CONTENT_REVIEW', stopped=stopped))
    print(output, code, captures, acks)
    return code


if __name__ == '__main__':
    raise SystemExit(main())
