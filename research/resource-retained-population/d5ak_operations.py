# SPDX-License-Identifier: GPL-3.0-or-later
"""Source-locked D5AK guards, reusing owned D5AI content protection (SOR-P-0002).

Reads prospective plan, source lock, protected contents and session evidence.
Writes fresh ignored pre/postflight receipts and inherited restoration COPIES.
No deployment, launch, game action, original-save write, attachment or network.
All safety-sensitive imports follow an optimization refusal. Historical helpers
and their assertions remain frozen and are only imported without optimization.
"""
import sys
if not __debug__ or sys.flags.optimize:
    raise RuntimeError('Use the pinned Python interpreter with -E -B; optimization is forbidden')

import argparse
import json
from pathlib import Path

import d5ai_a_operations as content
import d5ai_operations as original
import d5aj_checkpoint as checkpoint
from d5ai_episode import ROOT, require, sha
from common import fresh, guard, regular

POLICY = 'sor-d5ak-operational-lock/1'


def required_sources():
    """Exact owned operational and analysis closure, excluding stdlib modules."""
    research = Path(__file__).parent
    names = ('d5ak_episode.py', 'd5ak_operations.py', 'd5ak_bundle.py', 'd5ai_episode.py',
             'd5ai_a_episode.py', 'd5ai_a_operations.py', 'd5ai_operations.py',
             'd5ab_p4_operations.py', 'd5aj_checkpoint.py', 'd5aj_reduce.py',
             'd5aj_scope.py', 'd5ai_geometry.py', 'd5ai_lifetime.py', 'd5ae_baseline.py')
    runtime = ROOT / 'runtime/construction-winner'
    dynamic = (
        'research/resource-retained-population/build.py',
        'research/resource-retained-population/native_reduce.py',
        'research/resource-retained-population/prepare_native.py',
        'research/resource-retained-population/preservation_native.py',
        'research/resource-retained-population/qualify.py',
        'research/resource-retained-population/reduce.py',
        'research/resource-retained-population/reliability_contract.py',
        'research/resource-retained-population/verify_native.py',
        'research/resource-oracle-retail/collect.py',
        'research/resource-query-reachability/audit.py',
        'research/resource-query-reachability/remaining_inputs.py',
        'research/resource-carinae-source-context/protection.py',
        'research/resources-evidence-consolidation/cutover.py',
        'research/resources-evidence-consolidation/discover.py',
        'research/resources-evidence-consolidation/prepare.py',
        'research/resources-evidence-consolidation/resources_preservation.py',
        'research/evidence-access/access.py',
        'research/evidence-access/executor.py',
        'research/evidence-access/retirement.py',
        'research/evidence-archive-discovery/archive.py',
        'research/evidence-archive-discovery/inventory.py',
        'research/evidence-archive-discovery/scope.py',
        'research/evidence-archive-stage-b/engine.py',
        'runtime/session-tools/session.py',
        'runtime/session-tools/archive.py',
        'runtime/session-tools/adapter070.py',
    )
    return ({(research / name).resolve() for name in names} |
            {ROOT / name for name in dynamic} |
            {(runtime / name).resolve() for name in
             ('p4_controller.py', 'controller.py', 'worker_health.py', 'read_capture.py',
              'reduce_v3.py', 'reduce_v4.py', 'd5ai_controller.py',
              'd5ai_read_geometry.py', 'd5ai_read_lifetime.py')} |
            {ROOT / 'runtime/session-tools/common.py',
             ROOT / 'research/resource-carinae-source-context/save_policy.py',
             ROOT / 'research/resource-carinae-source-context/save_policy.json'})


def source_pins(plan):
    """Verify both the integrated closure and unchanged versioned D5AJ closure."""
    require(plan.get('episode') == 'A', 'D5AK supports only Episode A')
    manifest = original.pinned_json(plan['d5ak_source_lock'], plan['d5ak_source_lock_sha256'])
    require(manifest.get('schema') == POLICY, 'D5AK operational source lock required')
    require(Path(manifest['interpreter']).resolve() == Path(sys.executable).resolve() and
            sha(sys.executable) == manifest['interpreter_sha256'], 'Pinned interpreter identity mismatch')
    pins = manifest['sources']
    expected = required_sources() | {Path(p).resolve() for p in plan['package_pins']}
    require(len(pins) == len(expected) and
            {Path(p).resolve() for p in pins} == expected, 'Exact D5AK source closure required')
    for path, digest in pins.items():
        require(sha(regular(path)) == digest, 'D5AK source changed: ' + path)
    require(manifest['dll_sha256'] == plan['dll_sha256'], 'D5AK producer identity mismatch')
    checkpoint.verify_source_lock(plan['d5aj_source_lock'], plan['d5aj_source_lock_sha256'], plan['dll_sha256'])
    return manifest


def verify_plan(plan):
    source_pins(plan)
    content.adapter_pins(plan)
    original.verify_plan(plan)


def lightweight(plan, preflight):
    source_pins(plan)
    return content.lightweight(plan, preflight)


def preflight(plan, plan_hash, out):
    verify_plan(plan)
    # The full preservation audit precedes operator deployment. The lightweight
    # controller admission separately verifies the deployed DLL after install.
    value = original.preflight(plan, plan_hash, out)
    value['protection']['archive_content_sha256'] = content.archive_hashes(value['protection'])
    # Operator configuration reports from the consumed episode are historical,
    # never a new confirmation of a prospective operator's setup.
    for field in ('steam_cloud', 'operator_confirmation_basis'):
        value.pop(field, None)
    value.update(authority='D5AK_OFFLINE_PREFLIGHT_ONLY_SEPARATE_GO_REQUIRED',
                 d5ak_source_lock_sha256=plan['d5ak_source_lock_sha256'],
                 d5aj_source_lock_sha256=plan['d5aj_source_lock_sha256'])
    return value


def postflight(plan, before, session, approval, out):
    verify_plan(plan)
    return content.postflight(plan, before, session, approval, out)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('preflight', 'postflight'))
    for name in ('plan', 'preflight', 'approval'):
        parser.add_argument('--' + name, type=Path, required=name == 'plan')
        parser.add_argument('--' + name + '-sha256', required=name == 'plan')
    parser.add_argument('--session', type=Path)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    out = args.out.resolve()
    require(out.is_relative_to(ROOT / '.local-work/d5ak'), 'Fresh D5AK output required')
    guard()
    out.mkdir(parents=True, exist_ok=False)
    try:
        plan = original.pinned_json(args.plan, args.plan_sha256)
        plan['plan_sha256'] = args.plan_sha256
        if args.action == 'preflight':
            value = preflight(plan, args.plan_sha256, out)
        else:
            before = original.pinned_json(args.preflight, args.preflight_sha256)
            before['receipt_sha256'] = args.preflight_sha256
            require(before['plan_sha256'] == args.plan_sha256, 'Preflight plan mismatch')
            value = postflight(plan, before, args.session,
                               original.pinned_json(args.approval, args.approval_sha256), out)
    except BaseException as error:
        fresh(out / 'receipt.json', dict(state='CHECK_ERROR', action=args.action, error=repr(error)))
        raise
    fresh(out / 'receipt.json', value)
    print(json.dumps(dict(state=value.get('state', value.get('status')), out=str(out))))


if __name__ == '__main__':
    main()
