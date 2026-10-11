"""SPDX-License-Identifier: GPL-3.0-or-later
Offline native-order arithmetic diagnostic, deliberately NOT an exact angular API.
Stdlib only; CLI reads angles, writes stdout. No target/file writes. Source-informed
by hash-pinned 1423321f0/14096ecb0/14096f4d0; see resumption algorithm/ledger.
Python trig is a surrogate for native SIMD/CRT and is never used to silently
populate a missing qualified site cell in durable_position_v2.
"""
import argparse
import json
import math
import struct


def f32(x):
    return struct.unpack('<f', struct.pack('<f', x))[0]


def square_xyz(x, y, z):
    if not all(math.isfinite(v) for v in (x, y, z)):
        raise ValueError('FINITE_VECTOR_REQUIRED')
    norm2 = ((y*y)+(x*x))+(z*z)
    norm = f32(math.sqrt(f32(norm2)))
    if norm == 0 or not math.isfinite(norm):
        raise ValueError('NORMALIZATION_DOMAIN')
    reciprocal = f32(f32(1.0)/norm)
    x, y, z = reciprocal*x, reciprocal*y, reciprocal*z
    tag = int(z < 0)
    if tag:
        x = -x
    denominator = abs(z)+1.0
    a, b = (max(-1.0, min(1.0, v/denominator)) for v in (x, y))
    aa, bb = a*a, b*b
    first, second = (aa+2.0)-bb, (2.0-aa)+bb
    ka, kb = 2.8284271247461903*a, 2.8284271247461903*b
    radii = [first+ka, first-ka, second+kb, second-kb]
    radii = [0.0 if abs(r) < 1e-7 else r for r in radii]
    if min(radii) < 0:
        raise ValueError('NEGATIVE_RADICAND')
    roots = [math.sqrt(r)*0.25 for r in radii]
    return tag, roots[0]-roots[1], roots[2]-roots[3]


def nested_axis(u):
    if not math.isfinite(u) or not -0.5 <= u <= 0.5:
        raise ValueError('SQUARE_DOMAIN')
    block, resolution = 12, 256
    width = 16*block
    n = width*resolution
    w = max(0.0, min(1.0-1.0/(block*n), u+0.5))
    coarse = math.floor(resolution*w)
    t = (math.fmod((width*resolution)*w, width)*(1.0/width))*16.0
    sub = math.floor(t)
    fine = math.floor((t-float(sub))*block)
    return dict(coarse=coarse, sub=sub, fine=fine,
                index=width*coarse+block*sub+fine, intermediate=t)


def kernel_sin(x, mode):
    """Recovered small-input SIMD lane, explicit AVX/FMA dispatch, RN assumed.

    Source: resumption-native-math-02-retry.tsv,14374dda0/14374e650.
    This is an instruction-derived implementation, not a runtime oracle.
    """
    if mode not in ('avx', 'fma') or not math.isfinite(x) or abs(x) >= 2**24:
        raise ValueError('SMALL_KERNEL_DOMAIN_OR_MODE')
    ax, magic = abs(x), float.fromhex('0x1.8p52')
    invpi = float.fromhex('0x1.45f306dc9c883p-2')
    if mode == 'avx':
        m = ax*invpi+magic
        n = m-magic
        r = ax
        for h in ('0x1.921fb4p1', '0x1.4442dp-23', '0x1.846988p-47', '0x1.8cc51701b839ap-71'):
            r = r-n*float.fromhex(h)
    else:
        m = math.fma(invpi, ax, magic)
        n = m-magic
        r = math.fma(-math.pi, n, ax)
        r = math.fma(-n, float.fromhex('0x1.1a62633145c06p-53'), r)
        r = math.fma(-n, float.fromhex('0x1.c1cd129024e09p-106'), r)
    sign = (struct.unpack('<Q', struct.pack('<d', m))[0] & 1) << 63
    v = struct.unpack('<d', struct.pack('<Q', struct.unpack('<Q', struct.pack('<d', r))[0] ^ sign))[0]
    s = r*r
    coefficients = [float.fromhex(h) for h in (
        '-0x1.55555555554a8p-3', '0x1.111111110a573p-7', '-0x1.a01a019a659ddp-13',
        '0x1.71de3806add1ap-19', '-0x1.ae6355aaa4a53p-26', '0x1.60e6bee01d83ep-33',
        '-0x1.9f1517e9f65f0p-41')]
    p = coefficients[-1]
    for c in reversed(coefficients[:-1]):
        p = math.fma(p, s, c) if mode == 'fma' else p*s+c
    q = s*p
    result = math.fma(q, v, v) if mode == 'fma' else v+v*q
    bits = struct.unpack('<Q', struct.pack('<d', result))[0]
    input_sign = struct.unpack('<Q', struct.pack('<d', x))[0] & (1 << 63)
    return struct.unpack('<d', struct.pack('<Q', bits ^ input_sign))[0]


def diagnose_mode(longitude, latitude, mode):
    if not all(math.isfinite(v) for v in (longitude, latitude)) or abs(latitude) > math.pi/2:
        raise ValueError('ANGLE_DOMAIN')
    # Native wrapper offsets SIMD lanes by pi/2; separate scalar cos(lat).
    # Scalar cos remains a libm surrogate; dispatch is explicit, never guessed.
    clat = math.cos(latitude)
    xyz = [kernel_sin(longitude+math.pi/2, mode)*clat,
           kernel_sin(longitude, mode)*clat, kernel_sin(latitude, mode)]
    tag, u, v = square_xyz(*xyz)
    x, y = nested_axis(u), nested_axis(v)
    return dict(status='MODEL-PREDICTED-DIAGNOSTIC', surrogate_xyz=xyz,
        square=[tag, u, v], cell=[tag, x['index'], y['index']], hierarchy=[x, y],
        dispatch=mode,
        unknowns=['imported scalar cos exactness', 'MXCSR environment',
                  'native same-operation output validation'])


def diagnose(longitude, latitude):
    if not math.isfinite(longitude) or abs(longitude) > math.pi:
        raise ValueError('CANONICAL_LONGITUDE_DOMAIN')
    candidates = {mode: diagnose_mode(longitude, latitude, mode) for mode in ('avx', 'fma')}
    cells = [value['cell'] for value in candidates.values()]
    return dict(status='MODEL-PREDICTED-DIAGNOSTIC', dispatch_candidates=candidates,
        cell_agreement=cells[0] == cells[1],
        unknowns=['unobserved CPU dispatch', 'imported scalar cos exactness',
                  'MXCSR environment', 'native same-operation output validation'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('longitude', type=float)
    parser.add_argument('latitude', type=float)
    args = parser.parse_args()
    print(json.dumps(diagnose(args.longitude, args.latitude), indent=2, allow_nan=False))
