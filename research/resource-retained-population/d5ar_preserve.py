# SPDX-License-Identifier: GPL-3.0-or-later
"""Selected D5AR offline preservation, adapted from owned D5AQ (SOR-P-0002).

Reads twenty designated originals/backups/analysis cores, three installed inputs
and existing exact manifests. Does not decode saves or open databases. Writes
one exclusive ignored receipt; no game/configuration/Git/network operation.
This is selected content preservation, not complete live admission.
"""
import os
import sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):
    raise RuntimeError('Use pinned Python -E -B without optimization')

import json
from pathlib import Path
from d5ap_analyze import ROOT, guard, require, sha, write


def main():
    out = Path(sys.argv[1]).resolve()
    floors = guard()
    require(out.is_relative_to(ROOT / '.local-work/d5ar') and not out.exists(), 'Fresh ignored D5AR output')
    require(not any(p.is_symlink() or p.is_junction() for p in (out, *out.parents)), 'No reparse outputs')
    pins = ROOT / '.local-work/d5am/selected-preservation03.json'
    selected = json.loads(pins.read_bytes())['rows']
    rows = {name: dict(bytes=Path(name).stat().st_size, sha256=sha(name)) for name in selected}
    require(rows == selected, 'Selected protected content changed')
    initial = ROOT / '.local-work/d5t/initial.json'
    installed = json.loads(initial.read_bytes())['installed']
    require({name: sha(name) for name in installed} == installed, 'Installed input changed')
    write(out, dict(status='PASS', selected=rows, installed=installed,
                    input_pins={str(pins): sha(pins), str(initial): sha(initial)},
                    method_sha256=sha(__file__), floors=floors, postflight_floors=guard(),
                    scope='Selected original-content comparison, no save decode/database opening; not live admission'))
    print(json.dumps(dict(status='PASS', selected=len(rows), installed=len(installed))))


if __name__ == '__main__':
    main()
