# SPDX-License-Identifier: GPL-3.0-or-later
"""Original startup causal/negative controls, approved013 versus candidate014.

Reads explicit adapter/fixture inputs, hashes them and queries C:/D: free space.
Writes NEW ignored receipts/streams/fixture evidence only. Launches disposable
Python targets and event_fixture.exe, never Starfield. Retail tests deliberately
reject wrong identity; never spoof game guards. Fixture tests use its genuine
hash/plan, verify detach/code independently, then release for normal exit.
No dependencies/downloads. Run from repo root with installed 64-bit Python.
"""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
GAME_SHA = '7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28'


def sha(path):
    with Path(path).open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def guard():
    free = {d: shutil.disk_usage(d).free for d in ('C:/', 'D:/')}
    if min(free.values()) < 40_000_000_000:
        raise OSError('disk guard')
    return free


def wait(path, processes):
    until = time.monotonic() + 30
    while not path.exists():
        if any(p.poll() is not None for p in processes) or time.monotonic() > until:
            raise RuntimeError('readiness timeout/exit: ' + str(path))
        time.sleep(.03)


def run(exe, out, fixture, version):
    guard()
    out.mkdir(exist_ok=False)
    results = []
    targets = []
    try:
        for permission in ('ordinary', 'deny-open'):
            p = subprocess.Popen([sys.executable, '-B', str(Path(__file__).with_name('disposable_target.py')),
                                  *(['deny-open'] if permission == 'deny-open' else [])],
                                 stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                 text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            targets.append(p)
            ready = json.loads(p.stdout.readline())
            assert ready['pid'] == p.pid
            for existing in (False, True):
                case = out / (permission + ('-existing' if existing else '-absent'))
                case.mkdir()
                root = case / 'output'
                if existing:
                    root.mkdir()
                command = [str(exe), '--reviewed-retail', str(p.pid), str(root), GAME_SHA, '--center-only']
                result = subprocess.run(command, cwd=ROOT, capture_output=True, timeout=15,
                                        creationflags=subprocess.CREATE_NO_WINDOW)
                (case / 'stdout.txt').write_bytes(result.stdout)
                (case / 'stderr.txt').write_bytes(result.stderr)
                expected = 0xC0000409 if version == '0.1.3' and not existing else 1
                assert result.returncode & 0xffffffff == expected
                primary = b'open:5' if permission == 'deny-open' else b'retail_identity:'
                assert primary in result.stderr if expected == 1 else not result.stderr
                assert p.poll() is None and not (root / 'evidence').exists()
                results.append({'case': case.name, 'args': command, 'exit': result.returncode,
                                'status_hex': hex(result.returncode & 0xffffffff),
                                'stderr': result.stderr.decode(), 'root_exists': root.exists(),
                                'disposable_target_alive': True})
        ordinary = targets[0]
        cases = [
            ('missing-args', [], 2), ('version', ['--version'], 0),
            ('unknown-mode', ['--unknown', str(ordinary.pid)], 2),
            ('invalid-pid', ['--reviewed-retail', 'nonsense'], 1),
            ('overflow-pid', ['--reviewed-retail', '18446744073709551616'], 1),
            ('pid-trailing', ['--reviewed-retail', str(ordinary.pid) + 'junk'], 1),
            ('pid-negative', ['--reviewed-retail', '-1'], 1),
            ('pid-zero', ['--reviewed-retail', '0'], 1),
            ('relative-output', ['--reviewed-retail', str(ordinary.pid), 'relative-output'], 1),
        ]
        for name, args, expected in cases:
            case = out / name
            case.mkdir()
            root = case / 'absent-output'
            if len(args) == 2:
                args += [str(root), GAME_SHA, '--center-only']
            elif name == 'relative-output':
                args += [GAME_SHA, '--center-only']
            command = [str(exe), *args]
            result = subprocess.run(command, cwd=case, capture_output=True, timeout=15,
                                    creationflags=subprocess.CREATE_NO_WINDOW)
            (case / 'stdout.txt').write_bytes(result.stdout)
            (case / 'stderr.txt').write_bytes(result.stderr)
            if version == '0.1.3' and expected == 1:
                expected = 0xC0000409
            assert result.returncode & 0xffffffff == expected, (name, result.returncode, result.stderr)
            assert not root.exists()
            results.append({'case': name, 'args': command, 'cwd': str(case), 'exit': result.returncode,
                            'status_hex': hex(result.returncode & 0xffffffff), 'stderr': result.stderr.decode()})
        # Native Start-Process launch shape, redirected hidden process, changed
        # cwd and a space-containing output path passed with explicit quotes.
        case = out / 'powershell-hidden-redirected'
        case.mkdir()
        root = case / 'space parent' / 'absent-output'
        ps = ("$ErrorActionPreference='Stop'; "
              f"$p=Start-Process -FilePath '{exe}' -ArgumentList @('--reviewed-retail','{ordinary.pid}','\"{root}\"','{GAME_SHA}','--center-only') "
              f"-WorkingDirectory '{case}' -WindowStyle Hidden -Wait -PassThru -RedirectStandardOutput '{case / 'stdout.txt'}' -RedirectStandardError '{case / 'stderr.txt'}'; "
              "$p.WaitForExit();Write-Output $p.ExitCode")
        result = subprocess.run(['powershell', '-NoProfile', '-Command', ps], capture_output=True, timeout=20,
                                env={k.upper(): v for k, v in os.environ.items()})
        expected = 0xC0000409 if version == '0.1.3' else 1
        (case / "launcher.stdout.txt").write_bytes(result.stdout)
        (case / "launcher.stderr.txt").write_bytes(result.stderr)
        code = int(result.stdout.strip())
        assert code & 0xffffffff == expected
        results.append({'case': case.name, 'command': ps, 'exit': code,
                        'status_hex': hex(code & 0xffffffff), 'stderr': (case / 'stderr.txt').read_text()})
        case = out / 'inherited-streams'
        case.mkdir()
        command = [str(exe), '--reviewed-retail', str(ordinary.pid),
                   str(case / 'absent-output'), GAME_SHA, '--center-only']
        result = subprocess.run(command, cwd=case, timeout=15)
        expected = 0xC0000409 if version == '0.1.3' else 1
        assert result.returncode & 0xffffffff == expected
        results.append({'case': case.name, 'args': command, 'exit': result.returncode,
                        'status_hex': hex(result.returncode & 0xffffffff),
                        'streams': 'inherited; no adapter-specific redirection', 'creationflags': 0})
        for failure in ('bad-fixture-hash', 'output-is-file'):
            case = out / failure
            case.mkdir()
            target_dir = case / 'target'
            target_dir.mkdir()
            root = case / 'output'
            if failure == 'output-is-file':
                root.write_bytes(b'PROTECTED_DISPOSABLE_SENTINEL\n')
            with (case / 'fixture.log').open('wb') as fl:
                target = subprocess.Popen([str(fixture), str(target_dir), 'zero'], stdout=fl, stderr=fl)
                try:
                    wait(target_dir / 'fixture.plan', [target])
                    command = [str(exe), '--fixture', str(target.pid), str(root),
                               '0' * 64 if failure == 'bad-fixture-hash' else sha(fixture),
                               str(target_dir / 'fixture.plan')]
                    result = subprocess.run(command, capture_output=True, timeout=15)
                    (case / 'stdout.txt').write_bytes(result.stdout)
                    (case / 'stderr.txt').write_bytes(result.stderr)
                    expected = 0xC0000409 if version == '0.1.3' else 1
                    assert result.returncode & 0xffffffff == expected
                    if version == '0.1.4':
                        assert (b'fixture_identity' if failure == 'bad-fixture-hash' else b'output_create') in result.stderr
                    if failure == 'output-is-file':
                        assert root.read_bytes() == b'PROTECTED_DISPOSABLE_SENTINEL\n'
                    results.append({'case': failure, 'args': command, 'exit': result.returncode,
                                    'status_hex': hex(result.returncode & 0xffffffff),
                                    'stderr': result.stderr.decode(), 'target_alive': target.poll() is None})
                finally:
                    (target_dir / 'GO').touch()
                    (target_dir / 'RELEASE').touch()
                    target.wait(timeout=15)
                    assert target.returncode == 0
        for inject_timing_failure in (False, True):
            case = out / ('fixture-fresh-root' if not inject_timing_failure else 'fixture-timing-failure')
            case.mkdir()
            target_dir = case / 'target'
            target_dir.mkdir()
            root = case / 'fresh-output'
            with (case / 'fixture.log').open('wb') as fl, (case / 'adapter.log').open('wb') as al:
                target = subprocess.Popen([str(fixture), str(target_dir), 'zero'], stdout=fl, stderr=fl)
                adapter = None
                try:
                    wait(target_dir / 'fixture.plan', [target])
                    command = [str(exe), '--fixture', str(target.pid), str(root), sha(fixture), str(target_dir / 'fixture.plan')]
                    adapter = subprocess.Popen(command, stdout=al, stderr=al)
                    wait(root / 'READY', [target, adapter])
                    (target_dir / 'GO').touch()
                    wait(target_dir / 'counts.json', [target, adapter])
                    if inject_timing_failure:
                        (root / 'timing.json').mkdir()
                    (root / 'STOP').touch()
                    adapter.wait(timeout=30)
                    expected = (0xC0000409 if version == '0.1.3' else 1) if inject_timing_failure else 0
                    assert adapter.returncode & 0xffffffff == expected
                    sys.path.insert(0, str(ROOT / 'debugger/exp0002a'))
                    from process_read import ProcessRead
                    sys.path.insert(0, str(ROOT / 'debugger/event-oracle'))
                    from materialize_epochs import decode
                    rows, wal = decode(root / 'evidence/epochs.wal')
                    base = int(next(row['base'] for row in rows if row['kind'] == 'ready'), 16)
                    reader = ProcessRead(target.pid)
                    try:
                        assert reader.alive() and not reader.debugged()
                        for line in (target_dir / 'fixture.plan').read_text().splitlines():
                            _, rva, original = line.split()
                            expected_bytes = bytes.fromhex(original)
                            assert reader.read(base + int(rva, 16), len(expected_bytes)) == expected_bytes
                    finally:
                        reader.close()
                    (target_dir / 'RELEASE').touch()
                    target.wait(timeout=15)
                    assert target.returncode == 0
                    results.append({'case': case.name, 'args': command, 'exit': adapter.returncode,
                                    'status_hex': hex(adapter.returncode & 0xffffffff), 'fixture_exit': target.returncode,
                                    'code_restore_detach_independent': True, 'wal': wal})
                finally:
                    if adapter and adapter.poll() is None:
                        (root / 'STOP').touch()
                        adapter.wait(timeout=30)
                    (target_dir / 'GO').touch()
                    (target_dir / 'RELEASE').touch()
                    target.wait(timeout=15)
    finally:
        (out / "partial-results.json").write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
        for p in targets:
            stdout, stderr = p.communicate('RELEASE\n', timeout=15)
            assert p.returncode == 0 and 'NORMAL_EXIT_DACL_RESTORED' in stdout, stderr
    report = {'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'version': version,
              'adapter_sha256': sha(exe), 'fixture_sha256': sha(fixture), 'cases': results,
              'all_targets_normal_exit': True, 'guard_final': guard(), 'no_game_access': True}
    (out / 'results.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(version, len(results), 'startup controls PASS', out)


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--adapter', type=Path, required=True)
    ap.add_argument('--fixture', type=Path, required=True)
    ap.add_argument('--version', choices=('0.1.3', '0.1.4'), required=True)
    ap.add_argument('--output', type=Path, required=True)
    a = ap.parse_args()
    run(a.adapter.resolve(), a.output.resolve(), a.fixture.resolve(), a.version)
