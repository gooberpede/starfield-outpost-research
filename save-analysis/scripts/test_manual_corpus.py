"""Synthetic checks of bounded decoder and alignment, never game semantics."""
import struct
import unittest
import zlib
from analyze_manual_corpus import decode, regions, compare


def fixture(raw):
    blocks=[zlib.compress(raw[i:i+262144]) for i in range(0,len(raw),262144)]
    b=bytearray(72+4*len(blocks)); b[:8]=b'BCPS\x01\0\0\0';b[68:72]=b'ZIP '
    for p,value in [(8,72),(24,len(b)),(32,len(raw)),(48,262144)]:
        struct.pack_into('<Q',b,p,value)
    for i,block in enumerate(blocks):struct.pack_into('<I',b,72+4*i,len(block))
    for block in blocks:
        b.extend(block);b.extend(b'\0'*((-len(b))%16))
    return bytes(b)


class Checks(unittest.TestCase):
    def test_multichunk(self):
        raw=b'SFS_SAVEGAME'+bytes(range(256))*1100
        decoded,chunks=decode(fixture(raw))
        self.assertEqual(decoded,raw);self.assertEqual(len(chunks),2)

    def test_corruption_and_truncation(self):
        b=fixture(b'SFS_SAVEGAME'+b'abcd'*200)
        with self.assertRaises((ValueError,zlib.error)):decode(b[:-20])
        bad=bytearray(b);bad[85]^=255
        with self.assertRaises((ValueError,zlib.error)):decode(bytes(bad))

    def test_header_and_size_bounds(self):
        b=bytearray(fixture(b'SFS_SAVEGAME'+b'abc'))
        struct.pack_into('<Q',b,32,2**40)
        with self.assertRaises(ValueError):decode(bytes(b))
        with self.assertRaises(ValueError):decode(b'not a save')

    def test_trailing_bytes(self):
        with self.assertRaises(ValueError):decode(fixture(b'SFS_SAVEGAME')+b'junk')

    def test_insertion_resynchronization(self):
        import random
        rng=random.Random(71);a=rng.randbytes(16000);b=a[:7100]+b'INSERTED'+a[7100:]
        diff=compare(a,b,regions(a),regions(b))
        self.assertEqual(diff['regions'],[dict(kind='insert',before=[7100,7100],after=[7100,7108])])
        self.assertEqual(diff['matched_bytes'],len(a))


if __name__=='__main__':unittest.main()
