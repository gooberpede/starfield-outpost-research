# SPDX-License-Identifier: GPL-3.0-or-later
"""Verify the v2 Workshop projection against explicit CORE originals and main ESM."""
import argparse
from collections import Counter
import copy
import json
from pathlib import Path
import struct
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from d5bt_reader import context, disk_guard, pin
from d5bx_workshop_archive import HABS, KEYWORDS, OWNER_KEY, canonical_da_groups, encoded, quest_operand, read_archive, require
from inspect_outpost_definitions import esm_records
from research_workshop_roots import supplement
from verify_d5bu_controls import BEACON, MAIN_ESM, ROOT, decode_member, fixture_records, member_pins
from workshop_inventory import audit, constructed_inventory, linked_prefix, ownership_ledger
from workshop_population import initial_prefix, typed_records
from workshop_population_extras import partial_extras

ASSETS = ROOT / 'research/evidence-data/evidence-access-d5bx/assets.json'


def check_alla_keywords(pairs):
    object_ids = {int(key.split(':')[1], 16) for key in KEYWORDS}
    require(all(row['keyword'] not in KEYWORDS and row['keyword_raw'] & 0xffffff not in object_ids
                for row in pairs), 'ALLA_FORBIDDEN_KEY')


def check_definitions(esm, result, alla):
    extra_bases = Counter(row['base_identity'] for row in result['additional_roots'])
    require(all(key.startswith('starfield.esm:') for key in extra_bases), 'SUPPLEMENT_NAMESPACE')
    require(alla['schema'] == 'global-installed-quest-alla/1', 'ALLA_SCHEMA')
    require(pin(esm) == MAIN_ESM, 'ROOT_ESM_IDENTITY')
    census = alla['census']
    require(len(census) == 38 and sum(row['quest_variants'] for row in census.values()) == alla['quest_variants']
            and sum(row['aliases'] for row in census.values()) == alla['alias_definitions'], 'ALLA_CENSUS')
    pairs = alla['pairs']
    require(Counter(row['plugin'].casefold() for row in pairs) ==
            Counter({plugin: row['ALLA_pairs'] for plugin, row in census.items()}), 'ALLA_PAIR_CENSUS')
    check_alla_keywords(pairs)
    definitions = [definition for root in result['combined_roots'] for definition in root['definition_provenance']]
    main = {(row['record_type'], row['formid']): row for row in definitions if row['plugin'].casefold() == 'starfield.esm'}
    wanted = {kind.encode('ascii') for kind, _ in main} | {b'QUST', b'STAT', b'FURN', b'PKIN'}
    classes, esm_pairs = Counter(), Counter()
    quest_records = aliases = 0
    for record, fields in esm_records(esm, wanted, repeated=True):
        if record['type'] != 'QUST':
            classes[record['type']] += extra_bases.pop(f"starfield.esm:{record['formid']:06x}", 0)
            definition = main.pop((record['type'], record['formid']), None)
            if definition:
                require((record['offset'], record['flags']) == (definition['offset'], definition['flags']),
                        'ROOT_MAIN_DEFINITION')
            continue
        quest_records += 1
        alias = None
        for tag, raw in fields:
            if tag in {b'ALST', b'ALLS'}:
                require(alias is None and len(raw) == 4, 'ALLA_ALIAS_START')
                alias, = struct.unpack('<I', raw)
                aliases += 1
            if tag == b'ALED':
                require(alias is not None and not raw, 'ALLA_ALIAS_END')
                alias = None
            if tag == b'ALLA':
                require(alias is not None, 'ALLA_OUTSIDE_ALIAS')
                esm_pairs.update((record['offset'], record['formid'], alias, word, target)
                                 for word, target in struct.iter_unpack('<II', raw))
        require(alias is None, 'ALLA_ALIAS_CLOSURE')
    main_pairs = [row for row in pairs if row['plugin'].casefold() == 'starfield.esm']
    require(all(row['keyword'] == (f"starfield.esm:{row['keyword_raw']:06x}" if row['keyword_raw'] else None)
                for row in main_pairs), 'ALLA_MAIN_NAMESPACE')
    require(esm_pairs == Counter((row['record_offset'], row['formid'], row['alias_id'], row['keyword_raw'], row['target_alias_id'])
                                 for row in main_pairs), 'ALLA_MAIN_PAIRS')
    require((quest_records, aliases) == (census['starfield.esm']['quest_variants'], census['starfield.esm']['aliases']),
            'ALLA_MAIN_RECORDS')
    require(not extra_bases and +classes == {'STAT': 51, 'FURN': 89, 'PKIN': 51}, 'ROOT_ADDITION_CLASSES')
    require(not main, 'ROOT_MAIN_DEFINITION_COVERAGE')
    require(pin(esm) == MAIN_ESM, 'ROOT_ESM_CHANGED')
    return {k: classes[k] for k in ('FURN', 'STAT', 'PKIN')}, dict(
        main_records=quest_records, main_aliases=aliases, main_pairs=esm_pairs.total(), projected_pairs=len(pairs),
        installed_census_replayed=False, excluded_keys=sorted(KEYWORDS),
        definition_provenance_by_plugin=Counter(row['plugin'] for row in definitions))


def replay_baseline(base):
    definitions = {r['construction_definition']: r['definition_provenance'] for r in base['constructed_instances']}
    rerun = constructed_inventory(dict(instances=base['instances'], unresolved_population=base['unresolved_population'],
                                       owners=copy.deepcopy(base['owners']), coverage={}), dict(records=definitions))
    for key in ('constructed_instances', 'member_roles', 'owners'):
        require(rerun[key] == base[key], f'BASELINE_REPLAY_{key}')


def check_canonical(base, typed, ledger, roots):
    unresolved = set(ledger['unknown_canonical_groups'])
    dispositions = Counter(row['disposition'] for row in ledger['rows'])
    require(dispositions == {'EXISTING_SUPPORTED_ROOT': 6, 'TYPE5_SHIP_SOURCE_MAPPING_NOT_ORDINARY_ROOT': 1,
                             'REPLACED_DUMMY_CANONICAL_HAB_GROUP_NOT_EXTRA_ROOT': 8,
                             'RETAINED_SOURCE_GROUP_PHYSICAL_ROOT_AND_OWNER_UNRESOLVED': 16}, 'CANONICAL_PARTITION')
    rows = base['instances'] + base['unresolved_population']
    by_id = {row['saved_reference']: row for row in rows}
    require(all((row['group_identity'] in roots) == (row['disposition'] == 'EXISTING_SUPPORTED_ROOT')
                for row in ledger['rows']), 'CANONICAL_ROOT_PARTITION')
    group_ids = {row['group_identity'] for row in ledger['rows']}
    counts = Counter(group for row in typed['canonical_da'] for group in canonical_da_groups(row['extras'], group_ids))
    require(counts == {row['group_identity']: row['retained_DA_member_records'] for row in ledger['rows']},
            'CANONICAL_DA_COUNT_JOIN')
    habs = {}
    for group in sorted(HABS):
        require(group not in by_id and group in unresolved, 'HAB_GROUP_REPRESENTATIVE')
        members = {row['saved_reference'] for row in base['unresolved_population']
                   if any(da['identities'][3] == group for da in row.get('linked_prefix', {}).get('packin', []))}
        require(len(members) == 4, 'HAB_DA_MEMBERS')
        replacements = {}
        for row in ledger['rows']:
            if row['canonical_group'] != group or row['group_identity'] == group:
                continue
            dummy = by_id[row['group_identity']]
            extras = dummy['linked_prefix']
            require(dummy['prefix']['disabled'] is True and extras['following_extras'] == 'CLOSED'
                    and dummy.get('owner_identity') is None
                    and all(e['keyword_identity'] != OWNER_KEY for e in extras['entries']), 'HAB_DUMMY_STATE')
            targets = [e['target_identity'] for e in extras['entries'] if e['keyword_identity'] == 'starfield.esm:000191']
            require(len(targets) == 1 and targets[0] in members, 'HAB_DUMMY_REPLACEMENT')
            replacements[row['group_identity']] = targets[0]
        require(set(replacements.values()) == members, 'HAB_REPLACEMENT_COVERAGE')
        for identity in members:
            wall = by_id[identity]
            require(wall['linked_prefix']['following_extras'] == 'CLOSED' and wall.get('owner_identity') is None
                    and all(edge['keyword_identity'] != OWNER_KEY
                            for edge in wall['linked_prefix']['entries']), 'HAB_WALL_OWNER_SCOPE')
        habs[group] = replacements
    gaps = {row['saved_reference']: row['linked_prefix']['following_gap'] for row in base['unresolved_population']
            if row.get('linked_prefix', {}).get('following_extras') == 'NOT_DECODED'}
    require(gaps == {'DYNAMIC:ff03fb72': 'EXTRA_EA_UNSUPPORTED', 'DYNAMIC:ff05ccc5': 'EXTRA_EA_UNSUPPORTED'},
            'BASELINE_UNSUPPORTED_EXTRAS')
    return dict(habs=habs, unsupported=gaps, partition=dispositions, nonowner_da_counts=counts)


def resolved_extras(extras, resolve, alias_key):
    for edge in extras['entries']:
        edge['keyword_identity'] = resolve(edge['keyword_token'])
        edge['target_identity'] = resolve(edge['target_token'])
    for alias in extras['alternate_groups']:
        alias[alias_key] = resolve(alias['base_token'])
    for packin in extras['packin']:
        packin['identities'] = [resolve(token) for token in packin['tokens']]
    return extras


def read_original(data, typed, rows, owner_rows, ledger):
    resolve, _ = context(data)
    lookup = {row['identity']: row for row in typed['references']}
    require(len(lookup) == len(typed['references']), 'DUPLICATE_TYPED_IDENTITY')
    da_rows = {row['identity']: row for row in typed['canonical_da']}
    require(len(da_rows) == len(typed['canonical_da']) and da_rows.keys() <= lookup.keys(), 'CANONICAL_DA_SELECTION')
    group_presence = {row['group_identity']: row['own_R3_present'] for row in ledger['rows']}
    present = set()
    expected_rows = {(row['saved_reference'], row['offset']): row for row in rows}
    require(len(expected_rows) == len(rows), 'DUPLICATE_BASELINE_ROW')
    owners = {row['owner_identity']: row for row in owner_rows}
    found, states, replayed = set(), {}, set()
    for record in typed_records(data):
        identity = resolve(record['token'])
        if identity in group_presence:
            present.add(identity)
        row = lookup.get(identity)
        if row:
            require(identity not in found and all(record[key] == row[key] for key in
                    ('offset', 'form_type', 'buffer_version_override')), 'ORIGINAL_TYPED_JOIN')
            found.add(identity)
        selected = (identity, record['offset'])
        if selected not in expected_rows and identity not in owners and identity not in da_rows:
            continue
        prefix = initial_prefix(data, record)
        if identity in da_rows:
            da = da_rows[identity]
            base = resolve(prefix['base_token']) if prefix['base_token'] else None
            if record['form_type'] != 0x4b and record['flags'] & 0x80:
                base = resolve(record['refs'][prefix['next_reference_index']]) or base
            extras = resolved_extras(partial_extras(data, record, prefix), resolve, 'quest_identity')
            require((record['end'], prefix['case'], base) == (da['end'], da['case'], da.get('base_identity'))
                    and extras == da['extras'], 'ORIGINAL_CANONICAL_DA')
        if identity in owners:
            owner = owners[identity]
            require(identity not in states and record['form_type'] == 0x4a and resolve(prefix['base_token']) == BEACON
                    and (prefix['disabled'], prefix['deleted'], record['offset'], record['token']) ==
                    (owner['saved_disabled'], owner['saved_deleted_bit'], owner['offset'], owner['token']), 'ORIGINAL_BEACON')
            states[identity] = prefix['disabled']
        if selected not in expected_rows:
            continue
        row = expected_rows[selected]
        require(record['end'] == row['end'] and record['token'] == row['token'] and
                record['buffer_version_override'] == row['explicit_type'], 'ORIGINAL_ROW_FRAME')
        replayed.add(selected)
        if 'linked_prefix' not in row:
            continue
        require(prefix == row['prefix'] and (resolve(prefix['base_token']) if prefix['base_token'] else None)
                == row.get('base_identity'), 'ORIGINAL_ROW_PREFIX')
        extras = resolved_extras(linked_prefix(data, record, prefix), resolve, 'base_identity')
        require(extras == row['linked_prefix'], 'ORIGINAL_ROW_EXTRAS')
        targets = {edge['target_identity'] for edge in extras['entries']
                   if edge['keyword_identity'] == OWNER_KEY and edge['target_mode'] == 0}
        if row.get('owner_identity') is not None:
            require(targets == {row['owner_identity']} and targets <= owners.keys(), 'ORIGINAL_OWNER_EDGE')
    require(found == lookup.keys() and replayed == expected_rows.keys(), 'ORIGINAL_JOIN_COVERAGE')
    require(states.keys() == owners.keys() and Counter(states.values()) == {False: 17, True: 2}, 'ORIGINAL_OWNER_COVERAGE')
    require(present == {group for group, is_present in group_presence.items() if is_present}, 'ORIGINAL_CANONICAL_PRESENCE')
    return states


def verify(projected, ledger, paths, esm, scratch):
    base, typed, alla = (projected[key] for key in ('baseline', 'typed', 'alla'))
    replay_baseline(base)
    result = supplement(base, typed, quest_operand(alla))
    pins = member_pins()
    require(result['source'] == dict(zip(('size', 'sha256'), pins['B4-F040'], strict=True)), 'ORIGINAL_SOURCE_JOIN')
    require((result['baseline_root_count'], len(result['additional_roots']), result['combined_count']) == (657, 191, 848)
            and result['population_complete'] is False, 'ROOT_COUNTS_AND_SCOPE')
    require(all(row['extra_flags'] is None for row in result['additional_roots']), 'OMITTED_9C')
    root_ids = {row['instance_identity'] for row in result['combined_roots']}
    unresolved = set(ledger['unknown_canonical_groups'])
    require(len(root_ids) == 848 and len(unresolved) == 16 and unresolved.isdisjoint(root_ids)
            and HABS <= unresolved and {'DYNAMIC:ff01fa5b', 'DYNAMIC:ff01fa5c', 'DYNAMIC:ff01fa5d'} <= root_ids,
            'ROOT_IDENTITY_EXCLUSIONS')
    exclusions = check_canonical(base, typed, ledger, root_ids)
    tuples = [(row['identity'], row['record_offset'], row['form_type'])
              for root in result['combined_roots'] for row in root['members']]
    require(len(tuples) == 6345, 'ROOT_TUPLE_COUNT')
    counts = Counter(row['role'] for row in result['member_roles'])
    require(counts == {'SINGLE_ROOT': 653, 'PACKIN_ROOT': 195, 'FOUNDATION_MEMBER': 2282,
                       'GENERATED_PACKIN_MEMBER': 5497, 'UNRESOLVED': 1}, 'ROOT_ROLE_COUNTS')
    types = {row['identity']: row['form_type'] for row in typed['references']}
    require(all(types[row['reference_identity']] == 0x4a for row in result['member_roles']), 'ROLE_TYPE')
    classes, alias = check_definitions(esm, result, alla)
    with decode_member(40, paths[40], scratch, pins) as (data, metrics):
        states = read_original(data, typed, base['instances'] + base['unresolved_population'], result['owners'], ledger)
        fixtures = fixture_records(data, False)
        require(len(fixtures) == 17, 'F040_FIXTURE_COUNT')
        rows = {row['saved_reference']: row for row in base['instances']}
        for fixture in fixtures:
            row = rows[fixture['identity']]
            require(row['offset'] == fixture['offset'] and states[row['owner_identity']] is False, 'F040_FIXTURE_OWNER')
            fixture['owner'] = row['owner_identity']
        require(len({row['owner'] for row in fixtures}) == 17, 'F040_DISTINCT_FIXTURE_OWNERS')
    controls = {}
    for number in (42, 43):
        with decode_member(number, paths[number], scratch, pins) as (data, _):
            control, = constructed_inventory(ownership_ledger(audit(data)))['constructed_instances']
            require(control['root_kind'] == 'PACKIN_ROOT', 'ROOT_BEACON_CONTROL')
            controls[number] = control['instance_identity']
    selected = dict(decoded=metrics['decoded_sha256'], supported=848, member_tuples=tuples, role_counts=counts,
                    additional_definition_types=classes, retained_unresolved_canonical_groups=sorted(unresolved),
                    original_beacon_states=states, population_complete=False, controls=controls)
    return dict(d5bu=selected, normalized_supplement=result, alias=alias, fixtures=fixtures,
                canonical=ledger, exclusions=exclusions)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--member', action='append', nargs=2, required=True, metavar=('ID', 'PATH'))
    for name in ('archive', 'esm', 'receipt'):
        parser.add_argument('--' + name, required=True, type=Path)
    args = parser.parse_args()
    require(sys.flags.isolated and sys.dont_write_bytecode and __debug__, 'USE_PYTHON_I_B')
    paths = {int(number): Path(path).resolve(strict=True) for number, path in args.member}
    require(paths.keys() == {40, 42, 43} and len(set(paths.values())) == len(args.member), 'MEMBER_SELECTION')
    disk_guard(args.receipt.parent)
    asset = json.loads(ASSETS.read_bytes())['workshop']
    expected = asset['bytes'], asset['sha256']
    require(pin(args.archive) == expected, 'ARCHIVE_IDENTITY')
    with args.archive.open('rb') as stream:
        projected, ledger = read_archive(stream, asset['members'])
    result = verify(projected, ledger, paths, args.esm, args.receipt.parent)
    require(pin(args.archive) == expected, 'ARCHIVE_CHANGED')
    disk_guard(args.receipt.parent)
    with args.receipt.open('xb') as stream:
        stream.write(encoded(result))


if __name__ == '__main__':
    main()
