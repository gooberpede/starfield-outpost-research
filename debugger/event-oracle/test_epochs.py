"""Original offline WAL integrity/recovery controls, no process access."""
import hashlib,json,struct,tempfile,unittest
from pathlib import Path
from materialize_epochs import decode,MAGIC,HEADER

def frame(row,sequence=1,previous=bytes(32)):
    payload=json.dumps(row).encode();digest=hashlib.sha256(struct.pack('<Q',sequence)+previous+payload).digest()
    return MAGIC+struct.pack('<QQ',len(payload),sequence)+previous+digest+payload

class EpochTests(unittest.TestCase):
    def read(self,b):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'epochs.wal';p.write_bytes(b);return decode(p)
    def test_every_torn_tail_retains_prior_commit(self):
        first=frame({'kind':'first'});second=frame({'kind':'second'},2,first[56:88])
        for n in range(len(second)):
            rows,r=self.read(first+second[:n]);self.assertEqual(rows,[{'kind':'first'}]);self.assertEqual(r['committed_bytes'],len(first))
    def test_complete_corrupt_payload_fatal(self):
        b=bytearray(frame({'kind':'first'}));b[-2]^=1
        with self.assertRaisesRegex(ValueError,'frame integrity'):self.read(b)
    def test_reordered_sequence_fatal(self):
        with self.assertRaisesRegex(ValueError,'sequence'):self.read(frame({'kind':'first'},2))
    def test_changed_prior_chain_fatal(self):
        with self.assertRaisesRegex(ValueError,'chain'):self.read(frame({'kind':'first'},1,bytes([1])*32))
    def test_raw_metadata_disagreement_fatal(self):
        row={'kind':'raw','bytes':3,'data_hex':'010203','sha256':'0'*64}
        with self.assertRaisesRegex(ValueError,'raw integrity'):self.read(frame(row))
    def test_valid_raw_and_terminal(self):
        row={'kind':'raw','bytes':3,'data_hex':'010203','sha256':hashlib.sha256(bytes([1,2,3])).hexdigest()}
        first=frame(row);b=first+frame({'kind':'terminal','terminal':'RETIRED'},2,first[56:88]);rows,r=self.read(b)
        self.assertEqual(len(rows),2);self.assertEqual(r['incomplete_tail_bytes'],0)
    def test_truncated_header(self):
        rows,r=self.read(MAGIC);self.assertEqual(rows,[]);self.assertEqual(r['incomplete_tail_bytes'],8)
    def test_bad_magic_fatal(self):
        b=bytearray(frame({'kind':'first'}));b[0]=0
        with self.assertRaisesRegex(ValueError,'magic'):self.read(b)

if __name__=='__main__':unittest.main()
