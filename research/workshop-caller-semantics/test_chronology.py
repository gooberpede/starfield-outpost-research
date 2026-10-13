# SPDX-License-Identifier: GPL-3.0-or-later
import unittest
from chronology import intervals, stats


class ChronologyTests(unittest.TestCase):
    def test_emission_reordering_is_not_a_negative_interval(self):
        self.assertEqual(intervals([{'qpc':30},{'qpc':10},{'qpc':20}],10),[1.,1.])

    def test_equal_ticks_remain_zero(self):
        self.assertEqual(intervals([{'qpc':10},{'qpc':10}],10),[0.])

    def test_gap_preserved_in_percentiles_and_maximum(self):
        self.assertEqual(stats([.001,.001,200])['maximum'],200)
        self.assertEqual(stats([.001,.001,200])['median'],.001)

    def test_singleton_has_no_frequency(self):
        self.assertIsNone(stats(intervals([{'qpc':10}],10)))


if __name__ == '__main__':
    unittest.main()
