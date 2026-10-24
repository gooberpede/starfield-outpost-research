# SPDX-License-Identifier: GPL-3.0-or-later
"""Offline current-source discriminator; writes an exclusive local report.

Reads verified SRO1 captures, frozen D3 output and installed-data corpus. Uses
owned C2B frame derivation and D3 source lookup, with no fitted transformation,
generation, target execution, save/config writes or historical epoch claim.
"""
import argparse
import json
from pathlib import Path
import struct
import sys
from qualify import independent, pin, write, ROOT, LOCAL
from admission import Tracker

sys.path.insert(0, str(ROOT/'.local-work/resource-save52-d3/build-v6/code'))
from predictor import resolve

FROZEN = ROOT/'.local-work/resource-save52-d3/revision06/first-pass-v1/D2-81a75b-stdout.json'
CORPUS = ROOT/'.local-work/resource-save52-d3/build-v6/normalized.json'


def discriminate(row, frozen, corpus):
    """Current metadata correspondence only; the native source pointer is local."""
    c = row['source_context']
    m = bytes.fromhex(c['raw_manager'])
    s = bytes.fromhex(c['raw_source'])
    offset = 0x1c0 if m[0x20] == 3 else 0xc8
    chart = m[offset]
    coarse = struct.unpack_from('<2i', m, offset+4)
    sub = struct.unpack_from('<2i', m, offset+0x14)
    fine = struct.unpack_from('<2i', m, offset+0x24)
    words = struct.unpack_from('<8i', s, 0x10)
    frame = [coarse[i]*192+sub[i]*12+fine[i] for i in (0, 1)]
    anchor = [frame[i]+words[i] for i in (0, 1)]
    result = dict(capture=row['capture'], source_key=row['source_key'],
                  source_wrapper=row['selected']['source_wrapper'], owner=c['owner_key_u32'],
                  current_frame=frame, current_chart=chart, source_anchor=list(words[:2]),
                  derived_geographic_anchor=anchor, generation_epoch='UNKNOWN',
                  historical_biom='UNKNOWN', source_representation='UNSUPPORTED',
                  geometry='UNSUPPORTED', earliest_mismatch='UNKNOWN')
    if (chart not in (0, 1) or any(v < 0 or v >= 16 for v in sub) or
            any(v < 0 or v >= 12 for v in fine) or
            any(v < 0 or v >= 256 for v in coarse) or
            c['owner_key_u32'] != 0x5de4c):
        result['reason'] = 'UNSUPPORTED_CURRENT_FRAME_OR_OWNER'
        return result
    try:
        body = corpus['payload']['bodies']['0005de4c']
        ax, ay, source_id, dx, dy, biome = resolve(corpus['payload'], body, chart, *anchor)
        family = body['biomes'][biome]
    except (KeyError, ValueError) as e:
        result['reason'] = 'INSTALLED_MODEL_COVERAGE:'+str(e)
        return result
    source = f'{chart}:{ax}:{ay}:{source_id}'
    resources = [r['id'] for r in family['resources']]
    lo,hi=frozen['halo']
    enumerated={resolve(corpus['payload'],body,frozen['request']['chart'],x,y)[:3] for x in range(lo[0],hi[0]+1) for y in range(lo[1],hi[1]+1)}
    assert len(enumerated)==frozen['source_count']
    represented=(ax,ay,source_id) in enumerated
    candidates = [g for g in frozen['regions'] if g['source'] == source]
    resource = f"{int.from_bytes(bytes.fromhex(row['selected']['raw_resource'])[40:44], 'little'):08x}"
    result.update(model_source=source, model_biom=biome, model_resources=resources,
                  model_source_exact_anchor=[ax, ay] == anchor,
                  source_representation='REPRESENTED' if represented else 'ABSENT_FROM_FROZEN_INPUT_SOURCES',
                  consumed_resource_represented=resource in resources)
    same_frame = chart == frozen['request']['chart'] and frame == frozen['request']['descriptor']
    if not same_frame:
        result['earliest_mismatch'] = 'CURRENT_DESCRIPTOR_FRAME'
    elif [ax, ay] != anchor:
        result['earliest_mismatch'] = 'CURRENT_SOURCE_ANCHOR_VS_MODEL_RESOLUTION'
    elif not represented:
        result['earliest_mismatch'] = 'SOURCE_NOT_REPRESENTED_IN_FROZEN_INPUT_SOURCES'
    elif resource not in resources:
        result['earliest_mismatch'] = 'CONSUMED_RESOURCE_VS_MODELED_FAMILY'
    else:
        result['earliest_mismatch'] = 'NO_EARLIER_CURRENT_METADATA_MISMATCH'
    matching = [g for g in candidates if g['resource'] == resource]
    if same_frame and [ax, ay] == anchor and matching:
        bound = row['geometry']['raw_region'][:32]
        points = row['geometry']['ordered_xyzw']
        result['geometry'] = 'MATCH' if any(g['native_bound_le'] == bound and g['ordered_xyzw_le'] == points for g in matching) else 'DIFFER'
    result['geometry_scope'] = 'EXACT_BYTES_IN_SAME_DESCRIPTOR_FRAME_NO_TRANSLATION'
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--captures', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    a = ap.parse_args()
    assert a.output.resolve().is_relative_to(LOCAL)
    frozen = json.loads(FROZEN.read_text(encoding='utf8'))
    corpus = json.loads(CORPUS.read_text(encoding='utf8'))
    assert corpus['sha256'] == frozen['corpus_sha256']
    tracker = Tracker()
    rows = []
    candidates = {}
    joined = []
    pending = {}
    session_identity = None
    events_path=a.captures/'events.json'
    events=json.loads(events_path.read_text(encoding='utf8')) if events_path.exists() else [json.loads(line) for line in (a.captures/'events.jsonl').read_text(encoding='utf8').splitlines()]
    for event in events:
        if event['kind']=='SESSION':
            assert session_identity is None
            session_identity=event
        if event['kind']=='ACK_ACCEPTED':
            accepted=pending.pop(event['capture'],None)
            if accepted is not None and event['accepted']:joined.append(discriminate(accepted,frozen,corpus))
        if event['kind']!='SAMPLE':
            tracker.feed(event)
            continue
        p=a.captures/f'capture-{event["capture"]:05d}.bin'
        session,row,end=independent(p)
        assert row==event and session==session_identity
        rows.append(dict(path=str(p),sha256=pin(p)))
        if tracker.feed(row):
            pending[row["capture"]]=tracker.last_match
    write(a.output, dict(schema='sor-d4a-comparison/1', inputs={str(p):pin(p) for p in (FROZEN,CORPUS)},
                         captures=rows, joined=joined, no_fitting=True,
                         synthetic=all(independent(Path(r['path']))[1].get('synthetic') for r in rows),
                         historical_cause='UNKNOWN', absence='NOT_INFERRED'))


if __name__ == '__main__':
    main()
