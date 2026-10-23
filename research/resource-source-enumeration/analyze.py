# SPDX-License-Identifier: GPL-3.0-or-later
"""C2C offline source-selection discrimination and whole-source diagnostic.

Reads existing owned derivatives, frozen requests, native receipts and exports.
Uses stdlib and unchanged project math; writes exclusive ignored JSON outputs.
No target, save, configuration, database, network or Git mutation. Run at root.
Candidate coverage varies compatible surface patterns, never generator seeds.
It is an uncertainty envelope, not a reconstructed native selected-source map.
"""
import argparse
import collections
import copy
import hashlib
import json
from pathlib import Path
import struct
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT/'research/resource-geometry'),
               str(ROOT/'research/resource-carinae-source-context'),
               str(ROOT/'save-analysis/scripts')]
import context
import geometry
from qualify import independent
from resource_spatial import evaluate_region


def pin(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def last(record, tag):
    return bytes.fromhex(next(v for t, v in reversed(record['fields']) if t == tag))


def inputs():
    rows = json.loads((ROOT/'.local-work/resource-geometry/source-definitions01.json').read_text())['records']
    styles = {r['formid']:int.from_bytes(last(r, 'NNAM'), 'little') for r in rows
              if r['type']=='BIOM' and any(t=='NNAM' for t, v in r['fields'])}
    blocks = {r['formid']:dict(dimensions=struct.unpack('<II', last(r, 'DNAM')))
              for r in rows if r['type']=='SFBK'}
    patterns = {r['formid']:dict(entries=list(zip(struct.unpack('<256I', last(r, 'FNAM')), last(r, 'GNAM'))))
                for r in rows if r['type']=='SFPT' and any(t=='CNAM' for t, v in r['fields'])}
    registry = [dict(id=r['formid'], style=int.from_bytes(last(r, 'CNAM'), 'little'))
                for r in rows if r['formid'] in patterns]
    return styles, blocks, patterns, registry


def possible_sources(frozen, selected, patterns, blocks, styles, registry):
    """Resolve every halo cell under every installed style-compatible pattern.

    Keeps the frozen no-whole-pattern-rotation initialization assumption. Pattern
    choice is a candidate dimension; no row asserts actual runtime selection.
    Missing anchors are reported, never silently converted into empty sources.
    """
    lo, hi = frozen['halo']['owner_cell_bounds']
    sources, failures, choices = {}, [], {}
    for x in range(lo[0], hi[0]+1):
        for y in range(lo[1], hi[1]+1):
            cx, cy = x//192, y//192
            slot = cx*256+cy
            biome = context.map_lookup(selected['map'], frozen['tag'], x, y)
            candidates = [r['id'] for r in registry if r['style']==styles.get(biome)]
            choices[f'{cx},{cy}'] = candidates
            prior = selected['tables'][frozen['tag']][slot]
            try:
                for pid in candidates:
                    selected['tables'][frozen['tag']][slot] = (pid, 8)
                    try:
                        source = context.source_at(frozen['tag'], x, y, frozen['origin'],
                                                   selected, patterns, blocks, padding=2)
                    except ValueError as error:
                        failures.append(dict(cell=[x,y], pattern=f'0x{pid:08x}', reason=str(error)))
                        continue
                    key = (source['id'], source['pattern'], source['source_flags'])
                    sources[key] = source
            finally:
                selected['tables'][frozen['tag']][slot] = prior
    return list(sources.values()), failures, choices


def signature(region):
    return struct.pack('<4f', *region['native_bound']) + b''.join(struct.pack('<4f', *p) for p in region['points'])


def witnessed_inventory(frozen, selected, patterns, blocks, witnesses):
    """Use retained coarse-pattern witnesses, never a supplied local anchor.

    Unwitnessed coarse cells retain explicitly conditional initialization inputs.
    Failed anchor resolutions remain unknown coverage pending native fallback.
    """
    selected = copy.deepcopy(selected)
    for w in witnesses:
        cx,cy=w['coarse']
        selected['tables'][w['tag']][cx*256+cy]=(int(w['pattern'],16),w['pattern_flags'])
    lo,hi=frozen['halo']['owner_cell_bounds']
    sources,failures={},[]
    for x in range(lo[0],hi[0]+1):
        for y in range(lo[1],hi[1]+1):
            try:
                s=context.source_at(frozen['tag'],x,y,frozen['origin'],selected,patterns,blocks,padding=2)
            except ValueError as error:
                failures.append(dict(cell=[x,y],reason=str(error)))
                continue
            sources[s['id']]=s
    return list(sources.values()),failures


def reframe(request, source, frozen):
    """Rebuild all spatial operands together, preserving complete resource order."""
    req = copy.deepcopy(request)
    req.update(source=source['id'], origin=source['origin'], clip_center=source['clip_center'],
               clip_half=source['clip_half'], cell_bounds=source['cell_bounds'])
    x0,x1,y0,y1 = source['cell_bounds']
    req['packed_keys'] = {f'{x},{y}':context.packed_seed_key(frozen['tag'], frozen['origin'],
                            source['origin'], [x,y], frozen['system'], frozen['index'])
                          for x in range(x0,x1) for y in range(y0,y1)}
    req['provenance'] = 'C2C conditional installed whole-source diagnostic; historical producer operands unobserved'
    return req


def run(output):
    assert output.resolve().is_relative_to(ROOT/'.local-work/resource-source-enumeration') and not output.exists()
    styles, blocks, patterns, registry = inputs()
    full_path = ROOT/'.local-work/resource-installed-settings/c2b-geometry01.json'
    full = json.loads(full_path.read_text())
    paths = [full_path, ROOT/'.local-work/resource-geometry/source-definitions01.json',
             ROOT/'.local-work/resource-milestone-b-spatial-constants.json', Path(__file__),
             ROOT/'research/resource-geometry/context.py', ROOT/'research/resource-geometry/geometry.py']
    paths += [ROOT/f'.local-work/resource-geometry-mature-context/site-{s}-initial02.json' for s in ('carinae','feynman')]
    paths += [ROOT/f'.local-work/outpost-biomes/{s}.biom' for s in ('carinae iii-a','feynman v')]
    paths += [ROOT/f'.local-work/resource-carinae-source-context/retail-attempt02/capture-{n:05d}.bin' for n in (84,94,115,2587)]
    paths += [ROOT/f'.local-work/resource-carinae/retail-attempt02/capture-{n:05d}.bin' for n in (1270,1280,1301,2587)]
    before = {str(p):pin(p) for p in paths}
    result = dict(schema='sor-c2c-source-analysis/1', publication='REVIEW-REQUIRED', inputs=before, sites=[])
    for site in ('Carinae', 'Feynman'):
        frozen = json.loads((ROOT/f'.local-work/resource-geometry-mature-context/site-{site.lower()}-initial02.json').read_text())
        m = context.read_map((ROOT/f'.local-work/outpost-biomes/{"carinae iii-a" if site=="Carinae" else "feynman v"}.biom').read_bytes())
        selected = context.select_patterns(m, styles, registry, frozen['system'], frozen['index'])
        selected['map'] = m
        halo = context.neighborhood(frozen['tag'], frozen['origin'], frozen['center'],
                  frozen['halo']['halo_native']-400-2*frozen['halo']['maximum_width'],
                  selected, patterns, blocks, maximum_width=frozen['halo']['maximum_width'])
        assert halo['owner_cell_bounds']==frozen['halo']['owner_cell_bounds']
        assert {s['id'] for s in halo['sources']}=={s['source']['id'] for s in frozen['sources']}
        proposed, failures, choices = possible_sources(frozen, selected, patterns, blocks, styles, registry)
        row = dict(site=site, frame=frozen['origin'], center=frozen['center'], halo=frozen['halo'],
                   before=[s['source'] for s in frozen['sources']], candidate_after=proposed,
                   failures=failures, compatible_patterns=choices,
                   native_selection='UNKNOWN; candidate envelope is not native source census')
        result['sites'].append(row)
        if site!='Carinae':
            continue
        captures = [independent(ROOT/f'.local-work/resource-carinae-source-context/retail-attempt02/capture-{n:05d}.bin')[1] for n in (84,94,115)]
        transfer = independent(ROOT/'.local-work/resource-carinae-source-context/retail-attempt02/capture-02587.bin')[1]
        decoded = []
        for r in captures:
            assert all(r[k]==transfer[k] for k in ('pid','tid','thread_lifetime','updater_token'))
            b = bytes.fromhex(r['source_context']['raw_source'])
            assert len(b)==0x70 and r['source_context']['status']=='COMPLETE'
            decoded.append(dict(block=f'0x{struct.unpack_from("<I",b)[0]:08x}',
                tag=b[0x38],coarse=list(struct.unpack_from('<2i',b,0x3c)),
                pattern=f'0x{struct.unpack_from("<I",b,0x44)[0]:08x}',
                pattern_flags=b[0x48], sub=list(struct.unpack_from('<2i', b, 0x4c)),
                source_block=f'0x{struct.unpack_from("<I",b,0x54)[0]:08x}',
                source_flags=b[0x58], raw_sha256=hashlib.sha256(b).hexdigest()))
        assert decoded[0]==decoded[1]==decoded[2]
        observed = decoded[0]
        pid = int(observed['pattern'],16)
        slot = observed['coarse'][0]*256+observed['coarse'][1]
        base_pid = selected['tables'][0][slot][0]
        after, unresolved = witnessed_inventory(frozen,selected,patterns,blocks,[observed])
        row.update(after=after,after_unresolved_cells=unresolved)
        # Diagnostic selection comes from copied constructor fields, independently
        # of geometry. The candidate envelope above never consults these fields.
        selected['tables'][0][slot] = (pid, observed['pattern_flags'])
        source = context.source_at(0, 21396,15636,frozen['origin'],selected,patterns,blocks,padding=2)
        assert source['block']==int(observed['block'],16) and source['source_flags']==observed['source_flags']
        assert source['local_cell_origin']==[-12,-12] and source['dimensions']==[10,10]
        assert source in proposed
        row.update(observed=observed, frozen_pattern=f'0x{base_pid:08x}', diagnostic_source=source,
                   observed_anchor_inside_old_halo=all(frozen['halo']['owner_cell_bounds'][0][k]<=source['geographic_origin'][k]<=frozen['halo']['owner_cell_bounds'][1][k] for k in (0,1)))
        old_sources = [s for s in full if s['site']==site]
        template = next(s for s in old_sources if s['request']['cell_bounds']==source['cell_bounds'])
        assert all(s['request']['ordered_resources']==template['request']['ordered_resources']
                   and s['request']['owner_key']==386266 for s in old_sources)
        assert all(source['resource_biome']==s['source']['resource_biome'] for s in frozen['sources'])
        req = reframe(template['request'],source,frozen)
        constants = {int(c['va'],16):c['float'] for c in json.loads((ROOT/'.local-work/resource-milestone-b-spatial-constants.json').read_text())['constants']}
        constants.update({int(c['va'],16):c['value'] for c in frozen['constants']})
        generated = geometry.populate_source(req,constants)
        assert generated['status']=='CONDITIONAL_PLANAR_SOURCE'
        regions = generated['regions']
        comparisons=[]
        for n in (1270,1280,1301):
            r=independent(ROOT/f'.local-work/resource-carinae/retail-attempt02/capture-{n:05d}.bin')[1]
            fid=f'{struct.unpack_from("<I",bytes.fromhex(r["selected"]["raw_resource"]),0x28)[0]:08x}'
            native=dict(points=list(struct.iter_unpack('<4f',bytes.fromhex(r['geometry']['ordered_xyzw']))),
                        native_bound=struct.unpack_from('<4f',bytes.fromhex(r['geometry']['raw_region'])))
            matches=[g for g in regions if g['resource']==fid and signature(g)==signature(native)]
            comparisons.append(dict(resource='0x'+fid,capture=n,exact_matches=len(matches),
                                    cells=[g['cell'] for g in matches],native_sha256=hashlib.sha256(signature(native)).hexdigest()))
        native_query = captures[0]
        q = struct.unpack('<3f',bytes.fromhex(native_query['qb_retained_bits']))
        radius,upper=struct.unpack_from('<2f',bytes.fromhex(native_query['raw_closure']),16)
        hits=[dict(resource='0x'+g['resource'],cell=g['cell']) for g in regions if evaluate_region(q,radius,upper,g['native_bound'][:3],g['native_bound'][3],g['points'])['accepted']]
        row['replay']=dict(request=req,comparisons=comparisons,paths=len(regions),
                           per_resource=dict(collections.Counter(g['resource'] for g in regions)),
                           query=dict(xyz=q,radius=radius,upper=upper,positive_paths=hits),
                           historical_inputs='UNKNOWN; current copied descriptor plus installed BIOM/RSGD/order/mask/settings',
                           generated_regions=regions)
        selected_regions=[]
        for s in after:
            assert s['resource_biome']==source['resource_biome']
            ax,ay=s['geographic_origin'];dx,dy=s['dimensions']
            masks={context.mask_lookup(m,0,x,y)&15 for x in range(ax-4,ax+dx+5) for y in range(ay-4,ay+dy+5)}
            assert masks=={4}
            replayed=geometry.populate_source(reframe(template['request'],s,frozen),constants)
            assert replayed['status']=='CONDITIONAL_PLANAR_SOURCE'
            selected_regions.extend(replayed['regions'])
        row['selected_population']=dict(paths=len(selected_regions),
            per_resource=dict(collections.Counter(g['resource'] for g in selected_regions)),
            positive_paths=[dict(source=g['source'],resource='0x'+g['resource'],cell=g['cell'])
                for g in selected_regions if evaluate_region(q,radius,upper,g['native_bound'][:3],g['native_bound'][3],g['points'])['accepted']],
            incomplete_due_to_unresolved_cells=True)
    assert before=={str(p):pin(p) for p in paths}
    with output.open('x',encoding='utf8',newline='\n') as stream:
        json.dump(result,stream,indent=2);stream.write('\n')
    print(json.dumps([dict(site=s['site'],before=len(s['before']),candidates=len(s['candidate_after']),failures=len(s['failures']),comparisons=s.get('replay',{}).get('comparisons')) for s in result['sites']],indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    run(parser.parse_args().output)
