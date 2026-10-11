# SPDX-License-Identifier: GPL-3.0-or-later
"""Read-only operational checks; never attach, stop, write or control a target.

offline: hashes approved package/tool/game/protected saves and queries disk space.
process: future authorized live read pre/postflight, using original project reader
and PowerShell module inventory. Writes one exclusive JSON receipt; stdlib only.
Run with installed 64-bit Python from repository root. No elevation/retry implied.
"""
import argparse
import ctypes as C
from ctypes import wintypes as W
import datetime
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[2]
GAME = Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield/Starfield.exe')
GAME_SHA = '7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28'
TOOL = ROOT / '.local-work/event-instrumentation/latency-candidate-013-02/adapter.exe'
TOOL_SHA = 'b0751a86655b0a4759932f0b90cfcd7aeb9314f9a03b5a52d4522ba5bd1c1eb3'
ZIP = ROOT / '.local-work/event-latency/review-01/SorEventOracle-0.1.3.zip'
ZIP_SHA = '2e29c452b566b992bc504cf0d6e2c4971675aabd47ad4d3408b455268c121efc'
SITES = {
    'center_entry': (0xF4AB80, '702240fe34296bf5b3845f8d877438ffc5a2343beac2811bf67307a6de0fc7cc'),
    'center_exit': (0xF4AC44, '75395a678542d156d2480f475573ff5c81c9459684c7e5eabe2e2f9a9df85e6d'),
}


def sha(path):
    with Path(path).open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def require(value, message):
    if not value:
        raise ValueError(message)


def space():
    free = {d: shutil.disk_usage(d).free for d in ('C:/', 'D:/')}
    require(min(free.values()) >= 40_000_000_000, '40 GB caller-available guard')
    return free


def offline(out):
    out['free_bytes'] = space()
    out['hashes'] = {}
    pinned = {str(GAME): GAME_SHA, str(TOOL): TOOL_SHA, str(ZIP): ZIP_SHA}
    saved = json.loads((ROOT / '.local-work/event-latency/input-integrity-after.json').read_text())
    pinned.update(saved['protected_saves'])
    pinned.update({str(ROOT / 'docs/experiments/engine-oracle' / name): value
                   for name, value in saved['frozen'].items()})
    for name, expected in pinned.items():
        actual = sha(name)
        out['hashes'][name] = actual
        require(actual == expected, 'pinned hash mismatch: ' + name)
    saves = Path('C:/Users/User/Documents/My Games/Starfield/Saves')
    out['save_inventory'] = [{'name': p.name, 'bytes': p.stat().st_size,
                              'mtime_ns': p.stat().st_mtime_ns}
                             for p in sorted(saves.iterdir()) if p.is_file()]
    content = Path('C:/Users/User/AppData/Local/Starfield/Plugins.txt')
    out['content_list'] = {'path': str(content), 'sha256': sha(content),
                           'text': content.read_text(encoding='utf-8-sig')}
    out['scope'] = 'OFFLINE_INPUT_INTEGRITY_ONLY'


def process(out, pid, previous):
    # Only enumerate the requested game's modules; no debugger APIs are used.
    script = ("$ErrorActionPreference='Stop'; "
              "$games=@(Get-Process Starfield -ErrorAction SilentlyContinue); "
              "if($games.Count -ne 1){throw 'Expected exactly one Starfield process'}; "
              f"$p=Get-Process -Id {pid}; "
              "if($games[0].Id -ne $p.Id){throw 'Wrong PID'}; "
              "ConvertTo-Json -Depth 4 -InputObject @($p.Modules | ForEach-Object { "
              "@{path=$_.FileName;base=$_.BaseAddress.ToInt64()} })")
    spec = importlib.util.spec_from_file_location('process_read', ROOT / 'debugger/exp0002a/process_read.py')
    reader = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(reader)
    p = reader.ProcessRead(pid)
    try:
        kernel = reader.K
        kernel.GetProcessTimes.argtypes = [W.HANDLE] + [C.POINTER(W.FILETIME)] * 4
        kernel.GetProcessTimes.restype = W.BOOL
        times = [W.FILETIME() for _ in range(4)]
        if not kernel.GetProcessTimes(p.handle, *(C.byref(t) for t in times)):
            raise C.WinError(C.get_last_error())
        token = (times[0].dwHighDateTime << 32) | times[0].dwLowDateTime
        out.update(pid=pid, creation_filetime=token, path=p.path(), alive=p.alive(), debugger_present=p.debugged())
        require(out['alive'], 'Target exited; no live restoration check')
        require(Path(out['path']).resolve() == GAME.resolve(), 'Wrong executable path')
        require(not out['debugger_present'], 'Debugger present')
        require(sha(GAME) == GAME_SHA, 'Game changed')
        if previous:
            old = json.loads(previous.read_text())
            require(old.get('status') == 'PASS' and old.get('mode') == 'pre', 'Invalid preflight receipt')
            require(old['pid'] == pid and old['creation_filetime'] == token, 'PID reuse / different process')
        modules = json.loads(subprocess.check_output(['powershell', '-NoProfile', '-Command', script], text=True))
        out['modules'] = modules
        blocked = [m for m in modules if Path(m['path']).name.lower().startswith(('sfse', 'sorbeaconobserver'))
                   or '/sfse/plugins/' in m['path'].replace('\\', '/').lower()]
        require(not blocked, 'SFSE/observer module present; stop for configuration review')
        main = [m for m in modules if Path(m['path']).resolve() == GAME.resolve()]
        require(len(main) == 1, 'Ambiguous main module')
        out['base'] = main[0]['base']
        if previous:
            require(old['base'] == out['base'], 'Main module changed')
        out['sites'] = {}
        for name, (rva, expected) in SITES.items():
            data = p.read(out['base'] + rva, 32)
            actual = hashlib.sha256(data).hexdigest()
            out['sites'][name] = {'rva': hex(rva), 'va': hex(out['base'] + rva), 'bytes_hex': data.hex(), 'sha256': actual}
            require(actual == expected, 'Original 32-byte window mismatch: ' + name)
        # Retain the handle across enumeration and reads; recheck survival.
        require(p.alive(), 'Target exited during check')
        out['free_bytes'] = space()
    finally:
        p.close()


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('mode', choices=('offline', 'pre', 'post'))
    ap.add_argument('--pid', type=int)
    ap.add_argument('--pre', type=Path)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    require(not args.output.exists() and args.output.parent.is_dir(), 'NEW receipt in existing parent required')
    receipt = {'mode': args.mode, 'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'status': 'FAIL'}
    try:
        if args.mode == 'offline':
            offline(receipt)
        else:
            require(args.pid is not None and args.pid > 0, '--pid required')
            require(args.mode != 'post' or args.pre is not None, '--pre required for postflight')
            process(receipt, args.pid, args.pre if args.mode == 'post' else None)
        receipt['status'] = 'PASS'
    except Exception as error:
        receipt['error'] = str(error)
    with args.output.open('x', encoding='utf-8', newline='\n') as f:
        json.dump(receipt, f, indent=2)
        f.write('\n')
    print(receipt['status'], args.output)
    raise SystemExit(0 if receipt['status'] == 'PASS' else 1)
