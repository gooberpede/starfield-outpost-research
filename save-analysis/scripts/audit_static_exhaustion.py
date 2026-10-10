"""SPDX-License-Identifier: GPL-3.0-or-later
Original EXP0020 receipt comparison. Stdlib only; reads previously frozen durable
center / mature extraction and manually authored network JSON, writes one NEW
ignored output directory. No decoding, downloads, target or database effects.
Requires 40GB free on C:/D:. Names join independent examples, never infer bodies.
This checks identity, not continuous geographical accuracy.
"""
import argparse
import csv
import json
from pathlib import Path

from inventory_historical_saves import guard, identity


def compare_bodies(samples, frozen, manual):
    matches = [s for s in samples if s['metrics']['decoded_sha256'] == frozen['decoded_sha256']]
    if len(matches) != 1:
        raise ValueError('FROZEN_SAMPLE_NOT_UNIQUE')
    saved = matches[0]['extraction']['beacons']
    rows = []
    for op in manual['networks'][0]['network']['outposts']:
        candidates = [b for b in saved if not b['saved_disabled'] and
                      any(n['text'] == op['name'] for n in b['name_for_comparison'])]
        if len(candidates) != 1:
            raise ValueError('NAME_JOIN_NOT_UNIQUE')
        b = candidates[0]
        direct = sorted({p['body_formid'] for p in b['points']})
        cache = sorted({v['formid'] for c in b['cache'] for v in c['body_options']})
        systems = sorted({c['system_id'] for c in b['cache']})
        expected_body, expected_system = int(op['bodyId'], 16), int(op['systemId'])
        rows.append(dict(name=op['name'], token=b['token'],
                         body=f'{expected_body:08X}', system=expected_system,
                         direct_equal=direct == [expected_body],
                         cache_equal=cache == [expected_body],
                         system_equal=systems == [expected_system]))
    if len(rows) != sum(not b['saved_disabled'] for b in saved):
        raise ValueError('ACTIVE_MEMBERSHIP_MISMATCH')
    return rows


def main():
    ap = argparse.ArgumentParser()
    for name in ('samples', 'frozen', 'manual', 'output'):
        ap.add_argument('--'+name, type=Path, required=True)
    a = ap.parse_args()
    guard(a.output.parent)
    paths = [a.samples, a.frozen, a.manual]
    before = [identity(p) for p in paths]
    # Inputs must already have been extracted/frozen; this tool cannot inspect
    # the comparison document until both save-derived files have been loaded.
    samples = json.loads(a.samples.read_text(encoding='utf8'))
    frozen = json.loads(a.frozen.read_text(encoding='utf8'))
    manual = json.loads(a.manual.read_text(encoding='utf8'))
    rows = compare_bodies(samples, frozen, manual)
    after = [identity(p) for p in paths]
    if before != after:
        raise ValueError('INPUT_CHANGED')
    a.output.mkdir(exist_ok=False)
    with (a.output/'body-comparison.csv').open('x', encoding='utf8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    result = dict(before=before, after=after, examples=len(rows),
                  all_equal=all(all(r[k] for k in ('direct_equal', 'cache_equal', 'system_equal')) for r in rows),
                  coverage='Active ordinary outposts in frozen Save52 extraction; no continuous-coordinate ground truth')
    (a.output/'receipt.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf8')
    if not result['all_equal']:
        raise ValueError('INDEPENDENT_IDENTITY_MISMATCH')
    print('Independent body/cache/system matches:', len(rows))


if __name__ == '__main__':
    main()
