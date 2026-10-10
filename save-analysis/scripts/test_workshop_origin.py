"""SPDX-License-Identifier: GPL-3.0-or-later
Original boundary/failure tests for the research-only Workshop prefix reader.
Hand-authored minimal fixture; no proprietary fixture or target I/O.
"""
import struct
import unittest
from research_workshop_origin import workshop_prefix, f32


class WorkshopOriginTests(unittest.TestCase):
    def fixture(self):
        # One extra, empty resource table, one queued handle, flag, uint32,
        # three float32 components, eight-byte identifier. Following byte is
        # deliberately outside this Workshop prefix and must not be consumed.
        b=b'\x04\xbc'+b'\0'*4+b'\x04\0'+struct.pack('<I3fQ',2,1.25,-2.5,4,123)+b'\xff'
        r=dict(flags=0,body=0,offset=0,end=len(b),refs=['812345'],strings=[17])
        p=dict(form_prefix_end=0,next_reference_index=0)
        return b,r,p

    def test_prefix_leaves_following_extra_unread(self):
        b,r,p=self.fixture(); result=workshop_prefix(b,r,p)
        self.assertEqual(result['end'],len(b)-1)
        self.assertEqual(result['handles'],['812345'])
        self.assertEqual(result['delta_hex'],f32([1.25,-2.5,4]).hex())

    def test_reject_nonempty_resource_table(self):
        b,r,p=self.fixture(); b=b[:2]+struct.pack('<I',1)+b[6:]
        with self.assertRaisesRegex(ValueError,'nonempty Workshop'): workshop_prefix(b,r,p)

    def test_reject_missing_handle_queue(self):
        b,r,p=self.fixture(); r['refs']=[]
        with self.assertRaisesRegex(ValueError,'queue bounds'): workshop_prefix(b,r,p)

    def test_reject_truncated_identifier(self):
        b,r,p=self.fixture(); r['end']-=4
        with self.assertRaisesRegex(ValueError,'boundary crossing'): workshop_prefix(b,r,p)

    def test_unknown_extra_stops(self):
        b,r,p=self.fixture(); b=b[:1]+b'\xff'+b[2:]
        with self.assertRaisesRegex(ValueError,'unsupported leading extra'): workshop_prefix(b,r,p)

    def test_reject_pre_extra_fields(self):
        b,r,p=self.fixture(); r['flags']=0x80
        with self.assertRaisesRegex(ValueError,'pre-extra fields'): workshop_prefix(b,r,p)


if __name__=='__main__': unittest.main()
