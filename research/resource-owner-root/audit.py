# SPDX-License-Identifier: GPL-3.0-or-later
"""Read protected inputs; write exclusive local integrity receipts.

Uses the owned D4A protection policy and Python stdlib. Hashes prior corpora,
predictions and captures without interpreting their answer payloads. No target,
save, configuration, database, network or Git writes. Run before and after work.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / '.local-work/resource-owner-root'
sys.path.insert(0, str(ROOT / 'research/resource-tungsten-acquisition'))
import protection


def pin(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf8', newline='\n') as stream:
        json.dump(value, stream, indent=2, allow_nan=False)
        stream.write('\n')


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('phase', choices=['before', 'after'])
    ap.add_argument('--label')
    args = ap.parse_args()
    label = args.label or args.phase
    assert label and all(c in 'abcdefghijklmnopqrstuvwxyz0123456789-' for c in label)
    assert min(shutil.disk_usage(d).free for d in ('C:/', 'D:/')) >= 40_000_000_000
    assert subprocess.check_output(['powershell', '-NoProfile', '-Command',
        '@(Get-Process Starfield -ErrorAction SilentlyContinue).Count'], text=True).strip() == '0'
    protected = protection.audit()
    write(OUT / f'protected-{label}.json', protected)
    assert not protected['changes']
    roots = ('resource-standalone', 'resource-save52', 'resource-save52-d3',
             'resource-tungsten-acquisition', 'resource-tungsten-repair')
    paths = [p for name in roots for p in (ROOT / '.local-work' / name).rglob('*') if p.is_file()]
    baseline = json.loads((ROOT / '.local-work/resource-tungsten-repair/baseline.json').read_text())
    for path, expected in baseline['pins'].items():
        assert pin(path) == expected, path
    paths += [Path(p) for p in baseline['pins']]
    paths += [Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield') / n
              for n in ('Starfield.exe', 'Data/Starfield.esm', 'Data/Starfield - PlanetData.ba2')]
    result = dict(head=subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
                  index_sha256=pin(ROOT / '.git/index'),
                  pins={str(p): pin(p) for p in sorted(set(paths))},
                  game_absent=True, protected_changes=0)
    if args.phase == 'after':
        before = json.loads((OUT / 'audit-before.json').read_text())
        assert result == before
    write(OUT / f'audit-{label}.json', result)
    print(args.phase, len(result['pins']), 'immutable pins; protected changes 0')


if __name__ == '__main__':
    main()
