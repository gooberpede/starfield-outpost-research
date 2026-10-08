"""Synthetic fail-closed tests; no game files, save edits or subprocesses."""
import struct
import unittest
from analyze_structural_containment import directory,string_pool,tail_table

class StructuralBounds(unittest.TestCase):
    def directory_fixture(self):
        b=bytearray(6000)
        struct.pack_into('<10I',b,200,4500,4516,300,350,500,4000,17,21,9,1)
        struct.pack_into('<I',b,4500,3)
        return b
    def pool_fixture(self):
        b=self.directory_fixture();struct.pack_into('<I',b,304,4516)
        names=[b'SOR-001',b'OBJ_Outpost_Beacon_Deploy',b'OBJ_Outpost_Beacon_On_LP']
        p=4516;struct.pack_into('<H',b,p,3);p+=2
        for t in names:struct.pack_into('<H',b,p,len(t));b[p+2:p+2+len(t)]=t;p+=2+len(t)
        struct.pack_into('<3H',b,800,0,1,2)
        return b,directory(b),{'beacon':{'offset':700}},p
    def test_unique_directory_and_ambiguity(self):
        b=self.directory_fixture();self.assertEqual(directory(b)['offset'],200)
        b[240:280]=b[200:240]
        with self.assertRaises(ValueError):directory(b)
    def test_reference_count_cannot_cross_boundary(self):
        b=self.directory_fixture();struct.pack_into('<I',b,4500,4)
        with self.assertRaises(ValueError):directory(b)
    def test_counted_string_pool_and_index(self):
        b,d,e,end=self.pool_fixture();p,n=string_pool(b,d,e)
        self.assertEqual(p['end'],end);self.assertEqual(n['beacon_index_relative_offset'],100)
        struct.pack_into('<3H',b,800,111,222,333)
        with self.assertRaises(ValueError):string_pool(b,d,e)
    def test_invalid_string_length_and_pointer(self):
        b,d,e,_=self.pool_fixture();struct.pack_into('<H',b,4518,65535)
        with self.assertRaises(ValueError):string_pool(b,d,e)
        b,d,e,_=self.pool_fixture();struct.pack_into('<I',b,304,999999)
        with self.assertRaises(ValueError):string_pool(b,d,e)
    def test_tail_order_and_exact_eof(self):
        b=struct.pack('<5I',2,0xff000100,1,0xff000200,2)
        self.assertEqual(tail_table(b)['count'],2)
        with self.assertRaises(ValueError):tail_table(b+b'X')

if __name__=='__main__':unittest.main()
