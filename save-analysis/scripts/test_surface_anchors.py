"""SPDX-License-Identifier: GPL-3.0-or-later
Original synthetic SOR-EXP-0013 checks; no game/source fixtures.
"""
import math
from pathlib import Path
import struct
import tempfile
import unittest
import zlib

from inspect_outpost_definitions import esm_records
from research_surface_anchors import angles, spherical, audit_pair, fixed_points


class SurfaceTests(unittest.TestCase):
    def test_axes_and_invalid_direction(self):
        for xyz, expected in [((1, 0, 0), (0, 0)), ((0, 1, 0), (math.pi/2, 0)),
                              ((0, 0, 1), (0, math.pi/2)), ((0, 0, -1), (0, -math.pi/2))]:
            self.assertEqual(angles(*xyz), expected)
        for xyz in [(0, 0, 0), (math.inf, 0, 1), (0, math.nan, 1)]:
            with self.assertRaises(ValueError): angles(*xyz)

    def test_wrap_and_precision(self):
        for lon in [-math.pi, -2.8, 0, 1.4, math.pi, 8*math.pi+.1]:
            for lat in [-math.pi/2, -.5, 0, 1.1, math.pi/2]:
                p = audit_pair(struct.pack('<2d', lon, lat))
                self.assertLess(p['roundtrip_error_rad'], 2e-15)
                self.assertLess(p['norm_error'], 3e-16)
        with self.assertRaises(ValueError): spherical(0, 2)
        with self.assertRaises(ValueError): audit_pair(b'\0'*15)
        with self.assertRaises(ValueError): audit_pair(struct.pack('<2d', math.nan, 0))

    def test_fixed_records_repetition_compression_and_order(self):
        def sub(t, b): return t+struct.pack('<H', len(b))+b
        with tempfile.TemporaryDirectory() as td:
            path = Path(td)/'synthetic.esm'; data = b''
            for i, (fid, world) in enumerate([(0x3f5a1, 0x1251b), (0x5e2b6, 0x27cfa2), (0x3f59a, 0x2cfc4a)]):
                raw = sub(b'CNAM', struct.pack('<ddI', .4, 2.3, world))
                raw += sub(b'BDST', b'')+sub(b'CNAM', b'\x02')
                payload = struct.pack('<I', len(raw))+zlib.compress(raw) if i else raw
                data += b'PNDT'+struct.pack('<III', len(payload), 0x40000 if i else 0, fid)+b'\0'*8+payload
            path.write_bytes(data)
            fs = list(esm_records(path, {b'PNDT'}, repeated=True))[0][1]
            self.assertEqual([t for t, _ in fs], [b'CNAM', b'BDST', b'CNAM'])
            self.assertEqual(list(esm_records(path, {b'PNDT'}))[0][1][b'CNAM'], b'\x02')
            rows = fixed_points(path)
            self.assertEqual(len(rows), 3)
            for row in rows:
                self.assertEqual((row['longitude_rad'], row['latitude_rad']), (2.3, .4))
            self.assertIsNotNone(rows[0]['pair_file_offset'])
            self.assertIsNone(rows[1]['pair_file_offset'])
            path.write_bytes(data[:-1])
            with self.assertRaises(ValueError): fixed_points(path)


if __name__ == '__main__': unittest.main()
