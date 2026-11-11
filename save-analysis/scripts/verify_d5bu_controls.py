# SPDX-License-Identifier: GPL-3.0-or-later
"""Explicit-input rereads for D5BU shared fixtures and construction controls."""
import argparse
from collections import Counter
from contextlib import contextmanager
import csv
import inspect
import json
from pathlib import Path
import struct
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from d5bt_reader import ROOT, context, disk_guard, pin, require
from inspect_outpost_definitions import esm_records
from research_workshop_roots import supplement
from stream_save import decoded_save
from test_outpost_record_framing import independent
from validate_mature_outposts import directory
from workshop_inventory import audit, constructed_inventory, ownership_ledger
from workshop_population import initial_prefix, typed_records

sys.path.insert(0, str(ROOT / 'research/historical-methods/b3/cr1-crew'))
import crew_extras

LEDGER = ROOT / 'docs/audits/release-assets-d5bf/release-assets.json'
LEDGER_SHA = '7e0b6bdea0119b86a6cdd9bd0a74ef12b783ef73d4710a4e40aed53a9a652306'
CREW_SHA = 'd97f4680499a76816bd314d0b0aaca41c5d9d109ab236b893f2047291db2d957'
BEACON = 'starfield.esm:2c60e9'
FIXTURE = 'sfbgs00d.esm:02af77'
OWNER = 'starfield.esm:054ba6'
CORE_CONTROLS = (
    (39, 0, None, None), (41, 0, None, None),
    (42, 1, 7, 1295916), (43, 1, 7, 1296522),
    (44, 2, 8, 1297992), (45, 2, 8, 1297602),
    (29, 4, 10, 1298279), (30, 4, 10, 1300997),
    (31, 4, 10, 1299585), (32, 4, 10, 1298829),
    (33, 4, 10, 1299971), (34, 4, 10, 1298332),
    (35, 4, 10, 1300071), (36, 4, 10, 1299654),
    (37, 3, 9, 1297629), (38, 3, 9, 1297586),
)
ROOT_RECEIPTS = (
    (417320665, '229b79deedec274ffd9816e7aee7675e14e5e657c17776930e2085b3b648480c'),
    (226146013, '1b4f69b4e5bfacfcecb91721670def8f9690dde2cc615ff97d55bdaeb37d9086'),
    (956014, 'b4533026f2c933cfe0057927149758964d2d0418c99d57c73d4a7a62b317ab68'),
)
CANONICAL_CONTEXT = (9469, '34972f368f95b671d68bcb0087a9b50619d87cc0f8f2d426eb88d6a5d1dfccb3')
MAIN_ESM = (1457098709, '1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7')
ADDON_ESM = (102054268, '35271d3221310094c70ac2f418d7d393db59dd94d303e830536f85034f44da95')


def member_pins():
    require(pin(LEDGER)[1] == LEDGER_SHA, 'D5BF_LEDGER_IDENTITY')
    assets = json.loads(LEDGER.read_bytes())['assets']
    return {row['identity']: (row['bytes'], row['sha256'])
            for asset in ('B4-F1-CORE', 'B4-F1-ADDENDUM')
            for row in assets[asset]['members'].values()}


@contextmanager
def decode_member(number, source, scratch, pins):
    identity = pins[f'B4-F{number:03}']
    require(pin(source) == identity, 'ORIGINAL_IDENTITY')
    try:
        with decoded_save(source, scratch, guard=disk_guard, seconds=float('inf')) as value:
            yield value
    finally:
        require(pin(source) == identity, 'ORIGINAL_CHANGED')


def fixture_records(data, include_owners):
    resolve, _ = context(data)
    fixtures = []
    beacons = set()
    for record in typed_records(data):
        if record['form_type'] != 0x4a or int(record['token'], 16) >> 22 != 2:
            continue
        queue = {resolve(token) for token in record['refs']}
        if not queue.intersection((BEACON, FIXTURE)):
            continue
        prefix = initial_prefix(data, record)
        base = resolve(prefix['base_token']) if prefix.get('base_token') else None
        identity = resolve(record['token'])
        if base == BEACON:
            beacons.add(identity)
        if base != FIXTURE:
            continue
        require(not record['flags'] & 0x08000020, 'SD2_INVENTORY_BRANCH')
        row = dict(identity=identity, offset=record['offset'], disabled=prefix['disabled'],
                   deleted=prefix['deleted'], inventory='NO_INVENTORY_CHANGE_BRANCH')
        if include_owners:
            view = crew_extras.extra_view(data, record, prefix, resolve)
            require(view['status'] == 'COUNT_CLOSED', 'SD2_COUNTED_EXTRAS')
            link, = [edge for extra in view['extras'] if extra['type'] == '4c'
                     for edge in extra['entries'] if edge['keyword'] == OWNER]
            row.update(owner=link['target'], owner_offset=link['offset'])
        fixtures.append(row)
    if include_owners:
        owners = {row['owner'] for row in fixtures}
        require(len(owners) == len(fixtures) and owners <= beacons, 'SD2_OWNER_COVERAGE')
    return fixtures


def sd2(paths, scratch, pins, addon, esm):
    require(pin(addon) == ADDON_ESM and pin(esm) == MAIN_ESM, 'SD2_DEFINITION_IDENTITY')
    definitions = {}
    for record, _ in esm_records(addon, {b'CONT', b'COBJ'}):
        form = record['formid'] & 0x00ffffff
        if form in (0x02af77, 0x02af79):
            require(form not in definitions, 'SD2_DUPLICATE_DEFINITION')
            definitions[form] = record['type'], record['offset']
    require(definitions == {0x02af77: ('CONT', 266798), 0x02af79: ('COBJ', 100611193)},
            'SD2_DEFINITION_LOCATORS')
    results = {}
    for number, count in ((64, 17), (51, 16), (40, 17), (42, 0)):
        with decode_member(number, paths[number], scratch, pins) as (data, metrics):
            rows = fixture_records(data, number == 64)
            require(len(rows) == count, f'SD2_FIXTURE_COUNT_{number}')
            if number == 64:
                require((rows[0]['identity'], rows[0]['offset']) == ('DYNAMIC:ff01a5a0', 3051921),
                        'SD2_FIRST_FIXTURE')
                require(all(r['disabled'] is False and r['deleted'] is False for r in rows),
                        'SD2_SAVED_FLAGS')
            results[number] = dict(decoded=metrics['decoded_sha256'], fixtures=rows)
    unsupported = bytearray(21)
    unsupported[16:21] = b'\x1b\0\0\0\x98'
    try:
        fixture_records(unsupported, False)
    except ValueError as error:
        require(str(error) == 'UNSUPPORTED_FORMAT_OR_BUFFER', 'SD2_WRONG_REFUSAL')
    else:
        raise ValueError('SD2_UNSUPPORTED_VERSION_ACCEPTED')
    require(pin(addon) == ADDON_ESM and pin(esm) == MAIN_ESM, 'SD2_DEFINITION_CHANGED')
    return dict(members=results, version_control='UNSUPPORTED_FORMAT_OR_BUFFER', definitions=definitions)


def variant_extra_view():
    """Reapply the pinned owned BM1 extension to the unchanged crew grammar."""
    require(pin(Path(crew_extras.__file__))[1] == CREW_SHA, 'BM1_CREW_GRAMMAR_IDENTITY')
    source = inspect.getsource(crew_extras.extra_view)
    dispatch = 'if tag == 0x9c:'
    require(source.count(dispatch) == 1, 'BM1_GRAMMAR_SELECTOR')
    extension = """if tag == 0xb4:
            row['original_base_u32'] = int.from_bytes(c.take(4), 'little')
        elif tag == 0xde:
            row['connections'] = []
            for _ in range(c.count()):
                target = refs(1)[0]
                pairs = [list(struct.unpack('<ii', c.take(8))) for _ in range(c.count())]
                row['connections'].append(dict(target=target, pairs=pairs))
        elif tag == 0x9c:"""
    scope = dict(vars(crew_extras))
    exec(compile(source.replace(dispatch, extension), '<D5BU owned BM1 adaptation>', 'exec'), scope)
    return scope['extra_view']


def variants(data):
    table = ROOT / 'docs/experiments/construction-variants/saved-replacements.csv'
    with table.open(encoding='utf8', newline='') as stream:
        expected = [row for row in csv.DictReader(stream) if row['sample'] == 'HIST-0255']
    view = variant_extra_view()
    resolve, _ = context(data)
    ids = {row[key] for row in expected for key in ('identity', 'replacement_target', 'owner') if row[key]}
    records = {}
    for record in typed_records(data):
        if record['form_type'] != 0x4a:
            continue
        identity = resolve(record['token'])
        if identity not in ids:
            continue
        require(identity not in records, 'BM1_DUPLICATE_IDENTITY')
        prefix = initial_prefix(data, record)
        base = resolve(prefix['base_token']) if prefix.get('base_token') else None
        records[identity] = record, prefix, base
    require(records.keys() == ids, 'BM1_MISSING_IDENTITY')
    result = []
    for oracle in expected:
        identity = oracle['identity']
        record, prefix, base = records[identity]
        target = oracle['replacement_target']
        _, target_prefix, target_base = records[target]
        require(record['offset'] == int(oracle['record_offset']) and base == oracle['base']
                and target_base == oracle['target_base'], 'BM1_BASE_OR_OFFSET')
        require(target_prefix['saved_form_flags'] == int(oracle['target_flags']), 'BM1_TARGET_FLAGS')
        extra = view(data, record, prefix, resolve)
        require(extra['status'] == oracle['body_closure'], 'BM1_EXTRA_CLOSURE')
        links = [e for row in extra['extras'] if row['type'] == '4c' for e in row['entries']]
        edge, = [e for e in links if e['keyword'] == 'starfield.esm:000191' and e['target'] == target]
        require(edge['offset'] == int(oracle['edge_body_offset']), 'BM1_191_OFFSET')
        selected = [item for row in extra['extras'] if row['type'] == 'da'
                    for item in row['references'] if item and item in oracle['selected_packin'].split(';')]
        require(selected == oracle['selected_packin'].split(';'), 'BM1_DA_PACKIN')
        owners = [e['target'] for e in links if e['keyword'] == OWNER]
        require(owners == ([oracle['owner']] if oracle['owner'] else []), 'BM1_OWNER')
        if owners:
            require(records[owners[0]][2] == BEACON, 'BM1_OWNER_BASE')
        result.append(dict(identity=identity, target=target, owner=owners, packin=selected,
                           edge_offset=edge['offset'], target_disabled=target_prefix['disabled'],
                           target_deleted=target_prefix['deleted']))
    return result


def beacon_budget(data, identity, value, offset=None, registrations=None):
    resolve, _ = context(data)
    rows = [r for r in typed_records(data)
            if r['form_type'] == 0x4a and resolve(r['token']) == identity]
    if value is None:
        require(not rows, 'BUDGET_BEACON_ABSENT')
        return None
    record, = rows
    prefix = initial_prefix(data, record)
    require(resolve(prefix['base_token']) == BEACON
            and prefix['disabled'] is False and prefix['deleted'] is False, 'BUDGET_BEACON')
    extra = crew_extras.extra_view(data, record, prefix, resolve)
    require(extra['status'] == 'COUNT_CLOSED', 'BUDGET_COUNTED_EXTRAS')
    selected, = [(section['bits'], row) for entry in extra['extras'] if entry['type'] == 'bf'
                 for section in entry['sections'] for row in section['values']
                 if row['av'] == 'starfield.esm:000399']
    bits, budget = selected
    require(bits == 1 and budget['value'] == value
            and struct.unpack_from('<f', data, budget['offset'])[0] == value, 'BUDGET_VALUE')
    if offset is not None:
        require(budget['offset'] == offset, 'BUDGET_OFFSET')
    if registrations is not None:
        count, = [row['resource_count'] for row in extra['extras'] if row['type'] == 'bc']
        require(count == registrations, 'PLACEMENT_REGISTRATION')
    return dict(value=value, offset=budget['offset'], registrations=registrations)


def placement_oracles():
    folder = ROOT / 'docs/experiments/spatial-placement'
    tables = {}
    for name in ('roots', 'bulldozed'):
        with (folder / f'{name}.csv').open(encoding='utf8', newline='') as stream:
            tables[name] = list(csv.DictReader(stream))
    return tables


def construction(paths, scratch, pins):
    results = {}
    tables = placement_oracles()
    for number, roots, bulldozed, gaps in zip(
        range(11, 17), (0, 1, 3, 0, 1, 3), (0, 1, 4, 0, 1, 12),
        (167, 167, 167, 165, 166, 166), strict=True
    ):
        with decode_member(number, paths[number], scratch, pins) as (data, metrics):
            raw = audit(data)
            d = directory(data)
            arithmetic = independent(data, *d['regions']['region_R3'], d['words'][9])
            require([(r['offset'], r['end'], r['token'], r['change_flags']) for r in raw['records']]
                    == [r[:4] for r in arithmetic], 'PLACEMENT_INDEPENDENT_FRAMING')
            inventory = constructed_inventory(ownership_ledger(raw))
            selected = inventory['constructed_instances']
            resolve, _ = context(data)
            masked = [(resolve(r['token']), r['offset'], r['end'], r['flags'])
                      for r in typed_records(data) if r['form_type'] == 0x4a and r['flags'] & 0x01000000]
            require(len(selected) == roots and len(masked) == bulldozed
                    and raw['coverage'].get('prefix_errors', 0) == gaps, 'PLACEMENT_COUNTS')
            require(all(r['saved_disabled'] is False and r['saved_deleted_bit'] is False for r in selected),
                    'PLACEMENT_ROOT_SAVED_STATE')
            name = f'Save{(30, 31, 33, 34, 35, 36)[number-11]}'
            expected_roots = [r for r in tables['roots'] if r['sample'] == name]
            require({(r['instance_identity'], r['owner_identity'], r['base_identity'],
                      r['construction_definition'], r['record_offset'], r['record_end'],
                      tuple(r['raw_position'])) for r in selected} ==
                    {(r['identity'], r['owner'], r['base'], r['definition'],
                      int(r['record_offset']), int(r['record_end']),
                      (float(r['x']), float(r['y']), float(r['z']))) for r in expected_roots},
                    'PLACEMENT_ROOT_ORACLE')
            require(set(masked) == {(r['identity'], int(r['record_offset']), int(r['record_end']),
                                     int(r['change_mask'], 16))
                                    for r in tables['bulldozed'] if r['sample'] == name},
                    'PLACEMENT_BULLDOZED_ORACLE')
            value = {12: 7, 13: 9, 15: 7, 16: 9}.get(number)
            budget = beacon_budget(data, 'DYNAMIC:ff029ab6' if number <= 13 else 'DYNAMIC:ff041cc1',
                                   value, registrations=int(number in (13, 16)))
            results[number] = dict(decoded=metrics['decoded_sha256'], roots=selected,
                                   bulldozed_rows=masked, prefix_errors=gaps, budget=budget)
    for number, count, value, offset in CORE_CONTROLS:
        with decode_member(number, paths[number], scratch, pins) as (data, metrics):
            inventory = constructed_inventory(ownership_ledger(audit(data)))
            require(len(inventory['constructed_instances']) == count, 'CORE_CONSTRUCTION_ROOTS')
            budget = beacon_budget(data, 'DYNAMIC:ff022c5d', value, offset)
            results[number] = dict(decoded=metrics['decoded_sha256'], roots=count, budget=budget)
    with decode_member(51, paths[51], scratch, pins) as (data, metrics):
        results[51] = dict(decoded=metrics['decoded_sha256'], variant_edges=variants(data))
    return results


def roots(paths, scratch, pins, historical, canonical_path, esm):
    inputs = []
    for path, expected in zip(historical, ROOT_RECEIPTS, strict=True):
        require(pin(path) == expected, 'ROOT_CONTEXT_IDENTITY')
        with path.open('rb') as stream:
            inputs.append(json.load(stream))
    result = supplement(*inputs)
    require(result['source']['sha256'] == pins['B4-F040'][1], 'ROOT_CONTEXT_ORIGINAL_JOIN')
    require((result['baseline_root_count'], len(result['additional_roots']), result['combined_count'])
            == (657, 191, 848), 'ROOT_COUNTS')
    require(not result['population_complete'], 'ROOT_SCOPE')
    require(pin(canonical_path) == CANONICAL_CONTEXT, 'ROOT_CANONICAL_CONTEXT')
    canonical = json.loads(canonical_path.read_bytes())
    unresolved = set(canonical['unknown_canonical_groups'])
    root_ids = {row['instance_identity'] for row in result['combined_roots']}
    require(len(unresolved) == 16 and unresolved.isdisjoint(root_ids)
            and {'DYNAMIC:ff01b59b', 'DYNAMIC:ff05d48a'} <= unresolved, 'ROOT_CANONICAL_EXCLUSIONS')
    require(all(row['extra_flags'] is None for row in result['additional_roots']), 'ROOT_NO_9C_IMPUTATION')
    bases = Counter(int(row['base_identity'].split(':')[1], 16) for row in result['additional_roots'])
    require(pin(esm) == MAIN_ESM, 'ROOT_ESM_IDENTITY')
    classes = Counter()
    for record, _ in esm_records(esm, {b'STAT', b'FURN', b'PKIN'}):
        if record['formid'] in bases:
            classes[record['type']] += bases.pop(record['formid'])
    require(not bases and classes == {'STAT': 51, 'FURN': 89, 'PKIN': 51}, 'ROOT_ADDITION_CLASSES')
    require(pin(esm) == MAIN_ESM and pin(canonical_path) == CANONICAL_CONTEXT, 'ROOT_SUPPORT_CHANGED')
    states = Counter(owner['saved_disabled'] for owner in result['owners'])
    require(states == {False: 17, True: 2}, 'ROOT_OWNER_STATES')
    require({f'DYNAMIC:ff01fa5{suffix}' for suffix in ('b', 'c', 'd')}
            <= root_ids, 'ROOT_CHAIR_IDENTITIES')
    member_tuples = [(member['identity'], member['record_offset'], member['form_type'])
                     for root in result['combined_roots'] for member in root['members']]
    require(len(member_tuples) == 6345, 'ROOT_MEMBER_TUPLE_COUNT')
    roles = Counter(row['role'] for row in result['member_roles'])
    require(roles == {'SINGLE_ROOT': 653, 'PACKIN_ROOT': 195, 'FOUNDATION_MEMBER': 2282,
                      'GENERATED_PACKIN_MEMBER': 5497, 'UNRESOLVED': 1}
            and len(result['unresolved_member_roles']) == 1,
            'ROOT_ROLE_COUNTS')
    expected = {r['instance_identity']: (r['record_offset'], 0x4a) for r in result['combined_roots']}
    for identity, offset, form_type in member_tuples:
        require(identity not in expected or expected[identity] == (offset, form_type),
                'ROOT_MEMBER_CONFLICT')
        expected[identity] = offset, form_type
    typed = {r['identity']: r for r in inputs[1]['references']}
    for row in result['member_roles']:
        identity = row['reference_identity']
        record = typed[identity]
        require(record['form_type'] == 0x4a, 'ROOT_ROLE_TYPE')
        expected[identity] = record['offset'], record['form_type']
    found = {}
    owner_ids = {row['owner_identity'] for row in result['owners']}
    original_owner_states = {}
    with decode_member(40, paths[40], scratch, pins) as (data, metrics):
        resolve, _ = context(data)
        for record in typed_records(data):
            identity = resolve(record['token'])
            if identity in owner_ids:
                prefix = initial_prefix(data, record)
                require(record['form_type'] == 0x4a and resolve(prefix['base_token']) == BEACON,
                        'ROOT_ORIGINAL_OWNER_BASE')
                require(identity not in original_owner_states, 'ROOT_ORIGINAL_OWNER_DUPLICATE')
                original_owner_states[identity] = prefix['disabled']
            if identity in expected:
                require(identity not in found, 'ROOT_ORIGINAL_DUPLICATE')
                found[identity] = record['offset'], record['form_type']
    require(found == expected, 'ROOT_ORIGINAL_TYPED_JOINS')
    require(original_owner_states.keys() == owner_ids
            and Counter(original_owner_states.values()) == {False: 17, True: 2},
            'ROOT_ORIGINAL_OWNER_STATES')
    for path, expected_pin in zip(historical, ROOT_RECEIPTS, strict=True):
        require(pin(path) == expected_pin, 'ROOT_CONTEXT_CHANGED')
    controls = {}
    for number in (42, 43):
        with decode_member(number, paths[number], scratch, pins) as (data, _):
            inventory = constructed_inventory(ownership_ledger(audit(data)))
            control, = inventory['constructed_instances']
            require(control['root_kind'] == 'PACKIN_ROOT', 'ROOT_BEACON_CONTROL')
            controls[number] = control['instance_identity']
    return dict(decoded=metrics['decoded_sha256'], supported=848, member_tuples=member_tuples,
                role_counts=roles, additional_definition_types=classes,
                retained_unresolved_canonical_groups=sorted(unresolved),
                original_beacon_states=original_owner_states, population_complete=False, controls=controls)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('check', choices=('sd2', 'construction', 'roots'))
    parser.add_argument('--member', action='append', nargs=2, required=True, metavar=('ID', 'PATH'))
    parser.add_argument('--receipt', required=True, type=Path)
    parser.add_argument('--root-context', nargs=3, type=Path, metavar=('BASELINE', 'TYPED', 'ALLA'))
    parser.add_argument('--canonical-context', type=Path)
    parser.add_argument('--esm', type=Path)
    parser.add_argument('--addon', type=Path)
    args = parser.parse_args()
    require(sys.flags.isolated and sys.dont_write_bytecode and __debug__, 'USE_PYTHON_I_B')
    paths = {int(number): Path(path).resolve(strict=True) for number, path in args.member}
    expected = {'sd2': {40, 42, 51, 64},
                'construction': {*range(11, 17), 51, *(row[0] for row in CORE_CONTROLS)},
                'roots': {40, 42, 43}}[args.check]
    require(paths.keys() == expected and len(set(paths.values())) == len(args.member), 'MEMBER_SELECTION')
    require(all((path is not None) == (args.check == 'roots')
                for path in (args.root_context, args.canonical_context)), 'ROOT_CONTEXT_SELECTION')
    require((args.esm is not None) == (args.check in {'roots', 'sd2'})
            and (args.addon is not None) == (args.check == 'sd2'), 'DEFINITION_SELECTION')
    disk_guard(args.receipt.parent)
    with args.receipt.open('x', encoding='utf8', newline='\n') as stream:
        try:
            checks = {'sd2': sd2, 'construction': construction, 'roots': roots}
            context_paths = {'sd2': [args.addon, args.esm], 'construction': [],
                             'roots': [args.root_context, args.canonical_context, args.esm]}
            result = checks[args.check](paths, args.receipt.parent, member_pins(), *context_paths[args.check])
        except Exception as error:
            json.dump(dict(error=type(error).__name__, detail=str(error)), stream)
            raise
        json.dump(result, stream, indent=2)
        stream.write('\n')


if __name__ == '__main__':
    main()
