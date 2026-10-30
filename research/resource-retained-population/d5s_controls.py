# SPDX-License-Identifier: GPL-3.0-or-later
"""Check D5S evidence, or explicitly replay its retained disposable methods.

Check mode reads JSON and owned method files and writes one new JSON receipt.
Replay mode also reads the pinned installed PE/static lease, copies owned local
methods into a new ignored directory and starts separate Python processes.
Those processes execute extracted native instructions only in their own memory.
No game launch, attachment, installed write, save access, Ghidra edit, network
or Git mutation occurs. Replay requires the retained local evidence; it does not
download or reconstruct missing proprietary inputs. Stop on a failed process,
callback diagnostic, identity mismatch or 40-billion-byte C:/D: disk-floor breach.
"""
from pathlib import Path
import argparse
import hashlib
import json
import math
import os
import re
import shutil
import struct
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
METHODS = ['start.py', 'geometry_compare.py', 'registration.py',
           'winner_candidates.py', 'native_probe.py', 'native_cell.py',
           'native_keys.py', 'native_spatial.py', 'native_queue.py',
           'native_dispatch.py', 'native_retirement.py', 'native_query.py']
RECEIPTS = ['geometry.json', 'registration.json', 'winner-candidates03.json',
            'native-probe.json', 'native-cell.json', 'native-keys03.json',
            'native-spatial.json', 'native-queue03.json',
            'native-dispatch04.json', 'native-retirement04.json', 'native-query.json']


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as source:
        for block in iter(lambda: source.read(8 * 1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def free_space():
    values = {drive: shutil.disk_usage(drive).free for drive in ('C:/', 'D:/')}
    assert min(values.values()) >= 40_000_000_000, values
    return values


def read(path):
    return json.loads(Path(path).read_text(encoding='utf8'))


def registration(low=(-16, -16), high=(23, 23)):
    """Registration transcription only; execution order needs native evidence."""
    coordinates, density, order = set(), set(), []

    def coordinate(q):
        if q in coordinates:
            return
        coordinates.add(q)
        for dx, dy in [(-1, 1), (-1, 0), (0, 1), (1, 1)]:
            neighbor = (q[0] + dx, q[1] + dy)
            if neighbor not in density:
                density.add(neighbor)
                order.append(neighbor)
            if all(low[i] <= neighbor[i] <= high[i] for i in (0, 1)):
                coordinate(neighbor)

    for x in range(low[0], high[0] + 1):
        for y in range(high[1], low[1] - 1, -1):
            coordinate((x, y))
    return coordinates, order


def check(evidence):
    rows = {name: read(evidence / name) for name in RECEIPTS}
    coordinates, order = registration()
    assert len(coordinates) == 1600 and len(order) == 1720
    assert order == list(map(tuple, rows['registration.json']['density_order']))
    # A singleton and a contrasting rectangle challenge enumeration/dedup scope.
    assert registration((0, 0), (0, 0))[1] == [(-1, 1), (-1, 0), (0, 1), (1, 1)]
    assert len(registration((0, 0), (1, 1))[0]) == 4
    keys = [(q[0] & 65535) | ((q[1] & 65535) << 16) for q in order]
    assert len(set(keys)) == len(keys)
    dispatch = rows['native-dispatch04.json']
    for run, query, index, prior in zip(dispatch['runs'], [(10, 11), (-2, -2)],
                                       [845, 874], [58, 28]):
        assert run['pool_contexts'] == 5
        assert run['first_query'] == list(query) and run['first_padded'] == index
        assert sorted(run['order']) == list(range(1720))
        assert run['order'].index(index) == prior
        assert all(not all(-2 <= v < 12 for v in order[i])
                   for i in run['order'][:prior])
    assert dispatch['runs'][0]['neutral_pump_markers'] == 1720
    assert [r['pump_publications'] for r in dispatch['wakes']] == [1, 0, 0]
    assert all(r['wake_calls'] == 1720 for r in dispatch['wakes'])
    candidates = rows['winner-candidates03.json']
    for row, mask in zip(candidates['rows'][2:], [3, 0]):
        assert [r['mask'] for r in row['branches']] == [mask, mask]
        assert len(row['emission_orders']) == 24
        assert all('0:37536:20928:0029d20e' in r for r in row['emission_orders'])
    # The upper-left corner refutes a tempting density-only exclusion rule.
    # The constructive proof instead keeps every layer's prep dependency pending.
    counterexamples = []
    for x in range(-2, 12):
        for y in range(-2, 12):
            if not any(-2 <= x + dx < 12 and -2 <= y + dy < 12
                       for dx, dy in [(-1, 1), (-1, 0), (0, 1), (1, 1)]):
                counterexamples.append([x, y])
    assert counterexamples == [[-2, 11]]
    census = candidates['global_fifo_raster_census']
    assert next(i for i, r in enumerate(census) if r['mask'] == 0) == 78
    key_data = rows['native-keys03.json']
    assert len(key_data['packed_keys']) == 144
    assert len(key_data['visited_sources']) == 324
    for name in ('low_word', 'orientation_disabled_low_word'):
        target = key_data['target'][name]
        assert sum(r[name] == target for r in key_data['visited_sources']) == 1
    geometry = rows['geometry.json']
    assert geometry['summary']['first_resource_counts'] == [2, 25]
    cell = rows['native-cell.json']
    assert [len(r['regions']) for r in cell['runs']] == [2, 25, 25]
    assert cell['runs'][1]['regions'] == cell['runs'][2]['regions']
    assert all(len(r['calls']) == 144 for r in cell['runs'])
    high = cell['runs'][1]['regions'][0]
    assert high['count'] == 1
    point = struct.unpack('<4f', bytes.fromhex(high['points']))
    for region in cell['runs'][0]['regions']:
        bound = struct.unpack('<4f', bytes.fromhex(region['header'][:32]))
        assert math.dist(point[:3], bound[:3]) > bound[3]
    spatial = rows['native-spatial.json']
    assert spatial['positive']['hit'] and not spatial['far_negative']['hit']
    assert not any(r['hit'] for r in spatial['low_negatives'])
    assert spatial['native_cell_sha256'] == sha(evidence / 'native-cell.json')
    retirement = rows['native-retirement04.json']['runs']
    assert [r['retired'] for r in retirement] == [False, True]
    assert [r['new_origin'] for r in retirement] == [[-98, -100], [156, -100]]
    assert all(r['source_extent'] == [10, 10] and r['grid_reference_count'] == 2
               for r in retirement)
    series = rows['native-retirement04.json']['ordinary_shift_series']
    assert series['retirement_step'] == 38 and series['retirement_callbacks'] == 1
    assert [r['remaining_sources'] for r in series['steps']] == [1] * 37 + [0]
    query_rows = rows['native-query.json']['rows']
    assert [r['original_int2'] for r in query_rows[:2]] == [[10, 11], [-2, -2]]
    assert [r['converted_face_cell'] for r in query_rows[:2]] == [[37546, 20939], [37534, 20926]]
    code = {'native-probe.json': 'native_probe.py', 'native-cell.json': 'native_cell.py',
            'native-keys03.json': 'native_keys.py', 'native-spatial.json': 'native_spatial.py',
            'native-queue03.json': 'native_queue.py', 'native-dispatch04.json': 'native_dispatch.py',
            'native-retirement04.json': 'native_retirement.py', 'native-query.json': 'native_query.py'}
    for receipt, method in code.items():
        assert rows[receipt]['code_sha256'] == sha(evidence / method), method
    return {'classification': 'Offline consistency controls; native feasibility needs the static proof',
            'coordinates': len(coordinates), 'density_keys': len(order),
            'winner_original_int2': [[10, 11], [-2, -2]],
            'winner_converted_face_cells': [[37546, 20939], [37534, 20926]],
            'ordinary_first_resource_counts': [2, 25],
            'receipts': {name: sha(evidence / name) for name in RECEIPTS},
            'methods': {name: sha(evidence / name) for name in METHODS},
            'free': free_space()}


def replay(evidence, output):
    """Replay retained owned methods; no target invocation or new Ghidra export."""
    assert os.name == 'nt', 'Disposable native replay requires this Windows baseline'
    baseline = check(evidence)
    initial = read(evidence / 'initial.json')
    assert {p: sha(p) for p in initial['installed']} == initial['installed']
    output.mkdir(parents=True, exist_ok=False)
    for name in METHODS + ['initial.json']:
        shutil.copyfile(evidence / name, output / name)
    (output / 'functions').mkdir()
    # Preserve only ranges and referenced-address metadata needed by the mapper.
    # Raw instruction/decompiler text remains in the original ignored exports.
    for path in (evidence / 'functions').glob('*.txt'):
        source = path.read_text(encoding='utf8').split('DECOMPILE')[0]
        metadata = source.splitlines()[0] + '\n' + ''.join(
            'DATA [0x' + address + ']\n'
            for address in sorted(set(re.findall(r'\[0x([0-9a-f]+)\]', source))))
        (output / 'functions' / path.name).write_text(metadata, encoding='utf8')
    environment = dict(os.environ, D5S_OUTPUT=str(output.resolve()))
    invocations = [('geometry_compare.py', []), ('registration.py', []),
                   ('winner_candidates.py', ['winner-candidates03.json']),
                   ('native_probe.py', []), ('native_cell.py', []),
                   ('native_keys.py', []), ('native_spatial.py', []),
                   ('native_queue.py', ['native-queue03.json']),
                   ('native_dispatch.py', []), ('native_retirement.py', []),
                   ('native_query.py', [])]
    results = []
    for name, args in invocations:
        free_space()
        command = [sys.executable, '-B', str(output / name), *args]
        result = subprocess.run(command, cwd=ROOT, env=environment,
                                capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
        (output / (name + '.stdout.log')).write_bytes(result.stdout)
        (output / (name + '.stderr.log')).write_bytes(result.stderr)
        results.append({'method': name, 'exit': result.returncode})
        (output / 'execution.json').write_text(json.dumps(results, indent=2), encoding='utf8')
        assert result.returncode == 0, (name, result.returncode)
        diagnostics = result.stdout + result.stderr
        assert b'Traceback' not in diagnostics and b'Exception ignored' not in diagnostics, name
    repeated = check(output)
    # Paths/free-space vary; compare the complete numerical generation results.
    assert read(output / 'geometry.json')['results'] == read(evidence / 'geometry.json')['results']
    for name, member in [('native-cell.json', 'runs'), ('native-keys03.json', 'packed_keys'),
                         ('native-dispatch04.json', 'runs'), ('native-retirement04.json', 'runs'),
                         ('native-retirement04.json', 'ordinary_shift_series'), ('native-query.json', 'rows')]:
        assert read(output / name)[member] == read(evidence / name)[member], name
    (output / 'replay.json').write_text(json.dumps({'baseline': baseline, 'repeated': repeated,
                                                  'execution': results}, indent=2), encoding='utf8')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=['check', 'replay'])
    parser.add_argument('--evidence', type=Path, default=ROOT / '.local-work/d5s')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    evidence, output = args.evidence.resolve(), args.output.resolve()
    assert output.is_relative_to((ROOT / '.local-work').resolve()) and not output.exists()
    if args.mode == 'replay':
        replay(evidence, output)
    else:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(check(evidence), indent=2), encoding='utf8')
    print('PASS', args.mode, output)


if __name__ == '__main__':
    main()
