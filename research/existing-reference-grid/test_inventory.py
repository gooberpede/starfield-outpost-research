# SPDX-License-Identifier: GPL-3.0-or-later
"""Original offline cooperative-inventory fixtures; no game/process access.
Actual receipt parsing, nonce files and health validator on synthetic copies.
"""
from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import environment as e
import procedure as p
REAL_PROCESS_ID=p.native.process_identity

BASE=p.ROOT/'.local-work/existing-reference-grid/fixtures';BASE.mkdir(parents=True,exist_ok=True)

class InventoryTests(unittest.TestCase):
    def setUp(self):
        self.root=Path(tempfile.mkdtemp(dir=BASE));self.live=self.root/'live';self.live.mkdir()
        self.session=self.live/'session-fixture';self.session.mkdir();self.rows=[]
        for i,name in enumerate(('Starfield.exe','sfse_1_16_244.dll','SorNativePositionOracle.dll','gameoverlayrenderer64.dll','nvspcap64.dll')):
            path=self.root/name;path.write_bytes(('synthetic '+name).encode())
            self.rows.append(dict(path=str(path),base=hex(0x140000000+i*0x100000),size=4096,sha256=p.sha(path),hash_status='READ_OK',role='recorded_no_blanket_allowlist'))
        self.lock=dict(version='0.4.0',schema=4,module_inventory_source='040_WORKER_COOPERATIVE_INVENTORY',live_root=str(self.live),game_sha256=self.rows[0]['sha256'],sfse_sha256=self.rows[1]['sha256'],dll_sha256=self.rows[2]['sha256'])
        self.ready=dict(component='SorNativePositionOracle',version='0.4.0',schema=4,event_size=17768,pid=123,process_creation_filetime=456,module_base='0x140000000',qpc_frequency=1000,**{k:self.lock[k] for k in ('game_sha256','sfse_sha256','dll_sha256')})
        (self.session/'ready.json').write_text(json.dumps(self.ready),encoding='utf8')
        self.inventory();self.health=[];self.append_health('')
        for target,name,value in [(p.native,'process_identity',lambda pid:456),(e,'guard',lambda:{}),(p.native,'guard',lambda:{})]:
            m=patch.object(target,name,side_effect=value);m.start();self.addCleanup(m.stop)
        self.real_publish=p.native.publish_request
        m=patch.object(p.native,'publish_request',side_effect=self.respond);m.start();self.addCleanup(m.stop)
        m=patch.object(e,'module_snapshot',side_effect=PermissionError(5,'Access denied fixture'));m.start();self.addCleanup(m.stop)
    def inventory(self,serial=1):
        (self.session/f'modules-{serial}.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in self.rows),encoding='utf8')
    def append_health(self,nonce):
        row=self.ready|dict(health_sequence=len(self.health)+1,health_utc=datetime.now(timezone.utc).isoformat(),qpc=(len(self.health)+1)*1000,nonce=nonce,flushed_events=0,flushed_offset=0,queue_depth=0,lost=0,depth_errors=0,health_timeouts=0,stopping=False,active=[0,0,0],entered=[0,0,0])
        self.health.append(row)
        (self.session/'health.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in self.health),encoding='utf8')
    def respond(self,session,nonce):
        self.real_publish(session,nonce);self.append_health(nonce)
    def test_cooperative_success_despite_external_access_denied(self):
        report=e.modules(self.lock,self.session)
        self.assertTrue(report['pass_check']);self.assertEqual(len(report['modules']),5)
        self.assertEqual(report['source'],'040_WORKER_COOPERATIVE_INVENTORY')
        self.assertEqual(report['ACK_health_sequence'],2);self.assertEqual(report['inventory_serial'],1)
        self.assertIn('A-B-A',report['limits']);self.assertTrue((self.session/('control-'+report['nonce']+'.request')).is_file())
        e.module_snapshot.assert_not_called()
    def test_unreadable_nonessential_module_is_noncritical(self):
        self.rows[-1]['hash_status']='UNREADABLE_ASSESS_SPECIFIC_RISK';self.rows[-1]['sha256']='';self.inventory()
        report=e.modules(self.lock,self.session);self.assertTrue(report['pass_check'])
        self.assertIn('UNREADABLE_NONCRITICAL',report['modules'][-1]['assessment'])
    def test_external_runtime_required_identity(self):
        path=self.root/'msvcp140.dll';path.write_bytes(b'original synthetic runtime identity')
        self.lock['external_runtime_prerequisites']={str(path):p.sha(path)}
        with self.assertRaisesRegex(ValueError,'inventory_required_identity:msvcp140.dll'):
            e.read_inventory(self.session/'modules-1.jsonl',self.lock,self.ready)
        self.rows.append(dict(path=str(path),base='0x160000000',size=4096,sha256=p.sha(path),hash_status='READ_OK'))
        self.inventory();rows,_=e.read_inventory(self.session/'modules-1.jsonl',self.lock,self.ready)
        self.assertEqual(len(rows),6)
        self.rows[-1]['hash_status']='UNREADABLE';self.inventory()
        with self.assertRaisesRegex(ValueError,'inventory_required_identity:msvcp140.dll'):
            e.read_inventory(self.session/'modules-1.jsonl',self.lock,self.ready)
    def test_new_complete_inventory_before_ACK_selected(self):
        def respond(session,nonce):self.inventory(2);self.respond(session,nonce)
        with patch.object(p.native,'publish_request',side_effect=respond):report=e.modules(self.lock,self.session)
        self.assertEqual(report['pre_ACK_inventory_serial'],1);self.assertEqual(report['inventory_serial'],2)
    def test_ACK_sequence_is_matching_row_not_later_heartbeat(self):
        def respond(session,nonce):self.respond(session,nonce);self.append_health('')
        with patch.object(p.native,'publish_request',side_effect=respond):report=e.modules(self.lock,self.session)
        self.assertEqual(report['ACK_health_sequence'],2);self.assertEqual(len(self.health),3)
    def test_missing_and_gapped_inventories_fail(self):
        (self.session/'modules-1.jsonl').unlink()
        with self.assertRaisesRegex(ValueError,'sequence'):e.modules(self.lock,self.session)
        self.inventory(3)
        with self.assertRaisesRegex(ValueError,'sequence'):e.modules(self.lock,self.session)
    def test_partial_empty_oversized_inventory(self):
        file=self.session/'modules-1.jsonl'
        for data in (b'',b'{}',b'x'*(1024**2+1)):
            file.write_bytes(data)
            with self.assertRaises(ValueError):e.modules(self.lock,self.session)
    def test_duplicate_and_missing_required_rows(self):
        original=list(self.rows)
        for rows in (original+[original[0]],original[:2],original[1:]):
            self.rows=rows;self.inventory()
            with self.assertRaises(ValueError):e.modules(self.lock,self.session)
    def test_hash_unreadable_drift_and_game_base(self):
        for key,value in [('hash_status','UNREADABLE_ASSESS_SPECIFIC_RISK'),('sha256','0'*64),('base','0x123456')]:
            old=self.rows[0][key];self.rows[0][key]=value;self.inventory()
            with self.assertRaises(ValueError):e.modules(self.lock,self.session)
            self.rows[0][key]=old
    def test_wrong_session_identity(self):
        self.ready['dll_sha256']='0'*64;(self.session/'ready.json').write_text(json.dumps(self.ready),encoding='utf8')
        with self.assertRaisesRegex(ValueError,'session_identity'):e.modules(self.lock,self.session)
    def test_old_contract_cannot_silently_switch_provenance(self):
        del self.lock['module_inventory_source']
        with self.assertRaisesRegex(ValueError,'contract_not_pinned'):e.modules(self.lock,self.session)
        self.assertFalse(list(self.session.glob('control-*.request')))
    def test_retired_failed_stale_health_never_publishes(self):
        for name in ('STOP','retired.json','failure.json'):
            file=self.session/name;file.write_text('{}',encoding='utf8')
            with self.assertRaisesRegex(ValueError,'initial_health'):e.modules(self.lock,self.session)
            file.unlink()
        self.health[0]['health_utc']='2000-01-01T00:00:00+00:00'
        (self.session/'health.jsonl').write_text(json.dumps(self.health[0])+'\n',encoding='utf8')
        with self.assertRaisesRegex(ValueError,'initial_health'):e.modules(self.lock,self.session)
        self.assertFalse(list(self.session.glob('control-*.request')))
    def test_inventory_changed_during_validation(self):
        original=e.read_inventory
        def changing(*args):result=original(*args);self.inventory(2);return result
        with patch.object(e,'read_inventory',side_effect=changing):
            with self.assertRaisesRegex(ValueError,'changed_during_read'):e.modules(self.lock,self.session)
    def test_nonce_timeout_and_late_ACK(self):
        clock=[0]
        with patch.object(p.native,'publish_request',side_effect=self.real_publish),patch.object(e.time,'monotonic',side_effect=lambda:clock[0]),patch.object(e.time,'sleep',side_effect=lambda n:clock.__setitem__(0,clock[0]+n)):
            with self.assertRaisesRegex(ValueError,'inventory_ACK'):e.modules(self.lock,self.session)
        with patch.object(e.time,'monotonic',side_effect=[0,16]):
            with self.assertRaisesRegex(ValueError,'ACK_late'):e.modules(self.lock,self.session)
    def test_nonlocal_and_reparse_inputs(self):
        self.rows[0]['path']='\\\\server\\share\\Starfield.exe';self.inventory()
        with self.assertRaisesRegex(ValueError,'nonlocal'):e.modules(self.lock,self.session)
        with patch.object(Path,'is_junction',return_value=True):
            with self.assertRaisesRegex(ValueError,'reparse'):e.modules(self.lock,self.session)
    def test_process_identity_failure(self):
        with patch.object(p.native,'process_identity',return_value=999):
            with self.assertRaisesRegex(ValueError,'initial_health'):e.modules(self.lock,self.session)
    def test_final_process_identity_and_inventory_changes(self):
        with patch.object(p.native,'process_identity',side_effect=[456,456,999]):
            with self.assertRaisesRegex(ValueError,'final_health'):e.modules(self.lock,self.session)
        actual=p.native.check_health;calls=[0]
        def changed(*args):
            result=actual(*args);calls[0]+=1
            if calls[0]==3:self.inventory(2)
            return result
        with patch.object(p.native,'check_health',side_effect=changed):
            with self.assertRaisesRegex(ValueError,'changed_after_health'):e.modules(self.lock,self.session)
    def test_real_bounded_helper_with_controlled_python_fixture(self):
        # The ONLY process queried is this test interpreter. Child is our reader,
        # parent thread supplies synthetic worker receipts; never game/live capture.
        import os,threading,time
        self.ready['pid']=os.getpid();self.ready['process_creation_filetime']=REAL_PROCESS_ID(os.getpid())
        (self.session/'ready.json').write_text(json.dumps(self.ready),encoding='utf8')
        self.health=[];self.append_health('')
        lock=self.root/'lock.json';lock.write_text(json.dumps(self.lock),encoding='utf8')
        stop=threading.Event();errors=[]
        def worker():
            try:
                while not stop.is_set():
                    requests=list(self.session.glob('control-*.request'))
                    if requests:
                        nonce=requests[0].name[8:40]
                        row=self.health[0]|dict(health_sequence=2,qpc=2000,nonce=nonce,health_utc=datetime.now(timezone.utc).isoformat())
                        with (self.session/'health.jsonl').open('ab') as f:f.write((json.dumps(row)+'\n').encode());f.flush();os.fsync(f.fileno())
                        return
                    time.sleep(0.02)
            except Exception as exc:errors.append(str(exc))
        thread=threading.Thread(target=worker);thread.start()
        try:
            self.assertTrue(e.bounded_modules(lock,p.sha(lock),self.session,self.root/'bounded-report.json'))
            self.assertFalse(errors)
            self.assertEqual(p.read(self.root/'bounded-report.json')['source'],'040_WORKER_COOPERATIVE_INVENTORY')
        finally:stop.set();thread.join(timeout=2)

if __name__=='__main__':unittest.main(verbosity=2)
