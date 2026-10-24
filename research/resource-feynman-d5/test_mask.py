# SPDX-License-Identifier: GPL-3.0-or-later
"""Opposite-mask and exact-boundary controls for the final sampling stage."""
import math
import unittest
from mask import sample, raster_index


class RasterTests(unittest.TestCase):
    def test_construction_query_differs_from_beacon_and_later_cell(self):
        raster = bytes([0x81, 0x08, 0x22, 0x34])
        construction = (-0.25, 0.25)
        beacon = (0.25, 0.25)
        later_cell = (0.25, -0.25)
        self.assertEqual(sample(construction, raster, 2, 2), 1)
        self.assertEqual(sample(beacon, raster, 2, 2), 8)
        self.assertEqual(sample(later_cell, raster, 2, 2), 4)

    def test_exact_column_boundary(self):
        self.assertEqual(raster_index(-1e-12, 0.25, 2, 2), 0)
        self.assertEqual(raster_index(0.0, 0.25, 2, 2), 1)

    def test_y_is_inverted(self):
        self.assertEqual(raster_index(-0.25, 0.0, 2, 2), 2)
        self.assertEqual(raster_index(-0.25, 1e-12, 2, 2), 0)

    def test_asymmetric_dimensions_and_clamp(self):
        self.assertEqual(raster_index(0.5, -0.5, 3, 2), 5)
        self.assertEqual(raster_index(-2.0, 2.0, 3, 2), 0)

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            raster_index(math.nan, 0, 2, 2)
        with self.assertRaises(ValueError):
            sample((0, 0), b'', 2, 2)


if __name__ == '__main__':
    unittest.main()
