"""SPDX-License-Identifier: GPL-3.0-or-later
Synthetic independent algebra/boundary checks for SOR-EXP-0019's numerical model.
No file/target effects and no claim of executing native code.
"""
import unittest
from audit_activated_grid import hierarchy, offset, signed_remainder, transform, N
from beacon_terrain_projection import from_square, grid_centre, to_square
import math


class GridTests(unittest.TestCase):
    def test_hierarchy_all_indices(self):
        for i in range(N):
            c,s,f = hierarchy(i)
            self.assertTrue(0<=c<256 and 0<=s<16 and 0<=f<12)
            self.assertEqual(192*c+12*s+f,i)

    def test_signed_wrap_and_tags(self):
        self.assertEqual(signed_remainder(-N-1,N),-1)
        for tag in range(4):
            self.assertEqual(offset(tag,0,0,-1,0),(tag^1,N-1,0))
            self.assertEqual(offset(tag,0,0,0,-1),(tag^3,0,N-1))
            self.assertEqual(offset(tag,N-1,N-1,1,1),(tag^2,0,0))
            self.assertEqual(offset(tag,12,34,N,-N),(tag,12,34))

    def test_designated_center_and_poles(self):
        self.assertAlmostEqual(from_square(0,0,0)[1],math.pi/2)
        self.assertAlmostEqual(from_square(1,0,0)[1],-math.pi/2)
        for tag in (0,1):
            for i,j in [(0,0),(N-1,N-1),(N//2,N//2),(10467,21144)]:
                lon,lat = grid_centre(tag,i,j)
                t,u,v = to_square(lon,lat)
                self.assertEqual(t,tag)
                self.assertAlmostEqual((u+.5)*N,i+.5,places=6)
                self.assertAlmostEqual((v+.5)*N,j+.5,places=6)
                self.assertLess(abs(lat),math.pi/2)
        for u,v in [(.5,0),(0,.5),(-.5,-.5)]:
            self.assertAlmostEqual(from_square(0,u,v)[1],0,places=14)

    def test_rotations_reflections_are_square_permutations(self):
        matrices=[(1,0,0,1),(0,-1,1,0),(-1,0,0,-1),(0,1,-1,0),
                  (1,0,0,-1),(0,1,1,0),(-1,0,0,1),(0,-1,-1,0)]
        expected={(x,y) for x in range(16) for y in range(16)}
        for m in matrices:
            self.assertEqual({transform(m,x,y) for x,y in expected},expected)
        footprint={(x,y) for x in range(2,4) for y in range(5,9)}
        rotated={transform(matrices[1],x,y) for x,y in footprint}
        self.assertEqual(len({x for x,y in rotated}),4)
        self.assertEqual(len({y for x,y in rotated}),2)


if __name__ == '__main__':
    unittest.main()
