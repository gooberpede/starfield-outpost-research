# SPDX-License-Identifier: GPL-3.0-or-later
"""Build the v2 Workshop projection from four explicitly supplied pinned files."""
import argparse
from collections import Counter
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from d5bt_reader import disk_guard, pin
from d5bx_workshop_archive import (CANONICAL, HABS, SCHEMA, SOURCE_PINS, canonical_da_groups, encoded,
                                   quest_operand, require, write_archive)
from research_workshop_roots import supplement

ROW_FIELDS = ('saved_reference', 'token', 'owner_identity', 'base_identity', 'offset', 'end',
              'explicit_type', 'reason', 'association_status', 'definition_provenance',
              'editor_name', 'prefix', 'linked_prefix', 'linked_gap', 'prefix_error')
TYPED_FIELDS = ('identity', 'offset', 'form_type', 'buffer_version_override')
CANONICAL_FIELDS = ('identity', 'end', 'case', 'base_identity', 'extras')
PAIR_FIELDS = ('plugin', 'record_offset', 'formid', 'alias_id', 'keyword', 'keyword_raw', 'target_alias_id')


def fields(row, names):
    return {key: row[key] for key in names if key in row}


def project(baseline, typed, alla, ledger):
    require(baseline['source'] == typed['source'], 'SOURCE_CONTEXT_MISMATCH')
    roles = baseline['member_roles']
    roots = baseline['constructed_instances']
    owners = baseline['owners']
    selected = {row['reference_identity'] for row in roles}
    selected.update(root['instance_identity'] for root in roots)
    selected.update(member for root in roots for member in root['member_identities'])
    selected.update(owner['owner_identity'] for owner in owners)
    canonical_groups = {row['group_identity'] for row in ledger['rows']}
    canonical_groups.update(HABS)

    def control(row):
        extras = row.get('linked_prefix', {})
        return (extras.get('following_extras') == 'NOT_DECODED'
                or row.get('saved_reference') in canonical_groups
                or any(canonical_groups.intersection(entry['identities']) for entry in extras.get('packin', [])))

    for row in baseline['unresolved_population']:
        if control(row):
            selected.add(row['saved_reference'])
    base = dict(source=fields(baseline['source'], ('size', 'sha256')), constructed_instances=roots,
                member_roles=roles, owners=owners)
    for key in ('instances', 'unresolved_population'):
        base[key] = [fields(row, ROW_FIELDS) for row in baseline[key] if row.get('saved_reference') in selected]
    # Reject duplicates across the full typed population before reducing it.
    require(len({row['identity'] for row in typed['references']}) == len(typed['references']), 'DUPLICATE_TYPED_IDENTITY')
    canonical_da = [fields(row, CANONICAL_FIELDS) for row in typed['references']
                    if canonical_da_groups(row.get('extras') or {}, canonical_groups)]
    typed_ids = selected | {row['identity'] for row in canonical_da} | canonical_groups
    records = [fields(row, TYPED_FIELDS) for row in typed['references'] if row['identity'] in typed_ids]
    type_view = dict(source=base['source'], independent_framing=typed['independent_framing'],
                     population_complete=typed['population_complete'], references=records, canonical_da=canonical_da)
    pairs = [fields(row, PAIR_FIELDS) for row in alla['links']]
    counts = Counter(row['keyword'] for row in pairs)
    require(counts == {row['keyword']: row['count'] for row in alla['keyword_counts']}
            and len(pairs) == alla['ALLA_pairs'], 'SOURCE_ALLA_PAIR_CLOSURE')
    quest = dict(schema=alla['schema'], pairs=pairs, census=alla['census'], quest_variants=alla['quest_variants'],
                 alias_definitions=alla['alias_definitions'])
    return dict(schema=SCHEMA, baseline=base, typed=type_view, alla=quest)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('baseline', 'typed', 'alla', 'canonical', 'archive', 'fidelity'):
        parser.add_argument('--' + name, required=True, type=Path)
    args = parser.parse_args()
    require(sys.flags.isolated and sys.dont_write_bytecode and __debug__, 'USE_PYTHON_I_B')
    inputs = (args.baseline, args.typed, args.alla, args.canonical)
    pins = (*SOURCE_PINS, CANONICAL)
    free = disk_guard(args.archive.parent)
    disk_guard(args.fidelity.parent)
    require(tuple(map(pin, inputs)) == pins, 'ORIGINAL_INPUT_IDENTITY')
    original = []
    for path in inputs[:3]:
        with path.open('rb') as stream:
            original.append(json.load(stream))
    ledger = args.canonical.read_bytes()
    projected = project(*original, json.loads(ledger))
    reference = supplement(*original)
    reference['source'] = projected['baseline']['source']
    derived = supplement(projected['baseline'], projected['typed'], quest_operand(projected['alla']))
    require(derived == reference, 'FULL_SUPPLEMENT_COMPARISON')
    require(tuple(map(pin, inputs)) == pins, 'ORIGINAL_INPUT_CHANGED')
    final_free = disk_guard(args.archive.parent)
    payload = encoded(projected)
    with args.archive.open('xb') as stream:
        write_archive(stream, payload, ledger)
    with args.fidelity.open('xb') as stream:
        stream.write(encoded(dict(source_pins=pins, before_free=free, after_free=final_free,
                                  exact_normalized_supplement=reference, archive=pin(args.archive))))


if __name__ == '__main__':
    main()
