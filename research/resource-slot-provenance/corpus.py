# SPDX-License-Identifier: GPL-3.0-or-later
"""Version D4E portable corpora from installed components and frozen D4C layout.

Reads pinned installed definitions, the D4E freeze and D4C prepared corpus.
Reuses owned D3 descriptor qualification conservatively. Writes exclusive local
corpus, flat inference bundle, dependency/byte ledger and unsupported reasons.
No native answer, save, target, network, database or Git access.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import struct
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / 'research' / p) for p in
               ('resource-standalone', 'resource-owner-root')]
import builder
import corpus_d3
from audit import pin, write
from layout_validate import expanded
import predictor_d4e as predictor
from candidate_order import candidates as ordered_candidates
from qualification import qualify


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base', type=Path, required=True)
    parser.add_argument('--freeze', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    out = args.output.resolve()
    assert out.is_relative_to(ROOT / '.local-work/resource-slot-provenance')
    out.mkdir(exist_ok=False)
    seal = json.loads((args.freeze / 'freeze-v1.json').read_text())
    assert all(pin(args.freeze / n) == h for n, h in seal['outputs'].items())
    assert pin(builder.ESM) == builder.DEFINITION
    records = {h['formid']: (h, fs) for h, fs in builder.esm_records(builder.ESM,
        {b'PNDT', b'BIOM', b'RSGD', b'IRES'}, repeated=True)}
    predictions = json.loads((args.freeze / 'prediction-v1.json').read_text())
    rarities = {fid: builder.last(fs, b'SNAM')[0] for fid, (h, fs) in records.items()
                if h['type'] == 'IRES'}
    # Freeze the source-backed ordering refinement before generating geometry.
    refined = {body: {key: ordered_candidates(int(key),
        {int(k): v for k, v in data['map']['maps'].items()}, rarities)
        for key in data['map']['maps']} for body, data in predictions.items()}
    write(out / 'candidate-freeze-v2.json', dict(candidates=refined,
        method_sha256=pin(Path(__file__).with_name('candidate_order.py')),
        original_freeze_sha256=pin(args.freeze / 'freeze-v1.json'),
        refinement='STATIC small-list stable insertion; prior target answers already known'))
    payload = copy.deepcopy(json.loads(args.base.read_text())['payload'])
    baseline = len(predictor.canonical(payload))
    payload['schema'] = predictor.SCHEMA
    ledger = []
    descriptors = {hashlib.sha256(b).hexdigest(): b for h, fs in records.values()
                   if h['type'] == 'RSGD' for t, b in fs if t == b'DNAM'}
    for body, data in payload['bodies'].items():
        prediction = builder.selections(records, int(body, 16))
        qualify(records, prediction)
        frozen = predictions[body]
        rows = {r['biome']: r for r in frozen['components']}
        for biome, old in data['biomes'].items():
            row = rows.get(int(biome, 16))
            try:
                if row is None:
                    raise ValueError('MISSING_BIOME_SELECTION')
                original, detail = corpus_d3.ordinary(records, prediction, int(biome, 16),
                                                      payload['generation_blocks'])
                candidates = refined[body].get(str(row['root']))
                if not candidates or candidates['ordered'] is None:
                    raise ValueError('UNRESOLVED_OWNER_MAP_CANDIDATES')
                raw = descriptors[detail['dnam_sha256']]
                resources = []
                for fid in candidates['ordered']:
                    rarity = builder.last(records[fid][1], b'SNAM')[0]
                    block = list(struct.unpack_from('<8f', raw, 40 * (rarity + 7)))
                    key = hashlib.sha256(struct.pack('<8f', *block)).hexdigest()[:16]
                    if key in payload['generation_blocks'] and payload['generation_blocks'][key] != block:
                        raise ValueError('BLOCK_COLLISION')
                    payload['generation_blocks'][key] = block
                    resources.append(dict(id=f'{fid:08x}', rarity=rarity, block=key))
                resources.extend(r for r in original['resources'] if r.get('branch') == 'special')
                data['biomes'][biome] = dict(status='ORDINARY_AND_SPECIAL', resources=resources)
                ledger.append(dict(body=body, biome=biome, root=row['root'],
                    candidates=candidates, descriptor=detail, old=old,
                    new=data['biomes'][biome]))
            except (ValueError, KeyError, StopIteration) as error:
                data['biomes'][biome] = dict(status=str(error) or 'UNRESOLVED_DESCRIPTOR', resources=[])
                ledger.append(dict(body=body, biome=biome, unsupported=data['biomes'][biome]['status'], old=old))
    predictor.validate(predictor.seal(payload))
    used = {r['block'] for b in payload['bodies'].values() for v in b['biomes'].values()
            for r in v['resources']}
    payload['generation_blocks'] = {k: v for k, v in payload['generation_blocks'].items() if k in used}
    for variant, value in [('normalized', payload), ('expanded', expanded(payload))]:
        envelope = predictor.seal(value)
        predictor.validate(envelope)
        (out / f'{variant}.json').write_bytes(predictor.canonical(envelope) + b'\n')
    code = out / 'code'
    code.mkdir()
    for path in (ROOT / '.local-work/resource-save52-d3/revision06/build-v1/code').glob('*.py'):
        (code / path.name).write_bytes(Path(__file__).with_name('predictor_d4e.py').read_bytes()
                                     if path.name == 'predictor.py' else path.read_bytes())
    assert (code / 'predictor.py').exists()
    write(out / 'preparation.json', dict(schema='sor-d4e-build/1', base=str(args.base),
        base_sha256=pin(args.base), freeze_sha256=pin(args.freeze / 'freeze-v1.json'),
        installed_esm_sha256=pin(builder.ESM), lineage=ledger,
        canonical_payload_before=baseline, canonical_payload_after=len(predictor.canonical(payload)),
        incremental_payload_bytes=len(predictor.canonical(payload)) - baseline,
        normalized_file_bytes=(out / 'normalized.json').stat().st_size,
        expanded_file_bytes=(out / 'expanded.json').stat().st_size,
        code={p.name: pin(p) for p in code.glob('*.py')},
        note='Only derived candidates/blocks retained at inference; raw component/map lineage local-only'))
    print(json.dumps(dict(biomes=len(ledger), unsupported=sum('unsupported' in r for r in ledger),
        delta=len(predictor.canonical(payload)) - baseline)))


if __name__ == '__main__':
    main()
