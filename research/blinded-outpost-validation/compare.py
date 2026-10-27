# SPDX-License-Identifier: GPL-3.0-or-later
"""Fixed offline comparison of sealed alternatives and authenticated revelation.

Pure functions; CLI reads two explicit JSON files and emits stdout. The gate
authenticates bytes before calling this module. No target, network or writes.
Geometry is the complete ordered accepted-region sequence for each source;
area intersection alone is never ordinary Workshop admission. Stdlib only.
"""
import sys
import json
from bridge import exact, hexword, f32, integer, validate


def regions(rows):
    if type(rows) is not list:
        raise ValueError('REGION_LIST')
    for row in rows:
        exact(row, 'resource points_le bound_le')
        hexword(row['resource'], 8)
        raw = row['points_le']
        if type(raw) is not str or len(raw) % 32:
            raise ValueError('POINT_ARITY')
        values = f32(raw, len(raw)//8)
        bounds = f32(row['bound_le'], 4)
        if bounds[3] < 0 or any(x < 0 for x in values[3::4]):
            raise ValueError('NEGATIVE_WIDTH_OR_RADIUS')
    return rows


def sourcekey(value):
    if type(value) is not str:
        raise ValueError('SOURCE_KEY')
    parts = value.split(':')
    if len(parts) != 4:
        raise ValueError('SOURCE_KEY')
    for text, low, high in zip(parts[:3], (0, 0, 0), (1, 49151, 49151)):
        if not text.isascii() or not text.isdigit() or str(int(text)) != text:
            raise ValueError('SOURCE_ENCODING')
        integer(int(text), low, high)
    hexword(parts[3], 8)
    return value


def resource_set(values):
    if type(values) is not list or len(set(values)) != len(values):
        raise ValueError('RESOURCE_SET')
    for value in values:
        hexword(value, 8)
    return values


def validate_prediction(p):
    if p.get('schema') == 'sor-blind-prediction/1':
        exact(p, 'schema trial body body_formid workshop location classification reason sources presence special_helium3 terrestrial_water atmospheric scope_complete')
        validate(p['location'])
        if any(p[k] != p['location'][k] for k in ('trial', 'body', 'body_formid', 'workshop')):
            raise ValueError('LOCATION_IDENTITY')
        if (p['classification'] != 'UNSUPPORTED' or p['sources'] != [] or p['presence'] != {} or
            p['scope_complete'] is not False or p['reason'] != 'MISSING_EFFECTIVE_WORKSHOP_FRAME_AND_COMPLETE_CANDIDATE_CORPUS' or
            any(p[k] != 'UNKNOWN' for k in ('special_helium3', 'terrestrial_water', 'atmospheric'))):
            raise ValueError('UNSUPPORTED_PREDICTION_FIELDS')
        return p
    exact(p, 'schema trial body body_formid workshop session epoch scope_complete sources')
    if p['schema'] != 'sor-blind-comparable/1' or p['body'] not in ('Kreet', 'Vectera', 'Jemison', 'SYNTHETIC', 'HISTORICAL'):
        raise ValueError('PREDICTION_VERSION')
    for key, length in (('trial', 32), ('workshop', 16), ('body_formid', 8), ('session', 32), ('epoch', 32)):
        hexword(p[key], length)
    if type(p['scope_complete']) is not bool or type(p['sources']) is not list:
        raise ValueError('PREDICTION_SCOPE')
    keys = []
    for source in p['sources']:
        exact(source, 'source alternatives')
        keys.append(sourcekey(source['source']))
        if type(source['alternatives']) is not list or not source['alternatives']:
            raise ValueError('ALTERNATIVES_REQUIRED')
        for alternative in source['alternatives']:
            exact(alternative, 'mask regions presence')
            integer(alternative['mask'], 0, 15)
            regions(alternative['regions'])
            resource_set(alternative['presence'])
        masks = [a['mask'] for a in source['alternatives']]
        if masks != sorted(set(masks)):
            raise ValueError('ALTERNATIVE_ORDER')
    if len(set(keys)) != len(keys):
        raise ValueError('DUPLICATE_SOURCE')
    return p


def validate_truth(t):
    exact(t, 'schema trial body body_formid workshop session epoch oracle complete sources')
    if t['schema'] != 'sor-blind-truth/1' or t['oracle'] not in ('ORDINARY_WORKSHOP_TRANSFER', 'SYNTHETIC_WORKSHOP_TRANSFER'):
        raise ValueError('UNQUALIFIED_ORACLE')
    if type(t['complete']) is not bool or type(t['sources']) is not list:
        raise ValueError('TRUTH_COMPLETENESS')
    if t['oracle'] == 'ORDINARY_WORKSHOP_TRANSFER' and t['complete']:
        raise ValueError('UNQUALIFIED_NATIVE_CENSUS')
    # Reuse identity and sequence validation without interpreting a winner.
    projected = {k: t[k] for k in ('trial', 'body', 'body_formid', 'workshop', 'session', 'epoch')}
    sources = []
    for source in t['sources']:
        exact(source, 'source regions presence')
        sources.append(dict(source=source['source'], alternatives=[dict(mask=0, regions=source['regions'], presence=source['presence'])]))
    validate_prediction(dict(projected, schema='sor-blind-comparable/1', scope_complete=t['complete'], sources=sources))
    for source in t['sources']:
        if any(r['resource'] not in source['presence'] or not r['points_le'] for r in source['regions']):
            raise ValueError('INCONSISTENT_ACCEPTED_REGION_TRUTH')
    return t


def compare(p, t):
    validate_prediction(p)
    validate_truth(t)
    if p['schema'] == 'sor-blind-prediction/1':
        mismatch = [k for k in ('trial', 'body', 'body_formid', 'workshop') if p[k] != t[k]]
        return dict(protocol='ACQUISITION_FAILURE' if mismatch else 'UNSUPPORTED_PREDICTION',
            scientific='UNKNOWN', identity_mismatches=mismatch, sources=[],
            accuracy_is_acceptance_criterion=False)
    identity = [k for k in ('trial', 'body', 'body_formid', 'workshop', 'session', 'epoch') if p[k] != t[k]]
    if identity or (t['oracle'].startswith('SYNTHETIC') and t['body'] != 'SYNTHETIC'):
        return dict(protocol='ACQUISITION_FAILURE', identity_mismatches=identity,
                    scientific='UNKNOWN', sources=[])
    pp = {s['source']: s for s in p['sources']}
    tt = {s['source']: s for s in t['sources']}
    rows = []
    for key in sorted(pp.keys() | tt.keys()):
        if key not in pp or key not in tt:
            rows.append(dict(source=key, result='UNMODELED' if key not in pp else 'GROUND_TRUTH_MISSING',
                             alternatives=[]))
            continue
        actual = tt[key]
        if not t['complete']:
            partial = []
            positives = set(actual['presence'])
            for a in pp[key]['alternatives']:
                observed = [dict(observed_ordinal=i, resource=r['resource'],
                    exact_predicted_ordinals=[j for j, expected in enumerate(a['regions']) if r == expected])
                    for i, r in enumerate(actual['regions'])]
                partial.append(dict(mask=a['mask'], observed_regions=observed,
                    all_observed_included=all(r['exact_predicted_ordinals'] for r in observed) if observed else None,
                    observed_presence_admitted=sorted(positives & set(a['presence'])),
                    observed_presence_unpredicted=sorted(positives - set(a['presence'])),
                    admission_all_observed_included=positives <= set(a['presence']) if positives else None))
            presence = {}
            resources = sorted(positives | {v for a in pp[key]['alternatives'] for v in a['presence']})
            for resource in resources:
                count = sum(resource in a['presence'] for a in pp[key]['alternatives'])
                presence[resource] = dict(modeled=('ALL_ALTERNATIVES' if count == len(partial)
                    else 'SOME_ALTERNATIVES' if count else 'NONE_WITHIN_QUALIFIED_SCOPE' if p['scope_complete'] else 'UNKNOWN'),
                    observed='PRESENT' if resource in positives else 'UNKNOWN')
            rows.append(dict(source=key, result='INCOMPLETE_ACQUISITION',
                observed_positive_resources=actual['presence'], geometry_exact=None,
                absence='UNKNOWN', alternatives=partial, presence=presence))
            continue
        comparisons = []
        for a in pp[key]['alternatives']:
            expected = a['regions']
            per_region = []
            for i in range(max(len(expected), len(actual['regions']))):
                left = expected[i] if i < len(expected) else None
                right = actual['regions'][i] if i < len(actual['regions']) else None
                if left is None or right is None:
                    per_region.append(dict(ordinal=i, exact=False, reason='MISSING_OR_EXTRA_REGION'))
                else:
                    per_region.append(dict(ordinal=i, exact=left == right,
                        fields_differ=[k for k in left if left[k] != right[k]]))
            comparisons.append(dict(mask=a['mask'], geometry_exact=expected == actual['regions'],
                region_comparisons=per_region,
                presence_missing=sorted(set(a['presence']) - set(actual['presence'])),
                presence_unpredicted=sorted(set(actual['presence']) - set(a['presence']))))
        included = [a['mask'] for a in comparisons if a['geometry_exact'] and not a['presence_missing'] and not a['presence_unpredicted']]
        resources = sorted(set(actual['presence']) | {v for a in pp[key]['alternatives'] for v in a['presence']})
        presence = {}
        for resource in resources:
            count = sum(resource in a['presence'] for a in pp[key]['alternatives'])
            presence[resource] = dict(modeled=('ALL_ALTERNATIVES' if count == len(comparisons)
                else 'SOME_ALTERNATIVES' if count else 'NONE_WITHIN_QUALIFIED_SCOPE' if p['scope_complete'] else 'UNKNOWN'),
                observed=('PRESENT' if resource in actual['presence'] else 'NOT_ADMITTED_WITHIN_COMPLETE_SCOPE' if t['complete'] else 'UNKNOWN'))
        rows.append(dict(source=key, result='INCLUDED_ALTERNATIVE' if included else 'DISCREPANCY',
            included_masks=included, alternatives=comparisons, presence=presence))
    return dict(schema='sor-blind-comparison/1',
        protocol='COMPARABLE' if t['complete'] else 'INCOMPLETE_ACQUISITION',
        scientific='CORRESPONDENCE_REPORTED' if t['complete'] else
            'PARTIAL_POSITIVE_CORRESPONDENCE' if any(s['presence'] or s['regions'] for s in t['sources']) else 'UNKNOWN_NO_POSITIVES',
        prediction_scope_complete=p['scope_complete'], truth_scope_complete=t['complete'], sources=rows,
        accuracy_is_acceptance_criterion=False)


if __name__ == '__main__':
    from bridge import loads
    with open(sys.argv[1], encoding='utf8') as stream:
        prediction = loads(stream.read())
    with open(sys.argv[2], encoding='utf8') as stream:
        truth = loads(stream.read())
    print(json.dumps(compare(prediction, truth), sort_keys=True, allow_nan=False))
