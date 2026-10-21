# SPDX-License-Identifier: GPL-3.0-or-later
"""RG2-A original point selection over an RG1 receipt, pure stdlib/project math.

No target or file effects on import. CLI reads one pinned local RG1 receipt and
writes a NEW local JSON. It retains all paths, including outside-start paths.
Does not equate scanner pixels, extractor footprint, tapered strips and bounded
region membership. See prediction-contract.md for tolerances and scope.
"""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'resource-geometry'))
import geometry

VERSION = 'rg2a-points/1'


def classify(paths, q):
    return dict(region=sorted({p['resource'] for p in paths
                              if geometry.region_membership(p['points'], q) == 'INTERIOR'}),
                strips=sorted({p['resource'] for p in paths
                              if geometry.point_membership(p['points'], q) == 'INTERIOR'}))


def transect(a, b, occupied, *, iterations=30):
    """Maintain opposite endpoint labels; no assumption of one global crossing.

    The bracket certifies only a local transition along this segment. Explicit
    point classifications, rather than assumed edge-normal distances, govern
    the resulting controls. Euclidean along-transect offsets are not signed
    distances to every other boundary.
    """
    a, b = list(a), list(b)
    if occupied(a) == occupied(b):
        raise ValueError('opposite endpoint labels required')
    label = occupied(a)
    for _ in range(iterations):
        m = [(x+y)/2 for x, y in zip(a, b)]
        if occupied(m) == label:
            a = m
        else:
            b = m
    return a, b


def select(receipt):
    paths = [p for s in receipt['sources'] for p in s['regions']]
    center = receipt['center']
    lattice = receipt['fixed_queries']
    positive = sorted((q for q in lattice if q['resources']),
                      key=lambda q: (math.dist(q['point'], center), q['point']))
    negative = sorted((q for q in lattice if not q['resources']),
                      key=lambda q: (math.dist(q['point'], center), q['point']))
    if not positive or not negative:
        raise ValueError('independent positive and negative controls required')
    a, b = positive[0]['point'], negative[0]['point']
    # Target one resource's aggregate union; separately retain every resource.
    resource = positive[0]['resources'][0]
    def has(q):
        return any(p['resource'] == resource and
                   geometry.region_membership(p['points'], q) == 'INTERIOR' for p in paths)
    lo, hi = transect(a, b, has)
    edge = [(x+y)/2 for x, y in zip(lo, hi)]
    d = [b[i]-a[i] for i in (0, 1)]; length = math.hypot(*d)
    direction = [x/length for x in d]
    samples = [('positive-control', a), ('negative-control', b), ('beacon', center)]
    for distance in (-5, -1, 1, 5):
        samples.append((f'edge{distance:+d}', [edge[i]+distance*direction[i] for i in (0, 1)]))
    result = []
    for label, q in samples:
        result.append(dict(id=label, xy=q, offset=[q[i]-center[i] for i in (0, 1)],
                           nominal_circle=math.dist(q, center) < 150,
                           expected=classify(paths, q)))
    assert resource in result[0]['expected']['region']
    assert not result[1]['expected']['region']
    # Fail closed if other nearby crossings spoil the intended edge controls.
    for s in result[3:]:
        assert (resource in s['expected']['region']) == ('edge-' in s['id']), s
    return dict(version=VERSION, center=center, radius=150, resource=resource,
                edge_bracket=[lo, hi], bracket_width=math.dist(lo, hi),
                transect_direction=direction, samples=result,
                coverage=dict(sources=len(receipt['sources']), paths=len(paths),
                              resource_cell_calls=sum(s['cells'] for s in receipt['sources'])),
                status='FROZEN_PREDICTION_NOT_RUNTIME_OBSERVATION')


def main():
    import argparse, json, hashlib
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--input', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    root = Path(__file__).resolve().parents[2]
    if not args.output.resolve().is_relative_to(root/'.local-work'):
        raise ValueError('CLI output must stay local')
    raw = args.input.read_bytes()
    result = select(json.loads(raw))
    result['source'] = dict(path=str(args.input), sha256=hashlib.sha256(raw).hexdigest())
    result['method_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    with args.output.open('x', encoding='utf8', newline='\n') as f:
        json.dump(result, f, indent=2); f.write('\n')


if __name__ == '__main__':
    main()
