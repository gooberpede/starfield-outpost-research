# SPDX-License-Identifier: GPL-3.0-or-later
"""Synthetic arithmetic and falsification controls; no native oracle claim."""
import copy
from pathlib import Path
import unittest

from fallback_provenance import audit, r
from audit_activated_grid import offset
from durable_position_v2 import reflect_packed
from identity_provenance import queued_static_ids


class Arithmetic(unittest.TestCase):
    def test_static_array_and_inline_record_ids(self):
        rows = [{'token': '43f7e8', 'saved_record_formid': '0003F7E8'},
                {'token': '000001', 'saved_record_formid': '0013D13C'},
                {'token': '800001', 'saved_record_formid': 'FF02380F'},
                {'token': '000002', 'saved_record_formid': '01007145'}]
        self.assertEqual(queued_static_ids([{'queue_leads': rows}]), {0x3f7e8, 0x13d13c})

    def test_hand_worked_branches(self):
        # Literal expectations from integer examples and static tag transitions.
        # No expected value is computed by offset or its underlying implementation.
        cases = [
            ((1, 10464, 21141, 0, 0), (1, 10464, 21141)),
            ((1, 11, 191, 1, 1), (1, 12, 192)),
            ((1, 100, 100, -1, -2), (1, 99, 98)),
            ((1, 49151, 10, 1, 0), (0, 0, 10)),
            ((1, 0, 10, -1, 0), (0, 49151, 10)),
            ((1, 10, 49151, 0, 1), (2, 10, 0)),
            ((1, 10, 0, 0, -1), (2, 10, 49151)),
            ((1, 49151, 49151, 1, 1), (3, 0, 0)),
            ((1, 0, 0, -1, -1), (3, 49151, 49151)),
            # C IDIV remainder: entire-axis turns are discarded before carry.
            ((1, 10, 20, 49152, -49152), (1, 10, 20)),
            ((1, 10, 20, -49153, 49153), (1, 9, 21)),
        ]
        for inp, expected in cases:
            with self.subTest(inp=inp):
                self.assertEqual(offset(*inp), expected)

    def test_reflected_domain_and_rejection(self):
        self.assertEqual(reflect_packed(2, 0, 49151), (2, 49151, 0))
        self.assertEqual(reflect_packed(3, 12, 192), (3, 49139, 48959))
        for values in [(4, 0, 0, 0, 0), (1, -1, 0, 0, 0), (1, 49152, 0, 0, 0)]:
            with self.assertRaises(ValueError):
                offset(*values)


class CapturedControls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Local immutable evidence only; no proprietary fixture copied into Git.
        import json
        cls.session = Path('.local-work/native-oracle-live/session-36756-82447437')
        cls.events, _ = r.records(cls.session)
        cls.base = int(json.loads((cls.session / 'ready.json').read_text())['module_base'], 16)

    def test_observed_and_counterexamples(self):
        result = audit(self.events, self.base)
        self.assertEqual(result['identity']['base_formid'], '00007145')
        self.assertEqual(result['route']['grid'][0]['native_grid'], [1, 10464, 21141])
        self.assertEqual(result['native_nonzero_observations'], 0)
        self.assertNotEqual(result['route']['grid'][0]['native_grid'], [1, 10467, 21144])
        self.assertFalse(result['route']['selected_reference_bound'])

    def test_missing_duplicate_and_changed_evidence_fail(self):
        mutations = []
        mutations.append([e for e in self.events if e['kind'] != 32])
        mutations.append(self.events + [next(e for e in self.events if e['kind'] == 33)])
        changed = copy.deepcopy(self.events)
        next(e for e in changed if e['kind'] == 34)['thread'] += 1
        mutations.append(changed)
        for events in mutations:
            with self.assertRaises((ValueError, TypeError)):
                audit(events, self.base)


if __name__ == '__main__':
    unittest.main()
