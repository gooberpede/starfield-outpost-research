# SPDX-License-Identifier: GPL-3.0-or-later
"""Rerun inherited owned debugger suites and geometry controls, stdlib only.

Reads pinned inherited builds and protected evidence. Executes disposable
synthetic Windows targets, never retail. Writes fresh ignored receipts/logs.
No saves, configuration, downloads, database or Git mutations.
"""
import argparse
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
LOCAL = ROOT / '.local-work/resource-owner-acquisition'


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--name', required=True)
    args = ap.parse_args()
    assert args.name and all(c in 'abcdefghijklmnopqrstuvwxyz0123456789-' for c in args.name)
    out = LOCAL / args.name
    out.mkdir(exist_ok=False)
    suites = [('resource-tungsten-acquisition', 'd4b-build04'),
              ('resource-selection-context', 'build12'), ('resource-selection-operands', 'build05'),
              ('resource-region-ancestry', 'build06'), ('resource-oracle-retail', 'build14'),
              ('resource-oracle-collector', 'build08')]
    commands = [[sys.executable, '-B', str(ROOT / 'research' / name / 'qualify.py'),
        '--build', str(ROOT / '.local-work' / name / build),
        '--output', str(ROOT / '.local-work' / name / ('d4d-' + args.name))] for name, build in suites]
    commands += [[sys.executable, '-B', str(ROOT / 'research/resource-owner-acquisition/regressions.py')],
                 [sys.executable, '-B', str(ROOT / 'research/resource-owner-acquisition/checks.py')],
                 [sys.executable, '-B', str(ROOT / 'research/resource-tungsten-repair/replay.py'),
                  '--output', str(out / 'archimedes')]]
    results = []
    for index, command in enumerate(commands):
        run = subprocess.run(command, cwd=ROOT, capture_output=True)
        (out / f'{index}-stdout.txt').write_bytes(run.stdout)
        (out / f'{index}-stderr.txt').write_bytes(run.stderr)
        results.append(dict(command=command, exit_code=run.returncode))
        print(index, run.returncode, flush=True)
    (out / 'summary.json').write_text(json.dumps(results, indent=2) + '\n', encoding='utf8', newline='\n')
    assert all(r['exit_code'] == 0 for r in results)


if __name__ == '__main__':
    main()
