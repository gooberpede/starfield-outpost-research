# SPDX-License-Identifier: GPL-3.0-or-later
"""Synthetic original controls only; no files, game or proprietary fixtures."""
import unittest
from points import transect, classify, select


class Points(unittest.TestCase):
    def test_opposite_bracket(self):
        a, b = transect([0, 0], [10, 0], lambda q: q[0] < 3)
        self.assertLess(a[0], 3); self.assertGreaterEqual(b[0], 3)
        self.assertLess(b[0]-a[0], 1e-7)

    def test_same_endpoint_refused(self):
        with self.assertRaises(ValueError):
            transect([0, 0], [1, 1], lambda q: True)

    def test_empty_union(self):
        self.assertEqual(classify([], [0, 0]), dict(region=[], strips=[]))

    def test_disk_controls_and_far_source(self):
        # Disk center is outside nominal circle. Must not discard its geometry.
        p = dict(resource='synthetic', points=[[160, 0, 0, 20]])
        r = dict(center=[0, 0], sources=[dict(regions=[p], cells=1)],
                 fixed_queries=[dict(point=[150, 0], resources=['synthetic']),
                                dict(point=[0, 0], resources=[])])
        result = select(r)
        self.assertEqual(result['coverage']['paths'], 1)
        self.assertEqual(result['samples'][3]['expected']['region'], ['synthetic'])
        self.assertEqual(result['samples'][5]['expected']['region'], [])


if __name__ == '__main__':
    unittest.main()
