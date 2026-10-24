# SPDX-License-Identifier: GPL-3.0-or-later
"""Counterexamples to body-only success and borrowed source/frame lineage."""
import struct
import unittest
from source_gate import Tracker


def row(site, **fields):
    return dict(kind='SAMPLE', tid=1, thread_lifetime=1, invocation_token=1,
                required_reads_complete=True, frame_matches=True, site=site, **fields)


def field(raw):
    return dict(status='COMPLETE', raw=raw.hex())


class SourceTests(unittest.TestCase):
    def attempt(self, change=None):
        target = dict(chart=0, descriptor=[384, 576], source_keys=['0:386:579:00000009'])
        t = Tracker('00000007', target)
        frame = bytearray(0x2c)
        struct.pack_into('<2i', frame, 4, 2, 3)
        source = bytearray(0x70)
        struct.pack_into('<I', source, 0, 9)
        struct.pack_into('<2i', source, 0x10, 2, 3)
        if change == 'other_source':
            struct.pack_into('<I', source, 0, 10)
        if change == 'other_descriptor':
            struct.pack_into('<i', frame, 4, 3)
        t.observe(row('selection', capture=10, manager_frame_descriptor=field(frame)))
        if change == 'exception':
            t.observe(dict(kind='EXCEPTION', tid=1))
        t.observe(row('generation_entry', upstream_join=True, entry_bound=True,
            owner_key_u32=7, source=field(source), upstream_query_capture=11 if change == 'borrowed' else 10))
        t.observe(row('resource_call', selection_chain_complete=True,
                      file_provenance={'main_file_identity':True}))
        return t.observe(row('provider_return'))

    def test_exact_requested_source(self):
        self.assertTrue(self.attempt())

    def test_same_body_is_insufficient(self):
        for change in ('other_source', 'other_descriptor', 'exception', 'borrowed'):
            with self.subTest(change=change):
                self.assertFalse(self.attempt(change))


if __name__ == '__main__':
    unittest.main()
