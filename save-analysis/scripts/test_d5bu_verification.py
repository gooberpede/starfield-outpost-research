# SPDX-License-Identifier: GPL-3.0-or-later
"""Synthetic refusal and boundary tests for the finite D5BU adapters."""
import json
from pathlib import Path
import struct
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import verify_d5bu_cargo as cargo
import verify_d5bu_controls as controls
import verify_d5bu_fabricators as fabricators
import verify_d5bu_geography as geography


class FiniteReaderTests(unittest.TestCase):
    def test_sd2_unsupported_buffer(self):
        for version in (0, 152, 154, 255):
            data = bytearray(21)
            data[16:21] = b'\x1b\x00\x00\x00' + bytes([version])
            with self.assertRaisesRegex(ValueError, 'UNSUPPORTED_FORMAT_OR_BUFFER'):
                controls.fixture_records(data, False)

    def test_sd2_zero_and_unrelated_type(self):
        record = dict(form_type=0x4b, token='800001')
        with (patch.object(controls, 'context', return_value=(str, 1)),
              patch.object(controls, 'typed_records', return_value=iter([record]))):
            self.assertEqual(controls.fixture_records(b'', True), [])

    def test_sd2_inline_base_required(self):
        record = dict(form_type=0x4a, token='800001', refs=[controls.FIXTURE])
        with (patch.object(controls, 'context', return_value=(str, 1)),
              patch.object(controls, 'typed_records', return_value=iter([record])),
              patch.object(controls, 'initial_prefix', return_value=dict(base_token=None))):
            self.assertEqual(controls.fixture_records(b'', False), [])

    def test_ship_extra33_refusals(self):
        self.assertEqual(len(cargo.refuse_ship_extensions()), 3)

    def test_ship_extra33_positive_and_unknown(self):
        record = dict(end=4, refs=['one', 'two'])
        view = dict(status='UNSUPPORTED_EXTRA', extras=[dict(type='33', offset=0)],
                    next_reference_index=0, count=1)
        parsed = cargo.ship_instance_tail(b'3\x02\x08\x00', record, view, str)
        self.assertEqual(parsed['status'], 'COUNT_CLOSED')
        self.assertEqual(parsed['next_reference_index'], 2)
        self.assertEqual(parsed['body_end'], 4)
        for tag in (0x30, 0xd9):
            record['end'] = 5
            view['count'] = 2
            with self.assertRaisesRegex(ValueError, f'C1_SHIP_TAIL_EXTRA_0x{tag:x}'):
                cargo.ship_instance_tail(b'3\x02\x08\x00' + bytes([tag]), record, view, str)

    def test_graph_storage_cargo_cycle_and_decoy(self):
        fabricators.graph_control()

    def test_graph_empty_and_unknown(self):
        self.assertEqual(fabricators.upstream('start', {'need'}, {}, {}, {}), ([], {}, 0))
        paths, boundaries, cycles = fabricators.upstream(
            'start', {'need'}, {}, {'start': ['unknown']}, {})
        self.assertEqual((paths, boundaries, cycles), ([], {'unknown': 1}, 0))

    def test_positive_area_tangent_and_negative_floor(self):
        cells = geography.enumerate_cells(150, 150)
        points = {(x, y) for x, y, _ in cells}
        self.assertIn((1, 1), points)
        self.assertNotIn((3, 1), points)
        self.assertTrue(any(x == -2 for x, _, _ in geography.enumerate_cells(-.1, 0)))
        self.assertTrue(any(x == 2 for x, _, _ in geography.enumerate_cells(50.00001, 50)))
        self.assertFalse(any(x == 2 for x, _, _ in geography.enumerate_cells(49.99999, 50)))

    def test_map_version_refusal(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / 'synthetic.biom'
            source.write_bytes(struct.pack('<BBI', 4, 0, 0))
            with self.assertRaises(AssertionError):
                geography.readmap(source)

    def test_output_is_exclusive(self):
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder) / 'receipt.json'
            geography.write(target, dict(result='preserve'))
            original = target.read_bytes()
            with self.assertRaises(FileExistsError):
                geography.write(target, dict(result='overwrite'))
            self.assertEqual(target.read_bytes(), original)
            self.assertEqual(json.loads(original), dict(result='preserve'))

    def test_member_wrong_identity_refuses_before_decode(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / 'synthetic.sfs'
            source.write_bytes(b'wrong')
            with self.assertRaisesRegex(ValueError, 'ORIGINAL_IDENTITY'):
                with controls.decode_member(64, source, folder, {'B4-F064': (0, '0'*64)}):
                    self.fail('Decoder entered')


if __name__ == '__main__':
    unittest.main(verbosity=2)
