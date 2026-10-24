# SPDX-License-Identifier: GPL-3.0-or-later
"""Freeze an installed-data conditional map before reading native answers.

Reads pinned EXE/ESM/PlanetData, owned selection modules and frozen label-free
D3 requests. Writes exclusive local inputs/trace and their hashes. No native
call/geometry receipts are opened. Family-to-slot projection is an explicit
unvalidated hypothesis, never a replacement corpus or a complete native map.
"""
import argparse
import datetime
import json
from pathlib import Path
import struct
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'research/resource-standalone'))
import builder
from owner_map import reconstruct, ordinary_candidates
from audit import pin, write


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    out = args.output.resolve()
    assert out.is_relative_to(ROOT / '.local-work')
    out.mkdir(parents=True, exist_ok=False)
    required = {builder.ESM: builder.DEFINITION, builder.EXE: builder.EXE_HASH,
                builder.ARCHIVE: builder.ARCHIVE_HASH}
    required.update({builder.OWNED / n: h for n, h in builder.OWNED_PINS.items()})
    for p, expected in required.items():
        assert pin(p) == expected, p
    requests = ROOT / '.local-work/resource-save52-d3/requests-v1.json'
    required[requests] = pin(requests)
    records = {h['formid']: (h, fs) for h, fs in builder.esm_records(builder.ESM,
        {b'PNDT', b'BIOM', b'RSGD', b'IRES'}, repeated=True)}
    owner = 0x0005de4c
    prediction = builder.selections(records, owner)
    rows = []
    for v in prediction.biome_results:
        biome = int(str(v.orchestration.biome.form_id), 16)
        family = v.common_assignment.family
        # This is the tested hypothesis, not a claim that all native fields are
        # derivable from a cached family. Unmodeled slots remain named below.
        slots = [0]*6
        if family:
            for ref in family.emitted_descendants:
                fid = int(str(ref.form_id), 16)
                rarity = builder.last(records[fid][1], b'SNAM')[0]
                assert 1 <= rarity <= 4
                slots[rarity-1] = fid
        rows.append(dict(identity=f'{biome:08x}', biome=biome,
                         root=int(str(family.root.form_id), 16) if family else 0,
                         slots=slots, status='HYPOTHETICAL_FAMILY_SLOT_PROJECTION',
                         installed_order=v.orchestration.biome.index,
                         rsgd=str(v.orchestration.effective_rsgd.form_id),
                         selected_special=str(v.orchestration.special_selection.form_id)
                         if v.orchestration.special_selection else None,
                         everywhere=[str(e.resource_form_id) for e in v.orchestration.effective_rsgd.entries
                                     if e.resource_rarity.value == 'Everywhere'],
                         record_header=records[biome][0]))
    rows.sort(key=lambda r: r['biome'])
    root = next(r['root'] for r in rows if r['biome'] == 0x0028acd1)
    result = reconstruct(rows)
    rarities = {fid: builder.last(fs, b'SNAM')[0] for fid, (h, fs) in records.items()
                if h['type'] == 'IRES'}
    candidates = ordinary_candidates(root, result['maps'], rarities)
    source = dict(owner=owner, selected_biome=0x0028acd1, selected_root=root,
                  source='0:27156:35988:0028be0d', components=rows,
                  input_basis='Installed main-file selection; empty atmosphere occupancy',
                  first_missing_operand=dict(record='0007d721', container_offset='0x74',
                    payload_offset='0x54', value='UNKNOWN',
                    reason='No qualified mapping from installed selection to all six native slot words'))
    write(out / 'inputs-v1.json', source)
    write(out / 'map-v1.json', result)
    write(out / 'candidates-v1.json', dict(**candidates,
          complete_native_sequence='UNKNOWN', special_call_sequence='UNKNOWN',
          family_projection_only=True))
    write(out / 'freeze-v1.json', dict(time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        inputs={str(p): h for p, h in required.items()},
        methods={str(p): pin(p) for p in (Path(__file__), Path(__file__).with_name('owner_map.py'),
                 ROOT / 'research/resource-standalone/builder.py')},
        outputs={p.name: pin(p) for p in out.glob('*.json')},
        primary_call_answers_read=False,
        prior_knowledge='Question, expected resource names and order disclosed in invoked brief and required D4A/D4B reports; researcher is not blind',
        status='FROZEN_CONDITIONAL_HYPOTHESIS_WITH_FIRST_MISSING_OPERAND'))
    assert all(pin(p) == expected for p, expected in required.items())
    print(json.dumps(dict(candidates=candidates, freeze=pin(out / 'freeze-v1.json'))))


if __name__ == '__main__':
    main()
