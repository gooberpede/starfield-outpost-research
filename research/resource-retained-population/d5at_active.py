# SPDX-License-Identifier: GPL-3.0-or-later
"""Reconcile the active Save52 census and extend coverage to both prewarm windows.

Read pinned owned receipts, installed ESM/BA2 and UCRT scalar math. Reuse the
audited ordinary Grid model and sample only supplemental source keys. Write
derived tables and a receipt to a new ignored directory. No game/process or
save writes. The prior package remains a separate, immutable baseline.
"""
import os
import sys

if sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):
    raise RuntimeError('Use pinned Python -E -B without optimization')

from collections import Counter, defaultdict
import csv
import ctypes
from itertools import product
import json
from pathlib import Path

from d5at_activation import prepare
from d5at_audit import distribution
import d5at_grid as grid
import d5at_grid_audit as audit
import d5at_survey as s
from d5at_tables import csv_table
from planet_world_key import qualified_grid


ROOT = s.ROOT
ACTIVATION = ROOT / '.local-work/d5aq/d5at-activation08/activation.json'
TRACE = ROOT / '.local-work/d5at-grid03.json'
CONSTANTS = ROOT / '.local-work/resource-query-reachability/native-bytes09.json'
MANIFEST = s.LEASE / 'resource-save52/build-v1/manifest.json'
LOCK = ROOT / '.local-work/d5at-activation-final-source-lock.json'
LOCK_SHA = '5d8c049a9d9637cbb33c79c56ce000dffc5caefd900c0aedb39689dfcb00e4b6'


def windows(site):
    result = {}
    for trigger, center in (('manager', site['saved_angular_input']['center']), ('focus', site['focus'])):
        if trigger == 'focus' and site['aligned']:
            continue
        bounds = prepare(center, {})['bounds']
        roots = set(product(*(range(lo, hi + 1) for lo, hi in zip(bounds['low'], bounds['high']))))
        density = {(x + dx, y + dy) for x, y in roots for dx, dy in grid.OFFSETS}
        result['both' if site['aligned'] else trigger] = (roots, density)
    return result


def enumerate_sources(corpus, body, chart, anchor, queries):
    """Select installed padded footprints touching the finite query set."""
    dx, dy = anchor
    geographic = {(x + dx, y + dy) for x, y in queries}
    widths = [max(values[axis] for values in corpus['source_blocks'].values()) for axis in (0, 1)]
    tiles = [range((min(values) - size + 3) // 192, (max(values) + 2) // 192 + 1)
             for size, values in zip(widths, zip(*geographic))]
    found = {}
    for tx, ty in product(*tiles):
        for source in grid.tile_sources(corpus, body, chart, tx, ty):
            ax, ay = source['anchor']
            w, h = source['size']
            if geographic.intersection(product(range(ax - 2, ax + w + 2), range(ay - 2, ay + h + 2))):
                found[source['key']] = source
    # Reverse the search from each query to the only 12-step anchors that
    # can cover it. This checks the tile-walk bounds and footprint endpoint.
    inverse = set()
    for qx, qy in geographic:
        xs = range(-(-(qx - widths[0] + 3) // 12), (qx + 2) // 12 + 1)
        ys = range(-(-(qy - widths[1] + 3) // 12), (qy + 2) // 12 + 1)
        for x, y in product(xs, ys):
            tx, ix = divmod(x, 16)
            ty, iy = divmod(y, 16)
            sfpt, orientation, *_ = corpus['bodies'][body]['tiles'][f'{chart}:{tx}:{ty}']
            s.require(orientation == 8, 'Unqualified inverse tile')
            block, flags = corpus['patterns'][sfpt][ix * 16 + iy]
            if flags & 8:
                w, h = corpus['source_blocks'][block]
                if qx < x * 12 + w - 2 and qy < y * 12 + h - 2:
                    inverse.add(f'{body}/{chart}:{x * 12}:{y * 12}:{block}')
    s.require(found.keys() == inverse, 'Query-to-anchor oracle differs')
    return found


def sample_source(case, source, corpus, raster, constants, crt):
    body, chart = case['body'], case['request']['chart']
    ax, ay = source['anchor']
    width, height = source['size']
    source = dict(source_id=source['key'], body=body, chart=chart, anchor=(ax, ay),
                  width=width, height=height)
    rows, missing = s.evaluate(source, product(range(-2, width + 2), range(-2, height + 2)),
                               raster, constants, crt)
    s.require(not missing, 'Supplemental atlas sample unqualified')
    for row in rows:
        column, line = (ax + row['x']) // 192, 255 - (ay + row['y']) // 192
        byte = raster['faces'][chart]['mask'][256 * line + column]
        s.require((row['chart'], row['column'], row['row'], row['byte'], row['mask']) ==
                  (chart, column, line, byte, byte & 15), 'Integer atlas oracle differs')
    source['rows'] = rows
    result = grid.trace(corpus, case, source, {}, {})
    tiles, indexed = audit.contributors(corpus, body, chart, source)
    s.require(result['status'] == 'FIXED_INPUT_TRACE' and set(tiles) == set(result['tiles']),
              'Supplemental Grid trace did not close')
    for row in result['rows']:
        q = row['relative']
        expected = audit.emission(indexed[q])
        s.require(row['emitted'] == expected and row['grid'] in ('RETAINED', 'CLIPPED', 'NOT_RETAINED'),
                  'Supplemental source slots disagree')
    atlas = {(r['x'], r['y']): r for r in rows}
    return result, atlas


def stats(masks):
    result = distribution([dict(mask=value) for value in masks])
    counts = {f'0x{k:x}': v for k, v in result['counts'].items()}
    total = sum(counts.values())
    return dict(coordinates=total, mask_counts=json.dumps(counts),
                mask_shares=json.dumps({k: v / total for k, v in counts.items()}),
                classes=len(counts), largest_share=result['largest_share'],
                effective_classes=result['effective_classes'] if counts else None)


def ranked(rows):
    groups = defaultdict(list)
    for row in rows:
        groups[row['family']].append(row)
    for family in ('grid', 'density', 'layer'):
        ordered = sorted(groups[family], key=lambda r: (
            not r['coordinates'], r['classes'] != 2, r['classes'] < 2,
            r['largest_share'] if r['classes'] == 2 else 0, -(r['effective_classes'] or 0),
            r['outpost'], r['source'], r['trigger']))
        for index, row in enumerate(ordered, 1):
            yield dict(rank=index if row['coordinates'] else 'UNRANKED', **row)


def run(output):
    before = s.guard()
    s.require(s.sha(LOCK) == LOCK_SHA, 'Reviewed source lock changed')
    locked = s.load(LOCK)['sha256']
    paths = (ACTIVATION, TRACE, grid.SURVEY, CONSTANTS, MANIFEST, s.D5,
             Path(sys.executable), s.domains.ARCHIVE, Path('C:/Windows/System32/ucrtbase.dll'))
    pins = {}
    for path in paths:
        key = path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else path
        digest = locked.get(key) or s.PINNED.get(path)
        s.require(digest and s.sha(path) == digest, f'Input identity differs: {path.name}')
        pins[str(key)] = digest
    corpus = s.load(s.D5)['payload']
    survey = s.load(grid.SURVEY)
    activation = s.load(ACTIVATION)
    sites = {row['case']: row for row in activation['sites']}
    cases = {row['case']: row for row in survey['outposts'] if row['eligibility'] == 'ACTIVE'}
    s.require(len(cases) == 17 and cases.keys() == sites.keys(), 'Active population mismatch')
    old = defaultdict(dict)
    exclusions = defaultdict(list)
    traces = s.load(TRACE)['results']
    for row in traces:
        case, key = row['outpost'], row['source']
        s.require(case in cases, 'Trace includes an excluded outpost')
        if row['status'] == 'FIXED_INPUT_TRACE':
            old[case][key] = row
        else:
            exclusions[case].append(row)
    rasters = s.domains.maps(s.load(MANIFEST), {row['body'] for row in cases.values()})
    constants = s.load(CONSTANTS)['sine_constants']
    crt = ctypes.CDLL('C:/Windows/System32/ucrtbase.dll')
    for name, count in (('cos', 1), ('atan2', 2)):
        fn = getattr(crt, name)
        fn.argtypes = [ctypes.c_double] * count
        fn.restype = ctypes.c_double
    fp = ctypes.c_uint32()
    crt._controlfp_s.argtypes = [ctypes.POINTER(ctypes.c_uint32), ctypes.c_uint32, ctypes.c_uint32]
    s.require(crt._controlfp_s(ctypes.byref(fp), 0, 0) == 0 and fp.value & 0x300 == 0,
              'Host rounding must be round-to-nearest')

    inventory, relations, ranks, supplemental, new_traces = [], [], [], [], []
    for identity, case in cases.items():
        frame, site = case['request'], sites[identity]
        chart, anchor, body = frame['chart'], frame['descriptor'], case['body']
        packed = qualified_grid(int(case['descriptor_key'], 16))
        definition = corpus['bodies'][body]
        s.require(case['registered'] and case['body_concordant'] and body == frame['body']
                  and (packed['tag'], packed['x'], packed['y'], packed['system_id'], packed['body_index']) ==
                  (chart, *anchor, definition['system'], definition['index'])
                  and site['saved_angular_input']['snap'] == site['saved_descriptor'], 'Saved site identity differs')
        queries = windows(site)
        occupied = tuple(site['focus'])
        site_cell = tuple(case['site_cell'][i + 1] - anchor[i] for i in range(2))
        relevant = {occupied, site_cell}.union(*(keys for window in queries.values() for keys in window))
        s.require(all(-100 <= v < 100 for q in relevant for v in q), 'Grid envelope clips the scope')
        installed = enumerate_sources(corpus, body, chart, anchor, relevant)
        direct, resident, added = [], [], 0
        for key in sorted(installed.keys() | old[identity].keys()):
            previous = old[identity].get(key)
            if previous is None:
                trace, atlas = sample_source(case, installed[key], corpus, rasters[body], constants, crt)
                new_traces.append(trace)
            else:
                trace = previous
            masks = {tuple(r['native']): r['mask'] for r in trace['rows'] if r['grid'] == 'RETAINED'}
            if previous is None and not masks.keys() & relevant:
                continue
            actual = key == s.C1
            hit = occupied in masks
            if hit:
                direct.append(key)
            if actual:
                resident.append(key)
            if previous is None:
                added += 1
                manager, focus = (queries.get(trigger, queries.get('both')) for trigger in ('manager', 'focus'))
                for row in trace['rows']:
                    q = tuple(row['native'])
                    if q not in masks:
                        continue
                    ref = atlas[row['relative']]
                    supplemental.append(dict(outpost=identity, source=key, x=q[0], y=q[1], face=ref['chart'],
                                             column=ref['column'], row=ref['row'], atlas_byte=hex(ref['byte']),
                                             mask=hex(ref['mask']), manager_density=q in manager[1],
                                             manager_layer=q in manager[0], focus_density=q in focus[1],
                                             focus_layer=q in focus[0]))
            qualification = ('VERIFIED_RESIDENT' if actual else 'VERIFIED_INDEXED_GRID' if hit
                             else 'CONDITIONAL_SAVED_WINDOW' if masks.keys() & relevant else 'CONDITIONAL_HALO')
            selection = trace['selected']
            relations.append(dict(outpost=identity, source=key, qualification=qualification,
                                  occupied_cell_retained=hit, saved_pair_cell_retained=site_cell in masks,
                                  observed_resident=actual, installed_sfpt=selection['sfpt'],
                                  biome=selection['biome'], fnam_index=selection['fnam_index'],
                                  selected_main_key=key,
                                  retained_grid=len(masks), basis='REVIEWED_HALO' if previous else 'SUPPLEMENTAL_WINDOW',
                                  effect='QUALIFIED_FOR_SCOPED_RANK'))
            ranks.append(dict(family='grid', outpost=identity, source=key, trigger='grid',
                              qualification=qualification, cohort='RETAINED_GRID', **stats(list(masks.values()))))
            for trigger, (layers, densities) in queries.items():
                for family, keys in (('layer', layers), ('density', densities)):
                    ranks.append(dict(family=family, outpost=identity, source=key, trigger=trigger,
                                      qualification=qualification, cohort='CONDITIONAL_SAVED_ANGLE_PREWARM',
                                      **stats([masks[q] for q in keys & masks.keys()])))
        for row in exclusions[identity]:
            s.require(row['status'] in ('DIFFERENT_MAIN_FILE_BLOCK', 'NO_MAIN_FILE_ANCHOR'),
                      'Material unresolved installed selection')
            relations.append(dict(outpost=identity, source=row['source'], qualification='UNRESOLVED_ALTERNATE_ROUTE',
                                  occupied_cell_retained='UNKNOWN', saved_pair_cell_retained='UNKNOWN',
                                  observed_resident=False, installed_sfpt='UNKNOWN', biome='UNKNOWN',
                                  fnam_index='UNKNOWN', selected_main_key=(row.get('selected') or {}).get('key', 'NONE'),
                                  retained_grid='UNKNOWN', basis=row['status'],
                                  effect='EXCLUDED_FROM_INSTALLED_MAIN_RANK'))
        s.require(direct, 'No installed source covers the saved indexed center')
        inventory.append(dict(outpost=identity, saved_reference=case['token'], workshop_id=case['workshop_id'],
                              body=body, packed_descriptor=case['descriptor_key'], chart=chart,
                              descriptor_x=anchor[0], descriptor_y=anchor[1], occupied_x=occupied[0] + anchor[0],
                              occupied_y=occupied[1] + anchor[1], saved_pair_x=site_cell[0] + anchor[0],
                              saved_pair_y=site_cell[1] + anchor[1], indexed_grid_sources=';'.join(direct),
                              observed_resident_sources=';'.join(resident), retained_halo=len(old[identity]),
                              added_window=added, alternate_routes=len(exclusions[identity])))
    installed_audit = audit.verify_installed(dict(results=new_traces), corpus)
    s.guard()
    output.mkdir()
    for name, rows in (('active-sites', inventory), ('active-source-relations', relations),
                       ('active-rankings', list(ranked(ranks))), ('supplemental-masks', supplemental)):
        csv_table(output, name, rows)
    s.write(output / 'receipt.json', dict(before=before, after=s.guard(), inputs=pins, sites=inventory,
                                          relationships=dict(Counter(r['qualification'] for r in relations)),
                                          supplemental_atlas_rows=len(supplemental), esm_audit=installed_audit))
    print(len(inventory), len(relations), len(ranks), len(supplemental), installed_audit)


if __name__ == '__main__':
    output = Path(sys.argv[1]).absolute()
    s.require(output.is_relative_to(ROOT / '.local-work') and output == output.resolve() and not output.exists(),
              'Fresh ignored output required')
    run(output)
