# SPDX-License-Identifier: GPL-3.0-or-later
"""Read-only independent accounting of one D5B capture; no target operations.

Reads original SRO1 frames, durable sidecars and the controller event journal.
Writes exclusive ignored analysis receipts. Reuses owned framing/reducer methods
under SOR-P-0002; Python stdlib only. Does not fit predictions, modify originals,
access live process memory, change saves/configuration, or mutate Git.
"""
import argparse
import collections
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import struct

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'research/resource-combined-acquisition'))
from reduce import Tracker


def pin(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream,'sha256').hexdigest()


def write(path,value):
    with path.open('x',encoding='utf8',newline='\n') as stream:
        json.dump(value,stream,indent=2,allow_nan=False)
        stream.write('\n')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--captures',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    capture=args.captures.resolve();out=args.output.resolve()
    local=ROOT/'.local-work/resource-combined-acquisition'
    assert capture.is_relative_to(local) and out.is_relative_to(local)
    out.mkdir(exist_ok=False)
    spec=importlib.util.spec_from_file_location('d5b_live_verifier',ROOT/'research/resource-tungsten-acquisition/qualify.py')
    verifier=importlib.util.module_from_spec(spec);spec.loader.exec_module(verifier)
    events=[];truncated=None
    data=(capture/'events.jsonl').read_bytes()
    for index,line in enumerate(data.splitlines()):
        try:
            events.append(json.loads(line))
        except (ValueError,UnicodeDecodeError):
            truncated=dict(line=index+1,bytes=len(line),sha256=hashlib.sha256(line).hexdigest())
            assert index==len(data.splitlines())-1,'corruption before final journal line'
    sessions=[r for r in events if r['kind']=='SESSION']
    assert len(sessions)==1,'single measured session required'
    samples={r['capture']:r for r in events if r['kind']=='SAMPLE'}
    assert len(samples)==sum(r['kind']=='SAMPLE' for r in events)
    receipts=[];missing=[];invalid=[]
    for number,row in sorted(samples.items()):
        path=capture/f'capture-{number:05d}.bin'
        if not path.exists():
            missing.append(number);continue
        try:
            decoded=verifier.independent(path)
            assert decoded[0]==sessions[0] and decoded[1]==row and row['pid']==sessions[0]['pid']
            receipts.append(dict(capture=number,sha256=pin(path),ack_sha256=pin(path.with_suffix('.ack.json')),
                                 complete=decoded[2]['complete'],site=row['site']))
        except (AssertionError,ValueError,OSError,struct.error) as failure:
            invalid.append(dict(capture=number,reason=str(failure)))
    actual={int(p.stem.removeprefix('capture-')) for p in capture.glob('capture-*.bin')}
    assert not actual-set(samples),'unlogged raw receipt'
    positive=[r['capture'] for r in events if r['kind']=='ACK_ACCEPTED' and r.get('accepted')]
    assert len(positive)==len(set(positive)),'duplicate numbered ACK'
    tracker=Tracker()
    for row in events:
        tracker.feed(row)
    reduction=tracker.result()
    if missing or invalid or truncated is not None:
        reduction=dict(schema='sor-d5b-live-invalid/1',status='INVALID',constructions=[],consumptions=[],synthetic_links=[],native_epoch=None,reason='Journal projection is not authoritative without every matching durable receipt.',unverified_journal_projection=reduction)
    write(out/'reduction.json',reduction)
    write(out/'receipts.json',receipts)
    stop=next((i for i,r in enumerate(events) if r['kind']=='STOP_COMMITTED'),None)
    forbidden=[r for r in events[stop+1:] if r['kind'] in ('SAMPLE','PHASE','THREAD_BEGIN','STARTUP_ARMED','RESUME_VERIFIED')] if stop is not None else []
    summary=dict(schema='sor-d5b-live-analysis/1',session=sessions[0],events=len(events),
        journal_sha256=pin(capture/'events.jsonl'),truncated_journal=truncated,
        samples=len(samples),verified_receipts=len(receipts),incomplete_receipts=sum(not r['complete'] for r in receipts),
        missing=missing,invalid=invalid,accepted_acks=len(positive),
        sample_ack_bijection=set(samples)==set(positive),
        sites=dict(collections.Counter(r['site'] for r in samples.values())),
        loss=[r for r in events if r['kind'] in ('LOSS','EXCEPTION')],
        phases=[r for r in events if r['kind']=='PHASE'],
        terminal=[r for r in events if r['kind'] in ('STOP_COMMITTED','EXIT','FAILURE_CLEANUP')],
        post_stop_forbidden=forbidden,scientific_result=reduction['status'],
        constructions=len(reduction['constructions']),consumptions=len(reduction['consumptions']),
        native_epoch=None,synthetic_links=reduction['synthetic_links'],
        framing_integrity=not missing and not invalid and truncated is None)
    write(out/'summary.json',summary)
    print(json.dumps({k:summary[k] for k in ('samples','verified_receipts','incomplete_receipts','accepted_acks','scientific_result','constructions','consumptions','framing_integrity')},indent=2))


if __name__=='__main__':
    main()
