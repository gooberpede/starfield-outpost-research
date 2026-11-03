# SPDX-License-Identifier: GPL-3.0-or-later
"""Exercise the disposition truth table without inventing any trial evidence.

Reads pinned authored forecast/oracle; writes an exclusive local receipt. No
game, build, external dependency, save, database or operational authority use.
"""
import os
import sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE','') not in ('','0'):
    raise RuntimeError('Python optimization is forbidden; invoke with -E -B')

import json
from pathlib import Path
import re
import d5am_prediction_oracle as oracle
from d5ad_baseline import guard, sha

ROOT = Path(__file__).resolve().parents[2]


def main():
    if len(sys.argv) != 2 or not re.fullmatch('[a-z0-9-]+', sys.argv[1]):
        raise ValueError('Fresh bounded label required')
    guard()
    out = ROOT/'.local-work/d5am'/(sys.argv[1]+'.json')
    if out.exists() or any(p.is_symlink() or p.is_junction() for p in (out, *out.parents)):
        raise ValueError('Fresh non-reparse output required')
    if sha(oracle.PREDICTION) != oracle.PIN:
        raise ValueError('Forecast changed')
    checks = []
    qualified = dict.fromkeys(oracle.REQUIRED, True)
    def check(name, actual, expected):
        checks.append(dict(name=name, actual=actual, expected=expected, passed=actual == expected))
    for mask in range(16):
        check('ordinary-mask-'+str(mask), oracle.classify(True, mask, qualified)['disposition'],
              'CONFIRMED' if mask == 3 else 'CONTRADICTED')
    for mask in (None, -1, 16, True, 3.0, '3'):
        check('domain-'+repr(mask), oracle.classify(True, mask, qualified)['disposition'], 'INCONCLUSIVE')
    for field in oracle.REQUIRED:
        for mask in (0, 3):
            facts = dict(qualified, **{field: False})
            check(field+'-'+str(mask), oracle.classify(True, mask, facts)['disposition'], 'INCONCLUSIVE')
    check('no-trial', oracle.classify(False, None, dict.fromkeys(oracle.REQUIRED, False))['disposition'], 'NOT TESTED')
    for name, attempted, mask, facts in (
            ('no-trial-with-sample', False, 3, qualified),
            ('missing-field', True, 3, {}),
            ('nonboolean-fact', True, 3, dict(qualified, first_eligible_trial=1)),
            ('nonboolean-attempt', 1, 3, qualified)):
        refused = False
        try:
            oracle.classify(attempted, mask, facts)
        except ValueError:
            refused = True
        check(name, refused, True)
    result = dict(schema='sor-d5am-prediction-controls/1', result='PASS' if all(c['passed'] for c in checks) else 'FAIL',
                  checks=checks, method_sha256=sha(__file__), oracle_sha256=sha(oracle.__file__), prediction_sha256=oracle.PIN,
                  scope='Synthetic disposition truth table only; no observed trial, coverage qualification or prediction confirmation.')
    with out.open('x', encoding='utf8', newline='\n') as stream:
        json.dump(result, stream, indent=2)
        stream.write('\n')
    print(json.dumps(dict(result=result['result'], checks=len(checks), out=str(out))))
    if result['result'] != 'PASS':
        raise SystemExit(1)


if __name__ == '__main__':
    main()
