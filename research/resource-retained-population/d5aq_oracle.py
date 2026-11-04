# SPDX-License-Identifier: GPL-3.0-or-later
"""Independent numerical reference for the qualified interior atlas pipeline.

Original D5AQ implementation, informed by the native paths cited in the method.
Uses a rationalized inverse and host libm, not roundtrip.py or native_sine.py.
Pure arithmetic; no I/O, target, save or database access. Binary32 boundaries
remain explicit. This reference checks atlas cells, not native point geometry.
"""
import os
import sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):
    raise RuntimeError('Use pinned Python -E -B without optimization')

import math
import struct
from decimal import Decimal, localcontext


def binary32(value):
    return struct.unpack('<f', struct.pack('<f', value))[0]


def convert(descriptor, query, dimension=256, step=12):
    """Recompose interior mixed-radix coordinates without native normalization."""
    chart, coarse, sub, fine = descriptor
    if chart not in (0, 1) or dimension <= 0 or step <= 0:
        raise ValueError('Unqualified descriptor')
    face = [16 * step * coarse[i] + step * sub[i] + fine[i] + query[i] for i in (0, 1)]
    extent = dimension * 16 * step
    if any(v < 0 or v >= extent for v in face):
        raise ValueError('Outside the qualified interior chart')
    with localcontext() as ctx:
        ctx.prec = 70
        scale = Decimal.from_float(float(Decimal(1) / Decimal(extent)))
        normalized = [float(Decimal.from_float(float((Decimal(v) + Decimal('0.5')) * scale)) - Decimal('0.5')) for v in face]
    return chart, face, normalized


def sample(descriptor, query, raster, dimension=256, step=12):
    """Evaluate a separate sphere/inverse route and return the exact atlas cell."""
    if raster is None:
        raise ValueError('Raster unavailable; no mask assigned')
    chart, face, normalized = convert(descriptor, query, dimension, step)
    a, b = (2 * n for n in normalized)
    sx = a * math.sqrt(1 - b * b / 2)
    sy = b * math.sqrt(1 - a * a / 2)
    divisor = 1 + sx * sx + sy * sy
    vector = [2 * sx / divisor, 2 * sy / divisor, abs((sx * sx + sy * sy - 1) / divisor)]
    if chart:
        vector[0] = -vector[0]
        vector[2] = -vector[2]
    lon = math.atan2(vector[1], vector[0])
    lat = math.atan2(vector[2], binary32(math.sqrt(binary32(vector[0] ** 2 + vector[1] ** 2))))
    vector = [math.cos(lon) * math.cos(lat), math.sin(lon) * math.cos(lat), math.sin(lat)]
    norm = binary32(1 / binary32(math.sqrt(binary32(sum(v * v for v in vector)))))
    vector = [v * norm for v in vector]
    hemisphere = int(vector[2] < 0)
    if hemisphere:
        vector[0] = -vector[0]
    u, v = (vector[i] / (1 + abs(vector[2])) for i in (0, 1))
    # Rationalization avoids subtracting the two close square roots used by
    # the primary instruction transcription.
    def inverse(p, q):
        common = 2 + p * p - q * q
        delta = math.sqrt(8) * p
        return delta / (2 * (math.sqrt(common + delta) + math.sqrt(common - delta)))
    xy = [inverse(u, v), inverse(v, u)]
    column = max(0, min(255, math.floor(256 * (0.5 + xy[0]))))
    row = max(0, min(255, math.floor(256 * (0.5 - xy[1]))))
    byte = raster['faces'][hemisphere]['mask'][256 * row + column]
    return dict(chart=hemisphere, face=face, normalized=normalized, column=column,
                row=row, byte=byte, mask=byte & 15)
