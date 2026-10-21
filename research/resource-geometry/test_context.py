# SPDX-License-Identifier: GPL-3.0-or-later
"""Original synthetic context controls; no proprietary fixtures or I/O."""
import unittest
from context import (select_patterns,source_at,packed_seed_key,rotate_cell,
                     neighborhood,map_lookup,mask_lookup)
from geometry import (region_membership,region_circle,point_membership,
                      native_bound,competition_rejects,bounded_region_circle,
                      segment_rectangle_circle)


class ContextControls(unittest.TestCase):
    def fixture(self):
        m=dict(faces=[dict(values=[1]*65536,mask=[8]*65536) for _ in range(2)])
        selected=select_patterns(m,{1:7},[dict(style=7,id=2)],1,2)
        selected['map']=m
        patterns={2:dict(entries=[(3,8)]*256)};blocks={3:dict(dimensions=[14,14])}
        return m,selected,patterns,blocks

    def test_defaults_and_raster_axes(self):
        m,s,p,b=self.fixture()
        self.assertEqual(s['draw_count'],0)
        self.assertEqual(s['tables'][0][0],(2,8))
        m['faces'][0]['values'][255*256+1]=4
        self.assertEqual(map_lookup(m,0,192,0),4)
        self.assertEqual(mask_lookup(m,0,192,0),8)

    def test_source_padding_frame_and_key_domains(self):
        m,s,p,b=self.fixture()
        source=source_at(0,14314,12779,[14304,12768],s,p,b,padding=2)
        self.assertEqual(source['geographic_origin'],[14304,12768])
        self.assertEqual(source['origin'],[-200,-200])
        self.assertEqual(source['dimensions'],[10,10])
        self.assertEqual(source['clip_center'],[300,300,0])
        self.assertEqual(source['cell_bounds'],[1,13,1,13])
        key=packed_seed_key(0,[14304,12768],[-200,-200],[1,1],88327,15)
        self.assertEqual(key&65535,14105)
        self.assertEqual((key>>16)&65535,12569)
        with self.assertRaises(ValueError):packed_seed_key(0,[0,0],[-200,0],[1,1],1,2)

    def test_neighbor_halo_includes_outside_owners(self):
        m,s,p,b=self.fixture()
        h=neighborhood(0,[14304,12768],[1088,1179],150,s,p,b,maximum_width=33)
        self.assertEqual(h['halo_native'],616)
        self.assertEqual(len(h['sources']),4)
        self.assertTrue(any(x['origin']==[1000,1000] for x in h['sources']))

    def test_nonanchor_and_orientations(self):
        m,s,p,b=self.fixture()
        p[2]['entries'][8*16+8]=(3,8)
        p[2]['entries'][9*16+8]=(3,16)
        source=source_at(0,9*12,8*12,[0,0],s,p,b,padding=2)
        self.assertEqual(source['geographic_origin'],[96,96])
        for orientation in range(8):
            points={rotate_cell(x,y,orientation) for x in range(16) for y in range(16)}
            self.assertEqual(points,{(x,y) for x in range(16) for y in range(16)})

    def test_distinct_point_and_area_products(self):
        path=[[0,0,0,1],[100,0,0,10]]
        self.assertEqual(region_membership(path,[1,8]),'INTERIOR')
        self.assertEqual(point_membership(path,[1,8]),'OUTSIDE')
        self.assertEqual(region_membership(path,[-1,0]),'BOUNDARY')
        self.assertEqual(region_circle([[0,0,0,2]],[151,0])['intersection'],'POSITIVE_AREA')
        self.assertEqual(region_circle([[0,0,0,1]],[151,0])['intersection'],'TANGENT_ONLY')
        self.assertEqual(region_circle(path,[10000,0])['intersection'],'DISJOINT_OR_ZERO_AREA')

    def test_native_broadphase_is_semantic(self):
        # Reviewer counterexample: a width increase leaves rectangle at thin
        # first end outside the incremental sphere. Omitting the bound rejects
        # this candidate incorrectly; a sound larger sphere is not equivalent.
        points=[[0,0,0,1],[1000,0,0,100]]
        self.assertEqual(native_bound(points),[549.5,0,0,550.5])
        self.assertEqual(region_membership(points,[0,99]),'OUTSIDE')
        self.assertFalse(competition_rejects([0,99,0,0],'b',[dict(resource='a',points=points)]))
        self.assertTrue(competition_rejects([500,99,0,0],'b',[dict(resource='a',points=points)]))
        self.assertEqual(bounded_region_circle(points,[500,0],1)['intersection'],'POSITIVE_AREA')
        self.assertEqual(bounded_region_circle(points,[10000,0],1)['intersection'],'DISJOINT_OR_ZERO_AREA')

    def test_exact_rectangle_circle_corner_distance(self):
        a,b=[0,0,0,1],[100,0,0,1]
        self.assertEqual(segment_rectangle_circle(a,b,[-3,5],5),'TANGENT_ONLY')
        self.assertEqual(segment_rectangle_circle(a,b,[-3,5],5.000001),'POSITIVE_AREA')
        self.assertEqual(segment_rectangle_circle(a,b,[-3,5],4.999999),'DISJOINT')
        self.assertEqual(segment_rectangle_circle(a,b,[50,151],150),'TANGENT_ONLY')
        self.assertEqual(segment_rectangle_circle(a,b,[50,0],.001),'POSITIVE_AREA')


if __name__=='__main__':unittest.main()
