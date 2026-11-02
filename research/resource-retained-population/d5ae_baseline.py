# SPDX-License-Identifier: GPL-3.0-or-later
"""Freeze D5AE offline input identities and available space.

SOR-P-0002: adapted from d5ad_baseline.py. Reads installed EXE/ESM/PlanetData, existing Ghidra database pins, the protected
Save52 research copy, historical session/ACK files, Git HEAD/index and owned
methods. Writes one exclusive ignored JSON receipt; stdlib only. No game,
database, original-save, configuration, network or Git mutation. SOR-P-0002:
uses the existing D5X database roster and Carinae save policy as data inputs.
"""
import ctypes
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]


def sha(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        while block := stream.read(8 * 1024 * 1024):
            digest.update(block)
    return digest.hexdigest()


def guard():
    result = {}
    for drive in ('C:/', 'D:/'):
        free = ctypes.c_ulonglong()
        if not ctypes.windll.kernel32.GetDiskFreeSpaceExW(
                ctypes.c_wchar_p(drive), ctypes.byref(free), None, None):
            raise OSError('Free-space query failed')
        if free.value < 40_000_000_000:
            raise RuntimeError('Free-space floor violated')
        result[drive] = free.value
    return result


def main():
    if not __debug__ or sys.flags.optimize:
        raise RuntimeError('Invoke installed Python with -E -B')
    out = ROOT / '.local-work/d5ae' / sys.argv[1]
    if out.exists() or not out.resolve().is_relative_to(ROOT / '.local-work/d5ae'):
        raise ValueError('Fresh local receipt required')
    free = guard()
    identity = ROOT / '.local-work/d5x/identity05/identity.json'
    database = json.loads(identity.read_bytes())['database']
    pins = dict(database)
    install = Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield')
    pins.update({str(install / name): value for name, value in {
        'Starfield.exe': '7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28',
        'Data/Starfield.esm': '1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7',
        'Data/Starfield - PlanetData.ba2': '2fb1fff5d8fc074718bf05022c099f3c87ef70e00050229b368ae7d680fbe5d5',
    }.items()})
    policy = ROOT / 'research/resource-carinae-source-context/save_policy.json'
    saves = json.loads(policy.read_bytes())['designated']
    name = next(n for n in saves if n.startswith('Save52_'))
    save = ROOT / '.local-work/savegames' / name
    if save.stat().st_size != saves[name]['bytes']:
        raise ValueError('Save52 size mismatch')
    pins[str(save)] = saves[name]['sha256']
    b2 = ROOT / '.local-work/d5x/live/session-5ed302aea9da7dc2261163b3dd1816e670a3c2f39891f1ec8d20094afa72b3a1'
    pins[str(b2 / 'events.bin')] = '4a8feb68f667f417967a0cd4a332cefde768658d254ead8d555b3e5f44515218'
    rows = {}
    for name, expected in pins.items():
        p = Path(name)
        actual = sha(p)
        if actual != expected:
            raise ValueError('Pinned input mismatch: ' + name)
        rows[name] = dict(sha256=actual, bytes=p.stat().st_size)
    notes = ROOT / '.local-work/d5ab/B2-APPROVED-002-notes'
    for p in sorted(notes.glob('*.json')):
        rows[str(p)] = dict(sha256=sha(p), bytes=p.stat().st_size)
    git = lambda *args: subprocess.check_output(['git', *args], cwd=ROOT).decode()
    result = dict(head=git('rev-parse', 'HEAD').strip(),
                  status=git('status', '--short'), index_sha256=sha(ROOT / '.git/index'),
                  inputs=rows, free=free, save_copy=str(save),
                  interpreter=dict(path=sys.executable, version=sys.version, sha256=sha(sys.executable)),
                  brief_sha256=sha(ROOT / 'docs/implementation-briefs/CODEX_BRIEF_SOR_RG2_D5AE_GC10_construction_winner_scheduling.md'),
                  script_sha256=sha(__file__), policy_sha256=sha(policy),
                  identity_roster_sha256=sha(identity),
                  scope='Offline identity checks; no complete active-save audit or live operation')
    out.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8', newline='\n')
    print(json.dumps(dict(head=result['head'], inputs=len(rows), free=free, save_sha256=sha(save))))


if __name__ == '__main__':
    main()
