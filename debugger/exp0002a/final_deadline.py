# SPDX-License-Identifier: GPL-3.0-or-later
"""Single-use CDB deadline/flush guard, version 0.1.4; not a debugger backend.

Reads the explicit PID's identity, executable hash, disk space and bounded CDB
log. Retains that process handle. Writes create-new receipts under the final
experiment root. At the ten-second active deadline, requests one OS debugger
control break if no hit has begun. Never writes DR registers, installs a research
breakpoint, launches a target, retries attachment, detaches or terminates it.
The researcher owns CDB commands and cleanup. See the final-attempt brief.
"""
import argparse
import ctypes as C
from ctypes import wintypes as W
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import time

VERSION = '0.1.4'
ROOT = Path(__file__).resolve().parents[2] / '.local-work/exp0002a-final-software'

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--identity', type=Path, required=True)
    parser.add_argument('--directory', type=Path, required=True)
    args = parser.parse_args()
    directory = args.directory.resolve()
    if not directory.is_relative_to(ROOT) or not directory.is_dir():
        raise ValueError('existing final-experiment directory required')
    identity = json.loads(args.identity.read_text(encoding='utf-8-sig'))
    def record(name, **values):
        with (directory / name).open('x', encoding='utf-8', newline='\n') as f:
            json.dump(dict(version=VERSION, utc=datetime.now(timezone.utc).isoformat(),
                           monotonic=time.monotonic(), **values), f, indent=2)
            f.flush()
            os.fsync(f.fileno())
    kernel = C.WinDLL('kernel32', use_last_error=True)
    kernel.OpenProcess.argtypes = [W.DWORD, W.BOOL, W.DWORD]
    kernel.OpenProcess.restype = W.HANDLE
    kernel.CloseHandle.argtypes = [W.HANDLE]
    kernel.GetProcessTimes.argtypes = [W.HANDLE] + [C.POINTER(W.FILETIME)] * 4
    kernel.QueryFullProcessImageNameW.argtypes = [W.HANDLE, W.DWORD, W.LPWSTR, C.POINTER(W.DWORD)]
    kernel.DebugBreakProcess.argtypes = [W.HANDLE]
    kernel.GetExitCodeProcess.argtypes = [W.HANDLE, C.POINTER(W.DWORD)]
    handle = kernel.OpenProcess(0x43A, False, identity['pid'])
    if not handle:
        raise C.WinError(C.get_last_error())
    try:
        times = [W.FILETIME() for _ in range(4)]
        if not kernel.GetProcessTimes(handle, *[C.byref(t) for t in times]):
            raise C.WinError(C.get_last_error())
        created = times[0].dwLowDateTime | (times[0].dwHighDateTime << 32)
        path = C.create_unicode_buffer(32768)
        length = W.DWORD(len(path))
        if not kernel.QueryFullProcessImageNameW(handle, 0, path, C.byref(length)):
            raise C.WinError(C.get_last_error())
        if created != identity['created_filetime'] or Path(path.value) != Path(identity['path']):
            raise ValueError('target identity mismatch')
        if hashlib.sha256(Path(path.value).read_bytes()).hexdigest() != identity['sha256']:
            raise ValueError('target image hash mismatch')
        record('guard-ready.json', pid=identity['pid'], created_filetime=created)
        setup_deadline = time.monotonic() + 300
        active = None
        hit_started = None
        while True:
            now = time.monotonic()
            if (directory / 'guard.cancel').exists():
                record('guard-ended.json', reason='researcher_cancel')
                return
            logfile = directory / 'cdb.log'
            if logfile.exists() and logfile.stat().st_size > 2_000_000:
                reason = 'output_limit'
                break
            lines = logfile.read_text(errors='replace').splitlines() if logfile.exists() else []
            if 'SOR_HIT_BEGIN' in lines and hit_started is None:
                hit_started = now
            if 'SOR_HIT_END' in lines:
                # The next CDB command closes the log. Give it up to one second
                # to release its handle; never declare scientific completeness here.
                for _ in range(20):
                    try:
                        with logfile.open('r+b') as f:
                            os.fsync(f.fileno())
                        break
                    except PermissionError:
                        time.sleep(0.05)
                else:
                    raise RuntimeError('capture log could not be durably flushed')
                record('capture-flushed.json', status='OUTPUT_FLUSHED_PENDING_VALIDATION',
                       log_sha256=hashlib.sha256(logfile.read_bytes()).hexdigest())
                return
            if active is None and 'SOR_CAPTURE_ACTIVE' in lines:
                active = now
                record('active.json', deadline_monotonic=active + 10)
            if min(shutil.disk_usage(v).free for v in ['C:/', 'D:/']) < 40_000_000_000:
                reason = 'low_disk_stop'
                break
            exit_code = W.DWORD()
            if not kernel.GetExitCodeProcess(handle, C.byref(exit_code)):
                raise C.WinError(C.get_last_error())
            if exit_code.value != 259:
                record('guard-ended.json', reason='target_exit', exit_code=exit_code.value)
                return
            if hit_started is not None and now > hit_started + 5:
                record('guard-ended.json', reason='hit_output_incomplete', complete=False)
                return
            if hit_started is None and active is not None and now >= active + 10:
                reason = 'capture_deadline'
                break
            if active is None and now >= setup_deadline:
                reason = 'setup_deadline'
                break
            time.sleep(0.02)
        ok = bool(kernel.DebugBreakProcess(handle))
        record('guard-ended.json', reason=reason, control_break_requested=True,
               control_break_succeeded=ok, winerror=0 if ok else C.get_last_error())
    finally:
        kernel.CloseHandle(handle)

if __name__ == '__main__':
    main()
