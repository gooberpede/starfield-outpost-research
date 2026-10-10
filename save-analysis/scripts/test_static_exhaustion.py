"""SPDX-License-Identifier: GPL-3.0-or-later
Independent identity-comparison rejection controls; no external inputs/effects.
"""
import copy
import unittest

from audit_static_exhaustion import compare_bodies


class IdentityControls(unittest.TestCase):
    def setUp(self):
        self.samples = [dict(metrics=dict(decoded_sha256='frozen'), extraction=dict(beacons=[
            dict(token='abc', saved_disabled=False, name_for_comparison=[dict(text='Site')],
                 points=[dict(body_formid=1)], cache=[dict(system_id=2, body_options=[dict(formid=1)])])]))]
        self.frozen = dict(decoded_sha256='frozen')
        self.manual = dict(networks=[dict(network=dict(outposts=[dict(name='Site', bodyId='00000001', systemId='2')]))])

    def test_direct_cache_and_system_are_independent(self):
        b = self.samples[0]['extraction']['beacons'][0]
        b['cache'][0]['body_options'][0]['formid'] = 3
        row = compare_bodies(self.samples, self.frozen, self.manual)[0]
        self.assertTrue(row['direct_equal'])
        self.assertFalse(row['cache_equal'])
        self.assertTrue(row['system_equal'])

    def test_same_name_different_body_is_not_confirmation(self):
        self.manual['networks'][0]['network']['outposts'][0]['bodyId'] = '00000004'
        row = compare_bodies(self.samples, self.frozen, self.manual)[0]
        self.assertFalse(row['direct_equal'])
        self.assertFalse(row['cache_equal'])

    def test_duplicate_frozen_sample_rejected(self):
        with self.assertRaisesRegex(ValueError, 'FROZEN_SAMPLE_NOT_UNIQUE'):
            compare_bodies(self.samples*2, self.frozen, self.manual)

    def test_disabled_duplicate_cannot_supply_active_identity(self):
        b = copy.deepcopy(self.samples[0]['extraction']['beacons'][0])
        b['saved_disabled'] = True
        b['points'] = [dict(body_formid=9)]
        self.samples[0]['extraction']['beacons'].append(b)
        self.assertTrue(compare_bodies(self.samples, self.frozen, self.manual)[0]['direct_equal'])

    def test_two_active_same_names_rejected(self):
        self.samples[0]['extraction']['beacons'] *= 2
        with self.assertRaisesRegex(ValueError, 'NAME_JOIN_NOT_UNIQUE'):
            compare_bodies(self.samples, self.frozen, self.manual)


if __name__ == '__main__':
    unittest.main()
