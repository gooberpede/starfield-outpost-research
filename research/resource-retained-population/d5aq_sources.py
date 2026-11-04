# SPDX-License-Identifier: GPL-3.0-or-later
"""Index D5AQ evidence identities without exporting proprietary payloads.

Reads explicit local/native/owned evidence and source indices. Writes the authored
source CSV and one fresh ignored receipt containing its hash. No game, save,
database, installed-file, network or Git mutation. Requires existing evidence;
refuses missing files, reparse output and disk-floor failure. Publication status
is recorded separately from byte identity and scientific confidence.
"""
import os
import sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):
    raise RuntimeError('Use pinned Python -E -B without optimization')

import argparse
import csv
from pathlib import Path
from d5ap_analyze import ROOT, guard, require, sha, write


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--census', type=Path, required=True)
    parser.add_argument('--startup', type=Path, required=True)
    parser.add_argument('--verification', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    floors = guard()
    out = args.out.resolve()
    require(out.is_relative_to(ROOT / '.local-work/d5aq') and not out.exists(), 'Fresh D5AQ output')
    require(not any(p.is_symlink() or p.is_junction() for p in (out, *out.parents)), 'No reparse output')
    paths = [
        (args.census, 'All 196 independent conversion and conditional mask comparisons'),
        (args.startup, '392 original native samples and two numeric startup preimages'),
        (args.verification, 'Cross-source native/oracle/CSV/geometry and optimization checks'),
        (ROOT / '.local-work/d5ap/d5aq-auth01/summary.json', 'Fresh original N2 extraction and authenticated result identities'),
        (ROOT / '.local-work/d5ap/d5aq-auth01/authentication.json', 'All 174 retained payloads/archive members and 484 source pins'),
        (ROOT / '.local-work/d5aq/geometry01/control.json', 'First fresh complete native ordinary-stage process'),
        (ROOT / '.local-work/d5aq/geometry02/control.json', 'Second independent complete native ordinary-stage process'),
        (ROOT / '.local-work/d5aq/extra-inputs01.json', 'Fixed main-file Special and Everywhere applicability'),
        (ROOT / '.local-work/d5aq/preservation01.json', 'Selected protected originals and installed-input comparison'),
        (ROOT / '.local-work/d5aq/native-replay04/replay.json', 'Fresh eleven-method ordinary native transition replay'),
        (ROOT / '.local-work/d5aq/native-replay04/d5aq-invocation.json', 'Exact guarded native-replay method and result identities'),
        (ROOT / '.local-work/d5aq/owner-native04/d5aq-invocation.json', 'Exact guarded owner-audit method and result identities'),
        (ROOT / '.local-work/d5aq/source-baseline02.json', 'Initial HEAD/index and tracked-source preservation baseline'),
    ]
    for number in range(2, 11):
        paths.append((ROOT / f'.local-work/d5aq/owner-native04/owner-census{number:02d}.json', 'Receiver/alias census original-instruction byte audit'))
    for name in ('d5s', 'd5t', 'd5ae', 'd5af', 'd5ag'):
        paths.append((ROOT / f'docs/experiments/resource-retained-population/{name}-sources.csv', 'Inherited exact primary native/file/line source locators'))
    paths += [(p, 'D5AQ owned reproducible method; SOR-P-0002 lineage stated in source') for p in sorted((ROOT / 'research/resource-retained-population').glob('d5aq_*.py'))]
    rows = []
    for index, (path, use) in enumerate(paths, 1):
        path = path.resolve()
        require(path.is_file(), 'Missing source: ' + str(path))
        rows.append(dict(id=f'D5AQ-S{index:03d}', path=path.relative_to(ROOT).as_posix(),
                         sha256=sha(path), use=use,
                         eligibility='LOCAL-ONLY' if '.local-work' in path.parts else 'REVIEW-REQUIRED'))
    target = ROOT / 'docs/experiments/resource-retained-population/d5aq-sources.csv'
    with target.open('w', encoding='utf8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)
    write(out, dict(status='PASS', rows=len(rows), csv_sha256=sha(target),
                    method_sha256=sha(__file__), floors=floors, postflight_floors=guard()))
    print(f'PASS {len(rows)} source records')


if __name__ == '__main__':
    main()
