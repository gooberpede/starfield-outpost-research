# D5AO N2 derivative of owned N1 prediction oracle under SOR-P-0002.
# SPDX-License-Identifier: GPL-3.0-or-later
"""Evaluate the frozen next-trial mask rule after separate evidence adjudication.

Reads one explicit adjudication JSON; writes a fresh local result. This rule
does not establish coverage, authenticate adjudication, operate a target, or
turn lossless sidecars into scientific completeness. Stdlib only. The reviewer
must bind the adjudication to actual trial/source/coverage/postflight evidence.
"""
import os
import sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE','') not in ('','0'):
    raise RuntimeError('Python optimization is forbidden; invoke with -E -B')

import json
from pathlib import Path
import re
from d5ad_baseline import guard, sha

ROOT = Path(__file__).resolve().parents[2]
PREDICTION = ROOT/'docs/experiments/resource-retained-population/d5ao-n2-prediction-text-v1.md'
PIN = 'cc4275df23cd70653fe37c31f025eec84aa5aa30c87676376418540c97a4ec2b'
REQUIRED = ('first_eligible_trial', 'independent_process_and_context',
            'exact_source_and_constructing_sample', 'required_causal_coverage',
            'complete_required_recording', 'full_protected_postflight')


def classify(attempted, mask, qualifications):
    """Pure disposition rule; qualification facts are external reviewed inputs."""
    if type(attempted) is not bool or set(qualifications) != set(REQUIRED):
        raise ValueError('Exact adjudication fields required')
    if any(type(value) is not bool for value in qualifications.values()):
        raise ValueError('Qualification values must be booleans')
    if not attempted:
        if mask is not None or any(qualifications.values()):
            raise ValueError('No-trial adjudication cannot claim observations')
        return dict(disposition='NOT TESTED', reasons=['No new attempted trial'])
    reasons = [name for name in REQUIRED if not qualifications[name]]
    anomaly = type(mask) is not int or not 0 <= mask <= 15
    if anomaly:
        reasons.append('Unbound sample or native-domain anomaly; preserve without masking/replacement')
    if reasons:
        return dict(disposition='INCONCLUSIVE', reasons=reasons)
    return dict(disposition='CONFIRMED' if mask == 3 else 'CONTRADICTED', reasons=[])


def unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('Duplicate JSON key')
        result[key] = value
    return result


def main():
    if len(sys.argv) != 3 or not re.fullmatch('[a-z0-9-]+', sys.argv[2]):
        raise ValueError('Usage: adjudication.json fresh-label')
    guard()
    source = Path(sys.argv[1]).resolve()
    record = json.loads(source.read_text(encoding='utf8'), object_pairs_hook=unique,
                        parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)))
    if set(record) != {'schema', 'prediction_sha256', 'attempted', 'mask', 'qualifications', 'evidence', 'review'}:
        raise ValueError('Exact adjudication schema required')
    if record['schema'] != 'sor-d5ao-n2-prediction-adjudication/1' or record['prediction_sha256'] != PIN or sha(PREDICTION) != PIN:
        raise ValueError('Prediction identity mismatch')
    if record['attempted'] and (not isinstance(record['evidence'], dict) or
            set(record['evidence']) != set(REQUIRED) or not all(isinstance(v, str) and v.strip() for v in record['evidence'].values()) or
            not isinstance(record['review'], str) or not record['review'].strip()):
        raise ValueError('Evidence references and independent adjudication required; this is not their authentication')
    result = classify(record['attempted'], record['mask'], record['qualifications'])
    out = ROOT/'.local-work/d5ao/n2-live01'/(sys.argv[2]+'.json')
    if out.exists() or any(p.is_symlink() or p.is_junction() for p in (out, *out.parents)):
        raise ValueError('Fresh non-reparse output required')
    result.update(schema='sor-d5ao-n2-prediction-result/1', adjudication_sha256=sha(source),
                  prediction_sha256=PIN, method_sha256=sha(__file__),
                  limit='Disposition rule only; supplied evidence/coverage/review remain separately authenticated.')
    with out.open('x', encoding='utf8', newline='\n') as stream:
        json.dump(result, stream, indent=2)
        stream.write('\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
