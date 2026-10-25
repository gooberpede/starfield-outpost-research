# SPDX-License-Identifier: GPL-3.0-or-later
"""Expand one verified transfer into separately qualified resource chains.

Reads the completed live analysis, original journal, five selected SRO1 receipts
and unchanged D5A predictions. Writes an exclusive local derivative. Each member
is reduced separately with the owned selector so its first-match behavior cannot
hide other accepted members. No operand is edited and no epoch is inferred.
Python stdlib and project-owned modules only; no target or original-file writes.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
LOCAL = ROOT / '.local-work/resource-combined-acquisition'
sys.path.insert(0, str(ROOT / 'research/resource-combined-acquisition'))
from reduce import Tracker, SOURCE
from compare import compare, verifier, PREDICTIONS, FROZEN_SHA256


def pin(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--entry', type=int, required=True)
    parser.add_argument('--accepts', type=int, nargs='+', required=True)
    parser.add_argument('--transfer', type=int, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    assert args.output.resolve().is_relative_to(LOCAL)
    capture = LOCAL / 'retail-attempt01'
    analysis = LOCAL / 'pilot-analysis01/summary.json'
    summary = json.loads(analysis.read_text(encoding='utf8'))
    assert summary['framing_integrity'] and summary['sample_ack_bijection']
    assert not summary['incomplete_receipts'] and not summary['post_stop_forbidden']
    assert pin(capture / 'events.jsonl') == summary['journal_sha256']
    events = [json.loads(line) for line in (capture / 'events.jsonl').read_text(encoding='utf8').splitlines()]
    samples = {r['capture']:r for r in events if r['kind'] == 'SAMPLE'}
    acks = {r['capture']:r for r in events if r['kind'] == 'ACK_ACCEPTED' and r['accepted']}
    selected = [args.entry] + args.accepts + [args.transfer]
    positions = {r['capture']:i for i,r in enumerate(events) if r['kind'] == 'SAMPLE'}
    ack_positions = {r['capture']:i for i,r in enumerate(events)
        if r['kind'] == 'ACK_ACCEPTED' and r['accepted']}
    start, end = positions[args.entry], positions[args.transfer]
    assert start < end and len(set(args.accepts)) == len(args.accepts)
    assert samples[args.entry]['site'] == 'updater_entry'
    assert samples[args.transfer]['site'] == 'spatial_transfer_payload'
    assert all(samples[n]['site'] == 'region_accept' and samples[n]['decision'] == 'ACCEPT'
        for n in args.accepts)
    assert all(positions[n] < ack_positions[n] for n in selected)
    assert all(start < positions[n] < end for n in args.accepts)
    # Projection is safe only inside one uninterrupted observed evaluation.
    # Do not omit a state invalidation or a competing updater entry.
    assert not any(r['kind'] in ('PHASE', 'LOSS', 'EXCEPTION', 'THREAD_END')
        or (r['kind'] == 'SAMPLE' and r['site'] == 'updater_entry')
        for r in events[start+1:end])
    pins = {}
    for number in selected:
        path = capture / f'capture-{number:05d}.bin'
        session, row, end = verifier.independent(path)
        assert session == summary['session'] and row == samples[number] and end['complete']
        assert number in acks
        pins[path.name] = pin(path)
        pins[path.with_suffix('.ack.json').name] = pin(path.with_suffix('.ack.json'))
    assert pin(PREDICTIONS) == FROZEN_SHA256
    alternatives = [r for r in json.loads(PREDICTIONS.read_text(encoding='utf8')) if r['source'] == SOURCE]
    assert [r['mask'] for r in alternatives] == [0, 3]
    results = []
    for number in args.accepts:
        tracker = Tracker()
        # A projection of unchanged, verified observations from one evaluation.
        # The selector itself verifies query, ancestry, source and membership.
        for row in [summary['session'], samples[args.entry], samples[number],
                    acks[number], samples[args.transfer], acks[args.transfer]]:
            tracker.feed(row)
        result = tracker.result()
        assert result['status'] == 'CONSUMER_ONLY' and len(result['consumptions']) == 1
        accepted = result['consumptions'][0]['accepted']
        resource = int.from_bytes(bytes.fromhex(accepted['selected']['raw_resource'])[40:44], 'little')
        results.append(dict(accept_capture=number, transfer_capture=args.transfer,
            resource_formid=f'0x{resource:08x}', source=SOURCE,
            comparison=compare(result, alternatives), native_epoch=None))
    output = dict(schema='sor-d5b-transfer-members/1', analysis_sha256=pin(analysis),
        journal_sha256=summary['journal_sha256'], selected_receipt_pins=pins,
        projection='One unchanged ACCEPT per selector replay, common entry and transfer',
        results=results, complete_resource_census=False, native_epoch=None)
    with args.output.open('x', encoding='utf8', newline='\n') as stream:
        json.dump(output, stream, indent=2)
        stream.write('\n')
    print(json.dumps([dict(resource=r['resource_formid'], accept=r['accept_capture'],
        matches=[a['consumptions'][0]['exact_region_matches'] for a in r['comparison']['alternatives']])
        for r in results]))


if __name__ == '__main__':
    main()
