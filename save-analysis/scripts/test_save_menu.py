"""SPDX-License-Identifier: GPL-3.0-or-later
Original synthetic fixtures only; reads/writes temporary test files, no game.
"""
import contextlib
import datetime as dt
import io
import json
import os
from pathlib import Path
import struct
import tempfile
import unittest
import zlib

import save_menu as sm


def fixture(name='Test Character', location='Test - Outpost', level=4, play='0d.2h.31m.0 days.2 hours.31 minutes'):
    b = bytearray(b'SFS_SAVEGAME'.ljust(25, b'\0'))
    struct.pack_into('<I', b, 16, 27)
    def string(text):
        encoded = text.encode('utf-8')
        b.extend(struct.pack('<H', len(encoded)) + encoded)
    string(name)
    b.extend(struct.pack('<I', level))
    for text in (location, play, 'HumanRace'):
        string(text)
    b.extend(bytes(10) + struct.pack('<Q', 134360149444202448))
    b.extend(bytes(100))
    compressed = zlib.compress(b)
    h = bytearray(80)
    h[:8] = b'BCPS\1\0\0\0'
    for p, n in ((8, 72), (24, 80), (32, len(b)), (48, sm.BLOCK)):
        struct.pack_into('<Q', h, p, n)
    h[68:72] = b'ZIP '
    struct.pack_into('<I', h, 72, len(compressed))
    out = h + compressed
    out.extend(bytes((-len(out)) % 16))
    return bytes(out)


class SaveMenuTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.zone = sm.fixed_zone('+11:00')
        self.ns = 1791541342000000000

    def tearDown(self):
        self.tmp.cleanup()

    def save(self, filename='Save25_fixture.sfs', **kw):
        p = self.root / filename
        p.write_bytes(fixture(**kw))
        os.utime(p, ns=(self.ns, self.ns))
        return p

    def inspect(self, p, **kw):
        return sm.inspect(dict(path=str(p), **kw), self.zone, '+11:00')

    def test_header_and_timestamp(self):
        r = self.inspect(self.save(), label='Save25')
        sm.instructions([r])
        self.assertEqual(r['status'], 'OK')
        self.assertTrue(r['preserved'])
        self.assertEqual(r['fields']['timestamp']['value'], '10/9/26, 9:22:22 PM')
        self.assertEqual(r['fields']['playtime']['value'], '2h 31m')
        self.assertIn('not screenshot-verified', r['instruction'])
        self.assertNotEqual(r['raw_metadata']['header_filetime_candidate']['utc_candidate'], '2026-10-09T10:22:22+00:00')

    def test_absent_optional(self):
        r = self.inspect(self.save(location='', level=0, play='inconnu'))
        sm.instructions([r])
        self.assertEqual(r['status'], 'OK')
        self.assertEqual(r['fields']['location']['confidence'], 'UNKNOWN')
        self.assertIsNone(r['fields']['playtime']['value'])
        self.assertNotIn('Level', r['instruction'])

    def test_absent_character(self):
        r = self.inspect(self.save(name=''))
        sm.instructions([r])
        self.assertEqual(r['status'], 'INCOMPLETE')
        self.assertTrue(r['instruction'].startswith('No load instruction'))

    def test_copied_mtime_uses_hash_bound_source(self):
        p = self.save()
        source = sm.identity(p)
        os.utime(p, ns=(0, 0))
        r = self.inspect(p, source=source)
        self.assertEqual(r['fields']['timestamp']['value'], '10/9/26, 9:22:22 PM')
        source['sha256'] = 'wrong'
        self.assertEqual(self.inspect(p, source=source)['status'], 'ERROR')

    def test_missing_source_timestamp_never_falls_back_to_copy(self):
        p = self.save()
        source = sm.identity(p)
        del source['mtime_ns']
        self.assertEqual(self.inspect(p, source=source)['status'], 'INCOMPLETE')

    def test_multiple_characters_and_collision(self):
        a = self.inspect(self.save('a.sfs', name='Alpha'))
        b = self.inspect(self.save('b.sfs', name='Beta'))
        c = self.inspect(self.save('c.sfs', name='Alpha', location='Other'))
        sm.instructions([a, b, c])
        self.assertTrue(a.get('collision'))
        self.assertFalse(b.get('collision'))
        self.assertTrue(c['instruction'].startswith('Ambiguous'))

    def test_identical_bytes_not_collision(self):
        a = self.inspect(self.save('a.sfs'))
        b = self.inspect(self.save('b.sfs'))
        sm.instructions([a, b])
        self.assertFalse(a.get('collision'))
        self.assertIn('Duplicate input', a['warnings'][-1])

    def test_control_and_mismatch(self):
        p = self.save()
        evidence = self.root / 'synthetic-control.txt'
        evidence.write_text('Synthetic control; not gameplay evidence')
        control = dict(evidence=str(evidence), sha256=sm.identity(evidence)['sha256'], fields={'timestamp': '10/9/26, 9:22:22 PM'})
        r = self.inspect(p, control=control)
        self.assertEqual(r['fields']['timestamp']['confidence'], 'CONTROL_MATCHED')
        control['fields']['timestamp'] = 'wrong'
        self.assertIn('CONTROL_MISMATCH', self.inspect(p, control=control)['error'])
        control['sha256'] = 'wrong'
        self.assertIn('CONTROL_EVIDENCE_HASH_MISMATCH', self.inspect(p, control=control)['error'])

    def test_time_boundaries(self):
        epoch = dt.datetime(1970, 1, 1, tzinfo=dt.timezone.utc)
        for text, expected in [('2026-10-04T00:59:59+00:00', '10/4/26, 11:59:59 AM'),
                               ('2026-10-04T01:00:00+00:00', '10/4/26, 12:00:00 PM'),
                               ('2026-12-31T13:00:00+00:00', '1/1/27, 12:00:00 AM')]:
            ns = int((dt.datetime.fromisoformat(text) - epoch).total_seconds()) * 10**9 + 999999999
            self.assertEqual(sm.display_time(ns, self.zone), expected)
        self.assertEqual(sm.display_time(self.ns, sm.fixed_zone('+10:00')), '10/9/26, 8:22:22 PM')
        for invalid in ('11', '+24:00', '+01:60'):
            with self.assertRaises(ValueError):
                sm.fixed_zone(invalid)

    def test_malformed_and_hash_mismatch(self):
        p = self.save()
        self.assertEqual(self.inspect(p, sha256='wrong')['status'], 'ERROR')
        p.write_bytes(b'bad')
        r = self.inspect(p)
        sm.instructions([r])
        self.assertEqual(r['status'], 'ERROR')
        self.assertTrue(r['preserved'])
        self.assertNotIn('Load ', r['instruction'])

    def test_control_characters_and_invalid_utf8(self):
        self.assertEqual(self.inspect(self.save(name='unsafe\nname'))['status'], 'ERROR')
        p = self.save()
        b, _ = sm.first_stream(p)
        bad = bytearray(b)
        bad[27] = 255
        with self.assertRaises(ValueError):
            sm.parse_metadata(bad)

    def test_corrupt_compressed_stream(self):
        p = self.save()
        b = bytearray(p.read_bytes())
        b[85] ^= 255
        p.write_bytes(b)
        self.assertEqual(self.inspect(p)['status'], 'ERROR')

    def test_mapping_existing_manifest_and_cli_exclusive_output(self):
        p = self.save()
        source = sm.identity(p)
        mapping = self.root / 'mapping.json'
        mapping.write_text(json.dumps(dict(samples=[dict(label='S0', source_before=source, copy=source)])))
        self.assertEqual(sm.load_mapping(mapping)[0]['source']['mtime_ns'], self.ns)
        out = self.root / 'out.json'
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(sm.main(['--mapping', str(mapping), '--utc-offset', '+11:00', '--json', str(out)]), 0)
            original = out.read_bytes()
            self.assertEqual(sm.main([str(p), '--utc-offset', '+11:00', '--json', str(out)]), 2)
            self.assertEqual(out.read_bytes(), original)
            forbidden = self.root / 'never-create.sfs'
            self.assertEqual(sm.main([str(p), '--utc-offset', '+11:00', '--json', str(forbidden)]), 2)
            self.assertFalse(forbidden.exists())


if __name__ == '__main__':
    unittest.main()
