# SPDX-License-Identifier: GPL-3.0-or-later
"""Offline immutable-input and Steam namespace reads; no writes or restoration.

Caller persists the returned diagnostics before enforcing zero changes. Existing
hash expectations are not replaced by observed values. Python stdlib only.
"""
import hashlib
import json
from pathlib import Path
from save_policy import load_policy, classify, compare, snapshot, partition, changes

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / '.local-work/resource-carinae-source-context/protected-before.json'
LIVE = Path('C:/Users/User/Documents/My Games/Starfield/Saves')


def pin(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def audit_rows(rows, live_root, policy):
    """Only the exact active namespace gets transient treatment; archives stay strict."""
    failures = []
    skipped = []
    expected_live = {}
    for row in rows:
        p = Path(row['path'])
        if p.parent == live_root:
            kind = classify(p.name, policy)
            if row['sha256'] is not None:
                expected_live[p.name] = dict(bytes=0, sha256=row['sha256'])
            if kind['protection'] == 'TRANSIENT':
                skipped.append(str(p))
                continue
            if kind['protection'] == 'UNCLASSIFIED':
                failures.append(dict(path=str(p), reason='UNCLASSIFIED_SAVE'))
        actual = pin(p) if p.is_file() else None
        if actual != row['sha256']:
            failures.append(dict(path=str(p), expected=row['sha256'], actual=actual))
    current = snapshot(live_root, policy)
    # The old protected manifest has no size column; full content equality is
    # independently checked by its immutable SHA-256 pins above.
    for name in expected_live:
        expected_live[name]['bytes'] = current.get(name, {}).get('bytes', 0)
    delta = compare(expected_live, current, policy)
    if not delta['ok']:
        failures.append(dict(namespace=str(live_root), comparison=delta))
    return dict(count=len(rows), changes=failures, excluded_live_transients=skipped,
                live_classification=partition(current, policy), live_comparison=delta,
                historical_discrepancies=[r for r in rows if not r['match']])


def audit(policy=None):
    policy = load_policy() if policy is None else policy
    result = audit_rows(json.loads(MANIFEST.read_text(encoding='utf8')), LIVE, policy)
    return dict(result, manifest_sha256=pin(MANIFEST))


def sync_snapshot(policy=None):
    policy = load_policy() if policy is None else policy
    receipt = ROOT / '.local-work/resource-carinae/sync-paths-preflight02.json'
    prior = json.loads(receipt.read_text())
    remote = Path(prior['remote_path'])
    files = {}
    for p in sorted(remote.rglob('*')):
        if p.is_relative_to(remote / 'Saves'):
            continue
        assert not p.lstat().st_file_attributes & 0x400, p
        if p.is_file() and not p.is_relative_to(remote / 'Saves'):
            files[p.relative_to(remote).as_posix()] = dict(bytes=p.stat().st_size, sha256=pin(p))
    saves = snapshot(remote / 'Saves', policy)
    old_saves = {n[6:]: row for n, row in prior['remote'].items() if n.startswith('Saves/')}
    old_other = {n: row for n, row in prior['remote'].items() if not n.startswith('Saves/')}
    result = compare(old_saves, saves, policy)
    return dict(remote_path=str(remote), remote=saves, other=files,
                remotecache_sha256=pin(remote.parent / 'remotecache.vdf'),
                comparison=result,
                matches_historical=(result['ok'] and files == old_other and
                    pin(remote.parent / 'remotecache.vdf') == prior['remotecache_sha256']))


def sync_equal(before, after, policy):
    """Keep Cloud metadata/non-save checks strict; save diagnostics may churn."""
    return (before['remote_path'] == after['remote_path'] and before['other'] == after['other']
            and before['remotecache_sha256'] == after['remotecache_sha256']
            and compare(before['remote'], after['remote'], policy)['ok'])
