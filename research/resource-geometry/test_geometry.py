# SPDX-License-Identifier: GPL-3.0-or-later
"""Synthetic mathematical/source-transcription controls, not native execution."""
import copy
import math
import struct
import unittest
from fractions import Fraction as F
from geometry import (Draws, sincos, unopposed_cell, generate_cell, populate_source,
                      competition_rejects, conservative_bound, point_membership,
                      polygon_circle, nominal_strips)


def constants():
    # Bounded numerical facts from the pinned sin/cos study; see native.md.
    words = {
        0x144f0416c: 0x3e22f983, 0x144f049f4: 0x40c90fdb,
        0x144f04654: 0x3fc90fdb, 0x144f048dc: 0x40490fdb,
        0x144f052b0: 0xbfc90fdb, 0x144f052f8: 0xc0490fdb,
        0x144f03d80: 0x3638b88e, 0x144f03d40: 0x32cd365b,
        0x144f03e00: 0x39500bf1, 0x144f03ed4: 0x3c088886,
        0x144f04178: 0x3e2aaaab, 0x144f03dc4: 0x37cfb4c2,
        0x144f03d58: 0x348bdd11, 0x144f03e48: 0x3ab609aa,
        0x144f03fd4: 0x3d2aaaa3, 0x144f03f50: 0x3c8efa35,
    }
    return {a: struct.unpack('<f', struct.pack('<I', b))[0] for a, b in words.items()}


def request():
    return dict(packed_key=7, owner_key=259487, cell=[0, 0], origin=[0, 0],
                clip_center=[50, 50, 0], clip_half=[1000, 1000, 0],
                block=[3, 3, 4, 4, 20, 20, 0, 100, 0, 0], weight=1,
                source='SYNTHETIC/source', resource='SYNTHETIC/resource',
                provenance='synthetic control, no actual site', context_qualified=True,
                prior_different_resources=[])


class Generation(unittest.TestCase):
    def test_later_rejection_and_last_accepted_origin(self):
        req=request(); req['block'][0:2]=[4,4]; req['block'][6]=90
        baseline=generate_cell(req,constants())
        rejected=baseline['attempts'][1]['point']
        prior=dict(resource='SYNTHETIC/competitor',points=[rejected[:3]+[.01]])
        req['prior_different_resources']=[prior]
        result=generate_cell(req,constants())
        self.assertTrue(result['attempts'][1]['competing'])
        self.assertEqual(result['attempts'][2]['prior_accepted'],1)
        self.assertEqual(result['words'],baseline['words'])
        self.assertEqual(result['attempts'][2]['heading'],baseline['attempts'][2]['heading'])
        p=result['attempts'][2]['point']
        self.assertAlmostEqual(math.dist(p[:3],result['points'][0][:3]),20,delta=.00002)
        self.assertNotEqual(p,baseline['attempts'][2]['point'])
        req['prior_different_resources'][0]['resource']=req['resource']
        self.assertEqual(generate_cell(req,constants())['points'],baseline['points'])

    def test_generation_uses_nine_samples_and_constant_width_segment(self):
        # Candidate center misses; its upper-right corner is inside a prior disk.
        prior=[dict(resource='old',points=[[2,2,0,.25]])]
        self.assertTrue(competition_rejects([0,0,0,2],'new',prior))
        self.assertFalse(competition_rejects([0,0,0,2],'old',prior))
        # Max endpoint width 4, not a linearly tapered width near the narrow end.
        prior=[dict(resource='old',points=[[0,0,0,0],[100,0,0,4]])]
        self.assertTrue(competition_rejects([10,3,0,0],'new',prior))
        self.assertFalse(competition_rejects([10,5,0,0],'new',prior))

    def test_finite_source_order_keys_and_bound(self):
        req=request()
        source={k:req[k] for k in ('source','provenance','origin','owner_key','clip_center','clip_half','context_qualified')}
        source.update(cell_bounds=[-1,1,0,2],packed_keys={f'{x},{y}':7+x*100+y for x in (-1,0) for y in (0,1)},
                      order_qualified=True,ordered_resources=[dict(resource='A',block=req['block'],weight=1),dict(resource='B',block=req['block'],weight=1)])
        # Keys must be unsigned. Keep the synthetic mapping explicit.
        source['packed_keys']={k:v+1000 for k,v in source['packed_keys'].items()}
        first=populate_source(source,constants())
        self.assertEqual(first['status'],'CONDITIONAL_PLANAR_SOURCE')
        self.assertEqual(len(first['cells']),8)
        self.assertEqual([r['source'] for r in first['regions']],[source['source']]*len(first['regions']))
        a=[r['points'] for r in first['regions'] if r['resource']=='A']
        source['ordered_resources'].reverse()
        second=populate_source(source,constants())
        self.assertNotEqual(a,[r['points'] for r in second['regions'] if r['resource']=='A'])
        source['packed_keys'].pop('-1,0')
        self.assertEqual(populate_source(source,constants())['status'],'UNKNOWN')
        bound=conservative_bound([[0,0,0,1],[100,0,0,4]])
        self.assertGreaterEqual(bound['radius'],54)

    def test_mt_reference_sequence(self):
        rng = Draws(5489)
        for _ in range(5): rng.uniform()
        self.assertEqual(rng.words, [3499211612, 581869302, 3890346734, 3586334585, 545404204])

    def test_sincos_reference_and_reduction(self):
        c = constants()
        self.assertEqual(sincos(c[0x144f052b0], c), (-0.9999998807907104, -1.1920928955078125e-7))
        for angle in (-20, -6, -3, -1, 0, 1, 3, 6, 20):
            s, co = sincos(angle, c)
            self.assertAlmostEqual(s, math.sin(angle), delta=3e-6)
            self.assertAlmostEqual(co, math.cos(angle), delta=3e-6)

    def test_draw_schedule_and_lengths(self):
        result = unopposed_cell(request(), constants())
        self.assertEqual(result['status'], 'CONDITIONAL_UNOPPOSED_CELL')
        self.assertEqual(len(result['points']), 3)
        # gate, count, rounding, heading, then 3 draws initially and 4/extension.
        self.assertEqual(len(result['words']), 15)
        for a, b in zip(result['points'], result['points'][1:]):
            self.assertAlmostEqual(math.dist(a[:3], b[:3]), 20, delta=.00002)
            self.assertEqual(b[3], 4)

    def test_outside_start_enters_circle_without_radius_culling(self):
        # A supplied path starts outside the disk and crosses its interior.
        # Its start is not an admissible neighborhood-culling criterion.
        path=[[-250,0,0,2],[50,0,0,2]]
        self.assertGreater(math.dist(path[0][:2],[0,0]),150)
        self.assertEqual(nominal_strips(path,[0,0])['intersection'],'POSITIVE_AREA')

    def test_rejected_first_attempt_resamples_initial_xy(self):
        req = request(); req['clip_center'] = [1000000, 1000000, 0]
        result = unopposed_cell(req, constants())
        self.assertEqual(result['points'], [])
        self.assertEqual(len(result['words']), 13)  # 4 prefix + 3 draws per retry.
        self.assertTrue(all(a['clipped'] for a in result['attempts']))
        self.assertTrue(all(0 <= a['point'][0] <= 100 for a in result['attempts']))

    def test_gate_and_missing_inputs(self):
        req = request(); req['block'][7] = 0
        result = unopposed_cell(req, constants())
        self.assertEqual(result['branch'], 'chance_reject')
        self.assertEqual(len(result['words']), 1)
        for changes in ({'packed_key': None}, {'context_qualified': False},
                        {'prior_different_resources': ['unhandled competitor']}, {'weight': -1},
                        {'source': ''}, {'provenance': False}):
            req = request(); req.update(changes)
            self.assertEqual(unopposed_cell(req, constants())['status'], 'UNKNOWN')

    def test_no_resource_id_in_seed_and_no_input_mutation(self):
        req = request(); before = copy.deepcopy(req)
        a = unopposed_cell(req, constants()); self.assertEqual(req, before)
        req['resource'] = 'SYNTHETIC/other'
        b = unopposed_cell(req, constants())
        self.assertEqual(a['points'], b['points'])
        req['packed_key'] += 1
        self.assertNotEqual(a['points'], unopposed_cell(req, constants())['points'])


class Intersection(unittest.TestCase):
    def test_point_membership(self):
        p=[[-50,0,0,2],[50,0,0,2]]
        self.assertEqual(point_membership(p,[0,0]),'INTERIOR')
        self.assertEqual(point_membership(p,[0,10]),'OUTSIDE')
        self.assertEqual(point_membership([[0,0,0,2]],[2,0]),'BOUNDARY')
        self.assertEqual(point_membership([[0,0,0,2]],[0,0]),'INTERIOR')
    def test_contained_region_and_contained_circle(self):
        self.assertEqual(polygon_circle([[-1,-1],[1,-1],[1,1],[-1,1]], [0,0]), 'POSITIVE_AREA')
        self.assertEqual(polygon_circle([[-500,-500],[500,-500],[500,500],[-500,500]], [0,0]), 'POSITIVE_AREA')

    def test_sliver_tangent_negative_and_winding(self):
        for x, verdict in [(F(150)-F(1,2**40), 'POSITIVE_AREA'),
                           (150, 'TANGENT_ONLY'), (F(150)+F(1,2**40), 'DISJOINT')]:
            p = [[x,-1],[x+2,-1],[x+2,1],[x,1]]
            self.assertEqual(polygon_circle(p, [0,0]), verdict)
            self.assertEqual(polygon_circle(p[::-1], [0,0]), verdict)

    def test_crossing_without_vertex_inside(self):
        self.assertEqual(polygon_circle([[-200,10],[200,10],[200,11],[-200,11]], [0,0]), 'POSITIVE_AREA')

    def test_translation_and_scale(self):
        # Held-out 3-4-5 corner: disk touches one corner of a rectangle.
        p = [[3,4],[7,4],[7,8],[3,8]]
        self.assertEqual(polygon_circle(p,[0,0],5), 'TANGENT_ONLY')
        p = [[x*30+9876,y*30-4567] for x,y in p]
        self.assertEqual(polygon_circle(p,[9876,-4567],150), 'TANGENT_ONLY')

    def test_invalid_and_zero_area(self):
        self.assertEqual(polygon_circle([[0,0],[1,0],[2,0]], [0,0]), 'ZERO_AREA')
        with self.assertRaises(ValueError):
            polygon_circle([[0,0],[3,0],[1,1],[3,3],[0,3]], [0,0])
        with self.assertRaises(ValueError):
            polygon_circle([[0,0],[2,2],[0,2],[2,0]], [0,0])
        self.assertEqual(nominal_strips(None,[0,0])['status'], 'UNKNOWN')
        self.assertEqual(nominal_strips([[0,0,0,1]],[0,0])['status'], 'UNKNOWN')

    def test_strips_positive_negative_and_degenerate(self):
        p = [[-50,0,0,2],[50,0,0,2]]
        self.assertEqual(nominal_strips(p,[0,0])['intersection'], 'POSITIVE_AREA')
        self.assertEqual(nominal_strips(p,[0,300])['intersection'], 'DISJOINT_OR_ZERO_AREA')
        p = [[0,0,0,0],[0,0,0,0]]
        self.assertEqual(nominal_strips(p,[0,0])['intersection'], 'DISJOINT_OR_ZERO_AREA')


if __name__ == '__main__': unittest.main()
