# SPDX-License-Identifier: GPL-3.0-or-later
"""Original offline schema/join controls; owned fixture inputs only."""
import copy
import json
from pathlib import Path
import struct
import sys
import unittest
from inspect_resources import inspect, population_signature, records

ROOT=Path(sys.argv.pop(1)) if len(sys.argv)>1 else None


class Readiness(unittest.TestCase):
    def test_original_source_provider_fixture(self):
        r=inspect(ROOT)
        self.assertEqual(r['status'],'RETIRED_INTEGRITY_OK',r['errors'])
        self.assertEqual([o['kind'] for o in r['operations']],[111,112])
        child,provider=r['operations']
        self.assertEqual(child['parent'],r['evaluations'][1]['invocation'])
        self.assertFalse(any(o['parent']==r['evaluations'][0]['invocation'] for o in r['operations']))
        self.assertEqual([e['refresh_result'] for e in r['evaluations']],[0,1])
        self.assertEqual(child['before']['operand']['length'],8)
        self.assertEqual(child['before']['base']['length'],0x40)
        self.assertEqual(provider['after']['result'],0xabcdef)
        self.assertEqual(provider['cache_hit_miss'],'NOT_OBSERVED')

    def test_concurrent_writer_order(self):
        data=list(records(ROOT/'parallel'))
        self.assertEqual(len(data),1000)
        self.assertEqual([e['sequence'] for e in data],list(range(1,1001)))

    def test_snapshot_limit_is_failure(self):
        r=inspect(ROOT.parent/'bounded-fixtures')
        self.assertNotEqual(r['status'],'RETIRED_INTEGRITY_OK')
        data=list(records(ROOT.parent/'bounded-fixtures'))
        self.assertTrue(any(e['kind']==108 and e['status']==0x2000 for e in data))
        self.assertFalse(any(e['kind']==109 for e in data))

    def test_source_order_pointer_duplicates_and_unknown(self):
        m=dict(pointer=11,form_id=22,form_type=0x9f,status='READ_OK')
        def pop(ms):return dict(begin=8,end=8+8*len(ms),status=0,members=ms)
        p=[pop([m]),pop([]),pop([])]
        s=population_signature(p)
        self.assertNotEqual(s,population_signature([pop([]),pop([m]),pop([])]))
        self.assertNotEqual(s,population_signature([pop([m,m]),pop([]),pop([])]))
        q=copy.deepcopy(p);q[0]['members'][0]['pointer']=12
        self.assertNotEqual(s,population_signature(q))
        q[0]['members'][0]['status']='UNKNOWN_ID'
        self.assertIsNone(population_signature(q))
        q=copy.deepcopy(p);q[0]['status']=8
        self.assertIsNone(population_signature(q))

    def test_refresh_retained_relation(self):
        r=inspect(ROOT.parent/'fixtures')
        self.assertEqual(r['evaluations'][5]['refresh_result'],0)
        self.assertEqual(r['evaluations'][5]['within_invocation_population_change'],'UNCHANGED')
        self.assertEqual(r['evaluations'][3]['within_invocation_population_change'],'CHANGED')


if __name__=='__main__':unittest.main()
