# SPDX-License-Identifier: GPL-3.0-or-later
"""Freeze source operands for all four mixed-mask cases, without answer reads.

Reads the D5 corpus and existing label-free request files only. Writes exclusive
ignored per-source JSON with anchors, masks and precise missing operands. Uses
the unchanged owned source resolver; no selection fitting or target access.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / 'research' / p) for p in
               ('resource-standalone', 'resource-slot-provenance', 'resource-geometry', 'resource-spatial')]
import predictor_d4e as predictor


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--corpus', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--targets', type=Path)
    args = ap.parse_args()
    assert args.output.resolve().is_relative_to(ROOT / '.local-work/resource-feynman-d5')
    c = predictor.validate(json.loads(args.corpus.read_text()))
    cases = []
    for case in ('D2-81bf2a', 'D2-825f95', 'D2-832210', 'D2-844cc6', 'D2-84e101'):
        path = ROOT / f'.local-work/resource-save52-d3/revision06/first-pass-v1/{case}-request.json'
        q = json.loads(path.read_text())
        body, chart, origin = c['bodies'][q['body']], q['chart'], q['descriptor']
        halo = q['radius'] + 400 + 2 * c['maximum_width']
        lo = [math.floor(origin[k] + (q['query'][k] - halo) / 100) for k in (0, 1)]
        hi = [math.floor(origin[k] + (q['query'][k] + halo) / 100) for k in (0, 1)]
        sources = {}
        for x in range(lo[0], hi[0] + 1):
            for y in range(lo[1], hi[1] + 1):
                s = predictor.resolve(c, body, chart, x, y)
                sources[s[:3]] = s
        rows = []
        for ax, ay, fid, dx, dy, biome in sources.values():
            cells = [(x, y, predictor.tile_at(body, chart, x, y)[3])
                     for x in range(ax - 4, ax + dx + 5)
                     for y in range(ay - 4, ay + dy + 5)]
            masks = sorted({v & 15 for x, y, v in cells})
            rows.append(dict(anchor=[ax, ay], sfbk=fid, nominal=[dx, dy], biome=biome,
                source_key=f'{chart}:{ax}:{ay}:{fid}', selected=body['biomes'][biome],
                source_origin_native=[100 * (v - o - 2) for v, o in zip((ax, ay), origin)],
                neighborhood_low_masks=masks, neighborhood_high_states=sorted({bool(v & 240) for x, y, v in cells}),
                representative_cells={str(m):next([x, y] for x, y, v in cells if v & 15 == m) for m in masks},
                construction_query_xy='UNKNOWN: first cache-miss caller argument',
                construction_geographic='UNKNOWN: depends on query and effective manager descriptor',
                construction_mask=masks[0] if len(masks) == 1 else 'INDETERMINATE',
                mask_scope='Existing conservative footprint; not a proof of historical query reachability'))
        cases.append(dict(case=case, request=q, request_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                          sources=rows))
    out = dict(schema='sor-d5-inputs/1', corpus_sha256=hashlib.sha256(args.corpus.read_bytes()).hexdigest(),
               cases=cases, comparison_evidence_read=False)
    with args.output.open('x', encoding='utf8', newline='\n') as stream:
        json.dump(out, stream, indent=2)
        stream.write('\n')
    if args.targets:
        assert args.targets.resolve().is_relative_to(ROOT / '.local-work/resource-feynman-d5')
        targets = {v['case']: dict(chart=v['request']['chart'], descriptor=v['request']['descriptor'],
            source_keys=[r['source_key'] for r in v['sources'] if
                v['case'] == 'D2-832210' or len(r['neighborhood_low_masks']) != 1]) for v in cases}
        with args.targets.open('x', encoding='utf8', newline='\n') as stream:
            json.dump(targets, stream, indent=2)
            stream.write('\n')
    print(json.dumps({v['case']: dict(sources=len(v['sources']), mixed=sum(
        len(r['neighborhood_low_masks']) != 1 for r in v['sources'])) for v in cases}))


if __name__ == '__main__':
    main()
