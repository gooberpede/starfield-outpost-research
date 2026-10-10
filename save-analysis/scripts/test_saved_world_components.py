"""SPDX-License-Identifier: GPL-3.0-or-later
Independent malformed/ambiguous-context rejection controls. No external effects.
"""
import struct
import unittest

from saved_world_components import find_world_components


class ComponentControls(unittest.TestCase):
    def setUp(self):
        self.record = struct.pack('<5IB4i', 0x812345, 0x401234, 88327, 15,
                                  0x823456, 3, -1, 1, -2, 2)
        self.keys = {(88327, 15): '0003F59F'}
        self.descriptors = [dict(world_token='823456', body='0003F59F')]

    def parse(self, buffer, parents=None, descriptors=None):
        return find_world_components(buffer, 0, len(buffer), parents or {0x812345},
                                     self.keys, self.descriptors if descriptors is None else descriptors)

    def test_signed_bounds_and_nonzero_prefix(self):
        run = self.parse(b'prefix!'+self.record+bytes(4)+b'tail')
        self.assertEqual((run['start'], run['end']), (7, 48))
        row = run['rows'][0]
        self.assertEqual((row['xmin'], row['xmax'], row['ymin'], row['ymax']),
                         (-1, 1, -2, 2))

    def test_second_viable_run_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'RUN_NOT_UNIQUE'):
            self.parse(self.record+bytes(4)+b'junk'+self.record+bytes(4))

    def test_secondary_world_requires_independent_body_agreement(self):
        with self.assertRaisesRegex(ValueError, 'RUN_NOT_UNIQUE'):
            self.parse(self.record+bytes(4), descriptors=[dict(world_token='823456', body='0003F5A1')])

    def test_truncation_and_missing_parent_rejected(self):
        for buffer, parents in ((self.record+bytes(3), {0x812345}),
                                (self.record+bytes(4), {0x812345, 0x845678})):
            with self.assertRaisesRegex(ValueError, 'RUN_NOT_UNIQUE'):
                self.parse(buffer, parents)

    def test_duplicate_descriptor_is_not_silently_chosen(self):
        with self.assertRaisesRegex(ValueError, 'DUPLICATE_WORLD_DESCRIPTOR'):
            self.parse(self.record+bytes(4), descriptors=self.descriptors*2)


if __name__ == '__main__':
    unittest.main()
