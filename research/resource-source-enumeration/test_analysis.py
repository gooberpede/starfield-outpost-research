# SPDX-License-Identifier: GPL-3.0-or-later
"""Synthetic uncertainty-envelope and exact-comparison controls; offline only."""
import copy
import unittest
from analyze import possible_sources, reframe, signature, witnessed_inventory
import context


class Controls(unittest.TestCase):
    def test_pattern_envelope_discovers_alternative_without_observed_input(self):
        m=dict(faces=[dict(values=[1]*65536, mask=[4]*65536) for _ in range(2)])
        registry=[dict(id=10,style=7),dict(id=20,style=7),dict(id=30,style=8)]
        selected=context.select_patterns(m,{1:7},registry,1,2)
        selected['map']=m
        patterns={10:dict(entries=[(40,8)]*256),20:dict(entries=[(50,8)]*256),
                  30:dict(entries=[(60,8)]*256)}
        blocks={i:dict(dimensions=[14,14]) for i in (40,50,60)}
        frozen=dict(tag=0,origin=[96,96],halo=dict(owner_cell_bounds=[[100,100],[102,102]]))
        before=copy.deepcopy(selected)
        sources,failures,choices=possible_sources(frozen,selected,patterns,blocks,{1:7},registry)
        self.assertEqual({s['block'] for s in sources},{40,50})
        self.assertEqual(len(sources),2)
        self.assertFalse(failures)
        self.assertEqual(choices,{'0,0':[10,20]})
        self.assertEqual(selected,before)
        witnessed,unresolved=witnessed_inventory(frozen,selected,patterns,blocks,
            [dict(tag=0,coarse=[0,0],pattern='0x00000014',pattern_flags=8)])
        self.assertEqual({s['block'] for s in witnessed},{50})
        self.assertFalse(unresolved)
        self.assertEqual(selected,before)

    def test_failed_anchor_is_explicit_and_selection_restored(self):
        m=dict(faces=[dict(values=[1]*65536) for _ in range(2)])
        selected=dict(tables=[[(10,8)]*65536 for _ in range(2)],map=m)
        frozen=dict(tag=0,origin=[96,96],halo=dict(owner_cell_bounds=[[96,96],[96,96]]))
        sources,failures,_=possible_sources(frozen,selected,{10:dict(entries=[(40,0)]*256)},
                                           {40:dict(dimensions=[14,14])},{1:7},[dict(id=10,style=7)])
        self.assertFalse(sources)
        self.assertEqual(len(failures),1)
        self.assertEqual(selected['tables'][0][0],(10,8))

    def test_reframe_rebuilds_keys_without_mutating_order(self):
        req=dict(ordered_resources=[dict(resource='a'),dict(resource='b')],packed_keys={'old':0})
        source=dict(id='candidate',origin=[-1400,-1400],clip_center=[-900,-900,0],
                    clip_half=[700,700,0],cell_bounds=[1,13,1,13])
        frozen=dict(tag=0,origin=[21408,15648],system=1,index=2)
        out=reframe(req,source,frozen)
        self.assertEqual(out['ordered_resources'],req['ordered_resources'])
        self.assertEqual(req['packed_keys'],{'old':0})
        self.assertEqual(len(out['packed_keys']),144)
        self.assertEqual(out['packed_keys']['1,1']&65535,20009)

    def test_exact_oracle_rejects_resource_independent_geometry_changes(self):
        region=dict(points=[[1.,2.,0.,3.],[4.,5.,0.,6.]],native_bound=[2.,3.,0.,7.])
        original=signature(region)
        for field in ('points','native_bound'):
            altered=copy.deepcopy(region)
            if field=='points':altered[field].reverse()
            else:altered[field][3]+=0.000001
            self.assertNotEqual(signature(altered),original)


if __name__=='__main__':
    unittest.main()
