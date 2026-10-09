"""SPDX-License-Identifier: GPL-3.0-or-later
SOR-EXP-0015: original mathematical model of observed native terrain projection.
Source-informed by SOR-S-0127, pinned 1423321f0/142332410; no decompiled text
copied. Stdlib only, no I/O or target effects. This is NOT an exact-beacon API.
Double mathematical model; native mixed-float rounding is separately disclosed.
"""
import math
import struct


def f32(value):
    return struct.unpack('<f', struct.pack('<f', value))[0]


def to_square(longitude, latitude):
    """Unit sphere -> hemisphere tag and centred square in [-.5,.5].
    Actual angle encoder emits tags 0 (north) / 1 (south), not six cube faces.
    Longitude is engine-oriented; no texture/compass calibration is implied.
    """
    if not all(math.isfinite(x) for x in (longitude, latitude)):
        raise ValueError('NONFINITE')
    if abs(latitude) > math.pi/2:
        raise ValueError('LATITUDE_RANGE')
    x = math.cos(latitude)*math.cos(longitude)
    y = math.cos(latitude)*math.sin(longitude)
    z = math.sin(latitude)
    tag = int(z < 0)
    a = (-x if tag else x)/(1+abs(z))
    b = y/(1+abs(z))
    k = 2*math.sqrt(2)
    def component(a, b):
        p = 2+a*a-b*b
        return (math.sqrt(max(0, p+k*a))-math.sqrt(max(0, p-k*a)))/4
    return tag, component(a, b), component(b, a)


def from_square(tag, u, v, native_latitude_rounding=False):
    """Four native tags supported; 2/3 occur in seam/index operations.
    Optional latitude rounding models sqrtss after double horizontal norm;
    platform atan2 and all native instruction rounding are not reproduced.
    """
    if tag not in (0, 1, 2, 3) or not all(math.isfinite(x) for x in (u, v)):
        raise ValueError('INVALID_SQUARE')
    if max(abs(u), abs(v)) > .5:
        raise ValueError('SQUARE_RANGE')
    a = 2*u*math.sqrt(1-2*v*v)
    b = 2*v*math.sqrt(1-2*u*u)
    denominator = 1+a*a+b*b
    x, y = 2*a/denominator, 2*b/denominator
    z = (a*a+b*b-1)/denominator
    if tag in (1, 2):
        x = -x
    if tag in (2, 3):
        y = -y
    if tag in (0, 2):
        z = abs(z)
    h2 = x*x+y*y
    horizontal = (f32(math.sqrt(f32(h2))) if native_latitude_rounding
                  else math.sqrt(h2))
    return math.atan2(y, x), math.atan2(z, horizontal)


def grid_cell(longitude, latitude, block=12, resolution=256):
    """Mathematical uniform quantizer, not native bit-exact nested fmod path."""
    if block <= 0 or resolution <= 0:
        raise ValueError('GRID_SIZE')
    tag, u, v = to_square(longitude, latitude)
    n = 16*block*resolution
    return tag, min(n-1, max(0, math.floor((u+.5)*n))), min(n-1, max(0, math.floor((v+.5)*n)))


def grid_centre(tag, i, j, block=12, resolution=256, native=False):
    n = 16*block*resolution
    if n <= 0 or not (0 <= i < n and 0 <= j < n):
        raise ValueError('INDEX_RANGE')
    return from_square(tag, (i+.5)/n-.5, (j+.5)/n-.5, native)


def split_local(value):
    """Observed float32 0.01 multiply then floor, followed by x - 100*q."""
    x = f32(value)
    q = math.floor(f32(x*f32(.01)))
    return q, f32(x-f32(q*100))
