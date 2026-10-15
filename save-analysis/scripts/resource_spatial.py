# SPDX-License-Identifier: GPL-3.0-or-later
"""Original reconstruction of retail 1.16.244.0 FUN_1421e0f50.

Reads no files and has no side effects. Native static evidence and limitations:
docs/experiments/resource-availability-milestone-b/native-provenance.md.
All coordinates must already share the qualified translated native frame.
Synthetic tests verify this transcription, not independent native equivalence.
"""
from __future__ import annotations

import math
import struct

SCHEMA = "sor-resource-spatial-result/1"


def f32(value):
    if not math.isfinite(value):
        raise ValueError("nonfinite arithmetic requires qualified native FP state")
    if value and abs(value) < 2 ** -126:
        raise ValueError("subnormal arithmetic requires qualified native MXCSR")
    result = struct.unpack("<f", struct.pack("<f", value))[0]
    if not math.isfinite(result):
        raise ValueError("binary32 arithmetic overflow")
    return result


def _add(a, b): return f32(a + b)
def _sub(a, b): return f32(a - b)
def _mul(a, b): return f32(a * b)
def _div(a, b): return f32(a / b)


def _vector(value, length):
    if not isinstance(value, (list, tuple)) or len(value) != length:
        raise ValueError("wrong vector length")
    out = []
    for x in value:
        if isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x):
            raise ValueError("finite numeric operand required")
        y = f32(x)
        if not math.isfinite(y) or (y and abs(y) < 2 ** -126):
            raise ValueError("nonfinite/subnormal native rounding state is unqualified")
        out.append(y)
    return out


def _sum_squares(v):
    # Native scalar/DPPS grouping: (x*x+y*y)+z*z.
    return _add(_add(_mul(v[0], v[0]), _mul(v[1], v[1])), _mul(v[2], v[2]))


def segment_distance_squared(a, b, q):
    """141116580's scalar 3D segment distance, including endpoint branches."""
    d = [_sub(b[i], a[i]) for i in range(3)]
    w = [_sub(q[i], a[i]) for i in range(3)]
    dot = _add(_add(_mul(w[0], d[0]), _mul(w[1], d[1])), _mul(w[2], d[2]))
    length2 = _sum_squares(d)
    if not dot > 0:
        return _sum_squares([_sub(a[i], q[i]) for i in range(3)])
    if dot >= length2:
        # Native reconstructs the endpoint as A+(B-A), not raw B.
        return _sum_squares([_sub(_add(a[i], d[i]), q[i]) for i in range(3)])
    return max(_sub(_sum_squares(w), _div(_mul(dot, dot), length2)), 0.0)


def strip_quad(a, b):
    """Consecutive xyz/width points -> native rotated, tapered four-vertex strip."""
    d = [_sub(b[i], a[i]) for i in range(3)]
    length = f32(math.sqrt(_sum_squares(d)))
    d = [_div(x, length) for x in d] if length != 0 and math.isfinite(length) else [0.0] * 3
    # 1404a7f90 polynomial at constant bfc90fdb, independently read from PE.
    sine, cosine = f32(-0.9999998807907104), f32(-1.1920928955078125e-7)
    # Preserve the three matrix-column operations, including the zero terms.
    v = [_add(_add(_mul(d[0], cosine), _mul(d[1], -sine)), _mul(d[2], 0.0)),
         _add(_add(_mul(d[0], sine), _mul(d[1], cosine)), _mul(d[2], 0.0)),
         _add(_add(_mul(d[0], 0.0), _mul(d[1], 0.0)), _mul(d[2], 1.0))]
    av, bv = [[_mul(w, x) for x in v] for w in (a[3], b[3])]
    return [[_sub(a[i], av[i]) for i in range(3)],
            [_sub(b[i], bv[i]) for i in range(3)],
            [_add(bv[i], b[i]) for i in range(3)],
            [_add(av[i], a[i]) for i in range(3)]]


def quad_membership(quad, query, radius, height):
    """Native condition order; returns acceptance and diagnostic branch."""
    inside = True
    for i, a in enumerate(quad):
        b = quad[(i + 1) & 3]
        cross = _sub(_mul(_sub(query[1], a[1]), _sub(b[0], a[0])),
                     _mul(_sub(b[1], a[1]), _sub(query[0], a[0])))
        if cross > 0:
            inside = False
            break
    if inside:
        return True, "quad_xy_containment"
    rr = _mul(radius, radius)
    for a in quad:
        dx, dy = _sub(query[0], a[0]), _sub(query[1], a[1])
        if rr >= _add(_mul(dy, dy), _mul(dx, dx)) and height >= a[2]:
            return True, "vertex_xy_radius_height"
    for i, a in enumerate(quad):
        if segment_distance_squared(a, quad[(i + 1) & 3], query) <= rr:
            return True, "edge_3d_radius"
    return False, "strip_rejected"


def evaluate_region(query_xyz, query_radius, height, region_center, region_radius, points, *, point_count=None):
    """Evaluate one complete 48-byte region plus its complete point sequence.

    None denotes unavailable operands. UNKNOWN never denotes rejection. Malformed
    inputs, nonfinite/subnormal operands or arithmetic beyond finite binary32 are
    conservatively UNKNOWN because the captured MXCSR state is unavailable.
    An empty complete point list means native point_count=0; missing list is None.
    Identity resolution, region enumeration and resource deduplication are callers'
    obligations. A one-point region uses broadphase only, ignoring point contents.
    """
    result = dict(schema=SCHEMA, status="UNKNOWN", accepted=None, branch=None,
                  provenance="static native transcription; synthetic qualification")
    if any(x is None for x in (query_xyz, query_radius, region_center, region_radius)):
        return {**result, "reason": "MISSING_NATIVE_OPERAND"}
    try:
        q = _vector(query_xyz, 3)
        center = _vector(region_center, 3)
        radius, rr = _vector([query_radius, region_radius], 2)
        if point_count is None:
            if points is None:
                return {**result, "reason": "MISSING_NATIVE_POINT_COUNT"}
            point_count = len(points)
        if isinstance(point_count, bool) or not isinstance(point_count, int) or not 0 <= point_count <= 0xffffffff:
            raise ValueError("invalid native point count")
        if points is not None and (not isinstance(points, (list, tuple)) or len(points) != point_count):
            raise ValueError("point count does not match complete sequence")
        if radius < 0 or rr < 0:
            raise ValueError("invalid radius/point sequence")
        dx, dy = _sub(center[0], q[0]), _sub(center[1], q[1])
        distance = _add(_mul(dy, dy), _mul(dx, dx))
        bound = _mul(_add(rr, radius), _add(rr, radius))
        if distance > bound:
            accepted, branch = False, "broadphase_rejected"
        elif point_count == 1:
            accepted, branch = True, "single_point_broadphase"
        elif point_count == 0:
            accepted, branch = False, "zero_points"
        else:
            if points is None or height is None:
                return {**result, "reason": "MISSING_MULTI_POINT_OPERAND"}
            h = _vector([height], 1)[0]
            ps = [_vector(p, 4) for p in points]
            if any(p[3] < 0 for p in ps):
                raise ValueError("negative point width")
            accepted, branch = False, "all_strips_rejected"
            for i in range(1, len(ps)):
                accepted, candidate_branch = quad_membership(strip_quad(ps[i-1], ps[i]), q, radius, h)
                if accepted:
                    branch = candidate_branch
                    break
        return {**result, "status": "KNOWN", "accepted": accepted, "branch": branch, "reason": None}
    except (ValueError, OverflowError, ZeroDivisionError, TypeError) as error:
        return {**result, "reason": "UNQUALIFIED_NUMERIC_OR_MALFORMED_INPUT", "detail": str(error)}
