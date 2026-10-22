# SPDX-License-Identifier: GPL-3.0-or-later
"""Pre/postflight local save audit and independent backup rehearsal.

Reads the live save tree, known Save52 baseline, protected inputs and user-confirmed
Cloud-disabled state. Preflight copies every live file to a fresh ignored backup,
hashes source/destination and rehearses restore to a separate scratch file.
Postflight hashes both trees and reports changes; never restores or deletes.
No game, configuration, sync settings, network or Git mutation.
"""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[2]
LOCAL = ROOT / '.local-work/resource-oracle-retail'
SAVES = Path('C:/Users/User/Documents/My Games/Starfield/Saves')
EXPECTED = '6b4a10084c7e752c31fd2de121a00850aaa2bf1decd700b437d7dccfcdbc82e8'


def pin(p):
    with Path(p).open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def inventory(folder):
    result = {}
    for p in sorted(folder.rglob('*')):
        assert not p.lstat().st_file_attributes & 0x400, p
        if p.is_file():
            result[p.relative_to(folder).as_posix()] = dict(bytes=p.stat().st_size, sha256=pin(p))
    return result


def write(p, value):
    import os
    with p.open('x', encoding='utf8', newline='\n') as f:
        json.dump(value, f, indent=2)
        f.write('\n')
        f.flush()
        os.fsync(f.fileno())


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('phase', choices=('pre', 'post'))
    ap.add_argument('--name', required=True)
    ap.add_argument('--cloud-disabled-confirmed', action='store_true')
    a = ap.parse_args()
    assert all(c in 'abcdefghijklmnopqrstuvwxyz0123456789-' for c in a.name)
    out = LOCAL / (a.name + '.json')
    assert not out.exists()
    process_count = subprocess.check_output(['powershell', '-NoProfile', '-Command',
        "@(Get-Process Starfield -ErrorAction SilentlyContinue).Count"], text=True).strip()
    assert process_count == '0', 'Audit only before launch or after target exit'
    space = {d: shutil.disk_usage(d).free for d in ('C:/', 'D:/')}
    assert min(space.values()) >= 40_000_000_000
    live = inventory(SAVES)
    backup = LOCAL / 'protected-saves'
    value = dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), phase=a.phase,
                 live_path=str(SAVES), backup_path=str(backup), live=live, space=space)
    if a.phase == 'pre':
        assert a.cloud_disabled_confirmed, 'Explicit operator confirmation required'
        assert not backup.exists()
        assert any(n.startswith('Save52_') and r['sha256'] == EXPECTED for n, r in live.items())
        total = sum(r['bytes'] for r in live.values())
        assert space['D:/'] - total >= 40_000_000_000
        shutil.copytree(SAVES, backup)
        copied = inventory(backup)
        assert copied == live and inventory(SAVES) == live
        # Practical exact-byte restore rehearsal outside all game write/sync paths.
        save52 = next(n for n, r in live.items() if n.startswith('Save52_') and r['sha256'] == EXPECTED)
        rehearsal = LOCAL / 'restore-rehearsal.sfs'
        shutil.copyfile(backup / save52, rehearsal)
        assert pin(rehearsal) == EXPECTED
        value.update(backup=copied, cloud_disabled='operator-confirmed 2026-10-22',
                     restore_rehearsal=dict(path=str(rehearsal), sha256=pin(rehearsal)),
                     expected_writes='Live Saves including autosave/quicksave/exit saves; Cloud held disabled',
                     restore_contract='After process exit compare inventories, archive new/changed files before any replacement; restore only named baseline files from independent backup and verify hash. No automatic restore in this script.')
    else:
        before = json.loads((LOCAL / 'preflight-saves.json').read_text())
        copied = inventory(backup)
        value.update(backup=copied, backup_unchanged=copied == before['backup'],
                     changed=[n for n in live if n in before['live'] and live[n] != before['live'][n]],
                     new=sorted(set(live) - set(before['live'])), missing=sorted(set(before['live']) - set(live)))
        assert copied == before['backup'], 'Protected backup changed: STOP, no restore'
    write(out, value)
    print(out, 'files', len(live), 'bytes', sum(r['bytes'] for r in live.values()),
          'deltas', {k: value[k] for k in ('changed', 'new', 'missing') if k in value})


if __name__ == '__main__':
    main()
