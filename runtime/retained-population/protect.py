# SPDX-License-Identifier: GPL-3.0-or-later
"""Read-only Phase A preservation using the active archive-backed method.

Reads authenticated archive/index, surviving pins, installed inputs, configuration
and protected saves/backups. Writes a new ignored receipt directory and a Save52
rehearsal COPY there. No game, original save, Vortex or Git mutation. Requires
installed CPython and the retained owned D5L preservation sources and evidence.
"""

import sys

# Safety checks below require assertions, including when imported as a helper.
if not __debug__ or sys.flags.optimize != 0:
    raise RuntimeError('Python optimization is forbidden; invoke with -E -B and no -O/-OO')
import importlib.util
import json
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[2]


def main():
    label=sys.argv[1]
    assert re.fullmatch('[a-z0-9-]+',label)
    out=ROOT/'.local-work/d5p'/label
    out.mkdir(parents=True,exist_ok=False)
    directory=ROOT/'research/resource-retained-population'
    sys.path.insert(0,str(directory))
    spec=importlib.util.spec_from_file_location('d5p_existing_protection',directory/'prepare_native.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    receipt=module.full_preservation(out)
    module.write(out/'protection.json',receipt)
    print(json.dumps(dict(out=str(out),protected_saves=len(receipt['protected_live']),
                          installed=len(receipt['installed']),config=len(receipt['config']))))


if __name__=='__main__':main()
