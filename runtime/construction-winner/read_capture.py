# SPDX-License-Identifier: GPL-3.0-or-later
"""Independently authenticate durable prefixes and reduce narrow causal chains.

Reads a stopped/crashed local session and externally pinned DLL hash. Optional
--out creates a new JSON result; never repairs evidence or modifies the target.
CPython stdlib only. CRC detects transport damage; external SHA-256 manifests
bind identity and original capture bytes. Neither mechanism proves semantics.
"""
import argparse
import hashlib
import json
from pathlib import Path
import struct
import zlib

NAMES = 'sequence kind invocation parent thread ticks epoch hazards status proc source frame holder a b c d selection'.split()
KINDS = 'unused entry selected visited lookup descriptor generating sample generated returned fence_begin fence_end cold ready'.split()
SIZE = 312
TARGET = '0:37536:20928:0029d20e'


def decode(raw):
    event = dict(zip(NAMES, struct.unpack_from('<18Q', raw)))
    event['request'] = list(struct.unpack_from('<2i', raw, 144))
    event['source_bytes'] = raw[152:264].hex()
    event['descriptor'] = raw[264:308].hex()
    return event


def source_key(event):
    raw = bytes.fromhex(event['source_bytes'])
    def signed(offset):
        return struct.unpack_from('<i', raw, offset)[0]
    x = signed(0x3c) * 192 + signed(0x4c) * 12 + signed(0x5c)
    y = signed(0x40) * 192 + signed(0x50) * 12 + signed(0x60)
    return f'{raw[0x38]}:{x}:{y}:{struct.unpack_from("<I", raw)[0]:08x}'


def reduce(events):
    """Require the causal prefix through the direct sample; report incomplete tails."""
    certificates, resets, anchors, groups, selections = {}, {}, {}, {}, {}
    first_miss, first_access, geographic = {}, {}, {}
    uncertain_maps, orphan_activity = {}, {}
    diagnostics, chains = [], []
    for e in events:
        k, proc, epoch = e['kind'], e['proc'], e['epoch']
        if k == 10 and e['a'] == 0:
            resets[proc] = e
        if k == 12:
            begin = resets.get(proc)
            if begin and not e['status'] and e['hazards'] == 1 and begin['epoch'] == epoch:
                anchors[proc] = e
        if k == 11 and e['a'] == 0:
            anchor = anchors.pop(proc, None)
            if anchor and not e['status'] and not e['hazards'] and anchor['epoch'] == epoch:
                certificates[(epoch, proc)] = anchor
            resets.pop(proc, None)
        invocation = e['invocation']
        if invocation:
            groups.setdefault(invocation, []).append(e)
        elif k in range(2, 9):
            diagnostics.append(dict(outcome='ORPHAN_BOUNDARY_MISSING_ORIGINAL_REQUEST', boundary=KINDS[k]))
            if k!=4:orphan_activity.setdefault(epoch,[]).append(e['sequence'])
        if k == 2:
            selections[(invocation, e['selection'])] = [e]
        elif e['selection'] and (invocation, e['selection']) in selections:
            selections[(invocation, e['selection'])].append(e)
        if k == 4:
            actual_epoch=e['d']
            first_access.setdefault((actual_epoch, proc, e['c']), e['sequence'])
            if e['a'] == e['b']:
                first_miss.setdefault((actual_epoch, proc, e['c']), e['sequence'])
            if e['status']:
                uncertain_maps.setdefault((actual_epoch,proc),[]).append(e['sequence'])
            if not e['status']:
                geographic.setdefault((epoch, proc, source_key(e)), set()).add(e['source'])
    for invocation, parts in groups.items():
        entry = next((e for e in parts if e['kind'] == 1), None)
        selected = [rows for (ident, _), rows in selections.items() if ident == invocation]
        returned = any(e['kind'] == 9 for e in parts)
        if not selected:
            diagnostics.append(dict(invocation=invocation, outcome='PROVIDER_ONLY_NO_SELECTION_OBSERVED', returned=returned))
        for all_rows in selected:
            samples = [e for e in all_rows if e['kind'] == 7]
            end = samples[0]['sequence'] if samples else all_rows[-1]['sequence']
            rows = [e for e in all_rows if e['sequence'] <= end]
            first = rows[0]
            epoch, proc = first['epoch'], first['proc']
            result = dict(invocation=invocation, selection=first['selection'], source=first['source'],
                          proc=proc, epoch=epoch, request=entry['request'] if entry else None, returned=returned,
                          thread=entry['thread'] if entry else None)
            by_kind = {k: [e for e in rows if e['kind'] == k] for k in range(2, 9)}
            visited, lookup, descriptors, generators = (by_kind[k] for k in (3, 4, 5, 6))
            anchor = certificates.get((epoch, proc))
            relevant = ([entry] if entry else []) + rows
            invalid = [e for e in relevant if e['status'] or e['hazards'] or e['epoch'] != epoch]
            if not entry:
                reason = 'MISSING_ORIGINAL_REQUEST'
            elif invalid:
                reason = 'CONTEXT_OR_LIFETIME_INVALID'
                result.update(first_invalid_boundary=KINDS[invalid[0]['kind']], status=invalid[0]['status'])
            elif any(e['proc'] != proc or e['request'] != entry['request'] or e['thread'] != entry['thread'] or e['parent'] != entry['parent'] for e in relevant):
                reason = 'CONTRADICTORY_INVOCATION_CONTEXT'
            elif any(e['source'] != first['source'] or e['frame'] != first['frame'] for e in rows):
                reason = 'CONTRADICTORY_SELECTION_CONTEXT'
            elif not visited:
                reason = 'SELECTION_ONLY_MISSING_VISITED_BOUNDARY'
            elif len(visited) != 1:
                reason = 'CONTRADICTORY_VISITED_DECISIONS'
            elif visited[0]['a']:
                reason = 'VISITED_BYPASS'
            elif not lookup:
                reason = 'MISSING_MAP_DECISION'
            elif len(lookup) != 1:
                reason = 'CONTRADICTORY_MAP_DECISIONS'
            elif lookup[0]['a'] != lookup[0]['b']:
                reason = 'MAP_HIT'
            elif not descriptors:
                reason = 'MISS_WITHOUT_DESCRIPTOR'
            elif descriptors[0]['d']!=descriptors[0]['holder']+0xc8:
                reason = 'DESCRIPTOR_FRAME_CONTEXT_UNQUALIFIED'
            elif not generators:
                reason = 'MISS_WITHOUT_GENERATOR'
            elif not samples:
                reason = 'MISS_WITHOUT_SAMPLE_PREREQUISITE_UNKNOWN'
            elif len(samples) != 1 or len(generators) != 1 or len(descriptors) != 1:
                reason = 'CONTRADICTORY_SAMPLE_CHAIN'
            elif samples[0]['a'] > 15:
                reason = 'SAMPLE_OUTSIDE_ORDINARY_NIBBLE'
            elif samples[0]['c'] != generators[0]['c']:
                reason = 'CONTRADICTORY_GEOGRAPHIC_POINTER'
            elif not anchor or anchor['sequence'] >= entry['sequence']:
                reason = 'SAMPLE_WITHOUT_QUALIFIED_COLD_STATE'
            elif any(sequence>anchor['sequence'] for sequence in orphan_activity.get(epoch,[])) or any(anchor['sequence']<sequence<lookup[0]['sequence'] for sequence in uncertain_maps.get((epoch,proc),[])):
                reason = 'UNCERTAIN_NATIVE_ACTIVITY_COVERAGE'
            elif first_miss.get((epoch, proc, first['source'])) != lookup[0]['sequence']:
                reason = 'NOT_FIRST_CONSTRUCTING_MISS'
            elif first_access.get((epoch, proc, first['source'])) != lookup[0]['sequence']:
                reason = 'PRIOR_MAP_ACCESS_INVALIDATES_COLD_ATTRIBUTION'
            elif len(geographic.get((epoch, proc, source_key(lookup[0])), ())) > 1:
                reason = 'GEOGRAPHIC_IDENTITY_COLLISION'
            elif not (first['sequence'] < visited[0]['sequence'] < lookup[0]['sequence'] < descriptors[0]['sequence'] < generators[0]['sequence'] < samples[0]['sequence']):
                reason = 'CONTRADICTORY_BOUNDARY_ORDER'
            else:
                reason = 'QUALIFIED_FIRST_CONSTRUCTION_SAMPLE'
                result.update(mask=samples[0]['a'], owner=generators[0]['a'], source_key=source_key(lookup[0]),
                              source_descriptor=lookup[0]['source_bytes'], effective_descriptor=descriptors[0]['descriptor'],
                              cold_sequence=anchor['sequence'], sample_sequence=samples[0]['sequence'])
                result['target_identity'] = result['source_key'] == TARGET and result['owner'] == 0x5e0de
                chains.append(dict(result))
            result['outcome'] = reason
            diagnostics.append(result)
    if not groups:
        diagnostics.append(dict(outcome='NO_PROVIDER_RECORD_COVERAGE_NOT_NATIVE_ABSENCE'))
    return dict(chains=chains, diagnostics=diagnostics)


def inspect(folder, dll_sha256):
    folder = Path(folder)
    identity_bytes = (folder / 'identity.json').read_bytes()
    identity = json.loads(identity_bytes)
    assert identity['schema'] == 'sor-d5x/2' and identity['dll_sha256'] == dll_sha256
    assert len(identity['nonce']) == 64 and len(identity['sites']) == 14
    assert all(ch in '0123456789abcdef' for ch in identity['nonce'])
    assert [site['index'] for site in identity['sites']] == list(range(14))
    origin=identity.get('sequence_origin',0)
    assert isinstance(origin,int) and 0<=origin<2**63
    assert not identity['retail'] or origin==0
    raw = (folder / 'events.bin').read_bytes()
    acknowledgments = (folder / 'flush.jsonl').read_bytes()
    terminal = json.loads((folder / 'terminal.json').read_bytes()) if (folder / 'terminal.json').exists() else None
    ready = json.loads((folder / 'ready.json').read_bytes()) if (folder / 'ready.json').exists() else None
    for receipt in (terminal, ready):
        if receipt:
            assert all(receipt.get(key) == value for key, value in identity.items())
    events = []
    valid_bytes = 0
    damage = []
    for offset in range(0, len(raw), SIZE + 16):
        frame = raw[offset:offset + SIZE + 16]
        if len(frame) != SIZE + 16:
            damage.append('TORN_FRAME')
            break
        magic, size, sequence, crc = struct.unpack_from('<4I', frame)
        payload = frame[16:]
        event = decode(payload)
        expected=origin+len(events)+1
        if magic != 0x31505253 or size != SIZE or sequence != (expected & 0xffffffff) or event['sequence'] != expected or zlib.crc32(payload) != crc:
            damage.append('FRAME_INTEGRITY_OR_SEQUENCE')
            break
        if event['kind'] not in range(1, 14):
            damage.append('UNKNOWN_KIND')
            break
        events.append(event)
        valid_bytes = offset + len(frame)
    durable = 0
    id_hash = hashlib.sha256(identity_bytes).hexdigest()
    for line in acknowledgments.splitlines(keepends=True):
        if not line.endswith(b'\n'):
            damage.append('TORN_ACK')
            break
        try:
            ack = json.loads(line)
            assert ack['identity_sha256'] == id_hash
            assert ack['bytes'] == ack['records'] * (SIZE + 16)
            assert ack['bytes'] <= valid_bytes
            assert zlib.crc32(raw[:ack['bytes']]) == ack['prefix_crc32']
            if terminal and ack['records'] > terminal['acknowledged']:
                continue
            durable = max(durable, ack['records'])
        except (ValueError, AssertionError, KeyError):
            damage.append('ACK_INTEGRITY_OR_PREFIX')
            break
    if ready:
        assert ready['nonce'] == identity['nonce'] and ready['dll_sha256'] == dll_sha256 and ready['hooks'] == 14 and ready['ready'] is True
    result = reduce(events[:durable])
    result.update(schema='sor-d5x-reduction/1', retail=identity['retail'], ready_installed=bool(ready),
                  durable_records=durable, parsed_records=len(events), raw_bytes=len(raw), damage=damage,
                  terminal_success=bool(terminal and not terminal['failed']),
                  complete_session=bool(terminal and not terminal['failed'] and not damage and
                      durable==terminal['flushed']==terminal['written']==terminal['acknowledged'] and
                      terminal['enqueued']==origin+durable and len(raw)==durable*(SIZE+16)),
                  terminal=terminal, identity_sha256=id_hash,
                  raw_sha256=hashlib.sha256(raw).hexdigest(), flush_sha256=hashlib.sha256(acknowledgments).hexdigest(),
                  native_activity_absence_proven=False)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('session', type=Path)
    parser.add_argument('--dll-sha256', required=True)
    parser.add_argument('--out', type=Path)
    args = parser.parse_args()
    result = inspect(args.session, args.dll_sha256)
    text = json.dumps(result, indent=2) + '\n'
    if args.out:
        with args.out.open('x', encoding='utf8', newline='\n') as stream:
            stream.write(text)
    print(text)


if __name__ == '__main__':
    main()
