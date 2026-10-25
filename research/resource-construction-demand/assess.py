# SPDX-License-Identifier: GPL-3.0-or-later
"""Audit closed journals and inherited pins; never execute a target or generator.

Reads existing source ledgers, native exports/logs, closed event journals and the
frozen ten-control ledger. Writes exclusive ignored JSON and a sanitized source
pin CSV. Requires installed Python 3.14, stdlib and project-owned audit.py.
No game, save, configuration, analysis database, index, ref or network writes.
Journal summaries are diagnostic transcription, not renewed SRO1 qualification.
"""
import collections
import csv
import datetime
import io
import json
from pathlib import Path
from audit import ROOT, OUT, pin, write

DOC = ROOT / 'docs/experiments/resource-construction-demand'
FOLDERS = ('resource-region-ancestry', 'resource-selection-operands',
           'resource-carinae', 'resource-carinae-source-context',
           'resource-tungsten-acquisition', 'resource-owner-acquisition',
           'resource-combined-acquisition')


def main():
    paths = set()
    inherited = 0
    ledgers = ['docs/experiments/resource-population-lifecycle/sources.csv']
    ledgers += [f'docs/experiments/{f}/phase-b-sources.csv' for f in FOLDERS]
    for name in ledgers:
        p = ROOT / name
        paths.add(p)
        for row in csv.DictReader(p.open(encoding='utf8')):
            p = ROOT / row['path']
            # Historical method code may have later authorized revisions. Only
            # the D5C ledger and immutable local evidence are requalified here.
            if '.local-work' in p.parts or 'resource-population-lifecycle' in name:
                assert pin(p) == row['sha256'], str(p)
                paths.add(p)
                inherited += 1
    streams = []
    for folder in FOLDERS:
        for p in sorted((ROOT / '.local-work' / folder).glob('retail-attempt*/events.jsonl')):
            counts = collections.Counter()
            selected, phases = [], []
            last = None
            for lineno, line in enumerate(p.open(encoding='utf8'), 1):
                row = json.loads(line)
                counts[row.get('site', row['kind'])] += 1
                if row['kind'] == 'PHASE':
                    phases.append(dict(line=lineno, record=row, previous_sample=last))
                if row['kind'] != 'SAMPLE':
                    continue
                small = {k: row[k] for k in ('capture', 'site', 'tid', 'thread_lifetime',
                    'provider_token', 'invocation_token', 'updater_token', 'source_key',
                    'source_pointer', 'population_epoch', 'utc_filetime_100ns') if k in row}
                if 'utc_filetime_100ns' in row:
                    small['utc'] = (datetime.datetime(1601, 1, 1, tzinfo=datetime.timezone.utc)
                        + datetime.timedelta(microseconds=row['utc_filetime_100ns'] // 10)).isoformat()
                if phases and 'next_sample' not in phases[-1]:
                    phases[-1]['next_sample'] = small
                if row.get('site') in ('region_accept', 'spatial_transfer_payload'):
                    selected.append(small)
                last = small
            paths.add(p)
            streams.append(dict(path=p.relative_to(ROOT).as_posix(), counts=dict(counts),
                                selected=selected, phases=phases))
    for n in range(1, 6):
        p = ROOT / f'.local-work/workshop-population-rework/specialist/d5d-demand{n:02}.tsv'
        t = p.read_text(encoding='utf8')
        assert t.rstrip().endswith('END') and 'BASE\t140000000' in t
        assert '7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28' in t
        assert 'ERROR ' not in p.with_suffix('.log').read_text(encoding='utf8')
        paths.update((p, p.with_suffix('.log')))
    control = ROOT / '.local-work/resource-construction-mask-selection/regression01/native-comparison.json'
    rows = json.loads(control.read_text())
    assert len(rows) == 20 and len({(r['body'], r['capture']) for r in rows}) == 10
    assert all(r['exact_matches'] == 1 and r['callback_equal'] for r in rows)
    paths.add(control)
    freeze = ROOT / '.local-work/resource-construction-mask-selection/prediction-freeze.json'
    prediction = freeze.with_name('conditional-results.json')
    assert pin(prediction) == json.loads(freeze.read_text())['results_sha256']
    paths.update((freeze, prediction))
    for name in ('research/resource-population-lifecycle/audit.py',
                 'research/resource-population-lifecycle/package.py',
                 'research/workshop-population/ReadSpecialist.java',
                 'research/workshop-population/export.ps1',
                 'research/resource-combined-acquisition/controller.cpp',
                 'research/resource-tungsten-acquisition/protection.py',
                 'runtime/session-tools/export_review.py'):
        paths.add(ROOT / name)
    out = io.StringIO(newline='')
    w = csv.writer(out, lineterminator='\n')
    w.writerow(('path', 'sha256', 'role'))
    for p in sorted(paths):
        w.writerow((p.relative_to(ROOT).as_posix() if p.is_relative_to(ROOT) else p.as_posix(), pin(p),
                    'LOCAL-ONLY primary/export/receipt' if '.local-work' in p.parts
                    else ('Installed tool identity; separately installed; no incorporation'
                          if not p.is_relative_to(ROOT)
                          else 'Existing project method or source ledger; baseline HEAD')))
    DOC.mkdir(parents=True, exist_ok=True)
    with (DOC / 'sources.csv').open('x', encoding='utf8', newline='') as f:
        f.write(out.getvalue())
    write(OUT / 'assessment.json', dict(inherited_pins_verified=inherited, streams=streams,
        source_pins=len(paths), exports_complete=5, ten_controls_integrity_checked=True,
        geometry_rerun=False, frozen_alternatives_unchanged=True,
        limit='Primary receipt qualification inherited; journal metadata independently recounted'))
    print('PASS', inherited, 'inherited pins;', len(streams), 'journals;', len(paths), 'source pins')


if __name__ == '__main__':
    main()
