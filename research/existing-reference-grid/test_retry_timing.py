# SPDX-License-Identifier: GPL-3.0-or-later
"""Original offline controls for user timing correction; no game/process access."""
import json
import os
from pathlib import Path
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from unittest.mock import patch
import retry_monitor as m


class TimingTests(unittest.TestCase):
    def test_external_gap_is_warning_after_actual_health_passes(self):
        with tempfile.TemporaryDirectory() as folder,patch.object(m.p,'guard',return_value={}):
            result,reasons=m.sample(Path(folder),{},1,100,lambda s:dict(pass_check=True))
            self.assertTrue(result['pass_check']);self.assertIn('external_sample_gap_over_10s',reasons)

    def test_stale_worker_is_not_a_timing_waiver(self):
        with tempfile.TemporaryDirectory() as folder,patch.object(m.p,'guard',return_value={}):
            with self.assertRaisesRegex(ValueError,'health:stale'):
                m.sample(Path(folder),{},1,100,lambda s:dict(pass_check=False,reason='stale'))

    def test_disk_and_output_remain_hard(self):
        with tempfile.TemporaryDirectory() as folder:
            s=Path(folder)
            with patch.object(m.p,'guard',side_effect=RuntimeError('disk_guard')):
                with self.assertRaisesRegex(RuntimeError,'disk_guard'):m.sample(s,{},1,100)
            with (s/'events.bin').open('wb') as f:f.truncate(2*1024**3+1)
            with patch.object(m.p,'guard',return_value={}):
                with self.assertRaisesRegex(ValueError,'output_stop'):m.sample(s,{},1,100)

    def test_healthy_overruns_never_automatically_STOP(self):
        self.simulation(False,False)

    def test_missing_ACK_never_publishes_ready_or_aborts_for_clock(self):
        self.simulation(True,False)

    def test_genuine_worker_failure_requests_STOP(self):
        self.simulation(False,True)

    def test_aged_ACK_with_fresh_worker_rechallenges_without_STOP(self):
        self.simulation(False,False,True)

    def simulation(self,missing_ack,fail_health,aged_ack=False):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);live=root/'live';live.mkdir();s=live/'session-test';s.mkdir();run=root/'run';run.mkdir()
            def put(path,obj):path.write_text(json.dumps(obj)+'\n',encoding='utf8')
            put(run/'audit.json',dict(mode='deployed',prior_sessions=[]))
            put(run/'operator-confirmation.json',dict(vortex_profile_confirmed=True,no_competing_native_instrument=True,pre_edit_modules_assessed=True))
            wall=2000000000;ready_at=wall-121
            put(s/'ready.json',dict(process_creation_filetime=int((ready_at-151+11644473600)*10000000)))
            os.utime(s/'ready.json',(ready_at,ready_at))
            for n in ('admission.json','patches.json','modules-pre-edit.jsonl'):(s/n).write_text('{}\n',encoding='utf8')
            (s/'health.jsonl').write_text('{}\n',encoding='utf8')
            clock=[0];sleeps=[0];challenges=[0]
            def sleep(seconds):
                clock[0]+=610;sleeps[0]+=1
                if sleeps[0]>=3:(s/'STOP').write_text('user STOP');put(s/'retired.json',{})
            def health(session,nonce=None):
                if fail_health:return dict(pass_check=False,reason='stale_or_failed_health')
                if nonce:
                    challenges[0]+=1
                    if aged_ack and challenges[0]==1:
                        put(s/'health.jsonl',dict(nonce=nonce,health_utc=(datetime.now(timezone.utc)-timedelta(seconds=20)).isoformat(),stopping=False,lost=0,depth_errors=0,health_timeouts=0))
                        return dict(pass_check=False,reason='stale_or_failed_health')
                    if missing_ack or challenges[0]==1:return dict(pass_check=False,reason='nonce_not_acknowledged_once')
                return dict(pass_check=True)
            def stop(session):
                (s/'STOP').write_text('hard failure STOP');put(s/'retired.json',{})
            with patch.object(m.p,'guard',return_value={}),patch.object(m.p,'admission',return_value={'pass_check':True}),patch.object(m.time,'time',return_value=wall),patch.object(m.time,'monotonic',side_effect=lambda:clock[0]),patch.object(m.time,'sleep',side_effect=sleep),patch.object(m.p.native,'publish_request'),patch.object(m.p.native,'check_health',side_effect=health),patch.object(m.p.native,'request_stop',side_effect=stop) as stopped:
                result=m.monitor(dict(live_root=str(live)),s,run)
            if fail_health:
                stopped.assert_called_once();self.assertFalse(result);return
            stopped.assert_not_called()
            if aged_ack:self.assertTrue((run/'timing-warning-initial_ACK_aged_during_external_wait.json').exists())
            self.assertEqual(result,not missing_ack)
            names={p.name for p in run.glob('timing-warning-*.json')}
            self.assertIn('timing-warning-admission_over_2min.json',names)
            self.assertIn('timing-warning-external_READY_over_150s.json',names)
            self.assertIn('timing-warning-external_sample_gap_over_10s.json',names)
            self.assertIn('timing-warning-monitored_interval_over_20min.json',names)
            self.assertEqual((run/'monitor-ready.json').exists(),not missing_ack)
            if not missing_ack:self.assertTrue(json.loads((run/'monitor-ready.json').read_text())['timing_confirmation_required'])


if __name__=='__main__':unittest.main(verbosity=2)
