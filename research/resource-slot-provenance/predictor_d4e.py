# SPDX-License-Identifier: GPL-3.0-or-later
"""Versioned D4E owner-map candidate and Special geometry interface.

Adapted from owned D3 predictor; see D4E source ledger. Duplicates survive.

Reads only caller-supplied corpus/request JSON in CLI mode, writes stdout.
Pure prediction uses owned RG1 geometry/context/spatial arithmetic. The local
builder copies those pinned modules into a flat standalone directory. No game,
native receipt, cached prediction, process, network or saved-state access.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import struct

import geometry
import context
from resource_spatial import evaluate_region

SCHEMA = 'sor-d4e-corpus/1'
REQUEST = 'sor-d1-request/1'
DEFINITION = '1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7'


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode('utf8')


def seal(payload):
    return dict(payload=payload, sha256=hashlib.sha256(canonical(payload)).hexdigest())


def validate(envelope):
    """Check payload identity and all retained references before prediction."""
    try:
        return _validate(envelope)
    except (KeyError,TypeError,AttributeError,IndexError,OverflowError,struct.error) as error:
        raise ValueError('MALFORMED_CORPUS: '+str(error)) from error


def _validate(envelope):
    c = envelope['payload']
    if envelope['sha256'] != hashlib.sha256(canonical(c)).hexdigest():
        raise ValueError('CORRUPT_CORPUS')
    if c['schema'] != SCHEMA or c['definition'] != DEFINITION:
        raise ValueError('INCOMPATIBLE_CORPUS')
    if c['representation'] not in ('normalized', 'expanded'):
        raise ValueError('UNSUPPORTED_REPRESENTATION')
    constants = {int(k, 16): v for k, v in c['constants'].items()}
    required = (0x144f0416c,0x144f049f4,0x144f04654,0x144f048dc,0x144f052b0,
                0x144f052f8,0x144f03d80,0x144f03d40,0x144f03e00,0x144f03ed4,
                0x144f04178,0x144f03dc4,0x144f03d58,0x144f03e48,0x144f03fd4,0x144f03f50)
    if set(constants) != set(required):
        raise ValueError('MISSING_GENERATOR_CONSTANT')
    if len(c['settings']) != 6 or not c['bodies'] or c['maximum_width'] < 0:
        raise ValueError('MISSING_REQUIRED_RECORD')
    for value in [*constants.values(), *c['settings'], c['maximum_width']]:
        geometry.number(value)
    if any(value < 0 for value in c['settings']):
        raise ValueError('NEGATIVE_SETTING')
    if c['representation']=='normalized':
        for fid,dimensions in c['source_blocks'].items():
            if (len(fid)!=8 or int(fid,16)<=0 or len(dimensions)!=2
                    or any(type(v) is not int or not 4<v<=49152 for v in dimensions)):
                raise ValueError('SOURCE_BLOCK_DOMAIN')
    for block in c['generation_blocks'].values():
        if len(block) != 8:
            raise ValueError('BLOCK_ARITY')
        values = list(map(geometry.number, block))
        if min(values) < 0 or any(values[i] > values[i+1] for i in (0,2,4)):
            raise ValueError('BLOCK_DOMAIN')
        if max(values[2:4]) > c['maximum_width']:
            raise ValueError('UNSOUND_WIDTH_BOUND')
    for body in c['bodies'].values():
        if not (type(body['system']) is int and 0 <= body['system'] < 2**18
                and type(body['index']) is int and 0 <= body['index'] < 64):
            raise ValueError('BODY_KEY_DOMAIN')
        for key,tile in body['tiles'].items():
            chart,cx,cy=map(int,key.split(':'))
            if chart not in (0,1) or not 0<=cx<256 or not 0<=cy<256 or len(tile)!=4:
                raise ValueError('TILE_DOMAIN')
            if tile[2] not in body['biomes'] or not 0 <= tile[3] <= 255:
                raise ValueError('MISSING_BIOME')
            if c['representation'] == 'normalized':
                entries = c['patterns'][tile[0]]
                if len(entries) != 256:
                    raise ValueError('PATTERN_ARITY')
                for fid, flags in entries:
                    if not 0 <= flags <= 255:
                        raise ValueError('PATTERN_FLAGS')
                    if fid != '00000000' and fid not in c['source_blocks']:
                        raise ValueError('MISSING_SOURCE_BLOCK')
        if c['representation']=='expanded':
            if set(body['routes'])!=set(body['tiles']):
                raise ValueError('MISSING_ROUTE_TILE')
            for key,entries in body['routes'].items():
                chart,cx,cy=map(int,key.split(':'))
                if not isinstance(entries,list) or len(entries)!=256:
                    raise ValueError('ROUTE_ARITY')
                for item in entries:
                    if item is None:
                        continue
                    if not isinstance(item,list) or len(item)!=5:
                        raise ValueError('ROUTE_ENTRY_ARITY')
                    ax,ay,fid,dx,dy=item
                    if (len(fid)!=8 or int(fid,16)<=0 or any(type(v) is not int for v in (ax,ay,dx,dy))
                        or ax%12 or ay%12 or ax//192!=cx or ay//192!=cy
                        or not 0<dx<=49148 or not 0<dy<=49148):
                        raise ValueError('ROUTE_DOMAIN')
        for biome in body['biomes'].values():
            special_seen = False
            for resource in biome['resources']:
                if resource['block'] not in c['generation_blocks'] or not 0 <= resource['rarity'] < 7:
                    raise ValueError('MISSING_RESOURCE_DEPENDENCY')
                branch = resource.get('branch','ordinary')
                if branch not in ('ordinary','special') or special_seen:
                    raise ValueError('RESOURCE_BRANCH_ORDER')
                if branch == 'special':
                    if resource['rarity'] != 5:
                        raise ValueError('SPECIAL_RARITY_DOMAIN')
                    special_seen = True
    return c


def tile_at(body, chart, x, y):
    if chart not in (0, 1) or not 0 <= x < 49152 or not 0 <= y < 49152:
        raise ValueError('UNSUPPORTED_CHART_OR_SEAM')
    return body['tiles'][f'{chart}:{x//192}:{y//192}']


def resolve(c, body, chart, x, y):
    """Single backlink and typed SFBK lookup, adapted from C2D source_at."""
    tile = tile_at(body, chart, x, y)
    if tile[1] != 8:
        raise ValueError('UNKNOWN_ORIENTATION')
    sx, sy = (x % 192)//12, (y % 192)//12
    if c['representation'] == 'expanded':
        item = body['routes'][f'{chart}:{x//192}:{y//192}'][sx*16+sy]
        if item is None:
            raise ValueError('UNKNOWN_DEFAULT_OR_NEIGHBOUR')
        ax, ay, fid, dx, dy = item
    else:
        entries = c['patterns'][tile[0]]
        fid, flags = entries[sx*16+sy]
        if not flags & 8:
            sx -= (flags >> 4) & 3
            sy -= (flags >> 6) & 3
            if not 0 <= sx < 16 or not 0 <= sy < 16:
                raise ValueError('UNKNOWN_NEIGHBOUR')
            fid, flags = entries[sx*16+sy]
        if fid not in c['source_blocks']:
            raise ValueError('UNKNOWN_DEFAULT_BLOCK')
        dx, dy = [v-4 for v in c['source_blocks'][fid]]
        ax, ay = (x//192)*192+sx*12, (y//192)*192+sy*12
    if min(dx,dy) <= 0:
        raise ValueError('NONPOSITIVE_DIMENSIONS')
    biome = tile_at(body, chart, ax, ay)[2]
    return ax, ay, fid, dx, dy, biome


def unknown(reason, **extra):
    return dict(schema='sor-d3-response/1', status='UNKNOWN', reason=reason,
                exhaustive=False, regions=[], availability={}, **extra)


def predict(envelope, request):
    """Generate ordinary/Special sources and derive area and callback results.

    Location is a geographic descriptor plus XYZ in that descriptor's native
    frame. It carries no selected pattern, source anchor or expected region.
    Unsupported source cells preserve partial positive geometry and UNKNOWN.
    """
    try:
        c = validate(envelope)
        if set(request) != {'schema','definition','body','chart','descriptor','query','radius','upper'}:
            raise ValueError('REQUEST_FIELDS')
        if request['schema'] != REQUEST or request['definition'] != c['definition']:
            raise ValueError('REQUEST_VERSION')
        body = c['bodies'][request['body']]
        chart, origin = request['chart'], request['descriptor']
        if type(chart) is not int or chart not in (0,1):
            raise ValueError('UNSUPPORTED_CHART_OR_SEAM')
        if len(origin) != 2 or any(type(v) is not int or v%96 or not 0 <= v < 49152 for v in origin):
            raise ValueError('UNSUPPORTED_DESCRIPTOR')
        q = geometry.vector(request['query'],3)
        radius, upper = map(geometry.number, (request['radius'],request['upper']))
        if radius <= 0:
            raise ValueError('POSITIVE_RADIUS_REQUIRED')
        halo = radius+400+2*c['maximum_width']
        lo = [math.floor(origin[k]+(q[k]-halo)/100) for k in (0,1)]
        hi = [math.floor(origin[k]+(q[k]+halo)/100) for k in (0,1)]
        # Reject unavailable coarse coverage before allocating a fine-cell walk.
        for x in range(lo[0]//192,hi[0]//192+1):
            for y in range(lo[1]//192,hi[1]//192+1):
                tile_at(body,chart,x*192,y*192)
        sources, failures = {}, []
        for x in range(lo[0],hi[0]+1):
            for y in range(lo[1],hi[1]+1):
                try:
                    source = resolve(c,body,chart,x,y)
                    sources[source[:3]] = source
                except (ValueError,KeyError) as error:
                    failures.append(dict(cell=[x,y],reason=str(error)))
        constants = {int(k,16): v for k,v in c['constants'].items()}
        regions, eligible = [], set()
        for ax,ay,fid,dx,dy,biome in sources.values():
            try:
                masks = {tile_at(body,chart,x,y)[3] & 15 for x in range(ax-4,ax+dx+5)
                         for y in range(ay-4,ay+dy+5)}
                if len(masks) != 1:
                    raise ValueError('MISSING_FIRST_CONSTRUCTION_QUERY_MASK')
                mask = masks.pop()
                selected = body['biomes'][biome]
                if selected['status'] != 'ORDINARY_AND_SPECIAL':
                    raise ValueError('UNSUPPORTED_RESOURCE_BRANCH')
                ordered = []
                for item in selected['resources']:
                    rarity = item['rarity']
                    if item.get('branch') == 'special':
                        high = {bool(tile_at(body,chart,x,y)[3] & 240)
                                for x in range(ax-4,ax+dx+5) for y in range(ay-4,ay+dy+5)}
                        if len(high) != 1:
                            raise ValueError('MISSING_FIRST_CONSTRUCTION_QUERY_SPECIAL_MASK')
                        weight = 1.0 if high.pop() else c['settings'][5]
                    else:
                        weight = (0.0 if rarity == 6 else c['settings'][rarity]) if mask == 8 or mask < rarity else 1.0
                    ordered.append(dict(resource=item['id'],block=c['generation_blocks'][item['block']]+[0,0],weight=weight))
                    eligible.add(item['id'])
                native = [100*(v-o-2) for v,o in zip((ax,ay),origin)]
                bounds = [1,dx+3,1,dy+3]
                req = dict(source=f'{chart}:{ax}:{ay}:{fid}',provenance='D3 installed-main conditional geometry',
                    origin=native,owner_key=int(request['body'],16),clip_center=[native[0]+dx//2*100,native[1]+dy//2*100,0],
                    clip_half=[dx//2*100+200,dy//2*100+200,0],context_qualified=True,order_qualified=True,
                    cell_bounds=bounds,ordered_resources=ordered,
                    packed_keys={f'{x},{y}':context.packed_seed_key(chart,origin,native,[x,y],body['system'],body['index'])
                        for x in range(1,dx+3) for y in range(1,dy+3)})
                generated = geometry.populate_source(req,constants)
                if generated['status'] != 'CONDITIONAL_PLANAR_SOURCE':
                    raise ValueError(str(generated.get('reason')))
                for r in generated['regions']:
                    r.pop('bound',None)
                    r['ordered_xyzw_le'] = b''.join(struct.pack('<4f',*p) for p in r['points']).hex()
                    r['native_bound_le'] = struct.pack('<4f',*r['native_bound']).hex()
                    r['callback'] = evaluate_region(q,radius,upper,r['native_bound'][:3],r['native_bound'][3],r['points'])
                    r['area'] = geometry.bounded_region_circle(r['points'],q[:2],radius)
                    regions.append(r)
            except (ValueError,KeyError) as error:
                failures.append(dict(source=[ax,ay,fid],reason=str(error)))
        availability = {}
        for resource in sorted(eligible):
            paths = [r for r in regions if r['resource']==resource]
            positive = any(r['area'].get('intersection')=='POSITIVE_AREA' for r in paths)
            uncertain = bool(failures) or any(r['area']['status']=='UNKNOWN' for r in paths)
            availability[resource] = dict(status='PRESENT' if positive else 'UNKNOWN' if uncertain else 'ABSENT_WITHIN_PROVEN_SCOPE',
                callback_present=any(r['callback']['accepted'] is True for r in paths),
                callback_complete=not failures and all(r['callback']['status']=='KNOWN' for r in paths),
                scope='Conditional ordinary and Special planar veins in enumerated source halo; final catalogue UNKNOWN')
        return dict(schema='sor-d3-response/1',status='PARTIAL' if failures else 'CONDITIONAL_GEOMETRY',
            definition=c['definition'],corpus_sha256=envelope['sha256'],request=request,
            coordinate_provenance='Caller-supplied geographic chart/descriptor and translated native XYZ; 100 native units per fine cell',
            halo=[lo,hi],source_count=len(sources),exhaustive=not failures,
            native_census='UNKNOWN',historical_epoch='UNKNOWN',other_resources='UNKNOWN: Water admission, atmosphere, nonzero Everywhere',
            regions=regions,availability=availability,failures=failures)
    except (ValueError,KeyError,TypeError,AttributeError,OverflowError,IndexError,struct.error) as error:
        return unknown(str(error))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--corpus',type=Path,required=True)
    parser.add_argument('--request',type=Path,required=True)
    args = parser.parse_args()
    try:
        response = predict(json.loads(args.corpus.read_text(encoding='utf8')),json.loads(args.request.read_text(encoding='utf8')))
    except (OSError,ValueError) as error:
        response = unknown(str(error))
    print(json.dumps(response,sort_keys=True,allow_nan=False))
