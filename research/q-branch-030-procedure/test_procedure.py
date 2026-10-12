# SPDX-License-Identifier: GPL-3.0-or-later
"""Original fixture-only operational tests. No game or live process handle.
Temporary copies/ACK/STOP/journals remain under ignored procedure fixtures.
"""
from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
import struct
import tempfile
import unittest
from unittest.mock import patch
import procedure as p
import environment as env

BASE=p.ROOT/'.local-work/q-branch-030-procedure/fixtures';BASE.mkdir(parents=True,exist_ok=True)
def dump(path,value):path.write_text(json.dumps(value),encoding='utf8')
def digest(b):return hashlib.sha256(b).hexdigest()

class ProcedureTests(unittest.TestCase):
    def setUp(self):
        self.root=Path(tempfile.mkdtemp(dir=BASE));self.live=self.root/'live';self.live.mkdir();self.session=self.live/'session-fixture';self.session.mkdir();self.run=self.root/'run';self.run.mkdir()
        self.no_process=patch.object(p.native,'process_identity',side_effect=AssertionError('NO LIVE PROCESS HANDLE AUTHORITY'));self.no_process.start();self.addCleanup(self.no_process.stop)
        self.disk=patch.object(p,'guard',return_value={'C:/':50000000000,'D:/':50000000000});self.disk.start();self.addCleanup(self.disk.stop)
        self.lock=dict(version='0.3.0',schema=3,live_root=str(self.live),dll_sha256='d'*64,game_sha256='g'*64,sfse_sha256='s'*64,calls=[])
        self.ready=dict(component='SorNativePositionOracle',version='0.3.0',schema=3,event_size=17768,dll_sha256='d'*64,game_sha256='g'*64,sfse_sha256='s'*64,pid=1,process_creation_filetime=2,module_base='0x140000000',qpc_frequency=1000,grid_channel=True,center_channel=True,heartbeat_ms=1000,health_deadline_ms=15000,startup_wait_ms=10)
        dump(self.session/'ready.json',self.ready)
        dump(self.session/'admission.json',self.ready|dict(owned_sites_original=True,sole_thread_observed=True,standard_overlays_accepted=True,patches_installed_at_receipt=False))
        edits=[];relays=[]
        for i in range(11):
            rva=0x100+i*0x20;relay=0x140100000+i*16;target=0x180000000+i*16
            original=digest(bytes([i])*5);self.lock['calls'].append(dict(rva=rva,sha256=original))
            edits.append(dict(runtime_va=hex(0x140000000+rva),length=5,original_sha256=original,installed_sha256=digest(b'\xe8'+struct.pack('<i',relay-(0x140000000+rva+5)))))
            relays.append(dict(runtime_va=hex(relay),target_va=hex(target),length=14,sha256=digest(b'\xff\x25'+bytes(4)+struct.pack('<Q',target)),protection='PAGE_EXECUTE_READ'))
        for i in range(2):edits.append(dict(runtime_va=hex(0x140000000+0x4b916f0+i*8),length=8,original_sha256=digest(struct.pack('<Q',0x140000000+0xad8ec0)),installed_sha256='x'*64))
        self.patch=self.ready|dict(patches=edits,relays=relays);dump(self.session/'patches.json',self.patch)
        modules=[dict(path='SorNativePositionOracle.dll',base='0x180000000',size=4096,sha256='d'*64),dict(path='gameoverlayrenderer64.dll',base='0x190000000',size=4096,sha256='o'*64),dict(path='nvspcap64.dll',base='0x200000000',size=4096,sha256='n'*64)]
        (self.session/'modules-pre-edit.jsonl').write_text(''.join(json.dumps(m)+'\n' for m in modules),encoding='utf8')
        dump(self.run/'audit.json',dict(mode='deployed',pass_check=True,prior_sessions=[],save_inventory={}))
        dump(self.run/'operator-confirmation.json',dict(vortex_profile_confirmed=True,no_competing_native_instrument=True,pre_edit_modules_assessed=True))
    def test_admission_and_accepted_overlays(self):
        result=p.admission(self.lock,self.session,self.run);self.assertTrue(result['pass_check']);self.assertEqual(len(result['modules']),3)
    def test_wrong_identity_and_sites(self):
        original=json.loads(json.dumps(self.patch))
        for mutate in (lambda r:r.update(schema=2),lambda r:r['patches'].pop(),lambda r:r['patches'][0].update(original_sha256='wrong'),lambda r:r['relays'][0].update(target_va='0x1234'),lambda r:r['patches'][-1].update(installed_sha256='different')):
            row=json.loads(json.dumps(original));mutate(row);dump(self.session/'patches.json',row)
            with self.assertRaises(ValueError):p.admission(self.lock,self.session,self.run)
    def test_old_session_refused_without_STOP(self):
        dump(self.run/'audit.json',dict(mode='deployed',pass_check=True,prior_sessions=['session-fixture']))
        with self.assertRaises(ValueError):p.monitor(self.lock,self.session,self.run)
        self.assertFalse((self.session/'STOP').exists())
    def test_admission_failure_requests_STOP(self):
        self.ready['dll_sha256']='wrong';dump(self.session/'ready.json',self.ready)
        self.assertFalse(p.monitor(self.lock,self.session,self.run));self.assertEqual((self.session/'STOP').read_bytes(),b'STOP\n')
    def test_confirmation_failure_requests_STOP(self):
        (self.run/'operator-confirmation.json').unlink() # disposable fixture only
        self.assertFalse(p.monitor(self.lock,self.session,self.run));self.assertTrue((self.session/'STOP').exists())
    def test_nonce_setup_failure_requests_STOP(self):
        with patch.object(p.native,'publish_request',side_effect=OSError('fixture write failure')):
            self.assertFalse(p.monitor(self.lock,self.session,self.run))
        self.assertTrue((self.session/'STOP').exists())
    def test_monitor_disk_health_cadence_failure(self):
        good=lambda s:dict(pass_check=True)
        self.assertTrue(p.monitor_sample(self.session,self.lock,0,9.9,good)['pass_check'])
        with self.assertRaisesRegex(ValueError,'gap'):p.monitor_sample(self.session,self.lock,0,10.1,good)
        with patch.object(p,'guard',side_effect=OSError('disk query failed')):
            with self.assertRaises(OSError):p.monitor_sample(self.session,self.lock,0,3,good)
        with self.assertRaisesRegex(ValueError,'health'):p.monitor_sample(self.session,self.lock,0,3,lambda s:dict(pass_check=False,reason='stale_or_failed_health'))
        (self.session/'failure.json').write_text('{}',encoding='utf8')
        with self.assertRaisesRegex(ValueError,'worker_failure'):p.monitor_sample(self.session,self.lock,0,3,good)
    def test_full_mock_monitor_ACK_STOP_and_late_ACK(self):
        clock=[0.0]
        def sleep(seconds):
            clock[0]+=seconds
            p.native.request_stop(self.session);dump(self.session/'retired.json',{})
        with patch.object(p.native,'guard',return_value={}),patch.object(p,'monitor_sample',return_value=dict(pass_check=True)),patch.object(p.native,'check_health',return_value=dict(pass_check=True)),patch.object(p.time,'monotonic',side_effect=lambda:clock[0]),patch.object(p.time,'sleep',side_effect=sleep):
            self.assertTrue(p.monitor(self.lock,self.session,self.run))
        self.assertTrue(p.read(self.run/'monitor-ready.json')['pass_check']);self.assertTrue(p.read(self.run/'monitor-ended.json')['initial_ACK'])
        # Fresh independent fixture for the late-ACK path, no deletion of originals.
        self.setUp();clock=[0.0]
        def late(*unused):clock[0]=16.0;return dict(pass_check=True)
        with patch.object(p.native,'guard',return_value={}),patch.object(p,'monitor_sample',return_value=dict(pass_check=True)),patch.object(p.native,'check_health',side_effect=late),patch.object(p.time,'monotonic',side_effect=lambda:clock[0]),patch.object(p.time,'sleep',side_effect=lambda s:clock.__setitem__(0,clock[0]+s)):
            self.assertFalse(p.monitor(self.lock,self.session,self.run))
        self.assertFalse((self.run/'monitor-ready.json').exists());self.assertTrue((self.session/'STOP').exists())
    def test_missing_dirs_and_lock_drift(self):
        with self.assertRaisesRegex(ValueError,'directory'):p.saves(self.root/'absent')
        lock=self.root/'lock.json';dump(lock,self.lock)
        self.assertEqual(p.lock_file(lock,p.sha(lock))['schema'],3)
        with self.assertRaisesRegex(ValueError,'lock_hash'):p.lock_file(lock,'wrong')
        self.lock['pins']={str(self.root/'missing'):'x'}
        with self.assertRaisesRegex(ValueError,'protected'):p.pins(self.lock)
    def test_session_junction_before_resolve(self):
        # Inject a reparse identity instead of needing privileged OS link creation.
        with patch.object(Path,'is_junction',return_value=True):
            with self.assertRaisesRegex(ValueError,'reparse'):p.session_path(self.lock,self.session)
        with self.assertRaises(ValueError):p.session_path(self.lock,self.root)
    def test_checkpoint_copy_never_overwrites_existing(self):
        self.lock['save_dir']=str(self.root);self.lock['pins']={}
        source=self.root/'fresh.sfs';source.write_bytes(b'original synthetic save')
        p.checkpoint(self.lock,self.run,source,'Q030-before');self.assertEqual(source.read_bytes(),b'original synthetic save')
        copy=self.run/'checkpoints/Q030-before/fresh.sfs';self.assertEqual(copy.read_bytes(),source.read_bytes())
        with self.assertRaises(FileExistsError):p.checkpoint(self.lock,self.run,source,'Q030-before')
        dump(self.run/'audit.json',dict(save_inventory={str(source):{}}))
        with self.assertRaisesRegex(ValueError,'preexisting'):p.checkpoint(self.lock,self.run,source,'Q030-after')
    def test_ACK_STOP_durable_disposable(self):
        # Production unchanged helper; filesystem writes are fixture-only.
        with patch.object(p.native,'guard',return_value={}):p.native.publish_request(self.session,'a'*32)
        self.assertEqual((self.session/('control-'+'a'*32+'.request')).read_bytes(),b'ACK\n')
        with patch.object(p.native,'guard',side_effect=OSError('below floor')):p.native.request_stop(self.session)
        self.assertEqual((self.session/'STOP').read_bytes(),b'STOP\n')
    def test_healthy_and_unhealthy_zero_event_inspector(self):
        stamp=datetime.now(timezone.utc).isoformat();self.ready.update(utc=stamp)
        dump(self.session/'ready.json',self.ready);(self.session/'events.bin').write_bytes(b'');(self.session/'records.jsonl').write_bytes(b'')
        health=self.ready|dict(health_sequence=1,qpc=1000,flushed_events=0,flushed_offset=0,queue_depth=0,lost=0,health_timeouts=0,depth_errors=0,stopping=True,active=[0,0,0],entered=[0,0,0],health_utc=stamp,nonce='')
        (self.session/'health.jsonl').write_text(json.dumps(health)+'\n',encoding='utf8')
        dump(self.session/'retired.json',self.ready|dict(retired_utc=stamp,retired_tick=1,events=0,lost=0,depth_errors=0,health_timeouts=0))
        report=p.inspect(self.session);self.assertTrue(report['diagnostics']['worker_evidence_qualified']);self.assertEqual(report['diagnostics']['query_observation'],'QUERY_NOT_OBSERVED')
        health['lost']=1;(self.session/'health.jsonl').write_text(json.dumps(health)+'\n',encoding='utf8')
        self.assertFalse(p.inspect(self.session)['diagnostics']['worker_evidence_qualified'])
    def healthy_fixture(self):
        self.test_healthy_and_unhealthy_zero_event_inspector()
        row=p.read(self.session/'health.jsonl');row['lost']=0
        (self.session/'health.jsonl').write_text(json.dumps(row)+'\n',encoding='utf8')
    def test_postflight_composition_success(self):
        self.healthy_fixture();out=self.root/'postflight';out.mkdir()
        with patch.object(p,'audit',return_value=dict(save_inventory={})):
            self.assertTrue(p.postflight(self.lock,self.session,self.run,out))
        self.assertTrue(p.read(out/'inspection.json')['diagnostics']['worker_evidence_qualified'])
        self.assertEqual(p.read(out/'branch-analysis.json')['native_equivalence'],'NOT_TESTED')
    def test_postflight_protected_checkpoint_and_inspector_failures(self):
        self.healthy_fixture();self.lock['save_dir']=str(self.root);self.lock['pins']={}
        source=self.root/'fresh.sfs';source.write_bytes(b'fixture save');p.checkpoint(self.lock,self.run,source,'Q030-before')
        source.write_bytes(b'tampered fixture');out=self.root/'postflight-checkpoint';out.mkdir()
        with patch.object(p,'audit',return_value=dict(save_inventory={})):
            with self.assertRaisesRegex(ValueError,'checkpoint_integrity'):p.postflight(self.lock,self.session,self.run,out)
        with patch.object(p,'audit',side_effect=ValueError('protected_or_source_hash')):
            with self.assertRaisesRegex(ValueError,'protected'):p.postflight(self.lock,self.session,self.run,self.root/'unused')
        # A separate fixture checks the real inspector's failed worker composition.
        self.setUp();self.test_healthy_and_unhealthy_zero_event_inspector();out=self.root/'postflight-unhealthy';out.mkdir()
        with patch.object(p,'audit',return_value=dict(save_inventory={})):
            self.assertFalse(p.postflight(self.lock,self.session,self.run,out))
    def test_environment_absent_unreadable_and_bounded_modules(self):
        game=self.root/'game';game.mkdir();(game/'Data').mkdir();lock=dict(game_dir=str(game))
        config=self.root/'Plugins.txt';config.write_text('*fixture.esm\n',encoding='utf8')
        self.assertTrue(env.files(lock,self.root/'files.json',[config,self.root/'absent.ini']))
        rows=p.read(self.root/'files.json')['rows'];self.assertEqual([r['state'] for r in rows],['PRESENT','ABSENT'])
        with patch.object(Path,'read_bytes',side_effect=PermissionError('fixture unreadable')):
            self.assertFalse(env.files(lock,self.root/'files-failed.json',[config]))
        import subprocess
        with patch.object(env,'guard',return_value={}):
            self.assertFalse(env.bounded_modules('lock','sha',self.session,self.root/'module-timeout.json',runner=lambda *a,**k:(_ for _ in ()).throw(subprocess.TimeoutExpired('fixture',30))))
            self.assertTrue(env.bounded_modules('lock','sha',self.session,self.root/'module-ok.json',runner=lambda *a,**k:subprocess.CompletedProcess([],0,json.dumps(dict(pass_check=True,modules=[])),'')))
    def test_module_binding_self_fixture_only(self):
        # Exercise actual Toolhelp ABI against THIS test interpreter, never Starfield.
        import os
        rows=env.module_snapshot(os.getpid());self.assertTrue(rows)
        self.assertTrue(any(Path(r['path']).name.lower().startswith('python') for r in rows))
        self.assertTrue(all(int(r['base'],16)>0 and r['size']>0 for r in rows))
if __name__=='__main__':unittest.main(verbosity=2)
