# SPDX-License-Identifier: GPL-3.0-or-later
"""Synthetic D2 controls: positive-only taxonomy and resource-label skipping.

Stdlib/project only; no files, proprietary fixtures or target effects. These
verify classification boundaries, not native geometry or population semantics.
"""
import struct
import unittest

from save52 import skip_resources
from save52_compare import classify
from outpost_record_framing import Reader


class Save52Tests(unittest.TestCase):
    def test_partial_omission_is_unknown(self):
        self.assertEqual(classify(dict(status='PARTIAL'), 'authored'), 'UNSUPPORTED_INDETERMINATE')

    def test_complete_omission_is_candidate(self):
        self.assertEqual(classify(dict(status='CONDITIONAL_GEOMETRY'), 'authored'), 'POTENTIAL_FALSE_NEGATIVE')

    def test_partial_positive_is_preserved(self):
        value = dict(status='PARTIAL',availability={'authored':dict(status='PRESENT')})
        self.assertEqual(classify(value,'authored'),'POSITIVE_CORRESPONDENCE')

    def test_unknown_does_not_become_absence(self):
        value = dict(status='CONDITIONAL_GEOMETRY',availability={'authored':dict(status='UNKNOWN')})
        self.assertEqual(classify(value,'authored'),'UNSUPPORTED_INDETERMINATE')

    def test_alternative_never_scores_vein_mismatch(self):
        self.assertEqual(classify(dict(status='CONDITIONAL_GEOMETRY'),'authored',True),'ALTERNATIVE_ADMISSION')

    def test_skip_drops_labels_and_consumes_exact_framing(self):
        data = struct.pack('<I',2)+b'X'*34+struct.pack('<I',0)
        reader = Reader(data,0,len(data))
        popped = []
        def refs(n):
            popped.append(n)
            return ['secret-answer']*n
        self.assertEqual(skip_resources(reader,refs,2),[])
        self.assertEqual(popped,[1,4,1,0])
        self.assertEqual(reader.p,len(data))

    def test_skip_rejects_truncation(self):
        with self.assertRaises(ValueError):
            skip_resources(Reader(struct.pack('<I',2),0,4),lambda n:[],1)


if __name__=='__main__':
    unittest.main()
