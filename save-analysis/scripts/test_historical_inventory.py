"""Synthetic safety/classification tests, stdlib only, no game/save fixtures."""
import struct
import unittest
from unittest.mock import patch
import zlib
import inventory_historical_saves as inv


def container(raw):
    c = zlib.compress(raw)
    b = bytearray(80)
    b[:8] = b'BCPS\x01\0\0\0'
    for p, n in [(8, 72), (24, 80), (32, len(raw)), (48, 262144)]:
        struct.pack_into('<Q', b, p, n)
    b[68:72] = b'ZIP '
    struct.pack_into('<I', b, 72, len(c))
    b.extend(c)
    b.extend(bytes((-len(b)) % 16))
    return bytes(b)


class SafetyTests(unittest.TestCase):
    def test_physical_closure_and_transform(self):
        raw = b'SFS_SAVEGAME'+bytes(300)
        b = container(raw)
        frame, spans = inv.framing(b)
        self.assertEqual(frame['streams'], 1)
        self.assertEqual(inv.transform(b, spans, True), raw)
        for bad in (b[:71], b+b'\0', b[:8]+bytes(8)+b[16:], b[:-16]):
            with self.subTest(length=len(bad)), self.assertRaises(ValueError):
                inv.framing(bad)

    def test_integrity_and_output_bound(self):
        b = container(b'SFS_SAVEGAME'+bytes(300))
        _, spans = inv.framing(b)
        corrupt = bytearray(b)
        corrupt[83] ^= 255
        with self.assertRaises((ValueError, zlib.error)):
            inv.transform(corrupt, spans, True)
        with self.assertRaises(ValueError):
            inv.transform(b, [(80, spans[0][1], 12)], True)

    def test_metadata_version_scope(self):
        b = bytearray(25)
        b[:12] = b'SFS_SAVEGAME'
        def text(t):
            v = t.encode()
            return struct.pack('<H', len(v))+v
        b.extend(text('Control')+struct.pack('<I', 3)+text('Site')+text('0h')+text('HumanRace'))
        b.extend(bytes(30)+text('1.16.244.0')+text('1.14.74.0')+bytes(150)+text('1723076033.1.0.16'))
        m = inv.metadata(b)
        self.assertEqual([x['text'] for x in m['build_strings']], ['1.16.244.0', '1.14.74.0'])
        self.assertEqual(m['level_candidate']['value'], 3)

    def test_empty_collection_positive_counterexample(self):
        f = dict(beacon_windows=[dict(names=[dict(name='Control')])], beacon_count=1,
                 marker_count=0, beacon_collection_count=0)
        self.assertEqual(inv.classify(f, ['1.16.244.0']), 'OUTPOSTS_CONFIRMED_PRESENT')

    def test_absence_requires_all_gates(self):
        f = dict(beacon_windows=[], beacon_count=0, marker_count=0, beacon_collection_count=0,
                 errors=[], animation_string_count=0, keyed_groups=1, endpoints=1)
        self.assertEqual(inv.classify(f, ['1.16.244.0']), 'NO_ACTIVE_OUTPOSTS_SUPPORTED')
        self.assertEqual(inv.classify(dict(f, keyed_groups=0, endpoints=0), ['1.16.244.0']), 'NO_ACTIVE_OUTPOSTS_SUPPORTED')
        for versions in ([], ['1.14.74.0'], ['1.16.244.0', '1.14.74.0']):
            self.assertEqual(inv.classify(f, versions), 'INDETERMINATE')
        for key, value in [('errors', ['unsupported']), ('animation_string_count', 2),
                           ('endpoints', 2), ('beacon_collection_count', None)]:
            with self.subTest(key=key):
                self.assertEqual(inv.classify(dict(f, **{key: value}), ['1.16.244.0']), 'INDETERMINATE')
        self.assertEqual(inv.classify(None, ['1.16.244.0']), 'INDETERMINATE')

    def test_residual_marker_blocks_absence(self):
        f = dict(beacon_windows=[], beacon_count=0, marker_count=1, beacon_collection_count=0)
        self.assertEqual(inv.classify(f, ['1.16.244.0']), 'POSSIBLE_RESIDUAL_OR_INACTIVE_STATE')

    def test_windows_require_prefix_token_repeat_and_base(self):
        b = bytearray(100)
        b[10:14] = bytes.fromhex('3a822c5d')
        b[25:31] = bytes.fromhex('6c60e9822c5d')
        self.assertEqual(len(inv.candidate_windows(b, 0, len(b), '6c60e9', 0x3a)), 1)
        b[26] ^= 1
        self.assertEqual(inv.candidate_windows(b, 0, len(b), '6c60e9', 0x3a), [])

    def test_low_disk_guard(self):
        with patch.object(inv.shutil, 'disk_usage', return_value=type('Space', (), {'free': 39_999_999_999})()):
            with self.assertRaises(RuntimeError):
                inv.guard()

    def test_location_probe_variable_index_count(self):
        from probe_inventory_locations import probe
        raw = bytearray(200)
        raw[40:44] = struct.pack('<2H', 1, 2)
        raw[49:61] = struct.pack('<3f', 122.5, 277.25, 18.0)
        entries = [dict(index=0, text='', text_offset=100), dict(index=1, text='Site Outpost 1', text_offset=102),
                   dict(index=2, text='OBJ_Outpost_Beacon_On_LP', text_offset=116)]
        f = dict(directory=dict(regions=dict(region_R3=[0, 200])),
                 beacon_windows=[dict(token='822c5d', offset=0, names=[])])
        result = probe(raw, f, entries)
        self.assertEqual(result[0]['names'][0]['method'], 'animation_predecessor_PROVISIONAL')
        self.assertEqual(result[0]['probes'][0]['offset'], 49)
        self.assertEqual(result[0]['probes'][0]['values'], [122.5, 277.25, 18.0])

    def test_unsupported_inspection_cannot_be_absence_or_corruption(self):
        p = type('Input', (), {'read_bytes': lambda self: b'unknown framing'})()
        source = dict(size=15, sha256=inv.sha(b'unknown framing'))
        with patch.object(inv, 'identity', return_value=source):
            row = inv.inspect(p, 'SYNTHETIC')
        self.assertEqual(row['status'], 'UNSUPPORTED')
        self.assertEqual(row['classification'], 'INDETERMINATE')
        self.assertNotEqual(row['status'], 'MALFORMED_CONFIRMED')


if __name__ == '__main__':
    unittest.main()
