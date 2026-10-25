# SPDX-License-Identifier: GPL-3.0-or-later
"""Proposal admission and restart reconciliation only; no deletion entrypoint.

Reads externally pinned allowlist/recovery receipts, exact source handles and
authenticated archive. Returns a dry-run decision. Never writes a journal to
historical directories or calls any file removal primitive.
"""
import hashlib
from pathlib import Path

import access as a


def prepare(store, root, plan_path, expected_plan, recovery_path, expected_recovery, journal=None):
    plan = a.e.authenticate(a.output(plan_path), expected_plan)
    recovery = a.e.authenticate(a.output(recovery_path), expected_recovery)
    if (plan.get('schema') != 'sor-cargo-retirement/1' or
            plan.get('authority') != 'DELETION NOT AUTHORIZED' or
            plan.get('index_sha256') != store.index_sha or
            plan.get('archive_sha256') != store.archive_sha or
            recovery.get('state') != 'RESTORED-TESTED' or
            recovery.get('index_sha256') != store.index_sha or
            recovery.get('archive_sha256') != store.archive_sha or
            recovery.get('manifest_sha256') != store.manifest_sha or
            recovery.get('members') != len(plan['rows'])):
        raise a.Error('Plan/recovery identity or state mismatch')
    a.e.names_valid([r['path'] for r in plan['rows']])
    with store.authenticated(True) as (entry, archive, members):
        if not plan['rows']:
            raise a.Error('Empty retirement set')
        for row in plan['rows']:
            if (row['path'] == a.e.MANIFEST or row['path'] not in members or
                    any(row[k] != members[row['path']][k] for k in ('sha256', 'bytes')) or
                    row.get('member') != row['path'] or row.get('owner') != entry['owner'] or
                    row.get('index_sha256') != store.index_sha):
                raise a.Error('Orphaned/substituted allowlist row')
    names = {r['path'] for r in plan['rows']}
    if journal is not None:
        if (set(journal) != {'state', 'plan_sha256', 'pending', 'completed'} or
                journal['plan_sha256'] != expected_plan or
                journal['state'] not in ('PREPARED', 'AWAITING-APPROVAL') or
                journal['pending'] or journal['completed']):
            raise a.Error('Ambiguous recovery; reconcile every intended removal before retry')
    # Reserve persistent journal/control margin before any prospective activity.
    free = a.e.space(2 * len(a.e.encode(plan)) + 4 * 1024 * 1024)
    a.e.inspect(root, plan['rows'])
    for row in plan['rows']:
        p = a.e.canonical(Path(root) / row['path'], root)
        with a.e.locked(p) as (stream, info):
            stat = __import__('os').fstat(stream.fileno())
            if row.get('file_id') is not None and (stat.st_ino != row['file_id'] or stat.st_dev != row['device']):
                raise a.Error('Source file identity changed')
    return dict(state='AWAITING-APPROVAL', plan_sha256=expected_plan,
                files=len(names), deleted=0, free=free,
                execution='No real executor supplied; future executor requires separate review and approval')
