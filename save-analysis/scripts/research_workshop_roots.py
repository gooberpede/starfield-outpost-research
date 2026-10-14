"""SPDX-License-Identifier: GPL-3.0-or-later
Supplement a preserved inventory with independently typed, closed single roots.
Reads explicit project receipts; writes an exclusive ignored rework directory.
Stdlib/project only, C/D40GB guards; no target/save/database/network/Git effects.
Does not certify population completeness. See workshop-population/schema.md.
"""
import argparse
import collections
import copy
import csv
import json
from pathlib import Path
from inventory_historical_saves import ROOT, guard, identity
from workshop_population import additional_single


def supplement(baseline, typed, quest_context):
    if baseline['source'] != typed['source']:
        raise ValueError('SAMPLE_IDENTITY_MISMATCH')
    if not typed['independent_framing'] or typed['population_complete']:
        raise ValueError('TYPED_AUDIT_CONTEXT')
    lookup = {r['identity']: r for r in typed['references']}
    if len(lookup) != len(typed['references']):
        raise ValueError('DUPLICATE_TYPED_IDENTITY')
    rows = baseline['instances'] + baseline['unresolved_population']
    counts = collections.Counter(r['saved_reference'] for r in rows)
    by_id = {r['saved_reference']: r for r in rows}
    roots = copy.deepcopy(baseline['constructed_instances'])
    roles = copy.deepcopy(baseline['member_roles'])
    additional = []
    for role in roles:
        if role['reason'] != 'EXTRA_FLAGS_OMITTED_DEFAULT_UNKNOWN':
            continue
        row = by_id[role['reference_identity']]
        actual = lookup[row['saved_reference']]
        if actual['form_type'] != 0x4a or actual['offset'] != row['offset']:
            raise ValueError('ACTUAL_REFERENCE_TYPE_OR_OFFSET')
        root = additional_single(row, counts)
        additional.append(root)
        role.update(role='SINGLE_ROOT', root_identity=root['instance_identity'],
                    reason=root['reason'])
    # Only the three relevant keys are excluded; other alias metadata is retained.
    forbidden = {'starfield.esm:054ba6', 'starfield.esm:000191', 'starfield.esm:000192'}
    if quest_context['schema'] != 'global-installed-quest-alla/1':
        raise ValueError('QUEST_CONTEXT_SCHEMA')
    if any(r['keyword'] in forbidden and r['count'] for r in quest_context['keyword_counts']):
        raise ValueError('ALIAS_KEY_REQUIRES_RESEARCH')
    for role in roles:
        if role['reason'] != 'ALTERNATE80_POSSIBLE_GROUP_CONTEXT_ONLY':
            continue
        row = by_id[role['reference_identity']]
        x = row['linked_prefix']
        group = role.get('group_identity')
        matches = [r for r in roots if r['instance_identity'] == group]
        if x['following_extras'] != 'CLOSED' or len(matches) != 1:
            raise ValueError('ALIAS_MEMBER_GROUP_UNQUALIFIED')
        if any(e['keyword_identity'] in {'starfield.esm:000191', 'starfield.esm:000192'} for e in x['entries']):
            raise ValueError('ALIAS_MEMBER_RELATION_INPUT')
        role.update(role='GENERATED_PACKIN_MEMBER', root_identity=group,
                    reason='QUEST_ALIAS_KEYS_EXCLUDED_EXISTING_DA_GROUP')
        root = matches[0]
        if row['saved_reference'] not in root['member_identities']:
            root['member_identities'].append(row['saved_reference'])
            root['member_offsets'].append(row['offset'])
    if {r['instance_identity'] for r in roots} & {r['instance_identity'] for r in additional}:
        raise ValueError('BASELINE_ROOT_COLLISION')
    roots = sorted(roots + additional, key=lambda r: (r['owner_identity'], r['instance_identity']))
    for root in roots:
        actual = lookup[root['instance_identity']]
        if actual['form_type'] != 0x4a or actual['offset'] != root['record_offset']:
            raise ValueError('ROOT_TYPE_OR_OFFSET')
        root['legacy_record_type_field'] = root.get('record_type')
        root.update(form_type=actual['form_type'], record_type=actual['form_type'],
                    record_type_name='REFR', buffer_version=153,
                    buffer_version_override=actual['buffer_version_override'])
        root['members'] = [dict(identity=mid, record_offset=lookup[mid]['offset'],
                                form_type=lookup[mid]['form_type'])
                           for mid in sorted(root['member_identities'])]
    owners = copy.deepcopy(baseline['owners'])
    for owner in owners:
        oid = owner['owner_identity']
        owner['supported_constructed_roots'] = sum(r['owner_identity'] == oid for r in roots)
        owner['root_role_counts'] = dict(collections.Counter(r['role'] for r in roles if r.get('owner_identity') == oid))
        owner['completeness'] = 'POPULATION_NOT_ESTABLISHED'
    return dict(schema='workshop-root-rework/2', source=baseline['source'],
                population_complete=False, baseline_root_count=len(baseline['constructed_instances']),
                additional_roots=additional, combined_roots=roots, combined_count=len(roots),
                member_roles=roles, owners=owners,
                unresolved_member_roles=[r for r in roles if r['role'] == 'UNRESOLVED'],
                coverage='Positive roots and all prior member roles; nonowner alternatives are a separate candidate ledger')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--baseline', type=Path, required=True)
    ap.add_argument('--typed', type=Path, required=True)
    ap.add_argument('--quest-context', type=Path, required=True)
    ap.add_argument('--run', required=True)
    a = ap.parse_args()
    if not a.run.isascii() or not a.run.replace('-', '').isalnum():
        raise ValueError('RUN_NAME')
    guard()
    paths = [a.baseline, a.typed, a.quest_context]
    pins = [identity(p) for p in paths]
    result = supplement(*(json.loads(p.read_text(encoding='utf8')) for p in paths))
    if [identity(p) for p in paths] != pins:
        raise ValueError('INPUT_CHANGED')
    result['input_receipts'] = pins
    out = ROOT / '.local-work/workshop-population-rework' / a.run
    out.mkdir(exist_ok=False)
    (out / 'inventory.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf8')
    for name, rows, keys in [
        ('roots.csv', result['combined_roots'], ['instance_identity','owner_identity','base_identity','construction_definition','root_kind','editor_name','record_offset','record_end','saved_disabled','saved_deleted_bit','reason']),
        ('owners.csv', result['owners'], ['owner_identity','state','saved_disabled','saved_deleted_bit','direct_member_records','supported_constructed_roots','completeness'])]:
        with (out / name).open('x', encoding='utf8', newline='') as f:
            w = csv.DictWriter(f, fieldnames=keys, extrasaction='ignore', lineterminator='\n')
            w.writeheader(); w.writerows(rows)
    print(result['baseline_root_count'], '+', len(result['additional_roots']), '=', result['combined_count'])
    guard()
