"""Synthetic intake and independent-grammar safety tests; no save fixtures."""
import unittest
import inventory_launch_corpus as launch


def listing(path='folder\\control.sfs', attrs='A', size=10, extra=''):
    return '\n----------\nPath = '+path+'\nSize = '+str(size)+'\nAttributes = '+attrs+'\nEncrypted = -\n'+extra+'\n'


class LaunchTests(unittest.TestCase):
    def test_safe_member_and_limits(self):
        self.assertEqual(launch.members(listing())[0]['size'], 10)
        for path in ('../bad.sfs', '/bad.sfs', 'C:\\bad.sfs', 'file.sfs:stream', 'folder\\CON.sfs', 'folder\\bad .sfs ', 'bad.exe'):
            with self.subTest(path=path), self.assertRaises(ValueError):
                launch.members(listing(path))
        for text in (listing(size=launch.inv.MAX_PHYSICAL+1), listing(extra='Symbolic Link = target\n'), listing(attrs='AL')):
            with self.assertRaises(ValueError):
                launch.members(text)

    def test_casefold_duplicates(self):
        text = listing() + listing('FOLDER\\CONTROL.sfs').split('\n----------\n')[1]
        with self.assertRaises(ValueError):
            launch.members(text)

    def test_empty_detection_is_not_absence_proof(self):
        f = dict(beacon_windows=[], errors=[], beacon_collection_count=0, beacon_count=0,
                 marker_count=0, animation_string_count=0, keyed_groups=0, endpoints=0)
        self.assertEqual(launch.classification(f), 'NO_ACTIVE_OUTPOST_INDICATORS_DETECTED')
        for change in (dict(animation_string_count=1), dict(errors=['unsupported']), dict(keyed_groups=2), dict(beacon_count=1)):
            self.assertEqual(launch.classification(dict(f, **change)), 'INCONCLUSIVE')
        self.assertEqual(launch.classification(dict(f, beacon_windows=[dict(names=[dict(name='Synthetic')])])), 'OUTPOST_EVIDENCE_PRESENT')
        self.assertEqual(launch.classification(None), 'INCONCLUSIVE')

    def test_independent_walk(self):
        successor = bytes.fromhex('7a00000028000000')
        payload = bytes.fromhex('0000')
        raw = bytes.fromhex('7900000002000000') + payload + successor
        f = dict(envelopes=[dict(payload_offset=8, end=10)])
        self.assertEqual(launch.audit(raw, f)[0]['consumed'], 2)
        for b in (raw[:8]+bytes.fromhex('0400')+successor, raw[:8]+bytes.fromhex('0300')+successor, raw[:-1]):
            with self.assertRaises(ValueError):
                launch.audit(b, f)


if __name__ == '__main__':
    unittest.main()
