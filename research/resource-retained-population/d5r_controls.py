# SPDX-License-Identifier: GPL-3.0-or-later
"""D5R finite ordering/weight controls; no engine scheduling simulation.

Reads a D5H-format numerical replay receipt and writes a fresh JSON receipt.
Only Python stdlib executes in this disposable process. The input must come
from authenticated static corpora/raster and the qualified D5H arithmetic.
The first-entry model assumes one stable source/map epoch, successful insertion,
generation and allocation, no visited collision, reset or retirement. Exhaustive
permutations here are model orders, not a proof that the engine admits each one.
No game, native generator, save, analysis project, network or Git operation.
"""
from pathlib import Path
import hashlib
import itertools
import json
import struct
import sys


def f32(value):
    return struct.unpack('<f', struct.pack('<f', value))[0]


def rectangle(low, high):
    """Qualified nonempty rectangle: native X ascends while Y descends."""
    return [(x, y) for x in range(low[0], high[0] + 1)
            for y in range(high[1], low[1] - 1, -1)]


def key(discriminator, tag, query):
    """Three u32 words; coordinate packing does not change provider Int2."""
    return [discriminator, tag, (query[0] & 65535) | ((query[1] & 65535) << 16)]


def ordinary(mask, rarity, inactive):
    if mask == 8 or mask < rarity:
        return f32(inactive[rarity]) if 0 <= rarity <= 5 else 0.0
    return 1.0


def main():
    source, output = map(Path, sys.argv[1:3])
    assert not output.exists()
    replay = json.loads(source.read_text(encoding='utf8'))
    assert rectangle((1, 2), (2, 3)) == [(1, 3), (1, 2), (2, 3), (2, 2)]
    assert key(1, 7, (-1, 2)) == key(1, 7, (65535, 65538))
    assert key(1, 7, (1, 2)) != key(1, 8, (1, 2))
    # Pinned effective ordinary order: Ionic Liquids rarity 3, Fluorine 1,
    # Copper 0. Only two inactive multipliers are needed by the chosen cases.
    inactive = {0: 1.0, 1: 0.2, 3: 0.05}
    rarities = [3, 1, 0]
    vectors = {m: [ordinary(m, r, inactive) for r in rarities] for m in (0, 3)}
    candidates = []
    for row in replay['rows']:
        expected = 0 if row['continuation'] == 'L' else 3
        root = row['root']
        for i, (query, delta) in enumerate(zip(row['density_queries'],
                           [(-1, 1), (-1, 0), (0, 1), (1, 1)], strict=True)):
            assert query['geographic_query'] == [37536 + root[0] + delta[0],
                                               20928 + root[1] + delta[1]]
            assert len(query['branches']) == 2
            for branch in query['branches']:
                assert branch['mask'] == expected
                assert branch['vector'] == vectors[expected]
            candidates.append(dict(id=row['continuation'] + str(i), mask=expected,
                                   query=query['geographic_query']))
    assert len(candidates) == 8 and vectors[0] != vectors[3]
    # Every permutation of lock-arrival candidates is deliberately a MODEL.
    # Only its first entrant populates this simplified stable-epoch map.
    winners = {0: 0, 3: 0}
    for order in itertools.permutations(range(8)):
        winners[candidates[order[0]]['mask']] += 1
    assert winners == {0: 20160, 3: 20160}
    # Positive equivalence control: distinct samples need not change a common
    # rarity-zero resource. This says nothing about complete population equality.
    assert ordinary(0, 0, inactive) == ordinary(3, 0, inactive) == 1.0
    # Boundary controls: numeric mask 8 is inactive even above rarity;
    # an unsupported inactive rarity keeps zero, rather than indexing settings.
    assert ordinary(8, 3, inactive) == f32(0.05)
    assert ordinary(0, 6, inactive) == 0.0
    value = dict(input_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                 helper_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                 candidates=candidates, vectors=vectors, model_orders=40320,
                 model_winners=winners, numerical_evaluations=16,
                 rectangle_control='PASS', key_controls='PASS',
                 weight_boundary_controls='PASS',
                 geometry='NOT EXECUTED', native_scheduler_orders='NOT OBSERVED',
                 qualification='Model permutations do not establish native interleavings or historical selection')
    with output.open('x', encoding='utf8', newline='\n') as stream:
        json.dump(value, stream, indent=2)
        stream.write('\n')
    print('PASS: 16 replay comparisons; 40320 model orders; key/rectangle/weight controls')


if __name__ == '__main__':
    main()
