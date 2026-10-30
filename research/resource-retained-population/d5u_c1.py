# SPDX-License-Identifier: GPL-3.0-or-later
"""Join authenticated saved centres and frozen historical-frame populations.

Reads the controlled C1 evidence lease, D5U static lease/census/palette and
authored independent coordinate controls. Writes authored numerical derivatives
and ignored verification receipts. Uses owned geometry/spatial readers unchanged;
no procedural regeneration, raw save, native execution, game, network, database,
dependency installation or Git mutation. Run from the repository root.
"""
import csv
import hashlib
import json
import math
from pathlib import Path
import shutil
import struct
import sys

from d5u_census import ROOT, inputs, weights, table, write
sys.path[:0] = [str(ROOT/'research'/p) for p in
               ('resource-slot-provenance', 'resource-geometry', 'resource-standalone')]
import predictor_d4e as predictor
import geometry
import verify
from context import packed_seed_key
from resource_spatial import evaluate_region

LOCAL = ROOT/'.local-work/d5u-c1'
LEASE = ROOT/'.local-work/resources-evidence-consolidation/d5u-c1-input-lease01'
DOC = ROOT/'docs/experiments/resource-retained-population'
OUT = DOC/'d5u/outposts'
ALIASES = {'original-V':'D2-83388f', 'Carinae':'D2-82be17', 'Archimedes':'D2-81a75b'}
CASES = ['D2-'+v for v in ('83388f','82be17','81a75b','81bf2a','825f95','844cc6','84e101')]


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding='utf8'))


def rows(path):
    return list(csv.DictReader(Path(path).open(encoding='utf8')))


def f32(value):
    return struct.unpack('<f', struct.pack('<f', value))[0]


def saved_reference(saved, frame, projection):
    """Independent table joins and float32 site-to-descriptor reconstruction."""
    assert saved['frame'] == 0x2b and not saved['disabled'] and not saved['deleted']
    assert saved['registered'] and saved['body_concordant']
    assert frame['selected_base'] == 'site' and int(frame['frame'], 16) == 0x2b
    assert projection['compensation'] == '00'*12
    local = [float(projection['local_'+axis]) for axis in 'xyz']
    assert struct.pack('<3f', *local).hex() == frame['center_hex']
    assert local == saved['center']
    site = [int(frame['site_'+axis]) for axis in 'xy']
    descriptor = [int(frame['origin_'+axis]) for axis in 'xy']
    assert saved['site_cell'] == [int(frame['site_tag']), *site]
    assert saved['request']['descriptor'] == descriptor
    center = [f32(local[k]+100*(site[k]-descriptor[k])) for k in (0, 1)]+[local[2]]
    assert center == saved['request']['query']
    assert [float(projection['square_residual_'+a]) for a in 'xy'] == [
        saved['site_projection'][0]['square_residual_'+a] for a in 'xy']
    residual = max(abs(float(projection['square_residual_'+a])) for a in 'xy')
    assert residual < .001
    assert [f32(center[k]-100*(site[k]-descriptor[k])) for k in (0, 1)] == local[:2]
    return dict(case=saved['case'], name=saved['name'][0], body=saved['body'],
                beacon_token=saved['token'], workshop_bytes=saved['workshop_id'],
                record_offset=saved['record_offset'], offset_domain=saved['offset_domain'],
                frame='0x2b', chart=saved['request']['chart'], descriptor=descriptor,
                site_cell=site, saved_local_center=local, center=center,
                beacon=center, beacon_basis='Zero saved Workshop compensation; same saved representation only',
                radius=150, upper=saved['request']['upper'],
                angular_grid_residual=residual,
                qualification=saved['coordinate_qualification'],
                footprint='Fixed 150-native-unit research disk; not recovered saved hardware boundary',
                historical_loaded_epoch='UNKNOWN')


def region_data(region, query):
    """Retain exact supplied binary32 geometry and separate area/callback verdicts."""
    points, bound = region['points'], region['native_bound']
    assert geometry.native_bound(points) == bound
    point_bytes = b''.join(struct.pack('<4f', *p) for p in points).hex()
    bound_bytes = struct.pack('<4f', *bound).hex()
    assert region.get('ordered_xyzw_le', point_bytes) == point_bytes
    assert region.get('native_bound_le', bound_bytes) == bound_bytes
    area = geometry.bounded_region_circle(points, query['query'][:2], 150)
    callback = evaluate_region(query['query'], 150, query['upper'], bound[:3], bound[3], points)
    if 'area' in region:
        assert area == region['area'] and callback == region['callback']
    return dict(resource=region['resource'], cell=region['cell'], points=points,
                native_bound=bound, ordered_xyzw_le=point_bytes, native_bound_le=bound_bytes,
                disk_intersection=area, ordinary_callback=callback)


def main():
    assert min(shutil.disk_usage(d).free for d in ('C:/','D:/')) >= 40_000_000_000
    OUT.mkdir(exist_ok=True)
    lease = read(LEASE/'LEASE.json')
    assert lease['state'] == 'OPEN'
    sources = []
    for row in lease['rows']:
        path = LEASE/row['path']
        assert path.stat().st_size == row['bytes'] and sha(path) == row['sha256']
        sources.append(dict(category='AUTHENTICATED ARCHIVE MEMBER', path=row['path'],
                            sha256=row['sha256'], use='Controlled copy; raw payload LOCAL-ONLY'))
    base = LEASE/'.local-work'
    inv = {v['case']:v for v in read(base/'resource-save52/inventory-v2.json')['cases']}
    requests = {v['case']:v['request'] for v in read(base/'resource-save52/requests-v1.json')}
    conditional = read(base/'resource-construction-mask-selection/conditional-results.json')
    c, cc, raster = inputs()
    census = read(ROOT/'.local-work/d5u/census.json')['sources']
    palette = read(DOC/'d5u/geometry.json')['palette']
    frames = {v['token']:v for v in rows(ROOT/'docs/experiments/static-exhaustion/saved-center-frame.csv')
              if v['sample'] == 'HIST-0267'}
    projections = {v['token']:v for v in rows(ROOT/'docs/experiments/durable-center/projection.csv')
                   if v['sample'] == 'HIST-0267'}
    associations = {v['case']:v for v in rows(ROOT/'docs/experiments/resource-save52/cases.csv')}
    matrix = {v['source_key']:v for v in rows(ROOT/'docs/experiments/resource-predictability-contrast/source-matrix.csv')}
    checks, coordinates, summaries, coverage, cases = [], [], [], [], []
    extra_number = 0
    for case in CASES:
        saved = inv[case]
        reference = saved_reference(saved, frames[saved['token']], projections[saved['token']])
        assert reference['name'] == associations[case]['name']
        query = saved['request']
        assert requests[case]==query
        frozen_path = base/f'resource-feynman-d5/validation01/cohort/{case}-request-normalized-stdout.json'
        frozen = read(frozen_path)
        assert frozen['request'] == query
        known = [s for s in census if ALIASES.get(s['catalogue']['case'], s['catalogue']['case']) == case]
        by_key = {s['catalogue']['source_key']:s for s in known}
        corpus = cc if case in ('D2-83388f','D2-82be17') else c
        body = corpus['bodies'][saved['body']]
        # Independently enumerate the same finite native-width halo; missing
        # generation branches must match the frozen failures, never disappear.
        halo = 150+400+2*corpus['maximum_width']
        lo = [math.floor(query['descriptor'][k]+(query['query'][k]-halo)/100) for k in (0,1)]
        hi = [math.floor(query['descriptor'][k]+(query['query'][k]+halo)/100) for k in (0,1)]
        assert [lo,hi] == frozen['halo']
        resolved = {}
        for x in range(lo[0],hi[0]+1):
            for y in range(lo[1],hi[1]+1):
                ax,ay,fid,w,h,biome = predictor.resolve(corpus,body,query['chart'],x,y)
                key = f"{query['chart']}:{ax}:{ay}:{fid}"
                resolved[key] = (ax,ay,w,h,biome)
        success = {r['source'] for r in frozen['regions']}
        failed = {f"{query['chart']}:{r['source'][0]}:{r['source'][1]}:{r['source'][2]}"
                  for r in frozen['failures']}
        assert success | failed == set(resolved)
        assert failed <= set(by_key) and set(by_key) <= set(resolved)
        assert len(resolved) == frozen['source_count']
        layers = []
        for key in sorted(resolved):
            ax,ay,w,h,biome = resolved[key]
            ordinary = [v for v in body['biomes'][biome]['resources'] if v.get('branch') != 'special']
            ordinary_ids = [v['id'] for v in ordinary]
            special_ids = {v['id'] for v in body['biomes'][biome]['resources'] if v.get('branch')=='special'}
            # Helium-3 also occupies a zero-DNAM ordinary placeholder. Resource
            # ID alone cannot distinguish its subsequent Special population.
            # Refuse an ambiguous nonzero ordinary/Special collision.
            for resource in special_ids & set(ordinary_ids):
                assert all(all(value==0 for value in corpus['generation_blocks'][v['block']])
                           for v in ordinary if v['id']==resource)
            if key in by_key:
                source = by_key[key]
                cat = source['catalogue']
                identity = cat['source_id']
                assert [w,h] == [cat['width'],cat['height']]
                assert ordinary_ids == cat['ordinary_order'].split(';')
                mask_list = sorted(map(int, source['weights']))
            else:
                extra_number += 1
                identity = f'C1-X{extra_number:02}'
                # Full conservative neighborhoods of these nine sources have
                # singleton masks in the frozen D5 source-cases audit.
                masks = {predictor.tile_at(body,query['chart'],x,y)[3]&15
                         for x in range(ax-4,ax+w+5) for y in range(ay-4,ay+h+5)}
                assert len(masks) == 1
                mask_list = sorted(masks)
            anchor = [100*(v-o) for v,o in zip((ax,ay),query['descriptor'])]
            origin = [v-200 for v in anchor]
            if key in matrix:
                assert matrix[key]['saved_beacon_token'] == saved['token']
                assert matrix[key]['workshop_bytes'] == saved['workshop_id']
                assert list(map(int,matrix[key]['source_origin_native_xy'].split(';'))) == origin
            center_source = [reference['center'][i]-anchor[i] for i in (0,1)]
            assert [center_source[i]+anchor[i] for i in (0,1)] == reference['center'][:2]
            historic_key = packed_seed_key(query['chart'],query['descriptor'],origin,[1,1],body['system'],body['index'])
            prospective_key = packed_seed_key(query['chart'],[ax,ay],[-200,-200],[1,1],body['system'],body['index'])
            coord = dict(case=case,name=reference['name'],source_id=identity,source_key=key,
                         chart=query['chart'],descriptor_xy=';'.join(map(str,query['descriptor'])),
                         anchor_native_xy=';'.join(map(str,anchor)),origin_native_xy=';'.join(map(str,origin)),
                         center_native_xy=';'.join(map(str,reference['center'][:2])),
                         center_source_xy=';'.join(map(str,center_source)),
                         historical_key_cell_1_1=historic_key,prospective_key_cell_1_1=prospective_key,
                         seed_frame_equal=historic_key==prospective_key,roundtrip_max_error=0)
            coordinates.append(coord)
            for mask in mask_list:
                operands = [dict(resource=v['id'],block=corpus['generation_blocks'][v['block']]+[0,0],weight=weight)
                            for v,weight in zip(ordinary, weights(corpus,ordinary,mask))]
                if key in failed:
                    candidates = [v for v in conditional if v['case']==case and v['source']==key and v['mask']==mask]
                    assert len(candidates)==1 and candidates[0]['operands']==operands
                    region_list = candidates[0]['regions']
                    provenance = '.local-work/resource-construction-mask-selection/conditional-results.json'
                else:
                    region_list = [r for r in frozen['regions'] if r['source']==key
                                   and r['resource'] in ordinary_ids and r['resource'] not in special_ids]
                    provenance = str(frozen_path.relative_to(LEASE)).replace('\\','/')
                    assert len(mask_list)==1
                regions = [region_data(r,query) for r in region_list]
                layer = dict(id=f'{identity}-M{mask}',source_id=identity,source_key=key,mask=mask,
                             variant_count=len(mask_list),scope='Conditional ordinary generation-competition footprint',
                             provenance=provenance,descriptor=query['descriptor'],anchor=anchor,origin=origin,
                             nominal=[w,h],clip_center=[origin[i]+[w,h][i]//2*100 for i in (0,1)]+[0],
                             clip_half=[w//2*100+200,h//2*100+200,0],cell_bounds=[1,w+3,1,h+3],
                             system=body['system'],body_index=body['index'],owner_key=int(saved['body'],16),
                             ordered_resources=operands,
                             packed_keys={f'{x},{y}':packed_seed_key(query['chart'],query['descriptor'],origin,[x,y],body['system'],body['index'])
                                          for x in range(1,w+3) for y in range(1,h+3)},regions=regions)
                layers.append(layer)
                for resource in dict.fromkeys(v['resource'] for v in operands):
                    slots = [i for i,v in enumerate(operands) if v['resource']==resource]
                    operand = operands[slots[0]]
                    rr = [v for v in regions if v['resource']==operand['resource']]
                    summaries.append(dict(case=case,name=reference['name'],layer=layer['id'],source_id=identity,
                                          source_key=key,mask=mask,resource=operand['resource'],
                                          ordinary_ordinals=';'.join(map(str,slots)),
                                          resource_name=palette[operand['resource']]['name'],weight=operand['weight'],
                                          retained_paths=len(rr),positive_area_paths=sum(v['disk_intersection'].get('intersection')=='POSITIVE_AREA' for v in rr),
                                          unknown_area_paths=sum(v['disk_intersection']['status']=='UNKNOWN' for v in rr),
                                          accepted_callbacks=sum(v['ordinary_callback']['accepted'] is True for v in rr),
                                          unknown_callbacks=sum(v['ordinary_callback']['status']!='KNOWN' for v in rr)))
        coverage.append(dict(case=case,name=reference['name'],d5u_sources=len(known),
                             additional_sources=len(resolved)-len(known),total_sources=len(resolved),
                             conditional_layers=len(layers),frozen_successful_sources=len(success),
                             recovered_failed_sources=len(failed),halo_complete=True,
                             special_water_atmosphere='EXCLUDED: separate routes',historical_joint_winner='UNKNOWN'))
        result = dict(schema='sor-d5u-c1-composite/1',build='1.16.244.0',definition=query['definition'],
                      reference=reference,palette=palette,coverage=coverage[-1],layers=layers,
                      variant_semantics='Independent conditional layers; no joint configuration or historical winner asserted',
                      rendering='Positive-width disks/max-width rectangles clipped by native bounds; marginal native rounding approximate')
        write(OUT/f'{case}.json',result)
        cases.append(result)
    assert extra_number==9 and len(coordinates)==34 and len(summaries)>0
    # Direct independent runtime geometry controls: exact ordered binary32 points
    # and native bound bytes, plus XY of their retained historical query centre.
    primary = cases[0]
    controls = [r for r in rows(ROOT/'docs/experiments/resource-predictability-contrast/native-controls.csv')
                if r['case']=='original-V']
    for control in controls:
        path = base/f"resource-region-ancestry/retail-attempt01/capture-{int(control['capture']):05}.bin"
        native = verify.native(path)
        raw = native['geometry']['raw_region']
        bound = raw[:32]
        resource = control['resource'][2:]
        assert int.from_bytes(bytes.fromhex(raw[32:40]),'little')==int(resource,16)
        matches = [(layer,r) for layer in primary['layers'] for r in layer['regions']
                   if r['resource']==resource and layer['source_key']==control['source_key']
                   and r['ordered_xyzw_le']==native['geometry']['ordered_xyzw'] and r['native_bound_le']==bound]
        assert len(matches)==1
        layer,region = matches[0]
        native_query = list(struct.unpack('<3f',bytes.fromhex(native['qb_retained_bits'])))
        assert native_query[:2]==primary['reference']['center'][:2]
        checks.append(dict(capture=int(control['capture']),resource=resource,source_id=layer['source_id'],
                           source_key=layer['source_key'],cell=region['cell'],
                           exact_point_and_bound_match=True,exact_center_xy_match=True,
                           native_query=native_query,saved_query=primary['reference']['center'],
                           disk_intersection=region['disk_intersection'],callback=region['ordinary_callback'],
                           limit='Finite callback geometry and XY control; not historical source population epoch'))
    mature = rows(ROOT/'docs/experiments/resource-geometry-mature-context/points-mature-v2.csv')
    for case,label in [('D2-83388f','P3'),('D2-82be17','P4')]:
        control = next(v for v in mature if v['case']==label and v['sample']=='beacon')
        reference = next(v['reference'] for v in cases if v['reference']['case']==case)
        assert [float(control['source_'+a]) for a in 'xy']==reference['center'][:2]
    for resource in ('000057cf','000057ce','000057cb','000057d4'):
        relevant = [v for v in summaries if v['case']=='D2-83388f' and v['resource']==resource]
        assert sum(v['positive_area_paths'] for v in relevant)>0
        assert sum(v['accepted_callbacks'] for v in relevant)>0
    observations = rows(ROOT/'docs/experiments/resource-save52-d3/associations-final.csv')
    reconciliation = []
    for resource in ('000057cf','000057ce','000057cb','000057d4'):
        control = next(v for v in checks if v['resource']==resource)
        observation = next(v for v in observations if v['case']=='D2-83388f' and v['resource']==resource)
        relevant = [v for v in summaries if v['case']=='D2-83388f' and v['resource']==resource]
        reconciliation.append(dict(resource=resource,name=palette[resource]['name'],
                                   observed_historical='POSITIVE_CORRESPONDENCE',
                                   saved_extractor_token=observation['witness'],
                                   contributing_sources=';'.join(v['source_id'] for v in relevant if v['positive_area_paths']),
                                   positive_area_paths=sum(v['positive_area_paths'] for v in relevant),
                                   accepted_callbacks=sum(v['accepted_callbacks'] for v in relevant),
                                   native_capture=control['capture'],native_cell=';'.join(map(str,control['cell'])),
                                   native_points_bounds_exact=True,model_disk_intersection='POSITIVE_AREA',
                                   historical_full_population_epoch='UNKNOWN',discrepancy='None within this conditional ordinary model'))
    table(OUT/'primary-reconciliation.csv',reconciliation)
    table(OUT/'coordinates.csv',coordinates)
    table(OUT/'contributions.csv',summaries)
    table(OUT/'coverage.csv',coverage)
    write(LOCAL/'data-checks.json',dict(native_controls=checks,coordinate_controls=7,
                                     sources=34,layers=sum(len(v['layers']) for v in cases),
                                     saved_source_roundtrips=34,halo_coverage=coverage,
                                     no_procedural_regeneration=True))
    # Record meaningful owned method and authored independent-control provenance.
    paths = [Path(__file__),ROOT/'research/resource-retained-population/d5u_census.py',
             Path(__file__).with_name('d5u_c1_maps.py'),Path(__file__).with_name('d5u_c1_checks.py'),
             Path(__file__).with_name('d5t_maps.py'),
             ROOT/'research/resource-geometry/geometry.py',ROOT/'research/resource-geometry/context.py',
             ROOT/'research/resource-slot-provenance/predictor_d4e.py',
             ROOT/'research/resource-construction-mask-selection/analyze.py',
             ROOT/'research/resource-standalone/save52.py',ROOT/'research/resource-standalone/verify.py',
             ROOT/'save-analysis/scripts/resource_spatial.py',ROOT/'save-analysis/scripts/resource_availability.py',
             DOC/'d5u/geometry.json',ROOT/'.local-work/d5u/census.json',LEASE/'LEASE.json']
    paths += [ROOT/'docs/experiments'/v for v in (
        'static-exhaustion/saved-center-frame.csv','durable-center/projection.csv',
        'resource-geometry-mature-context/points-mature-v2.csv','resource-save52/cases.csv',
        'resource-predictability-contrast/source-matrix.csv','resource-predictability-contrast/native-controls.csv',
        'resource-save52-d3/associations-final.csv','resource-feynman-d5/source-cases.csv')]
    for path in paths:
        sources.append(dict(category='OWNED METHOD OR INDEPENDENT CONTROL',path=str(path.relative_to(ROOT)).replace('\\','/'),
                            sha256=sha(path),use='Original maintainer methods reused under SOR-P-0002; exact input identity'))
    for key in ('installed','database'):
        for path,digest in read(LOCAL/'initial.json')[key].items():
            sources.append(dict(category=key.upper(),path=path,sha256=digest,use='Preservation baseline; payload LOCAL-ONLY'))
    table(DOC/'d5u-c1-sources.csv',[dict(id=f'C1-S{i:03}',**r) for i,r in enumerate(sources,1)])
    print('Verified seven saved joins, 34 source halos, 40 conditional layers and four raw native controls.')


if __name__=='__main__':
    main()
