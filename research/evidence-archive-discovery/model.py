# SPDX-License-Identifier: GPL-3.0-or-later
"""Non-save planning scenarios and a synthetic full-cardinality index rehearsal.

Reads metadata and authenticated benchmark/qualification receipts, never save
payloads. Scenario envelopes are not statistical confidence intervals. Writes
proposed tables and one explicitly synthetic index; performs no real migration.
"""
from collections import defaultdict
import csv
import argparse
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import tarfile
import time

import archive as a
from inventory import ROOT,LOCAL,DOC,csvout,write


def main():
    a.space(1024*1024*1024)
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--label',required=True);args=ap.parse_args()
    if not args.label.isalnum():raise ValueError('Fresh alphanumeric label')
    label=args.label
    scope=json.loads((LOCAL/'scope-summary02.json').read_text())
    db=sqlite3.connect(f'file:{(LOCAL/"candidate-owners-scoped02.sqlite").as_posix()}?mode=ro',uri=True)
    data=db.execute("select path,area,scheme_a,scheme_b,bytes,allocation_estimate from candidate where scope_state='ELIGIBLE-NON-SAVE-PROPOSAL' order by path").fetchall()
    inputs=json.loads((LOCAL/'benchmark01/results.json').read_text())
    results=[r for r in inputs['results'] if r['sample']!='protected-save-copy']
    measurements={r['sample']:r for r in results if r['format']=='tar.zst'}
    ratios=dict(low_text=measurements['large-definition-derivative']['pack']['compression_ratio'],
        high_text=measurements['native-export-receipt']['pack']['compression_ratio'],
        low_binary=measurements['live-native-binary']['pack']['compression_ratio'],high_binary=1.0,other=1.0)
    text={'.json','.jsonl','.csv','.tsv','.md','.log','.txt','.diff','.py','.ps1','.cpp','.h','.asm','.java','.xml','.cmd','.c'}
    binary={'.bin','.raw','.dat','.dmp'}
    buckets=defaultdict(lambda:dict(files=0,bytes=0,tar_header_padding_bytes=0))
    per_owner=defaultdict(lambda:dict(files=0,bytes=0,low=0.,high=0.,overhead=0))
    for path,area,owner,owner_b,size,allocated in data:
        ext=Path(path).suffix.lower();kind='text' if ext in text else 'binary' if ext in binary else 'other'
        info=tarfile.TarInfo(path);info.size=size;info.mtime=0
        overhead=len(info.tobuf(format=tarfile.PAX_FORMAT))+(-size)%512
        row=buckets[kind];row['files']+=1;row['bytes']+=size;row['tar_header_padding_bytes']+=overhead
        low=ratios['low_text'] if kind=='text' else ratios['low_binary'] if kind=='binary' else 1.0
        high=ratios['high_text'] if kind=='text' else 1.0
        item=per_owner[owner];item['files']+=1;item['bytes']+=size;item['low']+=size*low;item['high']+=size*high;item['overhead']+=overhead
    # Synthetic index: real path shapes/cardinality, zero-byte stand-in payloads,
    # no actual source hashes or bytes. It cannot be used as a migration manifest.
    scale=LOCAL/('synthetic-scale'+label);scale.mkdir(exist_ok=False);index=scale/'master.sqlite';a.init_index(index)
    start=time.perf_counter();connection=sqlite3.connect(index);empty=hashlib.sha256(b'').hexdigest()
    with connection:
        for owner in sorted(per_owner):
            connection.execute('insert into archives values(?,?,?,?,?,?)',(owner,str(scale/('NO_REAL_ARCHIVE_'+owner)), 'tar.zst',empty,0,'SYNTHETIC_SCALE_ONLY'))
        connection.executemany('insert into members values(?,?,?,?,?,?)',[(owner,path,empty,0,path,area) for path,area,owner,owner_b,size,allocated in data])
        connection.executemany('insert into aliases values(?,?,?,?,?)',[(owner,path,path,empty,0) for path,area,owner,owner_b,size,allocated in data])
    connection.close();anchor=a.pin(index);loaded=0
    for owner in sorted(per_owner):
        row,members,control_bytes=a.load(index,anchor,owner);loaded+=len(members)
    if loaded!=len(data):raise RuntimeError('Synthetic scale membership mismatch')
    index_bytes=index.stat().st_size
    write(scale/'result.json',dict(synthetic_only=True,paths=loaded,archive_roots=len(per_owner),
        actual_index_bytes=index_bytes,index_sha256=anchor,load_all_roots_seconds=time.perf_counter()-start,
        repeated_index_hash_bytes=index_bytes*len(per_owner),prototype_index_cap_bytes=256*1024*1024,
        no_real_payload_or_production_manifest=True))
    low=sum(r['low'] for r in per_owner.values())+index_bytes
    high=sum(r['high'] for r in per_owner.values())+sum(r['overhead'] for r in per_owner.values())+9*10240+index_bytes
    stored=sum(r['bytes']+r['tar_header_padding_bytes'] for r in buckets.values())+9*10240+index_bytes
    total=sum(r['pack']['input_bytes'] for r in measurements.values())
    tar_bytes=sum(r['pack']['archive_bytes'] for r in measurements.values())
    # Every hold stays loose. Two local archive replicas are an optional planning
    # case, not off-device or verified physical-device independence.
    held_files=scope['whole_estate_files']-scope['eligible_files']
    held_bytes=scope['whole_estate_bytes']-scope['eligible_bytes']
    residual_one=held_files+len(per_owner)+1
    residual_two=held_files+2*len(per_owner)+2
    baseline_allocation=scope['eligible_allocation_estimate']
    estimates=dict(current_scope='Non-save eligible proposal only; all saved/opaque/unknown holds stay loose',
        complete_logical_bytes=scope['eligible_bytes'],essential_logical_bytes=scope['essential_bytes'],
        target_bytes=10_000_000_000,required_complete_ratio=10_000_000_000/scope['eligible_bytes'],
        required_essential_ratio=10_000_000_000/scope['essential_bytes'],
        measured_non_save_sample_bytes=total,measured_non_save_tar_bytes=tar_bytes,sample_coverage_fraction=total/scope['eligible_bytes'],
        scenario_low_archive_plus_index_bytes=low,scenario_cautious_archive_plus_index_bytes=high,
        uncompressed_stored_tar_plus_index_bound=stored,
        evidence='Purposive transfer scenarios; text ratios observed, binary upper1.0 and unmeasured types stored. Not a statistical interval or fit proof.',
        complete_vs_essential_delta_bytes=scope['reproducible_candidate_bytes'],
        essential_scenario='Same two complete scenario budgets; not universal bounds. Omitting proven stand-ins cannot increase storage, but no speculative extra compressed saving is assigned',
        residual_frozen_namespace_files_one_replica=residual_one,residual_frozen_namespace_files_two_replicas=residual_two,
        frozen_namespace_held_files=held_files,frozen_namespace_held_bytes=held_bytes,
        net_eligible_allocation_recovery_one_replica_scenario_low=baseline_allocation-low,
        net_eligible_allocation_recovery_one_replica_scenario_cautious=baseline_allocation-high,
        net_eligible_allocation_recovery_two_replicas_scenario_low=baseline_allocation-2*low,
        net_eligible_allocation_recovery_two_replicas_scenario_cautious=baseline_allocation-2*high,
        caveats='All figures conditional on approved cutover and consumer compatibility; subtract post-freeze Stage A temporary growth from anchored free-space projections; no space recovered now; no off-device backup confirmed',
        future_verification='Current prototype rehashes master index per call; account for roots*index_bytes. A reviewed single-authenticated-session reader is a future optimization, not an achieved 80% migration result.')
    write(LOCAL/f'planning-model{label}.json',estimates)
    csvout('planning-scenarios.csv',['stratum','files','logical_bytes','tar_header_padding_bytes','ratio_low_scenario','ratio_cautious_scenario'],[
        dict(stratum=kind,files=row['files'],logical_bytes=row['bytes'],tar_header_padding_bytes=row['tar_header_padding_bytes'],ratio_low_scenario=ratios['low_text'] if kind=='text' else ratios['low_binary'] if kind=='binary' else 1.0,
             ratio_cautious_scenario=ratios['high_text'] if kind=='text' else 1.0) for kind,row in sorted(buckets.items())])
    # Refine the pre-amendment non-save cargo candidate without payload reads.
    pilot=json.loads((LOCAL/'cargo-pilot-candidates.json').read_text());eligible={r[0] for r in data}
    prior=json.loads((LOCAL/'expected-sample-pin-candidates03.json').read_text());checked=set();matched=0;selected=[];version_holds=[]
    for item in pilot:
        if item['path'] not in eligible:continue
        references=prior.get(os.path.normcase(os.path.normpath(str(ROOT/item['path']))),[])
        expected=set()
        for ref in references:
            if ref['ledger'] not in checked:
                if a.pin(ROOT/ref['ledger'])!=ref['ledger_sha256']:raise RuntimeError('Pilot source ledger changed')
                checked.add(ref['ledger'])
            expected.add(ref['sha256'])
        matches=item['sha256'] in expected
        conflict=len(expected)>1 or (bool(expected) and not matches)
        if conflict:
            version_holds.append(dict(path=item['path'],current_sha256=item['sha256'],historical_expectations=references,
                current_B5_creator_match=any(r['ledger']=='docs/audits/publication-readiness-b5/creator-inventory.csv' and r['sha256']==item['sha256'] for r in references),
                disposition='HOLD loose / recover historical method-version provenance before any deletion; never overwrite a historical pin'))
        item=dict(item,prior_source_ledger_match=matches,historical_version_hold=conflict,future_delete_authority=False)
        matched+=matches;selected.append(item)
    write(LOCAL/f'cargo-pilot-scoped{label}.json',selected)
    write(LOCAL/f'cargo-pilot-summary{label}.json',dict(files=len(selected),bytes=sum(r['bytes'] for r in selected),
        prior_source_ledger_matches=matched,current_hashes='Two prior Stage A passes; where old expectations absent, historical identity remains UNKNOWN',
        historical_method_version_holds=version_holds,
        proposal_only=True,no_source_move_or_delete=True))
    print(json.dumps(estimates,indent=2))


if __name__=='__main__':main()
