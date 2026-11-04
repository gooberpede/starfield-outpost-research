# SPDX-License-Identifier: GPL-3.0-or-later
"""Compare selected protected originals with retained historical identities.

Reads bytes of twenty designated saves/backups/analysis cores and D5T installed
inputs, without decoding saves or opening databases. Writes one fresh ignored
JSON; all other files are read-only. Uses owned D5AM/D5T fingerprints and stdlib.
Stop on mismatch, disk-floor breach, reparse output or existing output. This is
a selected preservation check, never complete active-save or live admission.
"""
import os
import sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):
    raise RuntimeError('Use pinned Python -E -B without optimization')

import argparse
import json
from pathlib import Path
from d5ap_analyze import ROOT, guard, require, sha, write


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    out = args.out.resolve()
    floors = guard()
    require(out.is_relative_to(ROOT / '.local-work/d5aq') and not out.exists(), 'Fresh task-local output')
    require(not any(p.is_symlink() or p.is_junction() for p in (out, *out.parents)), 'No reparse output')
    pins = ROOT / '.local-work/d5am/selected-preservation03.json'
    selected = json.loads(pins.read_bytes())['rows']
    rows = {name: dict(bytes=Path(name).stat().st_size, sha256=sha(name)) for name in selected}
    require(rows == selected, 'Selected protected content changed')
    initial = ROOT / '.local-work/d5t/initial.json'
    installed = json.loads(initial.read_bytes())['installed']
    require({name: sha(name) for name in installed} == installed, 'Installed input changed')
    out.parent.mkdir(parents=True, exist_ok=True)
    write(out, dict(status='PASS', selected=rows, installed=installed,
                    input_pins={str(pins): sha(pins), str(initial): sha(initial)},
                    method_sha256=sha(__file__), floors=floors, postflight_floors=guard(),
                    scope='Selected original-content comparison; no save decode or database opening'))
    print(json.dumps(dict(status='PASS', selected=len(rows), installed=len(installed))))


if __name__ == '__main__':
    main()
