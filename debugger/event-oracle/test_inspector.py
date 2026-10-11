"""SPDX-License-Identifier: GPL-3.0-or-later
Offline adverse evidence controls. Temporary derivatives, no targets or originals.
"""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from inspect_events import inspect

class InspectorTests(unittest.TestCase):
    def test_partial_final_line_and_unpaired_entry(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t);r={'kind':'boundary','thread':8,'invocation':4,'site':'center_entry','pairing':'entered'}
            (p/'records.jsonl').write_bytes((json.dumps(r)+'\n{"incomplete"').encode())
            result=inspect(p);self.assertTrue(result['journal_truncated_final_line']);self.assertEqual(result['unpaired'],1)
    def test_corrupt_raw_is_fatal(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t);b=b'1234';(p/'raw-1.bin').write_bytes(b'1235')
            r={'kind':'raw','file':'raw-1.bin','root':'a','bytes':4,'sha256':hashlib.sha256(b).hexdigest()}
            (p/'records.jsonl').write_text(json.dumps(r)+'\n')
            with self.assertRaisesRegex(ValueError,'integrity'):inspect(p)
    def test_cross_thread_exit_not_joined(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t);rows=[{'kind':'boundary','thread':x,'invocation':1,'site':site,'pairing':pairing} for x,site,pairing in [(8,'center_entry','entered'),(9,'center_exit','paired')]]
            (p/'records.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in rows))
            with self.assertRaisesRegex(ValueError,'invalid exit pair'):inspect(p)

if __name__=='__main__':unittest.main()
