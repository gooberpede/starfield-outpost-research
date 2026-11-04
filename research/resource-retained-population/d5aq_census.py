# SPDX-License-Identifier: GPL-3.0-or-later
"""Authenticate N2's typed cohort and compute the conditional all-request census.

SOR-P-0002: reuses owned D5H atlas reader and roundtrip/native SIMD arithmetic;
adapts D5T's disposable converter fixture by output namespace only. Reads pinned
installed EXE/PlanetData, static lease, D5T fixture sources and authenticated
D5AP/N2 derivatives. Writes fresh ignored receipts and, with --publish-derived,
only the requested CSV/Markdown maps. The child executes original converter
instructions in private memory with explicit null lookup/manager fixtures.
No live process, observer, save, database, network or Git writes. Refuse identity,
disk-floor, missing input, reparse output, child failure and oracle disagreement;
preserve failed outputs. Process exit releases native mappings.
"""
import os
import sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):
    raise RuntimeError('Use pinned Python -E -B without optimization')

import argparse
from collections import Counter
import csv
import hashlib
import json
import re
from pathlib import Path
import shutil
import struct
import subprocess
from d5ap_analyze import guard, require, sha, write
from d5aq_oracle import convert, sample

ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / 'docs/experiments/resource-retained-population'
DESCRIPTOR = (0, (195, 109), (8, 0), (0, 0))
EXE = Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield/Starfield.exe')


def native_converter(out):
    """Replay the retained all-coordinate native converter in a fresh child."""
    prior = ROOT / '.local-work/d5t'
    pins = {r['path']: r['sha256'] for r in csv.DictReader((DOC / 'd5t-sources.csv').open(encoding='utf8'))}
    for path in [prior / n for n in ('start.py', 'native_probe.py', 'native_keys.py', 'native_queries.py', 'geometry.json', 'initial.json', 'native-queries05.json')]:
        name = path.relative_to(ROOT).as_posix()
        require(name in pins and sha(path) == pins[name], 'D5T support pin mismatch: ' + name)
    child = out / 'native-converter'
    child.mkdir()
    inputs = ['start.py', 'native_probe.py', 'native_keys.py', 'geometry.json', 'initial.json']
    for name in inputs:
        shutil.copyfile(prior / name, child / name)
    functions = json.loads((prior / 'native-queries05.json').read_bytes())['functions']
    data = EXE.read_bytes()
    pe = struct.unpack_from('<I', data, 0x3c)[0]
    count = struct.unpack_from('<H', data, pe + 6)[0]
    opts = struct.unpack_from('<H', data, pe + 20)[0]
    sections = [struct.unpack_from('<IIII', data, pe + 24 + opts + i * 40 + 8) for i in range(count)]
    (child / 'functions').mkdir()
    for function in functions:
        path = prior / 'functions' / (function['entry'] + '.txt')
        body = path.read_text(encoding='utf8')
        low, high = [int(v, 16) for v in re.search(r'\[\[([0-9a-f]+), ([0-9a-f]+)\]\]', body.splitlines()[0]).groups()]
        require(low == int(function['entry'], 16) and high - low + 1 == function['bytes'], 'Native function extent')
        offsets = [raw + low - 0x140000000 - start for _, start, size, raw in sections if start <= low - 0x140000000 and high - 0x140000000 < start + size]
        require(len(offsets) == 1 and hashlib.sha256(data[offsets[0]:offsets[0] + function['bytes']]).hexdigest() == function['sha256'], 'Installed native function pin')
        if path.relative_to(ROOT).as_posix() in pins:
            require(sha(path) == pins[path.relative_to(ROOT).as_posix()], 'Export pin')
        shutil.copyfile(path, child / 'functions' / path.name)
    original = (prior / 'native_queries.py').read_text(encoding='utf8')
    prefix = "import os,sys\nif not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE','') not in ('','0'):\n    raise RuntimeError('Use pinned Python -E -B')\n"
    target = child / 'native_queries.py'
    target.write_text(prefix + original, encoding='utf8', newline='\n')
    result = subprocess.run([sys.executable, '-E', '-B', str(target)], cwd=ROOT,
                            env=dict(os.environ, D5S_OUTPUT=str(child)), capture_output=True,
                            creationflags=subprocess.CREATE_NO_WINDOW)
    (child / 'stdout.log').write_bytes(result.stdout)
    (child / 'stderr.log').write_bytes(result.stderr)
    require(result.returncode == 0 and not result.stderr, 'Native converter child failed; retain logs')
    receipt = json.loads((child / 'native-queries05.json').read_bytes())
    return receipt, {name: sha(prior / name) for name in inputs + ['native_queries.py']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--analysis', type=Path, required=True)
    parser.add_argument('--summary-sha256', required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--publish-derived', action='store_true')
    args = parser.parse_args()
    floors = guard()
    require(sha(sys.executable) == 'cce21c0e8710e304273e98ac4b2b0f5aceb639acbcd2343cbaa5c4e81619c45b', 'Interpreter identity')
    require(sha(EXE) == '7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28', 'Executable identity')
    out = args.out.resolve()
    require(out.is_relative_to(ROOT / '.local-work/d5aq') and not out.exists(), 'Fresh task-local output')
    require(not any(p.is_symlink() or p.is_junction() for p in (out, *out.parents)), 'No reparse output')
    source = args.analysis.resolve()
    require(sha(source / 'summary.json') == args.summary_sha256, 'N2 summary identity')
    summary = json.loads((source / 'summary.json').read_bytes())
    for name, digest in summary['outputs'].items():
        require(sha(source / name) == digest, 'N2 derivative changed: ' + name)
    contenders = json.loads((source / 'contenders.json').read_bytes())
    groups = {family: [r for r in contenders if r['family'] == family] for family in (1, 2)}
    expected = {(x, y) for x in range(-2, 12) for y in range(-2, 12)}
    require(len(contenders) == 392 and len({r['task'] for r in contenders}) == 392, 'Unique typed task allocations')
    for family, cohort in groups.items():
        require(len(cohort) == 196 and {tuple(r['request']) for r in cohort} == expected, 'Actual cohort rectangle')
        require(all({e['kind'] for e in r['scheduler']} == set(range(1, 13)) for r in cohort), 'Twelve typed stages')
    density = {tuple(r['request']): r for r in groups[1]}
    layers = {tuple(r['request']): r for r in groups[2]}
    published = sorted(groups[1], key=lambda r: next(e['sequence'] for e in r['scheduler'] if e['kind'] == 1))
    require([tuple(r['request']) for r in published] == sorted(expected, key=lambda q: (q[0] - q[1], q[0])), 'Actual density publication ordering')
    publication_rank = {tuple(r['request']): i for i, r in enumerate(published)}
    core = json.loads((source / 'core.json').read_bytes())
    generation = next(r for r in core if r['sequence'] == 3961)
    observed = next(r for r in core if r['sequence'] == 3962)
    desc = bytes.fromhex(generation['descriptor'])
    semantic = (desc[0], tuple(struct.unpack_from('<2i', desc, 4)),
                tuple(struct.unpack_from('<2i', desc, 20)), tuple(struct.unpack_from('<2i', desc, 36)))
    require(semantic == DESCRIPTOR and observed['descriptor'] == generation['descriptor'], 'Consumed descriptor differs')
    require(observed['a'] == 3 and observed['request'] == [-2, 11], 'Direct retail witness')
    out.mkdir(parents=True)
    native, support = native_converter(out)
    native_rows = {tuple(r['original_int2']): r for r in native['rows']}
    require(set(native_rows) == expected, 'Native converter coverage')
    sys.path.insert(0, str(ROOT / 'research/resource-query-reachability'))
    import domains
    from roundtrip import projected
    import ctypes
    domains.LEASE = ROOT / '.local-work/resources-evidence-consolidation/d5r-input-lease01'
    manifest = domains.load('.local-work/resource-save52/build-v1/manifest.json',
                            '9d2ff9012a573595227c8feda5345de35286b807103665486239ddbe8cbfa9de')
    raster = domains.maps(manifest, {'0005e0de'})['0005e0de']
    config_path = ROOT / '.local-work/resource-query-reachability/native-bytes09.json'
    evidence_pins = {r['path']: r['sha256'] for r in csv.DictReader((DOC / 'd5t-sources.csv').open(encoding='utf8'))}
    require(sha(config_path) == evidence_pins[config_path.relative_to(ROOT).as_posix()], 'Arithmetic source pin')
    config = json.loads(config_path.read_bytes())
    require(sha('C:/Windows/System32/ucrtbase.dll') == '3c60056371f82e4744185b6f2fa0c69042b1e78804685944132974dd13f3b6d9', 'CRT identity')
    crt = ctypes.CDLL('C:/Windows/System32/ucrtbase.dll')
    for name in ('cos', 'atan2'):
        function = getattr(crt, name)
        function.argtypes = [ctypes.c_double] * (2 if name == 'atan2' else 1)
        function.restype = ctypes.c_double
    prior = {tuple(r['query']): r['mask'] for r in json.loads((ROOT / '.local-work/d5t/winner-candidates05.json').read_bytes())['global_fifo_raster_census']}
    rows, detailed = [], []
    for x, y in sorted(expected):
        q = (x, y)
        reference = sample(DESCRIPTOR, q, raster)
        n = native_rows[q]
        require(n['chart'] == 0 and n['converted_face_cell'] == reference['face'] and n['normalized_xy'] == reference['normalized'], 'Independent/native conversion mismatch')
        branches = []
        for fused in (False, True):
            tag, col, row, error = projected(0, *reference['face'], constants=config['sine_constants'], fused=fused, scalar_math=crt)
            byte = raster['faces'][tag]['mask'][256 * row + col]
            require((tag, col, row, byte & 15) == (reference['chart'], reference['column'], reference['row'], reference['mask']), 'Independent SIMD/oracle disagreement')
            branches.append(dict(fused=fused, error_cells=error))
        require(prior[q] == reference['mask'], 'Historical fixed-input census disagreement')
        d, layer = density[q], layers[q]
        sampled = d['task'] == summary['winner_task']
        require(not sampled or reference['mask'] == observed['a'], 'Direct retail mismatch')
        row = dict(original_x=x, original_y=y, density_task=d['task'], layer_task=layer['task'],
                   density_publication_rank=publication_rank[q],
                   source_allocation=d['source_allocation'], density_provider=next(e['sequence'] for e in d['scheduler'] if e['kind'] == 9),
                   face_x=reference['face'][0], face_y=reference['face'][1], chart=reference['chart'],
                   normalized_x=reference['normalized'][0], normalized_y=reference['normalized'][1],
                   raster_column=reference['column'], raster_row=reference['row'], raster_byte=f"0x{reference['byte']:02x}",
                   mask=f"0x{reference['mask']:x}", classification='PROVEN' if sampled else 'CONDITIONAL',
                   stage_validity='actual direct ordinary sample' if sampled else 'typed provider observed; first-miss generation conditional',
                   eligibility='actual winner' if sampled else 'individual first-miss reachability not inferred',
                   input_contract='D5AQ-C1', native_sites='0x14078d660;0x14096f5c0;0x142339340',
                   verification_handle=f'census.json#cells/{x},{y}')
        rows.append(row)
        detailed.append(dict(query=q, reference=reference, branches=branches, density_task=d['task'], layer_task=layer['task']))
    controls = {}
    controls['actual_publication_order'] = 'PASS: all 196 coordinates in (x-y,x) ascending order; not admission order'
    require([sample(DESCRIPTOR, q, raster)['mask'] for q in ((4, -1), (4, 1), (5, 0))] == [0, 3, 3], 'Authentic D5AG fixed-input cases')
    controls['d5ag_queries'] = 'PASS: 0,3,3 under D5AQ-C1/D5AG coordinate contract'
    for label, descriptor in [('y_minus_192', (0, (195, 108), (8, 0), (0, 0))),
                              ('y_plus_192', (0, (195, 110), (8, 0), (0, 0))),
                              ('fine_y_plus_1', (0, (195, 109), (8, 0), (0, 1)))]:
        changed = [sample(descriptor, q, raster)['mask'] for q in sorted(expected)]
        controls[label] = dict(counts=dict(Counter(changed)), differing_cells=sum(a != b['reference']['mask'] for a, b in zip(changed, detailed)))
    for label, call in [('absent_raster', lambda: sample(DESCRIPTOR, (0, 0), None)),
                        ('unqualified_chart', lambda: sample((2, (195, 109), (8, 0), (0, 0)), (0, 0), raster)),
                        ('unqualified_dimension', lambda: sample(DESCRIPTOR, (0, 0), raster, dimension=128))]:
        try:
            call()
        except ValueError:
            controls[label] = 'REFUSED as required'
        else:
            raise ValueError('Adverse input silently assigned: ' + label)
    counts = Counter(r['mask'] for r in rows)
    require(counts == {'0x0': 28, '0x3': 168}, 'Unexpected census; investigate rather than publish')
    write(out / 'census.json', dict(schema='sor-d5aq-census/1', contract='D5AQ-C1',
          classification='conditional outcome map, not winner probabilities', analysis_summary_sha256=args.summary_sha256,
          consumed_generation_sequence=3961, direct_sample_sequence=3962, descriptor_semantic=semantic,
          actual_task_count=392, cells=detailed, counts=dict(counts), controls=controls,
          sources={str(config_path.relative_to(ROOT)): sha(config_path),
                   'd5aq_census.py': sha(__file__), 'd5aq_oracle.py': sha(Path(__file__).with_name('d5aq_oracle.py'))},
          native_fixture_support=support, native_functions=native['functions'], floors=floors, postflight_floors=guard()))
    with (out / 'request-mask-map.csv').open('x', encoding='utf8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)
    if args.publish_derived:
        (DOC / 'd5aq-request-mask-map.csv').write_bytes((out / 'request-mask-map.csv').read_bytes())
        table = ['# D5AQ conditional request mask map', '',
                 'All 196 N2 density coordinates, paired with their distinct layer tasks, are',
                 'enumerated in the [CSV](d5aq-request-mask-map.csv). Contract **D5AQ-C1** is',
                 'defined in the [method](d5aq-mask-method.md). `C0`/`C3` denote CONDITIONAL',
                 'first-construction outcomes. `N3` is N2\'s PROVEN direct sampled winner.',
                 'The other 195 rows have no individual first-miss eligibility certificate.', '',
                 '| y / x | ' + ' | '.join(str(x) for x in range(-2, 12)) + ' |',
                 '| --- | ' + ' | '.join('---' for _ in range(14)) + ' |']
        indexed = {(r['original_x'], r['original_y']): r for r in rows}
        for y in range(11, -3, -1):
            cells = [('N3' if (x, y) == (-2, 11) else 'C' + indexed[x, y]['mask'][-1]) for x in range(-2, 12)]
            table.append('| ' + str(y) + ' | ' + ' | '.join(cells) + ' |')
        table += ['', '| Mask | Coordinates | Percent of coordinates | Direct N2 sample | Conditional | Unresolved samples under C1 |',
                  '| --- | ---: | ---: | ---: | ---: | ---: |',
                  '| 0x0 | 28 | 14.285714% | 0 | 28 | 0 |',
                  '| 0x3 | 168 | 85.714286% | 1 | 167 | 0 |', '',
                  'The complete machine-readable grid is the Cartesian `(original_x, original_y)`',
                  'CSV key; there is exactly one row per cell. These are outcome counts, not',
                  'ready-at-one-time counts or winner probabilities. All 196 density tasks later',
                  'execute in N2; 195 bypass the already visited target.', '',
                  'Historical winner overlay, kept separate from the C1 counterfactual: B2',
                  '`(5,0)`, D5AK A0 `(8,3)`, A1 `(-1,11)`, D5AL B0 `(0,0)` and N2 `(-2,11)`',
                  'each directly sampled `0x3`. They are five constructions across four retail',
                  'sessions. Only N2\'s consumed descriptor is freshly bound here; matching C1',
                  'predictions do not fill other episodes\' unrecorded effective inputs.', '',
                  'Authored derivative REVIEW-REQUIRED; raw raster/native evidence LOCAL-ONLY.']
        (DOC / 'd5aq-mask-map.md').write_text('\n'.join(table) + '\n', encoding='utf8', newline='\n')
    print(json.dumps(dict(out=str(out), counts=counts, rows=len(rows), controls=controls)))


if __name__ == '__main__':
    main()
