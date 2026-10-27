# SPDX-License-Identifier: GPL-3.0-or-later
"""Offline historical rehearsal through authenticated existing archive access.

Reads the active pinned archive/index, earlier ledgers and owned math/readers.
Restores only explicitly selected historical operands/receipts into a fresh
existing access workspace; writes new task-local derivatives. Original members,
archives, historical verdicts and source code remain unchanged. No live target,
save edits, new acquisition, installation, network or publication. Historical
replay is not prospective validation and is not personally blinded.
"""
import csv
import argparse
import importlib.util
import json
from pathlib import Path
import sys

from audit import ROOT, LOCAL, pin, write
from gate import canonical, digest


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--label', required=True)
    parser.add_argument('--lease', type=Path)
    parser.add_argument('--lease-sha256')
    args = parser.parse_args()
    if not args.label.isalnum():
        raise ValueError('LABEL')
    out = LOCAL/args.label; out.mkdir()
    write(out/'command.json', dict(argv=sys.argv, helper_sha256=pin(Path(__file__))))
    sys.path.insert(0, str(ROOT/'research/resources-evidence-consolidation'))
    from cutover import trusted_configuration, transaction
    config = trusted_configuration(); tx = transaction(config)
    # This authenticates the scientific archive without changing the separate,
    # already failed strict excluded-ZIP namespace verdict.
    with tx.store.authenticated() as (entry, archive, members):
        available = {r['path']: r for r in entry['rows']}
    controls = list(csv.DictReader((ROOT/'docs/experiments/resource-predictability-contrast/native-controls.csv').open()))
    selected = []
    for row in controls:
        names = [name for name, r in available.items() if r['sha256'] == row['native_sha256']]
        if not names:
            raise ValueError('MISSING_PINNED_CONTROL')
        selected.append(sorted(names)[0])
    prefix = '.local-work/resource-combined-acquisition/retail-attempt01/'
    selected += [prefix+f'capture-{n:05d}'+suffix for n in (12205,12901,12906,12907,15119) for suffix in ('.bin','.ack.json')]
    operands = ['.local-work/resource-feynman-d5/inputs-v2.json',
        '.local-work/resource-feynman-d5/build04/normalized.json',
        '.local-work/resource-construction-mask-selection/conditional-results.json']
    selected += operands
    journal_name = prefix+'events.jsonl'
    selected.append(journal_name)
    if bool(args.lease) != bool(args.lease_sha256):
        raise ValueError('LEASE_REQUIRES_INDEPENDENT_DIGEST')
    if args.lease:
        from access import lease_rows
        destination = args.lease.resolve()
        lease = lease_rows(destination, args.lease_sha256)
        if {r['path'] for r in lease['rows']} != set(selected):
            raise ValueError('LEASE_SELECTION_CHANGED')
        result = dict(destination=str(destination), lease_sha256=args.lease_sha256, reused=True)
    else:
        destination = ROOT/('.local-work/resources-evidence-consolidation/d5k-'+args.label+'-lease')
        result = tx.store.restore(destination, selected)
    write(out/'lease.json', result)
    assert all(pin(destination/name) == available[name]['sha256'] for name in selected)
    sys.path[1:1] = [str(ROOT/'research/resource-geometry'), str(ROOT/'save-analysis/scripts'),
                   str(ROOT/'research/resource-slot-provenance'), str(ROOT/'research/resource-query-reachability')]
    import predictor_d4e
    from conditional import generate
    c = predictor_d4e.validate(json.loads((destination/operands[1]).read_bytes()))
    cases = json.loads((destination/operands[0]).read_bytes())['cases']
    selected_case = next(r for r in cases if r['case'] == 'D2-84e101')
    source = next(r for r in selected_case['sources'] if r['source_key'] == '0:37536:20928:0029d20e')
    prediction = generate(c, selected_case['request'], source, [0,3])
    assert canonical(prediction) == canonical(generate(c, selected_case['request'], source, [3,0]))
    write(out/'prediction.json', prediction)
    write(out/'prediction-freeze.json', dict(prediction_sha256=pin(out/'prediction.json'),
        methods={str(p.relative_to(ROOT)): pin(p) for p in
            (ROOT/'research/blinded-outpost-validation/conditional.py', ROOT/'research/resource-geometry/geometry.py',
             ROOT/'research/resource-geometry/context.py', ROOT/'save-analysis/scripts/resource_spatial.py')},
        note='Historical rehearsal; prior answers known; no prospective blindness claimed'))
    # Only after retaining the historical reproduction do we read native bytes.
    reader = load('d5k_framed', ROOT/'research/resource-query-reachability/check.py')
    framed_controls = []
    for row, name in zip(controls, selected[:len(controls)]):
        sample = reader.framed(destination/name, row['native_sha256'])
        framed_controls.append(dict(capture=row['capture'], sha256=row['native_sha256'], framed=True))
    samples = []
    journal = (destination/journal_name).read_bytes()
    # Independent committed ledger pin, separate from the restored index.
    if digest(journal) != '19dd7b956eacd74f3c38a3179f56f5bce2115f45033337e1ed5d3f005cc2f79b':
        raise ValueError('HISTORICAL_JOURNAL_IDENTITY')
    events = [json.loads(line) for line in journal.splitlines() if line]
    journal_samples = {r['capture']: r for r in events if r.get('kind') == 'SAMPLE'}
    for n in (12205,12901,12906,12907,15119):
        name = prefix+f'capture-{n:05d}.bin'
        sample = reader.framed(destination/name, available[name]['sha256'], ack=True)
        assert sample == journal_samples[n]
        samples.append(sample)
    consumer = load('d5k_consumer', ROOT/'research/resource-combined-acquisition/consumer.py')
    from truth import reduce_positive
    reduction = reduce_positive(journal, digest(journal), consumer, '0005e0de', ['000057d4','000057d0','000057cf'],
        'b0e207c2dee2c1b6', source['source_key'], [0,37536,20928])
    assert len(reduction['regions']) == 3 and reduction['complete'] is False
    write(out/'positive-truth.json', reduction)
    from compare import compare
    identity = dict(trial='f'*32, body='HISTORICAL', body_formid='0005e0de', workshop='b0e207c2dee2c1b6',
                    session=digest(journal)[:32], epoch='0'*32)
    cp = dict(identity, schema='sor-blind-comparable/1', scope_complete=False, sources=[dict(source=source['source_key'],
        alternatives=[dict(mask=a['mask'], regions=[{k: r[k] for k in ('resource','points_le','bound_le')} for r in a['paths']],
            presence=sorted({r['resource'] for r in a['paths'] if r['admission'].get('accepted') is True})) for a in prediction['alternatives']])])
    ct = dict(identity, schema='sor-blind-truth/1', oracle='ORDINARY_WORKSHOP_TRANSFER', complete=False,
        sources=[dict(source=source['source_key'], regions=[{k: r[k] for k in ('resource','points_le','bound_le')} for r in reduction['regions']],
                      presence=sorted({r['resource'] for r in reduction['regions']}))])
    comparison = compare(cp, ct)
    write(out/'comparison.json', comparison)
    # A mismatch here would remain a scientific correspondence result. The
    # adapter's three independently bound chains, not game agreement, are tested.
    bad = reduce_positive(journal, digest(journal), consumer, '0005e0de', ['000057d4','000057d0','000057cf'],
        '0'*16, source['source_key'], [0,37536,20928])
    assert not bad['regions'] and bad['absence'] == 'UNKNOWN'
    stale = b''.join(canonical(dict(r, updater_token=999) if r.get('site') == 'spatial_transfer_payload' else r) for r in events)
    assert not reduce_positive(stale, digest(stale), consumer, '0005e0de', ['000057d4'],
        'b0e207c2dee2c1b6', source['source_key'], [0,37536,20928])['regions']
    from saved_adapter import adapt
    inputs = json.loads((ROOT/'docs/experiments/engine-oracle/inputs.json').read_bytes())
    saved = []
    for row in inputs[:4]:
        result = adapt([row], 'f'*32, row['identity']['workshop_id'].lower())
        saved.append(dict(sample=row['source']['sample'], location=result['location'],
                          reconstructed_saved_center_le=result['saved_reconstruction']['center_hex'], effective='UNKNOWN'))
    write(out/'saved-controls.json', saved)
    write(out/'summary.json', dict(historical_only=True, strict_preservation='FAIL; excluded legacy ZIPs',
        lease=str(destination), lease_sha256=pin(destination/'LEASE.json'),
        unchanged_selected_members=all(pin(destination/name) == available[name]['sha256'] for name in selected),
        controls=framed_controls, positive_chains=3, complete_census=False, historical_correspondence=comparison,
        saved_controls=len(saved), frozen_historical_results_modified=False))
    print('Historical replay: 10 framed controls, 3 positive-only consumer chains, 4 saved location controls; no prospective validation')


if __name__ == '__main__':
    main()
