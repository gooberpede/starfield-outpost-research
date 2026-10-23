# SPDX-License-Identifier: GPL-3.0-or-later
"""Original synthetic C2D controls; no proprietary fixtures or target effects."""
import copy
import struct
import unittest
import zlib
from selector import eligible, predict, resolve_slot


class SelectionTests(unittest.TestCase):
    def setUp(self):
        self.m = dict(faces=[dict(values=[1, 2, 3, 1])])
        self.styles = {1: 7, 2: 8, 3: 0}
        self.registry = [None, dict(id=10, style=7), dict(id=99, style=9),
                         dict(id=20, style=7), dict(id=30, style=8)]
        self.targets = {(0, i, 255) for i in range(4)}

    def run_case(self, **change):
        values = dict(surface_seed=0x20201215, rotate=False, qualification={'registry': False})
        values.update(change)
        return predict(self.m, self.styles, self.registry, 118021, 8, self.targets, **values)

    def test_repeat_determinism_and_no_mutation(self):
        before = copy.deepcopy((self.m, self.registry))
        self.assertEqual(self.run_case(), self.run_case())
        self.assertEqual(before, (self.m, self.registry))

    def test_registry_order_changes_identity_without_changing_draw(self):
        before = self.run_case()['traces'][0]
        self.registry.reverse()
        after = self.run_case()['traces'][0]
        self.assertEqual(before['words'], after['words'])
        self.assertNotEqual(before['selected'], after['selected'])

    def test_null_unmatched_and_zero_style_are_ineligible(self):
        self.assertEqual(eligible(self.registry, 7), [10, 20])
        self.assertEqual(eligible(self.registry, 0), [])
        self.assertEqual(eligible(self.registry, 123), [])

    def test_single_and_empty_candidates_consume_no_selection_draw(self):
        t = self.run_case()['traces']
        self.assertEqual([len(r['words']) for r in t], [1, 0, 0, 1])
        self.assertEqual([r['draw_start'] for r in t], [0, 1, 1, 1])
        self.assertEqual(t[2]['selected'], '0x00000000')

    def test_crc_domain_and_operand_order(self):
        r = self.run_case()
        b = struct.pack('<III', 8, 118021, 0x20201215)
        self.assertEqual(r['seed'], zlib.crc32(b, 0xffffffff) ^ 0xffffffff)
        self.assertNotEqual(r['seed'], zlib.crc32(struct.pack('<III', 118021, 8, 0x20201215), 0xffffffff) ^ 0xffffffff)
        self.assertNotEqual(r['traces'][0]['words'], self.run_case(surface_seed=1)['traces'][0]['words'])

    def test_orientation_draws_shift_later_identity_stream(self):
        a, b = self.run_case(), self.run_case(rotate=True)
        self.assertEqual(a['traces'][0]['selected'], b['traces'][0]['selected'])
        self.assertNotEqual(a['traces'][-1]['words'][0], b['traces'][-1]['words'][0])
        self.assertEqual(b['draw_count'], a['draw_count'] + 6)

    def test_qualification_cannot_change_numeric_trace(self):
        a, b = self.run_case(), self.run_case(qualification={'registry': True})
        self.assertEqual(a['traces'], b['traces'])
        self.assertNotEqual(a['outcome'], b['outcome'])


class BlockTests(unittest.TestCase):
    def setUp(self):
        self.entries = [(0, 0)] * 256
        self.entries[6 * 16 + 7] = (40, 64)
        self.entries[6 * 16 + 6] = (50, 16)
        self.entries[5 * 16 + 6] = (60, 8)
        self.blocks = {40: {}, 50: {}, 60: {}}

    def test_single_backlink_accepts_typed_nonanchor(self):
        r = resolve_slot(self.entries, 6, 7, self.blocks)
        self.assertEqual((r['block'], r['slot'], r['flags']), (50, [6, 6], 16))
        self.assertFalse(r['used_fallback'])
        self.assertNotEqual(r['block'], 60)

    def test_anchor_does_not_translate(self):
        self.assertEqual(resolve_slot(self.entries, 5, 6, self.blocks)['block'], 60)

    def test_missing_or_wrong_type_needs_default(self):
        del self.blocks[50]
        self.assertEqual(resolve_slot(self.entries, 6, 7, self.blocks)['status'], 'UNKNOWN_DEFAULT_BLOCK')
        self.assertEqual(resolve_slot(self.entries, 6, 7, self.blocks, 60)['status'], 'RESOLVED_DEFAULT')
        self.assertEqual(resolve_slot(self.entries, 6, 7, self.blocks, 0)['status'], 'NO_CALLBACK_NULL_DEFAULT')

    def test_neighbour_translation_is_not_clamped(self):
        self.entries[0] = (40, 16)
        self.assertEqual(resolve_slot(self.entries, 0, 0, self.blocks)['status'], 'UNKNOWN_NEIGHBOUR_CHART')

    def test_unrepresented_nonzero_default_is_not_null(self):
        del self.blocks[50]
        r = resolve_slot(self.entries, 6, 7, self.blocks, 999)
        self.assertEqual(r['status'], 'UNKNOWN_DEFAULT_DEFINITION')
        self.assertEqual(r['default_block'], 999)
        self.assertNotEqual(r['status'], resolve_slot(self.entries, 6, 7, self.blocks, 0)['status'])


if __name__ == '__main__':
    unittest.main()
