# SPDX-License-Identifier: GPL-3.0-or-later
"""Synthetic linked-tree loader and native-order counterexamples; offline only."""
import struct
import unittest
from installed import planet_tree, decode_tree


class InstalledTests(unittest.TestCase):
    def test_planet_link_is_not_last_orbital_fnam(self):
        fields = [(b'FNAM', struct.pack('<I', 17)), (b'BDST', b''),
                  (b'FNAM', bytes(24)), (b'BDED', b'')]
        self.assertEqual(planet_tree(fields), 17)
        with self.assertRaises(ValueError):
            planet_tree([(b'FNAM', bytes(24))])

    def test_missing_or_ambiguous_link_fails(self):
        for fields in ([], [(b'FNAM', bytes(4))],
                       [(b'FNAM', struct.pack('<I', 1))] * 2):
            with self.assertRaises(ValueError):
                planet_tree(fields)

    def test_native_table_order_is_not_biome_raster_order(self):
        words = list(range(65536))
        ids = struct.pack('<65536I', *words)
        fields = [(b'CNAM', struct.pack('<I', 2)), (b'DNAM', struct.pack('<I', 256)),
                  (b'FNAM', ids), (b'GNAM', bytes([8]) * 65536)]
        fields += fields[2:]
        tables = decode_tree(fields)
        self.assertEqual(tables[0][111 * 256 + 81], (28497, 8))
        self.assertNotEqual(tables[0][(255 - 81) * 256 + 111][0], 28497)
        self.assertEqual(tables[0], tables[1])

    def test_packed_or_truncated_faces_fail(self):
        prefix = [(b'CNAM', struct.pack('<I', 2)), (b'DNAM', struct.pack('<I', 256))]
        for body in ([(b'ENAM', bytes(4))] * 2,
                     [(b'FNAM', bytes(4)), (b'GNAM', bytes(1))] * 2):
            with self.assertRaises(ValueError):
                decode_tree(prefix + body)


if __name__ == '__main__':
    unittest.main()
