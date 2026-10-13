"""SPDX-License-Identifier: GPL-3.0-or-later
Read-only offline consolidation driver. Stdlib and existing owned readers only.
Reads frozen JSON, protected corpus archives/ESM and sealed 050/060 captures.
Writes exclusive ignored receipts and temporary decoder scratch (removed by reader).
No game, native execution, network, configuration, database or original writes.
See docs/position-model/self-check.md for dependencies, effects and limits.
"""
import argparse
import collections
import importlib.util
import json
from pathlib import Path
import struct
import subprocess
import sys

from durable_position_model import reconstruct
from durable_position_v2 import reproduce
from beacon_terrain_projection import f32, split_local
from audit_activated_grid import offset
from verify_position_v2 import guard, digest, verify

ROOT = Path(__file__).resolve().parents[2]
PINS = {
    'docs/experiments/engine-oracle/inputs.json': '9fe2924ff7bc444714fbab685893b8d8e0572dc2c7aad96cbd06de8aac93ad91',
    'docs/experiments/engine-oracle/predictions.json': 'a8a7402697ed866a3410d4bd58796de513c7ca11f89e770a80deb5a8651a0487',
    'save-analysis/scripts/durable_position_model.py': '06e42a5610ff7474298d32648c8e4a118e13c6ec17e938cd296603323bca378c',
}


def write(path, data):
    with path.open('x', encoding='utf8', newline='\n') as f:
        json.dump(data, f, indent=2, allow_nan=False)
        f.write('\n')


def command(out, name, args):
    guard()
    with (out / (name + '.txt')).open('xb') as log:
        p = subprocess.run([sys.executable, '-B', *args], cwd=ROOT,
                           stdout=log, stderr=subprocess.STDOUT)
    if p.returncode:
        raise RuntimeError(f'{name}: exit {p.returncode}; see retained log')


def hierarchy(data):
    return (data[0], *(struct.unpack_from('<i', data, c)[0] * 192
        + struct.unpack_from('<i', data, s)[0] * 12
        + struct.unpack_from('<i', data, f)[0] for c, s, f in ((4,20,36),(8,24,40))))


def native_grids(module, inputs):
    rows = []
    for event in module.records(5):
        if event['kind'] != 3:
            continue
        wid, _ = module.identity(event)
        center = struct.unpack('<3f', module.blob(event, 'center', 12))
        translation = struct.unpack('<2f', module.blob(event, 'translation', 8)[:8])
        xy = [f32(center[i] + translation[i]) for i in range(2)]
        floors = tuple(split_local(v)[0] for v in xy)
        assert floors == struct.unpack('<2i', module.blob(event, 'floor_xy', 8))
        source = hierarchy(module.blob(event, 'input_hierarchy', 44))
        result = hierarchy(module.blob(event, 'result', 44))
        assert offset(*source, *floors) == result
        candidates = [i for i in inputs if i['identity']['workshop_id'] == wid
                      and i['source']['sample'] in ('Save25', 'Save26')]
        assert len(candidates) == 2
        body = f"{struct.unpack_from('<I', module.blob(event, 'landscape', 0x58), 0x54)[0]:08X}"
        for candidate in candidates:
            prediction = reproduce(candidate)
            assert prediction['body'] == body
            assert prediction['center_hex'][:16] == struct.pack('<2f', *xy).hex()
            assert [result[0], *result[1:]] == [prediction['native_cell']['tag'], *prediction['native_cell']['xy']]
        rows.append(dict(sequence=event['sequence'], workshop=wid, body=body,
            native_center=module.blob(event, 'center', 12).hex(),
            translation=list(translation), floor=list(floors), source=list(source), result=list(result),
            exact_xy_bits=True, structural_grid=True,
            full_xyz_equal=prediction['center_hex'] == module.blob(event, 'center', 12).hex()))
    assert len(rows) == 40
    grain = collections.Counter((r['workshop'], tuple(r['translation']), tuple(r['result'])) for r in rows)
    assert len(grain) == 2 and set(grain.values()) == {20}
    assert any(r['source'][2] % 192 // 12 == 0 and r['result'][2] % 192 // 12 == 2 for r in rows)
    assert all(not r['full_xyz_equal'] for r in rows)
    return rows


def run(out):
    disk = guard()
    # All writes are confined to ignored task receipts and the owned extraction run.
    out = out.resolve()
    allowed = (ROOT / '.local-work/position-consolidation').resolve()
    if not out.is_relative_to(allowed) or out == allowed:
        raise ValueError('OUTPUT_MUST_BE_NEW_CHILD_OF_TASK_LOCAL_DIRECTORY')
    out.mkdir(parents=True, exist_ok=False)
    for path, expected in PINS.items():
        assert digest(ROOT / path) == expected, path
    inputs = json.loads((ROOT / 'docs/experiments/engine-oracle/inputs.json').read_bytes())
    predictions = json.loads((ROOT / 'docs/experiments/engine-oracle/predictions.json').read_bytes())
    assert [reconstruct(i) for i in inputs] == predictions
    baseline_rows = []
    for data, expected in zip(inputs, predictions):
        result = reproduce(data)
        expected_residual = struct.pack('<3f', *expected['residual']).hex()
        assert result['center_hex'] == expected['center_hex']
        assert result['residual_hex'] == expected_residual
        baseline_rows.append(dict(sample=data['source']['sample'],
            workshop=data['identity']['workshop_id'], baseline_center=expected['center_hex'],
            current_center=result['center_hex'], baseline_residual=expected_residual,
            current_residual=result['residual_hex'], baseline_cell=expected['cell'],
            current_cell=[result['native_cell']['tag'], *result['native_cell']['xy']]))
    write(out / 'baseline-comparison.json', baseline_rows)
    command(out, 'position-tests', ['-m', 'unittest', 'discover', '-s', 'save-analysis/scripts', '-p', 'test_durable_position*.py', '-v'])
    command(out, 'decoder-tests', ['-m', 'unittest', 'discover', '-s', 'research/cross-session-center', '-p', 'test_*.py', '-v'])
    # Reuse the corpus reader rather than introducing another extraction model.
    run_name = 'consolidation-' + out.name
    command(out, 'corpus', ['save-analysis/scripts/research_durable_center.py', '--run', run_name])
    extraction = ROOT / '.local-work/durable-center' / run_name / 'results.json'
    regression = verify(out / 'frozen', extraction=extraction)
    samples = json.loads(extraction.read_bytes())
    assert not next(s for s in samples if s['label'] == 'Save3')['rows']
    mature = next(s for s in samples if s['label'] == 'HIST-0267')
    mature_beacons = [r for r in mature['rows'] if r['role'] == 'beacon']
    assert len(mature_beacons) == 19
    assert all(r['workshop']['delta_hex'] == '00' * 12 for r in mature_beacons)
    spec = importlib.util.spec_from_file_location('cross_session', ROOT / 'research/cross-session-center/verify.py')
    native = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(native)
    command(out, 'native-replay', ['research/cross-session-center/verify.py', '--output', str(out / 'native')])
    rows = native_grids(native, inputs)
    write(out / 'native-grids.json', rows)
    unknown = dict(inputs[0], frame=0x2b, site_cell=None)
    partial = reproduce(unknown)
    assert partial['native_cell'] is None and partial['stages']['cell'] == 'UNKNOWN'
    for path, expected in PINS.items():
        assert digest(ROOT / path) == expected, path
    summary = dict(result='PASS', frozen_regressions=regression['frozen_cases'],
        archive_model_input_comparisons=regression['archive_cases'], corpus_labels=len(samples),
        mature_compensations=19, native_grid_calls=40, distinct_workshop_geometries=2,
        native_workshop_bodies=1, full_native_xyz_equivalence='NOT TESTED',
        missing_site='UNKNOWN', evidence_basis='saved redecodes + sealed native replay + synthetic controls; no new native execution',
        pins=PINS, disk_before=disk, disk_after=guard(), argv=sys.argv, python=sys.version,
        source_hashes={str(p.relative_to(ROOT)): digest(p) for p in sorted((ROOT/'save-analysis/scripts').glob('*.py'))},
        limitations=['23 frozen cases are regressions, not native oracles',
                    '050 captured-input replay covers two geometries on Kreet; save join conditional',
                    '060 center matches do not prove historical restoration or continuous lifetime',
                    'Save27/28 landing context inherited from reports; not extra model fixtures'])
    write(out / 'receipt.json', summary)
    human = ('PASS: 23 frozen regressions; exact center/residual bits and structural cells.\n'
             'PASS: 23 archive input comparisons; Save3 negative; 19 mature zero compensations.\n'
             'PASS: 16 position tests + 12 decoder controls.\n'
             'PASS: 40 native XY/grid replays = 2 geometries, 20 repeats each, 1 body.\n'
             'UNKNOWN: missing qualified site cell; full native XYZ equivalence NOT TESTED.\n'
             f'Command: {subprocess.list2cmdline([sys.executable, "-B", *sys.argv])}\n'
             f'Receipt: {out / "receipt.json"}\n')
    with (out / 'summary.txt').open('x', encoding='utf8', newline='\n') as f:
        f.write(human)
    print(human, end='')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    try:
        run(parser.parse_args().output)
    except Exception as error:
        print(f'FAIL: {type(error).__name__}: {error}', file=sys.stderr)
        raise
