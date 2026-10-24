# SPDX-License-Identifier: GPL-3.0-or-later
"""Export bounded authored D5 tables after the frozen comparison step.

Reads local receipts, prior association tables and manually authored visual
observations below. Writes new CSV tables/source pins under the D5 report and
local accounting. No raw images, saves, corpus payloads or native exports leave
the ignored evidence boundary. Python stdlib and maintainer-owned methods only.
"""
import collections
import argparse
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LOCAL = ROOT / '.local-work/resource-feynman-d5'
DOC = ROOT / 'docs/experiments/resource-feynman-d5'
REFRESH = False
REFRESH_ALL = False


def pin(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def table(name, rows):
    if REFRESH and name != 'sources.csv':
        return
    with (DOC / name).open('w' if REFRESH or REFRESH_ALL else 'x', encoding='utf8', newline='') as stream:
        writer = csv.DictWriter(stream, list(rows[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


def main():
    global REFRESH, REFRESH_ALL
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--refresh-sources', action='store_true')
    parser.add_argument('--refresh-all', action='store_true')
    args = parser.parse_args()
    assert not (args.refresh_sources and args.refresh_all)
    REFRESH, REFRESH_ALL = args.refresh_sources, args.refresh_all
    access = json.loads((LOCAL / 'screenshot-comparison-access.json').read_text())
    assert access['prediction_freeze_sha256'] == pin(LOCAL / 'validation01/prediction-freeze.json')
    images = json.loads((LOCAL / 'screenshots01/manifest.json').read_text())['images']
    observations = [
        ('Fluorine', 'Turquoise apparent patch with white preview', 'NONE_VISIBLE'),
        ('Fluorine', 'Turquoise apparent patch at another view', 'NONE_VISIBLE'),
        ('Fluorine', 'Turquoise apparent patch; existing nearby extractor', 'RADIUS_OVERLAP'),
        ('Ionic Liquids', 'Turquoise apparent patch partly obscured by pads', 'NONE_VISIBLE'),
        ('Ionic Liquids', 'Broad turquoise apparent patch', 'NONE_VISIBLE'),
        ('Ionic Liquids', 'Turquoise apparent patch; existing nearby extractor', 'RADIUS_OVERLAP'),
        ('Copper', 'Turquoise apparent patch beside installed objects', 'NONE_VISIBLE'),
        ('Copper', 'Turquoise apparent patch at another view', 'NONE_VISIBLE'),
        ('Fluorine', 'Turquoise apparent patch beside pads', 'NONE_VISIBLE'),
        ('Water', 'No distinct deposit overlay visible in this frame', 'NONE_VISIBLE'),
        ('Antimony', 'Yellow apparent patch', 'NONE_VISIBLE'),
        ('Antimony', 'Yellow apparent patch and existing nearby extractor', 'RADIUS_OVERLAP'),
        ('Antimony', 'Yellow apparent patch and existing nearby extractors', 'RADIUS_OVERLAP'),
        ('Copper', 'Turquoise apparent patch', 'NONE_VISIBLE'),
        ('Gold', 'Yellow apparent patch and existing nearby extractors', 'RADIUS_OVERLAP'),
        ('Water Vapor', 'No distinct deposit overlay visible in this frame', 'NONE_VISIBLE'),
        ('Water', 'No distinct deposit overlay visible in this frame', 'NONE_VISIBLE'),
        ('Iridium', 'Yellow apparent patch', 'NONE_VISIBLE'),
        ('Uranium', 'Yellow apparent patch; explicit overlap-error banner', 'RADIUS_OVERLAP'),
        ('Uranium', 'Yellow apparent patch at another view', 'NONE_VISIBLE'),
        ('Uranium', 'Yellow apparent patch partly obscured by landing pad', 'NONE_VISIBLE'),
        ('Vanadium', 'Yellow apparent patch beside landing pad', 'NONE_VISIBLE'),
        ('Vanadium', 'Yellow apparent patch at another view', 'NONE_VISIBLE'),
        ('Vanadium', 'Broad yellow apparent patch and existing nearby extractor', 'RADIUS_OVERLAP')]
    inv = json.loads((ROOT / '.local-work/resource-save52/inventory-v2.json').read_text())
    cases = {r['case']: r for r in inv['cases']}
    rows = []
    for i, (image, observation) in enumerate(zip(images, observations), 1):
        case, label = ('D2-84e101', 'FEYNMAN V CU IL F') if i <= 8 else (
            ('D2-844cc6', 'FEYNMAN VIII-B AU SB') if i <= 15 else ('D2-832210', 'FEYNMAN III V U'))
        selected, deposit, error = observation
        rows.append(dict(image_id=f'D5-I{i:02}', filename=image['filename'],
            sha256=image['sha256'], bytes=image['bytes'], visible_label=label,
            case_candidate=case, saved_workshop_bytes=cases[case]['workshop_id'],
            selected=selected, apparent_deposit=deposit, placement=error,
            qualifier='Catalogue/visual observation only; no native path count or construction success',
            identity_limit='Unique label/body match within 19 saved rows; screenshot-to-native Workshop handle unobserved'))
    assert len(rows) == len(images) == len(observations) == 24
    table('screenshots.csv', rows)
    old = json.loads((ROOT / '.local-work/resource-slot-provenance/validation03/association-comparison.json').read_text())
    new = json.loads((LOCAL / 'validation01/association-comparison.json').read_text())
    old_by = {(r['case'], r['resource']): r for r in old}
    pairs = []
    for row in new:
        before = old_by[row['case'], row['resource']]['d4e_diagnostic']
        pairs.append(dict(case=row['case'], control=row['control'], resource=row['resource'],
            saved_witness=row['witness'], d2=row['d2'], d3=row['d3'], d4e=before,
            d5=row['d5_diagnostic'], changed_from_d4e=before != row['d5_diagnostic']))
    table('associations.csv', pairs)
    nine = [dict(r, mechanism='Ordered alternate descriptor' if r['case'] == 'D2-832210'
                 else 'First cache-miss construction query',
                 evidence='native.md; validation01; saved witness retained',
                 consequence='Conditional positive; historical component epoch unknown' if r['case'] == 'D2-832210'
                 else 'Indeterminate; capture original query, frame and sampled AL for joined source')
            for r in pairs if r['d4e'] == 'UNSUPPORTED_INDETERMINATE']
    assert len(nine) == 9
    table('nine-pairs.csv', nine)
    case_rows = []
    for row in cases.values():
        p = LOCAL / f'validation01/cohort/{row["case"]}-request-normalized-stdout.json'
        result = json.loads(p.read_text()) if p.exists() else None
        positive = {k for k, v in result['availability'].items() if v['status'] == 'PRESENT'} if result else set()
        associated = {r['resource'] for r in pairs if r['case'] == row['case']}
        case_rows.append(dict(case=row['case'], name=row['name'][0],
            saved_state='SAVED_ACTIVE_QUALIFIED' if row['eligibility'] == 'ACTIVE' else row['eligibility'],
            membership='NOT_AUTHORITATIVE_RUNTIME_MEMBERSHIP',
            prediction=result['status'] if result else 'PRESERVED_DISABLED_EXCLUSION',
            source_count=result['source_count'] if result else 0,
            generated_paths=len(result['regions']) if result else 0,
            positive_resources=';'.join(sorted(positive)), additional_unverified=';'.join(sorted(positive-associated)),
            association_counts=json.dumps(dict(collections.Counter(r['d5'] for r in pairs if r['case'] == row['case'])), sort_keys=True),
            failures=';'.join(sorted({r['reason'] for r in result['failures']})) if result else ''))
    table('cases.csv', case_rows)
    inputs = json.loads((LOCAL / 'inputs-v2.json').read_text())
    source_rows = []
    for item in inputs['cases']:
        for row in item['sources']:
            source_rows.append(dict(case=item['case'], source_key=row['source_key'],
                body=item['request']['body'], workshop_bytes=cases[item['case']]['workshop_id'], biome=row['biome'],
                component_status=row['selected']['status'],
                neighborhood_masks=';'.join(map(str,row['neighborhood_low_masks'])),
                first_query='UNKNOWN_CACHE_MISS_HISTORY', geographic_query='UNKNOWN_QUERY_AND_EFFECTIVE_FRAME',
                mask=row['construction_mask'], input_evidence='inputs-v2.json; build03/preparation.json',
                qualification='Installed-main source projection; no historical producer join'))
    table('source-cases.csv', source_rows)
    paths = [ROOT / 'docs/implementation-briefs/CODEX_BRIEF_SOR_RG2_D5_feynman_construction_mask_component_selection.md',
        ROOT / '.local-work/screengrabs/screengrabs-feynman.zip',
        ROOT / '.local-work/resource-slot-provenance/freeze01/freeze-v1.json',
        ROOT / '.local-work/resource-slot-provenance/validation03/summary.json']
    paths += [ROOT / '.local-work/recon' / n for n in ('resource-milestone-b-producers-01.tsv',
        'resource-availability-cont-01.tsv', 'resource-availability-cont-11.tsv',
        'activated-grid-01.tsv', 'surface-projection-14.tsv')]
    paths += list((ROOT / '.local-work/workshop-population-rework/specialist').glob('d5-*'))
    paths += [p for p in LOCAL.rglob('*') if p.is_file() and p.suffix in ('.json', '.jpg') and
              not p.is_relative_to(LOCAL / 'build01')]
    paths += [Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield') / n for n in
              ('Starfield.exe', 'Data/Starfield.esm', 'Data/Starfield - PlanetData.ba2')]
    for folder in ('resource-feynman-d5', 'resource-slot-provenance', 'resource-owner-root', 'resource-standalone', 'resource-selection-context'):
        paths += list((ROOT / 'research' / folder).glob('*.py'))
    table('sources.csv', [dict(id=f'D5-S{i:03}', path=str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else str(p),
        bytes=p.stat().st_size, sha256=pin(p),
        use='D5 authored method; derived from owned D4/D4E where stated' if p.is_relative_to(ROOT/'research/resource-feynman-d5')
            else 'Owned method under SOR-P-0002' if p.is_relative_to(ROOT/'research')
            else 'Pinned primary input or local derived evidence',
        eligibility='REVIEW-REQUIRED authored code/metadata' if p.is_relative_to(ROOT/'research') else 'LOCAL-ONLY payload; metadata REVIEW-REQUIRED')
        for i, p in enumerate(sorted(set(paths)), 1)])
    print(json.dumps(dict(images=24, cases=len(case_rows), associations=len(pairs), nine=len(nine),
                          source_rows=len(source_rows))))


if __name__ == '__main__':
    main()
