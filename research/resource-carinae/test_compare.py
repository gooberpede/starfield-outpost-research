# SPDX-License-Identifier: GPL-3.0-or-later
"""Phase A comparator checks using closed synthetic receipts, never retail.

Reads qualification output selected by C2A_QUALIFICATION (default qualification05).
Writes nothing; tests exact bits, ordering, identity refusal and transfer joins.
"""
import copy
import json
import os
import struct
import unittest
from compare import ROOT, LOCAL, compare


class Comparison(unittest.TestCase):
    def rows(self, mode='good'):
        folder = LOCAL / os.environ.get('C2A_QUALIFICATION', 'qualification05') / mode
        return json.loads((folder / 'events.json').read_text())

    def prediction(self, rows):
        d = next(r for r in rows if 'decision' in r)
        raw = bytes.fromhex(d['geometry']['raw_region'])
        points = list(struct.iter_unpack('<4f', bytes.fromhex(d['geometry']['ordered_xyzw'])))
        return [dict(site='Carinae', regions=[dict(source='synthetic-source', cell=[3, 4],
                    resource='000057c7', points=points,
                    native_bound=struct.unpack_from('<4f', raw))])]

    def test_exact_is_not_source_identity(self):
        rows = self.rows()
        d = compare(rows, self.prediction(rows))['regions'][0]
        self.assertEqual(d['geometry_equality'], 'EXACT')
        self.assertEqual(d['source_frame_identity'], 'UNKNOWN')
        self.assertTrue(d['transfer_membership'])
        self.assertFalse(d['census_complete'])

    def test_point_bit_and_bound_bit_are_decisive(self):
        rows = self.rows()
        for field in ('points', 'native_bound'):
            p = self.prediction(rows)
            target = list(p[0]['regions'][0][field][0] if field == 'points' else p[0]['regions'][0][field])
            bits = struct.unpack('<I', struct.pack('<f', target[0]))[0]
            target[0] = struct.unpack('<f', struct.pack('<I', bits+1))[0]
            if field == 'points':
                p[0]['regions'][0][field][0] = target
            else:
                p[0]['regions'][0][field] = target
            self.assertEqual(compare(rows, p)['regions'][0]['geometry_equality'], 'NO_EXACT_MATCH')

    def test_point_order_and_resource_are_decisive(self):
        rows = self.rows('multi')
        p = self.prediction(rows)
        p[0]['regions'][0]['points'].reverse()
        self.assertEqual(compare(rows, p)['regions'][0]['geometry_equality'], 'NO_EXACT_MATCH')
        p = self.prediction(rows)
        p[0]['regions'][0]['resource'] = '000057c9'
        self.assertEqual(compare(rows, p)['regions'][0]['geometry_equality'], 'NO_EXACT_MATCH')

    def test_negative_and_corrupt_are_not_absence(self):
        for mode in ('wrong-workshop', 'wrong-cell', 'partial-page', 'invalid-procgen'):
            result = compare(self.rows(mode), [])
            self.assertFalse(result['regions'][0]['qualified'])
            self.assertEqual(result['regions'][0]['geometry_equality'], 'NOT_TESTED')
            self.assertFalse(result['missing_events_are_absence'])
        for mode in ('no-hit', 'retained-cache'):
            self.assertEqual(compare(self.rows(mode), [])['regions'], [])

    def test_transfer_requires_reference_frame_token_and_order(self):
        rows = self.rows()
        for field in ('binding_reference', 'updater_bp', 'updater_token', 'temporary_set', 'thread_lifetime', 'capture'):
            altered = copy.deepcopy(rows)
            t = next(r for r in altered if 'refresh_payload' in r)
            t[field] = 0
            self.assertFalse(compare(altered, [])['regions'][0]['transfer_membership'], field)

    def test_rejection_and_missing_transfer(self):
        self.assertFalse(compare(self.rows('reject'), [])['regions'][0]['transfer_membership'])
        rows = [r for r in self.rows() if 'refresh_payload' not in r]
        self.assertFalse(compare(rows, [])['regions'][0]['transfer_membership'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
