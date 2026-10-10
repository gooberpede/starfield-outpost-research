"""SPDX-License-Identifier: GPL-3.0-or-later
Known evidence matches and adversarial packed-field separation controls.
No external inputs or effects; fixture provenance is EXP0020 trace notes.
"""
import unittest

from planet_world_key import (unpack_world_key, qualified_grid, find_unit3_context,
                              unit3_world_descriptors)


class WorldKeyControls(unittest.TestCase):
    def test_archived_kreet_origin_and_installed_identity(self):
        self.assertEqual(qualified_grid(0x02b20e79528028e0),
                         dict(x=10464, y=21120, tag=1, body_index=15,
                              system_id=88327, reserved=0))

    def test_independent_jemison_identity(self):
        self.assertEqual(qualified_grid(0x022e401882204260),
                         dict(x=16992, y=33312, tag=0, body_index=3,
                              system_id=71456, reserved=0))

    def test_system_is_18_bits_not_unmasked_upper_word(self):
        value = (31 << 59) | (0x3ffff << 41) | (63 << 35) | (3 << 32)
        r = unpack_world_key(value)
        self.assertEqual((r['system_id'], r['body_index'], r['tag'], r['reserved']),
                         (0x3ffff, 63, 3, 31))
        with self.assertRaisesRegex(ValueError, 'UNSUPPORTED'):
            qualified_grid(value)

    def test_invalid_and_noninteger_rejected(self):
        for value in (-1, 1 << 64, True, 1.0):
            with self.assertRaisesRegex(ValueError, 'UINT64'):
                unpack_world_key(value)
        with self.assertRaisesRegex(ValueError, 'INVALID'):
            unpack_world_key((1 << 64)-1)

    def test_tag_and_axes_not_silently_wrapped(self):
        for value in (4 << 32, 49152, 49152 << 16):
            with self.assertRaises(ValueError):
                qualified_grid(value)
        r = qualified_grid((3 << 32) | (100 << 16) | 200)
        self.assertEqual((r['tag'], r['x'], r['y']), (3, 200, 100))

    def test_unit3_requires_exact_closure_and_valid_count(self):
        # Tag3, count1, one uint16 string index, length12, key and checksum.
        fixture = bytes.fromhex('03000000 04 0700 0c000000 '
                                'e0288052790eb202 78563412')
        row = find_unit3_context(fixture, 0, len(fixture))
        self.assertEqual((row['start'], row['strings'], row['checksum']),
                         (11, 1, 0x12345678))
        self.assertEqual((row['x'], row['y'], row['system_id']),
                         (10464, 21120, 88327))
        for malformed in (fixture[:-1], fixture+b'\0',
                          fixture[:4]+b'\x03'+fixture[5:],
                          fixture[:7]+b'\xff'*4+fixture[11:]):
            with self.assertRaisesRegex(ValueError, 'ENVELOPE_NOT_UNIQUE'):
                find_unit3_context(malformed, 0, len(malformed))

    def test_unit3_cannot_escape_caller_region(self):
        with self.assertRaisesRegex(ValueError, 'ENVELOPE_BOUNDS'):
            find_unit3_context(b'1234', -1, 4)
        with self.assertRaisesRegex(ValueError, 'ENVELOPE_BOUNDS'):
            find_unit3_context(b'1234', 0, 5)

    def test_descriptor_legacy_token_width_and_string_budget(self):
        # Explicitly authored numeric fixture: one Kreet descriptor with a
        # three-byte legacy token and a following unrelated sentinel byte.
        prefix = bytes.fromhex('e0288052790eb202 78563412 01000000')
        descriptor = bytes.fromhex('9ff50300 e0288052790eb202 812345')
        buffer = prefix+descriptor+b'\x7f'
        context = dict(start=0, length=len(buffer), strings=2)
        rows, end = unit3_world_descriptors(buffer, context)
        self.assertEqual((end, buffer[end]), (31, 0x7f))
        self.assertEqual((rows[0]['world_token'], rows[0]['body']),
                         ('812345', '0003F59F'))
        for bad in (dict(context, strings=1), dict(context, length=30)):
            with self.assertRaisesRegex(ValueError, 'DESCRIPTOR_BOUNDS'):
                unit3_world_descriptors(buffer, bad)


if __name__ == '__main__':
    unittest.main()
