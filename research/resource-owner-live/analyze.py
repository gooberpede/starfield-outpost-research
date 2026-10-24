# SPDX-License-Identifier: GPL-3.0-or-later
"""Offline D4D receipt audit and source-bound component-origin reconstruction.

Reads existing SRO1/ACK/event files, frozen D4C inputs and owned decoders. Requires
Starfield absent. Writes a fresh ignored derivative directory, never originals.
No attachment, target/save/configuration/database/Git/network effects. Python
stdlib only. Reconstructed slot origins are not historical generation epochs.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
LOCAL = ROOT / '.local-work/resource-owner-acquisition'


def pin(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


def write(path, value):
    with path.open('x', encoding='utf8', newline='\n') as stream:
        json.dump(value, stream, indent=2)
        stream.write('\n')


def origins(chain):
    """Carry distinct (component, slot, word) tokens through witnessed exchanges.

    This is a static reconstruction checked against observed map/staging values.
    Reject any disagreement; never invent an origin through an unmodeled write.
    """
    if chain['first_operation_divergence'] is not None:
        return dict(status='UNKNOWN_OPERATION_DIVERGENCE')
    mapping, stage, operations = {}, [], []
    for ordinal, component in enumerate(chain['components']):
        for slot, word in enumerate(component['slots']):
            if word:
                stage.append(dict(component=ordinal, slot=slot, word=word,
                                  biome=component['biome'], root=component['root']))
        root = component['root']
        if root:
            mapping[root], stage = stage, mapping.get(root, [])
        snapshot = chain['snapshots'][ordinal+1]
        observed = {int(k): v for k, v in snapshot['mapping'].items()}
        assert {k: [t['word'] for t in v] for k, v in mapping.items()} == observed
        assert [t['word'] for t in stage] == snapshot['staging']
        operations.append(dict(component=ordinal, root=root,
            installed=([t.copy() for t in mapping[root]] if root else None),
            staging_after=[t.copy() for t in stage]))
    selected = mapping.get(chain['selected'])
    assert selected is not None and [t['word'] for t in selected] == chain['native_selected_array']
    return dict(status='STATIC_RECONSTRUCTION_MATCHES_EVERY_OBSERVED_BOUNDARY',
                selected_origins=selected, operations=operations,
                historical_generation_join=None)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--captures', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    assert args.captures.resolve().is_relative_to(LOCAL)
    assert args.output.resolve().is_relative_to(LOCAL)
    assert subprocess.check_output(['powershell', '-NoProfile', '-Command',
        '@(Get-Process Starfield -ErrorAction SilentlyContinue).Count'], text=True).strip() == '0'
    args.output.mkdir(exist_ok=False)
    sys.path.insert(0, str(ROOT / 'research/resource-oracle-retail'))
    receipt = module('live_d4a_receipts', ROOT / 'research/resource-tungsten-acquisition/qualify.py')
    compare = module('live_d4d_compare', ROOT / 'research/resource-owner-acquisition/compare.py')
    admission = module('live_d4d_admission', ROOT / 'research/resource-owner-acquisition/admission.py')
    events = args.captures / 'events.jsonl'
    rows = [json.loads(line) for line in events.read_text(encoding='utf8').splitlines()]
    samples = [r for r in rows if r['kind'] == 'SAMPLE']
    assert [r['capture'] for r in samples] == list(range(1, len(samples)+1))
    acknowledged = {r['capture']: r['accepted'] for r in rows if r['kind'] == 'ACK_ACCEPTED'}
    verified, incomplete = [], []
    tracker, useful = admission.Tracker(), []
    for row in rows:
        if row['kind'] == 'SAMPLE':
            path = args.captures / f'capture-{row["capture"]:05d}.bin'
            decoded = receipt.independent(path)
            assert decoded[1] == row
            if not decoded[-1]['complete']:
                incomplete.append(row['capture'])
            verified.append(dict(capture=row['capture'], sha256=pin(path),
                ack_sha256=pin(path.with_suffix('.ack.json')),
                complete=decoded[-1]['complete'], acknowledged=acknowledged.get(row['capture'])))
        if tracker.feed(row):
            match = tracker.last_match
            useful.append(dict(transfer=row['capture'], accepted_capture=match['consumption']['capture'],
                construction_entry=match['construction']['entry']['capture'],
                qualification=match['qualification'], generation_epoch=None))
    result = compare.validate(rows)
    model_path = ROOT / '.local-work/resource-owner-root/freeze01/inputs-v1.json'
    model = json.loads(model_path.read_text(encoding='utf8'))
    selected = [c for c in result['chains'] if c['source_identity'] == admission.TARGET_SOURCE and c['owner'] == 0x5de4c]
    details = []
    for chain in selected:
        model_comparison = []
        for ordinal, (observed, projected) in enumerate(zip(chain['components'], model['components'])):
            model_comparison.append(dict(component=ordinal,
                biome_equal=observed['biome']==projected['biome'],
                root_equal=observed['root']==projected['root'],
                changed_slots=[dict(slot=slot, observed=word, projected=other)
                    for slot, (word, other) in enumerate(zip(observed['slots'], projected['slots'])) if word != other]))
        calls = [r for r in samples if r.get('site')=='ordinary_resource_call' and
            r['pid']==chain['entry']['pid'] and r['tid']==chain['entry']['tid'] and
            r['thread_lifetime']==chain['entry']['thread_lifetime'] and
            r['invocation_token']==chain['entry']['invocation_token']]
        details.append(dict(entry_capture=chain['entry']['capture'], source_identity=chain['source_identity'],
            owner=chain['owner'], components=chain['components'], selected=chain['selected'],
            native_selected_array=chain['native_selected_array'], calls=chain['calls'],
            candidate_call_coverage=chain['candidate_call_coverage'],
            selected_array_reconciliation=chain['selected_array_reconciliation'],
            first_model_divergence=compare.first_divergence(chain, model),
            model_comparison=model_comparison,
            call_metadata=[dict(capture=r['capture'], resource=int.from_bytes(bytes.fromhex(r['ires']['raw'])[0x28:0x2c], 'little'),
                rarity=bytes.fromhex(r['ires']['raw'])[0x110], weight_bits=r['effective_weight_bits'],
                main_file_identity=r['file_provenance']['main_file_identity']) for r in calls], origins=origins(chain)))
    summary = dict(schema='sor-d4d-live-audit/1', synthetic=False, events_sha256=pin(events),
        captures=len(samples), receipt_records=len(samples)*3, incomplete=incomplete,
        all_samples_acknowledged=all(acknowledged.get(r['capture']) is True for r in samples),
        complete_constructions=len(result['chains']), rejected_fragments=result['rejected'],
        target_constructions=len(selected), useful=useful,
        loss=[r for r in rows if r['kind']=='LOSS'], exceptions=[r for r in rows if r['kind']=='EXCEPTION'],
        terminal=[r for r in rows if r['kind'] in ('STOP_COMMITTED','EXIT','FAILURE_CLEANUP')],
        frozen_model_sha256=pin(model_path), historical_generation_join=None)
    write(args.output / 'verified-receipts.json', verified)
    write(args.output / 'all-constructions.json', result)
    write(args.output / 'target-constructions.json', details)
    write(args.output / 'summary.json', summary)
    print(json.dumps({k: summary[k] for k in ('captures', 'incomplete', 'all_samples_acknowledged',
        'complete_constructions', 'target_constructions', 'useful')}, indent=2))


if __name__ == '__main__':
    main()
