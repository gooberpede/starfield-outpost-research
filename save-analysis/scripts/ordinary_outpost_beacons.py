"""SPDX-License-Identifier: GPL-3.0-or-later
Scoped offline beacon detector, schema 1.0. Reads decoded bytes/catalog only;
no I/O, dependencies, raw payload output or target effects. Reuses project
SOR-EXP-0009/0010 readers; native/content basis SOR-S-0127/0128. Ownership and
complete enumeration are separate, unresolved questions. See SOR-EXP-0011.
"""
from collections import Counter
from outpost_membership import classify

SCHEMA = 'ordinary-outpost-beacons/1.0'
STATES = ('EXPLICITLY_CLEAR', 'EXPLICITLY_SET', 'OMITTED', 'UNRESOLVED')
CATEGORIES = ('ordinary', 'exceptional/faction', 'unresolved beacon-like')


def catalog_for(b, definitions):
    """Direct vanilla identity is fixed to Starfield.esm 002C60E9.
    Additional full-plugin mapping is an R1/template lead only. Regex plugin
    sequence is not a validated save plugin table or an override merger.
    """
    import re
    plugins = [x.decode('ascii') for x in
               re.findall(rb'[A-Za-z0-9_ -]+\.(?:esm|esp|esl)', b[:8192])]
    catalog = dict(direct_bases={0x2c60e9: 'OutpostBeaconActivator'}, templates={})
    for name, definition in definitions.items():
        if name not in plugins or plugins.index(name) > 0xfd:
            continue
        slot = plugins.index(name)
        for d in definition['definitions']:
            catalog['direct_bases'][(slot << 24) | (d['formid'] & 0xffffff)] = d['editor_id']
        for t in definition['templates']:
            catalog['templates'][(slot << 24) | (t['formid'] & 0xffffff)] = (
                slot << 24) | (t['base_formid'] & 0xffffff)
    return catalog, plugins


def summarize(decoded, catalog):
    """Expose positive evidence without changing the old membership result."""
    return report(classify(decoded, catalog, diagnostics=True))


def report(raw):
    candidates = []
    for r in raw['candidates']:
        p = r.get('prefix', {})
        # A successfully consumed case-5 prefix and repeated self are required.
        # An unsupported later extra does not invalidate already read flags.
        direct = p.get('case') == 5 and p.get('base_token') is not None
        fid = r.get('base_formid') if direct else None
        ordinary = direct and fid == 0x2c60e9
        faction = direct and r.get('identity_label') in (
            'OutpostBeaconActivatorFC', 'OutpostBeaconActivatorRI', 'OutpostBeaconActivatorUC')
        category = 'ordinary' if ordinary else 'exceptional/faction' if faction else 'unresolved beacon-like'
        state = ('OMITTED' if p and not r['flags'] & 1 else
                 'EXPLICITLY_SET' if p.get('disabled') is True else
                 'EXPLICITLY_CLEAR' if p.get('disabled') is False else 'UNRESOLVED')
        candidates.append(dict(
            category=category,
            category_confidence='STRONG_SCOPED_PROPOSED' if ordinary else 'PROVISIONAL',
            category_basis='CONSUMED_INLINE_BASE_AND_SELF' if direct else 'TEMPLATE_ADJACENCY_LEAD',
            sources=['SOR-F-0014', 'SOR-F-0015', 'SOR-S-0127', 'SOR-S-0128'],
            location=dict(domain='DECODED_LOGICAL_STREAM', region='R3',
                record_index=r.get('ordinal'), record_start=r['offset'], record_end=r['end'],
                body_start=r['body'], reference_queue_start=r.get('reference_start'),
                string_queue_start=r.get('string_start')),
            saved_reference_token=r['token'], reference_domain='TAGGED_SAVE_TOKEN_BEFORE_LOAD_REMAP',
            raw_base_token=p.get('base_token'), saved_base_formid=fid,
            esm_base_identity='Starfield.esm:002C60E9' if ordinary else None,
            base_mapping_basis='DIRECT_OR_ONE_BASED_FORM_ARRAY; NOT_LOAD_REMAP' if direct else None,
            type_basis=r['type_basis'], explicit_type=r['explicit_type'],
            initial_case=p.get('case'), change_flags=r['flags'],
            disabled_state=state, disabled_mask=0x800,
            saved_form_flags=p.get('saved_form_flags'), saved_aux_flags=p.get('saved_aux_flags'),
            saved_flags_logical_offset=p.get('saved_flags_offset'),
            disabled_basis='CHANGE_BIT_0; LE_U32_FORM_AND_U16_AUX; STATIC_RESTORE_MASK_00D12960',
            interpretation=f'{category}: saved disabled {state}',
            player_membership='INDETERMINATE', template_leads=r.get('template_leads', []),
            gaps=([r['decode_error']] if 'decode_error' in r else []) +
                ['INHERITED_TYPE_CONDITIONAL' if r['explicit_type'] is None else 'LOAD_AUTHORITY_UNVALIDATED',
                 'REGISTRATION_AND_OWNERSHIP_NOT_ESTABLISHED'] +
                ([] if direct else ['R1_ADJACENCY_NOT_A_RESOLVED_BASE']),
            extra_stop_reason=r.get('extra_prefix', {}).get('stop_reason')))
    included = {r['saved_reference_token'] for r in candidates}
    # Known-base reference occurrences alone are inspectable leads, never matches.
    for r in raw.get('reference_leads', []):
        if r['token'] in included:
            continue
        candidates.append(dict(category='unresolved beacon-like', category_confidence='PROVISIONAL',
            category_basis='KNOWN_BASE_REFERENCE_OCCURRENCE_ONLY',
            saved_reference_token=r['token'], location=dict(domain='DECODED_LOGICAL_STREAM',
                region='R3', record_index=r['ordinal'], record_start=r['offset'],
                record_end=r['end'], body_start=r['body']),
            disabled_state='UNRESOLVED', disabled_mask=0x800, saved_form_flags=None,
            saved_aux_flags=None, raw_base_token=None, saved_base_formid=None,
            player_membership='INDETERMINATE', reference_occurrences=r['occurrences'],
            change_flags=r['flags'], explicit_type=r['explicit_type'],
            interpretation='Reference occurrence does not establish beacon identity',
            gaps=['BASE_POSITION_NOT_VALIDATED'], sources=['SOR-F-0014']))
    counts = {cat: {state: 0 for state in STATES} for cat in CATEGORIES}
    for r in candidates:
        counts[r['category']][r['disabled_state']] += 1
    n = sum(counts['ordinary'].values())
    return dict(schema=SCHEMA, headline='RECOGNIZED_ORDINARY_BEACONS' if n else
        'NO_RECOGNIZED_ORDINARY_BEACONS', ordinary_count=n, counts=counts,
        authoritative_player_membership='INDETERMINATE', candidates=candidates,
        rejected=raw['rejected'], coverage=dict(raw['coverage'],
            profile='BCPS1/R3-QUEUES/CONDITIONAL-REFR-4-7',
            ordinary_identification='CASE5_INLINE_Starfield.esm_002C60E9_AND_SELF',
            complete_ordinary_enumeration=False),
        reason_codes=raw['reason_codes'])


def compact(result):
    return f"{result['headline']}: {result['ordinary_count']} ordinary; " + ', '.join(
        f'{state}={n}' for state, n in result['counts']['ordinary'].items())
