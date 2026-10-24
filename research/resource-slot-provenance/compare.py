# SPDX-License-Identifier: GPL-3.0-or-later
"""Post-freeze component/transition comparison with original D4D SRO1 bytes.

Reads frozen prediction, original captures 358–374 and owned independent decoder.
Writes exclusive ignored comparisons. No target, source, Git or network writes.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / 'research' / p) for p in
               ('resource-oracle-retail', 'resource-owner-root')]
from audit import pin, write
from owner_map import reconstruct


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--freeze', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    assert args.output.resolve().is_relative_to(ROOT / '.local-work/resource-slot-provenance')
    args.output.mkdir(exist_ok=False)
    seal = json.loads((args.freeze / 'freeze-v1.json').read_text())
    assert all(pin(args.freeze / n) == h for n, h in seal['outputs'].items())
    assert all(pin(p) == h for p, h in seal['methods'].items())
    prediction = json.loads((args.freeze / 'prediction-v1.json').read_text())['0005de4c']
    decoder = module('d4e_decoder', ROOT / 'research/resource-tungsten-acquisition/qualify.py')
    comparator = module('d4e_map_comparator', ROOT / 'research/resource-owner-acquisition/compare.py')
    captures = ROOT / '.local-work/resource-owner-acquisition/retail-attempt01'
    rows, pins = [], {}
    for number in range(358, 375):
        path = captures / f'capture-{number:05d}.bin'
        session, row, end = decoder.independent(path)
        assert end['complete'] and row['capture'] == number
        rows.append(row)
        pins[str(path)] = pin(path)
    # This is an explicitly cropped chain, not a full-session continuity audit.
    state = comparator.State()
    state.last_capture = rows[0]['capture'] - 1
    state.sequences[(rows[0]['tid'], rows[0]['thread_lifetime'])] = rows[0]['thread_sequence'] - 1
    result = comparator.validate(rows, state=state)
    assert len(result['chains']) == 1
    assert not result['rejected']
    chain = result['chains'][0]
    slots, transitions = [], []
    for ordinal, (projected, actual) in enumerate(zip(prediction['components'], chain['components'])):
        for slot in range(6):
            slots.append(dict(component=ordinal, slot=slot, biome=actual['biome'],
                identity_equal=projected['biome'] == actual['biome'],
                root_equal=projected['root'] == actual['root'],
                second_key_equal=projected['biome'] == actual['identity'][1],
                predicted=f"0x{projected['slots'][slot]:08x}",
                observed=f"0x{actual['slots'][slot]:08x}",
                equal=projected['slots'][slot] == actual['slots'][slot]))
        prefix = reconstruct(prediction['components'][:ordinal + 1])
        snapshot = chain['snapshots'][ordinal + 1]
        expected = {str(k): v for k, v in prefix['maps'].items()}
        observed = {str(k): v for k, v in snapshot['mapping'].items()}
        transitions.append(dict(component=ordinal, predicted_map=expected,
            observed_map=observed, predicted_staging=prefix['discarded_staging'],
            observed_staging=snapshot['staging'],
            equal=expected == observed and prefix['discarded_staging'] == snapshot['staging']))
    candidates = prediction['candidates'][str(chain['selected'])]
    write(args.output / 'comparison.json', dict(freeze_sha256=pin(args.freeze / 'freeze-v1.json'),
        receipt_pins=pins, slots=slots, components_predicted=len(prediction['components']),
        components_observed=len(chain['components']), transitions=transitions,
        first_operation_divergence=chain['first_operation_divergence'],
        predicted_calls=candidates['ordered'], observed_calls=chain['calls'],
        calls_equal=candidates['ordered'] == chain['calls'],
        final_selected_equal=prediction['map']['maps'][str(chain['selected'])] == chain['native_selected_array'],
        observed_native_keys=[c['identity'] for c in chain['components']],
        registered_type_prediction='UNKNOWN; registration is a runtime input',
        cropped_chain=True, rejected=result['rejected'],
        coverage=chain['candidate_call_coverage'], snapshots=chain['snapshots']))
    print(json.dumps(dict(slots_equal=sum(s['equal'] for s in slots),
        transitions_equal=sum(t['equal'] for t in transitions), calls_equal=candidates['ordered'] == chain['calls'])))


if __name__ == '__main__':
    main()
