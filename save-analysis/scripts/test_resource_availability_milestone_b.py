# SPDX-License-Identifier: GPL-3.0-or-later
"""Original synthetic integration tests; no captured spatial oracle implied."""
import copy
import unittest
from resource_availability import EXE_SHA256, evaluate_json

def operand(p, f): return dict(pointer=p,form_id=f)
def example():
    return dict(schema='sor-resource-availability-input/2',exe_sha256=EXE_SHA256,
                session='SYNTHETIC',evidence='authored control; no native oracle',
                query=dict(xyz=[0,0,0],radius=1,height=0,frame_qualified=True),
                candidate_enumeration_complete=True,
                regions=[dict(identity='synthetic region 1',evidence='authored',resolved_form_type=159,
                              resource=operand(100,1),center=[0,0,0],radius=1,points=[[0,0,0,1]],point_count=1)],
                atmosphere=[operand(200,2)],biome=[operand(300,3)],selector_observed=True,
                selected_form_id=None,allocations_complete=True)

class AvailabilityTests(unittest.TestCase):
    def test_spatial_to_union(self):
        x=evaluate_json(example()); self.assertEqual(x['ui_form_set'],[1,2]); self.assertEqual(x['status'],'CONDITIONAL_NATIVE_AVAILABILITY')
    def test_spatial_rejection(self):
        r=example();r['regions'][0]['center']=[10,0,0]
        self.assertEqual(evaluate_json(r)['ui_form_set'],[2])
    def test_incomplete_enumeration(self):
        r=example();r['candidate_enumeration_complete']=None
        x=evaluate_json(r);self.assertEqual(x['status'],'UNKNOWN');self.assertIsNone(x['ui_form_set']);self.assertEqual(x['known_spatial_resource_lower_bound'],[1])
    def test_missing_geometry(self):
        r=example();r['regions'][0]['points']=None;r['regions'][0]['point_count']=2
        self.assertEqual(evaluate_json(r)['status'],'UNKNOWN')
    def test_no_candidates_observed_empty(self):
        r=example();r['regions']=[]
        self.assertEqual(evaluate_json(r)['ui_form_set'],[2])
    def test_missing_frame_even_empty(self):
        r=example();r['regions']=[];r['query']['frame_qualified']=False
        self.assertEqual(evaluate_json(r)['status'],'UNKNOWN')
    def test_atmosphere_unknown_not_empty(self):
        r=example();r['atmosphere']=None
        self.assertIsNone(evaluate_json(r)['ui_form_set'])
    def test_water_selected_only(self):
        r=example();r['selected_form_id']=3
        self.assertEqual(evaluate_json(r)['ui_form_set'],[1,2,3])
    def test_wrong_native_type(self):
        r=example();r['regions'][0]['resolved_form_type']=109
        self.assertEqual(evaluate_json(r)['ui_form_set'],[2])
    def test_build_rejected(self):
        r=example();r['exe_sha256']='other'
        with self.assertRaises(ValueError):evaluate_json(r)
    def test_conflicting_pointer(self):
        r=example();s=copy.deepcopy(r['regions'][0]);s['resource']['form_id']=4;r['regions'].append(s)
        with self.assertRaises(ValueError):evaluate_json(r)
    def test_unqualified_query_numeric_is_unknown(self):
        for value in (float('nan'),1e-40,1e40,-1):
            r=example();r['query']['radius']=value
            self.assertEqual(evaluate_json(r)['status'],'UNKNOWN')

if __name__=='__main__': unittest.main()
