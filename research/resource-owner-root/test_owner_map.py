# SPDX-License-Identifier: GPL-3.0-or-later
"""Authored transition oracles; no game bytes or native execution."""
import unittest
from owner_map import reconstruct, ordinary_candidates


def row(root, *ids):
    return dict(root=root, slots=list(ids) + [0] * (6-len(ids)))


class Transitions(unittest.TestCase):
    def test_exchange_carries_displaced_array_to_another_root(self):
        result = reconstruct([row(10, 11), row(10, 12), row(20, 21)])
        self.assertEqual(result['maps'], {10: [12], 20: [11, 21]})
        self.assertEqual(result['trace'][1]['staging_after'], [11])

    def test_duplicate_and_zero_root_carry(self):
        result = reconstruct([row(0, 11, 11), row(10, 12)])
        self.assertEqual(result['maps'], {10: [11, 11, 12]})

    def test_empty_replacement_is_not_retention(self):
        result = reconstruct([row(10, 11), row(10)])
        self.assertEqual(result['maps'], {10: []})
        self.assertEqual(result['discarded_staging'], [11])

    def test_order_changes_cross_root_result(self):
        a = reconstruct([row(10, 11), row(10, 12), row(20, 21)])
        b = reconstruct([row(10, 12), row(10, 11), row(20, 21)])
        self.assertEqual(b['maps'], {10: [11], 20: [12, 21]})
        self.assertNotEqual(a['maps'], b['maps'])

    def test_failed_append_does_not_stop_later_slots(self):
        result = reconstruct([row(10, 11, 12)], {(0, 0)})
        self.assertEqual(result['maps'], {10: [12]})

    def test_no_occurrence_cap_or_deduplication(self):
        result = reconstruct([row(0, *([11]*6))]*5 + [row(10)])
        self.assertEqual(result['maps'][10], [11]*30)

    def test_empty_range(self):
        self.assertEqual(reconstruct([])['maps'], {})

    def test_missing_map_and_tied_rarity(self):
        self.assertEqual(ordinary_candidates(10, {}, {10: 0})['status'], 'NO_ROOT_MAP_ENTRY')
        self.assertIsNone(ordinary_candidates(10, {10: [11]}, {10: 0, 11: 0})['ordered'])

    def test_unresolved_root_stops_before_supplemental_resolution(self):
        self.assertEqual(ordinary_candidates(10, {10: [11]}, {11: 1})['status'], 'UNRESOLVED_ROOT')

    def test_sorted_duplicates_and_unresolved_forms(self):
        self.assertEqual(ordinary_candidates(10, {10: [11, 11, 99]}, {10: 0, 11: 2})['ordered'],
                         [11, 11, 10])

    def test_invalid_domains(self):
        with self.assertRaises(ValueError):
            reconstruct([row(-1)])
        with self.assertRaises(ValueError):
            reconstruct([row(10, True)])


if __name__ == '__main__':
    unittest.main()
