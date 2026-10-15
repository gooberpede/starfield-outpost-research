# SPDX-License-Identifier: GPL-3.0-or-later
"""Synthetic static-transcription controls; none is a captured native oracle."""
import unittest

from resource_spatial import evaluate_region, quad_membership, segment_distance_squared, strip_quad


class SpatialTests(unittest.TestCase):
    def run_region(self, points, q=(0, 0, 0), radius=1, h=0, center=(0, 0, 0), rr=10):
        return evaluate_region(q, radius, h, center, rr, points)

    def test_count_branches(self):
        self.assertFalse(self.run_region([])["accepted"])
        self.assertTrue(self.run_region([[999, 999, 999, 0]])["accepted"])
        self.assertFalse(self.run_region([[0, 0, 0, 1]], q=(12, 0, 0))["accepted"])
        self.assertTrue(self.run_region([[0, 0, 0, 1]], q=(11, 0, 0))["accepted"])
        self.assertTrue(evaluate_region([0, 0, 0], 1, None, [0, 0, 0], 1, None, point_count=1)["accepted"])
        self.assertFalse(evaluate_region([0, 0, 0], 1, None, [0, 0, 0], 1, None, point_count=0)["accepted"])
        self.assertEqual(evaluate_region([0, 0, 0], 1, None, [0, 0, 0], 1, None, point_count=2)["status"], "UNKNOWN")

    def test_containment_ignores_height_and_query_z(self):
        ps = [[-5, 0, 20, 2], [5, 0, 20, 2]]
        out = self.run_region(ps, q=(0, 0, -900), radius=0, h=-100)
        self.assertTrue(out["accepted"])
        self.assertEqual(out["branch"], "quad_xy_containment")

    def test_vertices_have_absolute_height_gate(self):
        quad = [[-2, 2, 7], [2, 2, 7], [2, -2, 7], [-2, -2, 7]]
        self.assertEqual(quad_membership(quad, (2, 3, -100), 1, 7), (True, "vertex_xy_radius_height"))
        self.assertEqual(quad_membership(quad, (2, 3, -100), 1, 6), (False, "strip_rejected"))

    def test_edge_uses_3d_distance(self):
        quad = [[-2, 2, 7], [2, 2, 7], [2, -2, 7], [-2, -2, 7]]
        self.assertEqual(quad_membership(quad, (0, 3, 7), 1, -10), (True, "edge_3d_radius"))
        self.assertFalse(quad_membership(quad, (0, 3, 9), 1, -10)[0])

    def test_segment_endpoints_and_interior(self):
        self.assertEqual(segment_distance_squared((0, 0, 0), (2, 0, 0), (-1, 1, 0)), 2)
        self.assertEqual(segment_distance_squared((0, 0, 0), (2, 0, 0), (3, 1, 0)), 2)
        self.assertEqual(segment_distance_squared((0, 0, 0), (2, 0, 0), (1, 1, 0)), 1)

    def test_polynomial_residual_preserved(self):
        quad = strip_quad((-1, 0, 0, 1), (1, 0, 0, 1))
        self.assertNotEqual(quad[0][0], -1)
        self.assertNotEqual(quad[0][1], 1)

    def test_no_implicit_path_closure(self):
        ps = [[-10, -10, 0, 1], [10, -10, 0, 1], [10, 10, 0, 1]]
        self.assertFalse(self.run_region(ps, q=(-5, -5, 0), radius=0, rr=30)["accepted"])

    def test_unknown_never_false(self):
        for out in (evaluate_region(None, 1, 1, [0, 0, 0], 1, []),
                    self.run_region(None), self.run_region([[0, 0, 0, 1]], radius=float("nan")),
                    self.run_region([[0, 0, 0, 1]], q=(1e-40, 0, 0)),
                    self.run_region([[0, 0, 0, 1]], q=(1e-20, 0, 0)),
                    self.run_region([[0, 0, 0, 1]], radius=1e30)):
            self.assertEqual(out["status"], "UNKNOWN")
            self.assertIsNone(out["accepted"])

    def test_repeated_points_follow_degenerate_native_containment(self):
        out = self.run_region([[0, 0, 0, 1], [0, 0, 0, 1]], q=(4, 0, 0))
        self.assertTrue(out["accepted"])

    def test_binary32_boundary_differs_from_binary64(self):
        # 1+2^-24 lies exactly halfway between binary32 1 and its successor.
        # Ties-to-even rounds the actual query to tangent, while binary64
        # would reject this strictly outside point. Expected rule is native f32.
        self.assertGreater((1+2**-24)**2, 1)
        out=self.run_region([[0,0,0,0]],q=(1+2**-24,0,0),radius=1,rr=0)
        self.assertTrue(out['accepted'])

    def test_translated_common_frame(self):
        points=[[-5,0,2,1],[5,0,2,1]]
        q=[0,0,2]
        original=self.run_region(points,q=q,h=2)
        shift=[1024,-2048,32]
        moved=[[p[i]+shift[i] for i in range(3)]+[p[3]] for p in points]
        transformed=self.run_region(moved,q=[q[i]+shift[i] for i in range(3)],
                                    h=34,center=shift)
        self.assertEqual((original['accepted'],original['branch']),
                         (transformed['accepted'],transformed['branch']))

    def test_reflected_geometry_is_rebuilt_in_selected_frame(self):
        # Rebuild the ordered strip from reflected source points. Blindly
        # reflecting an already ordered quad reverses its winding instead.
        points=[[-5,0,2,1],[5,0,2,1]]
        reflected=[[-p[0],p[1],p[2],p[3]] for p in points]
        self.assertTrue(self.run_region(reflected,q=(0,0,2))['accepted'])
        quad=strip_quad(points[0],points[1])
        mirrored=[[-p[0],p[1],p[2]] for p in quad]
        self.assertEqual(quad_membership(mirrored,(0,0,2),0,-10),(False,'strip_rejected'))


if __name__ == "__main__":
    unittest.main()
