# SPDX-License-Identifier: GPL-3.0-or-later
"""Read-only final pilot audit, byte-read comparison and local allocation inventory.

Reads exact non-save sources, current archive and metadata. Writes a fresh local
receipt set. Measures requested bytes and reported NTFS allocation, not device I/O
or guaranteed physical reclamation. Skips and records synthetic reparse nodes.
"""
import argparse
import csv
import ctypes as c
import datetime
import hashlib
import json
import msvcrt
import os
from pathlib import Path
import subprocess
import sqlite3
import sys
import time

import engine as e


def main(label, anchor):
    before_free = e.space(32*1024*1024)
    out = e.LOCAL/label
    if out.exists() or not label.isalnum():
        raise e.Error('Fresh alphanumeric audit label required')
    rows = json.loads((e.LOCAL/'membership02.json').read_text())
    start = time.perf_counter()
    e.inspect(e.ROOT,rows)
    source_seconds = time.perf_counter()-start
    start = time.perf_counter()
    with e.verified(e.ARCHIVES/'index.json',anchor):
        pass
    archive_seconds = time.perf_counter()-start
    plan = e.LOCAL/'deletion-manifest02.json'
    dry = e.retire(e.ROOT,e.ARCHIVES/'index.json',anchor,plan,e.pin(plan))
    baseline = json.loads((e.LOCAL/'baseline.json').read_text())
    assert subprocess.check_output(['git','rev-parse','HEAD']).decode().strip()==baseline['head']
    assert e.pin(e.ROOT/'.git/index')==baseline['index_sha256']
    out.mkdir()
    inputs = [e.ROOT/'AGENTS.md',e.ROOT/'README.md',e.ROOT/'WORKFLOW.md',e.ROOT/'THIRD_PARTY_POLICY.md',
              e.ROOT/'research/evidence-archive-discovery/archive.py',e.ROOT/'research/review_package.py',
              e.ROOT/'research/editorial/screen.py']
    inputs += [e.ROOT/'docs'/name for name in ('CHARTER.md','EVIDENCE_STANDARD.md','RESEARCH_EXECUTION_PROTOCOL.md',
                                             'EDITORIAL_STANDARD.md','SAVE_PROTECTION.md','reviewers/research-completion-reviewer.md',
                                             'implementation-briefs/CODEX_BRIEF_SOR_consolidated_evidence_archival_stage_b_pilot.md')]
    inputs += list((e.ROOT/'research/evidence-archive-stage-b').glob('*.py'))
    inputs += [e.LOCAL/name for name in ('freeze02.json','membership02.json','measurements02.json','build02.json',
                                        'restore02.json','source-postflight02.json','consumers02.json','version-holds02.json',
                                        'deletion-manifest02.json','retain-loose02.json','initial-real-attempt-failure.json')]
    e.record(out/'sources.json',[dict(path=str(p),sha256=e.pin(p),bytes=p.stat().st_size) for p in inputs])
    stage_a = e.ROOT/'.local-work/evidence-archive-discovery'
    connection = sqlite3.connect('file:'+(stage_a/'candidate-owners-scoped02.sqlite').as_posix()+'?mode=ro',uri=True)
    workshop = connection.execute('select path,bytes,scope_state from candidate where path like ?',
                                   ('.local-work/workshop-inventory/%',)).fetchall()
    connection.close()
    discrepancies = []
    for name, size, scope in workshop:
        p = e.canonical(e.ROOT/name,e.ROOT/'.local-work/workshop-inventory')
        if not p.is_file() or p.stat().st_size != size:
            discrepancies.append(name)
    roster = list(csv.DictReader((e.ROOT/'docs/experiments/evidence-archive-discovery/archive-options.csv').open(encoding='utf8')))
    roster = [r for r in roster if r['scheme']=='A-nine-system' and not r['candidate_archive'].startswith(('HELD','LOOSE'))]
    e.record(out/'grouping.json',dict(nine_systems=roster,workshop_files=len(workshop),
             workshop_logical_bytes=sum(r[1] for r in workshop),metadata_discrepancies=discrepancies,
             workshop_recommendation='Consider one separate workshop identity/population archive: ten system owners total; retain explicit lifecycle cross-references. No boundary or data migrated.',
             hard_ceiling=30,classification='Metadata-only bounded assessment; payload authenticity not revalidated'))
    allocation = []
    skipped = []
    identities = set()
    folders = 0
    for root in (e.LOCAL,e.ARCHIVES):
        stack = [root]
        while stack:
            folder = stack.pop()
            folders += 1
            for entry in os.scandir(folder):
                p = Path(entry.path)
                info = p.lstat()
                if info.st_file_attributes & 0x400:
                    skipped.append(dict(path=str(p),reason='Synthetic reparse fixture; never traversed'))
                    continue
                if stat_is_directory(info.st_mode):
                    stack.append(p)
                    continue
                identity = (info.st_dev,info.st_ino)
                duplicate = identity in identities
                identities.add(identity)
                # Allocation-only query: synthetic hardlinks are recorded once.
                with p.open('rb') as stream:
                    standard = e.Standard()
                    if not e.K.GetFileInformationByHandleEx(msvcrt.get_osfhandle(stream.fileno()),1,c.byref(standard),c.sizeof(standard)):
                        raise c.WinError(c.get_last_error())
                allocation.append(dict(path=str(p),bytes=info.st_size,allocated_bytes=standard.allocation,
                                       duplicate_file_object=duplicate))
    e.record(out/'exclusions.json',dict(local_files=allocation,reparse_nodes=skipped,
             other_exclusions='Preexisting local evidence, proprietary inputs, saves/backups, game installation and native analysis projects remain excluded; no saved payload was read',
             publication_clearance=False))
    size = (e.ARCHIVES/'index.json').stat().st_size
    archive = e.ARCHIVES/'cargo-transport-fuel-b02/cargo-transport-fuel.tar.zst'
    e.record(out/'audit.json',dict(time_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
             source=dict(files=len(rows),payload_hash_invocations=len(rows),enumerations=0,
                         payload_bytes_read_hashed=sum(r['bytes'] for r in rows),seconds=source_seconds),
             archive=dict(index_hash_invocations=1,archive_hash_invocations=1,
                          control_bytes_read_hashed=size,encoded_archive_bytes_read=archive.stat().st_size*2,
                          decoded_member_bytes_read_hashed=sum(r['bytes'] for r in rows)+len(e.encode(rows)),
                          member_hash_invocations=len(rows)+1,enumerations=0,seconds=archive_seconds,
                          note='Index is opened for lock then read by authenticated loader; archive is hashed then decoded. Bytes are API-level requests; cache/device I/O unmeasured.'),
             dry_run=dry,original_recovery_bytes=0,
             retained_task_file_allocations=sum(r['allocated_bytes'] for r in allocation if not r['duplicate_file_object']),
             retained_task_logical_bytes=sum(r['bytes'] for r in allocation if not r['duplicate_file_object']),
             retained_file_count=len(allocation),directories=folders,
             temporary_peak_file_allocation_bound=sum(r['allocated_bytes'] for r in allocation if not r['duplicate_file_object'])+8*1024*1024,
             peak_limit='Retained artifacts plus 8 MiB for transient controls; directory/MFT metadata and concurrent OS changes are not measured. No exact physical peak claim.',
             before_free=before_free,after_free=e.space(),
             head=baseline['head'],index_sha256=baseline['index_sha256'],engine_sha256=e.pin(Path(e.__file__))))
    print(str(out/'audit.json'))


def stat_is_directory(mode):
    import stat
    return stat.S_ISDIR(mode)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--label',required=True)
    parser.add_argument('--index-sha256',required=True)
    args=parser.parse_args()
    main(args.label,args.index_sha256)
