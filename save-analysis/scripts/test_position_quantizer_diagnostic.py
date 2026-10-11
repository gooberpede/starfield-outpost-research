"""SPDX-License-Identifier: GPL-3.0-or-later
Instruction/algebra controls only, no native oracles, I/O or target effects.
"""
import math
import unittest
import struct
from position_quantizer_diagnostic import nested_axis, square_xyz, diagnose, kernel_sin


class QuantizerTests(unittest.TestCase):
    def test_poles_hemisphere_and_equator(self):
        self.assertEqual(square_xyz(0, 0, 1), (0, 0, 0))
        self.assertEqual(square_xyz(0, 0, -1), (1, 0, 0))
        self.assertEqual(square_xyz(1, 0, 0), (0, 0.5, 0))
        self.assertEqual(square_xyz(-1, 0, 0), (0, -0.5, 0))

    def test_nested_boundaries(self):
        for u, index, coarse, sub, fine in [(-.5,0,0,0,0), (0,24576,128,0,0),
                                            (.5,49151,255,15,11)]:
            r = nested_axis(u)
            self.assertEqual((r['index'],r['coarse'],r['sub'],r['fine']),
                             (index,coarse,sub,fine))
        # Independent binary64 nextafter boundary; not a native trig result.
        self.assertEqual(nested_axis(math.nextafter(0, -1))['index'], 24576)
        self.assertEqual(nested_axis(-2**-53)['index'], 24575)

    def test_invalid_domains(self):
        for args in [(0,0,0), (math.nan,0,1)]:
            with self.assertRaises(ValueError):
                square_xyz(*args)
        with self.assertRaises(ValueError):
            nested_axis(.5001)
        with self.assertRaises(ValueError):
            diagnose(0, math.pi)

    def test_kernel_explicit_dispatch_and_signed_zero(self):
        for mode in ('avx', 'fma'):
            self.assertEqual(kernel_sin(0.0, mode), 0.0)
            self.assertEqual(struct.pack('<d', kernel_sin(-0.0, mode)).hex(), '0000000000000080')
            self.assertAlmostEqual(kernel_sin(math.pi/2, mode), 1.0, places=15)
            self.assertEqual(kernel_sin(-.7, mode), -kernel_sin(.7, mode))
        with self.assertRaises(ValueError):
            kernel_sin(1, 'guessed')
        self.assertEqual(set(diagnose(.2, .3)['dispatch_candidates']), {'avx','fma'})


if __name__ == '__main__':
    unittest.main()
