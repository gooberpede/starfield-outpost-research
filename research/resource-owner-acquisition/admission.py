# SPDX-License-Identifier: GPL-3.0-or-later
"""Offline stop selector; no I/O or target effects.

Combines a complete construction trace with separately verified Workshop-bound
consumption. Equal retained source bytes establish correspondence only. The
historical producer/consumer epoch remains UNKNOWN, including identical ABA.
"""
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('d4a_admission', HERE.parent / 'resource-tungsten-acquisition/admission.py')
d4a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(d4a)
spec = importlib.util.spec_from_file_location('d4d_validate', HERE / 'compare.py')
comparison = importlib.util.module_from_spec(spec)
spec.loader.exec_module(comparison)

TARGET_SOURCE = '0:27156:35988:0028be0d'


class Tracker:
    """Feed only persisted, independently decoded samples; ACK precedes stop."""
    def __init__(self):
        self.consumer = d4a.Tracker()
        self.active_constructions = comparison.State()
        self.construction = None
        self.last_match = None

    def feed(self, row):
        result = comparison.validate([row], self.active_constructions, finalize=False)
        for chain in result['chains']:
            if chain['source_identity'] == TARGET_SOURCE and chain['owner'] == d4a.BODY:
                self.construction = chain
        consumed = self.consumer.feed(row)
        if not consumed:
            return False
        accepted = self.consumer.last_match
        for chain in [self.construction] if self.construction is not None else []:
            if (chain['source_identity'] == TARGET_SOURCE and chain['owner'] == d4a.BODY and
                    chain['source'] == accepted['source_context']['raw_source'] and
                    chain['selected'] == 0x57d5 and chain['calls'] and
                    chain['selected_array_reconciliation'] == 'EXACT_IDS_AND_DESCENDING_RARITY' and
                    chain['entry']['pid'] == accepted['pid']):
                self.last_match = dict(construction=chain, consumption=accepted,
                    qualification='SOURCE_CORRESPONDENCE_WITH_SEPARATE_WORKSHOP_BINDING',
                    generation_epoch=None, historical_producer_join=None)
                return True
        return False
