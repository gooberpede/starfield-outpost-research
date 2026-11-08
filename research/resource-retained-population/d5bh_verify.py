# SPDX-License-Identifier: GPL-3.0-or-later
"""Read-only verifier for the D5BH projected witness, using owned D5AJ methods.

CPython 3.14, standard library. Reads only the explicitly supplied ZIP and the
tracked Python modules. A projected event spine is not the original wire.
"""
import argparse
from collections import Counter
import hashlib
import io
import json
from pathlib import Path
import struct
import zipfile
import zlib

import d5aj_reduce as reducer
from d5al_baseline import assess
from d5ai_geometry import normalize
from d5ai_read_geometry import loads_unique
from d5ai_read_lifetime import decode_frames, HEADER, qualify_mark, qualify_snapshot

SCHEMA = 'sor-d5bh-episode-witness/1'
TARGET = '0:37536:20928:0029d20e'
OWNER = 0x5e0de
DLL = '9df5a04ef770887b402dca7c61ee3af52f6046711fcd4e997b66922055bbe67c'
EXE = '7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28'
PREDICTION = 'aa3a5605c3724c042e3d2cd7bc71ca40c23bb46cf8016df6d4112a1b1fe56b80'
NORMALIZED = '0c05d4a4c458b533d1ec7ae3acc8b34698ac48b91ff2965224e5c37ca055da96'
SAVE = '6b4a10084c7e752c31fd2de121a00850aaa2bf1decd700b437d7dccfcdbc82e8'
PROCESSES = {
    'a': (45128, 134381533873950860, '55244e50d337d4e3d594444c8c9c2e52427c0d69462bd4e6aeb46377672ea742'),
    'b': (36876, 134381612033827554, '91a9a5e2ce3e475c1feac6f2ce504e11d7c6d2e347b60f3a147d442c810a000e'),
}
CAPTURES = {
    'a0': ('a', 1, '747947b097c6a22b5e047c036137c24e12a07e16787a965fab76950e4f50809a'),
    'a1': ('a', 2, '2a9a30ef10d806faae689dfeab909d261c12ae508c152415967c6091ab4d5ddf'),
    'b0': ('b', 1, 'a4df584676f114464ce601d46b5c62c1204f131255a51d224384f2ddb5c6f5c2'),
}
COUNTS = {'a': (92109, 13956, 2), 'b': (32101, 5968, 1)}
CORE_PINS = {
    'a': '1c2557dfe19517bd1b4890a4a2ee6776dfc53331f28cb7ef64098dd08d1c4a75',
    'b': 'ab18d52bc704d69ae8c83debdc65d34942765db31e6365cac1c946adf54e6f3d',
}
ARCHIVE_PINS = {
    'a': (37432407, 'fe4bdbcfda8b0689e39444afbef5e9094cd78739787cc4fe2dfc7fd777bd9509',
          '852979e7d960ec0ed1a92c54c5f47a876929623a1219ed16ecc755b6cdb2ac5b', 164),
    'b': (34657445, '7ada51002e4311c6db49001f49e8c34b59aea6698eabbcb37473c67719ac19e5',
          '85eb157a7589a2a8f25268a5eab582bd5ce776d9d4e7aaf4490f097999e0a7fd', 107),
}
PREFIX_PINS = {
    'a0': ('checkpoint-1793680114040295400.json',
           '48c89dacd38718828a16634536c857419ccaca9dbfc4fd31bc1926e488ae9f6a'),
    'b0': ('checkpoint-1793688531891753600.json',
           'c3f7e3dbd19493b7c9d8c742d1d6242569feac066932dc465c94af7e19e59626'),
}
PREFIX_EXTENTS = {
    'a0': (10526176, '56550329c1f311b8c6ea4199a1a48f29f07fa110e851a86e156f5f40b8cf8587'),
    'b0': (10529128, CORE_PINS['b']),
}
SESSION_FILES = ('identity.json', 'ready.json', 'terminal.json', 'flush.jsonl',
                 'lifetimes.bin', 'lifetimes-flush.jsonl')
MEMBERS = {
    'prediction.txt', 'eligibility.json', 'b/geometry-request-1.json',
    *(f'{episode}/{name}' for episode in COUNTS for name in (*SESSION_FILES, 'events.jsonl')),
    *(f'{label}/{name}' for label in CAPTURES for name in
      ('geometry.json', 'original-receipt.json', 'normalized.bin')),
}
CALL = 'invocation parent thread epoch hazards status proc source frame holder a b c d selection request'
FIELDS = {
    4: CALL, 5: CALL + ' descriptor pad_class', 6: CALL + ' descriptor pad_class',
    8: CALL + ' descriptor pad_class',
    10: 'epoch thread status hazards proc a', 11: 'epoch thread status hazards proc a',
    12: 'epoch thread status hazards proc a b',
    14: 'source status hazards d holder a thread epoch selection birth_fields',
    15: 'source status hazards epoch holder thread a selection',
}
SPINE = ('sequence', 'kind', 'ticks')
BIRTH_SLICES = ((0, 4), (0x38, 1), (0x3c, 8), (0x4c, 8), (0x5c, 8), (0x68, 8))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def project_event(event, padding_classes):
    kind = event['kind']
    fields = (*SPINE, *FIELDS.get(kind, '').split())
    result = {key: event[key] for key in fields if key not in ('birth_fields', 'pad_class')}
    if kind == 14:
        data = bytes.fromhex(event['source_bytes'])
        result['birth_fields'] = [data[at:at + size].hex() for at, size in BIRTH_SLICES]
    if 'descriptor' in result:
        data = result['descriptor']
        result['descriptor'] = data[:2] + data[8:]
        result['pad_class'] = padding_classes.setdefault(data[2:8], len(padding_classes))
    return result


def event_rows(lines, count):
    rows = []
    index = 0
    for index, line in enumerate(lines, 1):
        row = loads_unique(line)
        kind = row['kind']
        require(type(kind) is int and 1 <= kind <= 17 and
                set(row) == set(SPINE) | set(FIELDS.get(kind, '').split()) and
                row['sequence'] == index, 'Core spine gap, reorder, kind or field mismatch')
        for key, value in row.items():
            if key not in ('request', 'descriptor', 'birth_fields'):
                require(type(value) is int and 0 <= value < 2 ** 64, 'Invalid core scalar')
        if kind == 14:
            raw = bytearray(112)
            for (at, size), encoded in zip(BIRTH_SLICES, row.pop('birth_fields'), strict=True):
                field = bytes.fromhex(encoded)
                require(len(field) == size, 'Bad constructor field width')
                raw[at:at + size] = field
            row['source_bytes'] = raw.hex()
        if 'request' in row:
            request = row['request']
            require(len(request) == 2 and all(type(n) is int and -(1 << 31) <= n < (1 << 31)
                                              for n in request), 'Invalid request coordinates')
        if 'descriptor' in row:
            data = bytes.fromhex(row['descriptor'])
            require(len(data) == 41 and row['pad_class'] < 2 ** 24, 'Bad consumed descriptor width or pad class')
            # Preserve exact within-process equality without publishing uninitialized bytes.
            row['descriptor'] = (data[:1] + row.pop('pad_class').to_bytes(3, 'little') + data[1:]).hex()
        if kind in FIELDS:
            # Historical generation scans call keys before filtering event kind.
            # Non-call kinds cannot contribute to the four-event join.
            for key in ('invocation', 'selection', 'source'):
                row.setdefault(key, 0)
            rows.append(row)
    require(index == count, 'Core spine record count mismatch')
    return rows


def journal_from_bytes(data, flush, terminal, identity, identity_sha):
    count = terminal['lifetime_flushed']
    header = HEADER.unpack_from(data)
    start, through = (terminal[f'lifetime_qualified_{which}_ticks'] for which in ('from', 'through'))
    crc = zlib.crc32(data)
    require(len(data) == HEADER.size + 112 * count == terminal['lifetime_bytes'] and
            crc == terminal['lifetime_prefix_crc32'] and
            count == terminal['lifetime_written'] == terminal['lifetime_acknowledged'] and
            terminal['lifetime_drops'] == terminal['lifetime_unlogged_cutoff_ticks'] == 0 and
            terminal['lifetime_failed'] is False and
            header[:5] == (0x31464c4941493544, 1, 96, 96, start) and
            header[5] and not header[7] and header[8].hex() == identity_sha,
            'Lifetime terminal, loss or header mismatch')
    decoded = decode_frames(data[HEADER.size:])
    rows = [loads_unique(line) for line in flush.splitlines()]
    matches = [row for row in rows if row['records'] == count and row['qualified_through_ticks'] == through]
    require(matches and all(row == matches[0] for row in matches), 'Missing or ambiguous lifetime flush')
    ack = matches[0]
    require(flush.endswith(b'\n') and ack['schema'] == 'sor-d5ai-lifetime-ack/1' and
            ack['identity_sha256'] == identity_sha and ack['bytes'] == len(data) and
            ack['prefix_crc32'] == crc and ack['qualified_from_ticks'] == start and
            ack['coverage_mark']['ticks'] == through and ack['drops'] == 0 and ack['failed'] is False and
            0 < start <= through and decoded['records'] == count and not decoded['open_intervals'] and
            all(row['ticks'] >= start for row in decoded['events']), 'Invalid lifetime flush provenance')
    qualify_mark(ack['coverage_mark'], decoded['events'], count)
    return dict(schema=identity['lifetime_schema'], session_id=identity_sha, complete=True, loss=0,
                qualified_from_ticks=start, qualified_through_ticks=through,
                raw_prefix_sha256=sha(data), **decoded)


def load_episode(data, episode):
    def get(name):
        return data[f'{episode}/{name}']

    identity_bytes = get('identity.json')
    identity = loads_unique(identity_bytes)
    identity_sha = sha(identity_bytes)
    def terminal_pairs(pairs):
        # Both pinned v0.7.0 terminals repeat this one identical identity key.
        result = {}
        for key, value in pairs:
            require(key not in result or key == 'qpc_frequency' and result[key] == value,
                    'Conflicting or unexpected duplicate terminal key')
            result[key] = value
        return result

    terminal = json.loads(get('terminal.json'), object_pairs_hook=terminal_pairs)
    ready = loads_unique(get('ready.json'))
    reducer.validate_candidate_identity(identity)
    process = reducer.process_certificate(identity)
    require((process['pid'], process['creation_filetime'], identity_sha) == PROCESSES[episode] and
            process['host_sha256'] == EXE and identity['retail'] is True and identity['dll_sha256'] == DLL and
            all(all(receipt.get(k) == v for k, v in identity.items()) for receipt in (terminal, ready)) and
            ready['ready'] is True and ready['hooks'] == 18, 'Wrong native process or producer')
    core_count, lifetime_count, captures = COUNTS[episode]
    loss_keys = ('drops', 'queue_full', 'contention_exhausted', 'reentrant_losses', 'loss_generation',
                 'first_loss_sampled_admission', 'last_loss_sampled_admission')
    require(all(terminal[k] == core_count for k in ('written', 'flushed', 'acknowledged', 'enqueued')) and
            terminal['failed'] is False and terminal['resident_inert'] is True and
            terminal['output_faults'] == 0 and terminal['output_fault'] == 'none' and
            terminal['geometry_completed'] == terminal['geometry_captured'] == captures and
            terminal['geometry_failed'] is False and terminal['geometry_no_slot'] == 0 and
            terminal['lifetime_flushed'] == lifetime_count, 'Wrong terminal accounting')
    flush = get('flush.jsonl')
    previous = 0
    for line in flush.splitlines():
        row = loads_unique(line)
        require(row['identity_sha256'] == identity_sha and previous < row['records'] <= core_count and
                row['bytes'] == row['records'] * 328 and 0 <= row['prefix_crc32'] < 2 ** 32 and
                all(row[key] == 0 for key in loss_keys) and row['loss_bounds_uncertain'] is False,
                'Inconsistent original core flush operands')
        previous = row['records']
    require(flush.endswith(b'\n') and previous == core_count and all(terminal[key] == 0 for key in loss_keys) and
            terminal['loss_bounds_uncertain'] is False, 'Incomplete original core flush accounting')
    journal = journal_from_bytes(get('lifetimes.bin'), get('lifetimes-flush.jsonl'), terminal,
                                 identity, identity_sha)
    events = event_rows(io.BytesIO(get('events.jsonl')), core_count)
    return identity_sha, process, events, journal


def geometry(data, label, episode):
    _, request, original_hash = CAPTURES[label]
    identity_sha, process, events, journal = episode
    snapshot = loads_unique(data[f'{label}/geometry.json'])
    h = snapshot['header']
    receipt = loads_unique(data[f'{label}/original-receipt.json'])
    require(receipt['schema'] == 'sor-d5ai-raw/2' and receipt['identity_sha256'] == identity_sha and
            receipt['sha256'] == original_hash and receipt['bytes'] == h['payload_bytes'] + 456 == 291032 and
            receipt['flushed'] is True and receipt['native_quality'] == 'UNKNOWN' and
            receipt['snapshot_id'] == h['snapshot'] == receipt['request_id'] == h['request'] == request and
            receipt['capture_status'] == h['status'] == 0, 'Wrong original capture receipt')
    require(h['magic'] == 0x3149413544524f53 and h['version'] == 2 and
            h['hazards'] == h['completion_hazards'] == 0 and h['completion_epoch'] == h['epoch'] and
            h['ticks_begin'] < h['ticks_end'] <= h['completion_ticks'] and
            not h['lock_state'] & 0xffc00000 and h['lock_owner'] != h['thread'],
            'Unqualified Raw2 scan boundary')
    holders = snapshot['holders']
    require(len(holders) == h['holders'] == 36 <= h['map_capacity'] and
            len({row['source_pointer'] for row in holders}) == len(holders) and
            len({row['holder_pointer'] for row in holders}) == len(holders), 'Incomplete resident census')
    for holder in holders:
        counts = holder['counts']
        require(0x10000 <= holder['holder_pointer'] < 0x7fffffffffff and
                len(counts) == 3 and all(type(n) is int and n >= 0 for n in counts) and
                counts[0] <= holder['resource_capacity'], 'Malformed holder census')
    require([sum(row['counts'][i] for row in holders) for i in range(3)] ==
            [h[key] for key in ('resources', 'regions', 'points')] == [102, 2984, 7372],
            'Inconsistent Raw2 map census')
    # The reducer resolves every holder through its actual birth/publication.
    # Only the target needs geometry payload. A different selected source fails.
    snapshot['complete_representation'] = True
    envelope, proof = reducer.envelope(snapshot, events, identity_sha, TARGET, OWNER)
    populated = [holder for holder in holders if holder['resources']]
    require(len(populated) == 1 and populated[0]['holder_pointer'] == proof['holder_pointer'] and
            [envelope['capture'][key] for key in ('resource_slots', 'region_total', 'point_total')] ==
            populated[0]['counts'] == [3, 78, 180],
            'Wrong or ambiguous target population')
    proof['lifetime_coverage'] = qualify_snapshot(snapshot, journal)
    proof['process_identity'] = process
    reducer.qualify_construction(proof, journal)
    computed = normalize(envelope)
    require(len(computed) == 5090 and computed == data[f'{label}/normalized.bin'],
            'Complete normalization mismatch')
    return dict(envelope=envelope, proof=proof, raw_sha256=original_hash), computed


def nested_endings(before, after, events, journal, prior):
    ah, bh = before['header'], after['header']
    start, stop = ah['completion_ticks'], bh['ticks_begin']
    interval = sorted((row for row in events if start < row['ticks'] < stop and row['kind'] in (10, 11)),
                      key=lambda row: (row['ticks'], row['sequence']))
    stacks, pairs = {}, []
    epoch, hazards = ah['epoch'], 0
    for end in interval:
        require(not end['status'] and end['a'] in range(7), 'Unknown or exceptional fence')
        stack = stacks.setdefault(end['thread'], [])
        epoch += int(end['kind'] == 10 or end['a'] != 0)
        hazards += 1 if end['kind'] == 10 else -1
        require(end['epoch'] == epoch and end['hazards'] == hazards and hazards >= 0,
                'Inconsistent fence epoch or hazard operands')
        if end['kind'] == 10:
            stack.append(end)
        else:
            require(stack, 'Unpaired fence')
            begin = stack.pop()
            require((begin['proc'], begin['a']) == (end['proc'], end['a']) and
                    begin['ticks'] < end['ticks'], 'Mismatched fence receiver or chronology')
            pairs.append((begin, end))
    reasons = Counter(begin['a'] for begin, _ in pairs)
    require(not any(stacks.values()) and len(pairs) == 196 and
            bh['epoch'] - ah['epoch'] == len(interval) - reasons[0],
            'Unclosed fence or incomplete epoch bridge')
    require(prior['qualified'] and prior['state'] == 'PRIOR_COLLECTION_GEOMETRY_ENDED' and
            len(prior['collections']) == 3, 'Old content survival or uncertainty')
    old = [prior['holder'], *prior['collections']]
    require(all(row['state'] == 'ENDED' and len(row['ending_sequences']) == 1 for row in old),
            'Missing qualified ending for holder or content')
    endings = [(journal['events'][row['ending_sequences'][0] - 1],
                journal['events'][row['ending_end_sequence'] - 1]) for row in old]

    def contains(outer, inner):
        return (outer[0]['thread'] == inner[0]['thread'] and
                outer[0]['ticks'] < inner[0]['ticks'] <= inner[1]['ticks'] < outer[1]['ticks'])

    erase = [pair for pair in pairs if pair[0]['a'] == 2 and pair[0]['proc'] == ah['proc'] + 0x10
             and all(contains(pair, ending) for ending in endings)]
    require(len(erase) == 1 and all(contains(endings[0], end) and
                                    end[0]['parent'] == endings[0][0]['invocation']
                                    for end in endings[1:]), 'Missing unique nested old-content erase')
    enclosing = {reason: [pair for pair in pairs if pair[0]['a'] == reason and contains(pair, erase[0])]
                 for reason in (3, 5, 6)}
    require(all(len(pairs) == 1 for pairs in enclosing.values()) and
            enclosing[3][0][0]['proc'] == before['source']['owning_grid'] and
            enclosing[5][0][0]['proc'] == enclosing[6][0][0]['proc'] == ah['manager'] and
            contains(enclosing[5][0], enclosing[6][0]) and contains(enclosing[6][0], enclosing[3][0]),
            'Missing target Grid/reset/installer nesting')
    require(endings[0][1]['ticks'] < after['source']['birth_ticks'] < after['generation']['ticks'] and
            before['source']['allocation'] != after['source']['allocation'], 'Missing replacement source lifetime')
    later_installers = [pair for pair in pairs if pair[0]['a'] == 5 and
                        erase[0][1]['ticks'] < pair[0]['ticks'] < pair[1]['ticks'] < after['source']['birth_ticks']]
    require(len(later_installers) == 1 and
            later_installers[0][0]['proc'] == bh['manager'] and
            sum(pair[0]['a'] == 6 and pair[0]['proc'] == bh['manager'] and
                contains(later_installers[0], pair) for pair in pairs) == 1,
            'Missing second installer/reset before replacement birth')
    return dict(fence_pairs=len(pairs), epoch_delta=bh['epoch'] - ah['epoch'],
                endings=[[begin['sequence'], end['sequence']] for begin, end in endings],
                erase=[row['sequence'] for row in erase[0]],
                cold=[[row['sequence'], row['status'], row['hazards']] for row in events
                      if row['kind'] == 12 and start < row['ticks'] < stop])


def prediction(data, a0, b0, lineage):
    require(sha(data['prediction.txt']) == PREDICTION, 'Wrong frozen prediction text')
    evidence = loads_unique(data['eligibility.json'])
    for label, observation in (('a0', a0), ('b0', b0)):
        prefix = evidence['prefixes'][label]
        header = observation['proof']['header']
        require(prefix['state'] == 'BASELINE_PREFIX_QUALIFIED' and
                prefix['identity_sha256'] == observation['envelope']['session_id'] and
                prefix['snapshot_id'] == header['snapshot'] == header['request'] == 1 and
                prefix['snapshot_sha256'] == observation['raw_sha256'] and
                prefix['envelope_source'] == observation['envelope']['source'] and
                prefix['envelope_frame'] == observation['envelope']['frame'] and
                (prefix['acknowledged_bytes'], prefix['raw_prefix_sha256']) == PREFIX_EXTENTS[label],
                'Wrong original qualified prefix binding')
    owned = evidence['b0_owned_request']
    record = owned['record']
    request_receipt = loads_unique(data['b/geometry-request-1.json'])
    require(owned['identity_sha256'] == record['identity_sha256'] == request_receipt['identity_sha256'] ==
            b0['envelope']['session_id'] and owned['d5al_arms'] == {'B0': 1} and
            owned['geometry_last_request'] == record['request_id'] == 1 and record['label'] == 'B0' and
            record['owner_class'] == owned['owner_class'] and record['receipt'] == request_receipt and
            data['b/geometry-request-1.json'] == data['b0/original-receipt.json'], 'Wrong owned B0 request binding')
    first, second = evidence['starting_inputs']
    for group, size in (('definitions', 39), ('config', 23), ('installed', 3)):
        require(len(first[group]) == len(second[group]) == size and first[group] == second[group],
                'Frozen starting-input mismatch')
    require(first['save52'] == second['save52'] == {'bytes': 16411136, 'sha256': SAVE} and
            evidence['profile'] == 'Starfield - SFSE' and evidence['steam_cloud'] == 'DISABLED',
            'Save52 or operator profile/Cloud qualification differs')
    post = evidence['postflight']
    require(post['schema'] == 'sor-d5ai-postflight/1' and post['action'] == 'postflight' and
            post['episode'] == 'B' and post['status'] == 'PASS_POSTFLIGHT' and post['process_state'] == 'EXITED' and
            post['protection_errors'] == post['capture_errors'] == [] and
            post['identity_sha256'] == PROCESSES['b'][2] and
            post['plan_sha256'] == '98f3b73f0572f96d9eddce4467368461ebeb920e84dc781f8d6e7d1081093ac2' and
            post['preflight_sha256'] == 'b6737779d19de5bd2dd3571544e7e0fc3f8cd6ef06a944f101063b288dead5b0',
            'Bound B postflight does not qualify')
    freeze = evidence['freeze']
    require(freeze['prediction_id'] == 'D5AI-PRED-01' and freeze['text_version'] == 1 and
            freeze['text_sha256'] == PREDICTION and freeze['phase_b_results_accessed'] is False and
            freeze['utc'] == '2026-11-02T13:22:18.575350+00:00',
            'Wrong original prediction freeze')
    return assess(a0, b0, lineage)


def verify_members(data):
    episodes = {key: load_episode(data, key) for key in COUNTS}
    observations = {label: geometry(data, label, episodes[process])
                    for label, (process, _, _) in CAPTURES.items()}
    (a0, a0_bytes), (a1, a1_bytes), (b0, b0_bytes) = observations.values()
    a_events, a_lifetime = episodes['a'][2:]
    b_events, b_lifetime = episodes['b'][2:]
    first = reducer.relation(a0, a1, a_events, a_events, a_lifetime)
    second = reducer.relation(a0, b0, a_events, b_events, b_lifetime)
    require(first['process_relation'] == 'SAME_PROCESS' and first['relation'] == 'RECONSTRUCTED' and
            second['process_relation'] == 'DISTINCT_PROCESSES' and second['relation'] == 'RECONSTRUCTED',
            'Original paired construction/process relation differs')
    require(sha(a0_bytes) == NORMALIZED and a0_bytes == a1_bytes and a0_bytes == b0_bytes,
            'Original complete byte equality differs')
    endings = nested_endings(a0['proof'], a1['proof'], a_events, a_lifetime, first['prior_storage'])
    forecast = prediction(data, a0, b0, second)
    require(forecast['prediction'] == 'CONFIRMED', 'Original frozen prediction did not confirm')
    return dict(schema=SCHEMA, process_relation=second['process_relation'], lifecycle=endings,
                source_allocations=[v['proof']['source']['allocation'] for v in (a0, a1, b0)],
                generating_sequences=[v['proof']['generation']['generate_sequence'] for v in (a0, a1, b0)],
                normalized_bytes=len(a0_bytes), normalized_sha256=NORMALIZED, prediction=forecast['prediction'],
                scope='Original-data projection and complete paired comparison. Source fidelity uses separate original audit.')


def read_zip(package, expected_sha):
    with package.open('rb') as stream:
        require(hashlib.file_digest(stream, 'sha256').hexdigest() == expected_sha,
                'Candidate SHA-256 mismatch')
        with zipfile.ZipFile(stream) as archive:
            infos = archive.infolist()
            require(len(infos) == len(MEMBERS) + 1 and
                    {row.filename for row in infos} == MEMBERS | {'manifest.json'}, 'Wrong ZIP inventory')
            require(all(not row.is_dir() and not row.flag_bits & 1 and row.compress_type == zipfile.ZIP_DEFLATED
                        and row.external_attr == 0o100644 << 16 for row in infos), 'Unsupported ZIP member')
            manifest = loads_unique(archive.read('manifest.json'))
            require(manifest['schema'] == SCHEMA and set(manifest['members']) == MEMBERS,
                    'Wrong derivative manifest inventory')
            data = {}
            for name, pin in manifest['members'].items():
                require(archive.getinfo(name).file_size == pin['bytes'], 'ZIP member length differs')
                raw = archive.read(name)
                require(sha(raw) == pin['sha256'], 'ZIP member digest differs')
                data[name] = raw
        stream.seek(0)
        require(hashlib.file_digest(stream, 'sha256').hexdigest() == expected_sha,
                'Candidate changed during verification')
    for episode in COUNTS:
        original = manifest['originals'][episode]
        require(tuple(original[key] for key in ('archive_bytes', 'archive_sha256', 'seal_sha256',
                                                'sealed_payloads')) == ARCHIVE_PINS[episode],
                'Original archive identity differs')
        sources = original['members']
        require(sources['raw/events.bin']['sha256'] == CORE_PINS[episode], 'Original core source pin differs')
        for name in SESSION_FILES:
            raw = data[f'{episode}/{name}']
            require(sources[f'raw/{name}'] == {'size': len(raw), 'sha256': sha(raw)},
                    'Exact copied member source mismatch')
    for label, (episode, number, geometry_pin) in CAPTURES.items():
        sources = manifest['originals'][episode]['members']
        require(sources[f'raw/geometry-{number}.bin'] == {'size': 291032, 'sha256': geometry_pin},
                'Original Raw2 pin differs')
        name = ('notes/B0.normalized.bin' if episode == 'b' else
                f'notes/oracle-snapshot-{number}.normalized.bin')
        raw = data[f'{label}/normalized.bin']
        receipt = data[f'{label}/original-receipt.json']
        require(sources[name] == {'size': len(raw), 'sha256': sha(raw)} and
                sources[f'raw/geometry-{number}.json'] == {'size': len(receipt), 'sha256': sha(receipt)},
                'Exact normalized or capture receipt source mismatch')
    for label, (name, pin) in PREFIX_PINS.items():
        require(manifest['originals'][label[0]]['members'][f'notes/receipts/{name}']['sha256'] == pin,
                'Original qualified prefix pin differs')
    request = data['b/geometry-request-1.json']
    require(manifest['originals']['b']['members']['raw/geometry-request-1.json'] ==
            {'size': len(request), 'sha256': sha(request)}, 'Original B0 request receipt differs')
    return data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('candidate', type=Path)
    parser.add_argument('--sha256', required=True)
    args = parser.parse_args()
    try:
        result = verify_members(read_zip(args.candidate, args.sha256))
    except (OSError, ValueError, TypeError, AssertionError, KeyError, IndexError, struct.error,
            zipfile.BadZipFile) as error:
        parser.exit(1, f'D5BH verification failed: {error}\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
