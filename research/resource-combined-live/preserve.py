# SPDX-License-Identifier: GPL-3.0-or-later
"""Rehash the approved Phase B baseline after process exit, offline only.

Reads every prior evidence and Phase A file named in the prelaunch receipts,
and Git HEAD/index. Writes one exclusive ignored receipt, including failures.
Python stdlib only; no target, save, configuration, network or Git writes.
This verifies byte preservation, not scientific meaning or publication rights.
"""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
LOCAL = ROOT / '.local-work/resource-combined-acquisition'


def pin(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    assert subprocess.check_output(['powershell', '-NoProfile', '-Command',
        '@(Get-Process Starfield -ErrorAction SilentlyContinue).Count'], text=True).strip() == '0'
    before = json.loads((LOCAL / 'phase-b-evidence-before01.json').read_text(encoding='utf8'))
    baseline = json.loads((LOCAL / 'phase-b-baseline01.json').read_text(encoding='utf8'))
    result = dict(schema='sor-d5b-phase-b-preservation/1',
        utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), game_absent=True,
        baseline_sha256=pin(LOCAL / 'phase-b-baseline01.json'),
        evidence_before_sha256=pin(LOCAL / 'phase-b-evidence-before01.json'), groups={})
    for name, expected in [('prior_evidence', before['pins']), ('phase_a', baseline['phase_a_pins'])]:
        observed = {}; failures = []
        for path, digest in expected.items():
            try:
                observed[path] = pin(path)
                if observed[path] != digest:
                    failures.append(dict(path=path, reason='hash differs'))
            except OSError as error:
                failures.append(dict(path=path, reason=str(error)))
        result['groups'][name] = dict(count=len(expected), pins=observed, failures=failures)
    result['head'] = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    result['index_sha256'] = pin(ROOT / '.git/index')
    result['staged_paths'] = subprocess.check_output(['git', 'diff', '--cached', '--name-only'], cwd=ROOT, text=True)
    result['ok'] = (all(not g['failures'] for g in result['groups'].values())
        and result['head'] == baseline['head'] and result['index_sha256'] == baseline['index_sha256']
        and not result['staged_paths'])
    with (LOCAL / 'pilot-preservation01.json').open('x', encoding='utf8', newline='\n') as stream:
        json.dump(result, stream, indent=2)
        stream.write('\n')
    print(json.dumps(dict(ok=result['ok'], counts={k:v['count'] for k,v in result['groups'].items()})))
    assert result['ok']


if __name__ == '__main__':
    main()
