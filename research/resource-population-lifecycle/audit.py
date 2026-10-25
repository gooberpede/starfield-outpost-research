# SPDX-License-Identifier: GPL-3.0-or-later
"""Hash protected offline inputs and write exclusive local receipts.

Reads historical D5B pin inventories, installed inputs and protected-save policy.
Uses owned protection.py under SOR-P-0002 and Python stdlib; no target execution,
database, save, configuration, network or Git writes. Before snapshots all existing
D5B files, including sealed receipts; after compares exactly that inventory.
Hashes prove preservation, not native semantics. Run from the repository root.
"""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / '.local-work/resource-population-lifecycle'
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
    args = ap.parse_args()
    assert min(shutil.disk_usage(d).free for d in ('C:/', 'D:/')) >= 40_000_000_000
    assert subprocess.check_output(['powershell', '-NoProfile', '-Command',
        '@(Get-Process Starfield -ErrorAction SilentlyContinue).Count'], text=True).strip() == '0'
    protected = protection.audit()
    write(OUT / f'protected-{args.phase}.json', protected)
    assert not protected['changes'], protected['changes']
    if args.phase == 'before':
        local = ROOT / '.local-work/resource-combined-acquisition'
        expected = json.loads((local / 'phase-b-evidence-before01.json').read_text())['pins']
        expected.update(json.loads((local / 'phase-b-baseline01.json').read_text())['phase_a_pins'])
        for path, digest in expected.items():
            assert pin(path) == digest, path
        paths = set(map(Path, expected))
        paths.update(p for p in local.rglob('*') if p.is_file())
        paths.update(p for p in (ROOT / '.local-work/recon').glob('*.tsv'))
        result = dict(head=subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
            index_sha256=pin(ROOT / '.git/index'), pins={str(p): pin(p) for p in sorted(paths)})
    else:
        before = json.loads((OUT / 'audit-before.json').read_text())
        result = dict(head=subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
            index_sha256=pin(ROOT / '.git/index'), pins={p: pin(p) for p in before['pins']})
        assert result == before, 'Protected input, HEAD or index changed'
    assert not subprocess.check_output(['git', 'diff', '--cached', '--name-only'])
    write(OUT / f'audit-{args.phase}.json', result)
    write(OUT / f'audit-{args.phase}-time.json', dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        game_absent=True, pins=len(result['pins']), protected_changes=0))
    print(args.phase, len(result['pins']), 'unchanged pins; protected changes 0')


if __name__ == '__main__':
    main()
