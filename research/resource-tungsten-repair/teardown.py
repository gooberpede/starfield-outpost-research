# SPDX-License-Identifier: GPL-3.0-or-later
"""Real Windows D4B terminal-race fixture qualification; stdlib, owned transport.

Reads a pinned build and executes only its disposable synthetic fixture. Writes
fresh ignored receipts/events. No retail, saves, configuration, installs or Git
writes. API failure cases intentionally call invalid handle/owner APIs before
testing cleanup with the still-owned real process/event. Never simulates events.
"""
import argparse
import ctypes
from ctypes import wintypes
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'research/resource-tungsten-acquisition'))
from admission import Tracker
from qualify import preserve, independent
from collect import pin, write


def target_absent(pid):
    """Read only the synthetic PID's process state after debugger disposal."""
    kernel = ctypes.WinDLL('kernel32', use_last_error=True)
    kernel.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
    kernel.OpenProcess.restype = wintypes.HANDLE
    kernel.GetExitCodeProcess.argtypes = [wintypes.HANDLE, ctypes.POINTER(wintypes.DWORD)]
    kernel.CloseHandle.argtypes = [wintypes.HANDLE]
    handle = kernel.OpenProcess(0x1000, False, pid)
    if not handle:
        return ctypes.get_last_error() == 87
    try:
        code = wintypes.DWORD()
        assert kernel.GetExitCodeProcess(handle, ctypes.byref(code))
        return code.value != 259
    finally:
        kernel.CloseHandle(handle)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--build', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--legacy', action='store_true')
    args = ap.parse_args()
    build, out = args.build.resolve(), args.output.resolve()
    assert build.is_relative_to(ROOT / '.local-work') and out.is_relative_to(ROOT / '.local-work')
    if not args.legacy:
        manifest = json.loads((build / 'build.json').read_text())
        assert manifest['exit_code'] == 0
        assert all(pin(p) == h for p,h in manifest['files'].items())
    else:
        assert pin(build/'sor-d4a-fixture-controller.exe') == pin(ROOT/'.local-work/resource-tungsten-acquisition/build08/sor-d4a-fixture-controller.exe')
        assert pin(build/'sor-d4a-fixture.exe') == pin(ROOT/'.local-work/resource-tungsten-acquisition/d4b-build03/sor-d4a-fixture.exe')
    out.mkdir(parents=True, exist_ok=False)
    modes = ('stop-many',) if args.legacy else (
        'stop-threads', 'stop-many', 'pending-stop', 'terminate-failure', 'continue-failure',
        'duplicate-continue', 'crash-before', 'crash-after', 'no-hit',
        'ackfail', 'partial-ack', 'dropped-ack')
    results = []
    for mode in modes:
        folder = out / mode
        folder.mkdir()
        tracker, rows, useful, session = Tracker(), [], [], None
        command = [str(build / 'sor-d4a-fixture-controller.exe'), '--synthetic-fixture',
                   pin(build / 'sor-d4a-fixture.exe'), mode]
        with subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, text=True) as process:
            for line in process.stdout:
                row = json.loads(line)
                row['synthetic'] = True
                rows.append(row)
                if row['kind'] == 'SESSION':
                    session = row
                if row['kind'] == 'SAMPLE':
                    preserve(folder, session, row)
                    yes = tracker.feed(row)
                    if yes:
                        useful.append(row['capture'])
                    response = f'ACK {row["capture"]}'
                    if yes and mode not in ('pending-stop', 'crash-after'):
                        response += ' STOP'
                    if mode in ('ackfail', 'partial-ack'):
                        response = 'REJECT' if mode == 'ackfail' else 'ACK'
                    if mode == 'dropped-ack':
                        process.stdin.close()
                    else:
                        process.stdin.write(response + '\n')
                        process.stdin.flush()
                else:
                    tracker.feed(row)
                if mode == 'pending-stop' and row['kind'] == 'THREAD_END' and useful:
                    process.stdin.write('STOP\n')
                    process.stdin.flush()
            code = process.wait(timeout=15)
            stderr = process.stderr.read()
        write(folder / 'events.json', rows)
        write(folder / 'stderr.json', dict(text=stderr))
        # Reopen receipts after target/controller exit, including deliberate errors.
        receipts = list(folder.glob('capture-*.bin'))
        for path in receipts:
            independent(path)
        errors = []
        expected = 2 if mode in ('terminate-failure', 'continue-failure') else 0
        if code != expected:
            errors.append(f'controller exit {code} != {expected}')
        if args.legacy:
            ack = next(i for i,r in enumerate(rows) if r['kind']=='ACK_ACCEPTED' and r['capture']==useful[-1])
            if not any(r['kind']=='PHASE' for r in rows[ack+1:]):
                errors.append('unsafe late rearm not reproduced')
        else:
            stops = [i for i,r in enumerate(rows) if r['kind'] == 'STOP_COMMITTED']
            if len(stops) != 1:
                errors.append('nonmonotonic STOP')
            elif any(r['kind'] in ('SAMPLE', 'PHASE', 'STARTUP_ARMED', 'THREAD_BEGIN', 'RESUME_VERIFIED') for r in rows[stops[0]+1:]):
                errors.append('new observer obligation after STOP')
            if expected == 2:
                cleanup = [r for r in rows if r['kind'] == 'FAILURE_CLEANUP']
                if len(cleanup) != 1 or not all(cleanup[0][k] for k in ('termination_requested', 'continued', 'exit_observed')):
                    errors.append('failure drain incomplete')
            elif not any(r['kind'] == 'EXIT' for r in rows):
                errors.append('missing real EXIT_PROCESS')
            else:
                target_exit = next(r['code'] for r in rows if r['kind']=='EXIT')
                expected_exit = (0xe0c1e000 if mode=='crash-before' else
                                 0xe0c1e001 if mode=='crash-after' else
                                 0 if mode=='no-hit' else 0xc1d0 if mode=='pending-stop' else 0xc1c0)
                if target_exit != expected_exit:
                    errors.append('unexpected target exit code')
            if mode in ('stop-threads', 'duplicate-continue') and sum(r['kind'] == 'TERMINAL_EVENT' and r['event'] == 4 for r in rows) < 3:
                errors.append('multiple actual terminal thread exits not exercised')
            if mode == 'duplicate-continue' and not any(r['kind'] == 'DUPLICATE_CONTINUE_REFUSED' for r in rows):
                errors.append('duplicate API call not tested')
        absent = target_absent(session['pid'])
        if not absent:
            errors.append('synthetic target remains active')
        result = dict(mode=mode, controller_exit=code, useful=useful, target_absent=absent,
                      historical_api_error_reproduced='phase context win32=31' in stderr,
                      durable_receipts=len(receipts), errors=errors,
                      events_sha256=pin(folder / 'events.json'))
        results.append(result)
        print(mode, code, len(receipts), errors, flush=True)
    write(out / 'summary.json', dict(cases=results, passed=all(not r['errors'] for r in results)))
    assert all(not r['errors'] for r in results)


if __name__ == '__main__':
    main()
