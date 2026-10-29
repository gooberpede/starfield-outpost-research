# SPDX-License-Identifier: GPL-3.0-or-later
"""Reduce the approved R2 retail diagnostics after target exit; stdlib only.

Reads the immutable raw/ACK capture and independently recorded module-base,
milestone and terminal receipts. Creates one exclusive local summary JSON.
No game, memory, save, Vortex, configuration, Git or original-evidence mutation.
Uses the owned unchanged R1 reader and reviewed R2 predicate decoder.
"""
import argparse
from collections import Counter
import json
from pathlib import Path
import struct
from d5p_r2_diagnostics import ROOT, DLL, capture
from read_capture import decode, SIZE_V2


def analyze(folder):
    folder = Path(folder)
    admitted = json.loads((folder / 'admitted-session.json').read_text())
    session = Path(admitted['session'])
    result = capture(session, admitted['process']['image_base'])
    raw = (session / 'events.bin').read_bytes()
    events = [decode(raw[i + 16:i + 16 + SIZE_V2]) for i in range(0, len(raw), SIZE_V2 + 16)]
    assert len(events) == result['authentication']['independently_verified_durable_records']
    assert result['authentication']['unacknowledged_records'] == 0
    terminal = json.loads((session / 'terminal.json').read_text())
    assert terminal['dll_sha256'] == DLL
    assert terminal['failed'] is False and terminal['output_faults'] == 0
    assert terminal['enqueued'] == terminal['written'] == terminal['flushed'] == terminal['acknowledged'] == len(events)
    demands = [e for e in events if e['kind'] == 1]
    reasons = Counter(e['reason'] for e in demands)
    extents = Counter((e['grid_count'], e['grid_capacity']) for e in demands if e['reason'] == 24)
    assert len(demands) == len(result['diagnostics'])
    valid_type_values = []
    for e, diagnostic in zip(demands, result['diagnostics']):
        assert diagnostic['result'] == 'FIRST_FAILURE_IDENTIFIED'
        if e['reason'] == 24:
            assert e['grid_count'] <= e['grid_capacity'] and e['grid_count'] > 256
            assert e['actual_proc'] == e['proc']
            assert e['proc_type'] == admitted['process']['image_base'] + 0x4b3f3a8
            assert e['grid_type'] == admitted['process']['image_base'] + 0x4b67f48
            assert diagnostic['fields']['members']['validity'] == 'NOT_REACHED'
            assert diagnostic['fields']['retained_grid']['validity'] == 'NOT_REACHED'
            valid_type_values.append((e['proc_type'], e['grid_type']))
    loaded = json.loads((folder / 'loaded-health04.json').read_text())
    arrival = json.loads((folder / 'arrival-health05.json').read_text())
    cutoff = loaded['ack']['flushed']
    assert all(e['kind'] != 1 for e in events[:cutoff])
    assert all(e['sequence'] > cutoff for e in demands)
    # Admission order and ACK watermarks bound recorded observations, not the
    # native execution start or causal travel trigger of an asynchronous request.
    return dict(schema='sor-d5p-r2-retail-analysis/1',
        question='Which first predicate rejected the recorded R2 source-demand contexts?',
        answer='OBSERVER_GRID_INSPECTION_LIMIT_EXCEEDED' if set(reasons) == {24} else 'MIXED_FIRST_FAILURES',
        identity=result['authentication']['identity'], module_base=admitted['process']['image_base'],
        records=len(events), demands=len(demands), first_demand=demands[0]['sequence'], last_demand=demands[-1]['sequence'],
        first_failure_reasons=dict(reasons), extent_groups=[dict(count=n, capacity=c, records=total) for (n, c), total in sorted(extents.items())],
        type_operand_groups=[dict(proc_type=a, grid_type=b, records=n) for (a, b), n in Counter(valid_type_values).items()],
        owner_groups={f'0x{owner:08x}': n for owner, n in Counter(e['owner'] for e in demands).items()},
        mode_groups=dict(Counter(e['args'][4] for e in demands)),
        stage_counts=dict(Counter(e['kind'] for e in events)),
        epoch_count=len({e['epoch'] for e in demands}),
        invocation_count=len({e['invocation'] for e in demands}),
        starting_hazard_demands=sum(bool(e['hazards']) for e in demands),
        complete_chains=len(result['authentication']['complete_chains']),
        drop_causes=dict(total=terminal['drops'], queue_full=terminal['queue_full'], contention_exhausted=terminal['contention_exhausted']),
        terminal=terminal, authentication=result['authentication'],
        chronology=dict(pretravel_flushed=cutoff, arrival_flushed=arrival['ack']['flushed'],
            pretravel_demand_records=0, first_recorded_failure_after_pretravel_watermark=True,
            limits='No per-event clock; watermark is admission/persistence order, not exact event start or proof of travel causality'),
        outcome_dimensions=dict(plugin='LOADED_AND_ACTIVE_THROUGH_ARRIVAL', predicates='EXERCISED',
            diagnostics='DISCRIMINATING_AUTHENTICATED_RECORDS', acquisition='FINISHED_LOSSY_INCOMPLETE',
            retained_population='UNRESOLVED', historical_original_cause='NOT_RETROSPECTIVELY_PROVEN',
            selected_source_identity='UNQUALIFIED_MEMBERSHIP_AND_RETAINED_GRID_NOT_REACHED'),
        caveats=['All refers only to 6101 admitted demand records, not dropped or unobserved requests',
                 'No bound change, predicate relaxation, new binary or retry is authorized by this reduction',
                 'The first failed predicate prevents observing later membership, retained Grid and final lifetime predicates'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--folder', type=Path, default=ROOT / '.local-work/d5p-r2-retail')
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    result = analyze(args.folder)
    with args.out.open('x', encoding='utf8', newline='\n') as f:
        json.dump(result, f, indent=2)
        f.write('\n')
    print(json.dumps({k: result[k] for k in ('records', 'demands', 'first_demand', 'last_demand', 'extent_groups', 'stage_counts', 'chronology')}))


if __name__ == '__main__':
    main()
