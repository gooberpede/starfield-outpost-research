# SPDX-License-Identifier: GPL-3.0-or-later
"""Offline Python receipt, selector and predictor regressions; no live access.

Runs owned unittest files and the disposable receipt self-test using installed
CPython/stdlib. Writes exclusive ignored command/stdout/stderr records only.
No save, configuration, network, dependency or Git writes.
"""
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]


def main():
    out = ROOT / '.local-work/resource-owner-acquisition/python-checks01'
    out.mkdir(parents=True, exist_ok=False)
    env = dict(os.environ, PYTHONPATH=os.pathsep.join(str(ROOT / 'research' / p) for p in
        ('resource-standalone', 'resource-geometry', 'resource-pattern-selection')))
    commands = [
        [sys.executable, '-B', '-m', 'unittest', 'discover', '-s', str(ROOT/'research/resource-standalone'), '-v'],
        [sys.executable, '-B', '-m', 'unittest', 'discover', '-s', str(ROOT/'research/resource-tungsten-acquisition'), '-v'],
        [sys.executable, '-B', str(ROOT/'research/resource-ui-oracle/receipt_probe.py'), '--self-test', '--output', str(out/'transport')],
    ]
    rows = []
    for i, command in enumerate(commands):
        run = subprocess.run(command, cwd=ROOT, env=env, capture_output=True)
        (out / f'{i}-stdout.txt').write_bytes(run.stdout)
        (out / f'{i}-stderr.txt').write_bytes(run.stderr)
        rows.append(dict(command=command, exit=run.returncode))
        print(i, run.returncode, (run.stdout+run.stderr).decode(errors='replace')[-180:])
    with (out / 'summary.json').open('x', encoding='utf8', newline='\n') as stream:
        json.dump(rows, stream, indent=2)
        stream.write('\n')
    assert all(r['exit']==0 for r in rows)


if __name__ == '__main__':
    main()
