# SPDX-License-Identifier: GPL-3.0-or-later
"""Offline adapter080 fixtures; all process/deployment contacts mocked."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import adapter070
import adapter080
import common
import session


class Adapter080(unittest.TestCase):
    def test_version_isolation(self):
        self.assertEqual(adapter070.ops.LIVE.name,'live')
        self.assertIn('continuous-beacon-preview',str(adapter070.ops.LIVE))
        self.assertIn('local-readiness',str(adapter080.ops.LIVE))
        self.assertIn('local-readiness-080',adapter080.ops.inspect.__code__.co_filename)
        self.assertNotEqual(adapter070.ops.manifest,adapter080.ops.manifest)

    def test_select_and_reject_unknown(self):
        session.select_adapter('080')
        self.assertIs(session.adapter,adapter080)
        with self.assertRaises(ValueError):session.select_adapter('999')
        session.select_adapter('070')

    def test_actual_080_prelaunch_receipt_selection(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);build=p/'build';build.mkdir();common.fresh(build/'build.json',{})
            saves=p/'saves';saves.mkdir();loader=p/'sfse_loader.exe';loader.write_bytes(b'fixture')
            plan=p/'plan.json';common.fresh(plan,dict(adapter='080',build=str(build),manifest_sha256=common.sha(build/'build.json'),deployed=False,saves=str(saves),extra_pins={str(loader):common.sha(loader)}))
            with patch.object(session,'guard',return_value={'C:/':10**12,'D:/':10**12}),patch.object(adapter080,'prelaunch_processes',return_value=[]),patch.object(adapter080,'full',return_value={}):
                r=session.prelaunch(plan,common.sha(plan))
            self.assertEqual(r['adapter'],'080');self.assertEqual(r['status'],'PASS_PRELAUNCH')
            receipt=p/'prelaunch.json';common.fresh(receipt,r)
            self.assertEqual(session.reuse(receipt,common.sha(receipt))['adapter'],'080')
            r['plan_data']['adapter']='070';common.fresh(p/'bad.json',r)
            with self.assertRaises(ValueError):session.reuse(p/'bad.json',common.sha(p/'bad.json'))
        session.select_adapter('070')

    def test_080_nonce_wait_failure_and_retirement(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);s=dict(version='0.8.0',schema=8,pid=1,process_creation_filetime=2,dll_sha256='d',game_sha256='g',sfse_sha256='f',module_base='b')
            def put(n,r):common.fresh(p/n,r)
            self.assertEqual(adapter080.status(p,{},s,None)['status'],'WAITING_READY')
            put('ready.json',dict(s,capture_active=True,group_flush_spool=True))
            with patch.object(adapter080.ops,'admission',return_value={}):
                self.assertEqual(adapter080.status(p,{},s,None)['status'],'WAITING_FRESH_ACK')
                self.assertEqual(adapter080.status(p,{},s,dict(nonce='a'*32))['status'],'WAITING_ACK')
                put('ack-'+('a'*32)+'.json',dict(s,nonce='a'*32,integrity_failure=False,failed=0))
                self.assertEqual(adapter080.status(p,{},s,dict(nonce='a'*32))['status'],'READY_ACK')
            put('retired.json',dict(s,integrity_failure=False,failed=0,active=0,captured=5,last_durable_sequence=5))
            self.assertEqual(adapter080.status(p,{},s,None)['status'],'RETIRED')
            put('failure.json',dict(error='writer'))
            self.assertEqual(adapter080.status(p,{},s,None)['status'],'WORKER_FAILURE')


if __name__=='__main__':unittest.main()
