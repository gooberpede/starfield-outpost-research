# SPDX-License-Identifier: GPL-3.0-or-later
"""Reframe Save52 and audit the D5AT tables by a separate atlas calculation.

Reads the physical save, installed maps and the producer receipt. The owned
D2 frame readers and D5H map decoder are shared. The audit checks interior
atlas cells by integer indexing and cross-checks the historical native masks.
The decoder uses disposable scratch. The audit writes an exclusive local receipt.
"""
import os
import sys

if sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):
    raise RuntimeError('Use pinned Python -E -B without optimization')

from collections import Counter
from copy import deepcopy
import math
from pathlib import Path

import d5at_survey as s
import save52
from ordinary_outpost_beacons import catalog_for, summarize
from test_outpost_record_framing import independent


def audit_roster(receipt, scratch):
    from stream_save import disk_guard

    def guard(path, reserve):
        s.guard()
        disk_guard(path, reserve)

    definitions = s.ROOT / '.local-work/membership-completion/definitions-01/definitions.json'
    definition_sha = 'd48c67bba2c82603bbed9cc66039b36e24c056509b4fcc9ec37da6c7b5aa1c83'
    s.require(s.sha(definitions) == definition_sha, 'Expanded definition catalog changed')
    with save52.decoded_save(save52.source(), scratch, guard=guard) as (decoded, metrics):
        directory = save52.directory(decoded)
        bounds = directory['regions']['region_R3']
        count = directory['words'][9]
        records = independent(decoded, *bounds, count)
        original = summarize(decoded, dict(direct_bases={0x2c60e9: 'OutpostBeaconActivator'}, templates={}))
        catalog, _ = catalog_for(decoded, s.load(definitions))
        expanded = summarize(decoded, catalog)
        registered = [row['parsed']['beacons'] for row in save52.envelopes(decoded, directory)
                      if row['qualifies'] and 'parsed' in row]
        s.require(len(registered) == 1, 'Registration envelope is ambiguous')
    s.require(len(records) == receipt['independently_framed_records'], 'R3 arithmetic census mismatch')
    expected = {(row['saved_reference_token'], row['location']['record_start']): row for row in original['candidates']}
    observed = {(row['token'], row['record_offset']): row for row in receipt['outposts']}
    s.require(len(expected) == len(observed) == len(receipt['outposts']) and expected.keys() == observed.keys(),
              'Save52 beacon record identities differ')
    for key, row in observed.items():
        if expected[key]['category'] == 'ordinary':
            state = 'EXPLICITLY_SET' if row['disabled'] else 'EXPLICITLY_CLEAR'
            s.require(state == expected[key]['disabled_state'] and row['registered'] == (row['token'] in registered[0]),
                      'Saved disabled or registration state mismatch')
    extra = [row for row in expanded['candidates']
             if (row['saved_reference_token'], row['location']['record_start']) not in expected]
    return dict(framed_records=len(records), candidate_records=len(expected), counts=original['counts'],
                expanded_catalog=dict(digest=definition_sha, bases=len(catalog['direct_bases']),
                                      templates=len(catalog['templates']), counts=expanded['counts'],
                                      additional_candidates=extra, coverage=expanded['coverage']),
                decoded_sha256=metrics['decoded_sha256'])


def expected_joins():
    """Build expected outpost relations from the pinned upstream inputs."""
    from itertools import product

    inventory = s.load(s.LEASE / 'resource-save52/inventory-v2.json')
    corpora = [s.validate(s.load(s.LEASE / 'resource-save52-d3/build-v6/normalized.json')),
               s.load(s.D5)['payload']]
    pairs = set()
    for case in inventory['cases']:
        req = case['request']
        if not req or not case['body_concordant']:
            continue
        x, y = req['descriptor']
        qx, qy = req['query'][:2]
        for corpus in corpora:
            if req['body'] not in corpus['bodies']:
                continue
            spread = (req['radius'] + 400 + 2 * corpus['maximum_width']) / 100
            for ix, iy in product(
                range(math.floor(x + qx / 100 - spread), math.floor(x + qx / 100 + spread) + 1),
                range(math.floor(y + qy / 100 - spread), math.floor(y + qy / 100 + spread) + 1),
            ):
                try:
                    ax, ay, block, *_ = s.resolve(corpus, corpus['bodies'][req['body']], req['chart'], ix, iy)
                except (KeyError, ValueError):
                    continue
                pairs.add((case['case'], f"{req['body']}/{req['chart']}:{ax}:{ay}:{block}"))
    aliases = {'Archimedes': 'D2-81a75b', 'Carinae': 'D2-82be17', 'original-V': 'D2-83388f'}
    for row in s.read_csv(s.ROOT / 'docs/experiments/resource-query-reachability/source-domains.csv'):
        pairs.add((aliases.get(row['case'], row['case']), f"{row['body'][2:]}/{row['source_key']}"))
    disk_controls = set()
    for row in s.read_csv(s.COMPOSITES / 'coordinates.csv'):
        body = next(case['body'] for case in inventory['cases'] if case['case'] == row['case'])
        pairs.add((row['case'], f"{body}/{row['source_key']}"))
        if row['case'] == 'D2-83388f' and row['source_id'] in ('U01', 'U02'):
            disk_controls.add((row['case'], f"{body}/{row['source_key']}", 'VERIFIED_RESEARCH_DISK_INTERSECTION'))
    return ({(*pair, 'PLAUSIBLE_SOURCE_CANDIDATE') for pair in pairs} | disk_controls |
            {('D2-84e101', s.C1, 'RESIDENT_ONLY')})


def audit_tables(receipt, rasters, expected_relations):
    cases = {row['case']: row for row in receipt['outposts']}
    sources = receipt['sources']
    linked = set()
    joins = set()
    for row in receipt['joins']:
        outpost, key = row['outpost'], row['source_id']
        identity = outpost, key, row['qualification']
        s.require(identity not in joins and cases[outpost]['body'] == sources[key]['body'],
                  'Duplicate or wrong-body source join')
        joins.add(identity)
        linked.add(key)
    s.require(linked == set(sources), 'Unjoined source missing from the ranking population')
    s.require(joins == expected_relations, 'Outpost-specific relation inventory differs')
    unknown = {row['outpost'] for row in receipt['unresolved'] if row['outpost']}
    s.require(set(cases) <= unknown, 'Outpost without an explicit coverage disposition')
    for key, source in sources.items():
        ax, ay = source['anchor']
        s.require(key == source['source_id'] == f"{source['body']}/{source['chart']}:{ax}:{ay}:{source['block']}",
                  'Source key and operands disagree')
        width, height = (10, 10) if key == s.C1 else (source['width'], source['height'])
        expected = {(x, y) for x in range(-2, width + 2) for y in range(-2, height + 2)}
        rows = source['rows'] + source['missing']
        actual = {(row['x'], row['y']) for row in rows}
        s.require(actual == expected and len(rows) == len(expected) == source['cohort_size'],
                  'Missing, extra or duplicate coordinate')
        face = source['chart']
        ax, ay = source['anchor']
        for row in source['rows']:
            x, y = ax + row['x'], ay + row['y']
            s.require(0 <= x < 49152 and 0 <= y < 49152, 'Unqualified face transition')
            column, raster_row = x // 192, 255 - y // 192
            value = rasters[source['body']]['faces'][face]['mask'][256 * raster_row + column]
            s.require((row['chart'], row['column'], row['row'], row['byte'], row['mask']) ==
                      (face, column, raster_row, value, value % 16), 'Integer atlas audit disagrees')
    return len(joins)


def distribution(rows):
    counts = Counter(row['mask'] for row in rows)
    total = sum(counts.values())
    shares = [n / total for n in counts.values()]
    entropy = -sum(p * math.log2(p) for p in shares)
    return dict(counts=dict(sorted(counts.items())), effective_classes=2 ** entropy,
                largest_share=max(shares, default=None))


def main(path, output):
    s.guard()
    s.require(s.sha(sys.executable) == s.PINNED[Path(sys.executable)], 'Interpreter pin')
    receipt = s.load(path)
    for source, digest in receipt['inputs'].items():
        s.require(s.sha(source) == digest, 'Survey input differs from the audit input')
    rasters = s.domains.maps(s.load(s.LEASE / 'resource-save52/build-v1/manifest.json'),
                             {row['body'] for row in receipt['sources'].values() if row['rows']})
    roster = audit_roster(receipt, output.with_suffix('.scratch'))
    expected_relations = expected_joins()
    count = audit_tables(receipt, rasters, expected_relations)
    c1 = {(row['x'], row['y']): row['mask'] for row in receipt['sources'][s.C1]['rows']}
    native = s.load(s.ROOT / '.local-work/d5aq/startup-native05/receipt.json')['rows']
    s.require({(r['branch'], *r['original_int2']) for r in native} ==
              {(branch, *q) for branch in ('fma', 'nonfused') for q in c1} and
              len(native) == 392 and all(c1[tuple(r['original_int2'])] == r['mask'] for r in native),
              'D5AQ both-branch historical native control')
    controls = []
    for label, corrupt in (
        ('wrong_body', lambda d: d['joins'][0].update(outpost='D2-832210')),
        ('missing_join', lambda d: d.update(joins=[r for r in d['joins'] if r['source_id'] != s.C1])),
        ('same_body_wrong_outpost', lambda d: next(r for r in d['joins']
          if r['source_id'] == s.C1 and r['qualification'] == 'PLAUSIBLE_SOURCE_CANDIDATE').update(outpost='D2-83388f')),
        ('missing_plausible_join', lambda d: d.update(joins=[r for r in d['joins']
          if (r['source_id'], r['qualification']) != (s.C1, 'PLAUSIBLE_SOURCE_CANDIDATE')])),
        ('wrong_key_fields', lambda d: d['sources'][s.C1].update(block='0024ef55')),
        ('duplicate_request', lambda d: d['sources'][s.C1]['rows'].append(d['sources'][s.C1]['rows'][0])),
        ('wrong_atlas_byte', lambda d: d['sources'][s.C1]['rows'][0].update(byte=255)),
    ):
        altered = deepcopy(receipt)
        corrupt(altered)
        try:
            audit_tables(altered, rasters, expected_relations)
        except ValueError:
            controls.append(label)
        else:
            raise ValueError(f'Failed to detect {label}')
    for desc, query, raster, label in (
        ((0, (0, 0), (0, 0), (0, 0)), (-1, 0), rasters['0005e0de'], 'face_underflow'),
        ((1, (255, 255), (15, 15), (11, 11)), (0, 1), rasters['0005e0de'], 'face_overflow'),
        ((2, (0, 0), (0, 0), (0, 0)), (0, 0), rasters['0005e0de'], 'unknown_chart'),
        ((0, (0, 0), (0, 0), (0, 0)), (0, 0), None, 'missing_raster'),
    ):
        try:
            s.sample(desc, query, raster)
        except ValueError:
            controls.append(label)
        else:
            raise ValueError(f'Failed to detect {label}')
    fixture = distribution([{'mask': mask} for mask in (0, 3, 8, 8)])
    s.require(fixture['counts'] == {0: 1, 3: 1, 8: 2} and fixture['effective_classes'] > 2.8,
              'Three-class summary lost a class')
    corner = [dict(mask=s.sample(s.descriptor(0, 37440, 20928), (x, y), rasters['0005e0de'])['mask'])
              for x in range(-2, 12) for y in range(-2, 12)]
    corner = distribution(corner)
    s.require(corner['counts'] == {0: 24, 1: 4, 3: 168}, 'D5U U26 three-mask control')
    changed = Counter(s.sample((0, (195, 109), (8, 0), (0, 1)), q, rasters['0005e0de'])['mask'] for q in c1)
    s.require(changed == {0: 14, 3: 182}, 'Descriptor phase control')
    s.guard()
    s.write(output, dict(roster=roster, joins=count, survey_sha256=s.sha(path), native_samples=len(native),
                         refused=controls, three_class_fixture=fixture,
                         d5u_three_class_control=corner,
                         changed_descriptor_counts=changed, floors=s.guard()))
    print('Save52 roster, atlas arithmetic, both native branches and adverse cases passed')


if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise SystemExit('Usage: d5at_audit.py SURVEY_JSON FRESH_LOCAL_AUDIT_JSON')
    path, output = map(Path, sys.argv[1:])
    output = output.absolute()
    s.require(output.is_relative_to(s.ROOT / '.local-work') and output == output.resolve()
              and not output.exists(), 'Fresh local output required')
    main(path, output)
