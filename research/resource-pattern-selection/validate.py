# SPDX-License-Identifier: GPL-3.0-or-later
"""C2D validator, conditional coverage analysis and seven-path regression.

Reads a closed blind predictor output before loading witnesses. Reads existing
owned context, C2C and C1H derivatives and raw native receipts; writes exclusive
ignored results/full geometry. No target, save, config, database or Git effects.
Expected SFPT is used only for comparison and separately labelled coverage.
"""
import argparse
import collections
import copy
import json
from pathlib import Path
import sys
from predict import ROOT, pin
from selector import source_at
import context
import geometry

sys.path.insert(0, str(ROOT / 'research/resource-source-enumeration'))
from analyze import inputs, reframe, signature


def run(prediction, output):
    assert output.resolve().is_relative_to(ROOT / '.local-work/resource-pattern-selection')
    blind = json.loads(prediction.read_text())
    for path, sha in blind['inputs'].items():
        assert pin(Path(path)) == sha
    prediction_pin = pin(prediction)
    installed_tables = None
    if blind.get('mode') == 'INSTALLED_LINKED_TREE':
        assert pin(Path(blind['tables_path'])) == blind['tables_sha256']
        installed_tables = json.loads(Path(blind['tables_path']).read_text())
    prior_path = ROOT / '.local-work/resource-source-enumeration/analysis05.json'
    prior = json.loads(prior_path.read_text())
    for path, sha in prior['inputs'].items():
        assert pin(Path(path)) == sha
    styles, blocks, patterns, registry = inputs()
    full_path = ROOT / '.local-work/resource-installed-settings/c2b-geometry01.json'
    full = json.loads(full_path.read_text())
    result = dict(schema='sor-c2d-validation/1', predictor_sha256=prediction_pin,
        sites=[], inputs={str(prior_path): pin(prior_path), str(full_path): pin(full_path)})
    result['inputs'][str(Path(__file__))] = pin(Path(__file__))
    if installed_tables is not None:
        result['inputs'][blind['tables_path']] = blind['tables_sha256']
    generated_all = []
    constants = {int(r['va'], 16): r['float'] for r in json.loads((ROOT / '.local-work/resource-milestone-b-spatial-constants.json').read_text())['constants']}
    for old in prior['sites']:
        site = old['site']
        frozen = json.loads((ROOT / f'.local-work/resource-geometry-mature-context/site-{site.lower()}-initial02.json').read_text())
        constants.update({int(c['va'], 16): c['value'] for c in frozen['constants']})
        m = context.read_map((ROOT / f'.local-work/outpost-biomes/{"carinae iii-a" if site == "Carinae" else "feynman v"}.biom').read_bytes())
        selected = context.select_patterns(m, styles, registry, frozen['system'], frozen['index'])
        selected['map'] = m
        baseline_selected = copy.deepcopy(selected)
        if installed_tables is not None:
            selected['tables'] = installed_tables[site]
        row = dict(site=site, selection_validation='NO_RUNTIME_SFPT_WITNESS', source_inventories=[], cells=[])
        if site == 'Carinae':
            observed = old['observed']
            trace = next(r for s in blind['sites'] if s['site'] == site for r in s['traces'] if r['coarse'] == observed['coarse'])
            row['selection_validation'] = 'CONDITIONAL_MODEL_FALSIFIED; EFFECTIVE_INPUTS_UNRESOLVED' if trace['selected'] != observed['pattern'] else 'EXACT_UPSTREAM_INSTALLED_PREDICTION'
            row['predicted'] = trace['selected']
            row['observed'] = observed['pattern']
            cx, cy = observed['coarse']
            baseline_selected['tables'][observed['tag']][cx * 256 + cy] = int(observed['pattern'], 16), observed['pattern_flags']
            if installed_tables is None:
                selected['tables'] = copy.deepcopy(baseline_selected['tables'])
        lo, hi = frozen['halo']['owner_cell_bounds']
        sources = {}
        for x in range(lo[0], hi[0] + 1):
            for y in range(lo[1], hi[1] + 1):
                try:
                    before = context.source_at(frozen['tag'], x, y, frozen['origin'], baseline_selected, patterns, blocks, padding=2)
                    old_status = 'RESOLVED'
                except ValueError as error:
                    before = None
                    old_status = str(error)
                source, decision = source_at(frozen['tag'], x, y, frozen['origin'], selected, patterns, blocks)
                row['cells'].append(dict(cell=[x, y], before=old_status,
                    before_source=before['id'] if before else None,
                    after=decision['status'], source=source['id'] if source else None,
                    pattern=f'0x{selected["tables"][frozen["tag"]][(x//192)*256+y//192][0]:08x}',
                    initial_form=f'0x{decision["initial"][0]:08x}', initial_flags=f'0x{decision["initial"][1]:02x}',
                    resolved_flags=f'0x{decision.get("flags", 0):02x}', used_fallback=decision.get('used_fallback'),
                    rule=('Installed PNDT-linked SFTR; direct anchor or one backlink then typed block'
                          if installed_tables is not None else
                          'Retained-pattern diagnostic; direct anchor or one backlink then typed block')))
                if source:
                    sources[source['id']] = source
        previous = old.get('after', old['before'])
        all_ids = {s['id'] for s in previous} | set(sources)
        for identity in sorted(all_ids):
            source = sources.get(identity, next((s for s in previous if s['id'] == identity), None))
            ax, ay = source['geographic_origin']
            dx, dy = source['dimensions']
            masks = sorted({context.mask_lookup(m, frozen['tag'], x, y) & 15
                            for x in range(ax - 4, ax + dx + 5)
                            for y in range(ay - 4, ay + dy + 5)})
            assert masks == ([4] if site == 'Carinae' else [8])
            in_before = any(s['id'] == identity for s in previous)
            in_after = identity in sources
            if in_before and in_after:
                reason = 'Retained source identity; typed block accepted under selected linked tree'
            elif site == 'Carinae' and in_after:
                reason = 'Added by single-backlink typed-block correction under independently selected linked tree'
            elif in_after:
                reason = 'Added by installed linked-SFTR pattern substitution'
            else:
                reason = 'Excluded by installed linked-SFTR pattern substitution'
            row['source_inventories'].append(dict(identity=identity, pattern=f'0x{source["pattern"]:08x}',
                before=in_before, after=in_after, reason=reason,
                classification='DERIVED_CONDITIONAL', mask_footprint=masks, source=source))
        row['cell_counts'] = dict(collections.Counter(c['after'] for c in row['cells']))
        old_sources = [s for s in full if s['site'] == site]
        if site == 'Carinae':
            template = old_sources[0]['request']
        regions = []
        for source in sources.values():
            matching = next(s['source']['id'] for s in frozen['sources']
                            if s['source']['resource_biome'] == source['resource_biome'])
            template = next(s['request'] for s in old_sources if s['request']['source'] == matching)
            request = reframe(template, source, frozen)
            g = geometry.populate_source(request, constants)
            assert g['status'] == 'CONDITIONAL_PLANAR_SOURCE'
            regions.extend(g['regions'])
        row['paths'] = len(regions)
        if site == 'Carinae':
            native_comparisons = old['replay']['comparisons']
            from qualify import independent
            import struct
            comparisons = []
            for expected in native_comparisons:
                n = expected['capture']
                capture_path = ROOT / f'.local-work/resource-carinae/retail-attempt02/capture-{n:05d}.bin'
                r = independent(capture_path)[1]
                native = dict(points=list(struct.iter_unpack('<4f', bytes.fromhex(r['geometry']['ordered_xyzw']))),
                    native_bound=struct.unpack_from('<4f', bytes.fromhex(r['geometry']['raw_region'])))
                matches = [g for g in regions if g['resource'] == expected['resource'][2:] and signature(g) == signature(native)]
                comparisons.append(dict(capture=n, resource=expected['resource'], exact_matches=len(matches)))
                result['inputs'][str(capture_path)] = pin(capture_path)
            row['comparisons'] = comparisons
            assert [r['exact_matches'] for r in comparisons] == [1, 1, 1]
        else:
            original = [g for s in old_sources for g in s['regions']]
            assert [(g['resource'], g['cell'], signature(g)) for g in regions] == [(g['resource'], g['cell'], signature(g)) for g in original]
            row['geometry_unchanged'] = True
            row['source_identity_unchanged'] = [g['source'] for g in regions] == [g['source'] for g in original]
            control_path = ROOT / 'docs/experiments/resource-source-enumeration/controls-v1.json'
            controls = json.loads(control_path.read_text())['sites'][0]['accepted']
            from qualify import independent
            import struct
            row['comparisons'] = []
            for expected in controls:
                n = expected['capture']
                capture_path = ROOT / f'.local-work/resource-region-ancestry/retail-attempt01/capture-{n:05d}.bin'
                r = independent(capture_path)[1]
                fid = struct.unpack_from('<I', bytes.fromhex(r['selected']['raw_resource']), 0x28)[0]
                native = dict(points=list(struct.iter_unpack('<4f', bytes.fromhex(r['geometry']['ordered_xyzw']))),
                    native_bound=struct.unpack_from('<4f', bytes.fromhex(r['geometry']['raw_region'])))
                matches = [g for g in regions if g['resource'] == f'{fid:08x}' and signature(g) == signature(native)]
                row['comparisons'].append(dict(capture=n, resource=f'0x{fid:08x}', exact_matches=len(matches)))
                result['inputs'][str(capture_path)] = pin(capture_path)
            result['inputs'][str(control_path)] = pin(control_path)
            assert [r['exact_matches'] for r in row['comparisons']] == [1, 1, 1, 1]
        generated_all.append(dict(site=site, regions=regions))
        result['sites'].append(row)
    assert pin(prediction) == prediction_pin
    assert all(pin(Path(p)) == sha for p, sha in result['inputs'].items())
    with output.open('x', encoding='utf8', newline='\n') as f:
        json.dump(result, f, indent=2)
        f.write('\n')
    geometry_path = output.with_suffix('.geometry.json')
    with geometry_path.open('x', encoding='utf8', newline='\n') as f:
        json.dump(generated_all, f)
        f.write('\n')
    print([(s['site'], s['selection_validation'], s['cell_counts'], len(s['source_inventories']), s['paths']) for s in result['sites']])


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--prediction', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    run(a.prediction, a.output)
