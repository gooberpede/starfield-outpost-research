# SPDX-License-Identifier: GPL-3.0-or-later
"""Offline immutable-input and Steam namespace reads; no writes or restoration.

Caller persists the returned diagnostics before enforcing zero changes. Existing
hash expectations are not replaced by observed values. Python stdlib only.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / '.local-work/resource-carinae-source-context/protected-before.json'


def pin(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def audit():
    changes = []
    rows = json.loads(MANIFEST.read_text())
    for row in rows:
        p = Path(row['path'])
        actual = pin(p) if p.is_file() else None
        if actual != row['sha256']:
            changes.append(dict(path=str(p), expected=row['sha256'], actual=actual))
    return dict(manifest_sha256=pin(MANIFEST), count=len(rows), changes=changes,
                historical_discrepancies=[r for r in rows if not r['match']])


def sync_snapshot():
    receipt = ROOT / '.local-work/resource-carinae/sync-paths-preflight02.json'
    prior = json.loads(receipt.read_text())
    remote = Path(prior['remote_path'])
    files = {}
    for p in sorted(remote.rglob('*')):
        assert not p.lstat().st_file_attributes & 0x400, p
        if p.is_file():
            files[p.relative_to(remote).as_posix()] = dict(bytes=p.stat().st_size, sha256=pin(p))
    return dict(remote_path=str(remote), remote=files,
                remotecache_sha256=pin(remote.parent / 'remotecache.vdf'),
                matches_historical=(files == prior['remote'] and
                    pin(remote.parent / 'remotecache.vdf') == prior['remotecache_sha256']))
