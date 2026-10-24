# SPDX-License-Identifier: GPL-3.0-or-later
"""Pure controls for candidate selection; no process or filesystem mutation."""
import unittest
from readiness import Tracker


def row(site, **kw):
    return dict(kind='SAMPLE', site=site, tid=1, thread_lifetime=1,
                invocation_token=1, required_reads_complete=True,
                frame_matches=True, **kw)


class Tests(unittest.TestCase):
    def test_outcome_independent(self):
        t = Tracker('0005de4c')
        self.assertFalse(t.observe(row('generation_entry', upstream_join=True,
                                     owner_key_u32=0x5de4c, entry_bound=True)))
        self.assertFalse(t.observe(row('resource_call', selection_chain_complete=True,
                                     file_provenance={'main_file_identity': True})))
        self.assertTrue(t.observe(row('provider_return')))

    def test_reject_missing_identity_and_loss(self):
        for bad in ('owner', 'upstream', 'frame', 'namespace', 'exception', 'thread'):
            with self.subTest(bad=bad):
                t = Tracker('0005de4c')
                t.observe(row('generation_entry', upstream_join=bad != 'upstream',
                              owner_key_u32=7 if bad == 'owner' else 0x5de4c, entry_bound=True))
                c = row('resource_call', selection_chain_complete=True,
                        file_provenance={'main_file_identity': bad != 'namespace'})
                c['frame_matches'] = bad != 'frame'
                t.observe(c)
                if bad in ('exception', 'thread'):
                    t.observe(dict(kind='EXCEPTION' if bad == 'exception' else 'THREAD_END', tid=1))
                self.assertFalse(t.observe(row('provider_return')))


if __name__ == '__main__':
    unittest.main()
