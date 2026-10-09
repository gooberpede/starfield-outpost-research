"""Original numeric synthetic association fixtures; no game content."""
import struct
import unittest
from outpost_planetary_location import associations,body_catalog,global_suffix
from outpost_record_framing import iter_records
from stream_save import ResourceLimit


class PlanetaryTests(unittest.TestCase):
    def setUp(self):
        self.records=[dict(type='PNDT',formid=0x123,edid='SyntheticBody',fields={'GNAM':struct.pack('<III',42,1,7).hex()})]
        self.pairs,self.ids=body_catalog(self.records)
    def test_separate_cache_and_point(self):
        p=0x800123;body=0x400123
        cache=struct.pack('<5I',p,0,42,7,0x800456)
        point=struct.pack('<IIHddI',body,p,2,1.25,-0.5,p)
        b=cache+b'\0'*8+point
        c,s=associations(b,0,len(b),'800123',self.pairs,self.ids)
        self.assertEqual(len(c),1);self.assertEqual(len(s),1)
        self.assertEqual(c[0]['body_options'][0]['formid'],0x123)
        self.assertEqual(s[0]['pair'],[1.25,-0.5])
    def test_unknown_body_or_parent_not_accepted(self):
        b=struct.pack('<IIHddI',0x400124,0x800123,2,1.25,-0.5,0x800123)
        self.assertEqual(associations(b,0,len(b),'800123',self.pairs,self.ids),([],[]))
        b=struct.pack('<IIHddI',0x400123,0x800123,2,1.25,-0.5,0x800124)
        self.assertEqual(associations(b,0,len(b),'800123',self.pairs,self.ids),([],[]))
    def test_bounds_truncation_and_nan(self):
        b=struct.pack('<IIHddI',0x400123,0x800123,2,float('nan'),0.,0x800123)
        self.assertEqual(associations(b,0,len(b),'800123',self.pairs,self.ids),([],[]))
        for n in range(len(b)):
            self.assertEqual(associations(b[:n],0,n,'800123',self.pairs,self.ids),([],[]))
    def test_ambiguous_catalog_preserved(self):
        records=self.records+[dict(self.records[0],formid=0x124)]
        pairs,_=body_catalog(records);self.assertEqual(len(pairs[(42,7)]),2)
    def test_global_suffix_closure(self):
        b=b''.join(struct.pack('<II',i,1)+b'x' for i in range(4,17))
        d={'regions':{'region_R1':[0,len(b)]}}
        self.assertEqual(len(global_suffix(b,d)),13)
        with self.assertRaises(ValueError):global_suffix(b+b'x',{'regions':{'region_R1':[0,len(b)+1]}})
    def test_record_queue_budget(self):
        # tag8 (reference queue), token, count1, one reference; no body.
        b=bytes.fromhex('0880012304800123')
        with self.assertRaises(ResourceLimit):list(iter_records(b,0,len(b),1,queue_budget=1))


if __name__=='__main__':unittest.main()
