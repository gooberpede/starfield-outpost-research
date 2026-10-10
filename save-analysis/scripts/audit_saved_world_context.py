"""SPDX-License-Identifier: GPL-3.0-or-later
Original EXP0020 bounded unit-3 context audit. Reads frozen durable-center
receipt, explicit archived-source map and its frozen hash manifest; decodes only
those saves using the original project streaming decoder. Writes selected
numeric context CSV and preservation receipts to one NEW ignored directory.
Stdlib/project modules only; 40GB C:/D: guard, existing decoder resource bounds,
exact source/decoded hash checks. No source/target/database/network/Git effects.
The source map only selects inputs; frozen manifests and decoded hashes qualify
them. Existing unit-4 framing is reused, not established by this audit.
"""
import argparse
import json
import struct
from pathlib import Path

from audit_durable_center import table
from inventory_historical_saves import guard, identity
from inspect_outpost_definitions import esm_records
from planet_world_key import find_unit3_context, unit3_world_descriptors
from stream_save import decoded_save
from saved_world_components import find_world_components
from validate_mature_outposts import directory


def main():
    parser = argparse.ArgumentParser()
    for name in ('samples', 'source-map', 'before', 'esm', 'output'):
        parser.add_argument('--'+name, type=Path, required=True)
    args = parser.parse_args()
    guard(args.output.parent)
    inputs = [args.samples, args.source_map, args.before, args.esm]
    receipts_before = [identity(p) for p in inputs]
    if receipts_before[-1]['sha256'] != '1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7':
        raise ValueError('PINNED_ESM_HASH')
    bodies = {}
    for record, fields in esm_records(args.esm, {b'PNDT'}):
        gnam = fields.get(b'GNAM', b'')
        if len(gnam) == 12:
            system, orbital, index = struct.unpack('<3I', gnam)
            bodies[f"{record['formid']:08X}"] = (system, index)
    samples = json.loads(args.samples.read_text(encoding='utf8'))
    sources = json.loads(args.source_map.read_text(encoding='utf8'))
    frozen = json.loads(args.before.read_text(encoding='utf8'))
    args.output.mkdir(exist_ok=False)
    rows, worlds, components, protected = [], [], [], []
    body_keys = {key: body for body, key in bodies.items()}
    for label, source in sources.items():
        matches = [s for s in samples if s['label'] == label]
        if len(matches) != 1:
            raise ValueError('SAMPLE_NOT_UNIQUE')
        sample = matches[0]
        path = Path(source)
        prior = identity(path)
        if prior['sha256'] != frozen[str(path)]['sha256']:
            raise ValueError('SOURCE_HASH')
        with decoded_save(path, args.output/'scratch') as (buffer, metadata):
            if metadata['decoded_sha256'] != sample['metrics']['decoded_sha256']:
                raise ValueError('DECODED_HASH')
            layout = directory(buffer)
            start, end = layout['regions']['region_R1']
            unit4 = sample['extraction']['global_units']['4'][0]-8
            if not start < unit4 < end:
                raise ValueError('UNIT4_OUTSIDE_R1')
            context = find_unit3_context(buffer, start, unit4)
            descriptors, tail = unit3_world_descriptors(buffer, context)
            for descriptor in descriptors:
                expected = bodies.get(descriptor['body'])
                if expected != (descriptor['system_id'], descriptor['body_index']):
                    raise ValueError('DESCRIPTOR_INSTALLED_BODY_MISMATCH')
                descriptor['installed_identity_equal'] = True
            worlds.extend(dict(sample=label, **r) for r in descriptors)
            parents = {int(r['prefix']['parent_token'], 16) for r in sample['rows']}
            if parents:
                region = sample['extraction']['global_units']['6']
                run = find_world_components(buffer, *region, parents, body_keys, descriptors)
                components.extend(dict(sample=label, **r) for r in run['rows'])
                component_count = len(run['rows'])
                component_start, component_end = run['start'], run['end']
            else:
                component_count, component_start, component_end = 0, None, None
            rows.append(dict(sample=label, decoded_sha256=metadata['decoded_sha256'],
                             world_components=component_count, component_start=component_start,
                             component_end=component_end,
                             descriptors=len(descriptors), descriptor_end=tail, **context))
        after = identity(path)
        if prior != after:
            raise ValueError('SOURCE_CHANGED')
        protected.append(dict(before=prior, after=after))
        guard(args.output)
    if receipts_before != [identity(p) for p in inputs]:
        raise ValueError('RECEIPT_CHANGED')
    table(args.output/'saved-world-context.csv', rows)
    table(args.output/'saved-world-descriptors.csv', worlds)
    table(args.output/'saved-world-components.csv', components)
    receipt = dict(inputs=receipts_before, protected=protected, examples=len(rows),
                   descriptors=len(worlds), distinct_bodies=len({r['body'] for r in worlds}),
                   all_installed_identities_equal=True,
                   scoped_world_components=len(components),
                   scope='Scoped unit-3 packed context only; no continuous position or universal frame selection')
    (args.output/'receipt.json').write_text(json.dumps(receipt, indent=2)+'\n', encoding='utf8')
    print('Qualified saved world contexts:', len(rows))


if __name__ == '__main__':
    main()
