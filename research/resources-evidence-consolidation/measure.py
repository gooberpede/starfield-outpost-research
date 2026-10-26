# SPDX-License-Identifier: GPL-3.0-or-later
"""Read frozen receipts/current allocation; write bounded measurements and table.

Runs only the committed read-only Cargo routine command. No source/save payload
analysis, policy activation, retirement, target, network or Git mutations.
"""
from collections import defaultdict
import csv
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time

from cutover import ROOT, OUT, DOC, store, save, e
from prepare import ARCHIVE_FOLDER, PROPOSED_INDEX


def run():
    admission = json.loads((OUT / 'admission.json').read_text())['rows']
    namespace = json.loads((OUT / 'namespace.json').read_text())
    members = [r for r in admission if r['disposition'] == 'PROPOSED-ARCHIVE-ONLY']
    holds = [r for r in admission if r['disposition'] != 'PROPOSED-ARCHIVE-ONLY']
    groups = defaultdict(lambda: dict(eligible_files=0, logical_bytes=0, reported_allocation=0,
                         recurring_pins=0, archived_files=0, held_files=0, protected_exclusions=0))
    for row in admission:
        group = groups[row['path'].split('/')[1]]
        group['eligible_files'] += 1
        group['logical_bytes'] += row['bytes']
        group['reported_allocation'] += row['allocated_bytes']
        group['recurring_pins'] += row['recurring_pin']
        group['archived_files'] += row['disposition'] == 'PROPOSED-ARCHIVE-ONLY'
        group['held_files'] += row['disposition'] != 'PROPOSED-ARCHIVE-ONLY'
    for row in namespace['exclusions']:
        groups[row['path'].split('/')[1]]['protected_exclusions'] += 1
    DOC.mkdir(parents=True, exist_ok=True)
    with (DOC / 'subareas.csv').open('x', encoding='utf8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=['subarea', *next(iter(groups.values()))], lineterminator='\n')
        writer.writeheader()
        writer.writerows(dict(subarea=name, **values) for name, values in sorted(groups.items()))
    allocated = []
    def charge(path):
        with e.locked(path) as (_, info):
            allocated.append(dict(path=str(path.relative_to(ROOT)), bytes=info.length, allocation=info.allocation))
    for folder, dirs, files in os.walk(OUT):
        dirs[:] = [d for d in dirs if not d.startswith('full-restore01')]
        for name in files:
            charge(Path(folder) / name)
    charge(ARCHIVE_FOLDER / 'resources-production.tar.zst')
    charge(ARCHIVE_FOLDER / 'journal.json')
    charge(PROPOSED_INDEX)
    charge(store().index)
    archive_check = store().verify(False)
    selection = json.loads((ROOT / 'docs/experiments/cargo-evidence-cutover/active-baseline.json').read_text())
    start = time.perf_counter()
    cargo = subprocess.run(selection['routine_command'], cwd=ROOT, capture_output=True)
    if cargo.returncode:
        raise e.Error('Original committed Cargo routine regression failed')
    save(OUT / 'cargo-regression.json', dict(command=selection['routine_command'], returncode=cargo.returncode,
         stdout=cargo.stdout.decode(), stderr=cargo.stderr.decode(), seconds=time.perf_counter()-start))
    # Additional Stage B/Cargo synthetic fixture costs and final review/journal
    # storage are conservatively covered by a separately stated 512 MiB reserve.
    credit = sum(r['allocated_bytes'] for r in members if r['bytes'] > 4096)
    cost = sum(r['allocation'] for r in allocated)
    reserve = 512 * 1024 * 1024
    removed = sum(r['recurring_pin'] for r in members)
    result = dict(eligible_files=len(admission), eligible_bytes=sum(r['bytes'] for r in admission),
         archived_files=len(members), archived_bytes=sum(r['bytes'] for r in members),
         held_files=len(holds), held_bytes=sum(r['bytes'] for r in holds), protected_exclusions=len(namespace['exclusions']),
         historical_before=93334, historical_system_overlap=sum(r['recurring_pin'] for r in admission),
         historical_pins_proposed_removed=removed, historical_after_loose=93334-removed,
         historical_after_with_two_archive_objects=93334-removed+2,
         combined_routine_payload_objects=93334-removed+2+len(holds),
         archived_not_in_historical_pins=sum(not r['recurring_pin'] for r in members),
         actual_current_pins_removed=0, actual_original_files_retired=0, actual_original_bytes_freed=0,
         conservative_source_allocation_credit=credit, measured_retained_preparation_allocation=cost,
         additional_fixture_review_journal_reserve=reserve,
         projected_net_allocation_recovery_lower_bound=credit-cost-reserve,
         projection_scope='After successful approved retirement and lease cleanup; excludes resident/MFT and directory recovery. Additional fixtures, future journal and final package fit inside the stated reserve.',
         archive_only_routine_measurement=archive_check,
         full_after_routine_seconds='NOT TESTED before GO; no committed sources are absent yet',
         historical_overlap_pin_scan=json.loads((OUT / 'pin-verification.json').read_text())['seconds'],
         before_free=json.loads((OUT / 'baseline.json').read_text())['free'], current_free=e.space(),
         source_allocation_scope='Windows reported allocation at admission; resident/small files get zero recoverable credit',
         subareas_csv_sha256=e.pin(DOC / 'subareas.csv'))
    save(OUT / 'allocation.json', allocated)
    save(OUT / 'measurements.json', result)
    print(json.dumps(result, indent=2), flush=True)


if __name__ == '__main__':
    run()
