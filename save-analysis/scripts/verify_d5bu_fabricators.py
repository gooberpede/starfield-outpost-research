# SPDX-License-Identifier: GPL-3.0-or-later
"""Finite E3 HIST-0036 producer and upstream checks using the owned E3 method."""
import argparse
from collections import Counter, defaultdict, deque
import csv
import json
from pathlib import Path
import struct
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from d5bt_reader import ROOT, context, disk_guard, pin, require
from inspect_outpost_definitions import esm_records
from research_resource_availability import audit
from validate_mature_outposts import directory, envelopes
from verify_d5bu_controls import crew_extras, decode_member, member_pins
from workshop_population import initial_prefix, typed_records
ESM = (1457098709, '1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7')
TABLES = ROOT / 'docs/experiments/fabricators'

def table(name):
    with (TABLES / name).open(encoding='utf8', newline='') as stream:
        return list(csv.DictReader(stream))

def upstream(start, needed, registry, incoming, classes):
    seen = {start}
    queue = deque([[start]])
    matches = []
    boundaries = Counter()
    cycles = 0
    while queue:
        path = queue.popleft()
        node = path[-1]
        category = classes.get(node, 'unknown')
        keys = registry.get(node, set()) & needed
        if node != start:
            if keys:
                matches.append((path, sorted(keys)))
            elif category in {'storage', 'incoming cargo', 'unknown'}:
                boundaries[category] += 1
        if category == 'incoming cargo':
            continue
        for prior in incoming.get(node, ()):
            if prior in path:
                cycles += 1
            elif prior not in seen:
                seen.add(prior)
                queue.append(path + [prior])
    return (matches, boundaries, cycles)

def graph_control():
    registry = {'local': {'need'}, 'remote': {'need'}, 'decoy': {'different'}}
    incoming = {'consumer': ['store', 'pad', 'decoy'], 'store': ['local', 'consumer'], 'pad': ['remote']}
    classes = {'store': 'storage', 'pad': 'incoming cargo'}
    paths, boundaries, cycles = upstream('consumer', {'need'}, registry, incoming, classes)
    require(paths == [(['consumer', 'store', 'local'], ['need'])] and boundaries == {'storage': 1, 'incoming cargo': 1, 'unknown': 1} and (cycles == 1), 'E3_GRAPH_CONTROL')

def verify(source, esm, output):
    require(pin(esm) == ESM, 'E3_ESM_IDENTITY')
    recipes = {'starfield.esm:' + r['ires'][2:]: r for r in table('recipes.csv')}
    facilities = {'starfield.esm:' + r['formid'][2:]: r for r in table('facilities.csv')}
    esm_pin = ESM
    extra_view = crew_extras.extra_view
    manufactured = {}
    with decode_member(64, source, output.parent, member_pins()) as (data, metrics):
        resolve, _ = context(data)
        groups = []
        registry = defaultdict(set)
        for beacon in audit(data)['beacons']:
            for group in beacon.get('workshop', {}).get('resource_rows', []):
                resource = group['resource_identity']
                for producer in group['rows']:
                    identity, base = producer['reference_identities']
                    registry[identity].add(resource)
                    if resource in recipes:
                        assert identity not in manufactured
                        manufactured[identity] = (resource, base)
                if resource in recipes:
                    groups.append((beacon['identity'], resource))
        assert len(groups) == 14 and len(manufactured) == 17
        env, = [e for e in envelopes(data, directory(data)) if e['qualifies'] and 'parsed' in e]
        incoming = defaultdict(list)
        for group in env['parsed']['groups']:
            for token in group['refs']:
                incoming[resolve(group['key'])].append(resolve(token))
        bases = {}
        selected = {}
        framed = set()
        known = set(incoming) | {x for values in incoming.values() for x in values} | manufactured.keys()
        for record in typed_records(data):
            identity = resolve(record['token'])
            if identity in known:
                framed.add(identity)
            if record['form_type'] != 74 or identity not in known:
                continue
            try:
                prefix = initial_prefix(data, record)
            except (ValueError, struct.error):
                continue
            base = resolve(prefix['base_token']) if prefix['base_token'] else None
            bases[identity] = base
            if identity not in manufactured:
                continue
            resource, expected_base = manufactured[identity]
            av = 'starfield.esm:' + recipes[resource]['av'][2:]
            assert base == expected_base and facilities[base]['preset'] == recipes[resource]['av']
            extra = extra_view(data, record, prefix, resolve)
            assert extra['status'] == 'COUNT_CLOSED', (identity, extra['status'])
            for row in extra['extras']:
                if row['type'] == 'bf':
                    assert all((av not in section['avs'] for section in row['sections']))
            selected[identity] = dict(resource=resource, base=base, av=av, offset=record['offset'], bf=[row['offset'] for row in extra['extras'] if row['type'] == 'bf'])
        assert selected.keys() == manufactured.keys()
    defs = {}
    storage = set()
    want = {int(row['base'].split(':')[1], 16): row['av'] for row in selected.values()}
    for record, fields in esm_records(esm, {b'CONT'}):
        form = record['formid']
        if fields.get(b'EDID', b'').startswith(b'OutpostStorage'):
            storage.add(f'starfield.esm:{form:06x}')
        if form in want:
            values = {k: v for k, v, _ in struct.iter_unpack('<IfI', fields[b'PRPS'])}
            assert values[int(want[form].split(':')[1], 16)] == 1.0
            defs[form] = record['offset']
    assert defs.keys() == want.keys() and pin(esm) == esm_pin
    paths = {}
    cargo = {'starfield.esm:' + x for x in ('100b62', '219173', '2a6c3b')}
    outgoing = {'starfield.esm:' + x for x in ('100b63', '219171', '2a6c3a')}
    classes = {}
    for identity in sorted(framed):
        base = bases.get(identity)
        if base in cargo:
            classes[identity] = 'incoming cargo'
        elif base in outgoing:
            classes[identity] = 'outgoing cargo'
        elif registry[identity]:
            classes[identity] = 'producer'
        elif base in storage:
            classes[identity] = 'storage'
        else:
            classes[identity] = 'unknown'
    cycles = 0
    boundaries = Counter()
    for start, row in selected.items():
        needed = {'starfield.esm:' + v.split(':')[0][2:] for v in recipes[row['resource']]['inputs'].split(';') if v}
        matches, stops, count = upstream(start, needed, registry, incoming, classes)
        boundaries.update(stops)
        cycles += count
        paths[start] = matches
    assert sum(map(len, paths.values())) == 24 and cycles == 0
    assert any((path == ['DYNAMIC:ff01d4e7', 'DYNAMIC:ff05ee43'] for path, _ in paths['DYNAMIC:ff01d4e7']))
    require(len(env['parsed']['groups']) > 0, 'E3_ENVELOPE')
    for identity, start, bf in (('ff01a9f1', 3076059, 3076162), ('ff03107b', 4266093, 4266196), ('ff022310', 3382012, 3382115)):
        row = selected['DYNAMIC:' + identity]
        require(row['offset'] == start and row['bf'] == [bf], 'E3_BF_LOCATORS')
    require(boundaries['storage'] == 53 and boundaries['incoming cargo'] == 29, f'E3_BOUNDARY_COUNTS:{boundaries}')
    endpoint_counts = Counter(classes.values())
    require(endpoint_counts == {'storage': 123, 'producer': 101, 'incoming cargo': 37, 'outgoing cargo': 37, 'unknown': 9}, f'E3_ENDPOINT_COUNTS:{endpoint_counts}')
    graph_control()
    return dict(decoded=metrics['decoded_sha256'], groups=groups, producers=selected, paths=paths, cycles=cycles, definitions=defs, boundary_paths=boundaries, endpoint_classes=endpoint_counts, unframed_endpoint_ids=sorted(known - framed))

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--hist-0036', required=True, type=Path)
    parser.add_argument('--esm', required=True, type=Path)
    parser.add_argument('--receipt', required=True, type=Path)
    args = parser.parse_args()
    require(sys.flags.isolated and sys.dont_write_bytecode and __debug__, 'USE_PYTHON_I_B')
    disk_guard(args.receipt.parent)
    with args.receipt.open('x', encoding='utf8', newline='\n') as stream:
        try:
            result = verify(args.hist_0036, args.esm, args.receipt)
            disk_guard(args.receipt.parent)
            json.dump(result, stream, indent=2, sort_keys=True)
            stream.write('\n')
        except Exception as error:
            json.dump(dict(error=type(error).__name__, detail=str(error)), stream)
            raise
if __name__ == '__main__':
    main()
