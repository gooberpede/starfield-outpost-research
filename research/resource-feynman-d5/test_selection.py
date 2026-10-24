# SPDX-License-Identifier: GPL-3.0-or-later
"""Synthetic discriminators for native descriptor ordering; no game I/O."""
import unittest
import struct
from selection import descriptor, qualify_everywhere


def record(*pairs):
    return {}, [(tag, value.to_bytes(4, 'little') if isinstance(value, int) else value)
                for tag, value in pairs]


class SelectionTests(unittest.TestCase):
    def setUp(self):
        self.rows = [dict(biome=30, root=7, rsgd=300),
                     dict(biome=20, root=7, rsgd=200),
                     dict(biome=10, root=7, rsgd=100)]
        self.records = {10: record((b'RNAM', 100)), 20: record((b'RNAM', 200)),
                        30: record((b'RNAM', 300)),
                        100: record((b'RNAM', 7), (b'DNAM', b'A')),
                        200: record((b'RNAM', 7), (b'DNAM', b'B')),
                        300: record((b'RNAM', 8), (b'DNAM', b'C'))}

    def test_key_order_beats_authoring_order(self):
        raw, detail = descriptor(self.records, self.rows, 30)
        self.assertEqual(raw, b'A')
        self.assertEqual(detail['supplier_biome'], '0000000a')

    def test_failed_candidate_continues(self):
        self.records[100] = record((b'RNAM', 9), (b'DNAM', b'X'))
        raw, detail = descriptor(self.records, self.rows, 30)
        self.assertEqual(raw, b'B')
        self.assertTrue(any(r['outcome'] == 'NO_DESCRIPTOR' for r in detail['trace']))

    def test_current_effective_precedes_alternates(self):
        self.records[300] = record((b'RNAM', 7), (b'DNAM', b'CURRENT'))
        self.assertEqual(descriptor(self.records, self.rows, 30)[0], b'CURRENT')

    def test_alternate_override_is_not_its_rnam(self):
        self.rows[2]['rsgd'] = 200
        self.assertEqual(descriptor(self.records, self.rows, 30)[0], b'A')

    def test_wrong_root_skips_then_fallback(self):
        for row in self.rows[1:]:
            row['root'] = 9
        raw, detail = descriptor(self.records, self.rows, 30)
        self.assertEqual(raw, b'C')
        self.assertEqual(detail['descriptor_route'], 'FIRST_CURRENT_FALLBACK')

    def test_current_rnam_before_alternate(self):
        self.rows[0]['rsgd'] = 400
        self.records[400] = record()
        self.records[300] = record((b'RNAM', 7), (b'DNAM', b'RNAM'))
        self.assertEqual(descriptor(self.records, self.rows, 30)[0], b'RNAM')

    def test_duplicate_creation_keys_fail_closed(self):
        with self.assertRaisesRegex(ValueError, 'DUPLICATE'):
            descriptor(self.records, self.rows + [self.rows[0]], 30)

    def test_nonzero_everywhere_remains_unsupported(self):
        records = {7: record((b'SNAM', b'\x06'))}
        for chance in (0.0, 1.0):
            raw = bytearray(560)
            struct.pack_into('<f', raw, 40 * 13 + 28, chance)
            records[100] = record((b'RNAM', 7), (b'DNAM', bytes(raw)))
            if chance:
                with self.assertRaisesRegex(ValueError, 'NONZERO_EVERYWHERE'):
                    qualify_everywhere(records, 100)
            else:
                self.assertIsNone(qualify_everywhere(records, 100))


if __name__ == '__main__':
    unittest.main()
