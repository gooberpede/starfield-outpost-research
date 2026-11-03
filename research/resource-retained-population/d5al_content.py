# SPDX-License-Identifier: GPL-3.0-or-later
"""Content-based phase guards for prospective D5AL Episode B.

Reads exact plans/sources, protected-input audits and selected file bytes. Writes
only fresh private pre/postflight receipts and the inherited restoration COPY.
No launch, deployment, debugger, process intervention, original-save write or
network. The native DLL and frozen D5AI/P4 sources remain unchanged. SOR-P-0002:
source-informed adaptation of d5ab_p4_operations.py and d5ai_operations.py.
Use installed Python -E -B. Fail on content/path/policy/identity/disk failure;
timestamp-only differences are diagnosed after validating the relevant bytes.
"""
import sys
import os
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):
    raise RuntimeError('Use Python -E -B')

import argparse
import copy
import importlib.util
import json
from pathlib import Path

import d5ai_operations as original
from d5ai_episode import require, ROOT, scope_for_episode, same_structure
from common import guard, regular, sha, fresh

POLICY = 'sor-d5al-content-timestamp/1'
ADAPTERS = {Path(__file__).resolve(), Path(__file__).with_name('d5al_episode.py').resolve()}


class TimestampPending(RuntimeError):
    """Unstable metadata during equal-content reads requires another checkpoint."""


def adapter_pins(plan):
    require(plan.get('episode') == 'B' and same_structure(plan.get('scope'), scope_for_episode('B')),
            'Only the approved Episode B scope is supported')
    require(plan.get('timestamp_policy') == POLICY, 'Explicit content-based timestamp plan required')
    pins = plan.get('episode_b_adapter_pins', {})
    require({Path(p).resolve() for p in pins} == ADAPTERS and len(pins) == 2,
            'Exact two Episode B adapter sources required')
    for path, digest in pins.items():
        require(sha(regular(path)) == digest, 'Episode B adapter source changed: ' + path)


def content_guard(path, row, digest, always=False):
    """Check one pinned file; metadata differences alone never reject it."""
    path = regular(path)
    require(path.is_file(), 'Missing guarded file: ' + str(path))
    require(set(row) >= {'bytes', 'mtime_ns'} and isinstance(digest, str) and len(digest) == 64,
            'Incomplete independent content guard')
    before = path.stat()
    require(before.st_size == row['bytes'], 'Guarded file size changed: ' + str(path))
    before = regular(path).stat()
    require(before.st_size == row['bytes'], 'Guarded file size changed before read')
    require(sha(path) == digest, 'Guarded file content changed: ' + str(path))
    after = regular(path).stat()
    require(after.st_size == row['bytes'], 'Guarded file size changed during read')
    require(after.st_ino == before.st_ino, 'Guarded file identity changed during read')
    return dict(path=str(path), timestamp_changed=after.st_mtime_ns != row['mtime_ns'],
                metadata_unstable_during_read=after.st_mtime_ns != before.st_mtime_ns,
                old_mtime_ns=row['mtime_ns'], observed_mtime_ns=after.st_mtime_ns,
                content_sha256_verified=digest)



def lightweight(plan, preflight):
    """Retain namespace/identity gates and positively hash all guarded file content."""
    adapter_pins(plan)
    original.phase_pins(plan)
    guard()
    module = original.legacy()
    policy_module = module.policy_module()
    policy = policy_module.load_policy()
    previous = preflight['protection']
    require(policy_module.policy_hash(policy) == previous['save_policy_sha256'], 'Save policy changed')
    current = policy_module.partition(policy_module.sizes(previous['live_path'], policy), policy)
    require(not current['unclassified'], 'Unclassified live save')
    require(current['protected'] == {name: dict(bytes=row['bytes']) for name, row in previous['protected_live'].items()},
            'Protected live save namespace/size changed')
    for folder, names in preflight['remote_protected_sizes'].items():
        remote = policy_module.partition(policy_module.sizes(folder, policy), policy)
        require(not remote['unclassified'] and remote['protected'] == names,
                'Protected remote namespace/size changed')
    configurations, definitions = previous['config'], previous['definitions']
    require(not set(configurations) & set(definitions), 'Ambiguous configuration/definition roster')
    require(set(previous['file_guards']) == set(configurations) | set(definitions), 'Incomplete file guard roster')
    diagnostics = []
    for path, row in previous['file_guards'].items():
        result = content_guard(path, row, (configurations | definitions)[path], path in configurations)
        if result and result['timestamp_changed']:
            result['category'] = 'configuration' if path in configurations else 'definition'
            diagnostics.append(result)
    for path, row in previous['installed'].items():
        result = content_guard(path, row, row['sha256'])
        if result and result['timestamp_changed']:
            result['category'] = 'installed'
            diagnostics.append(result)
    require(sha(regular(plan['sfse_path'])) == plan['sfse_sha256'], 'SFSE content changed')
    deployed = regular(plan['deployed_dll'])
    require(sha(deployed) == plan['dll_sha256'], 'Deployed candidate content changed')
    competing = [p.name for p in deployed.parent.glob('Sor*.dll') if p != deployed]
    require(not competing, 'Competing SOR plugin: ' + str(competing))
    return dict(state='PASS_LIGHTWEIGHT', raw_verified=False, save_content_rehashed=False,
                timestamp_policy=POLICY, timestamp_changes=diagnostics,
                transient_names=sorted(current['transient']),
                limits='All guarded configuration, definitions and installed files are content checked, regardless of metadata. Protected save namespaces/sizes use the approved lightweight policy; no full live save scan.')


def archive_hashes(protection):
    return {path: sha(regular(path)) for path in protection['archive_guard']}


def preflight(plan, plan_hash, out):
    adapter_pins(plan)
    value = original.preflight(plan, plan_hash, out)
    value['protection']['archive_content_sha256'] = archive_hashes(value['protection'])
    require(sha(regular(plan['deployed_dll'])) == plan['dll_sha256'], 'Wrong deployed candidate')
    require(not [p.name for p in Path(plan['deployed_dll']).parent.glob('Sor*.dll')
                 if p.resolve() != Path(plan['deployed_dll']).resolve()], 'Competing SOR plugin')
    original.legacy().no_game()
    value.update(timestamp_policy=POLICY, operator_profile='Starfield - SFSE',
                 steam_cloud='CURRENT_OPERATOR_CONFIRMATION_REQUIRED',
                 operator_confirmation_basis='NO_CURRENT_OPERATOR_CONFIRMATION_FROM_OFFLINE_WORK',
                 authority='D5AL_OFFLINE_ONLY_SEPARATE_B_GO_REQUIRED')
    return value


def compare_protection(before, after):
    """Normalize only typed timestamp fields after exact content/size equality."""
    diagnostics = []
    a, b = copy.deepcopy(before), copy.deepcopy(after)
    for label, value in (('before', a), ('after', b)):
        require(set(value['archive_guard']) == set(value['archive_content_sha256']),
                'Archive metadata/content roster mismatch: ' + label)
        for path, row in value['archive_guard'].items():
            require(set(row) == {'bytes', 'mtime_ns'}, 'Unknown archive metadata schema')
        for rows in value['backups'].values():
            for row in rows:
                metadata = row['metadata']
                if metadata is not None:
                    require(row['kind'] == 'LOOSE_BACKUP' and set(metadata) == {'bytes', 'mtime_ns'},
                            'Unknown backup metadata schema')
    require(a['archive_content_sha256'] == b['archive_content_sha256'], 'Archive/index content changed')
    require(set(a['archive_guard']) == set(b['archive_guard']), 'Archive namespace changed')
    for path in a['archive_guard']:
        old, new = a['archive_guard'][path], b['archive_guard'][path]
        require(old['bytes'] == new['bytes'], 'Archive size changed')
        if old['mtime_ns'] != new['mtime_ns']:
            diagnostics.append(dict(category='archive', path=path, before=old['mtime_ns'], after=new['mtime_ns']))
        old.pop('mtime_ns'); new.pop('mtime_ns')
    require(set(a['backups']) == set(b['backups']), 'Backup namespace changed')
    for name in a['backups']:
        require(len(a['backups'][name]) == len(b['backups'][name]), 'Backup roster changed')
        for old, new in zip(a['backups'][name], b['backups'][name]):
            require(old['path'] == new['path'] and old['sha256'] == new['sha256'] and old['kind'] == new['kind'],
                    'Backup identity changed')
            require((old['metadata'] is None) == (new['metadata'] is None), 'Backup metadata kind changed')
            if old['metadata'] is not None:
                require(old['metadata']['bytes'] == new['metadata']['bytes'], 'Backup size changed')
                if old['metadata']['mtime_ns'] != new['metadata']['mtime_ns']:
                    diagnostics.append(dict(category='backup', path=old['path'],
                                            before=old['metadata']['mtime_ns'], after=new['metadata']['mtime_ns']))
                old['metadata'].pop('mtime_ns'); new['metadata'].pop('mtime_ns')
    for group in ('installed', 'file_guards'):
        require(set(a[group]) == set(b[group]), 'Guard roster changed: ' + group)
        for path in a[group]:
            old, new = a[group][path], b[group][path]
            require(old['bytes'] == new['bytes'], 'Guard size changed: ' + path)
            if old['mtime_ns'] != new['mtime_ns']:
                diagnostics.append(dict(category=group, path=path, before=old['mtime_ns'], after=new['mtime_ns']))
            old.pop('mtime_ns'); new.pop('mtime_ns')
        require(a[group] == b[group], 'Guard content identity changed: ' + group)
    result = original.legacy().compare_protection(a, b)
    result.update(timestamp_policy=POLICY, timestamp_changes=diagnostics,
                  archive_content_verified=True, installed_content_equal=True)
    return result


def postflight(plan, before, session, approval, out):
    """Reuse exact frozen finalization/reduction with a private content comparator."""
    adapter_pins(plan)
    original.verify_plan(plan)
    module = original.legacy()
    protection_results = []
    saved_full = module.full

    def full_with_content(path):
        value = saved_full(path)
        value['archive_content_sha256'] = archive_hashes(value)
        return value

    def compare(a, b):
        value = compare_protection(a, b)
        protection_results.append(value)
        return value

    module.full, module.compare_protection = full_with_content, compare
    spec = importlib.util.spec_from_file_location('episode_a_private_postflight', Path(original.__file__))
    private = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(private)
    private.legacy = lambda: module
    value = private.postflight(plan, before, session, approval, out)
    value.update(timestamp_policy=POLICY, protection_comparisons=protection_results)
    return value
