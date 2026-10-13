# SPDX-License-Identifier: GPL-3.0-or-later
"""Frozen-input association and falsification controls; offline only."""
import copy
import json
import unittest
from audit import ROOT, saved_cases


class SavedOperands(unittest.TestCase):
    def setUp(self):
        folder = ROOT / 'docs/experiments/engine-oracle'
        self.inputs = json.loads((folder/'inputs.json').read_bytes())
        self.predictions = json.loads((folder/'predictions.json').read_bytes())

    def test_nonzero_is_saved_evidence_not_native(self):
        rows = saved_cases(self.inputs, self.predictions)
        self.assertEqual(rows[0]['floor'], [1, 2])
        self.assertEqual(rows[1]['floor'], [3, 24])
        self.assertEqual(sum(r['nonzero'] for r in rows), 7)
        self.assertEqual(sum(r['negative'] for r in rows), 1)
        self.assertTrue(all('NO NATIVE OUTPUT' in r['evidence'] for r in rows))

    def test_reordered_equal_centers_do_not_supply_identity(self):
        predictions = copy.deepcopy(self.predictions)
        # Save25/26 SOR-002 have equal centers/cells but different saved identity.
        predictions[0], predictions[2] = predictions[2], predictions[0]
        with self.assertRaisesRegex(ValueError, 'frozen_identity'):
            saved_cases(self.inputs, predictions)

    def test_fitted_prediction_is_rejected(self):
        predictions = copy.deepcopy(self.predictions)
        predictions[1]['cell'][1] -= 3
        with self.assertRaisesRegex(ValueError, 'frozen_prediction_changed'):
            saved_cases(self.inputs, predictions)

    def test_dropped_case_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'frozen_count'):
            saved_cases(self.inputs[:-1], self.predictions)


if __name__ == '__main__':
    unittest.main()
