"""Original synthetic regression tests; no corpus, files or live effects."""
import struct
import unittest
from outpost_membership import token_value, initial_prefix, extra_prefix
from inspect_outpost_definitions import subrecords


def fixture(case=5, flags=1, saved=0x400408, shape=0):
    token = '800001'
    refs = ['400123', '6c60e9', token] if case == 5 else ['400123', token]
    b = b''
    if case in (4, 5, 6):
        b = bytes([shape]) + struct.pack('<3f', 1, 2, 3)
        b += b'\0' * (4 * sum(bool(shape & (1 << i)) for i in range(3)))
        if not shape & 0x18:
            b += b'\0'
        if case == 6:
            refs = ['400123', '800002', token]
            b += struct.pack('<2h', -1, 3)
    else:
        refs = ['800002', token]
    if flags & 1:
        b += struct.pack('<IH', saved, 0x40)
    return b, dict(token=token, refs=refs, flags=flags, body=0, end=len(b))


class MembershipTests(unittest.TestCase):
    def test_reference_domains_and_bounds(self):
        self.assertEqual(token_value('000001', [0x0302b256]), 0x0302b256)
        self.assertEqual(token_value('6c60e9', []), 0x2c60e9)
        self.assertEqual(token_value('82c210', []), 0xff02c210)
        self.assertEqual(token_value('000000', []), 0)
        for t in ['000002', 'c00000']:
            with self.assertRaises(ValueError):
                token_value(t, [0x123])

    def test_all_initial_cases(self):
        for case in [4, 5, 6, 7]:
            b, r = fixture(case)
            p = initial_prefix(b, r, case)
            self.assertEqual(p['form_prefix_end'], len(b))
            self.assertFalse(p['disabled'])
            self.assertEqual(p['base_token'], '6c60e9' if case == 5 else None)
            if case == 6:
                self.assertEqual(p['placement_indices'], [-1, 3])

    def test_omission_is_not_false(self):
        b, r = fixture(6, flags=0x92018200)
        p = initial_prefix(b, r, 6)
        self.assertIsNone(p['disabled'])
        self.assertIsNone(p['deleted'])
        self.assertIsNone(p['saved_form_flags'])

    def test_disabled_and_incidental_deleted_are_distinct(self):
        for flags, disabled, deleted in [(0x800, True, False), (0x20, False, True), (0, False, False)]:
            b, r = fixture(saved=flags)
            p = initial_prefix(b, r, 5)
            self.assertEqual((p['disabled'], p['deleted']), (disabled, deleted))

    def test_transform_shapes_and_self_queue(self):
        for shape in [0, 7, 0x18, 0x1f]:
            b, r = fixture(shape=shape)
            self.assertEqual(initial_prefix(b, r, 5)['form_prefix_end'], len(b))
        r['refs'][2] = '800099'
        with self.assertRaisesRegex(ValueError, 'SELF_REFERENCE_MISMATCH'):
            initial_prefix(b, r, 5)
        b, r = fixture()
        r['end'] -= 1
        with self.assertRaises(ValueError):
            initial_prefix(b, r, 5)

    def test_promoted_player_reference_is_not_owner(self):
        b = bytes([4, 0x84, 4, 0x01])
        r = dict(body=0, end=len(b), flags=0x02000000, refs=['400014'])
        p = dict(form_prefix_end=0, next_reference_index=0)
        x = extra_prefix(b, r, p)
        self.assertEqual(x['promoted_references'][0]['token'], '400014')
        self.assertIsNone(x['ownership'])
        self.assertTrue(x['complete'])

    def test_version_gate_and_empty_arrays(self):
        p = dict(form_prefix_end=0, next_reference_index=0)
        b = bytes([8, 0x9c]) + struct.pack('<I', 3) + bytes([0xbc])
        r = dict(end=len(b), flags=0x02000000, refs=[])
        self.assertIsNone(extra_prefix(b, r, p)['workshop_offset'])
        self.assertIsNone(extra_prefix(b, r, p, 0x50)['workshop_offset'])
        self.assertEqual(extra_prefix(b, r, p, 0x89)['workshop_offset'], 6)
        b = bytes([12, 0x4c, 0, 0x80, 0, 0xbc])
        r['end'] = len(b)
        self.assertEqual(extra_prefix(b, r, p)['workshop_offset'], 5)
        b = bytes([4, 0x80, 4])
        r['end'] = len(b)
        self.assertIn('NONEMPTY', extra_prefix(b, r, p)['stop_reason'])

    def test_extra_bounds_and_unknown_stop(self):
        p = dict(form_prefix_end=0, next_reference_index=0)
        r = dict(end=3, flags=0x02000000, refs=[])
        with self.assertRaisesRegex(ValueError, 'QUEUE_EXHAUSTED'):
            extra_prefix(bytes([4, 0x84, 4]), r, p)
        self.assertEqual(extra_prefix(bytes([4, 0xda, 0]), r, p)['stop_reason'], 'EXTRA_TYPE_DA_NOT_DECODED')

    def test_esm_subrecord_bounds(self):
        self.assertEqual(list(subrecords(b'NAME\x04\x00abcd')), [(b'NAME', b'abcd')])
        self.assertEqual(list(subrecords(b'XXXX\x04\x00\x04\x00\x00\x00NAME\x00\x00abcd')), [(b'NAME', b'abcd')])
        for b in [b'NAME', b'NAME\x04\x00abc', b'XXXX\x03\x00abcd']:
            with self.assertRaises(ValueError):
                list(subrecords(b))


if __name__ == '__main__':
    unittest.main()
