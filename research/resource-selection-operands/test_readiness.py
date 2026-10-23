# SPDX-License-Identifier: GPL-3.0-or-later
"""Pure selector regressions on independently expressed receipt shapes."""
import copy
import struct
import unittest
from readiness import Tracker


def group(b):
    return dict(status='COMPLETE', raw=b.hex())


def series():
    base = dict(kind='SAMPLE', tid=9, thread_lifetime=2, invocation_token=7,
                required_reads_complete=True, frame_matches=True)
    rows = [dict(base, site='generation_entry', entry_bound=True, owner_key_u32=385246,
                 origin=group(struct.pack('<ii', -3800, -200)))]
    for fid, cells in ((0x57d4, (10, 11)), (0x57cf, (11,))):
        r = bytearray(0x118)
        struct.pack_into('<I', r, 0x28, fid)
        rows.append(dict(base, site='resource_call', ires=group(r),
                         file_provenance=dict(status='COMPLETE', main_file_identity=True)))
        for x in cells:
            rows.append(dict(base, site='chance_branch', resource_call_join=True,
                             cell_xy_i32=group(struct.pack('<ii', x, 1))))
    rows.append(dict(base, site='provider_return'))
    return rows


class Tests(unittest.TestCase):
    def test_minimum_and_adverse(self):
        tracker = Tracker()
        self.assertEqual([tracker.observe(r) for r in series()], [False]*6+[True])
        for index, change in ((0, dict(owner_key_u32=7)), (2, dict(resource_call_join=False)),
                              (3, dict(required_reads_complete=False)),
                              (4, dict(file_provenance=dict(status='INCOMPLETE'))),
                              (6, dict(frame_matches=False)), (6, dict(thread_lifetime=3))):
            with self.subTest(index=index, change=change):
                rows = copy.deepcopy(series())
                rows[index].update(change)
                t = Tracker()
                self.assertFalse(any(t.observe(r) for r in rows))

    def test_lifecycle_and_nested(self):
        t = Tracker()
        rows = series()
        for r in rows[:-1]:
            t.observe(r)
        t.observe(dict(kind='EXCEPTION', tid=9))
        self.assertFalse(t.observe(rows[-1]))
        self.assertFalse(t.active)
        t = Tracker()
        for r in rows[:-1]:
            t.observe(r)
        nested = [dict(r, invocation_token=8) for r in rows]
        self.assertTrue([t.observe(r) for r in nested][-1])
        self.assertTrue(t.observe(rows[-1]))


if __name__ == '__main__':
    unittest.main()
