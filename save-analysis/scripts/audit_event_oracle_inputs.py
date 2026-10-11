# SPDX-License-Identifier: GPL-3.0-or-later
"""Offline input-integrity audit for SOR-EXP-0024; no live target access.

Reads exact prior receipt paths, protected Save25/26 paths and archived capture
journals/raw sections through the existing project inspector. Writes one NEW
JSON receipt at --output (parent must exist). CPython stdlib only; no installs,
native calls, source/save/config/database writes or new scientific acquisition.
Private paths stay in ignored receipts. Integrity is not semantic validation.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[2]


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(4 * 1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def audit():
    free = {d: shutil.disk_usage(d).free for d in ('C:/', 'D:/')}
    if min(free.values()) < 40_000_000_000:
        raise RuntimeError('Disk guard')
    spec = importlib.util.spec_from_file_location(
        'sor_inspector', ROOT / 'runtime/beacon-observer/inspect_capture.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    phase = json.loads((ROOT / '.local-work/engine-oracle-live/phase1-01/postflight.json').read_text())
    initial = json.loads((ROOT / '.local-work/beacon-observer-live-review/initial-01/final-summary.json').read_text())
    protected = {}
    for r in phase['protected_checks']:
        p = Path(r['path'])
        if p.suffix.lower() == '.sfs':
            actual = digest(p)
            if actual != r['sha256']:
                raise ValueError('Protected-save mismatch: ' + str(p))
            protected[str(p)] = actual
    if len(protected) != 4:
        raise ValueError('Expected four protected Save25/26 paths')
    sessions = [
        ('phase1', ROOT / '.local-work/beacon-observer-live/session-9236-127079640', phase['captures'], 9412),
        ('initial', ROOT / '.local-work/beacon-observer-live/session-17596-91165828', initial['snapshots'], 5233),
    ]
    results = []
    for name, session, checkpoints, expected in sessions:
        count = 0
        for item in checkpoints:
            label = item['label']
            data = module.inspect(session / label)
            if data['journal_truncated_final_line'] or not data['marker']:
                raise ValueError('Incomplete journal/marker: ' + label)
            count += data['raw_sections']
            results.append({'session': name, 'label': label,
                            'raw_sections': data['raw_sections'],
                            'journal_sha256': digest(session / label / 'records.jsonl'),
                            'native_output': data.get('native_workshop_output')})
        if count != expected:
            raise ValueError('Unexpected raw-section count: ' + name)
    frozen = {n: digest(ROOT / 'docs/experiments/engine-oracle' / n)
              for n in ('inputs.json', 'predictions.json', 'validation-protocol.md', 'Phase1-checkpoints.csv')}
    return {'scope': 'INTEGRITY_ONLY_NOT_ENGINE_VALIDATION', 'free_bytes': free,
            'protected_saves': protected, 'frozen': frozen, 'checkpoints': results}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = audit()
    with args.output.open('x', encoding='utf-8', newline='\n') as f:
        json.dump(result, f, indent=2)
        f.write('\n')
    print('PASS:', len(result['checkpoints']), 'checkpoints,',
          sum(r['raw_sections'] for r in result['checkpoints']), 'raw sections')
