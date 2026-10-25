# SPDX-License-Identifier: GPL-3.0-or-later
"""Join frozen D5A results to existing identity/provenance after prediction freeze.

Reads authored tables and owned saved/installed manifests, not raw screenshots
or extractor outcomes. Writes exclusive authored metadata CSV and local hashes.
Stdlib only; no target, Git, network or protected-input writes. This is original
join/report code; provenance for imported arithmetic is in sources.csv.
"""
import csv
import io
import json
from pathlib import Path
from analyze import ROOT, DOC, LOCAL, pin, write


def table(name, rows):
    """Permit exact-byte recovery of tables flushed before a metadata failure."""
    stream = io.StringIO(newline='')
    writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator='\n')
    writer.writeheader()
    writer.writerows(rows)
    data = stream.getvalue().encode('utf8')
    path = DOC / name
    if path.exists():
        assert path.read_bytes() == data, path
    else:
        with path.open('xb') as target:
            target.write(data)


def main():
    inventory_path = ROOT / '.local-work/resource-save52/inventory-v2.json'
    manifest_path = ROOT / '.local-work/resource-save52/build-v1/manifest.json'
    inventory = {v['case']: v for v in json.loads(inventory_path.read_text())['cases']}
    lineage = json.loads(manifest_path.read_text())['lineage']
    cases = list(csv.DictReader((DOC / 'cases.csv').open(encoding='utf8')))
    results = json.loads((LOCAL / 'conditional-results.json').read_text())
    identities, matrix = [], []
    for s in cases:
        saved = inventory[s['case']]
        assert saved['workshop_id'] == s['workshop_bytes'] and saved['body'] == s['body']
        assert not saved['disabled'] and not saved['deleted'] and saved['registered']
        chart, x, y, _ = s['source_key'].split(':')
        rows = [r for r in lineage if r['body'] == s['body'] and r['tile'] == [int(chart), int(x)//192, int(y)//192]]
        assert len(rows) == 1 and rows[0]['sfpt'] == s['sfpt']
        identities.append(dict(case=s['case'], source_key=s['source_key'], sftr=rows[0]['sftr'],
            saved_beacon_token=saved['token'], saved_frame=f"0x{saved['frame']:x}",
            saved_descriptor_key=saved['descriptor_key'], saved_record_offset=saved['record_offset'],
            offset_domain=saved['offset_domain'], workshop_bytes=saved['workshop_id'],
            site_cell=';'.join(map(str, saved['site_cell'])),
            qualification=saved['coordinate_qualification']))
        variants = [r for r in results if r['source'] == s['source_key']]
        a, b = variants
        changed = [x['resource'] for x, y in zip(a['summaries'], b['summaries']) if x['weight'] != y['weight']]
        path = lambda v: ';'.join(f"{r['resource']}:{r['paths']}" for r in v['summaries'])
        area = lambda v: ';'.join(f"{r['resource']}:{r['positive_area_paths']}" for r in v['summaries'])
        matrix.append(dict(case=s['case'], source_key=s['source_key'], masks=f"{a['mask']};{b['mask']}",
            changed_weight_resources=';'.join(changed), paths_a=path(a), paths_b=path(b),
            positive_area_paths_a=area(a), positive_area_paths_b=area(b),
            footprint_discrimination='PATH_COUNTS' if area(a) != area(b) else 'NONE_IN_FOOTPRINT',
            missing_operand='FIRST_QUERY_AND_EFFECTIVE_FRAME;SAMPLED_MASK;CURRENT_WORKSHOP_JOIN',
            falsifier='Opposite mask rejects this invocation branch; wrong weight/order rejects conditional installed projection; outside masks rejects neighborhood coverage'))
    table('identity-context.csv', identities)
    table('discrimination.csv', matrix)
    preferred = {'0:37536:20928:0029d20e': 'PRIMARY_CONDITIONAL',
                 '0:29568:10932:0006ce58': 'FALLBACK',
                 '1:38112:960:0029d211': 'DEFERRED_CANONICAL_ALTERNATIVE'}
    table('feasibility.csv', [dict(case=s['case'], source_key=s['source_key'],
        preference=preferred.get(s['source_key'], 'COMPARISON_ONLY' if s['context'].startswith('COMPARISON') else 'LOWER_FOOTPRINT_VALUE'),
        hypothesis_discrimination=matrix[i]['footprint_discrimination'],
        identity_binding='SAVED_QUALIFIED;CURRENT_WORKSHOP_JOIN_MISSING',
        natural_construction='UNKNOWN;LOAD_TRAVEL_BUILD_MAY_REUSE_CACHE',
        control='FOUR_SAME_BODY_NATIVE_CONTROLS_AT_OTHER_SITE' if s['case'] == 'D2-84e101' else 'SAVED_CONFIGURATION;NO_EXACT_NATIVE_SOURCE_CONTROL',
        operational_scope='11_PRODUCER_SITES_ROTATED_IN_FOUR_SLOTS;FOUR_CONSUMER_SITES_IN_LATER_PHASE',
        receipt_scope='COMPLETE_CALLS_AND_VISITED_ALTERNATES;BYTE_TOTAL_UNKNOWN',
        teardown='REPAIRED_TERMINAL_FOUNDATION;COMBINED_PATH_UNQUALIFIED',
        historical_confound='SOURCE_REPORTED_LIFECYCLE_SEPARATE' if s['case'] == 'D2-844cc6' else 'NO_SITE_SPECIFIC_INCIDENT_ESTABLISHED') for i, s in enumerate(cases)])
    paths = [inventory_path, manifest_path,
        ROOT / '.local-work/resource-feynman-d5/inputs-v2.json',
        ROOT / '.local-work/resource-feynman-d5/build04/normalized.json',
        ROOT / '.local-work/resource-feynman-d5/build04/preparation.json',
        ROOT / '.local-work/resource-feynman-d5/targets-v1.json',
        ROOT / '.local-work/screengrabs/screengrabs-feynman.zip']
    paths += [ROOT / 'research' / p for p in ('resource-slot-provenance/predictor_d4e.py',
        'resource-geometry/geometry.py', 'resource-geometry/context.py',
        'resource-feynman-d5/inputs.py', 'resource-feynman-d5/source_gate.py', 'resource-feynman-d5/collect.py',
        'resource-feynman-d5/validate.py', 'resource-feynman-d5/audit.py', 'resource-feynman-d5/package.py')]
    # The imported context module's actual path is the provenance authority.
    import context
    paths = [p for p in paths if p.name != 'context.py'] + [Path(context.__file__)]
    paths += [ROOT / 'save-analysis/scripts' / name for name in
              ('resource_spatial.py', 'resource_availability.py')]
    table('sources.csv', [dict(path=str(p.relative_to(ROOT)), bytes=p.stat().st_size,
        sha256=pin(p), use='Owned prior method or protected local evidence; see report provenance',
        eligibility='LOCAL-ONLY payload' if '.local-work' in p.parts else 'REVIEW-REQUIRED owned source') for p in paths])
    receipt = dict(qualified_sources=len(identities),
        inventory_sha256=pin(inventory_path), manifest_sha256=pin(manifest_path),
        prediction_freeze_sha256=pin(LOCAL / 'prediction-freeze.json'))
    if (LOCAL / 'metadata-check.json').exists():
        assert json.loads((LOCAL / 'metadata-check.json').read_text()) == receipt
    else:
        write(LOCAL / 'metadata-check.json', receipt)
    print('13 identity joins; original prediction freeze retained')


if __name__ == '__main__':
    main()
