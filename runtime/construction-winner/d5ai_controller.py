# SPDX-License-Identifier: GPL-3.0-or-later
"""Arm one geometry checkpoint through an admitted, exclusively owned controller.

Uses the owned P4 session/worker/protection controller under SOR-P-0002. Reads
hash-pinned plan/preflight/approval, actual identity/READY/ACK and process-query
handles. Writes only session-local arm/controller state and an exclusive receipt.
No launch, deployment, memory access, game action, unload, save or network write.
The CLI requires a future separately approved plan; D5AI grants no live authority.
"""
import argparse
import json
import os
from pathlib import Path
import secrets

from p4_controller import RetailController, disk_guard, pinned_json, read_json, sha, write_new
from d5ai_read_geometry import loads_unique


def read_json(path):
    return loads_unique(Path(path).read_bytes())


def pinned_json(path, digest):
    data = Path(path).read_bytes()
    if sha(path) != digest:
        raise ValueError('Pinned JSON hash mismatch')
    return loads_unique(data)


def publish_arm(controller, record):
    payload = (controller.identity_hash + '\n' + str(record['request_id'])).encode('ascii')
    path = controller.session / 'geometry-arm.txt'
    if path.exists() and path.read_bytes() == payload:
        return dict(state='GEOMETRY_ARM_PUBLICATION_PENDING', geometry_request=record, raw_verified=False)
    pending = controller.session / ('d5ai-arm-' + secrets.token_hex(16) + '.pending')
    with pending.open('xb') as stream:
        stream.write(payload)
        stream.flush()
        os.fsync(stream.fileno())
    try:
        os.replace(pending, path)
    except PermissionError:
        return dict(state='GEOMETRY_PUBLICATION_PENDING', geometry_request=record,
                    pending=str(pending), raw_verified=False)
    return dict(state='GEOMETRY_ARM_PUBLICATION_PENDING', geometry_request=record, raw_verified=False)


def arm(controller, label):
    """Require a fresh successful challenge before publishing one immutable arm ID."""
    if not controller.lock or not controller.lease or not controller.lease.alive():
        raise ValueError('No exclusive live worker owner')
    if (controller.expected.get('geometry_schema') != 'sor-d5ai-raw/2' or
            len(controller.expected.get('geometry_sites', [])) != 3 or
            controller.expected.get('geometry_header_bytes') != 456 or
            controller.expected.get('context_schema') != 'sor-d5ai-context/1' or
            len(controller.expected.get('context_sites', [])) != 2 or
            controller.expected.get('lifetime_schema') != 'sor-d5ai-lifetime/1' or
            len(controller.expected.get('lifetime_sites', [])) != 3):
        raise ValueError('Candidate has no qualified geometry schema')
    if not isinstance(label, str) or not label or len(label) > 80:
        raise ValueError('Bounded checkpoint label required')
    geometry = controller.state.get('geometry_request')
    if geometry and geometry['state'] in ('ARMED', 'PUBLICATION_PENDING'):
        if geometry['label'] != label:
            raise ValueError('Prior geometry request still pending')
        publish_arm(controller, geometry)
        if controller.state.get('challenge') is None:
            controller.request()
            return dict(state='GEOMETRY_ARM_ACK_PENDING', raw_verified=False)
        health = controller.poll()
        if health['state'] != 'HEALTHY_ACK':
            return dict(state='GEOMETRY_ARM_ACK_PENDING', health=health, raw_verified=False)
        ack = health['ack']
        if (ack.get('geometry_failed') is not False or ack.get('lifetime_failed') is not False or
                ack.get('lifetime_unlogged_cutoff_ticks') != 0):
            raise ValueError('Geometry worker failed')
        if ack.get('geometry_armed') == geometry['request_id']:
            geometry['state'] = 'ARMED'
            geometry['arm_ack'] = ack
            controller.save()
            return dict(state='GEOMETRY_ARMED', geometry_request=geometry, raw_verified=False)
        if (controller.session / f"geometry-request-{geometry['request_id']}.json").exists():
            result = poll_geometry(controller)
            result['state'] = 'GEOMETRY_CAPTURED_BEFORE_ARM_ACK'
            return result
        return dict(state='GEOMETRY_ARM_ACK_PENDING', ack=ack, raw_verified=False)
    if controller.state.get('challenge') is None:
        controller.request()
        return dict(state='GEOMETRY_CHALLENGE_PENDING', raw_verified=False)
    health = controller.poll()
    if health['state'] != 'HEALTHY_ACK':
        return dict(state='GEOMETRY_CHALLENGE_PENDING', health=health, raw_verified=False)
    ack = health['ack']
    if (ack.get('geometry_failed') is not False or ack.get('geometry_armed') != 0 or
            ack.get('lifetime_failed') is not False or ack.get('lifetime_unlogged_cutoff_ticks') != 0):
        raise ValueError('Geometry worker is failed or already armed')
    previous = controller.state.get('geometry_last_request', 0)
    request = previous + 1
    if request >= 2 ** 64:
        raise ValueError('Geometry request counter exhausted')
    record = dict(request_id=request, label=label, state='PUBLICATION_PENDING', identity_sha256=controller.identity_hash,
                  owner=controller.state['owner'])
    controller.state['geometry_last_request'] = request
    controller.state['geometry_request'] = record
    controller.save()
    return publish_arm(controller, record)


def poll_geometry(controller):
    record = controller.state.get('geometry_request')
    if not record:
        return dict(state='GEOMETRY_NOT_ARMED', raw_verified=False)
    path = controller.session / f"geometry-request-{record['request_id']}.json"
    if not path.exists():
        return dict(state='GEOMETRY_BOUNDARY_PENDING', geometry_request=record, raw_verified=False)
    receipt = read_json(path)
    if (receipt.get('identity_sha256') != controller.identity_hash or
            receipt.get('request_id') != record['request_id'] or receipt.get('flushed') is not True or
            receipt.get('schema') != 'sor-d5ai-raw/2'):
        raise ValueError('Geometry acknowledgment identity mismatch')
    record['state'] = 'CAPTURE_RECEIPT_UNVERIFIED'
    record['receipt'] = receipt
    controller.save()
    return dict(state='GEOMETRY_CAPTURE_RECEIPT', geometry_request=record, raw_verified=False)


def validate_geometry_plan(expected, plan):
    if (expected.get('geometry_schema') != plan.get('geometry_schema') or
            expected.get('geometry_schema') != 'sor-d5ai-raw/2' or
            expected.get('geometry_header_bytes') != 456):
        raise ValueError('Geometry plan schema mismatch')
    observed, pinned = expected.get('geometry_sites', []), plan.get('geometry_sites', [])
    if len(observed) != 3 or len(pinned) != 3:
        raise ValueError('All three geometry sites must be pinned')
    for actual, reference, (rva, size) in zip(observed, pinned, ((0x21e09ed, 5), (0x21e0aa5, 5), (0x21e0a7e, 9))):
        if (actual['va'] != expected['module_base'] + reference['rva'] or
                reference['rva'] != rva or reference['bytes'] != size or
                actual['bytes'] != reference['bytes'] or
                actual['preimage_sha256'] != reference['preimage_sha256']):
            raise ValueError('Geometry site identity mismatch')
    if expected.get('context_schema') != 'sor-d5ai-context/1' or plan.get('context_schema') != 'sor-d5ai-context/1':
        raise ValueError('Whole-context invalidation schema required')
    observed, pinned = expected.get('context_sites', []), plan.get('context_sites', [])
    if len(observed) != 2 or len(pinned) != 2:
        raise ValueError('Both whole-context invalidators must be pinned')
    for actual, reference, (rva, reason) in zip(observed, pinned, ((0x789ce0, 5), (0x788e70, 6))):
        if (actual['va'] != expected['module_base'] + reference['rva'] or actual['bytes'] != 5 or
                reference['rva'] != rva or reference['bytes'] != 5 or reference['reason'] != reason or actual['reason'] != reason or
                actual['guard_sha256'] != reference['guard_sha256']):
            raise ValueError('Whole-context site identity mismatch')


    if expected.get('lifetime_schema') != 'sor-d5ai-lifetime/1' or plan.get('lifetime_schema') != 'sor-d5ai-lifetime/1':
        raise ValueError('Baseline lifetime journal required')
    from d5ai_read_lifetime import validate_identity
    validate_identity(expected)
    observed, pinned = expected.get('lifetime_sites', []), plan.get('lifetime_sites', [])
    if len(pinned) != 3:
        raise ValueError('All three baseline ending/mutation sites must be pinned')
    for actual, reference, (rva, kind, adjustment) in zip(observed, pinned, (
            (0x7aab10, 'HOLDER_RESOURCE_MAP', 16), (0x7ac260, 'COLLECTION_GEOMETRY', 8),
            (0x7ac2f0, 'COLLECTION_MUTATION', 8))):
        if (actual['va'] != expected['module_base'] + reference['rva'] or reference['rva'] != rva or
                reference['bytes'] != 5 or reference['kind'] != kind or
                reference['allocation_adjustment'] != adjustment or actual['guard_sha256'] != reference['guard_sha256']):
            raise ValueError('Lifetime site identity mismatch')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['arm', 'poll'])
    parser.add_argument('--session', required=True, type=Path)
    for name in ('plan', 'preflight', 'approval'):
        parser.add_argument('--' + name, required=True, type=Path)
        parser.add_argument('--' + name + '-sha256', required=True)
    parser.add_argument('--label', required=True)
    parser.add_argument('--out', required=True, type=Path)
    args = parser.parse_args()
    plan = pinned_json(args.plan, args.plan_sha256)
    plan['plan_sha256'] = args.plan_sha256
    preflight = pinned_json(args.preflight, args.preflight_sha256)
    preflight['receipt_sha256'] = args.preflight_sha256
    approval = pinned_json(args.approval, args.approval_sha256)
    required = {'d5ai_read_lifetime.py', 'p4_controller.py', 'controller.py', 'worker_health.py', 'read_capture.py',
                'reduce_v3.py', 'reduce_v4.py', 'd5ai_controller.py', 'd5ai_read_geometry.py'}
    pins = plan.get('controller_pins', {})
    if {Path(p).name for p in pins} != required:
        raise ValueError('Exact lifecycle and geometry controller pins required')
    for p, expected in pins.items():
        if Path(p).resolve() != Path(__file__).parent / Path(p).name or sha(p) != expected:
            raise ValueError('Controller source identity mismatch')
    disk_guard()
    expected = read_json(args.session / 'identity.json')
    validate_geometry_plan(expected, plan)
    controller = RetailController(args.session, expected, plan, preflight, approval, 'request')
    try:
        result = arm(controller, args.label) if args.action == 'arm' else poll_geometry(controller)
        result.update(identity_sha256=controller.identity_hash, owner=controller.state['owner'])
        write_new(args.out, result)
    finally:
        controller.close()


if __name__ == '__main__':
    main()
