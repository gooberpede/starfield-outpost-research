# SPDX-License-Identifier: GPL-3.0-or-later
"""Authored synthetic D1 schema, coverage and availability controls.

Stdlib only; creates no files and reads no proprietary fixtures. Run unittest
with the owned geometry directories on PYTHONPATH, or from the local code bundle.
"""
import copy
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'research/resource-geometry'),str(ROOT/'save-analysis/scripts')]
from predictor import predict, seal, validate, resolve, DEFINITION, SCHEMA
import geometry


def fixture():
    constants=(0x144f0416c,0x144f049f4,0x144f04654,0x144f048dc,0x144f052b0,
        0x144f052f8,0x144f03d80,0x144f03d40,0x144f03e00,0x144f03ed4,
        0x144f04178,0x144f03dc4,0x144f03d58,0x144f03e48,0x144f03fd4,0x144f03f50)
    c=dict(schema=SCHEMA,definition=DEFINITION,representation='normalized',constants={hex(k):1.0 for k in constants},
        settings=[1.0]*6,maximum_width=0,generation_blocks={'test':[0.0]*8},
        patterns={'synthetic':[['00000001',8] for _ in range(256)]},source_blocks={'00000001':[16,16]},
        bodies={'00000001':dict(system=1,index=1,tiles={f'0:{x}:{y}':['synthetic',8,'biome',4]
            for x in (99,100) for y in (99,100)},biomes={'biome':dict(status='ORDINARY_ONLY',
                resources=[dict(id='authored',rarity=0,block='test')])})})
    q=dict(schema='sor-d1-request/1',definition=DEFINITION,body='00000001',chart=0,
        descriptor=[19200,19200],query=[0.0,0.0,0.0],radius=1.0,upper=1.0)
    return c,q


class PredictorTests(unittest.TestCase):
    def test_malformed_types_are_structured(self):
        for key in ('constants','bodies','generation_blocks'):
            c,q=fixture();c[key]=[]
            self.assertEqual(predict(seal(c),q)['status'],'UNKNOWN')

    def test_expanded_missing_and_malformed_routes(self):
        for entries in (None,[],[[1,2,'bad',0,0]]*256):
            c,q=fixture();c['representation']='expanded'
            if entries is not None:
                c['bodies']['00000001']['routes']={k:entries for k in c['bodies']['00000001']['tiles']}
            self.assertEqual(predict(seal(c),q)['status'],'UNKNOWN')

    def test_zero_chance_is_scoped_absence(self):
        c,q=fixture();r=predict(seal(c),q)
        self.assertEqual(r['status'],'CONDITIONAL_GEOMETRY')
        self.assertEqual(r['availability']['authored']['status'],'ABSENT_WITHIN_PROVEN_SCOPE')
        self.assertEqual(r['regions'],[])

    def test_no_expected_anchor_request(self):
        c,q=fixture();q['source']='witness'
        self.assertEqual(predict(seal(c),q)['reason'],'REQUEST_FIELDS')

    def test_schema_and_definition(self):
        for key,value in (('schema','future'),('definition','wrong')):
            c,q=fixture();q[key]=value
            self.assertEqual(predict(seal(c),q)['status'],'UNKNOWN')
            c,q=fixture();c[key]=value
            self.assertEqual(predict(seal(c),q)['status'],'UNKNOWN')

    def test_checksum_corruption(self):
        c,q=fixture();e=seal(c);e['payload']['settings'][0]=2
        self.assertEqual(predict(e,q)['reason'],'CORRUPT_CORPUS')

    def test_missing_groups(self):
        for key in ('bodies','constants','settings','generation_blocks','patterns','source_blocks'):
            c,q=fixture();del c[key]
            self.assertEqual(predict(seal(c),q)['status'],'UNKNOWN',key)

    def test_chart_seam_and_nonfinite(self):
        for key,value in (('chart',2),('descriptor',[0,0]),('query',[float('nan'),0,0]),('radius',-1)):
            c,q=fixture();q[key]=value
            self.assertEqual(predict(seal(c),q)['status'],'UNKNOWN')

    def test_missing_coverage_never_zero(self):
        c,q=fixture();c['bodies']['00000001']['tiles']={}
        r=predict(seal(c),q)
        self.assertEqual(r['status'],'UNKNOWN');self.assertEqual(r['availability'],{})

    def test_partial_resolution_is_unknown(self):
        c,q=fixture();c['patterns']['synthetic']=[['00000000',0] for _ in range(256)]
        r=predict(seal(c),q)
        self.assertEqual(r['status'],'PARTIAL');self.assertFalse(r['exhaustive'])
        self.assertTrue(r['failures'])

    def test_single_backlink_accepts_typed_nonanchor(self):
        c,q=fixture();entries=c['patterns']['synthetic']
        entries[17]=['00000000',0x10];entries[1]=['00000001',0]
        r=resolve(c,c['bodies']['00000001'],0,19200+12,19200+12)
        self.assertEqual(r[:2],(19200,19212))

    def test_source_mask_uncertainty(self):
        c,q=fixture();c['bodies']['00000001']['tiles']['0:99:99'][3]=8
        r=predict(seal(c),q)
        self.assertEqual(r['status'],'PARTIAL')
        self.assertFalse(r['exhaustive'])

    def test_unsupported_resource_branch(self):
        c,q=fixture();c['bodies']['00000001']['biomes']['biome']['status']='SPECIAL_UNRESOLVED'
        self.assertEqual(predict(seal(c),q)['status'],'PARTIAL')

    def test_positive_negative_and_boundary_geometry(self):
        points=[[0.0,0.0,0.0,10.0]]
        self.assertEqual(geometry.region_membership(points,[0,0]),'INTERIOR')
        self.assertEqual(geometry.region_membership(points,[10,0]),'BOUNDARY')
        self.assertEqual(geometry.region_membership(points,[20,0]),'OUTSIDE')
        self.assertEqual(geometry.bounded_region_circle(points,[0,0],1)['intersection'],'POSITIVE_AREA')
        self.assertEqual(geometry.bounded_region_circle(points,[20,0],1)['intersection'],'DISJOINT_OR_ZERO_AREA')

    def test_unused_descriptor_tail_redundancy(self):
        c,q=fixture();constants={int(k,16):v for k,v in c['constants'].items()}
        req=dict(packed_key=123,owner_key=1,cell=[5,5],origin=[100,100],clip_center=[500,500,0],
            clip_half=[1000,1000,1000],block=[1,1,2,2,0,0,0,100,0,0],weight=1,
            source='authored',resource='test',provenance='Synthetic tail ablation',context_qualified=True,
            prior_different_resources=[])
        a=geometry.generate_cell(req,constants)
        self.assertTrue(a['points'])
        req['block'][-2:]=[123,456]
        self.assertEqual(a,geometry.generate_cell(req,constants))

    def test_unresolved_area_boundary_propagates_unknown(self):
        points=[[0.0,0.0,0.0,10.0],[100.0,0.0,0.0,10.0]]
        self.assertEqual(geometry.bounded_region_circle(points,[111,0],1)['status'],'UNKNOWN')
        c,q=fixture();q['query']=[111,0,0]
        generated=dict(status='CONDITIONAL_PLANAR_SOURCE',regions=[dict(source='authored',resource='authored',
            cell=[0,0],points=points,native_bound=geometry.native_bound(points))])
        # This authored injected region tests aggregation, not native generation.
        with patch('predictor.geometry.populate_source',return_value=generated):
            r=predict(seal(c),q)
        self.assertEqual(r['availability']['authored']['status'],'UNKNOWN')


if __name__=='__main__':
    unittest.main()
