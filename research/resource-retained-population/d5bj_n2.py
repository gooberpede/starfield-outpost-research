# SPDX-License-Identifier: GPL-3.0-or-later
"""Join the D5BI typed N2 projection to the D5AQ coordinate table.

Uses the D5BI projected-event verifier and D5AP's owned task extractor.
Reads one explicit candidate ZIP and tracked inputs. JSON stdout only.
The join preserves one recorded sample and 195 other conditional masks.
"""
import argparse
import csv
import io
import json
from pathlib import Path
import struct
import sys
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parent))
import d5bi_verify as projection
import d5bj_sampler as sampler

CANDIDATE = 'a47bbd302553755d0fe87d746234d0d6c527ee7297cfda2e38915072edb7c3d7'


def check_context(body, descriptor):
    sampler.require(body == 0x5e0de, 'N2 selected body differs from C1')
    frame = (descriptor[0], *(struct.unpack_from('<2i', descriptor, at) for at in (4, 20, 36)))
    sampler.require(frame == sampler.FRAME, 'N2 consumed descriptor differs from C1')


def context_controls(body, descriptor):
    changed = bytearray(descriptor)
    struct.pack_into('<i', changed, 40, 1)
    for test_body, test_frame, message in (
        (body ^ 1, descriptor, 'N2 selected body differs from C1'),
        (body, changed, 'N2 consumed descriptor differs from C1'),
    ):
        try:
            check_context(test_body, test_frame)
        except ValueError as error:
            sampler.require(str(error) == message, 'Wrong C1 context refusal')
        else:
            raise ValueError('Incompatible C1 context was accepted')
    return ['wrong_body', 'wrong_fine_phase']


def join(rows, tasks, event):
    require = sampler.require
    keys = {(t['family'], tuple(t['request'])): t for t in tasks}
    require(len(tasks) == len(keys) == len({t['task'] for t in tasks}) == 392,
            'Duplicate or missing typed N2 allocations')
    require(set(keys) == {(family, query) for family in (1, 2) for query in sampler.GRID},
            'Wrong typed N2 coordinate domain')
    density = sorted((t for t in tasks if t['family'] == 1),
                     key=lambda t: next(e['sequence'] for e in t['scheduler'] if e['kind'] == 1))
    rank = {t['task']: i for i, t in enumerate(density)}
    require([(int(r['original_x']), int(r['original_y'])) for r in rows] == sampler.GRID,
            'Wrong historical table coordinate domain')
    actual = []
    for row, query in zip(rows, sampler.GRID):
        d, layer = (keys[family, query] for family in (1, 2))
        require(d['task'] == int(row['density_task']) and layer['task'] == int(row['layer_task'])
                and d['source_allocation'] == layer['source_allocation'] == int(row['source_allocation'])
                and rank[d['task']] == int(row['density_publication_rank'])
                and next(e['sequence'] for e in d['scheduler'] if e['kind'] == 9) == int(row['density_provider']),
                f'Wrong typed allocation, source or publication rank at {query}')
        if d['outcome'] == 'MISS':
            actual.append((query, int(row['mask'], 16)))
    require(actual == [(tuple(event['request']), event['mask'])] and event['sample'] == 3962,
            'N2 does not attest the declared single direct sample')
    return {'paired_coordinates': len(rows), 'distinct_allocations': len(keys),
            'observed_samples': [{'query': event['request'], 'mask': event['mask'], 'sequence': event['sample']}],
            'other_coordinates': len(rows) - len(actual)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('candidate', type=Path)
    args = parser.parse_args()
    try:
        sampler.require(sys.flags.isolated and sys.dont_write_bytecode and not sys.flags.optimize
                        and sys.version_info[:3] == (3, 14, 3), 'Use CPython 3.14.3 -I -B')
        manifest = projection.decode(projection.MANIFEST.read_bytes())
        sampler.require(manifest['candidate']['sha256'] == CANDIDATE, 'D5BI manifest is not the selected candidate')
        candidate = sampler.regular(args.candidate)
        session, snapshot, channels = projection.parse(projection.read_zip(candidate, manifest))
        core, causal, scheduler = (channels[name] for name in ('core', 'causal', 'scheduler'))
        result = projection.interpret(session, snapshot, channels)
        generation = projection.at(core, 3961)
        body, descriptor = generation['a'], bytes.fromhex(generation['descriptor'])
        check_context(body, descriptor)
        refusals = context_controls(body, descriptor)
        tasks, _ = projection.extract(core, {'events': causal},
                                      {'events': scheduler, 'histories': projection.task_histories(scheduler)},
                                      projection.core_reader)
        table = projection.MANIFEST.parents[2] / 'experiments/resource-retained-population/d5aq-request-mask-map.csv'
        raw = table.read_bytes()
        sampler.require(sampler.digest(raw) == sampler.CSV, 'Wrong D5AQ historical coordinate table')
        rows = list(csv.DictReader(io.StringIO(raw.decode('utf8'))))
        result = join(rows, tasks, result['construction'])
    except (OSError, ValueError, KeyError, struct.error, StopIteration, zipfile.BadZipFile) as error:
        parser.exit(1, f'D5BJ N2 join refused: {error}\n')
    print(json.dumps(dict(scope='Projected N2 typed identities and one instrumented sample',
                          candidate=CANDIDATE, context_refusals=refusals, **result), sort_keys=True))


if __name__ == '__main__':
    main()
