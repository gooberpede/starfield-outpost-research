# SPDX-License-Identifier: GPL-3.0-or-later
"""Conditional wrapper over unchanged D4E geometry, context and spatial code.

Imported pure interface receives a validated installed corpus, explicit source
context and an independently justified set of possible masks. No I/O or fitting.
This source-context API is distinct from the location-only predictor: it cannot
qualify a missing saved-to-effective-frame transform. Imports owned modules
from a provisioned flat bundle. The bundle manifest must bind their exact bytes.
"""
import struct
import geometry
import context
from resource_spatial import evaluate_region


def generate(corpus, request, source, masks):
    """Enumerate all supplied ordinary alternatives without choosing a winner.

    Request/source arity and numeric semantics follow D5A analyze.generate;
    corpus and requests must first pass the unchanged D4E validation contract.
    Mask membership must come from a qualified full support, not site fitting.
    """
    body = corpus['bodies'][request['body']]
    dx, dy = source['nominal']
    native = source['source_origin_native']
    ordinary = [r for r in source['selected']['resources'] if r.get('branch') != 'special']
    if any(r['rarity'] == 6 and corpus['generation_blocks'][r['block']][7] != 0 for r in ordinary):
        raise ValueError('UNSUPPORTED_NONZERO_RARITY6_WATER')
    alternatives = []
    if not masks or any(type(m) is not int or m not in range(16) for m in masks):
        raise ValueError('MASK_DOMAIN')
    for mask in sorted(set(masks)):
        ordered = []
        for item in ordinary:
            rarity = item['rarity']
            weight = (0.0 if rarity == 6 else corpus['settings'][rarity]) if mask == 8 or mask < rarity else 1.0
            ordered.append(dict(resource=item['id'], block=corpus['generation_blocks'][item['block']] + [0, 0], weight=weight))
        req = dict(source=source['source_key'], provenance='D5K explicit conditional ordinary support',
            origin=native, owner_key=int(request['body'], 16),
            clip_center=[native[0] + dx//2*100, native[1] + dy//2*100, 0],
            clip_half=[dx//2*100 + 200, dy//2*100 + 200, 0],
            context_qualified=True, order_qualified=True, cell_bounds=[1, dx+3, 1, dy+3],
            ordered_resources=ordered,
            packed_keys={f'{x},{y}': context.packed_seed_key(request['chart'], request['descriptor'], native,
                [x, y], body['system'], body['index']) for x in range(1, dx+3) for y in range(1, dy+3)})
        generated = geometry.populate_source(req, {int(k, 16): v for k, v in corpus['constants'].items()})
        if generated['status'] != 'CONDITIONAL_PLANAR_SOURCE':
            raise ValueError('UNSUPPORTED_GENERATOR_CONTEXT')
        paths = []
        for r in generated['regions']:
            paths.append(dict(resource=r['resource'],
                points_le=b''.join(struct.pack('<4f', *p) for p in r['points']).hex(),
                bound_le=struct.pack('<4f', *r['native_bound']).hex(),
                area=geometry.bounded_region_circle(r['points'], request['query'][:2], request['radius']),
                admission=evaluate_region(request['query'], request['radius'], request['upper'],
                    r['native_bound'][:3], r['native_bound'][3], r['points'])))
        alternatives.append(dict(mask=mask,
            weights_le=b''.join(struct.pack('<f', r['weight']) for r in ordered).hex(), paths=paths))
    return dict(source=source['source_key'], alternatives=alternatives,
        classification='INVARIANT' if len({a['weights_le']+str(a['paths']) for a in alternatives}) == 1 else 'CONDITIONAL_ALTERNATIVES',
        scope='Ordinary conditional planar veins; complete source-support proof required externally',
        special_helium3='UNKNOWN', terrestrial_water='UNKNOWN', atmospheric='UNKNOWN')
