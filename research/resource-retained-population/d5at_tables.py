# SPDX-License-Identifier: GPL-3.0-or-later
"""Export review-required derived tables from a checked D5AT receipt.

Reads the linked survey and audit JSON. Writes exclusive CSV and grid files
under a caller-selected new directory inside the repository. No raw save,
resource raster, process, target or Git operations.
"""
import os
import sys

if sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):
    raise RuntimeError('Use pinned Python -E -B without optimization')

from collections import defaultdict
import csv
import json
from pathlib import Path

import d5at_survey as s
from d5at_audit import distribution


HAB_INPUT = s.ROOT / 'docs/experiments/workshop-population/candidates.csv'
HAB_SHA = 'c0a1689310b3a372f8b5637c36389d9b90afe22895f5d74d959d8a0f7ee3390a'
HAB_GROUPS = {'DYNAMIC:ff01b58f': 'DYNAMIC:ff01b59b', 'DYNAMIC:ff0483f2': 'DYNAMIC:ff05d48a'}
HAB_QUALIFICATION = 'UNRESOLVED_HISTORICAL_HAB_OWNERSHIP'


def csv_table(output, name, rows):
    with (output / f'{name}.csv').open('x', encoding='utf8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


def encoded(value):
    return json.dumps(value, separators=(',', ':'), allow_nan=False)


def known(value):
    return 'UNKNOWN' if value is None else value


def summary(source):
    values = distribution(source['rows'])
    counts = {f'0x{mask:x}': count for mask, count in values['counts'].items()}
    complete = not source['missing']
    result = dict(source_id=source['source_id'], body='0x'+source['body'], chart=source['chart'],
                  anchor=encoded(source['anchor']), block='0x'+source['block'],
                  biome='0x'+source['biome'], sfpt=source['sfpt'],
                  effective_rsgd=source.get('effective_rsgd', 'UNKNOWN'),
                  width=source['width'], height=source['height'], descriptor=encoded(source['descriptor']),
                  contract=source['contract'], cohort_size=source['cohort_size'],
                  qualified_prior=source.get('qualified_prior', 'NONE'),
                  sampled=len(source['rows']), unresolved=len(source['missing']),
                  counts=encoded(counts),
                  shares=encoded({mask: count / len(source['rows']) for mask, count in counts.items()}),
                  classes=len(counts), largest_share=known(values['largest_share']),
                  effective_classes=values['effective_classes'] if counts else 'UNKNOWN',
                  rank_eligible=bool(counts) and complete)
    return result


def rank(joins, sources, outposts):
    rows = []
    for join in joins:
        if join['qualification'] != 'PLAUSIBLE_SOURCE_CANDIDATE':
            continue
        source = sources[join['source_id']]
        rows.append(dict(outpost=join['outpost'], qualification=join['qualification'],
                         provenance=join['provenance'], **source))
    rows.sort(key=lambda row: (
        not row['rank_eligible'], row['classes'] != 2, row['classes'] < 2,
        row['largest_share'] if row['rank_eligible'] and row['classes'] == 2 else 0,
        -row['effective_classes'] if row['rank_eligible'] else 0,
        row['outpost'], row['source_id']))
    for outpost in outposts:
        qualification = ('NOT_APPLICABLE' if outpost['saved_state'] == 'NON_OUTPOST_QUEST'
                         else 'UNRESOLVED_SOURCE_COVERAGE')
        rows.append(dict(outpost=outpost['outpost'], source_id='UNKNOWN',
                         qualification=qualification,
                         contract='UNKNOWN', rank_eligible=False))
    for join in joins:
        if join['qualification'] == HAB_QUALIFICATION:
            rows.append(dict(join, contract='UNKNOWN', rank_eligible=False))
    index = 0
    result = []
    for row in rows:
        if row['rank_eligible']:
            index += 1
        result.append(dict(rank=index if row['rank_eligible'] else 'UNRANKED', **row))
    fields = [*result[0], 'related_saved_identity']
    return [{field: row.get(field, 'UNKNOWN') for field in fields} for row in result]


def hab_associations(outposts):
    s.require(s.sha(HAB_INPUT) == HAB_SHA, 'Workshop candidate input identity')
    disabled = {f"DYNAMIC:{0xff000000 | (int(row['saved_token'], 16) & 0x3fffff):08x}": row['outpost']
                for row in outposts if row['saved_state'] == 'DISABLED'}
    results = []
    with HAB_INPUT.open(encoding='utf-8', newline='') as stream:
        for row in csv.DictReader(stream):
            parent, group = row['historical_beacon_context'], row['canonical_group']
            if HAB_GROUPS.get(parent) != group or row['group_identity'] != group:
                continue
            s.require(row['ordinary_owner'] == 'UNRESOLVED' and parent in disabled, 'Hab ownership or beacon changed')
            results.append(dict(outpost=disabled[parent], source_id='UNKNOWN', qualification=HAB_QUALIFICATION,
                                provenance='Typed Workshop clone location and historical beacon context',
                                related_saved_identity=group))
    s.require({row['related_saved_identity'] for row in results} == set(HAB_GROUPS.values())
              and len(results) == len(HAB_GROUPS), 'Historical Hab coverage changed')
    return results


def main(receipt, audit, output):
    s.guard()
    s.require(s.sha(sys.executable) == s.PINNED[Path(sys.executable)], 'Interpreter pin')
    s.require(s.sha(receipt) == s.load(audit)['survey_sha256'], 'Audit covers a different survey')
    data = s.load(receipt)
    outposts = []
    for row in data['outposts']:
        request = row.get('request')
        outposts.append(dict(outpost=row['case'], saved_token=row['token'], offset=row['record_offset'],
                             offset_domain=row['offset_domain'], label=(row.get('name') or ['UNKNOWN'])[0],
                             saved_state=row['eligibility'], body=known(row['body']),
                             body_concordant=known(row.get('body_concordant')),
                             saved_parent=known(row.get('parent')), workshop_id=known(row.get('workshop_id')),
                             disabled=known(row.get('disabled')), registered=known(row.get('registered')),
                             saved_descriptor=known(row.get('descriptor_key')),
                             saved_frame=hex(row['frame']) if row.get('frame') is not None else 'UNKNOWN',
                             local_center=encoded(row['center']) if row.get('center') else 'UNKNOWN',
                             site_cell=encoded(row['site_cell']) if row.get('site_cell') else 'UNKNOWN',
                             translated_center=encoded(request['query']) if request else 'UNKNOWN',
                             provenance='Save52 archived D2 inventory and fresh D5AT R3 audit'))
    sources = {key: summary(source) for key, source in sorted(data['sources'].items())}
    habs = hab_associations(outposts)
    joins = sorted([dict(row, related_saved_identity='UNKNOWN') for row in data['joins']] + habs,
                   key=lambda row: (row['outpost'], row['source_id'], row['qualification']))
    unresolved = [dict(row, outpost=known(row['outpost']), source_id=known(row['source_id']),
                       count=known(row['count']), related_saved_identity='UNKNOWN') for row in data['unresolved']]
    unresolved.extend(dict(outpost=row['outpost'], source_id='UNKNOWN', reason=HAB_QUALIFICATION,
                           count='UNKNOWN', related_saved_identity=row['related_saved_identity']) for row in habs)
    request_rows, grids = [], {}
    for key in sources:
        source = data['sources'][key]
        grid = defaultdict(dict)
        for row in source['rows'] + source['missing']:
            value = 'UNKNOWN' if 'reason' in row else f"0x{row['mask']:x}"
            sample_class = 'UNRESOLVED'
            if value != 'UNKNOWN':
                sample_class = ('DIRECT_N2' if key == s.C1 and (row['x'], row['y']) == (-2, 11)
                                else 'CONDITIONAL')
            grid[row['y']][row['x']] = '?' if value == 'UNKNOWN' else value[-1]
            request_rows.append(dict(source_id=key, contract=source['contract'], x=row['x'], y=row['y'],
                                     atlas_face=known(row.get('chart')), column=known(row.get('column')),
                                     row=known(row.get('row')), raster_byte=hex(row['byte']) if 'byte' in row else 'UNKNOWN',
                                     mask=value, sample_class=sample_class, unresolved_reason=row.get('reason', 'NONE')))
        grids[key] = dict(x_min=min(min(row) for row in grid.values()), y_min=min(grid),
                          ascending_y=[''.join(row[x] for x in sorted(row)) for _, row in sorted(grid.items())])
    ranking = rank(joins, sources, outposts)
    s.require({row['source_id'] for row in ranking} - {'UNKNOWN'} == set(sources), 'Ranking drops a source')
    output.mkdir()
    for name, rows in (
        ('outposts', outposts), ('outpost-source-joins', joins), ('request-masks', request_rows),
        ('source-distributions', list(sources.values())), ('candidate-ranking', ranking), ('unresolved', unresolved),
    ):
        csv_table(output, name, rows)
    s.write(output / 'mask-grids.json', grids)
    print(f'{len(outposts)} records, {len(joins)} joins, {len(sources)} sources, {len(request_rows)} samples')


if __name__ == '__main__':
    if len(sys.argv) != 4:
        raise SystemExit('Usage: d5at_tables.py SURVEY_JSON AUDIT_JSON FRESH_OUTPUT_DIRECTORY')
    survey, audit, output = map(Path, sys.argv[1:])
    output = output.absolute()
    s.require(output.is_relative_to(s.ROOT) and output == output.resolve() and not output.exists(),
              'Fresh repository output required')
    main(survey, audit, output)
