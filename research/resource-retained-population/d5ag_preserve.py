# SPDX-License-Identifier: GPL-3.0-or-later
"""Verify designated save/backups and historical raw streams by byte identity.

Reads the existing B2 protection receipt, policy, designated live/research saves,
loose backups and B1/B2 raw streams. Writes fresh ignored JSON only. Stdlib;
no game, save write, restore, database, network or Git mutation. This selected
identity check is not launch admission or a full active-save audit. Stop on
missing/changed input, non-loose designated backup or disk/output failure.
"""
from pathlib import Path
import json
import sys

from d5ae_baseline import guard, sha

ROOT = Path(__file__).resolve().parents[2]


def main():
    if not __debug__ or sys.flags.optimize:
        raise RuntimeError('Use Python -E -B')
    free = guard()
    prior = ROOT/'.local-work/d5ab/B2-APPROVED-002-preflight/receipt.json'
    if sha(prior) != '9af6437d5c1e615b71e4f3a20c84f0f4040a59e4ec2423d1ea8025f74400e6d5':
        raise ValueError('Historical protection receipt changed')
    protection = json.loads(prior.read_bytes())['protection']
    policy = ROOT/'research/resource-carinae-source-context/save_policy.json'
    baseline = json.loads((ROOT/'.local-work/d5ag/inputs02.json').read_bytes())
    if sha(policy) != baseline['policy_sha256']:
        raise ValueError('Task-start save policy changed')
    if json.loads(policy.read_bytes()) != protection['save_policy']:
        raise ValueError('Historical policy meaning differs')
    pins = {}
    for name, row in json.loads(policy.read_bytes())['designated'].items():
        pins[str(Path(protection['live_path'])/name)] = row['sha256']
        research = ROOT/'.local-work/savegames'/name
        if research.exists():
            pins[str(research)] = row['sha256']
        for backup in protection['backups'][name]:
            if backup['kind'] != 'LOOSE_BACKUP':
                raise ValueError('Unimplemented designated backup class')
            pins[backup['path']] = backup['sha256']
    sessions = {
        'ceb439b14ddc4db8b734526a124f1e879b64cd457774a87a6a67852fd4489894':
        'cd4762095a422fb537844546e923fff667e894a63b082b0205f3107786f49a5c',
        '5ed302aea9da7dc2261163b3dd1816e670a3c2f39891f1ec8d20094afa72b3a1':
        '4a8feb68f667f417967a0cd4a332cefde768658d254ead8d555b3e5f44515218'}
    for nonce, expected in sessions.items():
        pins[str(ROOT/'.local-work/d5x/live'/('session-'+nonce)/'events.bin')] = expected
    rows = {}
    for path, expected in pins.items():
        actual = sha(path)
        if actual != expected:
            raise ValueError('Protected identity changed: '+path)
        rows[path] = dict(sha256=actual, bytes=Path(path).stat().st_size)
    out = (ROOT/'.local-work/d5ag'/sys.argv[1]).resolve()
    if out.exists() or not out.is_relative_to(ROOT/'.local-work/d5ag'):
        raise ValueError('Fresh task-local receipt required')
    out.write_text(json.dumps(dict(rows=rows, free=free, method_sha256=sha(__file__),
                                  historical_protection_sha256=sha(prior),
                                  policy_sha256=sha(policy),
                                  historical_policy_sha256=protection['save_policy_sha256'],
                                  historical_policy_structured_equal=True,
                                  historical_policy_byte_equal=False), indent=2)+'\n',
                   encoding='utf8', newline='\n')
    print(json.dumps(dict(selected_protected_files=len(rows), free=free)))


if __name__ == '__main__':
    main()
