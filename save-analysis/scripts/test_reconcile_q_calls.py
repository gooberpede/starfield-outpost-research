"""SPDX-License-Identifier: GPL-3.0-or-later
Pure synthetic arithmetic/capture-shape regressions; no live evidence claims.
"""
import struct
import unittest
from reconcile_q_calls import packed_key, separation, saved_token_for_candidate
from q_hierarchy_diagnostic import snap, unpack


class PackedKeyTests(unittest.TestCase):
    def test_archived_key_independent_constants(self):
        v=packed_key(bytes.fromhex('c090e043780eb202'))
        self.assertEqual((v['system_id'],v['body_index'],v['tag']), (88327,15,0))
        self.assertEqual(v['packed_xy'],[37056,17376])
        self.assertEqual([x%12 for x in v['packed_xy']],[0,0])

    def test_field_boundaries_do_not_overlap(self):
        k=(0x3ffff<<41)|(0x3f<<35)|(7<<32)|(0xffff<<16)|1
        v=packed_key(struct.pack('<Q',k))
        self.assertEqual((v['system_id'],v['body_index'],v['tag']), (0x3ffff,63,7))
        self.assertEqual(v['packed_xy'],[1,65535])
        self.assertEqual(packed_key(bytes(8))['packed_xy'],[0,0])

    def test_bad_key_length(self):
        for n in (0,7,9):
            with self.assertRaises(ValueError):packed_key(bytes(n))

    def test_saved_tag_is_wire_little_endian(self):
        self.assertEqual(saved_token_for_candidate(0xff0149ec),'ec4981')
        self.assertEqual(saved_token_for_candidate(0x00325868),'685872')
        with self.assertRaises(ValueError):saved_token_for_candidate(0x01000001)


class BoundingTests(unittest.TestCase):
    def test_touch_is_overlap_and_latch_clears(self):
        self.assertFalse(separation([-1,1,-1,1],[0,0],[1,3,1,3]))
        self.assertFalse(separation([-1,1,-1,1],[0,0],[-3,-1,-3,-1]))

    def test_each_separating_axis_and_translation(self):
        for box in ([2,3,-1,1],[-3,-2,-1,1],[-1,1,2,3],[-1,1,-3,-2]):
            self.assertTrue(separation([-1,1,-1,1],[0,0],box))
        self.assertFalse(separation([-1,1,-1,1],[-2,0],[2,3,-1,1]))

    def test_native_signed_wrap(self):
        self.assertTrue(separation([-1,1,-1,1],[1,0],[2**31-1,2**31-1,-1,1]))
        self.assertFalse(separation([-1,1,-1,1],[1,0],[-1,0,-1,1]))


class ConditionalHierarchyTests(unittest.TestCase):
    def test_independent_archived_divisions(self):
        self.assertEqual(unpack(0x02b20e7843e090c0)['geometry'],[0,193,90,0,8,0,0])

    def test_snap_thresholds_and_seams(self):
        self.assertEqual(snap(0,10,20,3,4),[0,10,20,0,8,0,0])
        self.assertEqual(snap(1,10,20,12,12),[1,11,21,0,0,0,0])
        self.assertEqual(snap(0,255,255,12,12),[1,0,255,0,0,0,0])
        self.assertEqual(snap(0,10,255,0,12),[1,245,255,0,0,0,0])

    def test_reflection_total_domain(self):
        k=(2<<32)|(49151<<16)|49150
        self.assertEqual(unpack(k)['geometry'],[2,0,0,0,0,1,0])
        with self.assertRaises(ValueError):unpack((2<<32)|65535)
        with self.assertRaises(ValueError):unpack(0,block=0)


if __name__=='__main__':unittest.main()
