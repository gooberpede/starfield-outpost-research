# SPDX-License-Identifier: GPL-3.0-or-later
"""Verify protected saves, backups, analysis identities and original archives.

SOR-P-0002: source-informed adaptation of owned d5ai_preserve.py and D5AD
baseline guard and D5AM chronology authenticator. Reads historical pinned
protection/analysis rosters, designated bytes and every original sealed payload/
ZIP member; writes one exclusive D5AM-local receipt. Stdlib only. No game,
save/configuration write, restoration, database opening, download or Git change.
This selected offline audit is not full active-save or future launch admission.
"""
import os
import sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):
    raise RuntimeError('Use pinned Python -E -B without optimization')

import json
from pathlib import Path
from d5ad_baseline import guard, sha

ROOT = Path(__file__).resolve().parents[2]


def require(value, message):
    if not value:
        raise ValueError(message)


def main():
    out = Path(sys.argv[1]).absolute().resolve()
    require(out.is_relative_to(ROOT / '.local-work/d5am') and not out.exists(), 'Fresh D5AM-local output required')
    require(not any(p.is_symlink() or p.is_junction() for p in (out, *out.parents)), 'Reparse output path')
    free = guard()
    prior = ROOT / '.local-work/d5ab/B2-APPROVED-002-preflight/receipt.json'
    require(sha(prior) == '9af6437d5c1e615b71e4f3a20c84f0f4040a59e4ec2423d1ea8025f74400e6d5', 'Historical protection changed')
    protection = json.loads(prior.read_bytes())['protection']
    policy = ROOT / 'research/resource-carinae-source-context/save_policy.json'
    require(json.loads(policy.read_bytes()) == protection['save_policy'], 'Protected naming/designation policy changed')
    pins = {}
    for name, row in json.loads(policy.read_bytes())['designated'].items():
        pins[str(Path(protection['live_path']) / name)] = row['sha256']
        research = ROOT / '.local-work/savegames' / name
        if research.exists():
            pins[str(research)] = row['sha256']
        for backup in protection['backups'][name]:
            require(backup['kind'] == 'LOOSE_BACKUP', 'Unsupported backup class')
            pins[backup['path']] = backup['sha256']
    roster = ROOT / '.local-work/d5x/identity05/identity.json'
    database = json.loads(roster.read_bytes())['database']
    pins.update(database)
    rows = {}
    for path, expected in pins.items():
        actual = sha(path)
        require(actual == expected, 'Protected bytes differ: ' + path)
        rows[path] = dict(sha256=actual, bytes=Path(path).stat().st_size)
    chronology=ROOT/'research/resource-retained-population/d5am_chronology.py'
    require(sha(chronology)=='905594aa31e335e7e707493e4ee9b3cd08cd4bc4ca520e04ce4cfa57f5e136f9','Accepted chronology method changed')
    summary_path=ROOT/'.local-work/d5am/chronology06/summary.json'
    require(sha(summary_path)=='9c0ca2949550f94c41793618f40bf249d7348ed8e2788d8d866b768f1772cd87','Reviewed historical inventory changed')
    expected_sessions={session['case']:session for session in json.loads(summary_path.read_bytes())['sessions']}
    import d5am_chronology
    raw_sessions={}
    for label,folder,archive,zip_pin in d5am_chronology.CASES:
        _,verified,authentication=d5am_chronology.authenticate(ROOT/folder,archive,zip_pin)
        require(authentication==expected_sessions[label]['archive'],'Original archive/manifest identity changed')
        require(all(sha(path)==pin['sha256'] for path,pin in verified.items()),'Original payload changed during preservation')
        raw_sessions[label]=authentication
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open('x', encoding='utf8', newline='\n') as stream:
        json.dump(dict(schema='sor-d5am-selected-preservation/1', rows=rows,
                       historical_protection_sha256=sha(prior), policy_sha256=sha(policy),
                       database_roster_sha256=sha(roster), method_sha256=sha(__file__),
                       raw_sessions=raw_sessions,chronology_method_sha256=sha(chronology),chronology_summary_sha256=sha(summary_path),
                       guard_sha256=sha(ROOT / 'research/resource-retained-population/d5ad_baseline.py'),
                       initial_free=free, final_free=guard(),
                       scope='Selected designated originals/backups, file-only original analysis-core hashes, and complete original sealed payload/ZIP comparison; this method opens no Ghidra project and is not a complete live-save audit.'), stream, indent=2)
        stream.write('\n')
    print(json.dumps(dict(protected_files=len(rows), database_files=len(database),raw_payloads=sum(row['payload_files'] for row in raw_sessions.values()), result='PASS', out=str(out))))


if __name__ == '__main__':
    main()
