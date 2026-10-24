# SPDX-License-Identifier: GPL-3.0-or-later
"""Isolated D4E predictions, then full cohort and ten native comparisons.

Reads completed local corpora/requests and frozen earlier classification tables.
Writes exclusive ignored predictions and hashes before opening native answers.
Comparisons retain old classifications beside new diagnostic outcomes. Uses
owned isolation/decoder methods and stdlib; no target or protected-input writes.
"""
import argparse
import collections
import csv
import datetime
import json
from pathlib import Path
import struct
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / 'research' / p) for p in
               ('resource-standalone', 'resource-owner-root')]
from audit import pin, write
import verify
from save52_compare import classify


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--build', type=Path, required=True)
    parser.add_argument('--controls', type=Path, required=True)
    parser.add_argument('--reuse', type=Path)
    args = parser.parse_args()
    out = args.output.resolve()
    assert out.is_relative_to(ROOT / '.local-work/resource-slot-provenance')
    out.mkdir(exist_ok=False)
    results, controls = {}, {}
    def infer(label, request, build, variant):
        dest = out / label
        dest.mkdir(exist_ok=True)
        if args.reuse:
            previous = args.reuse / label
            freeze = json.loads((args.reuse / 'prediction-freeze.json').read_text())
            corpus = str(build / f'{variant}.json')
            assert pin(build / f'{variant}.json') == freeze['corpora'][corpus]
            source = previous / f'{request.stem}-{variant}-stdout.json'
            assert pin(source) == freeze['outputs'][str(source.resolve())]
            audit = json.loads((previous / f'{request.stem}-{variant}-audit.json').read_text())
            assert not audit['inference_forbidden'] and audit['denied_probes'] == 8
            (dest / source.name).write_bytes(source.read_bytes())
            (dest / f'{request.stem}-{variant}-audit.json').write_bytes(
                (previous / f'{request.stem}-{variant}-audit.json').read_bytes())
            return json.loads(source.read_text())
        command = [sys.executable, '-I', '-S', '-B', str(ROOT / 'research/resource-standalone/isolate.py'),
            '--code', str(build.resolve() / 'code'), '--corpus', str(build.resolve() / f'{variant}.json'),
            '--request', str(request.resolve())]
        run = subprocess.run(command, cwd=dest, capture_output=True)
        (dest / f'{request.stem}-{variant}-stdout.json').write_bytes(run.stdout)
        (dest / f'{request.stem}-{variant}-audit.json').write_bytes(run.stderr)
        assert run.returncode == 0, run.stderr.decode()
        audit = json.loads(run.stderr)
        assert not audit['inference_forbidden'] and audit['denied_probes'] == 8
        return json.loads(run.stdout)
    prior = ROOT / '.local-work/resource-save52-d3/revision06/first-pass-v1'
    for request in sorted(prior.glob('*-request.json')):
        pair = [infer('cohort', request, args.build, v) for v in ('normalized', 'expanded')]
        assert pair[0]['regions'] == pair[1]['regions']
        assert pair[0]['availability'] == pair[1]['availability']
        results[request.name.removesuffix('-request.json')] = pair[0]
    for body in ('0005e0de', '0005e4da'):
        request = out / f'{body}-request.json'
        write(request, verify.request(body))
        controls[body] = [infer('controls', request, args.controls, v) for v in ('normalized', 'expanded')]
        assert controls[body][0]['regions'] == controls[body][1]['regions']
    write(out / 'prediction-freeze.json', dict(time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        outputs={str(p): pin(p) for p in out.rglob('*-stdout.json')},
        corpora={str(b / f'{v}.json'): pin(b / f'{v}.json') for b in (args.build, args.controls)
                 for v in ('normalized', 'expanded')}, native_answers_opened_by_this_driver=False))
    native = []
    for body, folder, attempt, captures in (
        ('0005e0de', 'resource-region-ancestry', '01', (299, 325, 696, 716)),
        ('0005e4da', 'resource-carinae', '02', (1270, 1280, 1301)),
        ('0005de4c', 'resource-tungsten-acquisition', '01', (829, 2881, 2941))):
        outputs = controls.get(body) or [results['D2-81a75b']] * 2
        for number in captures:
            path = ROOT / f'.local-work/{folder}/retail-attempt{attempt}/capture-{number:05d}.bin'
            row = verify.native(path)
            resource = f'{struct.unpack_from("<I", bytes.fromhex(row["selected"]["raw_resource"]), 0x28)[0]:08x}'
            for variant, result in zip(('normalized', 'expanded'), outputs):
                source = None
                if body == '0005de4c':
                    raw = bytes.fromhex(row['source_context']['raw_source'])
                    ox, oy = result['request']['descriptor']
                    x, y = struct.unpack_from('<2i', raw, 0x10)
                    source = f'0:{ox+x}:{oy+y}:{struct.unpack_from("<I", raw)[0]:08x}'
                matches = [r for r in result['regions'] if r['resource'] == resource
                    and r['ordered_xyzw_le'] == row['geometry']['ordered_xyzw']
                    and r['native_bound_le'] == row['geometry']['raw_region'][:32]
                    and (source is None or r['source'] == source)]
                native.append(dict(body=body, capture=number, variant=variant, resource=resource,
                    exact_matches=len(matches), receipt_sha256=pin(path),
                    source_identity=source,
                    callback_equal=all(r['callback']['accepted'] == (row['decision'] == 'ACCEPT') for r in matches)))
    rows = []
    for previous in csv.DictReader((ROOT / 'docs/experiments/resource-save52-d3/associations-final.csv').open(encoding='utf8')):
        current = classify(results[previous['case']], previous['resource'], previous['d3'] == 'ALTERNATIVE_ADMISSION')
        rows.append(dict(**previous, d4e_diagnostic=current, changed=current != previous['d3']))
    write(out / 'association-comparison.json', rows)
    write(out / 'native-comparison.json', native)
    inventory = list(csv.DictReader((ROOT / 'docs/experiments/resource-save52-d3/cases-final.csv').open(encoding='utf8')))
    write(out / 'inventory.json', [dict(**r, d4e_status=results[r['case']]['status'] if r['case'] in results
                                     else 'PRESERVED_DISABLED_EXCLUSION') for r in inventory])
    write(out / 'summary.json', dict(cases=len(inventory), predicted=len(results), associations=len(rows),
        native_controls=len(native) // 2, all_exact=all(r['exact_matches'] == 1 and r['callback_equal'] for r in native),
        changed_associations=[r for r in rows if r['changed']],
        held_out_counts=dict(collections.Counter(r['d4e_diagnostic'] for r in rows if r['control'] == 'False')),
        historical_baselines_modified=False))
    print(json.dumps(dict(predicted=len(results), all_exact=all(r['exact_matches'] == 1 for r in native),
        changed_associations=sum(r['changed'] for r in rows))))


if __name__ == '__main__':
    main()
