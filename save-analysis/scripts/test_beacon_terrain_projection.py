"""SPDX-License-Identifier: GPL-3.0-or-later. Analytical checks, no runtime proof."""
import math
import unittest
from beacon_terrain_projection import to_square, from_square, grid_cell, grid_centre, split_local


class ProjectionTests(unittest.TestCase):
    def test_sphere_roundtrip(self):
        for lon in (-math.pi, -2.8, -.22, 0, 1.3, math.pi):
            for lat in (-1.55, -.7, -.0001, .0001, .7, 1.55):
                result = from_square(*to_square(lon, lat))
                self.assertLess(abs(math.remainder(result[0]-lon, 2*math.pi)), 1e-12)
                self.assertLess(abs(result[1]-lat), 1e-12)

    def test_explicit_axes(self):
        self.assertAlmostEqual(from_square(0, 0, 0)[1], math.pi/2)
        self.assertAlmostEqual(from_square(1, 0, 0)[1], -math.pi/2)
        self.assertAlmostEqual(from_square(0, .5, .5)[0], math.pi/4)
        self.assertAlmostEqual(from_square(1, .5, .5)[0], 3*math.pi/4)
        self.assertAlmostEqual(from_square(2, .5, .5)[0], -3*math.pi/4)
        self.assertAlmostEqual(from_square(3, .5, .5)[0], -math.pi/4)

    def test_centres_survive_quantization(self):
        for tag in (0, 1):
            for i,j in ((0,0),(10465,21122),(24576,24576),(49151,49151)):
                self.assertEqual(grid_cell(*grid_centre(tag,i,j)), (tag,i,j))

    def test_float_split_negative_and_boundary(self):
        self.assertEqual(split_local(-.25), (-1,99.75))
        self.assertEqual(split_local(-100), (-1,0))
        self.assertEqual(split_local(100), (1,0))
        self.assertEqual(split_local(2459.05859375), (24,59.05859375))

    def test_invalid(self):
        with self.assertRaises(ValueError): to_square(0,2)
        with self.assertRaises(ValueError): from_square(0,.6,0)
        with self.assertRaises(ValueError): grid_centre(0,-1,0)


if __name__ == '__main__': unittest.main()
