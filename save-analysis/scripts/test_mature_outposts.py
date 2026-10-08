"""Synthetic safety/grammar tests; no proprietary fixtures or file writes."""
import unittest
from validate_mature_outposts import grammar,Cursor,envelopes
class GrammarTests(unittest.TestCase):
 def test_counts(self):
  for n,w,tag in [(0,1,0),(1,1,0),(2,1,0),(17,1,0),(199,2,1),(16384,4,2)]:
   b=((n<<2)|tag).to_bytes(w,'little');c=Cursor(b)
   self.assertEqual(c.count('n'),n);self.assertEqual(c.p,w)
 def test_small_payloads(self):
  for h,n in [('04822c5d0400000004679bc3',1),('04822c5d08822d4804822da900000004679bc3',2)]:
   x=grammar(bytes.fromhex(h));self.assertEqual(len(x['groups']),n);self.assertEqual(x['consumed'],len(bytes.fromhex(h)))
 def test_all_truncations(self):
  b=bytes.fromhex('04822c5d08822d4804822da900000004679bc3')
  for n in range(len(b)):
   with self.subTest(n=n),self.assertRaises(ValueError): grammar(b[:n])
 def test_reject_invalid(self):
  for b in [b'\x03',b'\x01',b'\x02\x00',b'\xfc',b'\x00\xfc',b'\x00\x02\xff\xff\xff',b'\x00\x00\x00',b'\xff\xff\xff\xff']:
   with self.subTest(b=b),self.assertRaises(ValueError):grammar(b)
 def test_duplicate_and_zero_preserved(self):
  x=grammar(bytes.fromhex('08010203010203080000000804050604050600000000'))
  self.assertEqual(x['duplicate_beacons'],1);self.assertEqual(x['duplicate_keys'],1);self.assertEqual(x['duplicate_refs'],1)
  self.assertEqual(x['groups'][0]['key'],'000000')
 def test_framing(self):
  b=bytes.fromhex('790000000200000000007a00000028000000');d={'regions':{'region_R2':[0,len(b)]}}
  self.assertTrue(envelopes(b,d)[0]['qualifies'])
  for bad in [b[:-1],b[:4]+b'\xff'*4+b[8:],b[:-8]+b'\x00'*8]:
   self.assertFalse(envelopes(bad,{'regions':{'region_R2':[0,len(bad)]}})[0]['qualifies'])
if __name__=='__main__':unittest.main()
