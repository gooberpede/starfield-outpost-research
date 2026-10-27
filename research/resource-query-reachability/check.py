# SPDX-License-Identifier: GPL-3.0-or-later
"""D5H offline checks: framed controls, held-out journal and sine arithmetic.

Reads explicit authenticated leases, owned reducers and current authored tables.
Writes one fresh ignored JSON receipt. Does not generate geometry, execute a
target, modify inputs, install dependencies or mutate Git. Stdlib/owned code.
"""
import collections
import csv
from decimal import Decimal, localcontext
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import struct
import sys

from native_sine import sine

ROOT = Path(__file__).resolve().parents[2]
LOCAL = ROOT / '.local-work/resource-query-reachability'


def pin(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def framed(path, expected, ack=False):
    assert pin(path) == expected
    data, at, rows = path.read_bytes(), 0, []
    while at < len(data):
        magic, seq, size, digest = struct.unpack_from('<4sQI32s', data, at)
        at += 48
        body = data[at:at+size]
        at += size
        assert magic == b'SRO1' and seq == len(rows)+1 and len(body) == size
        assert hashlib.sha256(body).digest() == digest
        rows.append(json.loads(body))
    assert at == len(data) and [r['kind'] for r in rows] == ['SESSION', 'SAMPLE', 'END']
    if ack:
        value = json.loads(path.with_suffix('.ack.json').read_text())
        assert value['sha256'] == expected and value['bytes'] == len(data)
    return rows[1]


def main():
    output = Path(sys.argv[1]).resolve()
    assert output.is_relative_to(ROOT / '.local-work') and not output.exists()
    tables = ROOT / 'docs/experiments/resource-query-reachability'
    sources = list(csv.DictReader((tables / 'source-domains.csv').open()))
    assert len(sources) == len({(r['case'], r['source_key']) for r in sources}) == 25
    assert collections.Counter(r['classification'] for r in sources) == {
        'PROVED INVARIANT':19,'PROVED VARIABLE':1,'UNRESOLVED':5}
    assert sum(int(r['insertion_attempt_cells']) for r in sources) == 6340
    prior_domain=json.loads((LOCAL/'domains04.json').read_text())
    computed={(r['case'],r['source_key']):r for r in prior_domain['rows']}
    assert set(computed)=={(r['case'],r['source_key']) for r in sources}
    for source in sources:
        original=computed[source['case'],source['source_key']]
        assert len(original['attempt_cells'])==int(source['insertion_attempt_cells'])
        assert original['native_arithmetic_branches']==json.loads(source['native_arithmetic_branches'])
    admission=json.loads((LOCAL/'admission01.json').read_text())
    assert pin(tables/'source-domains.csv')==admission['source_sha256']
    assert pin(tables/'counterexamples.csv')==admission['counterexamples_sha256']
    assert pin(ROOT/admission['proof'])==admission['proof_sha256']
    examples=list(csv.DictReader((tables/'counterexamples.csv').open()))
    assert len(examples)==33
    assert all(r['actual_first_miss']=='NOT_PROVED' for r in examples[:31])
    assert all(r['actual_first_miss']=='PROVED_STATIC_FEASIBLE' for r in examples[31:])
    assert {r['raster_mask'] for r in examples[31:]}=={'0','3'}
    controls = list(csv.DictReader((ROOT / 'docs/experiments/resource-predictability-contrast/native-controls.csv').open()))
    lease = ROOT / '.local-work/resources-evidence-consolidation/d5h-input-lease03'
    files = {pin(p): p for p in lease.rglob('*.bin')}
    control_results = []
    for row in controls:
        sample = framed(files[row['native_sha256']], row['native_sha256'])
        assert ('source_context' in sample) == (row['native_source_context'] == 'PRESENT')
        control_results.append(dict(capture=row['capture'], sha256=row['native_sha256'],
                                    framed=True, source_context=row['native_source_context']))
    assert len(control_results) == 10
    # Independent convergent Taylor oracle; no native polynomial coefficients.
    config = json.loads((LOCAL / 'native-bytes09.json').read_text())
    constants = config['sine_constants']
    sine_error = 0.0
    with localcontext() as ctx:
        ctx.prec = 70
        angles = [(-math.pi + i * (2.5 * math.pi / 1000)) for i in range(1001)]
        angles += [0.0, -0.0, math.pi/2, -math.pi/2, math.pi,
                   math.nextafter(math.pi/2, -math.inf), math.nextafter(math.pi/2, math.inf)]
        for angle in angles:
            x = Decimal.from_float(angle)
            term, reference = x, x
            for n in range(1, 70):
                term *= -x*x / Decimal((2*n)*(2*n+1))
                reference += term
            for fused in (False, True):
                error = abs(Decimal.from_float(sine(angle, constants, fused)) - reference)
                sine_error = max(sine_error, float(error))
                assert error < Decimal('1e-12')
    held = ROOT / '.local-work/resources-evidence-consolidation/d5h-heldout-lease04/.local-work/resource-combined-acquisition'
    journal = held / 'retail-attempt01/events.jsonl'
    assert pin(journal) == '19dd7b956eacd74f3c38a3179f56f5bce2115f45033337e1ed5d3f005cc2f79b'
    spec = importlib.util.spec_from_file_location('d5h_owned_reducer', ROOT / 'research/resource-combined-acquisition/reduce.py')
    reducer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(reducer)
    tracker = reducer.Tracker()
    kinds, sites = collections.Counter(), collections.Counter()
    for line in journal.open(encoding='utf8'):
        event = json.loads(line)
        kinds[event['kind']] += 1
        if event['kind'] == 'SAMPLE':
            sites[event.get('site', 'UNKNOWN')] += 1
        tracker.feed(event)
    result = tracker.result()
    assert result['status'] == 'CONSUMER_ONLY' and not result['constructions']
    assert result['historical_epoch'] is None
    held_results = []
    expected = {row['path']:row['sha256'] for row in csv.DictReader(
        (ROOT / 'docs/experiments/resource-combined-acquisition/phase-b-sources.csv').open())}
    for number in (12205, 12901, 12906, 12907, 15119):
        name = f'.local-work/resource-combined-acquisition/retail-attempt01/capture-{number:05}.bin'
        path = held / 'retail-attempt01' / Path(name).name
        sample = framed(path, expected[name], ack=True)
        held_results.append(dict(capture=number, site=sample['site'], complete=sample.get('required_reads_complete')))
    value = dict(source_counts=dict(collections.Counter(r['classification'] for r in sources)),
        tested_cells=6340, simd_arithmetic_evaluations=12680, geometry_rerun=False,
        domain_replay_qualification='Prior exhaustive domains04 replay; this check verifies its table correspondence rather than recomputing all projections',
        domain_replay_sha256=pin(LOCAL/'domains04.json'),
        native_admission_receipt_sha256=pin(LOCAL/'admission01.json'),
        original_candidate_rows=31,admitted_static_witnesses=2,helper_sha256=pin(Path(__file__)),
        controls=control_results, control_ack_revalidation='Not rerun; old controls checked by hash and internal framing only',
        sine_oracle_angles=len(angles), sine_oracle_error=sine_error,
        journal_sha256=pin(journal), kinds=dict(kinds), sites=dict(sites),
        heldout_status=result['status'], heldout_constructions=len(result['constructions']),
        heldout_consumptions=len(result['consumptions']), native_epoch=None, heldout_receipts=held_results)
    with output.open('x', encoding='utf8', newline='\n') as stream:
        json.dump(value, stream, indent=2, allow_nan=False)
        stream.write('\n')
    print(json.dumps(value, indent=2))


if __name__ == '__main__':
    main()
