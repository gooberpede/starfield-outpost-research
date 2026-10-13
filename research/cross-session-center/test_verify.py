# SPDX-License-Identifier: GPL-3.0-or-later
"""Adversarial controls for the independent scientific verifier; no native code."""
import struct
import unittest
import verify as v


class Controls(unittest.TestCase):
    def event(self, version=6):
        raw=bytearray(3328 if version==6 else 17768)
        if version==6:
            struct.pack_into('<16Q',raw,0,1,2,0,3,4,0xf4a1d4,8,2,0x123400,0,0,0,0,0,0,0)
        else:
            struct.pack_into('<11Q',raw,0,1,2,0,4,0x123400,0,3,2,0,0x1f80,0)
        header,stride=(128,400) if version==6 else (88,1040)
        for index,length in [(0,0xd8 if version==6 else 0xd0),(1,0x30),(2,0xa0)]:
            struct.pack_into('<QII',raw,header+stride*index,0x123400+index*0x1000,length,1)
        struct.pack_into('<I',raw,header+16+0x28,0xff01aa50)
        struct.pack_into('<3f',raw,header+16+0x8c,122.70045471191406,273.0462341308594,18.352506637573242)
        struct.pack_into('<I',raw,header+stride+16+0x28,0x2c60e9)
        raw[header+2*stride+16+0x98:header+2*stride+16+0xa0]=bytes.fromhex('f1517de43e171745')
        return raw

    def test_raw_z_and_wrong_offsets(self):
        e=v.decode(self.event(),6);r=v.blob(e,'ref')
        self.assertEqual(r[0x94:0x98].hex(),'efd19241')
        self.assertNotEqual(r[0x90:0x94],r[0x94:0x98])
        self.assertNotEqual(r[0x98:0x9c],r[0x94:0x98])

    def test_wrong_schema_rejected(self):
        with self.assertRaises(ValueError):v.decode(self.event(),5)

    def test_out_of_bounds_rejected(self):
        raw=self.event();struct.pack_into('<I',raw,136,385)
        with self.assertRaises(ValueError):v.decode(raw,6)

    def test_unreadable_not_zero(self):
        raw=self.event();struct.pack_into('<I',raw,140,0)
        with self.assertRaises(ValueError):v.identity(v.decode(raw,6))

    def test_incoherent_identity_rejected(self):
        raw=self.event();struct.pack_into('<Q',raw,88,8)
        with self.assertRaises(ValueError):v.identity(v.decode(raw,6))

    def test_form_id_is_not_workshop_id(self):
        e=v.decode(self.event(),6);wid,form=v.identity(e)
        self.assertEqual(wid,'f1517de43e171745');self.assertEqual(form,0xff01aa50)
        raw=self.event();raw[128+2*400+16+0x98:128+2*400+16+0xa0]=struct.pack('<Q',form)
        with self.assertRaises(ValueError):v.identity(v.decode(raw,6))

    def test_pointer_reuse_splits(self):
        a=dict(session=1,pointer=123,form=1,base=2,workshop='a');b=dict(a,workshop='b')
        self.assertFalse(v.compatible_samples(a,b))
        self.assertFalse(v.compatible_samples(a,dict(a,session=2)))
        self.assertTrue(v.compatible_samples(a,a)) # only a candidate, not lifetime proof

    def test_missing_ancestry(self):
        with self.assertRaises(ValueError):v.ancestor(dict(parent=9,thread=1,sequence=3),{},7)

    def test_cross_thread_false_parent(self):
        with self.assertRaises(ValueError):v.ancestor(dict(parent=9,thread=1,sequence=3),{9:dict(kind=7,thread=2,sequence=1)},7)

    def test_conflicting_frame_fields_do_not_prove_translation(self):
        self.assertEqual(v.frame_claim(2,0,None),'COMMON_3D_FRAME_UNPROVEN')
        self.assertEqual(v.frame_claim(None,123,456),'FLAG_UNOBSERVED')
        self.assertEqual(v.frame_claim(0,123,456),'SAMPLED_FIELDS_ONLY_REQUIRES_SELECTED_EDGE')

    def test_cross_thread_sequence_does_not_order_native_writes(self):
        a=dict(thread=1,qpc=200);b=dict(thread=2,qpc=100)
        self.assertEqual(v.order_claim(a,b),'NO_TOTAL_NATIVE_ORDER')
        self.assertEqual(v.order_claim(a,dict(b,thread=1)),'TIMESTAMP_CONFLICT')

    def test_050_d3_missing_not_zero(self):
        r=v.blob(v.decode(self.event(5),5),'ref')
        self.assertEqual(len(r),0xd0);self.assertLess(len(r),0xd4)


if __name__=='__main__':unittest.main()
