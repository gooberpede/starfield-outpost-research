# SPDX-License-Identifier: GPL-3.0-or-later
"""Rerun the owned complete geometry control in a fresh D5AH namespace.

SOR-P-0002: D5AF geometry method, with only output namespace/name changed.
Reads pinned installed PE, D5S inputs and D5AF native metadata. Executes selected
native routines only in a disposable child; substituted allocators, collection
getters and coordinate keys retain inherited limits. Writes ignored receipts.
No game, save, database, observer, network or Git mutation. Requires Windows
CPython and verified local proprietary inputs. Stop on inherited guards/faults;
preserve outputs. Process exit releases private mappings.
"""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]


def main():
    inherited = ROOT / 'research/resource-retained-population/d5af_geometry.py'
    source = inherited.read_text(encoding='utf8').replace('d5af', 'd5ah').replace(
        'D5AF', 'D5AH')
    # Preserve subprocess recursion through this wrapper, which reapplies exactly
    # the same namespace transformation in the child process.
    namespace = {'__file__': str(Path(__file__).resolve()), '__name__': 'd5ah_geometry_adapter'}
    exec(compile(source, str(inherited), 'exec'), namespace)
    namespace['main']()


if __name__ == '__main__':
    main()
