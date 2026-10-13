# SPDX-License-Identifier: GPL-3.0-or-later
"""Offline ship-route/grid coverage audit; stdout JSON only.

Reads the explicit archived 040 session, frozen extracted saved inputs/predictions,
and existing project readers. Does not decode new saves or execute native code.
No network, process, database, configuration or original-file writes. Redirect
stdout to a new ignored receipt. CPython stdlib/project dependencies only.
Preserves both-drive 40,000,000,000-byte free-space guard. Source-informed by
Bethesda native exports; see docs/experiments/ship-relocation/dependencies.md.
Saved nonzero operands and synthetic controls are not native validation.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'research/existing-reference-grid'))
sys.path.insert(0, str(ROOT / 'save-analysis/scripts'))
from fallback_provenance import audit, r, guard
from durable_position_v2 import reproduce

INPUT_HASH = '9fe2924ff7bc444714fbab685893b8d8e0572dc2c7aad96cbd06de8aac93ad91'


def saved_cases(inputs, predictions):
    if len(inputs) != 23 or len(predictions) != 23:
        raise ValueError('frozen_count')
    rows = []
    for item, frozen in zip(inputs, predictions):
        result = reproduce(item)
        if result['identity'] != frozen['identity'] or result['source'] != frozen['source']:
            raise ValueError('frozen_identity')
        actual_cell = result['native_cell']
        cell = [actual_cell['tag'], *actual_cell['xy']] if actual_cell else None
        if cell != frozen['cell'] or result['center_hex'] != frozen['center_hex']:
            raise ValueError('frozen_prediction_changed')
        base = result['selected_base']
        floor = result['trace']['floor']
        rows.append(dict(sample=item['source']['sample'], identity=item['identity'],
                         source_offset=item['source']['record_offset'], frame=item['frame'],
                         base=base, floor=floor, cell=cell,
                         nonzero=any(floor), negative=any(q < 0 for q in floor),
                         hemisphere_crossing=cell[0] != base[0],
                         fine_carry=any((base[k+1] % 12) + floor[k] >= 12 or
                                        (base[k+1] % 12) + floor[k] < 0 for k in range(2)),
                         evidence='SAVE-DERIVED OPERAND / FROZEN PREDICTION; NO NATIVE OUTPUT'))
    return rows


def main(session):
    guard()
    inputs_path = ROOT / 'docs/experiments/engine-oracle/inputs.json'
    predictions_path = ROOT / 'docs/experiments/engine-oracle/predictions.json'
    paths = [inputs_path, predictions_path, session/'ready.json', session/'events.bin', session/'records.jsonl']
    hashes = lambda: {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    before = hashes()
    if before[str(inputs_path)] != INPUT_HASH or before[str(predictions_path)] != r.PREDICTION_HASH:
        raise ValueError('frozen_hash')
    events, integrity = r.records(session)
    ready = json.loads((session/'ready.json').read_text())
    observed = audit(events, int(ready['module_base'], 16))
    rows = saved_cases(json.loads(inputs_path.read_bytes()), json.loads(predictions_path.read_bytes()))
    if hashes() != before:
        raise ValueError('inputs_changed')
    print(json.dumps(dict(schema='sor-ship-grid-audit/1', inputs_sha256=before,
                         integrity=integrity, captured_route=observed,
                         saved_operand_summary={key: sum(row[key] for row in rows)
                                                for key in ('nonzero', 'negative', 'hemisphere_crossing', 'fine_carry')},
                         saved_cases=rows,
                         native_nonzero_validation='NOT TESTED',
                         native_workshop_equivalence='NOT TESTED'), indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('session', type=Path)
    main(parser.parse_args().session)
