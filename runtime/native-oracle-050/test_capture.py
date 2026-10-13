# SPDX-License-Identifier: GPL-3.0-or-later
"""Original offline adverse evidence tests. Reads fixtures, writes temp copies.
No target interaction. All generated sessions are explicitly synthetic.
"""
import copy
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
import inspect_capture as c
import route_inspect as r
BUILD=Path(sys.argv.pop(1))
def read_events(name):
    b=(BUILD/name).read_bytes()
    return [r.decode(b[i:i+r.SIZE]) for i in range(0,len(b),r.SIZE)]
class Tests(unittest.TestCase):
    def session(self,name='no-hit'):
        dest=Path(tempfile.mkdtemp(prefix='050-adverse-',dir=BUILD));shutil.copytree(BUILD/('lifecycle-'+name),dest,dirs_exist_ok=True);return dest
    def test_pre_ready_stop(self):
        from operate import stop_owned_session
        p=Path(tempfile.mkdtemp(prefix='050-stop-',dir=BUILD));(p/'waiting-sole-thread.json').write_text(json.dumps(dict(component='SorNativePositionOracle',version='0.5.0')))
        stop_owned_session(p);self.assertEqual((p/'STOP').read_bytes(),b'STOP\n');self.assertFalse((p/'ready.json').exists())
    def test_unowned_stop_rejected(self):
        from operate import stop_owned_session
        p=Path(tempfile.mkdtemp(prefix='050-stop-',dir=BUILD))
        with self.assertRaisesRegex(ValueError,'owned_session_identity_missing'):stop_owned_session(p)
        self.assertFalse((p/'STOP').exists())
    def test_production_no_hit(self):
        result=c.inspect(BUILD/'lifecycle-no-hit');self.assertTrue(result['instrumentation_complete']);self.assertEqual(result['deepest_observed'],'NO_NATIVE_HITS')
    def test_production_early_return(self):
        result=c.inspect(BUILD/'lifecycle-normal');self.assertTrue(result['instrumentation_complete']);self.assertEqual(len(result['workshop']),1);self.assertFalse(result['workshop'][0]['grid'])
    def test_failure_no_retirement(self):
        result=c.inspect(BUILD/'lifecycle-guard-failure');self.assertFalse(result['instrumentation_complete'])
    def test_wrong_ready(self):
        p=self.session();j=json.loads((p/'ready.json').read_bytes());j['schema']=4;(p/'ready.json').write_text(json.dumps(j))
        with self.assertRaisesRegex(ValueError,'ready_identity'):c.inspect(p)
    def test_raw_corruption(self):
        p=self.session('normal');b=bytearray((p/'events.bin').read_bytes());b[3]^=1;(p/'events.bin').write_bytes(b)
        with self.assertRaisesRegex(ValueError,'record_integrity'):c.inspect(p)
    def test_unjournaled_raw(self):
        p=self.session();(p/'events.bin').write_bytes(b'orphan');self.assertFalse(c.inspect(p)['instrumentation_complete'])
    def test_health_tail(self):
        p=self.session();(p/'health.jsonl').write_bytes((p/'health.jsonl').read_bytes()+b'{');self.assertFalse(c.inspect(p)['instrumentation_complete'])
    def test_health_counter_lie(self):
        p=self.session();lines=[json.loads(x) for x in (p/'health.jsonl').read_bytes().splitlines()];lines[-1]['entered'][2]=1;(p/'health.jsonl').write_text(''.join(json.dumps(x)+'\n' for x in lines));self.assertFalse(c.inspect(p)['instrumentation_complete'])
    def test_historical_delay_diagnostic_only(self):
        from operate import valid_health_transition
        a=dict(qpc=1,flushed_events=0,entered=[0,0,0]);b=dict(qpc=1_000_000,flushed_events=0,flushed_offset=0,entered=[0,0,0],queue_depth=0,lost=0,depth_errors=0,health_timeouts=0)
        self.assertTrue(valid_health_transition(a,b,1))
    def test_travel_primary(self):
        events=read_events('travel-events.bin');result=c.analyze(events,synthetic=True)
        self.assertTrue(result['travel']);self.assertTrue(any(x['decision']==1 for x in result['travel']));self.assertTrue(any(not x['normal_complete'] for x in result['travel']))
        self.assertTrue(all(x['asynchronous_identity'].startswith('UNASSOCIATED') for x in result['travel']))
    def test_missing_parent(self):
        es=read_events('travel-events.bin');root=es[0]['invocation'];pair=[e for e in es if e['invocation']==root];pair[0]['parent']=123456;pair[1]['parent']=123456
        self.assertFalse(c.analyze(pair)['structurally_complete'])
    def test_workshop_race_pre(self):
        es=read_events('fixtures/fixture-events.bin');es[2]['status']=8;row=c.analyze(es)['workshop'][0]['grid'][0];self.assertFalse(row['paired']);self.assertEqual(row['classification'],'PARTIAL_INVOCATION')
    def test_workshop_unwind(self):
        es=read_events('fixtures/fixture-events.bin');es[3]['kind']=56;es[4]['kind']=5;self.assertFalse(c.analyze(es)['structurally_complete'])
    def test_workshop_synthetic_never_native(self):
        es=read_events('fixtures/fixture-events.bin');self.assertEqual(c.analyze(es,synthetic=True)['workshop'][0]['grid'][0]['classification'],'SYNTHETIC_QUALIFICATION_ONLY')
    def test_generic_race(self):
        es=read_events('route-events.bin');root=es[0]['invocation'];es=[e for e in es if e['invocation']==root or e['parent']==root]
        next(e for e in es if e['kind']==33)['status']=8
        row=r.reconcile(es)['routes'][0];self.assertFalse(row['scientific_complete']);self.assertFalse(row['grid'][0]['reference_bound'])
    def test_orphan_child(self):
        es=read_events('route-events.bin');first=next(e for e in es if e['kind']==33);es=[e for e in es if e['invocation']==first['invocation']]
        for e in es:e['parent']=0
        self.assertFalse(c.analyze(es)['structurally_complete'])
    def test_wrong_parent_kind(self):
        es=read_events('route-events.bin');root=es[0]['invocation'];es=[e for e in es if e['invocation']==root or e['parent']==root]
        es[0]['kind']=7;es[-1]['kind']=8
        self.assertFalse(c.analyze(es)['structurally_complete'])
    def test_wrong_known_kind_in_q(self):
        es=read_events('fixtures/fixture-events.bin')[:4]
        for e in es:e['kind']={1:7,2:33,6:34,3:8}[e['kind']]
        self.assertFalse(c.analyze(es)['structurally_complete'])
    def test_unknown_kind(self):
        es=read_events('fixtures/fixture-events.bin');es[1]['kind']=99;self.assertFalse(c.analyze(es)['structurally_complete']);self.assertTrue(c.analyze(es)['defects'])
    def test_thread_change(self):
        es=read_events('fixtures/fixture-events.bin');es[1]['thread']+=1;self.assertFalse(c.analyze(es)['structurally_complete'])
if __name__=='__main__':unittest.main()
