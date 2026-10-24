# SPDX-License-Identifier: GPL-3.0-or-later
"""Pin D4C source/result metadata; write authored CSV and fresh local checks.

Reads existing sources/receipts and runs only original offline unit tests.
No raw payload is copied into tracked outputs. Stdlib and owned methods only;
no target, input, database, network or Git writes. Run before review packaging.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import subprocess
import sys

from audit import ROOT, pin, write
from owner_map import reconstruct, ordinary_candidates


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--label', default='checks01')
    args = ap.parse_args()
    assert args.label and all(c in 'abcdefghijklmnopqrstuvwxyz0123456789-' for c in args.label)
    local = ROOT / '.local-work/resource-owner-root'
    out = local / args.label
    out.mkdir(exist_ok=False)
    frozen = local / 'freeze01'
    rows = json.loads((frozen / 'inputs-v1.json').read_text())['components']
    old_trace = json.loads((frozen / 'map-v1.json').read_text())
    result = reconstruct(rows)
    assert json.loads(json.dumps(result)) == old_trace
    assert pin(frozen / 'owner_map-at-freeze.py') == json.loads(
        (frozen / 'freeze-v1.json').read_text())['methods'][str(ROOT / 'research/resource-owner-root/owner_map.py')]
    candidates = ordinary_candidates(0x57d5, result['maps'], {0x57c4: 1, 0x57d5: 0})
    assert candidates == {k: v for k, v in json.loads((frozen / 'candidates-v1.json').read_text()).items()
                          if k in ('status', 'before_sort', 'ordered')}
    write(out / 'method-delta.json', dict(original=pin(frozen / 'owner_map-at-freeze.py'),
          final=pin(ROOT / 'research/resource-owner-root/owner_map.py'),
          frozen_trace_and_candidates_unchanged=True,
          change='Unresolved root fails before supplemental lookup; added negative test'))
    for label, directory, pattern in [('owner-map', 'resource-owner-root', 'test_*.py'),
                                       ('standalone', 'resource-standalone', 'test_*.py')]:
        run = subprocess.run([sys.executable, '-B', '-m', 'unittest', 'discover', '-s',
              str(ROOT / 'research' / directory), '-p', pattern, '-v'], cwd=ROOT, capture_output=True)
        (out / f'{label}-tests.txt').write_bytes(run.stdout + run.stderr)
        assert run.returncode == 0
    paths = {ROOT / 'docs/implementation-briefs/CODEX_BRIEF_SOR_RG2_D4C_owner_root_map_archimedes.md': 'Governing supplied brief'}
    for name in ('resource-tungsten-repair', 'resource-tungsten-acquisition', 'resource-save52-d3', 'resource-standalone'):
        paths[ROOT / 'docs/experiments' / name / 'sources.csv'] = 'Inherited evidence/method provenance'
    for relative in ('research/workshop-population/ReadSpecialist.java', 'research/workshop-population/export.ps1',
        'research/resource-standalone/builder.py', 'research/resource-standalone/corpus_d3.py',
        'research/resource-standalone/predictor_d3.py', 'research/resource-standalone/verify.py',
        'research/resource-standalone/isolate.py', 'research/resource-geometry/geometry.py',
        'research/resource-tungsten-acquisition/protection.py', 'research/resource-tungsten-acquisition/qualify.py',
        'runtime/session-tools/export_review.py', 'research/editorial/screen.py'):
        paths[ROOT / relative] = 'Owned method reused under SOR-P-0002'
    frozen_meta = json.loads((frozen / 'freeze-v1.json').read_text())
    for name in frozen_meta['inputs']:
        paths[Path(name)] = 'Pinned installed/owned/frozen input; see freeze field lineage'
    for p in (ROOT / 'research/resource-owner-root').glob('*.py'):
        paths[p] = 'Original authored D4C method'
    for name in ('resource-availability-cont-01.tsv', 'resource-availability-cont-11.tsv',
                 'resource-availability-ui-29.tsv', 'resource-milestone-b-producers-01.tsv',
                 'resource-availability-cont-13.tsv'):
        paths[ROOT / '.local-work/recon' / name] = 'Existing pinned STATIC evidence'
    specialist = ROOT / '.local-work/workshop-population-rework/specialist'
    paths[specialist / 'd4b-owner-map01.tsv'] = 'Existing bounded native map evidence'
    for p in specialist.glob('d4c-*'):
        paths[p] = 'New read-only STATIC export/log; creationrefs01 is preserved partial failure'
    for p in local.rglob('*'):
        if p.is_file():
            paths[p] = 'D4C local freeze, prediction, comparison, check or preservation receipt'
    for name in ('resource-save52/build-v1/normalized.json', 'resource-save52-d3/build-v6/normalized.json'):
        paths[ROOT / '.local-work' / name] = 'Unchanged frozen normalized corpus'
    for capture in (86, 87, 88, 89, 829, 2881, 2941):
        for suffix in ('.bin', '.ack.json'):
            paths[ROOT / f'.local-work/resource-tungsten-acquisition/retail-attempt01/capture-{capture:05d}{suffix}'] = 'Original native answer, read only after freeze'
    target = ROOT / 'docs/experiments/resource-owner-root/sources.csv'
    existing = {r['path']: r['id'] for r in csv.DictReader(target.open(encoding='utf8'))} if target.exists() else {}
    next_id = max((int(value.split('S')[-1]) for value in existing.values()), default=0) + 1
    with target.open('w', encoding='utf8', newline='') as stream:
        writer = csv.writer(stream, lineterminator='\n')
        writer.writerow(['id', 'path', 'bytes', 'sha256', 'use', 'eligibility'])
        for i, (p, use) in enumerate(sorted(paths.items()), 1):
            display = p.relative_to(ROOT).as_posix() if p.is_relative_to(ROOT) else str(p)
            identity = existing.get(display)
            if identity is None:
                identity = f'D4C-S{next_id:03d}'
                next_id += 1
            writer.writerow([identity, display, p.stat().st_size, pin(p), use,
                'REVIEW-REQUIRED authored method/metadata' if '.local-work' not in str(p) and p.is_relative_to(ROOT)
                else 'LOCAL-ONLY payload; metadata REVIEW-REQUIRED'])
    print('Freeze delta equal; owner-map and standalone tests PASS;', len(paths), 'source/result pins')


if __name__ == '__main__':
    main()
