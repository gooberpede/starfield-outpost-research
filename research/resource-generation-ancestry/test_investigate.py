# SPDX-License-Identifier: GPL-3.0-or-later
"""Offline comparison discrimination tests; stdlib only, no file writes."""
import copy
import struct
import unittest
from investigate import signature, compare


class Discrimination(unittest.TestCase):
    def test_exact_words_bound_order_and_identity(self):
        region = dict(resource='000057d4', source='test', cell=[1, 1],
                      points=[[1., 2., 0., 3.], [4., 5., 0., 6.]], native_bound=[2., 3., 0., 9.])
        observed = [dict(resource=region['resource'], signature=signature(region))]
        self.assertTrue(compare(observed, [region])['000057d4'])
        for change in ('point_bit', 'bound_bit', 'order', 'resource'):
            r = copy.deepcopy(region)
            if change == 'point_bit':
                r['points'][0][0] = struct.unpack('<f', struct.pack('<I', 0x3f800001))[0]
            elif change == 'bound_bit':
                r['native_bound'][0] = struct.unpack('<f', struct.pack('<I', 0x40000001))[0]
            elif change == 'order':
                r['points'].reverse()
            else:
                r['resource'] = '000057cf'
            with self.subTest(change=change):
                self.assertFalse(compare(observed, [r])['000057d4'])


if __name__ == '__main__':
    unittest.main()
