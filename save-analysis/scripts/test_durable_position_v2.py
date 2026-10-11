"""SPDX-License-Identifier: GPL-3.0-or-later
Independent instruction-derived boundary expectations, not retail runtime oracles.
Pure offline tests; no target effects or original fixture writes.
"""
import copy
import json
from pathlib import Path
import struct
import unittest

from durable_position_v2 import N, reflect_packed, reproduce
from durable_position_model import reconstruct

ROOT = Path(__file__).resolve().parents[2]


class V2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.inputs = json.loads((ROOT/'docs/experiments/engine-oracle/inputs.json').read_text())
        cls.frozen = json.loads((ROOT/'docs/experiments/engine-oracle/predictions.json').read_text())

    def case(self, tag, x, y, dx=0, dy=0):
        data = copy.deepcopy(self.inputs[0])
        key = int(data['descriptor']['key'], 16)
        data['descriptor']['key'] = f'{(key & ~((1 << 35)-1)) | tag << 32 | y << 16 | x:016x}'
        data['frame'] = 0x0b
        data['position_hex'] = struct.pack('<3f', dx, dy, 0).hex()
        data['compensation_hex'] = '00'*12
        return data

    def test_all_frozen_outputs_and_v1_unchanged(self):
        self.assertEqual(len(self.inputs), 23)
        self.assertEqual([reconstruct(i) for i in self.inputs], self.frozen)
        for i, old in zip(self.inputs, self.frozen):
            r = reproduce(i)
            self.assertEqual(r['center_hex'], old['center_hex'])
            self.assertEqual([r['native_cell']['tag'], *r['native_cell']['xy']], old['cell'])
            self.assertEqual(r['residual'], old['residual'])

    def test_reflected_origin_instruction_expectations(self):
        for tag in (2, 3):
            r = reproduce(self.case(tag, 123, 456, 100, 0))
            self.assertEqual(r['source_origin']['native'], [tag, 49028, 48695])
            self.assertEqual(r['native_cell']['xy'], [49029, 48695])
            self.assertEqual(r['packed_cell'], [tag, 122, 456])

    def test_all_tag_and_crossing_branches(self):
        for tag in range(4):
            for dx, dy, xor_tag, xy in [(0,0,0,[0,0]),(-100,0,1,[N-1,0]),
                    (0,-100,3,[0,N-1]),(-100,-100,2,[N-1,N-1]),
                    (100,100,0,[1,1]),(-N*100,0,0,[0,0])]:
                px, py = (N-1, N-1) if tag in (2,3) else (0,0)
                r = reproduce(self.case(tag, px, py, dx, dy))
                self.assertEqual(r['native_cell']['tag'], tag ^ xor_tag)
                self.assertEqual(r['native_cell']['xy'], xy)

    def test_float32_floor_not_double_division(self):
        r = reproduce(self.case(0, 10, 10, -0.25, 99.99999237060547))
        self.assertEqual(r['trace']['floor'], [-1, 0])
        self.assertEqual(r['residual'][:2], [99.75, 99.99999237060547])

    def test_unknown_site_does_not_substitute_origin(self):
        i = self.case(0, 10, 20)
        i['frame'] = 0x2b
        i['site_cell'] = None
        r = reproduce(i)
        self.assertIsNone(r['native_cell'])
        self.assertIsNone(r['selected_base'])
        self.assertEqual(r['stages']['cell'], 'UNKNOWN')

    def test_reject_unqualified_site_domain_and_scale(self):
        i = self.case(0, 10, 20)
        i['frame'] = 0x2b
        i['site_cell'] = [2, 10, 20]
        with self.assertRaisesRegex(ValueError, 'SITE_CELL_DOMAIN'):
            reproduce(i)
        i = self.case(0, 10, 20, 2**-126, 0)
        with self.assertRaisesRegex(ValueError, 'SCALE_SUBNORMAL'):
            reproduce(i)

    def test_partial_frame_type_cannot_bypass_validation(self):
        for frame in (43.0, True, '43', None):
            i = self.case(0, 10, 20)
            i['frame'] = frame
            i['site_cell'] = None
            with self.assertRaisesRegex(ValueError, 'UNSUPPORTED_OR_DISABLED_SAVED_FRAME'):
                reproduce(i)

    def test_domain_reflection_involution(self):
        for tag in range(4):
            for xy in [(0,0), (N-1,N-1), (123,456)]:
                self.assertEqual(reflect_packed(*reflect_packed(tag,*xy)), (tag,*xy))


if __name__ == '__main__':
    unittest.main()
