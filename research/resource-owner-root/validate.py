# SPDX-License-Identifier: GPL-3.0-or-later
"""Conditional map geometry, then held-out native comparison and regressions.

Reads frozen D4C inputs, D3 corpus/request and pinned installed descriptors;
persists diagnostic predictions before opening primary D4A answers. Also reruns
all frozen D2/D3 requests under existing isolation and seven native controls.
Writes only a fresh ignored output directory. No target or input writes.
"""
import argparse
import copy
import json
from pathlib import Path
import struct
import subprocess
import sys
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / 'research' / n) for n in
               ('resource-standalone', 'resource-geometry', 'resource-pattern-selection')]
import builder
import predictor_d3 as predictor
import verify
from audit import pin, write


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--freeze', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--corpus', type=Path)
    ap.add_argument('--geometry-only', action='store_true')
    args = ap.parse_args()
    frozen, out = args.freeze.resolve(), args.output.resolve()
    assert out.is_relative_to(ROOT / '.local-work')
    out.mkdir(parents=True, exist_ok=False)
    seal = json.loads((frozen / 'freeze-v1.json').read_text())
    assert all(pin(p) == h for p, h in seal['inputs'].items())
    assert all(pin(frozen / n) == h for n, h in seal['outputs'].items())
    source = json.loads((frozen / 'inputs-v1.json').read_text())
    candidates = json.loads((frozen / 'candidates-v1.json').read_text())['ordered']
    base = ROOT / '.local-work/resource-save52-d3'
    corpus = args.corpus or base / 'build-v6/normalized.json'
    envelope = json.loads(corpus.read_text())
    previous = json.loads((base / 'revision06/first-pass-v1/D2-81a75b-stdout.json').read_text())
    records = {h['formid']: (h, fs) for h, fs in builder.esm_records(builder.ESM,
        {b'BIOM', b'RSGD', b'IRES'}, repeated=True)}
    selected = next(r for r in source['components'] if r['biome'] == source['selected_biome'])
    active = None
    for tag, raw in records[int(selected['rsgd'], 16)][1]:
        if tag == b'RNAM':
            active = int.from_bytes(raw, 'little')
        elif tag == b'DNAM' and active == source['selected_root']:
            descriptor = raw
            break
    resources = []
    for fid in candidates:
        rarity = builder.last(records[fid][1], b'SNAM')[0]
        weight = envelope['payload']['settings'][rarity] if rarity else 1.0
        resources.append(dict(resource=f'{fid:08x}',
            block=list(struct.unpack_from('<8f', descriptor, 40*(rarity+7)))+[0, 0], weight=weight))
    original = predictor.geometry.populate_source
    calls = []
    def diagnostic(request, constants):
        request = copy.deepcopy(request)
        if request['source'].endswith(':0028be0d'):
            request['ordered_resources'] = resources
            calls.append(request)
        return original(request, constants)
    with patch.object(predictor.geometry, 'populate_source', side_effect=diagnostic):
        result = predictor.predict(envelope, previous['request'])
    write(out / 'conditional-prediction.json', result)
    write(out / 'conditional-inputs.json', dict(resources=resources, calls=calls,
        corpus_path=str(corpus), corpus_sha256=pin(corpus),
        selected_dnam_sha256=builder.hashlib.sha256(descriptor).hexdigest(),
        basis='Installed descriptor; low mask zero from frozen D3 qualified source neighborhood'))
    write(out / 'prediction-before-answers.json', dict(
        prediction_sha256=pin(out / 'conditional-prediction.json'),
        input_sha256=pin(out / 'conditional-inputs.json'),
        freeze_sha256=pin(frozen / 'freeze-v1.json'),
        primary_call_answers_read=False))
    # First primary answer read occurs only after the preceding exclusive writes.
    events = ROOT / '.local-work/resource-tungsten-acquisition/retail-attempt01/events.jsonl'
    rows = [json.loads(line) for line in events.read_text().splitlines()]
    samples = [r for r in rows if r['kind'] == 'SAMPLE']
    accepted = [r for r in samples if r.get('decision') == 'ACCEPT']
    comparisons = []
    for accept in accepted:
        fid = f'{struct.unpack_from("<I", bytes.fromhex(accept["selected"]["raw_resource"]), 0x28)[0]:08x}'
        matches = [r for r in result['regions'] if r['resource'] == fid and
                   r['ordered_xyzw_le'] == accept['geometry']['ordered_xyzw'] and
                   r['native_bound_le'] == accept['geometry']['raw_region'][:32]]
        comparisons.append(dict(capture=accept['capture'], resource=fid,
                                matches=len(matches), sources=[r['source'] for r in matches]))
    actual = []
    for r in samples:
        if r['capture'] in (86, 87, 88, 89):
            actual.append(struct.unpack_from('<I', bytes.fromhex(r['ires']['raw']), 0x28)[0])
    write(out / 'native-comparison.json', dict(
        predicted_ordinary=candidates, observed_ordinary=actual,
        ordered_sequence_equal=candidates == actual,
        first_difference=dict(index=0, predicted=candidates[0], observed=actual[0]),
        geometry=comparisons, all_three_exact=all(r['matches'] == 1 for r in comparisons),
        candidate_completeness=False, historical_epoch='UNKNOWN',
        events_sha256=pin(events), corpus_incremental_bytes=0,
        no_corrected_production_corpus=True))
    if args.geometry_only:
        print(json.dumps(dict(geometry=comparisons, candidates_equal=candidates == actual)))
        return
    results = []
    for label, source_dir in [('D2', ROOT / '.local-work/resource-save52'),
                              ('D3', base / 'revision06')]:
        build, prior = source_dir / 'build-v1', source_dir / 'first-pass-v1'
        dest = out / label
        dest.mkdir()
        for request in sorted(prior.glob('*-request.json')):
            command = [sys.executable, '-I', '-S', '-B', str(ROOT / 'research/resource-standalone/isolate.py'),
                '--code', str(build / 'code'), '--corpus', str(build / 'normalized.json'), '--request', str(request)]
            run = subprocess.run(command, cwd=dest, capture_output=True)
            output = dest / request.name.replace('-request', '-stdout')
            output.write_bytes(run.stdout)
            (dest / request.name.replace('-request', '-audit')).write_bytes(run.stderr)
            assert run.returncode == 0, run.stderr.decode()
            expected = prior / output.name
            assert json.loads(run.stdout) == json.loads(expected.read_text())
            audit = json.loads(run.stderr)
            assert not audit['inference_forbidden'] and audit['denied_probes'] == 8
            results.append(dict(version=label, case=request.stem, exact=True, sha256=pin(output)))
    write(out / 'roster.json', results)
    verify.run(ROOT / '.local-work/resource-standalone/build03', out / 'seven-controls')
    print(json.dumps(dict(geometry=comparisons, candidates_equal=candidates == actual,
                          frozen_requests=len(results), seven_controls='PASS')))


if __name__ == '__main__':
    main()
