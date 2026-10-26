# SPDX-License-Identifier: GPL-3.0-or-later
"""Replay the real historical resource corpus reader from authenticated restore.

Reads restored historical modules, corpora, request and frozen output identities.
Runs the unchanged project-owned isolation driver in fresh empty directories;
writes stdout, audit stderr and an exclusive equivalence receipt. No game, save,
installed content, network, archive mutation or research-result changes.
"""
import hashlib
import argparse
import json
from pathlib import Path
import subprocess
import sys

from cutover import ROOT, OUT, store, save, e


def run(receipt=OUT / 'restore.json'):
    restored = json.loads(Path(receipt).read_text())
    destination = Path(restored['destination'])
    lease = e.authenticate(destination / 'LEASE.json', restored['lease_sha256'])
    base = '.local-work/resource-slot-provenance/build-controls02/'
    case = '.local-work/resource-construction-mask-selection/regression01/'
    selected = [base + 'code/' + name + '.py' for name in (
        'context', 'geometry', 'predictor', 'resource_availability', 'resource_spatial')]
    selected += [base + name for name in ('normalized.json', 'expanded.json', 'preparation.json')]
    selected += [case + '0005e0de-request.json', case + 'prediction-freeze.json']
    with store().authenticated(False) as (entry, archive, members):
        available = {r['path']: r for r in entry['rows']}
        leased = {r['path']: r for r in lease['rows']}
        for name in selected:
            if leased.get(name) != available.get(name) or name not in available:
                raise e.Error('Replay input absent from authenticated archive/lease')
        inputs = e.inspect(destination, [available[n] for n in selected])
    freeze = json.loads((destination / case / 'prediction-freeze.json').read_text())
    output = OUT / 'consumer-replay01'
    output.mkdir()
    results = []
    for kind in ('normalized', 'expanded'):
        cwd = output / (kind + '-empty-cwd')
        cwd.mkdir()
        command = [sys.executable, '-I', '-S', '-B', str(ROOT / 'research/resource-standalone/isolate.py'),
                   '--code', str(destination / base / 'code'), '--corpus', str(destination / base / (kind + '.json')),
                   '--request', str(destination / case / '0005e0de-request.json')]
        result = subprocess.run(command, cwd=cwd, capture_output=True)
        (output / (kind + '-stdout.json')).write_bytes(result.stdout)
        (output / (kind + '-stderr.json')).write_bytes(result.stderr)
        if result.returncode:
            raise e.Error('Historical corpus replay failed; retain stdout/stderr')
        expected_name = str(ROOT / case / 'controls' / ('0005e0de-request-' + kind + '-stdout.json'))
        expected = freeze['outputs'][expected_name]
        observed = hashlib.sha256(result.stdout).hexdigest()
        audit = json.loads(result.stderr)
        if observed != expected or audit['denied_probes'] != 8 or audit['inference_forbidden']:
            raise e.Error('Corpus output/audit differs from frozen historical contract')
        runtime = Path(sys.base_prefix).resolve()
        for event in audit['events']:
            if event['phase'] == 'inference' and event['allowed'] and 'path' in event:
                path = Path(event['path'])
                if not path.is_relative_to(destination) and not path.is_relative_to(runtime):
                    raise e.Error('Inference read outside restored inputs or interpreter runtime')
        results.append(dict(kind=kind, command=command, returncode=result.returncode,
                       stdout_bytes=len(result.stdout), expected_sha256=expected, observed_sha256=observed,
                       denied_probes=audit['denied_probes'], inference_forbidden=audit['inference_forbidden']))
    save(OUT / 'consumer-replay.json', dict(results=results, inputs=inputs,
         lease_sha256=restored['lease_sha256'], driver_sha256=e.pin(ROOT / 'research/resource-standalone/isolate.py'),
         executed_method_sha256=e.pin(Path(__file__)), scope='Two complete historical corpus-reader outputs; no new native or live validation'))
    print(json.dumps(results, indent=2), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--lease-receipt', type=Path, default=OUT / 'restore.json')
    run(parser.parse_args().lease_receipt)
