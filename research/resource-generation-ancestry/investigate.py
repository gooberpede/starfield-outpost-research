# SPDX-License-Identifier: GPL-3.0-or-later
"""C1F offline comparison and explicitly enumerated branch diagnostics.

Reads unchanged C1E SRO1 receipts, frozen v2 requests and owned evaluator.
Writes a NEW ignored JSON only; stdlib and existing project code. No target,
save, installed data, Ghidra, network or Git writes. Run from repository root.
Alternatives: active weights globally, only IL-family sources, or exotic setting
alone. Native 14079b520 supplies active weight 1 and per-rarity settings.
No alternative is claimed observed on Feynman; no scalar search is performed.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import struct
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'research/resource-region-ancestry'))
from qualify import independent
sys.path.insert(0, str(ROOT / 'research/resource-geometry'))
import geometry


def digest(p):
    with Path(p).open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def packed(values):
    return struct.pack('<' + 'f' * len(values), *values)


def signature(region):
    return b''.join(packed(p) for p in region['points']) + packed(region['native_bound'])


def compare(observed, regions):
    return {r['resource']: [dict(source=g['source'], cell=g['cell']) for g in regions
            if g['resource'] == r['resource'] and signature(g) == r['signature']]
            for r in observed}


def run():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    assert args.output.resolve().is_relative_to(ROOT / '.local-work')
    assert not args.output.exists()
    receipts = ROOT / '.local-work/resource-region-ancestry/retail-attempt01'
    freeze_path = ROOT / 'docs/experiments/resource-geometry-mature-context/freeze-mature-v2.json'
    freeze = json.loads(freeze_path.read_text())
    pin = next(p for p in freeze['complete_geometry'] if 'feynman' in p['path'])
    assert digest(pin['path']) == pin['sha256']
    frozen = json.loads(Path(pin['path']).read_text())
    events = [json.loads(l) for l in (receipts / 'events.jsonl').read_text().splitlines()]
    session = next(r for r in events if r['kind'] == 'SESSION')
    module_base = session['module_base']
    samples = [r for r in events if r['kind'] == 'SAMPLE']
    assert len(samples) == len(list(receipts.glob('capture-*.bin'))) == 967
    for row in samples:
        assert independent(receipts / f'capture-{row["capture"]:05d}.bin')[1] == row
    observed = []
    transfer = samples[-1]
    assert transfer['ancestry'] == 'BOUND_TRANSFER'
    for r in samples:
        if r.get('decision') != 'ACCEPT':
            continue
        h = bytes.fromhex(r['geometry']['raw_region'])
        points = bytes.fromhex(r['geometry']['ordered_xyzw'])
        assert len(points) == 16 * struct.unpack_from('<I', h, 24)[0]
        fid = struct.unpack_from('<I', bytes.fromhex(r['selected']['raw_resource']), 40)[0]
        ref, base, extra = [bytes.fromhex(r[k]) for k in ('raw_binding_reference', 'raw_binding_base', 'raw_binding_extra')]
        assert ref[0x2e] == 0x4a and base[0x2e] == 0x1e
        assert struct.unpack_from('<I', base, 0x28)[0] == 0x2c60e9
        assert struct.unpack_from('<Q', extra)[0] == module_base + 0x4c24e60
        assert extra[0x12] == 0xbc and extra[0x98:0xa0].hex() == 'c3a5866f4cfcf585'
        proof = r['file_provenance']
        assert proof['count'] == len(proof['files']) == 1
        prefix = bytes.fromhex(proof['files'][0]['raw_prefix'])
        assert prefix[0x38:].split(b'\0', 1)[0] == b'Starfield.esm'
        assert not (struct.unpack_from('<I', prefix, 0x1b8)[0] & 0x700)
        assert prefix[0x218] == 0 and fid >> 24 == 0
        assert r['ancestry'] == 'BOUND_CALLBACK' and r['file_provenance']['main_file_identity']
        assert all(r[k] == transfer[k] for k in ('pid', 'tid', 'thread_lifetime', 'updater_token', 'updater_bp', 'temporary_set'))
        assert any(m['pointer'] == r['resource_pointer'] for m in transfer['refresh_payload']['members'])
        assert packed(struct.unpack('<3f', bytes.fromhex(r['qb_retained_bits']))[:2]) == packed(frozen['center'])
        observed.append(dict(capture=r['capture'], resource=f'{fid:08x}',
                             signature=points + h[:16], row=r))
    assert len(observed) == 4
    ilrow, curow = [next(o['row'] for o in observed if o['resource'] == fid) for fid in ('000057d4', '000057cf')]
    assert all(ilrow[k] == curow[k] for k in ('source_key', 'source_slot', 'source_ordinal', 'procgen'))
    assert ilrow['selected']['source_wrapper'] == curow['selected']['source_wrapper']
    # Independent geometry bytes; existing separately pinned analysis qualifies
    # transfer membership, not this numeric comparison's oracle.
    analysis_path = ROOT / '.local-work/resource-region-ancestry/analysis-attempt01.json'
    analysis = json.loads(analysis_path.read_text())
    assert analysis['event_sha256'] == digest(receipts / 'events.jsonl')
    assert {j['capture'] for j in analysis['joins'] if j['accepted_region_to_transfer']} == {r['capture'] for r in observed}
    base = [r for s in frozen['sources'] for r in s['regions']]
    cs = json.loads((ROOT / '.local-work/resource-milestone-b-spatial-constants.json').read_text())['constants']
    constants = {int(c['va'], 16): c['float'] for c in cs}
    constants.update({int(c['va'], 16): c['value'] for c in frozen['constants']})
    variants = [('baseline', 'Unchanged frozen requests; reproducibility control.'),
                ('active_all', '14079b520 ordinary active-weight branch; all ordinary weights=1.'),
                ('active_il_family', 'Same branch limited to frozen IL-family sources; other source biomes unchanged.'),
                ('exotic_setting_one', 'Native per-rarity inactive settings are independent; test exotic weight=active unit endpoint, keeping lower rarity settings. Not an observed setting.')]
    results = []
    constraint = None
    for name, justification in variants:
        regions = []
        changed = []
        for source in frozen['sources']:
            req = copy.deepcopy(source['request'])
            if name == 'exotic_setting_one':
                for r in req['ordered_resources']:
                    if r['resource'] == '000057d4':
                        changed.append(dict(source=req['source'], resource=r['resource'], old=r['weight'], new=1))
                        r['weight'] = 1
            if name == 'active_all' or (name == 'active_il_family' and any(r['resource'] == '000057d4' for r in req['ordered_resources'])):
                for r in req['ordered_resources']:
                    if r['weight'] != 1:
                        changed.append(dict(source=req['source'], resource=r['resource'], old=r['weight'], new=1))
                        r['weight'] = 1
            generated = geometry.populate_source(req, constants)
            assert generated['status'] == 'CONDITIONAL_PLANAR_SOURCE'
            regions.extend(generated['regions'])
            if name == 'exotic_setting_one' and req['source'] == '0:25116:32448:00257f38':
                cu = next(r for r in base if r['source'] == req['source'] and r['resource'] == '000057cf' and r['cell'] == [11, 1])
                il = next(r for r in generated['regions'] if r['resource'] == '000057d4' and any(signature(r) == o['signature'] for o in observed if o['resource'] == '000057d4'))
                blockers = [r for r in generated['regions'] if r['resource'] == '000057d4' and geometry.competition_rejects(cu['points'][0], '000057cf', [r])]
                def gate(cell):
                    from resource_availability import generation_seed
                    rng = geometry.Draws(generation_seed(req['packed_keys'][f'{cell[0]},{cell[1]}'], req['owner_key']))
                    return geometry.mul(rng.uniform(), 100)
                constraint = dict(source=req['source'], il_cell=il['cell'], il_gate=gate(il['cell']),
                                  il_chance=15, baseline_threshold=geometry.mul(.009999999776482582, 15),
                                  copper_cell=cu['cell'],
                                  blockers=[dict(cell=r['cell'], gate=gate(r['cell'])) for r in blockers],
                                  observed_il_alone_rejects_copper=geometry.competition_rejects(cu['points'][0], '000057cf', [il]))
        same = sorted((r['resource'], r['source'], r['cell'], signature(r)) for r in regions) == sorted((r['resource'], r['source'], r['cell'], signature(r)) for r in base)
        if name == 'baseline':
            assert same
        results.append(dict(name=name, independent_justification=justification,
                            changes=changed, path_count=len(regions), exact_frozen_population=same,
                            native_matches=compare(observed, regions),
                            resource_counts={k: sum(r['resource'] == k for r in regions) for k in sorted({r['resource'] for r in base})}))
    out = dict(schema='sor-c1f-offline/1', event_sha256=digest(receipts / 'events.jsonl'),
               freeze_sha256=digest(freeze_path), geometry_sha256=pin['sha256'],
               script_sha256=digest(__file__), analysis_sha256=digest(analysis_path),
               raw_verified=len(samples), comparisons=compare(observed, base), replays=results,
               fixed_input_chance_constraint=constraint,
               observed=[dict(capture=r['capture'], resource=r['resource'],
                              raw_sha256=digest(receipts / f'capture-{r["capture"]:05d}.bin'),
                              source_ordinal=r['row']['source_ordinal'], region_ordinal=r['row']['selected']['ordinal'],
                              geometry_sha256=hashlib.sha256(r['signature']).hexdigest()) for r in observed],
               limits='CONDITIONAL MODEL; not generation identity; native census incomplete; no prediction edits')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('x', encoding='utf8', newline='\n') as f:
        json.dump(out, f, indent=2)
        f.write('\n')
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    run()
