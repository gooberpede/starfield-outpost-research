# SPDX-License-Identifier: GPL-3.0-or-later
"""Original synthetic discriminators; no installed or captured answers."""
from types import SimpleNamespace as N
import unittest
from components import components, first_everywhere
from candidate_order import candidates
from qualification import qualify


def record(*fields):
    return ({}, list(fields))


def word(value):
    return value.to_bytes(4, 'little')


class Initialization(unittest.TestCase):
    def test_special_selection_needs_native_capacity_and_descriptor(self):
        resource = N(form_id='0000002d')
        fields = [('provenance', N(value='SPECIAL')), ('occupied_count_before', 8), ('accepted', True)]
        event = N(kind=N(value='RESOURCE_OCCURRENCE_RECORDED'), fields=fields)
        state = N(biome=N(form_id='0000000a'), effective_rsgd=N(form_id='00000014'),
                  special_selection=resource, events=[event])
        prediction = N(biome_results=[N(orchestration=state)], everywhere_resources=[])
        records = {10: record(), 20: record((b'RNAM', word(45)), (b'DNAM', b'descriptor'))}
        with self.assertRaisesRegex(ValueError, 'CAPACITY_GUARD'):
            qualify(records, prediction)
        fields[1] = ('occupied_count_before', 7)
        self.assertEqual(qualify(records, prediction)['specials'][0]['occupied_before'], 7)
        records[20] = record((b'RNAM', word(45)))
        with self.assertRaisesRegex(ValueError, 'SELECTED_DESCRIPTOR'):
            qualify(records, prediction)

    def test_everywhere_prepass_difference_is_rejected(self):
        prediction = N(biome_results=[], everywhere_resources=[N(form_id='0000002e')])
        with self.assertRaisesRegex(ValueError, 'SHARED_OCCUPANCY'):
            qualify({}, prediction)

    def test_small_ties_are_stable_and_duplicates_survive(self):
        result = candidates(10, {10: [11, 12, 11]}, {10: 0, 11: 2, 12: 2})
        self.assertEqual(result['ordered'], [11, 12, 11, 10])

    def test_large_unequal_tie_is_unknown(self):
        self.assertIsNone(candidates(10, {10: [11, 12] * 16}, {10: 0, 11: 2, 12: 2})['ordered'])

    def test_biome_order_first_match_no_chance_or_override(self):
        records = {10: record((b'RNAM', word(20)), (b'RNAM', word(21))),
            20: record((b'RNAM', word(30)), (b'DNAM', b'ignored'),
                       (b'RNAM', word(31)), (b'RNAM', word(32))),
            21: record((b'RNAM', word(33))),
            30: record((b'SNAM', b'\x00')), 31: record((b'SNAM', b'\x06')),
            32: record((b'SNAM', b'\x06')), 33: record((b'SNAM', b'\x06'))}
        self.assertEqual(first_everywhere(records, 10), (31, 20))
        records[10] = record((b'RNAM', word(21)), (b'RNAM', word(20)))
        self.assertEqual(first_everywhere(records, 10), (33, 21))

    def test_no_match_is_zero(self):
        self.assertEqual(first_everywhere({10: record()}, 10), (0, None))

    def test_all_slots_and_key_order_preserve_duplicate_occurrences(self):
        def selected(biome, family, special):
            return N(orchestration=N(biome=N(form_id=f'{biome:08x}', index=biome),
                effective_rsgd=N(form_id='00000063'), special_selection=special),
                common_assignment=N(family=family, mechanism='synthetic'))
        refs = [N(form_id=f'{fid:08x}') for fid in (41, 42, 43, 44)]
        family = N(root=N(form_id='00000028'), emitted_descendants=refs)
        records = {10: record((b'RNAM', word(20))), 11: record((b'RNAM', word(20))),
                   20: record((b'RNAM', word(46))), 46: record((b'SNAM', b'\x06'))}
        records.update({fid: record((b'SNAM', bytes([rarity])))
                        for rarity, fid in enumerate((41, 42, 43, 44), 1)})
        rows = components(records, N(biome_results=[selected(11, None, None),
                          selected(10, family, N(form_id='0000002d'))]))
        self.assertEqual([r['biome'] for r in rows], [10, 11])
        self.assertEqual(rows[0]['slots'], [41, 42, 43, 44, 45, 46])
        self.assertEqual(rows[1]['slots'], [0, 0, 0, 0, 0, 46])
        self.assertEqual(rows[0]['rsgd'], 99)
        self.assertEqual(rows[0]['everywhere_rsgd'], 20)


if __name__ == '__main__':
    unittest.main()
