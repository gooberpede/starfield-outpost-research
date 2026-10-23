# SPDX-License-Identifier: GPL-3.0-or-later
"""Exact, nonfitting comparison of closed C2A receipts and pinned C1H geometry.

Reads receipts, prediction files and original project evaluator. Writes one new
local JSON derivative. Never operates a target or changes inputs. Synthetic use
is authorized in Phase A; retail interpretation requires a separately supplied
Phase C approval receipt bound to this card and the closed event file.
Source/frame identity remains UNKNOWN without a producer/context witness.
"""
import argparse
import hashlib
import json
from pathlib import Path
import struct
import sys

ROOT = Path(__file__).resolve().parents[2]
LOCAL = ROOT / '.local-work/resource-carinae'
sys.path.insert(0, str(ROOT / 'save-analysis/scripts'))
from resource_spatial import evaluate_region
from qualify import independent, pin, write

PREDICTION = ROOT / '.local-work/resource-installed-settings/geometry02.json'


def signature(region):
    return (struct.pack('<4f', *region['native_bound']) +
            b''.join(struct.pack('<4f', *point) for point in region['points']))


def key(row):
    return tuple(row[k] for k in ('pid', 'tid', 'thread_lifetime',
                                  'updater_token', 'updater_bp', 'temporary_set'))


def qualified(row):
    return (row.get('ancestry') == 'BOUND_CALLBACK' and
            row.get('required_reads_complete') is True and
            all(row.get(k) is True for k in ('qb_retained_read', 'closure_read', 'descriptor_read')) and
            all(row.get(k, {}).get('status') == 'COMPLETE' for k in ('selected', 'geometry', 'file_provenance')) and
            row['file_provenance']['main_file_identity'])


def compare(rows, predictions):
    """Keep observed decisions, geometry equality and ancestry as separate axes."""
    transfers = [r for r in rows if r.get('ancestry') == 'BOUND_TRANSFER' and
                 r.get('required_reads_complete') is True and
                 r.get('refresh_payload', {}).get('status') == 'COMPLETE']
    results = []
    for row in rows:
        if 'decision' not in row:
            continue
        result = dict(capture=row['capture'], native_decision=row['decision'],
                      qualified=qualified(row), source_frame_identity='UNKNOWN',
                      generation_epoch='UNKNOWN', census_complete=False,
                      geometry_equality='NOT_TESTED', matches=[],
                      region_classification='UNKNOWN', transfer_membership=False,
                      completed_cache_install='NOT_OBSERVED', catalogue='NOT_OBSERVED')
        if not result['qualified']:
            results.append(result)
            continue
        raw = bytes.fromhex(row['geometry']['raw_region'])
        points = bytes.fromhex(row['geometry']['ordered_xyzw'])
        n = struct.unpack_from('<I', raw, 0x18)[0]
        assert len(raw) == 48 and len(points) == 16*n
        fid = struct.unpack_from('<I', bytes.fromhex(row['selected']['raw_resource']), 0x28)[0]
        wanted = raw[:16] + points
        matches = [dict(source=r['source'], cell=r['cell']) for p in predictions
                   if p['site'] == 'Carinae' for r in p['regions']
                   if int(r['resource'], 16) == fid and signature(r) == wanted]
        result.update(resource=f'0x{fid:08x}', geometry_equality='EXACT' if matches else 'NO_EXACT_MATCH',
                      matches=matches, geometry_sha256=hashlib.sha256(wanted).hexdigest(),
                      source_slot=row['source_slot'], source_wrapper=row['selected']['source_wrapper'])
        joined = [t for t in transfers if key(t) == key(row) and t['capture'] > row['capture']
                  and t.get('binding_reference') == row['binding_reference']
                  and t.get('raw_binding_extra') == row['raw_binding_extra']]
        result['transfer_membership'] = (row['decision'] == 'ACCEPT' and len(joined) == 1 and
            any(m['pointer'] == row['resource_pointer'] for m in joined[0]['refresh_payload']['members']))
        q = struct.unpack('<3f', bytes.fromhex(row['qb_retained_bits']))
        radius, upper = struct.unpack_from('<2f', bytes.fromhex(row['raw_closure']), 16)
        result['query'] = dict(qb=list(q), radius=radius, upper=upper,
                               evidence='RETAINED_WORDS_NOT_EVERY_PER_USE_LOAD')
        # This diagnostic is deliberately conditional, including for a match.
        result['region_classification'] = evaluate_region(
            q, radius, upper, struct.unpack_from('<3f', raw),
            struct.unpack_from('<f', raw, 12)[0], list(struct.iter_unpack('<4f', points)))
        result['classification_scope'] = 'CONDITIONAL_RETAINED_QUERY_REPLAY'
        results.append(result)
    return dict(regions=results, coverage='VISITED_TERMINALS_ONLY',
                missing_events_are_absence=False, source_frame_identity='UNKNOWN')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--receipts', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--phase-c-approval', type=Path)
    a = parser.parse_args()
    assert a.receipts.resolve().is_relative_to(LOCAL) and a.output.resolve().is_relative_to(LOCAL)
    event_file = a.receipts / 'events.json'
    if event_file.exists():
        events = json.loads(event_file.read_text())
    else:
        event_file = a.receipts / 'events.jsonl'
        events = [json.loads(line) for line in event_file.read_text().splitlines()]
    assert events
    synthetic = all(r.get('synthetic') is True for r in events)
    if not synthetic:
        assert a.phase_c_approval is not None, 'Phase A refuses unapproved retail Phase C'
        assert a.phase_c_approval.resolve().is_relative_to(LOCAL)
        approval = json.loads(a.phase_c_approval.read_text())
        assert approval['status'] == 'GO_PHASE_C' and approval['human_instruction'].strip()
        assert approval['card_sha256'] == pin(ROOT / 'docs/experiments/resource-carinae/run-card.md')
        assert approval['events_sha256'] == pin(event_file)
        assert all(r.get('synthetic') is False for r in events)
    samples = [r for r in events if r['kind'] == 'SAMPLE']
    assert len(samples) == len(list(a.receipts.glob('capture-*.bin')))
    for row in samples:
        assert independent(a.receipts / f'capture-{row["capture"]:05d}.bin')[1] == row
    pins = {str(PREDICTION): pin(PREDICTION)}
    # Immutable versioned C1H source ledger is the authority for the full data.
    import csv
    ledger = ROOT / 'docs/experiments/resource-installed-settings/sources.csv'
    pinned = {r['path']: r['sha256'] for r in csv.DictReader(ledger.open())}
    assert pins[str(PREDICTION)] == pinned[PREDICTION.relative_to(ROOT).as_posix()]
    result = compare(samples, json.loads(PREDICTION.read_text()))
    write(a.output, dict(result, synthetic=synthetic, pins=pins, ledger_sha256=pin(ledger),
                         events_sha256=pin(event_file)))


if __name__ == '__main__':
    main()
