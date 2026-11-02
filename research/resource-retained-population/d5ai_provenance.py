# SPDX-License-Identifier: GPL-3.0-or-later
"""Pin D5AI authored methods, inherited sources and explicit primary receipts.

Reads repository text and selected local evidence; writes an exclusive local
receipt and the authored source CSV. Stdlib only. Does not execute evidence,
open Ghidra, touch saves/processes/network or mutate Git. Pins are provenance,
not proof of semantics or an attestation of perfect required-reading order.
Requires Python -E -B and both-drive caller-space guard. Raw payloads stay local.
"""
import argparse
import csv
import datetime
import json
from pathlib import Path
import subprocess
import sys

from d5ae_baseline import guard, sha

ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / 'docs/experiments/resource-retained-population'


def main():
    if not __debug__ or sys.flags.optimize:
        raise RuntimeError('Use Python -E -B')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('out', type=Path)
    parser.add_argument('--receipt', type=Path, action='append', default=[])
    args = parser.parse_args()
    free = guard()
    if not args.out.resolve().is_relative_to(ROOT / '.local-work/d5ai'):
        raise ValueError('Task-local output required')
    args.out.mkdir(exist_ok=False)
    baseline = json.loads((ROOT / '.local-work/d5ai/baseline.json').read_bytes())
    head = subprocess.check_output(['git', '--no-optional-locks', 'rev-parse', 'HEAD'], cwd=ROOT).decode().strip()
    if head != baseline['head'] or sha(ROOT / '.git/index') != baseline['index_sha256']:
        raise ValueError('HEAD/index drift')
    inherited = [ROOT / p for p in (
        'research/resource-retained-population/d5af_geometry.py',
        'research/resource-retained-population/d5ae_baseline.py',
        'research/resource-retained-population/d5ah_package.py',
        'research/resource-retained-population/d5ah_preserve.py',
        'runtime/retained-population/export_review.py',
        'runtime/construction-winner/read_capture.py',
        'runtime/construction-winner/reduce_v4.py',
        'runtime/construction-winner/observer.h',
        'runtime/construction-winner/transport.cpp',
        'runtime/construction-winner/p4_controller.py')]
    for path in inherited:
        name = path.relative_to(ROOT).as_posix()
        if sha(path) != baseline['files'][name]['sha256']:
            raise ValueError('Inherited source changed: ' + name)
    authored = sorted((ROOT / 'research/resource-retained-population').glob('d5ai_*'))
    authored += sorted((ROOT / 'research/resource-retained-population').glob('d5ai-*'))
    authored += sorted((ROOT / 'runtime/construction-winner').glob('d5ai_*'))
    authored.append(ROOT / 'research/resource-retained-population/ExploreD5AIManager.java')
    paths = inherited + authored + args.receipt
    rows = []
    for ordinal, path in enumerate(dict.fromkeys(p.resolve() for p in paths), 1):
        if not path.is_file():
            raise ValueError('Explicit evidence file missing: ' + str(path))
        local = path.is_relative_to(ROOT / '.local-work')
        rows.append(dict(id=f'D5AI-M{ordinal:03}', path=str(path), sha256=sha(path), bytes=path.stat().st_size,
                         locator='Complete file; explicit native addresses and instruction windows remain in ownership source ledger' if local else 'Complete authored method or pinned inherited source',
                         lineage='SOR-P-0002 owned source-informed adaptation; inherited baseline commit ' + head,
                         eligibility='LOCAL-ONLY' if local else 'REVIEW-REQUIRED'))
    with (DOC / 'd5ai-sources.csv').open('w', encoding='utf8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)
    result = dict(head=head, index_sha256=baseline['index_sha256'], utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  sources=rows, free=free, method_sha256=sha(__file__),
                  ownership_sources_sha256=sha(DOC / 'd5ai-ownership-sources.csv'),
                  reading_order='FAIL: disclosed truncated-reading and late historical-contract recovery; pins do not repair chronology')
    (args.out / 'receipt.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf8', newline='\n')
    print(json.dumps(dict(source_rows=len(rows), head=head)))


if __name__ == '__main__':
    main()
