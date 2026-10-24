# SPDX-License-Identifier: GPL-3.0-or-later
"""Freeze installed component and owner-map predictions before witness reads.

Reads pinned installed EXE/ESM/PlanetData identities, owned planetary methods,
label-free D3 body requests and STATIC exports. Writes exclusive ignored JSON.
No saves, D4D receipt/event files, target, network, database or Git writes.
"""
import argparse
import datetime
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / 'research' / p) for p in
               ('resource-standalone', 'resource-owner-root')]
import builder
from owner_map import reconstruct, ordinary_candidates
from audit import pin, write
from components import components


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    out = args.output.resolve()
    assert out.is_relative_to(ROOT / '.local-work/resource-slot-provenance')
    out.mkdir(exist_ok=False)
    inputs = {builder.ESM: builder.DEFINITION, builder.EXE: builder.EXE_HASH,
              builder.ARCHIVE: builder.ARCHIVE_HASH}
    inputs.update({builder.OWNED / n: h for n, h in builder.OWNED_PINS.items()})
    assert all(pin(p) == h for p, h in inputs.items())
    requests = ROOT / '.local-work/resource-save52-d3/requests-v1.json'
    inputs[requests] = pin(requests)
    records = {h['formid']: (h, fs) for h, fs in builder.esm_records(builder.ESM,
        {b'PNDT', b'BIOM', b'RSGD', b'IRES'}, repeated=True)}
    bodies = sorted({item['request']['body'] for item in json.loads(requests.read_text())
                     if item['request']})
    rarities = {fid: builder.last(fs, b'SNAM')[0] for fid, (h, fs) in records.items()
                if h['type'] == 'IRES'}
    predictions = {}
    for body in bodies:
        rows = components(records, builder.selections(records, int(body, 16)))
        result = reconstruct(rows)
        predictions[body] = dict(components=rows, map=result,
            candidates={str(root): ordinary_candidates(root, result['maps'], rarities)
                        for root in result['maps']})
    write(out / 'prediction-v1.json', predictions)
    methods = [Path(__file__), Path(__file__).with_name('components.py'),
               ROOT / 'research/resource-owner-root/owner_map.py',
               ROOT / 'research/resource-standalone/builder.py']
    static = ROOT / '.local-work/workshop-population-rework/specialist/d4e-slots03.tsv'
    assert static.read_bytes().rstrip().endswith(b'END')
    inputs[static] = pin(static)
    write(out / 'freeze-v1.json', dict(time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        schema='sor-d4e-component-prediction/1',
        inputs={str(p): h for p, h in inputs.items()},
        methods={str(p): pin(p) for p in methods},
        outputs={'prediction-v1.json': pin(out / 'prediction-v1.json')},
        primary_d4d_answers_read=False,
        prior_knowledge='Expected answers disclosed in brief/reports; researcher is not blind',
        scope='Installed main-file initialization and BIOM-key creation route; historical epoch unknown'))
    assert all(pin(p) == h for p, h in inputs.items())
    print(json.dumps(dict(bodies=len(bodies), freeze_sha256=pin(out / 'freeze-v1.json'))))


if __name__ == '__main__':
    main()
