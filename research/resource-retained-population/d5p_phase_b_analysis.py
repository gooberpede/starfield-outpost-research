# SPDX-License-Identifier: GPL-3.0-or-later
"""Bounded offline analysis of the two D5P Phase B startup/capture streams.

Reads original raw/flush/identity/terminal files, the frozen D5P reader and owned
D5L chart-0 decoder. Writes a fresh requested JSON derivative below task scratch.
No game, live reads, mutation of evidence, downloads, dependencies or Git changes.
Requires installed CPython stdlib and retained original receipts. A candidate
geographic label decoded from raw words is not a qualified source/lifetime join.
"""
import argparse
import collections
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'runtime/retained-population'))
from read_capture import SIZE,HEADER,decode,inspect


def sha(path):
    with Path(path).open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args();out=args.out.resolve()
    assert out.is_relative_to(ROOT/'.local-work/d5p-phase-b') and not out.exists()
    spec=importlib.util.spec_from_file_location('d5p_owned_native_decoder',Path(__file__).with_name('native_reduce.py'))
    native=importlib.util.module_from_spec(spec);spec.loader.exec_module(native)
    dll='935071691f6325f99d1f8ec99056349d6eb5fee19dba237cffd6e7d7833650cc'
    primary=ROOT/'.local-work/d5p/live/session-3424-98377281'
    secondary=ROOT/'.local-work/d5p/live/session-6460-98416593'
    verified=inspect(primary,dll);other=inspect(secondary,dll)
    raw=(primary/'events.bin').read_bytes();n=verified['independently_verified_durable_records']
    events=[decode(raw[i*(SIZE+HEADER.size)+HEADER.size:(i+1)*(SIZE+HEADER.size)]) for i in range(n)]
    histogram=collections.Counter((e['kind'],e['status']) for e in events)
    grouped=collections.defaultdict(list);selected=[]
    for e in events:
        if e['kind'] not in (1,2,3,4,5,6,11):continue
        key=native.geographic_key(bytes.fromhex(e['source_bytes']),bytes.fromhex(e['descriptor']))
        if not key:continue
        grouped[(e['owner'],key)].append(e)
        if e['owner']==0x5e0de and key=='0:37536:20928:0029d20e':selected.append(e)
    groups=[dict(owner_formid=f'0x{owner:08x}',geographic_key_candidate=key,
                 events=len(rows),status_values=sorted({e['status'] for e in rows}),
                 classification='RAW_CANDIDATE_ONLY_NOT_SOURCE_CONTEXT_QUALIFIED')
            for (owner,key),rows in sorted(grouped.items())]
    terminal=json.loads((primary/'terminal.json').read_text())
    visits=[e for e in events if e['kind']==1]
    qualified=[e for e in selected if e['status']==0 and not e['hazards']]
    result=dict(schema='sor-d5p-phase-b-analysis/1',primary=verified,secondary=other,
        terminal=terminal,kind_status=[dict(kind=k,status=s,count=c) for (k,s),c in sorted(histogram.items())],
        source_candidates=groups,selected_raw_candidate_events=len(selected),
        selected_context_qualified_events=len(qualified),qualified_selected_region_chains=0,
        visited_records=len(visits),visited_context_failure_records=sum(bool(e['status']&1) for e in visits),
        completed_snapshots=sum(e['kind']==6 for e in events),
        raw_lookup_comparisons=verified['hit_observations'],
        qualified_source_lookup_hits=sum(e['kind']==2 and e['status']==0 and not e['hazards'] and e['args'][2]!=e['args'][3] for e in events),
        final_record=dict(sequence=events[-1]['sequence'],kind=events[-1]['kind'],status=events[-1]['status']) if events else None,
        admission_failure='At least one reported emit failure; full-queue versus bounded-CAS-contention branch not recorded',
        context_failure='Read/context-invariant failure flag observed; individual first failed predicate/operands not recorded',
        scientific_result='INCOMPLETE_ACQUISITION_NOT_QUALIFIED_NONHIT_OR_HYPOTHESIS_FALSIFICATION',
        methods={str(p.relative_to(ROOT)):sha(p) for p in (Path(__file__).resolve(),ROOT/'runtime/retained-population/read_capture.py',Path(__file__).with_name('native_reduce.py'))},
        inputs={str(p):sha(p) for folder in (primary,secondary) for p in sorted(folder.iterdir()) if p.is_file()})
    assert n==1592 and terminal['enqueued']==terminal['written']==terminal['flushed']==n
    assert terminal['failed'] is True and terminal['drops']==1
    assert len(visits)==319 and result['visited_context_failure_records']==319
    assert not selected and not qualified and not verified['complete_chains']
    assert result['qualified_source_lookup_hits']==0 and other['raw_records']==1
    with out.open('x',encoding='utf8',newline='\n') as stream:json.dump(result,stream,indent=2);stream.write('\n')
    print(json.dumps({k:result[k] for k in ('selected_raw_candidate_events','selected_context_qualified_events','visited_records','visited_context_failure_records','completed_snapshots','raw_lookup_comparisons','qualified_source_lookup_hits','scientific_result')},indent=2))


if __name__=='__main__':main()
