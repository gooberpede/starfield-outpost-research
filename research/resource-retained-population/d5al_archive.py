# SPDX-License-Identifier: GPL-3.0-or-later
"""Guarded D5AL entry to the owned lossless archive implementation.

Reads pinned roots/seal/postflight and finished evidence; writes exclusive
archive/seal/verification outputs outside sealed roots. Preserves raw originals.
No network, deletion, save modification, game operation or native execution.
"""
import sys
import os
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):
    raise RuntimeError('Use pinned Python -E -B without PYTHONOPTIMIZE, -O or -OO')
from pathlib import Path
import importlib.util


def main():
    import argparse
    import d5al_operations as operations
    p = argparse.ArgumentParser(description=__doc__, add_help=False)
    p.add_argument('--plan', type=Path, required=True)
    p.add_argument('--plan-sha256', required=True)
    if '--help' in sys.argv:
        p.print_help()
        return
    args, remaining = p.parse_known_args()
    plan = operations.original.pinned_json(args.plan, args.plan_sha256)
    operations.source_pins(plan)
    sys.argv = [sys.argv[0], *remaining]
    path = Path(__file__).resolve().parents[2] / 'runtime/session-tools/archive.py'
    sys.path.insert(0, str(path.parent))
    spec = importlib.util.spec_from_file_location('d5al_owned_archive', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.main()

if __name__ == '__main__':
    main()
