# SPDX-License-Identifier: GPL-3.0-or-later
"""Original stdlib-only disposable offline evidence/adverse-comparison tests.
Reads original test fixture output; writes ignored synthetic derivatives only.
"""
import importlib.util
import json
from pathlib import Path
import struct
import sys
import tempfile
import unittest

spec=importlib.util.spec_from_file_location('oracle_inspect',Path(__file__).with_name('inspect_events.py'))
oracle=importlib.util.module_from_spec(spec);spec.loader.exec_module(oracle)
BASE=Path(sys.argv[1]);sys.argv=sys.argv[:1]
class EvidenceTests(unittest.TestCase):
    def fixture(self,rows=None):
        p=Path(tempfile.mkdtemp(prefix='evidence-',dir=BASE))
        data=(BASE/'fixture-events.bin').read_bytes()
        if rows is not None:data=b''.join(data[i*oracle.SIZE:(i+1)*oracle.SIZE] for i in rows)
        (p/'events.bin').write_bytes(data)
        records=[]
        for offset in range(0,len(data),oracle.SIZE):
            part=data[offset:offset+oracle.SIZE];event=oracle.decode(part)
            records.append(dict(offset=offset,length=oracle.SIZE,sha256=oracle.digest(part),**{k:event[k] for k in ('sequence','invocation','kind')}))
        (p/'records.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in records),encoding='utf8')
        (p/'ready.json').write_text(json.dumps(dict(component='SorNativePositionOracle',version='0.3.0',schema=3,event_size=oracle.SIZE,synthetic=True)),encoding='utf8')
        return p
    def test_real_abi_fixture(self):
        r=oracle.inspect(self.fixture());self.assertEqual(r['events'],5);self.assertTrue(r['comparisons'][0]['paired']);self.assertEqual(r['comparisons'][0]['classification'],'SYNTHETIC_QUALIFICATION_ONLY')
    def test_missing_exit(self):
        r=oracle.inspect(self.fixture([0,1,2,3]));self.assertFalse(r['comparisons'][0]['paired'])
    def test_missing_center(self):
        r=oracle.inspect(self.fixture([0,2,3,4]));self.assertEqual(r['comparisons'][0]['native_center_event_count'],0)
    def test_duplicate_sequence(self):
        with self.assertRaisesRegex(ValueError,'duplicate_sequence'):oracle.inspect(self.fixture([0,1,2,3,4,4]))
    def test_corruption(self):
        p=self.fixture();b=bytearray((p/'events.bin').read_bytes());b[4]^=1;(p/'events.bin').write_bytes(b)
        with self.assertRaisesRegex(ValueError,'raw_hash'):oracle.inspect(p)
    def test_truncated_record(self):
        p=self.fixture();data=(p/'events.bin').read_bytes();(p/'events.bin').write_bytes(data[:-1])
        with self.assertRaisesRegex(ValueError,'raw_hash'):oracle.inspect(p)
    def test_journal_crash_tail(self):
        p=self.fixture();with_tail=(p/'records.jsonl').read_bytes()+b'{"incomplete":';(p/'records.jsonl').write_bytes(with_tail)
        self.assertTrue(oracle.inspect(p)['truncated_journal'])
    def test_orphan_raw_retained(self):
        p=self.fixture();data=(p/'events.bin').read_bytes();(p/'events.bin').write_bytes(data+b'orphan')
        self.assertEqual(oracle.inspect(p)['unreferenced_tail_bytes'],6)
    def test_unreadable_not_zero(self):
        e=oracle.decode(bytes(oracle.SIZE));self.assertIsNone(oracle.raw(e,'center',12))
    def qualified(self):
        e=oracle.decode(bytes(oracle.SIZE));e['mxcsr']=0x1f80
        def setblob(name,data):e['blobs'][name]=dict(address=0x123456,length=len(data),ok=True,hex=data.hex())
        base=bytearray(0x30);struct.pack_into('<I',base,0x28,0x2c60e9);setblob('base',base)
        extra=bytearray(0xa0);extra[0x98:0xa0]=bytes.fromhex('f1517de43e171745');setblob('extra',extra)
        land=bytearray(0x58);struct.pack_into('<2I',land,0x50,256,0x3f59f);setblob('landscape',land)
        setblob('center',bytes.fromhex('a266f542eb858843efd19241'));setblob('translation',bytes(12));setblob('block',struct.pack('<I',10));setblob('merge',struct.pack('<I',2));setblob('scale',bytes.fromhex('0ad7233c'));setblob('floor_xy',struct.pack('<2i',1,2))
        def h(x,y):
            b=bytearray(44);b[0]=1
            for val,off in [(x,4),(y,8)]:struct.pack_into('<i',b,off,val//192);struct.pack_into('<i',b,off+16,(val%192)//12);struct.pack_into('<i',b,off+32,val%12)
            return b
        setblob('input_hierarchy',h(10464,21120));setblob('result',h(10465,21122))
        predictions=json.loads((oracle.ROOT/'docs/experiments/engine-oracle/predictions.json').read_text())
        return e,predictions,h,setblob
    def test_exact_comparison_and_mismatch(self):
        e,predictions,h,setblob=self.qualified()
        r=oracle.compare(e,predictions);self.assertTrue(r['floor_equal'] and r['grid_equal']);self.assertIn('UNASSESSED',r['saved_frame_comparison'])
        setblob('result',h(10466,21122));self.assertFalse(oracle.compare(e,predictions)['grid_equal'])
        e['status']=8;self.assertEqual(oracle.compare(e,predictions)['classification'],'UNASSESSED')
    def test_unsupported_fp(self):
        e,predictions,h,setblob=self.qualified();e['mxcsr']=0x6000
        self.assertEqual(oracle.compare(e,predictions)['reason'],'non_nearest_rounding')
    def test_subnormal_input(self):
        e,predictions,h,setblob=self.qualified();setblob('translation',struct.pack('<3f',2**-149,0,0))
        self.assertEqual(oracle.compare(e,predictions)['reason'],'subnormal_input_unqualified')
    def test_subnormal_product(self):
        e,predictions,h,setblob=self.qualified();setblob('center',struct.pack('<3f',2**-126,0,0));setblob('translation',bytes(12))
        self.assertEqual(oracle.compare(e,predictions)['reason'],'subnormal_scale_unqualified')
    def test_overflow(self):
        e,predictions,h,setblob=self.qualified();setblob('center',struct.pack('<3f',3.4e38,0,0));setblob('translation',struct.pack('<3f',3.4e38,0,0))
        self.assertEqual(oracle.compare(e,predictions)['reason'],'binary32_overflow')
    def changed_headers(self,changes):
        p=self.fixture();data=bytearray((p/'events.bin').read_bytes())
        for row,index,value in changes:struct.pack_into('<Q',data,row*oracle.SIZE+index*8,value)
        (p/'events.bin').write_bytes(data);records=[]
        for at in range(0,len(data),oracle.SIZE):
            part=data[at:at+oracle.SIZE];e=oracle.decode(part);records.append(dict(offset=at,length=oracle.SIZE,sha256=oracle.digest(part),**{k:e[k] for k in ('sequence','invocation','kind')}))
        (p/'records.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in records),encoding='utf8')
        return p
    def test_missing_grid_before(self):
        self.assertFalse(oracle.inspect(self.fixture([0,1,3,4]))['comparisons'][0]['paired'])
    def test_abnormal_exit(self):
        self.assertFalse(oracle.inspect(self.changed_headers([(4,7,5)]))['comparisons'][0]['paired'])
    def test_center_after_grid_before(self):
        self.assertFalse(oracle.inspect(self.changed_headers([(1,0,3),(2,0,2)]))['comparisons'][0]['paired'])
    def chain_fixture(self,name):
        p=self.fixture();data=(BASE/name).read_bytes();(p/'events.bin').write_bytes(data);records=[]
        for at in range(0,len(data),oracle.SIZE):
            part=data[at:at+oracle.SIZE];e=oracle.decode(part);records.append(dict(offset=at,length=oracle.SIZE,sha256=oracle.digest(part),**{k:e[k] for k in ('sequence','invocation','kind')}))
        (p/'records.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in records),encoding='utf8');return p
    def test_diagnostic_stage_matrix(self):
        for name,outcome in [('case-10.bin','QUERY_OBSERVED_ENUMERATION_NOT_OBSERVED'),('case-11.bin','ENUMERATION_OBSERVED_CALLBACK_NOT_OBSERVED'),('case-12.bin','CALLBACK_NATIVE_GRID_NOT_OBSERVED'),('case-positive.bin','CALLBACK_NATIVE_GRID_OBSERVED')]:
            r=oracle.inspect(self.chain_fixture(name));self.assertIn(outcome,[v['outcome'] for v in r['diagnostics']['scope_rows']]);self.assertTrue(r['diagnostics']['synthetic_qualification_only'])
        r=oracle.inspect(self.chain_fixture('case-0.bin'));self.assertEqual(r['diagnostics']['query_observation'],'QUERY_NOT_OBSERVED')
    def test_diagnostic_missing_parent(self):
        p=self.chain_fixture('case-positive.bin');data=bytearray((p/'events.bin').read_bytes());struct.pack_into('<Q',data,oracle.SIZE+16,999)
        events=[oracle.decode(data[i:i+oracle.SIZE]) for i in range(0,len(data),oracle.SIZE)];groups={}
        for e in events:groups.setdefault(e['invocation'],[]).append(e)
        r=oracle.diagnose(groups,dict(synthetic=True),False,p);self.assertTrue(any(not v['normal_complete'] for v in r['scope_rows'] if v['stage']=='E'))
    def test_no_health_no_native_negative(self):
        p=self.chain_fixture('case-0.bin');ready=json.loads((p/'ready.json').read_text());ready['synthetic']=False;(p/'ready.json').write_text(json.dumps(ready))
        r=oracle.inspect(p);self.assertEqual(r['diagnostics']['query_observation'],'UNQUALIFIED_NO_QUERY')
    def worker_fixture(self):
        import shutil
        p=Path(tempfile.mkdtemp(prefix='health-check-',dir=BASE));source=BASE/'health-control'/'health.jsonl';shutil.copyfile(source,p/'health.jsonl')
        ready=dict(component='SorNativePositionOracle',version='0.3.0',schema=3,event_size=oracle.SIZE)
        (p/'ready.json').write_text(json.dumps(ready),encoding='utf8')
        from datetime import datetime
        rows=[json.loads(line) for line in source.read_text(encoding='utf8').splitlines()]
        ready['qpc_frequency']=rows[0]['qpc_frequency'];(p/'ready.json').write_text(json.dumps(ready),encoding='utf8')
        return p,rows,datetime.fromisoformat(rows[-1]['health_utc'].replace('Z','+00:00'))
    def test_actual_production_health_ack(self):
        from operate import check_health
        p,rows,now=self.worker_fixture();self.assertTrue(check_health(p,'0123456789abcdef0123456789abcdef',now,False)['pass_check'])
    def test_stalled_health_and_wrong_nonce(self):
        from operate import check_health
        from datetime import timedelta
        p,rows,now=self.worker_fixture();self.assertFalse(check_health(p,None,now+timedelta(seconds=16),False)['pass_check']);self.assertFalse(check_health(p,'f'*32,now,False)['pass_check'])
    def test_health_identity_and_loss_and_stop(self):
        from operate import check_health
        for key,value in [('version','0.1.0'),('lost',1),('depth_errors',1),('health_timeouts',1),('stopping',True)]:
            p,rows,now=self.worker_fixture();rows[-1][key]=value;(p/'health.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in rows),encoding='utf8');self.assertFalse(check_health(p,None,now,False)['pass_check'])
    def test_nonce_ack_duplicate_rejected(self):
        from operate import check_health
        p,rows,now=self.worker_fixture();rows[-1]['nonce']='0123456789abcdef0123456789abcdef';(p/'health.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in rows),encoding='utf8');self.assertFalse(check_health(p,rows[-1]['nonce'],now,False)['pass_check'])
    def test_orphan_cannot_qualify_negative(self):
        p=self.fixture([0,4]);r=oracle.inspect(p)['diagnostics']
        self.assertFalse(r['worker_evidence_qualified']);self.assertEqual(r['scope_rows'][0]['outcome'],'INCOMPLETE_OR_UNHEALTHY')
    def test_incomplete_grid_diagnosis(self):
        for indices in ([0,2,4],[0,1,2,4],[0,1,3,4],[0,2,3,4]):
            r=oracle.inspect(self.fixture(indices))['diagnostics']
            self.assertFalse(r['scope_rows'][0]['normal_complete'])
            self.assertEqual(r['scope_rows'][0]['outcome'],'INCOMPLETE_OR_UNHEALTHY')
    def test_atomic_nonce_publication_and_stop_disk_floor(self):
        import operate
        from unittest.mock import patch
        p=Path(tempfile.mkdtemp(prefix='publication-',dir=BASE))
        def interleaved(pending,final):
            self.assertTrue(pending.exists());self.assertFalse(final.exists())
            self.assertFalse(any(v.name.endswith('.request') for v in p.iterdir()))
        with patch.object(operate,'guard',return_value={}):
            operate.publish_request(p,'0'*32,interleaved)
        self.assertEqual((p/('control-'+'0'*32+'.request')).read_bytes(),b'ACK\n')
        with patch.object(operate,'guard',side_effect=RuntimeError('disk_low')):
            operate.request_stop(p)
        self.assertEqual((p/'STOP').read_bytes(),b'STOP\n')
    def test_retired_zero_entered_contradiction(self):
        p=self.chain_fixture('case-0.bin');source=[json.loads(v) for v in (BASE/'health-control'/'health.jsonl').read_text().splitlines()][-1]
        ready=dict(component='SorNativePositionOracle',version='0.3.0',schema=3,event_size=oracle.SIZE,pid=1,process_creation_filetime=2,qpc_frequency=10000000,dll_sha256='synthetic-identity')
        source.update({k:ready[k] for k in ('component','version','pid','process_creation_filetime','qpc_frequency','dll_sha256')})
        source.update(health_sequence=1,stopping=True,active=[0,0,0],entered=[0,0,0],flushed_events=0,flushed_offset=0,queue_depth=0,lost=0,depth_errors=0,health_timeouts=0)
        retired=dict(ready,events=0,lost=0,depth_errors=0,health_timeouts=0,retired_utc=source['health_utc'],retired_tick=1)
        (p/'ready.json').write_text(json.dumps(ready));(p/'retired.json').write_text(json.dumps(retired))
        for entered,qualified in [([0,0,0],True),([1,0,0],False),([-1,0,0],False),([0,0],False)]:
            source['entered']=entered;(p/'health.jsonl').write_text(json.dumps(source)+'\n')
            result=oracle.inspect(p)['diagnostics'];self.assertEqual(result['worker_evidence_qualified'],qualified)
            if not qualified:self.assertEqual(result['query_observation'],'UNQUALIFIED_NO_QUERY')
    def test_recovered_worker_stall_rejected(self):
        from operate import check_health
        p,rows,now=self.worker_fixture()
        for row in rows[1:]:row['qpc']+=rows[0]['qpc_frequency']*16
        (p/'health.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in rows))
        self.assertFalse(check_health(p,None,now,False)['pass_check'])
    def test_counter_regression_rejected(self):
        from operate import check_health
        p,rows,now=self.worker_fixture();rows[0]['entered']=[2,0,0];rows[-1]['entered']=[1,0,0]
        (p/'health.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in rows))
        self.assertFalse(check_health(p,None,now,False)['pass_check'])
if __name__=='__main__':unittest.main(verbosity=2)
