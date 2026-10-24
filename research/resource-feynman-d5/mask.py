# SPDX-License-Identifier: GPL-3.0-or-later
"""Pure final native raster quantization, after geographic-to-chart conversion.

Caller supplies folded chart coordinates, dimensions and original raster bytes.
This does not reconstruct the missing first construction query or implement the
upstream trigonometric/chart conversion. No I/O or geometry-generation changes.
"""
import math


def raster_index(x, y, width, height):
    if not all(math.isfinite(v) for v in (x, y)):
        raise ValueError('NONFINITE_COORDINATE')
    if not all(type(v) is int and 0 < v < 2**31 for v in (width, height)):
        raise ValueError('DIMENSION_DOMAIN')
    u = min(1.0, max(0.0, 0.5 + x))
    v = min(1.0, max(0.0, 0.5 + y))
    column = min(width - 1, max(0, math.floor(width * u)))
    row = min(height - 1, max(0, math.floor((1.0 - v) * height)))
    return column + width * row


def sample(query, raster, width, height):
    if len(raster) != width * height:
        raise ValueError('RASTER_SIZE')
    return raster[raster_index(*query, width, height)] & 15
