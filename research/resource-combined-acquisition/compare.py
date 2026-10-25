# SPDX-License-Identifier: GPL-3.0-or-later
"""Compare fresh SRO1 receipts with unchanged D5A mask alternatives, read only.

Reads raw local receipts/events and pinned D5A prediction bytes. Writes one
exclusive local comparison. Stdlib only; no target, model fitting, save,
configuration, network or Git effects. Synthetic linkage is disabled by default.
"""
import argparse
import json
from pathlib import Path
import struct
from reduce import Tracker, SOURCE, ROOT, load
from build import pin

PREDICTIONS = ROOT / '.local-work/resource-construction-mask-selection/conditional-results.json'
FROZEN_SHA256 = '1c7420c884d5260b6d67f9ffe3f7ccd2f36f903501431feba2f2f85abddf8644'
verifier = load('d5b_independent_compare', 'research/resource-tungsten-acquisition/qualify.py')


def packed(values):
    return struct.pack('<' + 'f' * len(values), *values).hex()


def compare(result, alternatives):
    """Return both alternatives, preserving disagreements and missing evidence."""
    rows = []
    for alternative in alternatives:
        expected_order = [int(o['resource'], 16) for o in alternative['operands']]
        expected_weights = [packed([o['weight']]) for o in alternative['operands']]
        constructions = []
        for observed in result['constructions']:
            actual_order = [struct.unpack_from('<I', bytes.fromhex(c['ires']['raw']), 0x28)[0]
                            for c in observed['calls']]
            actual_weights = [struct.pack('<I', c['weight_bits']).hex() for c in observed['calls']]
            constructions.append(dict(capture=observed['terminal_capture'],
                sampled_mask_matches=observed['mask'] == alternative['mask'],
                observed_first_query=observed['first_query_xy_i32_le'],
                first_query_prediction='UNKNOWN_NOT_IN_FROZEN_ALTERNATIVES',
                ordered_candidates_match=actual_order == expected_order,
                effective_weights_match=actual_weights == expected_weights))
        consumptions = []
        for observed in result['consumptions']:
            accepted = observed['accepted']
            resource = struct.unpack_from('<I', bytes.fromhex(accepted['selected']['raw_resource']), 0x28)[0]
            matches = [r for r in alternative['regions'] if int(r['resource'], 16) == resource
                and packed([v for point in r['points'] for v in point]) == accepted['geometry']['ordered_xyzw']
                and packed(r['native_bound']) == accepted['geometry']['raw_region'][:32]]
            consumptions.append(dict(capture=observed['transfer_capture'], exact_region_matches=len(matches),
                decision=accepted['decision'], geometry_scope='CURRENT_ACCEPTED_REGION_ONLY',
                construction_attribution='UNKNOWN_NO_NATIVE_EPOCH_JOIN'))
        rows.append(dict(mask=alternative['mask'], constructions=constructions, consumptions=consumptions,
                         expected_order=expected_order, expected_weights_le=expected_weights))
    return dict(schema='sor-d5b-comparison/1', evidence_status=result['status'], alternatives=rows,
                frozen_predictions_sha256=FROZEN_SHA256, source=SOURCE,
                native_link=None, synthetic_links=result.get('synthetic_links', []), fit_performed=False)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--receipts', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    assert args.output.resolve().is_relative_to(ROOT / '.local-work/resource-combined-acquisition')
    assert pin(PREDICTIONS) == FROZEN_SHA256
    alternatives = [r for r in json.loads(PREDICTIONS.read_text(encoding='utf8')) if r['source'] == SOURCE]
    assert [r['mask'] for r in alternatives] == [0, 3]
    try:
        tracker = Tracker()
        event_path = args.receipts / 'events.json'
        events = json.loads(event_path.read_text(encoding='utf8')) if event_path.exists() else [json.loads(line) for line in (args.receipts / 'events.jsonl').read_text(encoding='utf8').splitlines()]
        sessions = [r for r in events if r['kind']=='SESSION']
        assert len(sessions)==1, 'receipt set must contain one session'
        samples = {r['capture']: r for r in events if r['kind'] == 'SAMPLE'}
        assert len(samples) == sum(r['kind'] == 'SAMPLE' for r in events), 'duplicate sample capture'
        paths = sorted(args.receipts.glob('capture-*.bin'))
        assert len(paths) == len(samples)
        for path in paths:
            decoded = verifier.independent(path)
            assert decoded[0] == sessions[0], 'cross-session receipt envelope'
            row = decoded[1]
            assert row['pid']==sessions[0]['pid'], 'sample process differs from session'
            assert samples.pop(row['capture']) == row
        assert not samples
        for row in events:
            tracker.feed(row)
        output = compare(tracker.result(), alternatives)
    except (AssertionError, ValueError, KeyError, OSError, struct.error) as failure:
        output = dict(schema='sor-d5b-comparison/1', evidence_status='INVALID',
                      reason=type(failure).__name__ + ': ' + str(failure),
                      alternatives=[dict(mask=r['mask'], comparison='NOT_TESTED_INVALID_EVIDENCE') for r in alternatives],
                      frozen_predictions_sha256=FROZEN_SHA256, native_link=None, fit_performed=False)
    with args.output.open('x', encoding='utf8', newline='\n') as stream:
        json.dump(output, stream, indent=2, allow_nan=False)
        stream.write('\n')
    assert pin(PREDICTIONS) == FROZEN_SHA256
    print(output['evidence_status'], 'two unchanged alternatives compared')


if __name__ == '__main__':
    main()
