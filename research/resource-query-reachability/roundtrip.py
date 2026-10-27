# SPDX-License-Identifier: GPL-3.0-or-later
"""Interior native-query numerical model, with explicit binary32 boundaries.

Instruction-derived from D5H's pinned 14078d660, 142332410, 142339340 and
1423321f0 exports. Default mode is a Python-math comparison. Explicit constants
select either native SIMD fast arithmetic path; scalar_math supplies the pinned
offline CRT cos/atan2 host. Qualifications are interior charts, RN and the caller's
coherent frame. No I/O, generation, target or saved-state access.
"""
import math
import struct


def f32(value):
    return struct.unpack('<f', struct.pack('<f', value))[0]


def projected(chart, x, y, *, constants=None, fused=False, scalar_math=math):
    if chart not in (0, 1) or not (0 <= x < 49152 and 0 <= y < 49152):
        raise ValueError('Qualified interior chart domain')
    # Interior 14096f5c0 recomposition; query and descriptor share this frame.
    x = (x + 0.5) * (1.0 / 49152) - 0.5
    y = (y + 0.5) * (1.0 / 49152) - 0.5
    xx, yy = x + x, y + y
    u = max(-1.0, min(1.0, xx * math.sqrt(1.0 - yy * yy * 0.5)))
    v = max(-1.0, min(1.0, yy * math.sqrt(1.0 - xx * xx * 0.5)))
    reciprocal = 1.0 / (u * u + 1.0 + v * v)
    vx = (u + u) * reciprocal
    vy = (v + v) * reciprocal
    vz = ((v * v + u * u) - 1.0) * reciprocal
    if chart == 1:
        vx = -vx
    else:
        vz = abs(vz)
    longitude = scalar_math.atan2(vy, vx)
    horizontal = f32(math.sqrt(f32(vx * vx + vy * vy)))
    latitude = scalar_math.atan2(vz, horizontal)
    cosine = scalar_math.cos(latitude)
    if constants is None:
        vx = math.cos(longitude) * cosine
        vy = math.sin(longitude) * cosine
        vz = math.sin(latitude)
    else:
        from native_sine import sine
        vx = sine(longitude + 1.5707963267948966, constants, fused) * cosine
        vy = sine(longitude, constants, fused) * cosine
        vz = sine(latitude, constants, fused)
    normalizer = f32(1.0 / f32(math.sqrt(f32(vx * vx + vy * vy + vz * vz))))
    result_chart = int(normalizer * vz < 0.0)
    vx *= normalizer
    vy *= normalizer
    vz *= normalizer
    if result_chart:
        vx = -vx
    denominator = abs(vz) + 1.0
    u = max(-1.0, min(1.0, vx / denominator))
    v = max(-1.0, min(1.0, vy / denominator))
    a = (u * u + 2.0) - v * v
    b = (2.0 - u * u) + v * v

    def root(value):
        return math.sqrt(0.0 if abs(value) < 1e-7 else value)

    qx = root(u * 2.8284271247461903 + a) * 0.25 - root(a - u * 2.8284271247461903) * 0.25
    qy = root(v * 2.8284271247461903 + b) * 0.25 - root(b - v * 2.8284271247461903) * 0.25
    column = min(255, max(0, math.floor(256 * min(1.0, max(0.0, 0.5 + qx)))))
    row = min(255, max(0, math.floor((1.0 - min(1.0, max(0.0, 0.5 + qy))) * 256)))
    error = max(abs(qx - x), abs(qy - y)) * 49152
    return result_chart, column, row, error
