"""SPDX-License-Identifier: GPL-3.0-or-later
Offline layout/partial-output guards only; no target access.
"""
import struct
import unittest
from contract import decode_pair,decode_line


class ContractTests(unittest.TestCase):
    def test_hierarchy_and_opaque_fields(self):
        b=bytearray(44);b[0]=1
        for o,v in [(4,54),(8,110),(20,8),(24,2),(36,3)]:struct.pack_into('<i',b,o,v)
        r=decode_pair(b)
        self.assertEqual((r['tag'],r['x'],r['y']),(1,10467,21144))
        b[0]=4
        with self.assertRaises(ValueError):decode_pair(b)

    def test_partial_is_evidence(self):
        r=decode_line('SOR_POSITION tid=1 center=???','SYNTHETIC')
        self.assertEqual(r['status'],'PARTIAL')
        self.assertIn('result',r['unreadable'])

    def test_kind_required_and_resolution_guard(self):
        with self.assertRaises(ValueError):decode_line('SOR_POSITION ','UNKNOWN')
        with self.assertRaises(ValueError):decode_pair(bytes(44),resolution=128)


if __name__=='__main__':unittest.main()
