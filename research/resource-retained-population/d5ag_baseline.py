# SPDX-License-Identifier: GPL-3.0-or-later
"""Freeze D5AG repository or selected input identities without target operations.

SOR-P-0002: adapts owned D5AF/D5AE baseline methods by output namespace and
brief name only. Reads repository, installed inputs, selected saves/evidence
and original database files as bytes. Writes fresh ignored receipts/copies.
Uses stdlib and Git; no database opening, game, network or Git mutation.
Stop on inherited identity, disk, output or index failure. Keep all receipts.
"""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]


def main():
    inherited = ROOT / 'research/resource-retained-population/d5af_baseline.py'
    source = inherited.read_text(encoding='utf8').replace('d5af', 'd5ag').replace(
        'CODEX_BRIEF_SOR_RG2_D5AF_construction_winner_stabilization.md',
        'CODEX_BRIEF_SOR_RG2_D5AG_terrain_resource_consistency_lifecycle.md')
    # The inherited input adapter replaces the D5AE basename before evaluation.
    namespace = {'__file__': str(Path(__file__).resolve()), '__name__': 'd5ag_baseline_adapter'}
    exec(compile(source, str(inherited), 'exec'), namespace)
    namespace['main']()


if __name__ == '__main__':
    main()
