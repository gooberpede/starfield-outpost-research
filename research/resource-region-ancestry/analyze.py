# SPDX-License-Identifier: GPL-3.0-or-later
"""Offline closed-receipt ancestry/replay audit. Never operates a target.

Reads named C1E receipt folder, unchanged owned evaluator and immutable RG2
freeze. Writes a fresh local derivative. Raw data stays ignored; no prediction
mutation, native invocation, databases, network or external dependencies.
"""
import argparse
import json
from pathlib import Path
import struct
import sys
from qualify import independent, pin, write, LOCAL, ROOT
sys.path.insert(0, str(ROOT/'save-analysis/scripts'))
from resource_spatial import evaluate_region


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--receipts',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    a=ap.parse_args()
    assert a.receipts.resolve().is_relative_to(LOCAL) and a.output.resolve().is_relative_to(LOCAL)
    event_file=a.receipts/'events.json'
    if event_file.exists():
        events=json.loads(event_file.read_text())
    else:
        event_file=a.receipts/'events.jsonl'
        events=[json.loads(line) for line in event_file.read_text().splitlines()]
    samples=[r for r in events if r['kind']=='SAMPLE']
    assert len(samples)==len(list(a.receipts.glob('capture-*.bin')))
    for row in samples:
        assert independent(a.receipts/f'capture-{row["capture"]:05d}.bin')[1]==row
    transfers=[r for r in samples if 'refresh_payload' in r and r.get('ancestry')=='BOUND_TRANSFER']
    joins=[]
    for d in samples:
        if not d.get('decision'):
            continue
        matching=[t for t in transfers if (t['pid'],t['tid'],t['thread_lifetime'],t['updater_token'])==
            (d['pid'],d['tid'],d['thread_lifetime'],d['updater_token']) and t['capture']>d['capture']
            and t['updater_bp']==d['updater_bp'] and t['temporary_set']==d['temporary_set']]
        joined=(d['ancestry']=='BOUND_CALLBACK' and d['selected']['status']=='COMPLETE'
                and d['geometry']['status']=='COMPLETE' and d['required_reads_complete']
                and d['qb_retained_read'] and d['closure_read'] and d['descriptor_read']
                and d['file_provenance']['main_file_identity'] and len(matching)==1
                and matching[0]['refresh_payload']['status']=='COMPLETE'
                and d['decision']=='ACCEPT' and any(m['pointer']==d['resource_pointer'] for m in matching[0]['refresh_payload']['members']))
        replay=dict(status='UNKNOWN',reason='MISSING_PER_USE_OR_GEOMETRY')
        if d['geometry']['status']=='COMPLETE' and d['qb_retained_read'] and d['closure_read']:
            raw=bytes.fromhex(d['geometry']['raw_region']);n=struct.unpack_from('<I',raw,24)[0]
            if n<=1:
                q=struct.unpack('<3f',bytes.fromhex(d['qb_retained_bits']))
                radius,upper=struct.unpack_from('<2f',bytes.fromhex(d['raw_closure']),16)
                pts=list(struct.iter_unpack('<4f',bytes.fromhex(d['geometry']['ordered_xyzw'])))
                replay=evaluate_region(q,radius,upper,struct.unpack_from('<3f',raw),struct.unpack_from('<f',raw,12)[0],pts)
                replay['admission']='CONDITIONAL_RETAINED_QB_AND_CLOSURE_STABILITY_NOT_PER_LOAD_WITNESS'
        joins.append(dict(capture=d['capture'],accepted_region_to_transfer=joined,conditional_replay=replay,
                          native_decision=d['decision'],generation_context='UNKNOWN',population_epoch='UNKNOWN'))
    freeze=ROOT/'docs/experiments/resource-geometry-mature-context/freeze-mature-v2.json'
    frozen=json.loads(freeze.read_text())
    for row in frozen['artifacts']+frozen['complete_geometry']:
        assert pin(row['path'])==row['sha256']
    write(a.output,dict(joins=joins,freeze_sha256=pin(freeze),frozen_geometry_unchanged=True,
        event_sha256=pin(event_file),synthetic=any(r.get('synthetic') is True for r in events),
        full_consumer_replay='NOT_QUALIFIED',region_census='NOT_CLAIMED',generator_replay='NOT_QUALIFIED'))
    print(a.output,len(joins),'decisions',sum(j['accepted_region_to_transfer'] for j in joins),'accepted joins')


if __name__=='__main__':
    main()
