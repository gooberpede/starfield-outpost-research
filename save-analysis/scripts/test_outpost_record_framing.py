"""SPDX-License-Identifier: GPL-3.0-or-later
Original synthetic and independent offset-walker checks. Stdlib only.
--corpus reads verified selected sources in memory and writes fresh ignored
test receipts; no target/save/database changes. No active-state test oracle.
"""
import argparse,json,struct,unittest
from pathlib import Path
from outpost_record_framing import Reader,records,beacon_prefix


def independent(b,a,z,n):
    """Separate arithmetic walker, no production cursor/count implementation."""
    p=a;result=[]
    for _ in range(n):
        begin=p;tag=b[p];p+=1
        if tag&1:p+=1
        token=b[p:p+3].hex();p+=3
        flags=struct.unpack_from('<I',b,p)[0] if tag&2 else 0x80008000
        if tag&2:p+=4
        counts=[]
        for bit in [8,16,32]:
            value=0
            if tag&bit:
                w=(1,2,4)[b[p]&3];value=int.from_bytes(b[p:p+w],'little')//4;p+=w
            counts.append(value)
        nr,ns,size=counts;body=p+3*nr+2*ns;p=body+size
        if p>z:raise ValueError('independent boundary')
        result.append((begin,p,token,flags,body,size))
    if p!=z:raise ValueError('independent closure')
    return result


class FramingTests(unittest.TestCase):
    def test_count_widths(self):
        for n,w,tag in [(0,1,0),(63,1,0),(64,2,1),(16383,2,1),(16384,4,2)]:
            b=((n<<2)|tag).to_bytes(w,'little');c=Reader(b,0,len(b));self.assertEqual(c.count(),n);self.assertEqual(c.p,len(b))
    def test_header_tables_body(self):
        b=bytes([0x3f,0x4a])+bytes.fromhex('800001')+struct.pack('<I',3)+bytes([4,4,8])+bytes.fromhex('400014')+struct.pack('<H',7)+b'ab'
        r=records(b,0,len(b),1)[0];self.assertEqual(r['explicit_type'],0x4a);self.assertEqual(r['refs'],['400014']);self.assertEqual(r['strings'],[7]);self.assertEqual(r['size'],2)
        self.assertEqual(independent(b,0,len(b),1)[0],(r['offset'],r['end'],r['token'],r['flags'],r['body'],r['size']))
    def test_defaults(self):
        r=records(bytes.fromhex('00800001'),0,4,1)[0];self.assertEqual(r['flags'],0x80008000);self.assertEqual(r['size'],0)
    def test_reject_truncations(self):
        for b in [b'',bytes.fromhex('20800001'),bytes.fromhex('0880000104'),bytes.fromhex('1080000104'),bytes.fromhex('2080000107')]:
            with self.subTest(b=b),self.assertRaises(ValueError):records(b,0,len(b),1)
    def test_exact_closure(self):
        for b,n in [(bytes.fromhex('0080000100'),1),(bytes.fromhex('00800001'),0),(bytes.fromhex('c0800001'),1)]:
            with self.subTest(b=b),self.assertRaises(ValueError):records(b,0,len(b),n)
    def test_prefix_offsets_and_decoy(self):
        for shape,rotation_n,tail in [(0,0,1),(4,1,1),(8,0,0),(16,0,0),(7,3,1)]:
            b=bytes([shape])+struct.pack('<3f',1,2,3)+bytes(4*rotation_n+tail)+struct.pack('<IH',0x400c08,0x41)
            r=dict(token='800001',flags=0x92000703,refs=['800002','6c60e9','800001'],body=0,end=len(b))
            x=beacon_prefix(b,r);self.assertTrue(x['disabled']);self.assertFalse(x['deleted']);self.assertEqual(x['saved_flags_offset'],13+4*rotation_n+tail)
            r['refs']=['6c60e9','800002','800001'];self.assertIsNone(beacon_prefix(b,r))


def corpus(run):
    from investigate_active_outposts import specs,identity,framing,transform,directory,ROOT
    selected={'Save3','S0','S0C','S1','S1C','S7','L0C','HIST-0267','HIST-0016','HIST-0083','TDX1798-0001'};result=[]
    for s in specs():
        if s['label'] not in selected:continue
        p=Path(s['copy']['path']);before=identity(p);assert before['sha256']==s['copy']['sha256']
        physical=p.read_bytes();_,sp=framing(physical);b=transform(physical,sp,True);d=directory(b);a,z=d['regions']['region_R3'];rs=records(b,a,z,d['words'][9]);other=independent(b,a,z,len(rs))
        assert other==[(r['offset'],r['end'],r['token'],r['flags'],r['body'],r['size']) for r in rs]
        assert identity(p)==before
        result.append(dict(label=s['label'],sha256=before['sha256'],records=len(rs),region=[a,z],match=True))
    assert {r['label'] for r in result}==selected
    if not run.replace('-','').isalnum():raise ValueError('run name')
    out=ROOT/'.local-work/active-outpost'/('independent-'+run+'.json')
    with out.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2);f.write('\n')
    print('Independent corpus PASS',len(result),'saves',sum(r['records'] for r in result),'records')


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--corpus',action='store_true');ap.add_argument('--run',default='tests');args=ap.parse_args()
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(FramingTests)
    if not unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful():raise SystemExit(1)
    if args.corpus:corpus(args.run)
