# SPDX-License-Identifier: GPL-3.0-or-later
"""Replay the owned D5AF complete ordinary-stage controls in D5AQ scratch.

SOR-P-0002 adaptation: namespace replacement only; all inherited PE/input,
disk-floor, allocation, callback and complete independent geometry checks remain.
Reads pinned D5S definitions/fixture metadata and installed native instructions;
writes fresh ignored D5AQ child files. Executes only private native pages in a
disposable host, with supplied keys/collections/allocators and suppressed private
deallocation. No game, save, database, installed file, observer, network or Git
mutation. Stops on inherited faults; retain outputs and let child exit free pages.
"""
import os
import sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):
    raise RuntimeError('Use pinned Python -E -B without optimization')

from pathlib import Path


def main():
    inherited = Path(__file__).with_name('d5af_geometry.py')
    source = inherited.read_text(encoding='utf8').replace('d5af', 'd5aq').replace('D5AF', 'D5AQ')
    namespace = {'__file__': str(Path(__file__).resolve()), '__name__': 'd5aq_geometry_adapter'}
    exec(compile(source, str(inherited), 'exec'), namespace)
    namespace['main']()


if __name__ == '__main__':
    main()
