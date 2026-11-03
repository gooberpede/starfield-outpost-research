# SPDX-License-Identifier: GPL-3.0-or-later
"""D5AJ versioned prefix qualification; SOR-P-0002 adaptation of d5ai_checkpoint.py.

Authenticate a completed snapshot against an explicitly acknowledged prefix.

Offline qualification and prospective read-only checkpoint helper. Reads an
explicit session, challenge ACK, flush ledger and exactly that durable raw prefix;
writes one exclusive local report. Never contacts a process, writes controller
commands, opens saves/Ghidra, changes Git or uses network. Fresh live worker and
operator authority remain separate controller/run-card gates. Does not require
terminal finalization or claim whole-session completeness/firstness. Stdlib only.
"""
import sys
if not __debug__ or sys.flags.optimize:
    raise RuntimeError('Use Python -E -B')

import argparse
import hashlib
import json
from pathlib import Path
import re
import struct
import zlib

from d5ae_baseline import guard
import d5aj_reduce as reducer


def verify_source_lock(path, expected_hash, dll_hash):
    data = Path(path).read_bytes()
    if hashlib.sha256(data).hexdigest() != expected_hash:
        raise ValueError('Source-lock manifest identity mismatch')
    manifest = reducer.load(path)
    required = {Path(__file__).resolve(), Path(reducer.__file__).resolve(),
                Path(reducer.__file__).with_name('d5aj_scope.py').resolve(),
                Path(reducer.__file__).with_name('d5ai_geometry.py').resolve(),
                Path(reducer.__file__).with_name('d5ai_lifetime.py').resolve(),
                Path(reducer.__file__).with_name('d5ae_baseline.py').resolve(),
                *(reducer.ROOT / 'runtime/construction-winner' / n for n in
                  ('read_capture.py', 'reduce_v3.py', 'reduce_v4.py', 'd5ai_read_geometry.py', 'd5ai_read_lifetime.py'))}
    if (manifest['schema'] != 'sor-d5aj-source-lock/1' or manifest['dll_sha256'] != dll_hash or
            Path(manifest['repository_root']).resolve() != reducer.ROOT or
            len(manifest['sources']) != len(required) or
            {Path(p).resolve() for p in manifest['sources']} != required or
            hashlib.sha256(Path(sys.executable).read_bytes()).hexdigest() != manifest['interpreter_sha256']):
        raise ValueError('Source-lock closure, producer or interpreter mismatch')
    for name, expected in manifest['sources'].items():
        if hashlib.sha256(Path(name).read_bytes()).hexdigest() != expected:
            raise ValueError('Checkpoint source changed: ' + name)
    return manifest


def load_ack(path):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                # Historical schema-4 identity and metrics both emitted this
                # immutable frequency. Preserve only identical legacy values.
                if key != 'qpc_frequency' or result[key] != value:
                    raise ValueError('Duplicate or contradictory ACK key')
            result[key] = value
        return result
    return json.loads(Path(path).read_bytes(), object_pairs_hook=unique)


def inspect_prefix(session, dll_hash, snapshot_id, nonce, target, owner):
    session = Path(session).absolute()
    for ancestor in (session, *session.parents):
        if ancestor.is_symlink() or ancestor.is_junction():
            raise ValueError('Reparse session path')
    if not re.fullmatch('[0-9a-f]{32}', nonce):
        raise ValueError('Exact challenge nonce required')
    for path in (session / 'identity.json', session / ('ack-' + nonce + '.json'),
                 session / 'flush.jsonl', session / 'events.bin',
                 session / f'geometry-{snapshot_id}.bin', session / f'geometry-{snapshot_id}.json'):
        if path.is_symlink() or path.is_junction() or not path.is_file():
            raise ValueError('Nonregular checkpoint evidence file')
    identity_bytes = (session / 'identity.json').read_bytes()
    identity = reducer.load(session / 'identity.json')
    reducer.validate_candidate_identity(identity)
    digest = hashlib.sha256(identity_bytes).hexdigest()
    if identity['schema'] != 'sor-d5x/4' or identity['dll_sha256'] != dll_hash:
        raise ValueError('Wrong lifecycle producer identity')
    ack_path = session / ('ack-' + nonce + '.json')
    ack = load_ack(ack_path)
    for field in ('flushed', 'acknowledged', 'drops', 'loss_generation', 'output_faults',
                  'geometry_completed', 'geometry_no_slot', 'qpc_frequency'):
        if type(ack[field]) is not int or not 0 <= ack[field] < 2 ** 64:
            raise ValueError('Malformed ACK integer')
    if (any(ack.get(k) != v for k, v in identity.items()) or ack['request_nonce'] != nonce or
            ack['hooks_intact'] is not True or ack['capture_active'] is not True or
            ack['counter_overflow'] is not False or ack['output_faults'] != 0 or ack['output_fault'] != 'none' or
            ack['drops'] != 0 or ack['loss_generation'] != 0 or ack['loss_bounds_uncertain'] is not False or
            ack['geometry_failed'] is not False or ack['geometry_no_slot'] != 0 or
            ack['geometry_completed'] < snapshot_id):
        raise ValueError('Challenge does not acknowledge a healthy completed snapshot')
    records = ack['flushed']
    if type(records) is not int or records <= 0 or ack['acknowledged'] != records:
        raise ValueError('Malformed durable prefix count')
    prefixes = []
    with (session / 'flush.jsonl').open('rb') as stream:
        for line in stream:
            if not line.endswith(b'\n'):
                break
            row = reducer.d5ai_read_geometry.loads_unique(line)
            if row['records'] == records:
                prefixes.append(row)
    if len(prefixes) != 1:
        raise ValueError('No unique matching durable flush prefix')
    prefix = prefixes[0]
    for field in ('records', 'bytes', 'drops', 'prefix_crc32'):
        if type(prefix[field]) is not int or not 0 <= prefix[field] < 2 ** 64:
            raise ValueError('Malformed flush-prefix integer')
    if prefix['identity_sha256'] != digest or prefix['bytes'] != records * 328 or prefix['drops'] != 0:
        raise ValueError('Flush ledger identity/length/loss mismatch')
    raw_path = session / f'geometry-{snapshot_id}.bin'
    receipt_path = session / f'geometry-{snapshot_id}.json'
    data = raw_path.read_bytes()
    receipt = reducer.load(receipt_path)
    snapshot = reducer.d5ai_read_geometry.decode(data)
    h = snapshot['header']
    if (receipt['schema'] != 'sor-d5ai-raw/2' or receipt['identity_sha256'] != digest or
            receipt['snapshot_id'] != snapshot_id or h['snapshot'] != snapshot_id or
            receipt['request_id'] != h['request'] or receipt['capture_status'] != h['status'] or
            receipt['sha256'] != hashlib.sha256(data).hexdigest() or receipt['bytes'] != len(data) or
            receipt['flushed'] is not True or receipt['native_quality'] != 'UNKNOWN'):
        raise ValueError('Snapshot is absent, contradictory or not fully flushed')
    snapshot['sha256'] = hashlib.sha256(data).hexdigest()
    if not snapshot['complete_representation']:
        raise ValueError('Snapshot consumer boundary did not qualify')
    sources = {h['source_pointer'] for h in snapshot['holders']}
    events, crc, raw_sha = [], 0, hashlib.sha256()
    origin = identity.get('sequence_origin', 0)
    with (session / 'events.bin').open('rb') as stream:
        for ordinal in range(records):
            raw = stream.read(328)
            if len(raw) != 328:
                raise ValueError('Acknowledged raw prefix is truncated')
            magic, size, sequence, checksum = struct.unpack_from('<4I', raw)
            event = reducer.read_capture.decode(raw[16:])
            expected = origin + ordinal + 1
            if (magic != 0x31505253 or size != 312 or sequence != (expected & 0xffffffff) or
                    event['sequence'] != expected or zlib.crc32(raw[16:]) != checksum or
                    event['kind'] not in range(1, 18)):
                raise ValueError('Durable native frame failed authentication')
            crc = zlib.crc32(raw, crc)
            raw_sha.update(raw)
            # Keep every admitted event through completion, including other
            # allocations and adverse histories. No scientific event quota.
            if event['ticks'] <= snapshot['header']['completion_ticks']:
                events.append(event)
    if crc != prefix['prefix_crc32']:
        raise ValueError('Durable raw prefix CRC mismatch')
    value, proof = reducer.envelope(snapshot, events, digest, target, owner)
    lifetime = reducer.d5ai_read_lifetime.read_prefix(session, ack)
    proof['lifetime_coverage'] = reducer.d5ai_read_lifetime.qualify_snapshot(snapshot, lifetime)
    proof['process_identity'] = reducer.process_certificate(identity)
    reducer.qualify_construction(proof, lifetime)
    present = value['availability']['exposed']
    return dict(method=reducer.METHOD, state='BASELINE_PREFIX_QUALIFIED' if present else 'BASELINE_UNAVAILABLE',
                identity_sha256=digest, snapshot_id=snapshot_id, request_nonce=nonce,
                acknowledged_records=records, acknowledged_bytes=records * 328,
                raw_prefix_sha256=raw_sha.hexdigest(), ack_sha256=hashlib.sha256(ack_path.read_bytes()).hexdigest(),
                snapshot_sha256=snapshot['sha256'], envelope=value, proof=proof,
                lifetime=lifetime,
                complete_session=False, scientific_firstness_qualified=False,
                live_worker_verified=False, permission_to_depart=False,
                scope='Authenticated completed geometry boundary in this durable prefix only; fresh controller health and separate live approval still required')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('session', type=Path)
    parser.add_argument('--dll-sha256', required=True)
    parser.add_argument('--snapshot', type=int, required=True)
    parser.add_argument('--nonce', required=True)
    parser.add_argument('--target', default=reducer.read_capture.TARGET)
    parser.add_argument('--owner-formid', default='0005e0de')
    parser.add_argument('--source-lock', type=Path, required=True)
    parser.add_argument('--source-lock-sha256', required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    manifest = verify_source_lock(args.source_lock, args.source_lock_sha256, args.dll_sha256)
    if not args.out.resolve().is_relative_to(Path(manifest['repository_root']) / '.local-work/d5aj'):
        raise ValueError('Task-local checkpoint receipt required')
    guard()
    result = inspect_prefix(args.session, args.dll_sha256, args.snapshot, args.nonce, args.target, int(args.owner_formid, 16))
    result['method_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    with args.out.open('x', encoding='utf8', newline='\n') as stream:
        stream.write(json.dumps(result, indent=2) + '\n')
    print(result['state'])


if __name__ == '__main__':
    main()
