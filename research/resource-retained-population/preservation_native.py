# SPDX-License-Identifier: GPL-3.0-or-later
"""Offline D5L preservation comparison and operational source amendment binding.

Reads completed pre/post receipts and immutable native build snapshots; writes
one fresh ignored comparison JSON. No target, original, archive or Git mutation.
Stdlib and maintainer-owned save helpers only. No full preservation audit here.
"""
import argparse
import json
from pathlib import Path
import sys
from build import ROOT, LOCAL, pin

sys.path.insert(0, str(ROOT/'research/resource-carinae-source-context'))
from protection import sync_equal
from save_policy import compare, policy_hash

PREFLIGHT_SCHEMA = 'sor-d5l-preflight/2'
OPERATIONAL = {str(ROOT/'research/resource-retained-population'/name)
               for name in ('prepare_native.py', 'collect_native.py', 'check_admission.py')}


def verify_build_files(manifest):
    """Retain native/tool pins; bind three amended Python files separately.

    The original build manifest also pins operational Python which is not
    compiled into the controller. Authenticate its preserved source snapshots
    and record current hashes only for this explicit three-file amendment.
    Every other build input/output remains exact; no native exception exists.
    """
    amended = {}
    for name, expected in manifest['files'].items():
        actual = pin(name)
        if actual == expected:
            continue
        assert name in OPERATIONAL, ('Unapproved build input change', name)
        snapshot = manifest['source_snapshots'][name]
        assert snapshot['sha256'] == expected and pin(snapshot['path']) == expected
        amended[name] = dict(build_source_sha256=expected, current_sha256=actual,
                             build_source_snapshot=snapshot['path'])
    return amended


def postflight_comparison(before, after):
    """Compare full scientific hashes after exit; sync metadata never gates."""
    assert before['schema'] == after['schema'] == PREFLIGHT_SCHEMA
    assert before['status'] == after['status'] == 'OFFLINE_CHECKED_NOT_AUTHORIZED'
    policy = before['save_policy']
    assert before['save_policy_sha256'] == after['save_policy_sha256'] == policy_hash(policy)
    assert after['save_policy'] == policy
    fields = ('source', 'live_path', 'save52', 'definitions', 'config', 'installed',
              'backups', 'archive_guard', 'restore_rehearsal_sha256', 'code_pins',
              'operational_sources', 'build_manifest', 'qualification', 'run_card')
    checks = {field: before[field] == after[field] for field in fields}
    checks['protected_live'] = compare(before['protected_live'], after['protected_live'], policy)['ok']
    checks['protected_remote'] = sync_equal(before['sync'], after['sync'], policy)
    return dict(schema='sor-d5l-postflight/1', checks=checks, ok=all(checks.values()),
                remotecache_diagnostic=dict(before=before['sync'].get('remotecache_sha256'),
                    after=after['sync'].get('remotecache_sha256'), protected=False))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('preflight', 'postflight', 'output'):
        parser.add_argument('--'+name, type=Path, required=True)
    args = parser.parse_args()
    assert all(p.resolve().is_relative_to(LOCAL) for p in (args.preflight, args.postflight, args.output))
    result = postflight_comparison(json.loads(args.preflight.read_text(encoding='utf8')),
                                  json.loads(args.postflight.read_text(encoding='utf8')))
    result['receipts'] = {str(p.resolve()): pin(p) for p in (args.preflight, args.postflight)}
    with args.output.open('x', encoding='utf8', newline='\n') as stream:
        json.dump(result, stream, indent=2)
        stream.write('\n')
    assert result['ok'], result
    print('D5L protected-input postflight PASS; synchronization metadata is diagnostic')


if __name__ == '__main__':
    main()
