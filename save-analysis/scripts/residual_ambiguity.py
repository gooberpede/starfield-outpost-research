"""SPDX-License-Identifier: GPL-3.0-or-later
EXP0020 original identifiability countermodel, NOT a planetary-position API.
Pure stdlib/project arithmetic; no I/O or target effects. Demonstrates that
integer center samples and translation invariance do not determine an off-grid
extension, even after choosing the same center phase. See residual-map.md.
"""
import math
from beacon_terrain_projection import from_square


def countermodel(tag, x, y, residual_x, residual_y, epsilon=0.0, n=49152):
    """Two illustrative extensions: linear and a smooth within-step warp.

    epsilon is a research counterexample parameter, never fitted to an outpost.
    Both agree at integer steps and have the same phase/orientation. This is
    deliberately restricted to the chart interior: no inferred seam extension.
    """
    if not all(math.isfinite(v) for v in (residual_x,residual_y,epsilon)):
        raise ValueError('NONFINITE')
    if abs(epsilon) >= 1/(2*math.pi):
        raise ValueError('NONMONOTONE_WARP')
    def axis(q, r):
        s = r/100
        return (q+.5+s+epsilon*math.sin(2*math.pi*s))/n-.5
    return from_square(tag, axis(x,residual_x), axis(y,residual_y))
