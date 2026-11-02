# SPDX-License-Identifier: GPL-3.0-or-later
"""Execute the owned fixed-input native geometry controls in fresh D5AI hosts.

SOR-P-0002 adaptation of d5af_geometry.py: output namespace and task name only.
Reads pinned installed PE, model and disposable-export metadata; executes selected
original native instructions inside its own child process with supplied allocators,
keys and collections. Writes ignored D5AI receipts, never retail or protected saves.
Requires installed Windows x64 CPython and authenticated existing local inputs.
Inherited failure/disk/identity guards apply; retain failed logs; exit frees mappings.
"""
from pathlib import Path


def main():
    inherited = Path(__file__).with_name('d5af_geometry.py')
    source = inherited.read_text(encoding='utf8').replace('d5af', 'd5ai').replace('D5AF', 'D5AI')
    namespace = {'__file__': str(Path(__file__).resolve()), '__name__': 'd5ai_geometry_host'}
    exec(compile(source, str(inherited), 'exec'), namespace)
    namespace['main']()


if __name__ == '__main__':
    main()
