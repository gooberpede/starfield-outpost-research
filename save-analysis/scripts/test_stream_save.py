"""Original synthetic BCPS fixtures; no proprietary payloads/dependencies."""
import io
from pathlib import Path
import struct
import tempfile
import tracemalloc
import unittest
from unittest.mock import patch
import zlib
from stream_save import BLOCK, CorruptSave, ResourceLimit, decoded_save, header, disk_guard


def fixture(path, size=BLOCK, declared=None):
    count = (size + BLOCK - 1)//BLOCK
    start = (72 + 4*count + 15)//16*16
    h = bytearray(start)
    h[:8] = b'BCPS\1\0\0\0'; h[68:72] = b'ZIP '
    for p, n in [(8,72),(24,start),(32,size if declared is None else declared),(48,BLOCK)]:
        struct.pack_into('<Q',h,p,n)
    chunks = []
    for i in range(count):
        raw = (b'SFS_SAVEGAME' if i == 0 else b'')
        raw += b'\0'*(min(BLOCK,size-i*BLOCK)-len(raw))
        c = zlib.compress(raw)
        struct.pack_into('<I',h,72+4*i,len(c))
        chunks.append(c+b'\0'*((-len(c))%16))
    path.write_bytes(h+b''.join(chunks))


class StreamingTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name);self.p=self.root/'input.sfs'
        self.scratch=self.root/'scratch'
    def decode(self, **kwargs):
        return decoded_save(self.p,self.scratch,guard=lambda *a:None,**kwargs)
    def test_large_aggregate_bounded_python_memory_and_cleanup(self):
        fixture(self.p, 65*1024**2+1)
        tracemalloc.start()
        with self.decode() as (b,m):
            self.assertEqual(len(b),65*1024**2+1)
            self.assertEqual(m['streams'],261)
            self.assertEqual(m['scratch_peak_bytes'],len(b))
            self.assertLess(tracemalloc.get_traced_memory()[1],2*1024**2)
        tracemalloc.stop()
        self.assertEqual(list(self.scratch.iterdir()),[])
    def test_extreme_header_rejected_before_scratch(self):
        fixture(self.p,declared=2**64-1)
        with self.assertRaises(CorruptSave):
            with self.decode():pass
        self.assertEqual(list(self.scratch.iterdir()),[])
    def test_false_length_expansion(self):
        fixture(self.p,declared=BLOCK-1)
        with self.assertRaises(CorruptSave):
            with self.decode():pass
    def test_truncation_and_checksum(self):
        fixture(self.p);good=self.p.read_bytes()
        for bad in [good[:71],good[:-16],good[:200]]:
            self.p.write_bytes(bad)
            with self.assertRaises(CorruptSave):
                with self.decode():pass
        bad=bytearray(good);bad[-17]^=1;self.p.write_bytes(bad)
        with self.assertRaises(CorruptSave):
            with self.decode():pass
    def test_resource_distinct_budget_timeout(self):
        fixture(self.p)
        for options in [dict(scratch_budget=1),dict(seconds=-1)]:
            with self.assertRaises(ResourceLimit):
                with self.decode(**options):pass
        self.assertEqual(list(self.scratch.iterdir()),[])
    def test_low_space(self):
        with patch('stream_save.shutil.disk_usage',return_value=type('D',(),{'free':40_000_000_000})()):
            with self.assertRaises(ResourceLimit):disk_guard(self.root,1)
    def test_consumer_exception_cleanup(self):
        fixture(self.p)
        with self.assertRaisesRegex(RuntimeError,'consumer'):
            with self.decode():raise RuntimeError('consumer')
        self.assertEqual(list(self.scratch.iterdir()),[])
    def test_table_false_chunk_size(self):
        fixture(self.p);h=bytearray(self.p.read_bytes());struct.pack_into('<I',h,72,2**32-1);self.p.write_bytes(h)
        with self.p.open('rb') as f:
            with self.assertRaises(CorruptSave):header(f)
    def test_header_above_old_one_gib_limit(self):
        # Header feasibility only: repeated compressed blocks, not a 1GiB write.
        count=4097;start=(72+4*count+15)//16*16
        c=zlib.compress(b'x'*BLOCK);stride=(len(c)+15)//16*16
        h=bytearray(start);h[:8]=b'BCPS\1\0\0\0';h[68:72]=b'ZIP '
        for p,n in [(8,72),(24,start),(32,count*BLOCK),(48,BLOCK)]:struct.pack_into('<Q',h,p,n)
        for i in range(count):struct.pack_into('<I',h,72+4*i,len(c))
        f=io.BytesIO(h+(c+b'\0'*(stride-len(c)))*count)
        self.assertGreater(header(f)['declared_decoded_size'],1024**3)


if __name__=='__main__':unittest.main()
