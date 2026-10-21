# SPDX-License-Identifier: GPL-3.0-or-later
"""RG1 original offline research calculations; stdlib, no file/process effects.

Native lineage and qualified planar/context limits:
docs/experiments/resource-geometry/evaluator.md.
The generator models 1.16.244.0 0079a330 with explicit source operands.
The exact planar intersection operates on supplied finite dyadic polygons.
"""
from fractions import Fraction as F
from pathlib import Path
import math
import random
import struct
import sys

# Existing maintainer-authored arithmetic, not third-party implementation.
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'save-analysis/scripts'))
from resource_availability import generation_seed
from resource_spatial import f32, strip_quad


def add(a, b): return f32(a + b)
def sub(a, b): return f32(a - b)
def mul(a, b): return f32(a * b)


def number(x):
    if isinstance(x, bool) or not isinstance(x, (int, float)):
        raise ValueError('finite numeric operand required')
    return f32(x)


def vector(x, n):
    if not isinstance(x, (list, tuple)) or len(x) != n:
        raise ValueError('vector arity')
    return list(map(number, x))


class Draws:
    """Native MT recurrence plus existing CPython twist, never Python seed()."""
    def __init__(self, seed):
        state = [seed]
        for i in range(1, 624):
            x = state[-1]
            state.append((1812433253 * (x ^ (x >> 30)) + i) & 0xffffffff)
        self.rng = random.Random(0)
        self.rng.setstate((3, tuple(state) + (624,), None))
        self.words = []

    def uniform(self):
        word = self.rng.getrandbits(32)
        self.words.append(word)
        return mul(f32(f32(word) / 4294967296.0),
                   struct.unpack('<f', bytes.fromhex('58ff7f3f'))[0])

    def between(self, low, high):
        return add(mul(sub(high, low), self.uniform()), low)


def sincos(angle, c):
    """Owned scalar polynomial generalized from the prior fixed-angle study.
    c maps static VAs to freshly pinned binary32 constants, not magic fittings.
    """
    x = number(angle)
    q = mul(x, c[0x144f0416c])
    q = add(q, .5) if x >= 0 else sub(q, .5)
    if not -(2**31) < q < 2**31:
        raise ValueError('angle reduction outside qualified int32 domain')
    x = sub(x, mul(f32(int(q)), c[0x144f049f4]))
    sign = 1.0
    if x > c[0x144f04654]:
        x, sign = sub(c[0x144f048dc], x), -1.0
    elif x < c[0x144f052b0]:
        x, sign = sub(c[0x144f052f8], x), -1.0
    z = mul(x, x)
    s = mul(sub(c[0x144f03d80], mul(z, c[0x144f03d40])), z)
    s = mul(sub(s, c[0x144f03e00]), z)
    s = mul(add(s, c[0x144f03ed4]), z)
    s = mul(sub(s, c[0x144f04178]), z)
    s = mul(add(s, 1.0), x)
    co = mul(sub(c[0x144f03dc4], mul(z, c[0x144f03d58])), z)
    co = mul(sub(co, c[0x144f03e48]), z)
    co = mul(add(co, c[0x144f03fd4]), z)
    co = mul(sub(co, .5), z)
    return s, mul(add(co, 1.0), sign)


def unopposed_cell(request, constants):
    """Conditional single-cell point generation; UNKNOWN for unqualified context.
    No prior different-resource regions is a substantive precondition, not an
    assumption that ordinary multi-resource generation has no competition.
    """
    return _cell(request, constants, allow_competition=False)


def generate_cell(request, constants):
    """Planar semantic generator including prior different-resource rejection.
    Uses the analytically equivalent disk/oriented-rectangle generation shapes;
    native quaternion/library rounding at marginal boundaries is not certified.
    """
    return _cell(request, constants, allow_competition=True)


def _cell(request, constants, *, allow_competition):
    result = dict(schema='sor-rg1-cell/1', status='UNKNOWN', points=None,
                  source=request.get('source'), resource=request.get('resource'),
                  provenance=request.get('provenance'), native_equivalence='NOT_TESTED')
    required = ('packed_key', 'owner_key', 'cell', 'origin', 'clip_center',
                'clip_half', 'block', 'weight', 'source', 'resource', 'provenance')
    missing = [k for k in required if request.get(k) is None]
    if request.get('context_qualified') is not True:
        missing.append('qualified_source_frame_and_selection')
    if not allow_competition and request.get('prior_different_resources') != []:
        missing.append('unopposed_generation_precondition')
    if allow_competition and not isinstance(request.get('prior_different_resources'), list):
        missing.append('complete_prior_region_population')
    for key in ('source', 'resource', 'provenance'):
        if not isinstance(request.get(key), str) or not request[key].strip():
            missing.append('nonempty_' + key)
    if missing:
        return dict(result, missing=missing)
    try:
        cell, origin = request['cell'], request['origin']
        for p in (cell, origin):
            if len(p) != 2 or any(type(x) is not int or not -2**31 <= x < 2**31 for x in p):
                raise ValueError('native Int2 required')
        if any(not -2**31 <= cell[i]*100 < 2**31 for i in range(2)):
            raise ValueError('cell multiplication overflow outside qualified domain')
        block = vector(request['block'], 10)
        if any(x < 0 for x in block[:8]) or any(block[i] > block[i+1] for i in (0, 2, 4)):
            raise ValueError('unsupported descriptor domain')
        center, half = vector(request['clip_center'], 3), vector(request['clip_half'], 3)
        if min(half) < 0:
            raise ValueError('negative clip extent')
        weight = number(request['weight'])
        if weight < 0:
            raise ValueError('negative weight')
        prior = request['prior_different_resources']
        if allow_competition:
            for region in prior:
                if not isinstance(region.get('resource'), str) or not region['resource']:
                    raise ValueError('prior resource identity required')
                for point in region['points']:
                    p = vector(point, 4)
                    if p[2] != 0 or p[3] < 0:
                        raise ValueError('planar nonnegative prior geometry required')
        seed = generation_seed(request['packed_key'], request['owner_key'])
        rng = Draws(seed)
        points, attempts_log = [], []
        status = 'CONDITIONAL_PLANAR_CELL' if allow_competition else 'CONDITIONAL_UNOPPOSED_CELL'
        gate = mul(rng.uniform(), 100.0)
        threshold = mul(weight, block[7])
        if threshold <= gate:
            return dict(result, status=status, points=[],
                        seed=seed, words=rng.words, branch='chance_reject')
        raw_count = rng.between(block[0], block[1])
        floor_count = math.floor(raw_count)
        count = floor_count + (not sub(raw_count, f32(floor_count)) < rng.uniform())
        if not 0 <= count < 2**32:
            raise ValueError('count outside uint32')
        if count == 0:
            return dict(result, status=status, points=[],
                        seed=seed, words=rng.words, branch='zero_attempts')
        heading = mul(rng.uniform(), constants[0x144f049f4])
        for attempt in range(count):
            width = rng.between(block[2], block[3])
            if not points:
                p = [add(add(f32(cell[i]*100), mul(rng.uniform(), 100.0)), f32(origin[i]))
                     for i in range(2)] + [0.0]
            else:
                turn = mul(mul(rng.uniform(), constants[0x144f03f50]), block[6])
                direction_draw = rng.uniform()
                heading = sub(heading, turn) if direction_draw < .5 else add(heading, turn)
                # 14079a8c2 XORs heading's sign before the sin/cos call.
                sine, cosine = sincos(-heading, constants)
                length = rng.between(block[4], block[5])
                p = [add(points[-1][i], mul(length, d)) for i, d in enumerate((cosine, sine, 0.0))]
            # Nonnegative widths: expanded box contains shrunken box. Preserve
            # native subtract-before-compare arithmetic for the expanded branch.
            admitted = all(sub(abs(sub(p[i], center[i])), add(half[i], width)) <= 0
                           for i in range(3))
            rejected = admitted and allow_competition and competition_rejects(p+[width], request['resource'], prior)
            attempts_log.append(dict(attempt=attempt, point=p+[width], clipped=not admitted,
                                     competing=rejected, prior_accepted=len(points), heading=heading))
            if admitted and not rejected:
                points.append(p + [width])
        return dict(result, status=status, points=points,
                    seed=seed, words=rng.words, attempts=attempts_log,
                    native_bound='NOT_REPRODUCED', representation='ordered_xyz_width')
    except (ValueError, OverflowError, KeyError, TypeError) as e:
        return dict(result, missing=[str(e)])


def competition_rejects(candidate, resource, regions):
    """007af1a0's nine binary32 samples, then planar 0079b020 shape semantics.
    Retains the native incremental sphere broadphase: it can clip part of a
    variable-width rectangle and therefore is semantically observable.
    Point disks use positive width; segments use maximum endpoint width and
    closed longitudinal/perpendicular limits, not tapered availability quads.
    Rational tests preserve the semantic boundary without sampling error. Exact
    native atan2/quaternion rounding at that boundary remains unqualified.
    """
    x, y, z, w = vector(candidate, 4)
    if z != 0 or w < 0:
        raise ValueError('planar candidate required')
    samples = [(x,y)] + [(add(x,i*w),add(y,j*w))
                         for i,j in ((-1,-1),(1,-1),(-1,1),(1,1),(-1,0),(0,-1),(0,1),(1,0))]
    for region in regions:
        if region['resource'] == resource:
            continue
        pts = [vector(p,4) for p in region['points']]
        bound = native_bound(pts) if pts else None
        for sample in samples:
            if bound is None or not bound_contains(bound,sample):continue
            q = tuple(map(F,sample))
            for p in pts:
                width = F(p[3])
                if width > 0 and sum((q[i]-F(p[i]))**2 for i in (0,1)) <= width*width:
                    return True
            for a,b in zip(pts,pts[1:]):
                width = max(F(a[3]),F(b[3]))
                if width <= 0: continue
                d = [F(b[i])-F(a[i]) for i in (0,1)]
                v = [q[i]-F(a[i]) for i in (0,1)]
                ll = sum(x*x for x in d)
                if not ll: continue  # Endpoint disk covers this zero-length case.
                dot = sum(d[i]*v[i] for i in (0,1))
                cross = d[0]*v[1]-d[1]*v[0]
                if 0 <= dot <= ll and cross*cross <= width*width*ll:
                    return True
    return False


def native_bound(points):
    """0079a330 bound loop + 142bf4850 scalar binary32 sphere merge.

    Each later positive-width point merges max(previous width,current width).
    The first point initializes directly. Static VA 144f03d6c is f32(1e-6),
    freshly pinned by RG1 at EXE file offset 82850668, bytes bd378635.
    This sphere is a predicate operand, distinct from conservative_bound().
    """
    pts=[vector(p,4) for p in points]
    if not pts:raise ValueError('nonempty bound path required')
    bound=pts[0][:];previous=pts[0][3]
    for p in pts[1:]:
        if p[3]>0:
            other=p[:3]+[max(previous,p[3])]
            delta=[sub(bound[i],other[i]) for i in range(3)]
            d2=add(add(mul(delta[0],delta[0]),mul(delta[1],delta[1])),mul(delta[2],delta[2]))
            dr=sub(other[3],bound[3]);dr2=mul(dr,dr)
            if dr2<d2:
                d=f32(math.sqrt(d2));old_radius=bound[3]
                if d>f32(1e-6):
                    factor=mul(sub(d,dr),f32(.5/d))
                    bound[:3]=[add(mul(factor,delta[i]),other[i]) for i in range(3)]
                bound[3]=mul(add(add(other[3],d),old_radius),.5)
            elif dr>=0:bound=other
        previous=p[3]
    return bound


def bound_contains(bound,xy):
    delta=[sub(xy[i],bound[i]) for i in (0,1)]
    d2=add(mul(delta[0],delta[0]),mul(delta[1],delta[1]))
    r=max(bound[3],.5)
    return d2<=mul(r,r)


def populate_source(request, constants):
    """Finite source/resource/X/Y population with explicitly supplied key map.
    Selection/equal-rarity tie order/frame are evidence obligations of the input.
    No radius culling: outside-start paths and all earlier same-source geometry
    remain available. Packed-key derivation itself is a separate context stage.
    """
    out = dict(schema='sor-rg1-source/1',status='UNKNOWN',source=request.get('source'),
               provenance=request.get('provenance'),regions=None)
    try:
        if request.get('context_qualified') is not True:
            raise ValueError('qualified source envelope required')
        bounds = request['cell_bounds']
        if len(bounds)!=4 or any(type(i) is not int for i in bounds):
            raise ValueError('integer half-open cell bounds required')
        xmin,xmax,ymin,ymax = bounds
        if xmin>xmax or ymin>ymax:
            raise ValueError('inverted cell bounds')
        resources = request['ordered_resources']
        if not isinstance(resources,list) or not request.get('order_qualified'):
            raise ValueError('actual selected resource order required')
        keys = request['packed_keys']
        if any(f'{x},{y}' not in keys for x in range(xmin,xmax) for y in range(ymin,ymax)):
            raise ValueError('complete cell-to-native-packed-key map required')
        regions,cells = [],[]
        for resource in resources:
            for x in range(xmin,xmax):
                for y in range(ymin,ymax):
                    cell = {k:request[k] for k in ('source','provenance','origin','owner_key','clip_center','clip_half','context_qualified')}
                    cell.update(resource,cell=[x,y],packed_key=keys[f'{x},{y}'],prior_different_resources=regions)
                    result = generate_cell(cell,constants)
                    if result['status']=='UNKNOWN':
                        return dict(out,reason=result['missing'],completed_cells=cells)
                    cells.append(result)
                    if result['points']:
                        regions.append(dict(source=request['source'],resource=cell['resource'],cell=[x,y],
                                            points=result['points'],bound=conservative_bound(result['points']),
                                            native_bound=native_bound(result['points'])))
        return dict(out,status='CONDITIONAL_PLANAR_SOURCE',regions=regions,cells=cells,
                    coverage='all supplied finite source cells and ordered resources; actual-site binding separate')
    except (ValueError,TypeError,KeyError,OverflowError) as e:
        return dict(out,reason=str(e))


def conservative_bound(points):
    """Sound outward-rounded sphere for supplied endpoint disks AND strip vertices.
    Rechecks every inequality exactly; does not rely on libm rounding for soundness.
    Used as diagnostic geometry, not a claim of native center/radius equality.
    """
    p = [vector(v,4) for v in points]
    if not p: raise ValueError('nonempty path required')
    center = [(min(v[i] for v in p)+max(v[i] for v in p))/2 for i in (0,1)]
    radius = max(math.hypot(v[0]-center[0],v[1]-center[1])+v[3] for v in p)
    vertices = [v for a,b in zip(p,p[1:]) for v in strip_quad(a,b)]
    if vertices: radius=max(radius,max(math.hypot(v[0]-center[0],v[1]-center[1]) for v in vertices))
    def sound(r):
        rr = F(r)
        return (all(rr >= F(v[3]) and (rr-F(v[3]))**2 >= sum((F(v[i])-F(center[i]))**2 for i in (0,1)) for v in p)
                and all(rr*rr >= sum((F(v[i])-F(center[i]))**2 for i in (0,1)) for v in vertices))
    while not sound(radius): radius=math.nextafter(radius,math.inf)
    return dict(center=center,radius=radius,proof='all endpoint disks and binary32 strip vertices enclosed by exact rational checks')


def rational(x):
    if isinstance(x, bool) or not isinstance(x, (int, float, F)) or not math.isfinite(x):
        raise ValueError('finite dyadic geometry required')
    return F(x)


def region_membership(points, xy):
    """Planar 0079b020 semantic union of disks and max-width rectangles.

    This is the generator competition footprint at one point, without the
    candidate's nine-sample dilation. It differs from tapered area strips.
    Algebraic predicates avoid native atan2/quaternion boundary roundoff.
    """
    try:
        pts=[vector(p,4) for p in points];q=tuple(map(F,vector(xy,2)))
        if any(p[2]!=0 or p[3]<0 for p in pts): return 'UNKNOWN'
        if not pts or not bound_contains(native_bound(pts),xy):return 'OUTSIDE'
        boundary=False
        for p in pts:
            w=F(p[3]);d2=sum((q[i]-F(p[i]))**2 for i in (0,1))
            if w>0 and d2<w*w:return 'INTERIOR'
            if w>0 and d2==w*w:boundary=True
        for a,b in zip(pts,pts[1:]):
            w=max(F(a[3]),F(b[3]));d=[F(b[i])-F(a[i]) for i in (0,1)]
            v=[q[i]-F(a[i]) for i in (0,1)];ll=sum(x*x for x in d)
            dot=sum(d[i]*v[i] for i in (0,1));cross=d[0]*v[1]-d[1]*v[0]
            if ll and w>0 and 0<dot<ll and cross*cross<w*w*ll:return 'INTERIOR'
            if ll and w>0 and 0<=dot<=ll and cross*cross<=w*w*ll:boundary=True
        return 'BOUNDARY' if boundary else 'OUTSIDE'
    except (ValueError,TypeError,OverflowError):return 'UNKNOWN'


def region_circle(points, center, radius=150):
    """Positive-area disk/constant-width rectangle union versus nominal disk.

    Exact algebraic rectangle-distance decisions avoid normalized-vertex
    approximation; native quaternion marginal-boundary equivalence is unclaimed.
    """
    try:
        pts=[vector(p,4) for p in points];q=tuple(map(rational,center));r=rational(radius)
        if len(q)!=2 or r<=0 or any(p[2]!=0 or p[3]<0 for p in pts):
            raise ValueError('qualified planar path and positive disk required')
        outcomes=[]
        for p in pts:
            if p[3]<=0:continue
            d2=sum((q[i]-F(p[i]))**2 for i in (0,1));rr=(r+F(p[3]))**2
            outcomes.append('POSITIVE_AREA' if d2<rr else 'TANGENT_ONLY' if d2==rr else 'DISJOINT')
        for a,b in zip(pts,pts[1:]):
            outcomes.append(segment_rectangle_circle(a,b,center,radius))
        verdict=('POSITIVE_AREA' if 'POSITIVE_AREA' in outcomes else
                 'TANGENT_ONLY' if 'TANGENT_ONLY' in outcomes else 'DISJOINT_OR_ZERO_AREA')
        return dict(status='CONDITIONAL_PLANAR_REGION_UNION',intersection=verdict,parts=outcomes)
    except (ValueError,TypeError,OverflowError) as e:return dict(status='UNKNOWN',reason=str(e))


def segment_rectangle_circle(a,b,center,radius):
    """Exact max-width oriented rectangle/disk distance, without sqrt vertices.

    For outside-corner distance the comparison is A-B*sqrt(length_squared);
    signs plus squaring nonnegative operands decide it exactly over rationals.
    """
    a=list(map(F,a));b=list(map(F,b));q=list(map(F,center));r=F(radius)
    w=max(a[3],b[3]);d=[b[i]-a[i] for i in (0,1)]
    v=[q[i]-a[i] for i in (0,1)];ll=sum(x*x for x in d)
    if not ll or w<=0:return 'ZERO_AREA'
    dot=sum(d[i]*v[i] for i in (0,1));cross=abs(d[0]*v[1]-d[1]*v[0])
    along=-dot if dot<0 else dot-ll if dot>ll else F(0)
    if cross*cross<=w*w*ll:
        signed=along*along-r*r*ll
    elif along==0:
        signed=cross*cross-(w+r)**2*ll
    else:
        aa=along*along+cross*cross+(w*w-r*r)*ll
        bb=2*w*cross
        signed=F(-1) if aa<0 else aa*aa-bb*bb*ll
    return 'POSITIVE_AREA' if signed<0 else 'TANGENT_ONLY' if signed==0 else 'DISJOINT'


def bounded_region_circle(points,center,radius=150):
    """Certified decisions for the sphere-clipped planar primitive union.

    Outer-disjoint and inner-witness proofs are exact for the supplied binary32
    shape operands. Unresolved sphere/primitive/query boundary arrangements
    return UNKNOWN, never a sampled negative. Native transcendental rounding is
    still a separate correspondence limit. Tapered-strip intersection is exact
    over its constructed polygons and is reported separately.
    """
    outer=region_circle(points,center,radius)
    if outer['status']=='UNKNOWN':return outer
    if outer['intersection']=='DISJOINT_OR_ZERO_AREA':
        return dict(status='QUALIFIED_PLANAR_BOUNDED_UNION',intersection='DISJOINT_OR_ZERO_AREA',proof='primitive union disjoint')
    pts=[vector(p,4) for p in points];bound=native_bound(pts)
    q=list(map(F,center));br=F(max(bound[3],.5));r=F(radius)
    def inside(p,c,rr):return sum((F(p[i])-F(c[i]))**2 for i in (0,1))<rr*rr
    d2=sum((q[i]-F(bound[i]))**2 for i in (0,1))
    if d2>(br+r)**2:
        return dict(status='QUALIFIED_PLANAR_BOUNDED_UNION',intersection='DISJOINT_OR_ZERO_AREA',proof='native bound disjoint')
    if br>r and d2<(br-r)**2:
        return dict(status='QUALIFIED_PLANAR_BOUNDED_UNION',intersection=outer['intersection'],proof='query disk strictly inside native bound')
    witnesses=[p[:2] for p in pts if p[3]>0]+[center,bound[:2]]
    # Interior lens point on the line joining query and endpoint-disk centers.
    # This is a constructive proof candidate, never a sampled absence test.
    for p in pts:
        d=math.dist(p[:2],center)
        if p[3]>0 and d>0 and d<float(r)+p[3]:
            t=(max(0,d-p[3])+min(d,float(r)))/(2*d)
            witnesses.append([float(q[i])+t*(p[i]-float(q[i])) for i in (0,1)])
    for a,b in zip(pts,pts[1:]):witnesses.append([(F(a[i])+F(b[i]))/2 for i in (0,1)])
    for p in witnesses:
        p=list(map(f32,p))
        if inside(p,q,r) and inside(p,bound,br) and region_membership(pts,list(map(float,p)))=='INTERIOR':
            return dict(status='QUALIFIED_PLANAR_BOUNDED_UNION',intersection='POSITIVE_AREA',proof='strict interior witness',witness=list(map(float,p)))
    return dict(status='UNKNOWN',reason='sphere-clipped union boundary arrangement unresolved',outer=outer['intersection'])


def point_membership(points, xy):
    """Closed planar membership, separate from radius/height UI admission.
    Single-point generated regions have their initialized width-radius disk;
    multi-point regions use the union of consecutive nonzero-area tapered quads.
    """
    try:
        pts = [vector(p,4) for p in points]
        q = tuple(map(F,vector(xy,2)))
        if any(p[2] != 0 or p[3] < 0 for p in pts):
            raise ValueError('qualified planar path required')
        if len(pts)==1:
            d2=sum((q[i]-F(pts[0][i]))**2 for i in (0,1)); w=F(pts[0][3])
            return 'INTERIOR' if d2<w*w else 'BOUNDARY' if d2==w*w else 'OUTSIDE'
        boundary=False
        for a,b in zip(pts,pts[1:]):
            p=[tuple(map(F,v[:2])) for v in strip_quad(a,b)]
            area=sum(p[i][0]*p[(i+1)%4][1]-p[i][1]*p[(i+1)%4][0] for i in range(4))
            if area==0: continue
            crosses=[(p[(i+1)%4][0]-p[i][0])*(q[1]-p[i][1])-(p[(i+1)%4][1]-p[i][1])*(q[0]-p[i][0]) for i in range(4)]
            sign=1 if area>0 else -1
            if all(sign*x>0 for x in crosses): return 'INTERIOR'
            if all(sign*x>=0 for x in crosses): boundary=True
        return 'BOUNDARY' if boundary else 'OUTSIDE'
    except (ValueError,TypeError,OverflowError): return 'UNKNOWN'


def polygon_circle(vertices, center, radius=150):
    """Exact positive-area decision for a nondegenerate convex polygon/disk.
    Rational operations eliminate sample spacing and floating tolerance. Convex
    validation rejects folded/concave polygons rather than inferring membership.
    """
    p = [tuple(map(rational, xy)) for xy in vertices]
    if len(p) < 3 or any(len(xy) != 2 for xy in p) or len(center) != 2:
        raise ValueError('polygon/center arity')
    q = tuple(map(rational, center)); r = rational(radius)
    if r <= 0:
        raise ValueError('positive circle radius required')
    def cross(a, b, c):
        return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])
    area2 = sum(p[i][0]*p[(i+1)%len(p)][1]-p[i][1]*p[(i+1)%len(p)][0]
                for i in range(len(p)))
    if area2 == 0:
        distinct = next((v for v in p[1:] if v != p[0]), p[0])
        if all(cross(p[0], distinct, v) == 0 for v in p):
            return 'ZERO_AREA'
        raise ValueError('folded zero-signed-area polygon')
    sign = 1 if area2 > 0 else -1
    if any(sign * cross(p[i], p[(i+1)%len(p)], v) < 0
           for i in range(len(p)) for v in p):
        raise ValueError('nonconvex or folded polygon')
    if all(sign * cross(p[i], p[(i+1)%len(p)], q) >= 0 for i in range(len(p))):
        return 'POSITIVE_AREA'
    distances = []
    for a, b in zip(p, p[1:] + p[:1]):
        d = (b[0]-a[0], b[1]-a[1]); w = (q[0]-a[0], q[1]-a[1])
        ll = sum(x*x for x in d)
        t = max(F(0), min(F(1), sum(d[i]*w[i] for i in range(2))/ll)) if ll else F(0)
        distances.append(sum((w[i]-t*d[i])**2 for i in range(2)))
    least = min(distances)
    return 'POSITIVE_AREA' if least < r*r else 'TANGENT_ONLY' if least == r*r else 'DISJOINT'


def nominal_strips(points, center, radius=150):
    """Planar multi-point strip product, separately from native UI acceptance.
    Missing/singleton and nonplanar source geometries remain UNKNOWN; no invented
    endpoint disk or count-one geometry. Uses existing binary32 strip vertices.
    """
    if points is None or len(points) < 2:
        return dict(status='UNKNOWN', reason='multi-point geometry required', strips=[])
    try:
        pts = [vector(p, 4) for p in points]
        if any(p[3] < 0 or p[2] != 0 for p in pts):
            raise ValueError('qualified horizontal z=0 nonnegative-width path required')
        rows = []
        for a, b in zip(pts, pts[1:]):
            quad = [v[:2] for v in strip_quad(a, b)]
            rows.append(dict(vertices=quad, intersection=polygon_circle(quad, center, radius)))
        verdict = ('POSITIVE_AREA' if any(r['intersection']=='POSITIVE_AREA' for r in rows)
                   else 'TANGENT_ONLY' if any(r['intersection']=='TANGENT_ONLY' for r in rows)
                   else 'DISJOINT_OR_ZERO_AREA')
        return dict(status='CONDITIONAL_PLANAR_STRIPS', intersection=verdict, strips=rows)
    except (ValueError, OverflowError, TypeError) as e:
        return dict(status='UNKNOWN', reason=str(e), strips=[])
