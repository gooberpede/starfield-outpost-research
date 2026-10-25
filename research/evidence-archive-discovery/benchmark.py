# SPDX-License-Identifier: GPL-3.0-or-later
"""Frozen actual-sample compression benchmarks on disposable authenticated copies.

Reads selected original files against pre-existing expected hashes; writes copies,
archives, restores and receipts only inside this Stage A workspace. No originals
are moved/deleted. Setup/copy/hash, format, validation and restore I/O are separate.
"""
import argparse
import csv
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import time

import archive as a
from inventory import ROOT,LOCAL,DOC,write


def main():
    a.space(1024*1024*1024)
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--label',required=True)
    ap.add_argument('--candidate-pin',required=True)
    args=ap.parse_args()
    if not args.label.isalnum():raise ValueError('Fresh alphanumeric label')
    out=LOCAL/args.label;out.mkdir(exist_ok=False)
    copy_root=out/'copies';copy_root.mkdir();(copy_root/a.MARKER).write_text('Synthetic/copy workspace only\n',encoding='utf8')
    candidate_path=LOCAL/'expected-sample-pin-candidates03.json'
    if a.pin(candidate_path)!=args.candidate_pin:raise a.ArchiveError('Derived expected-pin cache identity mismatch')
    candidates=json.loads(candidate_path.read_text())
    historical_path=ROOT/'.local-work/resource-predictability-contrast/audit-before.json'
    if a.pin(historical_path)!='a243c67c0e451aac21cbb5fcb671c9e94ad2b3806406d0fdec1b2626f153ab9b':raise a.ArchiveError('Historical expected-pin receipt mismatch')
    historical=json.loads(historical_path.read_text())['pins']
    normalized={os.path.normcase(os.path.normpath(p)):d for p,d in historical.items()}
    requested={
        'live-native-binary':['.local-work/position-write-history/live/session-40616-164222546/events.bin',
                              '.local-work/position-write-history/live/session-40616-164222546/records.jsonl'],
        'large-definition-derivative':['.local-work/r1-robots/definitions01.json'],
        'resource-journal':['.local-work/resource-combined-acquisition/retail-attempt01/events.jsonl'],
        'native-export-receipt':['.local-work/recon/workshop-origin-wide-inventory.tsv',
                                 '.local-work/resource-construction-demand/audit-before.json']}
    db=sqlite3.connect(f'file:{(LOCAL/"inventory03.sqlite").as_posix()}?mode=ro',uri=True)
    for group,top in (('resource-journal','resource-combined-acquisition'),('native-export-receipt','recon')):
        result=db.execute("select path from files where directory=? and extension='.log' and original_pin is not null and bytes>100 order by bytes desc limit 1",(top,)).fetchone()
        if result:requested[group].append(result[0])
    members={};expectations=[]
    for group,names in requested.items():
        members[group]={}
        for name in names:
            source=ROOT/name;key=os.path.normcase(os.path.normpath(str(source)))
            rows=candidates.get(key,[])
            for reference in rows:
                if a.pin(ROOT/reference['ledger'])!=reference['ledger_sha256']:
                    raise a.ArchiveError('Original source-ledger identity changed')
            digests={r['sha256'] for r in rows}
            if key in normalized:digests.add(normalized[key])
            if len(digests)!=1:raise a.ArchiveError('Missing/conflicting prior sample identity: '+name)
            digest=next(iter(digests));size=source.stat().st_size
            members[group][name]=dict(sha256=digest,bytes=size,original_location=name,system=group)
            expectations.append(dict(group=group,path=name,bytes=size,sha256=digest,
                basis=rows or 'D5G authenticated expected-pin inventory'))
    total=sum(r['bytes'] for group in members.values() for r in group.values())
    freeze=dict(workload='Whole-file purposive samples of major observed byte/type contributors; not random/statistically representative',
        formats=['tar.zst level 3','ZIP/Deflate level 6'],order='tar.zst then ZIP within each sample; warm-cache effects disclosed',
        samples=expectations,total_input_bytes=total,member_count=len(expectations),
        candidate_input_sha256=args.candidate_pin,historical_expected_sha256=a.pin(historical_path),
        metrics=['copy bytes/time','pack read/hash bytes','archive compressed bytes/SHA','initial member validation','full archive hash','full member validation','restore and restored byte reread','aggregate temporary disk high-water'],
        mutation_tests='Separate synthetic qualification; never alter actual source samples',
        method_hashes={p.name:a.pin(p) for p in Path(__file__).parent.glob('*.py')})
    write(out/'freeze.json',freeze)
    a.space(total*7+1024*1024*1024)
    setup_start=time.perf_counter();copied=0
    for group in members.values():
        for name,row in group.items():
            target=a.guard(copy_root/name);target.parent.mkdir(parents=True,exist_ok=True)
            h=hashlib.sha256();count=0
            with (ROOT/name).open('rb') as source,target.open('xb') as dest:
                while data:=source.read(a.CHUNK):
                    h.update(data);count+=len(data);dest.write(data)
            if count!=row['bytes'] or h.hexdigest()!=row['sha256']:
                raise a.ArchiveError('Actual source intake identity mismatch: '+name)
            copied+=count
            print('authenticated copy',name,count,flush=True)
    setup=dict(copy_seconds=time.perf_counter()-setup_start,original_bytes_read_hashed=copied,
               copied_bytes_written=copied,expected_hashes_checked=len(expectations))
    write(out/'setup.json',setup)
    index=out/'master-prototype.sqlite';a.init_index(index)
    results=[]
    for group,content in members.items():
        for fmt in ('tar.zst','zip'):
            start=time.perf_counter();archive_id=group+'-'+fmt.replace('.','-')
            packed=a.pack(copy_root,index,archive_id,fmt,content)
            verified=a.verify(index,packed['index_sha256'],archive_id)
            restored=a.restore(index,packed['index_sha256'],archive_id,out/('restore-'+archive_id))
            for name,row in content.items():
                if a.pin(out/('restore-'+archive_id)/name)!=a.pin(copy_root/name):
                    raise a.ArchiveError('Independent restored/copied byte-equality check')
            result=dict(sample=group,format=fmt,pack=packed,verify=verified,restore=restored,
                        independent_equality_payload_bytes_read=2*sum(r['bytes'] for r in content.values()),
                        total_phase_seconds=time.perf_counter()-start)
            results.append(result)
            write(out/(archive_id+'-result.json'),result)
            print('qualified',group,fmt,packed['compression_ratio'],flush=True)
    # Fresh source hashes at end, not a prior PASS standing in for present bytes.
    for row in expectations:
        if a.pin(ROOT/row['path'])!=row['sha256']:raise a.ArchiveError('Original sample changed')
    write(out/'results.json',dict(results=results,source_after_hashes=len(expectations),
        source_after_bytes_hashed=total,master_index_sha256=a.pin(index),
        temporary_logical_bytes=sum(p.stat().st_size for p in LOCAL.rglob('*') if p.is_file()),
        no_original_writes=True,no_original_deletions=True))
    fields=['sample','format','input_bytes','archive_bytes','ratio','creation_seconds','initial_member_validation_seconds',
            'archive_hash_seconds','full_member_verify_seconds','restore_seconds','total_phase_seconds']
    with (DOC/'benchmark-measurements.csv').open('x',encoding='utf8',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=fields,lineterminator='\n');writer.writeheader()
        for r in results:
            writer.writerow(dict(sample=r['sample'],format=r['format'],input_bytes=r['pack']['input_bytes'],archive_bytes=r['pack']['archive_bytes'],ratio=r['pack']['compression_ratio'],creation_seconds=r['pack']['creation_seconds'],initial_member_validation_seconds=r['pack']['initial_member_validation_seconds'],archive_hash_seconds=r['verify']['archive_hash_seconds'],full_member_verify_seconds=r['verify']['full_member_verify_seconds'],restore_seconds=r['restore']['wall_seconds'],total_phase_seconds=r['total_phase_seconds']))
    print('benchmark complete',len(results),'format/sample combinations',flush=True)


if __name__=='__main__':main()
