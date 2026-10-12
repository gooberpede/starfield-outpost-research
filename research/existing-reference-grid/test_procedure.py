# SPDX-License-Identifier: GPL-3.0-or-later
import hashlib
import json
from pathlib import Path
import struct
import tempfile
import unittest
from unittest.mock import patch
import zipfile
import procedure as p

def digest(b):return hashlib.sha256(b).hexdigest()
class Procedures(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name);self.game=self.root/'game';self.plugin=self.game/'Data/SFSE/Plugins';self.plugin.mkdir(parents=True)
  self.lock=dict(game_dir=str(self.game),runtime_essential=['Data/SFSE/Plugins/SorNativePositionOracle.dll'],package={'Data/SFSE/Plugins/SorNativePositionOracle.dll':digest(b'candidate'),'ResearchNotices/READ-ME.txt':digest(b'optional')},installed_loader={'sfse_loader.exe':digest(b'loader')})
  (self.plugin/'SorNativePositionOracle.dll').write_bytes(b'candidate');(self.game/'sfse_loader.exe').write_bytes(b'loader')
 def tearDown(self):self.tmp.cleanup()
 def test_dll_only_no_text_config_or_waiver(self):
  self.assertEqual(len(p.installation(self.lock,'deployed')),1)
 def test_optional_text_absent_or_modified_is_accepted(self):
  (self.plugin/'READ-ME.txt').write_bytes(b'other');(self.plugin/'SorNativePositionOracle.config').write_bytes(b'obsolete inert')
  p.installation(self.lock,'deployed')
 def test_unfamiliar_dll_inventory_not_automatic_conflict(self):
  (self.plugin/'Unrelated.dll').write_bytes(b'x');self.assertEqual(len(p.installation(self.lock,'deployed')),2)
 def test_competing_observer(self):
  (self.plugin/'SorBeaconObserver.dll').write_bytes(b'x')
  with self.assertRaisesRegex(ValueError,'competing_observer'):p.installation(self.lock,'deployed')
 def test_installed_dll_hash(self):
  (self.plugin/'SorNativePositionOracle.dll').write_bytes(b'wrong')
  with self.assertRaisesRegex(ValueError,'installed_package'):p.installation(self.lock,'deployed')
 def test_archive_effective_deployed_payload_independent(self):
  archive=self.root/'candidate.zip';self.lock['zip']=str(archive)
  with zipfile.ZipFile(archive,'x') as z:z.writestr('Data/SFSE/Plugins/SorNativePositionOracle.dll',b'candidate');z.writestr('ResearchNotices/READ-ME.txt',b'optional')
  p.archive_check(self.lock);p.installation(self.lock,'deployed')
  self.lock['package']['ResearchNotices/READ-ME.txt']=digest(b'corrupt')
  with self.assertRaisesRegex(ValueError,'archive_member_hash'):p.archive_check(self.lock)
 def test_postflight_only_runtime_essential_removal(self):
  (self.plugin/'SorNativePositionOracle.dll').unlink();(self.plugin/'READ-ME.txt').write_bytes(b'review note');p.installation(self.lock,'postflight')
 def test_protected_pin_drift(self):
  f=self.root/'protected.txt';f.write_bytes(b'protected');self.lock['pins']={str(f):digest(b'protected')};p.pins(self.lock);f.write_bytes(b'changed')
  with self.assertRaisesRegex(ValueError,'protected_or_source_hash'):p.pins(self.lock)
 def test_cadence_gap_10s_and_health_failure(self):
  session=self.root/'session';session.mkdir()
  with patch.object(p,'guard',return_value={'C':40000000000,'D':40000000000}):
   self.assertTrue(p.monitor_sample(session,self.lock,1,4,lambda s:dict(pass_check=True))['pass_check'])
   with self.assertRaisesRegex(ValueError,'monitor_gap'):p.monitor_sample(session,self.lock,1,11.1,lambda s:dict(pass_check=True))
   with self.assertRaisesRegex(ValueError,'health:'):p.monitor_sample(session,self.lock,1,4,lambda s:dict(pass_check=False,reason='stale'))
 def test_disk_failure_stops_poll(self):
  with patch.object(p,'guard',side_effect=RuntimeError('disk_guard')):
   with self.assertRaisesRegex(RuntimeError,'disk_guard'):p.monitor_sample(self.root,self.lock,1,4)
 def test_future_admission_15_calls_and_wrong_candidate(self):
  live=self.root/'live';live.mkdir();s=live/'session-fixture';s.mkdir();run=self.root/'run';run.mkdir();self.lock.update(live_root=str(live),dll_sha256=digest(b'candidate'),game_sha256='game',sfse_sha256='sfse')
  ready=dict(component='SorNativePositionOracle',version='0.4.0',schema=4,event_size=17768,dll_sha256=self.lock['dll_sha256'],game_sha256='game',sfse_sha256='sfse',grid_channel=True,center_channel=False,heartbeat_ms=1000,health_deadline_ms=15000,pid=1,process_creation_filetime=2,module_base='140000000',qpc_frequency=10000000,startup_wait_ms=0)
  edits=[];relays=[];calls=[];base=int(ready['module_base'],16)
  for i in range(15):
   rva=0x100+i*16;rv=base+0x10000+i*16;target=0x20000000+i*16;original=digest(b'original'+bytes([i]));calls.append(dict(rva=rva,sha256=original));edits.append(dict(runtime_va=hex(base+rva),length=5,original_sha256=original,installed_sha256=digest(b'\xe8'+struct.pack('<i',rv-(base+rva+5)))));relays.append(dict(runtime_va=hex(rv),target_va=hex(target),length=14,sha256=digest(b'\xff\x25'+bytes(4)+struct.pack('<Q',target)),protection='PAGE_EXECUTE_READ'))
  self.lock['calls']=calls;admit=dict(ready,owned_sites_original=True,sole_thread_observed=True,standard_overlays_accepted=True,patches_installed_at_receipt=False);patches=dict(ready,patches=edits,relays=relays)
  for name,obj in [('ready.json',ready),('admission.json',admit),('patches.json',patches)]: (s/name).write_text(json.dumps(obj))
  (s/'modules-pre-edit.jsonl').write_text(json.dumps(dict(path='SorNativePositionOracle.dll',sha256=self.lock['dll_sha256'],base='20000000',size=4096))+'\n');(run/'audit.json').write_text(json.dumps(dict(mode='deployed',pass_check=True,prior_sessions=[])))
  self.assertTrue(p.admission(self.lock,s,run)['pass_check']);ready['center_channel']=True;(s/'ready.json').write_text(json.dumps(ready))
  with self.assertRaisesRegex(ValueError,'ready_identity'):p.admission(self.lock,s,run)
if __name__=='__main__':unittest.main(verbosity=2)
