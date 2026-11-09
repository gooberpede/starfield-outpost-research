# SPDX-License-Identifier: GPL-3.0-or-later
"""Check the semantic joins of a D5BJ continuation receipt set.

Consumes explicit JSON files from the reader commands. Verification is a
composition of their bounded results with the named static premises. A JSON
file alone cannot attest how it was produced. Writes only JSON to stdout.
"""
import argparse
from copy import deepcopy
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import d5bj_sampler as host
from d5s_controls import registration

NAMES = ('components', 'preparation', 'workers', 'sources', 'dispatch', 'sampler', 'first-miss')
LIMITS = [
    'main-file resident worldspace, placement callbacks and original per-cell preparation',
    'engine pool constructors and integrated schedule on the same started pool',
    'server completion drain and subsequent density/layer dependency registration',
    'stable selected Grid, source allocation and ProcGen owner during the continuation',
]
require = host.require


def verify(rows):
    component, prep, workers, sources, dispatch, sampler, lookup = (rows[name] for name in NAMES)
    require(component['components']['1332288'] == [0x57cf, 0x57d0, 0, 0x57d4, 0, 0, 0],
            'Wrong native component family')
    require(prep['completion_queued'] and prep['cells'] == 1600 and prep['reader_released']
            and prep['rectangle'] == [-16, -16, 23, 23], 'Incomplete rectangle traversal or completion')
    require(prep['observed_post_receiver_va'] == '0x1428d8a4e'
            and prep['receiver_released_running_state'] == 9 and prep['native_layer_producer_pending']
            and dispatch['populated_receiver']['extra_publications'] == 0,
            'Layer can run before the competing density command')
    require(prep['native_pool_getter'] and workers['original_constructor_getter_operands'] == 2
            and workers['live_native_worker_loops'] == 3 and workers['shutdown_counters_drained'],
            'Wrong shared-pool binding or worker coverage')
    require(sources['admitted_sources'] == 324 and sources['target_low_words'] == [1718132308, 1003558160]
            and sources['retirement']['small_shift_retained'], 'Wrong source-token or lifetime qualification')
    require(lookup['branches']['cold'] == 'miss'
            and lookup['branches']['same_full_token'] == 'visited'
            and lookup['branches']['same_pointer_holder'] == 'hit',
            'Qualified cold protected map miss is absent')
    _, coords = registration()
    masks = {name: {tuple(row['query']): row['mask'] for row in branch['rows']}
             for name, branch in sampler['branches'].items()}
    corners = {tuple(row['query']): row for row in sources['corners']}
    require(set(masks) == {'fma', 'nonfused'}, 'Missing native sampler branch')
    require([row['route'] for row in dispatch['first_c1_coordinates']] == ['owner', 'peer'],
            'Wrong continuation route pair')
    routes = []
    for row, expected in zip(dispatch['first_c1_coordinates'],
                             [(58, 845, (10, 11), '0x28', 3), (28, 874, (-2, -2), '0x20', 0)], strict=True):
        prior, index, query, slot, mask = expected
        order = row['order']
        require(len(order) == len(coords) == 1720 and set(order) == set(range(1720)), 'Wrong native queue inventory')
        first = next((i, at, coords[at]) for i, at in enumerate(order) if coords[at] in host.GRID)
        require(first == (prior, index, query) and row['preceding'] == prior and row['registration'] == index
                and tuple(row['query']) == query, 'An earlier target claim changes the continuation')
        require(corners[query]['target_slot'] == slot and corners[query]['permutations'] == 24,
                'Native corner control does not retain the target')
        require({values[query] for values in masks.values()} == {mask}, 'Native mask differs at first eligible query')
        routes.append({'route': row['route'], 'first_target_capable_query': query,
                       'preceding_non_target_claims': prior, 'conditional_mask': mask,
                       'cold_selected_source_control': lookup['branches']['cold']})
    return routes


def negatives(rows):
    def check(label, field, value):
        test = deepcopy(rows)
        item = test
        for key in field[:-1]:
            item = item[key]
        item[field[-1]] = value
        try:
            verify(test)
        except ValueError as error:
            require(label in str(error), f'Unexpected counterexample diagnostic: {error}')
        else:
            raise ValueError(f'Counterexample accepted: {field}')

    controls = [
        ('Wrong native component', ('components', 'components', '1332288'), [0] * 7),
        ('Incomplete rectangle', ('preparation', 'completion_queued'), False),
        ('Layer can run', ('preparation', 'native_layer_producer_pending'), False),
        ('Wrong shared-pool', ('workers', 'original_constructor_getter_operands'), 1),
        ('Wrong source-token', ('sources', 'retirement', 'small_shift_retained'), False),
        ('Qualified cold', ('first-miss', 'branches', 'cold'), 'hit'),
    ]
    for index in (0, 1):
        run = rows['dispatch']['first_c1_coordinates'][index]
        order = run['order'].copy()
        at = run['preceding']
        order[0], order[at] = order[at], order[0]
        controls.append(('An earlier target', ('dispatch', 'first_c1_coordinates', index, 'order'), order))
    for label, field, value in controls:
        check(label, field, value)
    return len(controls)


def read(path):
    with host.regular(path).open('rb') as stream:
        raw = stream.read(262145)
    require(len(raw) <= 262144, 'Unexpected continuation receipt size')
    return json.loads(raw)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in NAMES:
        parser.add_argument('--' + name, required=True, type=Path)
    args = parser.parse_args()
    try:
        require(sys.flags.isolated and sys.dont_write_bytecode and not sys.flags.optimize, 'Use Python -I -B')
        rows = {name: read(getattr(args, name.replace('-', '_'))) for name in NAMES}
        sys.setrecursionlimit(10000)
        routes = verify(rows)
        refused = negatives(rows)
    except (OSError, ValueError, KeyError, TypeError, StopIteration) as error:
        parser.exit(1, f'D5BJ continuation refused: {error}\n')
    print(json.dumps(dict(scope='Static composition with independently bounded native controls',
                          continuations=routes, counterexamples_refused=refused, premises=LIMITS), sort_keys=True))


if __name__ == '__main__':
    main()
