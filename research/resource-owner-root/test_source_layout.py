# SPDX-License-Identifier: GPL-3.0-or-later
"""Asymmetric authored grids expose installation/index errors."""
import unittest
from source_layout import install_fnam


class Layout(unittest.TestCase):
    def test_asymmetric_coordinate_oracle(self):
        serialized = [(i, 255-i) for i in range(256)]
        native = install_fnam(serialized)
        self.assertEqual(native[8*16+7], (7*16+8, 255-(7*16+8)))
        self.assertEqual(native[7*16+7], serialized[7*16+7])

    def test_preserves_every_pair_and_flag(self):
        serialized = [(i % 7, i) for i in range(256)]
        self.assertEqual(sorted(install_fnam(serialized)), sorted(serialized))
        self.assertEqual(install_fnam(install_fnam(serialized)), serialized)

    def test_wrong_shape_rejected(self):
        with self.assertRaises(ValueError):
            install_fnam([0]*255)


if __name__ == '__main__':
    unittest.main()
