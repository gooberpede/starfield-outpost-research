# SPDX-License-Identifier: GPL-3.0-or-later
"""Offline preservation: read existing pins/saves; write exclusive local receipts.

Adapted from resource-construction-demand/audit.py at the recorded baseline.
Stdlib and owned protection policy only; no target, Git, save or database writes.
"""
import datetime
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / '.local-work/resource-predictability-contrast'
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
    phase = sys.argv[1]
    assert phase in ('before', 'after')
    assert min(shutil.disk_usage(d).free for d in ('C:/', 'D:/')) >= 40_000_000_000
    protected = protection.audit()
    write(OUT / f'protected-{phase}.json', protected)
    assert not protected['changes']
    if phase == 'before':
        expected = {}
        for folder in ('resource-feynman-d5', 'resource-construction-demand'):
            expected.update(json.loads((ROOT / f'.local-work/{folder}/audit-after.json').read_text())['pins'])
        for path, digest in expected.items():
            assert pin(path) == digest, path
        paths = set(map(Path, expected))
        for folder in ('resource-feynman-d5', 'resource-construction-mask-selection',
                       'resource-combined-acquisition', 'resource-construction-demand',
                       'resource-source-decisions'):
            paths.update(p for p in (ROOT / '.local-work' / folder).rglob('*') if p.is_file())
        result = dict(head=subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
            index_sha256=pin(ROOT / '.git/index'), pins={str(p): pin(p) for p in sorted(paths)})
        write(OUT / 'baseline.json', dict(branch=subprocess.check_output(['git', 'branch', '--show-current'], text=True).strip(),
            status=subprocess.check_output(['git', 'status', '--short'], text=True),
            brief_sha256=pin(ROOT / 'docs/implementation-briefs/CODEX_BRIEF_SOR_RG2_D5G_source_predictability_and_reachable_query_invariance.md')))
    else:
        before = json.loads((OUT / 'audit-before.json').read_text())
        paths = list(before['pins'])
        with ThreadPoolExecutor(max_workers=8) as pool:
            actual = dict(zip(paths, pool.map(pin, paths)))
        result = dict(head=subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
            index_sha256=pin(ROOT / '.git/index'), pins=actual)
        assert result == before
    assert not subprocess.check_output(['git', 'diff', '--cached', '--name-only'])
    write(OUT / f'audit-{phase}.json', result)
    write(OUT / f'audit-{phase}-time.json', dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        pins=len(result['pins']), protected_changes=0))
    print(phase, len(result['pins']), 'pins; protected changes 0')


if __name__ == '__main__':
    main()
