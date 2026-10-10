"""SPDX-License-Identifier: GPL-3.0-or-later
Countermodel tests establish ambiguity, not geographical accuracy.
"""
import math
import unittest
from residual_ambiguity import countermodel
from beacon_terrain_projection import grid_centre


class ResidualAmbiguityTests(unittest.TestCase):
    def test_same_integer_centers(self):
        for tag,x,y in ((0,100,200),(1,10467,21144),(0,16992,33312)):
            expected = grid_centre(tag,x,y)
            for epsilon in (0,.05,-.05):
                self.assertEqual(countermodel(tag,x,y,0,0,epsilon),expected)
                for a,b in zip(countermodel(tag,x,y,100,100,epsilon),
                               grid_centre(tag,x+1,y+1)):
                    self.assertAlmostEqual(a,b,places=14)

    def test_different_same_phase_interior(self):
        a = countermodel(1,10467,21144,56.820404052734375,59.05859375)
        b = countermodel(1,10467,21144,56.820404052734375,59.05859375,.05)
        self.assertGreater(max(abs(x-y) for x,y in zip(a,b)),1e-7)

    def test_integer_translation_cancels(self):
        # A chart origin change and the opposite local shift preserve both
        # examples. No claim of bit-exact runtime float32 translation follows.
        for epsilon in (0,.05):
            a = countermodel(1,10464,21120,356.8204040527344,2459.05859375,epsilon)
            b = countermodel(1,10467,21144,56.820404052734375,59.05859375,epsilon)
            for x,y in zip(a,b):
                self.assertAlmostEqual(x,y,places=14)

    def test_guard(self):
        with self.assertRaisesRegex(ValueError,'NONMONOTONE'):
            countermodel(0,100,100,0,0,1/(2*math.pi))
        with self.assertRaisesRegex(ValueError,'NONFINITE'):
            countermodel(0,100,100,math.nan,0)


if __name__ == '__main__':
    unittest.main()
