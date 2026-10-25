# SPDX-License-Identifier: GPL-3.0-or-later
"""Bounded D5A conditional source experiments; no target or answer access.

Reads the frozen D5 inputs/corpus and owned arithmetic modules. Writes new,
exclusive local JSON receipts and authored CSV summaries. Stdlib only. Source
request assembly is adapted from predictor_d4e.py at the recorded Git revision
under SOR-P-0002; generation and spatial math are imported unchanged. No process,
network, save, definition or analysis-project writes. Run from repository root.
"""
import csv
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / 'research' / p) for p in
               ('resource-slot-provenance', 'resource-geometry', 'resource-spatial')]
import predictor_d4e as predictor
import geometry
import context

LOCAL = ROOT / '.local-work/resource-construction-mask-selection'
DOC = ROOT / 'docs/experiments/resource-construction-mask-selection'


def pin(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf8', newline='\n') as stream:
        json.dump(value, stream, indent=2, allow_nan=False)
        stream.write('\n')


def table(name, rows):
    with (DOC / name).open('x', encoding='utf8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


def generate(c, q, source, mask):
    """Supply one explicit conditional mask, never infer a first query."""
    body = c['bodies'][q['body']]
    dx, dy = source['nominal']
    native = source['source_origin_native']
    ordinary = [r for r in source['selected']['resources'] if r.get('branch') != 'special']
    ordered = []
    for item in ordinary:
        rarity = item['rarity']
        weight = (0.0 if rarity == 6 else c['settings'][rarity]) if mask == 8 or mask < rarity else 1.0
        ordered.append(dict(resource=item['id'], block=c['generation_blocks'][item['block']] + [0, 0], weight=weight))
    req = dict(source=source['source_key'], provenance='D5A explicit conditional ordinary mask',
        origin=native, owner_key=int(q['body'], 16),
        clip_center=[native[0] + dx//2*100, native[1] + dy//2*100, 0],
        clip_half=[dx//2*100 + 200, dy//2*100 + 200, 0], context_qualified=True,
        order_qualified=True, cell_bounds=[1, dx+3, 1, dy+3], ordered_resources=ordered,
        packed_keys={f'{x},{y}': context.packed_seed_key(q['chart'], q['descriptor'], native,
            [x, y], body['system'], body['index']) for x in range(1, dx+3) for y in range(1, dy+3)})
    result = geometry.populate_source(req, {int(k, 16): v for k, v in c['constants'].items()})
    assert result['status'] == 'CONDITIONAL_PLANAR_SOURCE', result.get('reason')
    summaries = []
    for item, operand in zip(ordinary, ordered):
        paths = [r for r in result['regions'] if r['resource'] == item['id']]
        areas = [geometry.bounded_region_circle(r['points'], q['query'][:2], q['radius']) for r in paths]
        summaries.append(dict(resource=item['id'], rarity=item['rarity'], weight=operand['weight'],
            paths=len(paths), positive_area_paths=sum(a.get('intersection') == 'POSITIVE_AREA' for a in areas),
            unknown_area_paths=sum(a['status'] == 'UNKNOWN' for a in areas)))
    return dict(operands=ordered, summaries=summaries, regions=result['regions'])


def main():
    inputs = ROOT / '.local-work/resource-feynman-d5/inputs-v2.json'
    corpus = ROOT / '.local-work/resource-feynman-d5/build04/normalized.json'
    frozen = json.loads(inputs.read_text())
    c = predictor.validate(json.loads(corpus.read_text()))
    roster, outcomes, full = [], [], []
    identities = {'D2-81bf2a': '768fefacc1c939a7', 'D2-825f95': '011f99da36a6145d',
                  'D2-844cc6': 'bd2780da52fe20bd', 'D2-84e101': 'b0e207c2dee2c1b6'}
    for case in frozen['cases']:
        if case['case'] not in identities:
            continue
        q = case['request']
        for s in case['sources']:
            masks = s['neighborhood_low_masks']
            if len(masks) == 1:
                continue
            ax, ay = s['anchor']
            tile = predictor.tile_at(c['bodies'][q['body']], q['chart'], ax, ay)
            roster.append(dict(case=case['case'], source_key=s['source_key'], body=q['body'],
                workshop_bytes=identities[case['case']], biome=s['biome'], sfpt=tile[0],
                descriptor=';'.join(map(str, q['descriptor'])), source_origin=';'.join(map(str, s['source_origin_native'])),
                nominal_fine_cells=';'.join(map(str, s['nominal'])), reference_xyz=';'.join(map(str, q['query'])),
                radius_native=q['radius'], masks=';'.join(map(str, masks)),
                representative_cells=json.dumps(s['representative_cells'], separators=(',', ':')),
                constructor_query='UNKNOWN', historical_epoch='UNKNOWN',
                identity_status='SAVED_ACTIVE_QUALIFIED;CONDITIONAL_GEOGRAPHIC_SOURCE;NO_LIVE_WORKSHOP_JOIN',
                context='COMPARISON_ONLY_VII-b' if case['case'] == 'D2-825f95' else 'CANDIDATE',
                mask_support='INSTALLED_NEIGHBORHOOD;REACHABILITY_UNKNOWN'))
            for mask in masks:
                result = generate(c, q, s, mask)
                full.append(dict(case=case['case'], source=s['source_key'], mask=mask, **result))
                for ordinal, summary in enumerate(result['summaries']):
                    outcomes.append(dict(case=case['case'], source_key=s['source_key'], mask=mask,
                        ordinal=ordinal, **summary))
    assert len(roster) == 13
    # Freeze numeric predictions before any screenshot/extractor comparison.
    write(LOCAL / 'conditional-results.json', full)
    write(LOCAL / 'prediction-freeze.json', dict(inputs_sha256=pin(inputs), corpus_sha256=pin(corpus),
        results_sha256=pin(LOCAL / 'conditional-results.json'),
        code_sha256=pin(Path(__file__)), comparison_reads=False,
        earlier_resource_knowledge='Brief and required prior reports; not personally blinded',
        settings=c['settings']))
    DOC.mkdir(parents=True, exist_ok=True)
    table('cases.csv', roster)
    table('outcomes.csv', outcomes)
    print(json.dumps(dict(sources=len(roster), conditional_runs=len(full), rows=len(outcomes))))


if __name__ == '__main__':
    main()
