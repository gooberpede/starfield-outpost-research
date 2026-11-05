# SPDX-License-Identifier: GPL-3.0-or-later
"""Design-only exact fixed-30 binomial calculations; no sample ingestion.

Original stdlib arithmetic. Equal-tailed Clopper-Pearson method consulted in
NIST handbook prc241.htm; no implementation copied or adapted. Reads integer
count from CLI, writes one exclusive JSON. Every output is a model calculation,
never an assertion that retail cold starts are IID or p=1/7.
"""
import os
import sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):
    raise RuntimeError('Use pinned Python -E -B without optimization')

from fractions import Fraction
import json
from math import comb
from pathlib import Path

from d5ad_baseline import guard


def distribution(n=30, p=Fraction(1, 7)):
    return [comb(n, k) * p ** k * (1 - p) ** (n - k) for k in range(n + 1)]


def interval(k, n=30):
    def tail(p, lower):
        limits = range(k, n + 1) if lower else range(k + 1)
        return sum(comb(n, j) * p ** j * (1 - p) ** (n - j) for j in limits)

    def solve(lower):
        lo, hi = 0., 1.
        for _ in range(100):
            mid = (lo + hi) / 2
            if (tail(mid, lower) < .025) == lower:
                lo = mid
            else:
                hi = mid
        return (lo + hi) / 2

    return [0. if k == 0 else solve(True), 1. if k == n else solve(False)]


def calculate(k):
    if type(k) is not int or not 0 <= k <= 30:
        raise ValueError('Count must be an integer in [0,30]')
    pmf = distribution()
    pvalue = min(Fraction(1), 2 * min(sum(pmf[:k + 1]), sum(pmf[k:])))
    return dict(schema='sor-d5ar-fixed30-statistics/1', scope='DESIGN_ONLY_HYPOTHETICAL_IID_MODEL',
                n=30, p0='1/7', count=k, fraction=k / 30,
                pmf=[dict(k=j, exact=str(p), probability=float(p)) for j, p in enumerate(pmf)],
                two_sided_equal_tailed_p_exact=str(pvalue), two_sided_equal_tailed_p=float(pvalue),
                confidence_interval_95_clopper_pearson=interval(k),
                historical_sampled_mask_inference='NOT_ESTABLISHED')


if __name__ == '__main__':
    guard()
    if len(sys.argv) != 3:
        raise SystemExit('Usage: d5ar_statistics.py COUNT FRESH-OUTPUT.json')
    value = calculate(int(sys.argv[1]))
    guard()
    with Path(sys.argv[2]).open('x', encoding='utf8', newline='\n') as stream:
        stream.write(json.dumps(value, sort_keys=True, indent=2) + '\n')
