# SPDX-License-Identifier: GPL-3.0-or-later
"""Authenticate existing offline inputs without opening analysis projects.

SOR-P-0002 adaptation of d5ae_baseline.py: output root and governing brief only.
Reads pinned installed PE/data, database core bytes for identity only, protected
research-copy Save52 and B2 evidence. Writes one exclusive ignored receipt. No
game, original-save write, Ghidra opening, configuration, network or Git mutation.
This selected-input audit is not a future live preflight or complete backup audit.
Stdlib only; caller-available C:/D: floors and original identity guards retained.
"""
from pathlib import Path


def main():
    inherited = Path(__file__).with_name('d5ae_baseline.py')
    source = inherited.read_text(encoding='utf8').replace("'.local-work/d5ae'", "'.local-work/d5ai'").replace(
        'CODEX_BRIEF_SOR_RG2_D5AE_GC10_construction_winner_scheduling.md',
        'CODEX_BRIEF_SOR_RG2_D5AI_population_lifecycle_geometry_observer_readiness.md')
    namespace = {'__file__': str(Path(__file__).resolve()), '__name__': 'd5ai_inputs'}
    exec(compile(source, str(inherited), 'exec'), namespace)
    namespace['main']()


if __name__ == '__main__':
    main()
