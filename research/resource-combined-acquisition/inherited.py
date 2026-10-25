# SPDX-License-Identifier: GPL-3.0-or-later
"""Execute inherited synthetic debugger suites and ten offline geometry controls.

Reads unchanged owned scripts/builds and protected inputs. Writes fresh ignored
receipts and logs; never starts or attaches to Starfield. Stdlib only, installed
Windows tooling required. No save/configuration/analysis/Git mutation.
"""
import argparse
from pathlib import Path
import subprocess
import sys
from qualify import write
from build import ROOT, LOCAL


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--name', required=True)
    args = parser.parse_args()
    assert args.name and all(c in 'abcdefghijklmnopqrstuvwxyz0123456789-' for c in args.name)
    out = LOCAL / args.name
    out.mkdir(exist_ok=False)
    suites = [('resource-tungsten-acquisition', 'd4b-build04'),
              ('resource-selection-context', 'build12'), ('resource-selection-operands', 'build05'),
              ('resource-region-ancestry', 'build06'), ('resource-oracle-retail', 'build14'),
              ('resource-oracle-collector', 'build08')]
    commands = [[sys.executable, '-B', str(ROOT / 'research' / name / 'qualify.py'),
        '--build', str(ROOT / '.local-work' / name / build),
        '--output', str(ROOT / '.local-work' / name / ('d5b-' + args.name))] for name, build in suites]
    commands += [[sys.executable, '-B', str(ROOT / 'research/resource-tungsten-repair/teardown.py'),
                  '--build', str(ROOT / '.local-work/resource-tungsten-acquisition/d4b-build04'),
                  '--output', str(out / 'terminal')],
                 [sys.executable, '-B', str(ROOT / 'research/resource-combined-acquisition/regression.py'),
                  '--output', str(out / 'geometry'), '--build', str(ROOT / '.local-work/resource-feynman-d5/build04'),
                  '--controls', str(ROOT / '.local-work/resource-slot-provenance/build-controls02')]]
    results = []
    for index, command in enumerate(commands):
        run = subprocess.run(command, cwd=ROOT, capture_output=True)
        (out / f'{index}-stdout.txt').write_bytes(run.stdout)
        (out / f'{index}-stderr.txt').write_bytes(run.stderr)
        results.append(dict(command=command, exit_code=run.returncode))
        write(out / f'{index}-result.json', results[-1])
        print(index, run.returncode, flush=True)
    write(out / 'summary.json', results)
    assert all(r['exit_code'] == 0 for r in results)


if __name__ == '__main__':
    main()
