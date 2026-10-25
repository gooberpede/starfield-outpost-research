# SPDX-License-Identifier: GPL-3.0-or-later
"""Freeze and qualify the real cargo archive without modifying any source.

Reads the Stage A candidate/provenance ledgers and exact cargo members only.
Writes exclusive local inventory, archive, restore and measurement receipts.
No save payload, installation, game, database or original-file mutation.
"""
import argparse
import csv
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

import engine as e

A = e.ROOT / '.local-work/evidence-archive-discovery'
FOLDER = e.ARCHIVES / 'cargo-transport-fuel-b02'


def run():
    start = time.perf_counter()
    e.space(256*1024*1024)
    original = json.loads((A/'cargo-pilot-scoped04.json').read_text())
    holds = json.loads((A/'cargo-pilot-summary04.json').read_text())['historical_method_version_holds']
    provenance = json.loads((A/'expected-sample-pin-candidates03.json').read_text())
    seal_path = e.ROOT/'.local-work/c2-prose-spacing/final-seal.json'
    seal = json.loads(seal_path.read_text())
    supplemental = {Path(r['path']).relative_to(e.ROOT).as_posix():r['sha256'] for r in seal['receipts']}
    sources = []
    checked = set()
    for r in original:
        key = os.path.normcase(os.path.normpath(str(e.ROOT/r['path'])))
        refs = provenance.get(key, [])
        for ref in refs:
            if ref['ledger'] not in checked:
                if e.pin(e.ROOT/ref['ledger']) != ref['ledger_sha256']:
                    raise e.Error('Historical source ledger changed')
                checked.add(ref['ledger'])
        sources.append(dict(path=r['path'], bytes=r['bytes'], sha256=r['sha256'],
                            historical_expectations=refs, historical_identity='MATCH' if r['prior_source_ledger_match'] else 'UNKNOWN',
                            historical_identity_scope='Stage A external CSV ledger coverage only',
                            supplemental_seal_expectation=supplemental.get(r['path']),
                            owner='cargo-transport-fuel', historical_version_hold=r['historical_version_hold'],
                            active_consumer='RETAIN: fixed cargo-tool namespace' if not r['path'].startswith('.local-work/c2-prose-spacing/')
                            else 'Historical editorial package; controlled extraction, retired scripts not executed'))
    # This admission is an exact Stage A set, not a new recursive cargo discovery.
    frozen = e.inspect(e.ROOT, sources)
    if any(r['supplemental_seal_expectation'] and r['supplemental_seal_expectation'] != r['sha256'] for r in frozen):
        raise e.Error('Historical editorial final-seal receipt mismatch')
    e.record(e.LOCAL/'freeze02.json', frozen)
    e.record(e.LOCAL/'version-holds02.json', holds)
    rows = [r for r in frozen if not r['historical_version_hold']]
    e.record(e.LOCAL/'membership02.json', rows)
    # Fresh scan of authored references; execution is not inferred from a mention.
    names = subprocess.check_output(['git','ls-files','-z'], cwd=e.ROOT).decode().split('\0')[:-1]
    consumers = []
    for name in names:
        p = e.ROOT/name
        if p.suffix not in ('.py','.md','.csv','.ps1','.java','.cpp','.json'):
            continue
        try:
            raw = p.read_bytes()
            text = raw.decode('utf8')
        except (UnicodeDecodeError, OSError):
            continue
        for number, line in enumerate(text.splitlines(), 1):
            if any(d in line.replace('\\','/') for d in ('c1-cargo','c2-transit','c2-transport','c3-fuel','c2-prose-spacing')):
                consumers.append(dict(path=name, sha256=hashlib.sha256(raw).hexdigest(), line=number,
                                      text=line, treatment='Retain fixed cargo input namespaces; historical editorial files use verified extraction'))
    e.record(e.LOCAL/'consumers02.json', consumers)
    refs = [dict(consumer_system='governance-publication-review', owner='cargo-transport-fuel', path=r['path'])
            for r in rows if r['path'].startswith('.local-work/c2-prose-spacing/')]
    index_path = e.ARCHIVES/'index.json'
    result = e.build(e.ROOT, rows, FOLDER, index_path=index_path, cross_references=refs)
    e.record(e.LOCAL/'build02.json',result)
    anchor = result['index_sha256']
    restore = e.restore(index_path, anchor, e.LOCAL/'real-restoration02')
    e.record(e.LOCAL/'restore02.json',restore)
    e.checkpoint(FOLDER, 'RESTORED-TESTED', index_sha256=anchor, restoration=restore)
    # Preserve active cargo namespaces wholesale: dynamic paths need no guesswork.
    # Only the completed editorial package is proposed for controlled extraction.
    allow = [r for r in rows if r['path'].startswith('.local-work/c2-prose-spacing/')]
    retained = [dict(r, reason='Historical packager version hold' if r['historical_version_hold']
                     else 'Fixed/dynamic cargo consumers remain loose; no script retargeting or execution')
                for r in frozen if r not in allow]
    plan = dict(schema=1, index_sha256=anchor, rows=allow,
                authority='PROPOSAL ONLY: separate exact-hash human approval required')
    e.record(e.LOCAL/'deletion-manifest02.json', plan)
    e.record(e.LOCAL/'retain-loose02.json', dict(rows=retained,
             universal_exclusions=['All saves, backups, raw save streams, installed material, native analysis projects and unresolved live data'],
             scope='All paths outside this exact manifest are retained, without enumeration or save payload access'))
    dry = e.retire(e.ROOT, index_path, anchor, e.LOCAL/'deletion-manifest02.json',
                   e.pin(e.LOCAL/'deletion-manifest02.json'))
    # Reconcile every frozen original after packaging and full restoration.
    after = e.inspect(e.ROOT, frozen)
    if after != frozen:
        raise e.Error('Postflight source/metadata mismatch')
    e.record(e.LOCAL/'source-postflight02.json', dict(files=len(after), all_equal=True,
             membership_sha256=e.pin(e.LOCAL/'membership02.json'), freeze_sha256=e.pin(e.LOCAL/'freeze02.json')))
    e.checkpoint(FOLDER, 'AWAITING-APPROVAL', index_sha256=anchor,
                 deletion_manifest_sha256=e.pin(e.LOCAL/'deletion-manifest02.json'))
    # Logical and NTFS allocation accounting; directories and unrelated OS churn
    # are distinct from file allocation and cannot be inferred from free deltas.
    allocation = []
    measured_paths = list((e.LOCAL/'real-restoration02').rglob('*')) + list(FOLDER.rglob('*'))
    measured_paths += list(e.LOCAL.glob('*.json')) + [index_path]
    for p in measured_paths:
        if p.is_file():
            with e.locked(p) as (_, info):
                allocation.append(dict(path=str(p), bytes=info.length, allocated_bytes=info.allocation))
    restored_rows = [r for r in allocation if '/real-restoration02/' in r['path'].replace('\\','/')]
    result.update(restore=restore, pilot_candidate_files=len(frozen), candidate_bytes=sum(r['bytes'] for r in frozen),
                  historical_prior_matches=sum(r['historical_identity']=='MATCH' for r in frozen),
                  original_allocated_bytes=sum(r['allocated_bytes'] for r in frozen),
                  archived_source_allocated_bytes=sum(r['allocated_bytes'] for r in rows),
                  proposed_delete_files=len(allow), projected_gross_recoverable_allocated_bytes=dry['expected_allocated_bytes'],
                  deletion_manifest_sha256=e.pin(e.LOCAL/'deletion-manifest02.json'),
                  retain_loose_sha256=e.pin(e.LOCAL/'retain-loose02.json'),
                  actual_original_freed_bytes=0, dry_run=dry,
                  restored_allocated_bytes=sum(r['allocated_bytes'] for r in restored_rows),
                  measured_retained_file_allocation=sum(r['allocated_bytes'] for r in allocation),
                  peak_file_allocation_upper_bound=sum(r['allocated_bytes'] for r in allocation)+2*1024*1024,
                  peak_limit='Final real-run outputs and top-level receipts; extra 2 MiB covers small controls. Prior attempt, fixtures, directories and OS I/O accounted separately.',
                  elapsed_seconds=time.perf_counter()-start, final_free=e.space(),
                  method_sha256={p.name:e.pin(p) for p in Path(__file__).parent.glob('*.py')},
                  python=sys.version, python_sha256=e.pin(sys.executable),
                  stage_a_candidate_sha256=e.pin(A/'cargo-pilot-scoped04.json'),
                  historical_ledger_files_authenticated=len(checked),
                  supplemental_seal_sha256=e.pin(seal_path), supplemental_seal_matches=len(supplemental),
                  routine_verification_objective='80% reduction NOT TESTED; no migration/policy activation')
    e.record(e.LOCAL/'allocation02.json', allocation)
    e.record(e.LOCAL/'measurements02.json', result)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build', action='store_true', required=True)
    parser.parse_args()
    run()
