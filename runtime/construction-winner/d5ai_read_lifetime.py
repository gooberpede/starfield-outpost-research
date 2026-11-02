# SPDX-License-Identifier: GPL-3.0-or-later
"""Authenticate the dedicated D5AI content-ending journal offline.

Reads explicit local files and producer/worker coverage records; never reads
native addresses or contacts a process. Stdlib only. Content-ending events do
not assert outer allocation frees. Native coverage remains a separate premise.
"""
import struct
import zlib
from pathlib import Path
import re

from d5ai_read_geometry import loads_unique, regular_bytes, sha

SCHEMA = 'sor-d5ai-lifetime/1'
EVENT = struct.Struct('<12Q')
FRAME = struct.Struct('<4I')
HEADER = struct.Struct('<8Q32s')
NAMES = ('sequence kind phase invocation parent thread ticks receiver allocation status epoch hazards').split()
KINDS = {1: 'HOLDER_RESOURCE_MAP', 2: 'COLLECTION_GEOMETRY', 3: 'COLLECTION_MUTATION'}
PHASES = {0: 'BEGIN', 1: 'END'}


def validate_identity(identity):
    if (identity.get('lifetime_schema') != SCHEMA or identity.get('lifetime_header_bytes') != 96 or
            identity.get('lifetime_event_bytes') != 96 or identity.get('lifetime_capacity') != 32768):
        raise ValueError('Unsupported dedicated lifetime identity')
    sites = identity.get('lifetime_sites')
    if not isinstance(sites, list) or len(sites) != 3:
        raise ValueError('All typed lifetime observation sites required')
    addresses = []
    for site, kind, adjustment, rva in zip(sites, KINDS.values(), (16, 8, 8), (0x7aab10, 0x7ac260, 0x7ac2f0)):
        if (not isinstance(site, dict) or site.get('kind') != kind or site.get('allocation_adjustment') != adjustment or
                type(site.get('bytes')) is not int or site['bytes'] != 5 or
                type(site.get('va')) is not int or not 0x10000 <= site['va'] < 0x7fffffffffff or
                not isinstance(site.get('guard_sha256'), str) or not re.fullmatch('[0-9a-f]{64}', site['guard_sha256'])):
            raise ValueError('Lifetime site metadata mismatch')
        if identity.get('retail') and site['va'] != identity['module_base'] + rva:
            raise ValueError('Retail lifetime site RVA mismatch')
        addresses.append(site['va'])
    if len(set(addresses)) != 3:
        raise ValueError('Duplicate typed lifetime site')


def natural(value):
    if type(value) is not int or not 0 <= value < 2 ** 64:
        raise ValueError('Invalid lifetime counter')
    return value


def qualify_mark(mark, events, records):
    """Cross-check a quiescent marker against the actual native event prefix.

    Every admitted complete call increments generation twice and emits two
    records. Zero loss and no unlogged calls therefore imply generation==cursor
    at a quiescent marker. Native QPC values must agree with that cursor cut.
    """
    for field in ('cursor', 'ticks', 'generation_before', 'generation_after',
                  'active_before', 'active_after', 'loss', 'failed'):
        natural(mark[field])
    if (mark['cursor'] > records or mark['generation_before'] != mark['generation_after'] or
            mark['generation_before'] != mark['cursor'] or mark['active_before'] or
            mark['active_after'] or mark['loss'] or mark['failed']):
        raise ValueError('Incomplete or contradictory quiescent lifetime marker')
    for event in events:
        if (event['sequence'] <= mark['cursor'] and event['ticks'] > mark['ticks'] or
                event['sequence'] > mark['cursor'] and event['ticks'] < mark['ticks']):
            raise ValueError('Lifetime marker cursor contradicts native event times')


def decode_frames(data):
    """Reject malformed, duplicate, reordered, truncated or corrupted frames."""
    stride = FRAME.size + EVENT.size
    if len(data) % stride:
        raise ValueError('Truncated ending journal frame')
    events, opened, invocations = [], {}, set()
    for position in range(0, len(data), stride):
        magic, size, sequence_low, crc = FRAME.unpack_from(data, position)
        payload = data[position + FRAME.size:position + stride]
        event = dict(zip(NAMES, EVENT.unpack(payload)))
        expected = len(events) + 1
        if (magic != 0x314a4c53 or size != EVENT.size or sequence_low != expected & 0xffffffff or
                event['sequence'] != expected or crc != zlib.crc32(payload)):
            raise ValueError('Ending journal frame integrity/sequence failure')
        kind, phase = event['kind'], event['phase']
        if (kind not in KINDS or phase not in PHASES or not event['thread'] or not event['invocation'] or
                not event['allocation'] or event['status'] not in (0, 16) or (phase == 0 and event['status'] != 0) or
                event['receiver'] != event['allocation'] + (16 if kind == 1 else 8)):
            raise ValueError('Invalid typed ending event')
        key = (event['thread'], event['invocation'])
        if phase == 0:
            if key in invocations:
                raise ValueError('Ending invocation reused')
            invocations.add(key)
            opened[key] = event
        else:
            begin = opened.pop(key, None)
            if (begin is None or any(begin[k] != event[k] for k in
                                    ('kind', 'parent', 'receiver', 'allocation')) or
                    begin['sequence'] >= event['sequence'] or begin['ticks'] > event['ticks']):
                raise ValueError('Unmatched or contradictory ending interval')
        event['kind'], event['phase'] = KINDS[kind], PHASES[phase]
        # Keep the original typed event in the pairing table until its END.
        if phase == 0:
            opened[key] = dict(event, kind=kind, phase=phase)
        events.append(event)
    return dict(events=events, open_intervals=list(opened.values()), records=len(events),
                bytes=len(data), prefix_crc32=zlib.crc32(data), sha256=sha(data))


def read_prefix(session, checkpoint):
    """Read only a durably acknowledged prefix; ignore unacknowledged file tail.

    The caller authenticates its core checkpoint nonce/session/worker or terminal.
    This reader independently binds its lifetime counters to identity, native
    header, CRC-checked frames and a durable producer-safe coverage ledger row.
    """
    session = Path(session).absolute()
    for path in (session, *session.parents):
        if path.is_symlink() or path.is_junction():
            raise ValueError('Reparse lifetime session path')
    if session.resolve() != session:
        raise ValueError('Noncanonical lifetime session path')
    identity_bytes = regular_bytes(session / 'identity.json')
    identity_hash = sha(identity_bytes)
    identity = loads_unique(identity_bytes)
    validate_identity(identity)
    records = natural(checkpoint['lifetime_flushed'])
    size = natural(checkpoint['lifetime_bytes'])
    crc = natural(checkpoint['lifetime_prefix_crc32'])
    first = natural(checkpoint['lifetime_qualified_from_ticks'])
    through = natural(checkpoint['lifetime_qualified_through_ticks'])
    cutoff = natural(checkpoint['lifetime_unlogged_cutoff_ticks'])
    if (any(checkpoint.get(k) != v for k, v in identity.items()) or size != HEADER.size + records * 112 or
            crc > 0xffffffff or checkpoint['lifetime_failed'] is not False or
            natural(checkpoint['lifetime_drops']) != 0 or
            natural(checkpoint['lifetime_acknowledged']) != records):
        raise ValueError('Lifetime checkpoint identity/loss/accounting failure')
    if cutoff and through >= cutoff:
        raise ValueError('Lifetime watermark crosses an unlogged ending boundary')
    matched = []
    for line in regular_bytes(session / 'lifetimes-flush.jsonl').splitlines(keepends=True):
        if not line.endswith(b'\n'):
            if matched:
                break
            raise ValueError('Incomplete acknowledged lifetime ledger')
        row = loads_unique(line)
        if (row.get('records') == records and row.get('qualified_through_ticks') == through and
                row.get('bytes') == size and row.get('prefix_crc32') == crc):
            matched.append(row)
    if not matched or any(row != matched[0] for row in matched):
        raise ValueError('Missing or contradictory lifetime flush witness')
    row = matched[0]
    for field in ('records', 'bytes', 'prefix_crc32'):
        natural(row[field])
    if (row['schema'] != 'sor-d5ai-lifetime-ack/1' or row['identity_sha256'] != identity_hash or
            natural(row['qualified_from_ticks']) != first or natural(row['drops']) or row['failed'] is not False):
        raise ValueError('Invalid lifetime flush provenance')
    mark = row['coverage_mark']
    if (natural(mark['cursor']) > records or natural(mark['ticks']) != through or
            natural(mark['generation_before']) != natural(mark['generation_after']) or
            natural(mark['active_before']) or natural(mark['active_after']) or
            natural(mark['loss']) or natural(mark['failed']) or not first or through < first):
        raise ValueError('No stable quiescent producer-safe coverage mark')
    # Do not follow reparse points or consume bytes written after the ACK.
    raw_path = session / 'lifetimes.bin'
    if raw_path.is_symlink() or raw_path.is_junction() or not raw_path.is_file():
        raise ValueError('Nonregular lifetime evidence')
    with raw_path.open('rb') as stream:
        data = stream.read(size)
    if len(data) != size or zlib.crc32(data) != crc:
        raise ValueError('Lifetime prefix size/CRC failure')
    fields = HEADER.unpack_from(data)
    if (fields[:4] != (0x31464c4941493544, 1, 96, 96) or fields[4] != first or
            not fields[5] or fields[7] or fields[8].hex() != identity_hash):
        raise ValueError('Lifetime header/arming identity mismatch')
    decoded = decode_frames(data[HEADER.size:])
    if decoded['records'] != records:
        raise ValueError('Lifetime record census differs')
    if any(e['ticks'] <= through for e in decoded['open_intervals']):
        raise ValueError('Quiescent watermark contradicts an unfinished interval')
    if any(e['ticks'] < first for e in decoded['events']):
        raise ValueError('Lifetime event precedes journal arming')
    qualify_mark(mark, decoded['events'], records)
    return dict(schema=SCHEMA, session_id=identity_hash, complete=True, loss=0,
                qualified_from_ticks=first, qualified_through_ticks=through,
                coverage_mark=mark, events=decoded['events'], open_intervals=decoded['open_intervals'],
                unlogged_cutoff_ticks=cutoff,
                records=records, prefix_bytes=size, prefix_crc32=crc, raw_prefix_sha256=sha(data),
                flush_row=row, native_header=dict(armed_ticks=fields[4], armed_thread=fields[5], epoch_at_arm=fields[6]))


def qualify_snapshot(snapshot, journal):
    """Bind binary snapshot markers to the authenticated durable journal prefix."""
    header = snapshot['header']
    first, last = header['lifetime_start'], header['lifetime_end']
    for mark in (first, last):
        qualify_mark(mark, journal['events'], journal['records'])
    if (journal['qualified_from_ticks'] > header['ticks_begin'] or
            first['ticks'] > header['ticks_end'] or last['ticks'] < header['completion_ticks'] or
            first['ticks'] > last['ticks'] or first['cursor'] > last['cursor'] or
            journal['qualified_through_ticks'] < last['ticks']):
        raise ValueError('Snapshot lifetime coverage interval/cursor mismatch')
    return dict(qualified=True, from_ticks=journal['qualified_from_ticks'],
                through_ticks=journal['qualified_through_ticks'],
                snapshot_start=first, snapshot_end=last,
                journal_prefix_sha256=journal['raw_prefix_sha256'])
