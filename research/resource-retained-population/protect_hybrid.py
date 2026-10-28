# SPDX-License-Identifier: GPL-3.0-or-later
"""Offline full active archive/save/content preservation for D5N.

Reads authenticated existing scientific archives, protected saves/backups,
installed content/configuration and Git identity. Writes a fresh ignored
receipt directory including a scratch restoration copy; never alters inputs.
Uses the existing project-owned full_preservation method under SOR-P-0002.
No target, network, installs, analysis or Git mutation. Both disk floors apply.
"""
import json
from pathlib import Path
import shutil
import subprocess
import sys
from prepare_native import full_preservation, write, ROOT, pin


def main():
    out = Path(sys.argv[1]).resolve()
    assert out.is_relative_to(ROOT/'.local-work/d5n')
    assert min(shutil.disk_usage(d).free for d in ('C:/', 'D:/')) >= 40_000_000_000
    assert subprocess.check_output(['powershell', '-NoProfile', '-Command',
        '@(Get-Process Starfield -ErrorAction SilentlyContinue).Count'], text=True).strip() == '0'
    out.mkdir(parents=True, exist_ok=False)
    result = full_preservation(out)
    result['free_bytes'] = {d: shutil.disk_usage(d).free for d in ('C:/', 'D:/')}
    result['head'] = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
    result['index_sha256'] = pin(ROOT/'.git/index')
    write(out/'protection.json', result)
    print(json.dumps(dict(path=str(out/'protection.json'), free_bytes=result['free_bytes'], protected=len(result['protected_live']))))


if __name__ == '__main__':
    main()
