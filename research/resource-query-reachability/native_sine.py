# SPDX-License-Identifier: GPL-3.0-or-later
"""Finite small-angle arithmetic model for the two pinned vector sine paths.

Reads caller-supplied constants extracted from the pinned executable. No I/O or
target execution. The coefficient table stays local. This explanatory method
follows D5H gap14's arithmetic, including explicit FMA versus separate rounding.
Angles beyond the witnessed fast-path threshold are rejected, not approximated.
"""
import math


def sine(angle, constants, fused):
    def c(va):
        values = constants[hex(va)]
        assert len(set(values)) == 1
        return values[0]

    absolute = abs(angle)
    assert math.isfinite(angle) and absolute < c(0x14882ecc0)
    biased = (math.fma(absolute, c(0x14882ed00), c(0x14882ed40)) if fused else
              absolute * c(0x14882ed00) + c(0x14882ed40))
    multiple = biased - c(0x14882ed40)
    assert multiple == int(multiple) and 0 <= multiple <= 2
    if fused:
        remainder = math.fma(-c(0x14882ef00), multiple, absolute)
        remainder = math.fma(-multiple, c(0x14882ef40), remainder)
        remainder = math.fma(-multiple, c(0x14882ef80), remainder)
    else:
        remainder = absolute
        for va in (0x14882ee00, 0x14882ee40, 0x14882ee80, 0x14882eec0):
            remainder = remainder - multiple * c(va)
    square = remainder * remainder
    polynomial = c(0x14882f140)
    for va in (0x14882f100, 0x14882f0c0, 0x14882f080, 0x14882f040, 0x14882f000, 0x14882efc0):
        polynomial = math.fma(polynomial, square, c(va)) if fused else polynomial * square + c(va)
    signed = -remainder if (int(multiple) & 1) ^ (angle < 0) else remainder
    correction = square * polynomial
    return math.fma(correction, signed, signed) if fused else signed + signed * correction
