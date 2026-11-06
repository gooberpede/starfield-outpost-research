# SPDX-License-Identifier: GPL-3.0-or-later
"""Survey saved geographic candidates and count conditional raster samples.

Reads pinned installed data and authenticated Save52/D3/D5AQ derivatives.
Writes fresh JSON under ignored local work. Reuses owned D3 route resolution,
D5H insertion attempts/atlas loader, and both D5AQ numerical paths.
The D3 halo and source-anchor hypotheses never qualify an actual native cohort.
"""
import os
import sys

if sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):
    raise RuntimeError('Use pinned Python -E -B without optimization')

import argparse
from collections import Counter
import ctypes
import csv
import json
import math
from pathlib import Path
import re

from d5ap_analyze import ROOT, guard, require, sha, write
from d5aq_oracle import sample

for directory in ('research/resource-standalone', 'research/resource-geometry',
                  'save-analysis/scripts', 'research/resource-query-reachability'):
    sys.path.insert(0, str(ROOT / directory))

import domains
from predictor_d3 import resolve, validate
from roundtrip import projected

DOC = ROOT / 'docs/experiments/resource-retained-population'
LEASE = ROOT / '.local-work/resources-evidence-consolidation/d5at-inputs01/.local-work'
INSTALL = domains.ARCHIVE.parent.parent
C1 = '0005e0de/0:37536:20928:0029d20e'
D5 = ROOT / '.local-work/resources-evidence-consolidation/d5r-input-lease01/.local-work/resource-feynman-d5/build04/normalized.json'
COMPOSITES = DOC / 'd5u/outposts'
COMPOSITE_PINS = {
    'D2-81a75b': '61a26b4804e830ea538641a53f6aea8d24de5c625188fe7fdd3abac8a93ef5d4',
    'D2-81bf2a': '04d7f3e285406cf1faab7c066276373af264d90635ccdd9dad66edfde1e74481',
    'D2-825f95': 'ccd95c46cdde990a9c5f45241c1ef625a0488e9321df38d7ef43bf816fef65a9',
    'D2-82be17': 'c853ac9f6558e8b41e10ecf4d0dd8382cc8f8c0ba2bb434e03caeb325b2b83c7',
    'D2-83388f': '5cfb5b9a3af2bd33571197ca9855b749f58e38109d515ca59dae9c147e12c217',
    'D2-844cc6': '38717fdab5e23c067d090d39eb701c14988b70a87e5acf368b32ba96aaf72634',
    'D2-84e101': '8db687f2364281505e93bbf86900ae59a25f053fa38ae1f198605773de32edb5',
}
D5I = ROOT / 'docs/experiments/resource-query-variability/source-cases.csv'
PINNED = {
    Path(sys.executable): 'cce21c0e8710e304273e98ac4b2b0f5aceb639acbcd2343cbaa5c4e81619c45b',
    INSTALL / 'Starfield.exe': '7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28',
    INSTALL / 'Data/Starfield.esm': '1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7',
    domains.ARCHIVE: '2fb1fff5d8fc074718bf05022c099f3c87ef70e00050229b368ae7d680fbe5d5',
    Path('C:/Windows/System32/ucrtbase.dll'): '3c60056371f82e4744185b6f2fa0c69042b1e78804685944132974dd13f3b6d9',
    LEASE / 'resource-save52/inventory-v2.json': 'e42cc2969336c8eca36c837b860619647eed4461dc52d1679c67e0b9cda1b668',
    LEASE / 'resource-save52-d3/build-v6/normalized.json': 'd6fe11c89656f5a928d30e49e99e1ad7fb18dedbedad65ba8b4ef3f626a3ee12',
    LEASE / 'resource-save52/build-v1/manifest.json': '9d2ff9012a573595227c8feda5345de35286b807103665486239ddbe8cbfa9de',
    ROOT / '.local-work/d5aq/census04/census.json': '704e106a9698491dc37fc408bd38dec374bea2a8316bf874243fb2591eb35b8c',
    ROOT / '.local-work/d5aq/startup-native05/receipt.json': 'c54d27f5a0ad29319e6090b5577470ae0c051551bfc3d6f7d14e7e222cb0e8a6',
    ROOT / 'docs/experiments/resource-query-reachability/source-domains.csv': '1efa9663c586b9570fffb8d78a66aaa5dc5188673438179430719fecfb189374',
    D5: '97aa50e0eb6bc7a2d5157bffbb311942fd84e7c01e6bd2ef3ea28a4e9bd9e0f9',
    D5I: '6137dbf25c7ad8f525ecdd67c98da79139594c202bb6009545747033bbd9453d',
    COMPOSITES / 'coordinates.csv': 'a253cbae5bf8b6ee5b09c9b923f45a3749a443c5dab6f846807aa59f1c5e26f6',
    COMPOSITES / 'primary-reconciliation.csv': 'f4379c33fb1e677695fbfd7c9c16a898fb65c9549a47c82c7feb1525bcd864ce',
    **{COMPOSITES / f'{case}.json': digest for case, digest in COMPOSITE_PINS.items()},
}


def load(path):
    return json.loads(Path(path).read_bytes())


def read_csv(path):
    with path.open(encoding='utf8', newline='') as stream:
        return list(csv.DictReader(stream))


def archived_candidates(sources, joins, unresolved):
    """Keep D5H's competing selection rows alongside the older D3 routes."""
    path = ROOT / 'docs/experiments/resource-query-reachability/source-domains.csv'
    aliases = {'Archimedes': 'D2-81a75b', 'Carinae': 'D2-82be17', 'original-V': 'D2-83388f'}
    existing = {(row['outpost'], row['source_id']): row for row in joins}
    for row in read_csv(path):
        case = aliases.get(row['case'], row['case'])
        body = row['body'][2:]
        chart, ax, ay, block = row['source_key'].split(':')
        chart, ax, ay = map(int, (chart, ax, ay))
        left, right, bottom, top = map(int, re.fullmatch(
            r'\[(\d+),(\d+)\)x\[(\d+),(\d+)\)', row['nominal']).groups())
        require((left, bottom) == (ax, ay), 'D5H rectangle anchor')
        key = f"{body}/{row['source_key']}"
        source = dict(source_id=key, body=body, chart=chart, anchor=[ax, ay], block=block,
                      width=right-left, height=top-bottom, biome=row['biome'][2:],
                      sfpt=row['sfpt'][2:], effective_rsgd=row['effective_rsgd'][2:])
        if key in sources:
            require(all(sources[key][field] == source[field] for field in
                        ('body', 'chart', 'anchor', 'block', 'width', 'height')),
                    'D5H versus D3 shared key dimensions')
            for field in ('biome', 'sfpt'):
                if sources[key][field] != source[field]:
                    unresolved.append(dict(outpost=case, source_id=key,
                                           reason=f'COMPETING_{field.upper()} {sources[key][field]} versus D5H {source[field]}',
                                           count=None))
        sources[key] = source
        if (case, key) in existing:
            existing[case, key]['provenance'] += '; D5H source-domain table'
        else:
            joins.append(dict(outpost=case, source_id=key,
                              qualification='PLAUSIBLE_SOURCE_CANDIDATE', provenance='D5H source-domain table'))
        if key == C1:
            joins.append(dict(outpost=case, source_id=key, qualification='RESIDENT_ONLY',
                              provenance='D5AS direct-visit resident target; area intersection unverified'))
        competing = [other for saved, other in existing if saved == case and other != key
                     and sources[other]['anchor'] == [ax, ay]]
        for other in competing:
            unresolved.append(dict(outpost=case, source_id=key, reason=f'COMPETING_D3_SELECTION {other}', count=None))


def descriptor(chart, x, y):
    return chart, (x // 192, y // 192), (x % 192 // 12, y % 192 // 12), (x % 12, y % 12)


def composite_candidates(cases, sources, joins):
    """Reconcile the prior seven saved-frame composites by exact key."""
    historical = load(D5)['payload']
    existing = {(row['outpost'], row['source_id']): row for row in joins
                if row['qualification'] == 'PLAUSIBLE_SOURCE_CANDIDATE'}
    control_ids = {row['contributing_sources'] for row in read_csv(COMPOSITES / 'primary-reconciliation.csv')
                   if row['native_points_bounds_exact'] == 'True' and row['model_disk_intersection'] == 'POSITIVE_AREA'}
    for case in cases:
        if case['case'] not in COMPOSITE_PINS:
            continue
        composite = load(COMPOSITES / f"{case['case']}.json")
        ref = composite['reference']
        require((ref['body'], ref['beacon_token'], ref['record_offset'], ref['center']) ==
                (case['body'], case['token'], case['record_offset'], case['request']['query']),
                'Composite saved-frame identity mismatch')
        for layer in {row['source_key']: row for row in composite['layers']}.values():
            chart, ax, ay, block = layer['source_key'].split(':')
            chart, ax, ay = map(int, (chart, ax, ay))
            width, height = layer['nominal']
            key = f"{case['body']}/{layer['source_key']}"
            if key not in sources:
                tile = historical['bodies'][case['body']]['tiles'][f'{chart}:{ax//192}:{ay//192}']
                require(historical['source_blocks'][block] == [width + 4, height + 4],
                        'Composite dimensions disagree with D5 source block')
                sources[key] = dict(source_id=key, body=case['body'], chart=chart, anchor=[ax, ay],
                                    block=block, width=width, height=height, biome=tile[2], sfpt=tile[0])
            require([sources[key]['width'], sources[key]['height']] == [width, height],
                    'Composite source dimensions mismatch')
            identity = case['case'], key
            if identity in existing:
                existing[identity]['provenance'] += '; D5U-C1 saved-frame composite'
            else:
                joins.append(dict(outpost=case['case'], source_id=key,
                                  qualification='PLAUSIBLE_SOURCE_CANDIDATE',
                                  provenance='D5U-C1 saved-frame composite and D5 definitions'))
            if case['case'] == 'D2-83388f' and layer['source_id'] in control_ids:
                joins.append(dict(outpost=case['case'], source_id=key,
                                  qualification='VERIFIED_RESEARCH_DISK_INTERSECTION',
                                  provenance='D5U-C1 fixed 150-unit modeled disk with exact native point/bound controls'))


def route_candidates(corpus, case):
    request = case['request']
    if request is None or not case['body_concordant'] or request['body'] != case['body']:
        return {}, Counter({'UNQUALIFIED_SAVED_FRAME_OR_BODY': 1})
    if case['body'] not in corpus['bodies']:
        return {}, Counter({'MISSING_CORPUS_BODY': 1})
    body = corpus['bodies'][case['body']]
    chart = request['chart']
    origin, center = request['descriptor'], request['query']
    halo = request['radius'] + 400 + 2 * corpus['maximum_width']
    low = [math.floor(o + (c - halo) / 100) for o, c in zip(origin, center)]
    high = [math.floor(o + (c + halo) / 100) for o, c in zip(origin, center)]
    sources, missing = {}, Counter()
    for x in range(low[0], high[0] + 1):
        for y in range(low[1], high[1] + 1):
            try:
                ax, ay, block, dx, dy, biome = resolve(corpus, body, chart, x, y)
            except (KeyError, ValueError) as error:
                missing[str(error)] += 1
                continue
            key = f"{case['body']}/{chart}:{ax}:{ay}:{block}"
            row = dict(source_id=key, body=case['body'], chart=chart, anchor=[ax, ay],
                       block=block, width=dx, height=dy, biome=biome,
                       sfpt=body['tiles'][f'{chart}:{ax//192}:{ay//192}'][0])
            if key in sources:
                require(sources[key] == row, 'Inconsistent source identity')
            sources[key] = row
    return sources, missing


def evaluate(source, coordinates, raster, constants, crt):
    chart = source['chart']
    ax, ay = source['anchor']
    desc = descriptor(chart, ax, ay)
    rows, missing = [], []
    for x, y in sorted(coordinates):
        try:
            reference = sample(desc, (x, y), raster)
            expected = (reference['chart'], reference['column'], reference['row'], reference['byte'])
            for fused in (False, True):
                tag, col, row, _ = projected(chart, ax + x, ay + y, constants=constants,
                                             fused=fused, scalar_math=crt)
                got = (tag, col, row, raster['faces'][tag]['mask'][256 * row + col])
                if got != expected:
                    raise ValueError(f'Atlas discrepancy, fused={fused}, {got} versus {expected}')
        except (ValueError, KeyError, IndexError) as error:
            missing.append(dict(x=x, y=y, reason=str(error)))
            continue
        rows.append(dict(x=x, y=y, **reference))
    return rows, missing


def survey():
    floors = guard()
    pins = PINNED.copy()
    for ledger, names in (
        ('d5t-sources.csv', {'.local-work/resource-query-reachability/native-bytes09.json'}),
    ):
        selected = {ROOT / r['path']: r['sha256'] for r in read_csv(DOC / ledger) if r['path'] in names}
        require(len(selected) == len(names), 'Missing arithmetic pin')
        pins.update(selected)
    for path, digest in pins.items():
        require(sha(path) == digest, f'Input identity changed: {path}')
    inventory = load(LEASE / 'resource-save52/inventory-v2.json')
    require(inventory['sha256'] == '6b4a10084c7e752c31fd2de121a00850aaa2bf1decd700b437d7dccfcdbc82e8',
            'Save52 derivative input identity')
    corpus = validate(load(LEASE / 'resource-save52-d3/build-v6/normalized.json'))
    manifest = load(LEASE / 'resource-save52/build-v1/manifest.json')
    constants = load(ROOT / '.local-work/resource-query-reachability/native-bytes09.json')['sine_constants']
    crt = ctypes.CDLL('C:/Windows/System32/ucrtbase.dll')
    for name, count in (('cos', 1), ('atan2', 2)):
        fn = getattr(crt, name)
        fn.argtypes = [ctypes.c_double] * count
        fn.restype = ctypes.c_double
    control = ctypes.c_uint32()
    crt._controlfp_s.argtypes = [ctypes.POINTER(ctypes.c_uint32), ctypes.c_uint32, ctypes.c_uint32]
    require(crt._controlfp_s(ctypes.byref(control), 0, 0) == 0 and control.value & 0x300 == 0,
            'Host rounding mode must be round-to-nearest')
    sources, joins, unresolved = {}, [], []
    historical = load(D5)['payload']
    for case in inventory['cases']:
        site_joins = {}
        for label, inputs in (('D3', corpus), ('D5', historical)):
            candidates, missing = route_candidates(inputs, case)
            for key, row in candidates.items():
                if key in sources:
                    require(all(sources[key][field] == row[field] for field in
                                ('body', 'chart', 'anchor', 'block', 'width', 'height')),
                            'Conflicting cross-outpost identity')
                    for field in ('biome', 'sfpt'):
                        if sources[key][field] != row[field]:
                            unresolved.append(dict(outpost=case['case'], source_id=key,
                                                   reason=f'COMPETING_{field.upper()} {sources[key][field]} versus {label} {row[field]}',
                                                   count=None))
                sources[key] = row
                if key not in site_joins:
                    site_joins[key] = dict(outpost=case['case'], source_id=key,
                                           qualification='PLAUSIBLE_SOURCE_CANDIDATE', provenance=label)
                else:
                    site_joins[key]['provenance'] += f'; {label}'
            for reason, count in missing.items():
                unresolved.append(dict(outpost=case['case'], source_id=None, reason=f'{label} {reason}', count=count))
        for key, row in site_joins.items():
            row['provenance'] += ' saved-frame installed halo routes'
            if row['provenance'].startswith('D3 saved-frame'):
                unresolved.append(dict(outpost=case['case'], source_id=key,
                                       reason='D3_ROUTE_NOT_REPRODUCED_BY_D5', count=None))
        joins.extend(site_joins.values())
        unresolved.append(dict(outpost=case['case'], source_id=None,
                               reason='UNVERIFIED_COMPLETE_GEOGRAPHIC_SOURCE_CENSUS', count=None))
    archived_candidates(sources, joins, unresolved)
    composite_candidates(inventory['cases'], sources, joins)
    require(C1 in sources, 'Feynman target absent from corroborating source domains')
    candidates = inventory['census']['candidates']
    ordinary = {row['saved_reference_token'] for row in candidates if row['category'] == 'ordinary'}
    require(ordinary == {row['token'] for row in inventory['cases']}, 'Ordinary candidate reconciliation')
    for row in candidates:
        if row['category'] == 'ordinary':
            continue
        token = row['saved_reference_token']
        case = f'D5AT-{token}'
        quest = (token, row['location']['record_start'], row['category_basis']) == (
            '6a6c44', 1980560, 'KNOWN_BASE_REFERENCE_OCCURRENCE_ONLY')
        inventory['cases'].append(dict(case=case, token=token, body=None,
                                       eligibility='NON_OUTPOST_QUEST' if quest else 'INDETERMINATE',
                                       name=['SQ_OutpostCargoLink'] if quest else [],
                                       record_offset=row['location']['record_start'],
                                       offset_domain=row['location']['domain'], census_category=row['category']))
        unresolved.append(dict(outpost=case, source_id=None,
                               reason='QUEST_REFERENCE_NOT_APPLICABLE' if quest else 'UNCLASSIFIED_BEACON_LIKE_RECORD',
                               count=1))
    c1_prior = load(ROOT / '.local-work/d5aq/census04/census.json')
    c1_coordinates = {tuple(row['query']): row['reference'] for row in c1_prior['cells']}
    require(len(c1_coordinates) == 196, 'D5AQ cohort identity')
    rasters = domains.maps(manifest, {s['body'] for s in sources.values() if s['body'] in manifest['members']})
    witnessed = {f"{row['body'][2:]}/{row['source_key']}": row for row in read_csv(D5I)}
    for key, source in sources.items():
        width, height = source['width'], source['height']
        if key == C1:
            coordinates, contract = c1_coordinates, 'D5AQ-C1'
        else:
            coordinates, contract = domains.attempted_cells(width, height, 2), 'D5AT-INSERTION-ATTEMPT'
        rows, missing = evaluate(source, coordinates, rasters.get(source['body']), constants, crt)
        source.update(contract=contract, descriptor=descriptor(source['chart'], *source['anchor']),
                      cohort_size=len(coordinates), rows=rows, missing=missing)
        if key in witnessed:
            prior = witnessed[key]
            source['qualified_prior'] = prior['id']
            by_cell = {(row['x'], row['y']): row['mask'] for row in rows}
            for prefix in ('lower', 'interior'):
                x, y = map(int, prior[f'{prefix}_query'].split(';'))
                require(by_cell[x - source['anchor'][0], y - source['anchor'][1]] == int(prior[f'{prefix}_mask']),
                        'D5I qualified witness differs')
        if key == C1:
            require(not missing and all(
                {k: v for k, v in row.items() if k not in ('x', 'y')} == c1_coordinates[row['x'], row['y']]
                for row in rows), 'D5AQ row regression mismatch')
            require(Counter(row['mask'] for row in rows) == {0: 28, 3: 168}, 'D5AQ count mismatch')
        else:
            unresolved.append(dict(outpost=None, source_id=key,
                                   reason='ACTUAL_REQUEST_COHORT_AND_EFFECTIVE_FRAME_UNVERIFIED', count=None))
    return dict(outposts=inventory['cases'], independently_framed_records=inventory['independent_records'],
                sources=sources, joins=joins, unresolved=unresolved, floors=floors,
                postflight_floors=guard(), inputs={str(path): digest for path, digest in pins.items()})


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    path = args.output.absolute()
    require(path.is_relative_to(ROOT / '.local-work') and path == path.resolve() and not path.exists(),
            'Fresh local output required')
    result = survey()
    guard()
    write(path, result)
    print(len(result['outposts']), len(result['sources']), len(result['joins']))
