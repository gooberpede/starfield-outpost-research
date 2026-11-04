# SPDX-License-Identifier: GPL-3.0-or-later
"""Recheck fixed main-file Special/Everywhere applicability for D5AQ.

SOR-P-0002 namespace adaptation of owned D5AF extra-input reconstruction. Reads
pinned ESM and pinned maintainer-owned selection methods; writes one fresh local
JSON. No game, save, database, configuration, network or Git mutation. Stop on
inherited input/disk/applicability failure; retain outputs. Model output remains
conditional main-file selection, never an unrecorded loaded retail component.
"""
import os
import sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):
    raise RuntimeError('Use pinned Python -E -B without optimization')

from pathlib import Path


def main():
    inherited = Path(__file__).with_name('d5af_extra_inputs.py')
    source = inherited.read_text(encoding='utf8').replace('d5af', 'd5aq').replace('D5AF', 'D5AQ')
    namespace = {'__file__': str(Path(__file__).resolve()), '__name__': '__main__'}
    exec(compile(source, str(inherited), 'exec'), namespace)


if __name__ == '__main__':
    main()
