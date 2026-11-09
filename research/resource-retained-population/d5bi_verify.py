# SPDX-License-Identifier: GPL-3.0-or-later
"""Read the exact D5BI ZIP and recompute its projected N2 event relationships.

Only the caller-supplied ZIP, tracked manifest and tracked Python methods are
read. Standard library, no extraction, target, network or private inputs.
"""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
import os
from pathlib import Path
import struct
import sys
import zipfile

if not __debug__ or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):
    raise RuntimeError('Use Python -E -B without optimization')

import d5aj_reduce as source
from d5ap_analyze import extract, require, triples
from d5ap_native_controls import exhaustive_operands, transition
from d5ap_windows import HistoryIndex
from d5bh_verify import BIRTH_SLICES
from d5s_controls import registration
from d5ai_read_lifetime import qualify_mark, qualify_snapshot
from d5am_read_scheduler import NAMES as SCHEDULER_FIELDS
from d5an_read_causal import NAMES as CAUSAL_FIELDS
import read_capture as core_reader

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / 'docs/audits/evidence-derivative-d5bi/manifest.json'
SCHEMA = 'sor-d5bi-n2-projection/1'
IDENTITY = '41317ca8bdc549742905cbc3dc0b5c8062870d051175fe8f15c5e7d55a385412'
SAVE = '6b4a10084c7e752c31fd2de121a00850aaa2bf1decd700b437d7dccfcdbc82e8'
PROCESS = dict(pid=11688, creation_filetime=134382442326469086,
               nonce='056ebfa0b921ddfc67d76a845902c0f1f4ecf4ff07aa963b2022be248dc51537',
               host_sha256='7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28',
               dll_sha256='e48149c20bcc313d2ae694838e45a0f8450179b410f41cd23694491180241d91',
               sfse_sha256='28c5bda41d9959c885efcb6e889de69e92767c80a1a66842d711d215f722f82b',
               module_base=140697845432320, qpc_frequency=10000000)
BUILD = dict(game='1.16.244.0', observer='0.9.3', sample='protected Save52',
             save_sha256=SAVE, route='N2 direct route')
COUNTS = dict(core=32432, causal=79952, scheduler=119920, lifetime=5968)
CENSUS = dict(core=('written', 'flushed', 'enqueued', 'acknowledged'),
              causal=('causal_written', 'causal_enqueued'),
              scheduler=('scheduler_written', 'scheduler_enqueued'),
              lifetime=('lifetime_written', 'lifetime_enqueued', 'lifetime_flushed', 'lifetime_acknowledged'))
ZERO = ('drops queue_full contention_exhausted reentrant_losses loss_generation '
        'first_loss_sampled_admission last_loss_sampled_admission output_faults '
        'causal_active causal_bridge_active causal_drops causal_reentrant causal_native_counter_faults '
        'causal_baseline_unknown causal_multiowner causal_uncertain scheduler_active scheduler_drops '
        'scheduler_reentrant scheduler_bridge_active scheduler_registry_faults scheduler_identity_faults '
        'lifetime_drops lifetime_active lifetime_unlogged_cutoff_ticks geometry_no_slot counter_fault_ids').split()
FALSE = ('failed loss_bounds_uncertain causal_failed causal_counter_overflow scheduler_failed '
         'scheduler_counter_overflow scheduler_counter_contention lifetime_failed '
         'lifetime_counter_overflow geometry_failed').split()
TERMINAL_FIELDS = {*ZERO, *FALSE, *(k for fields in CENSUS.values() for k in fields),
                   'resident_inert', 'geometry_completed', 'geometry_captured',
                   'lifetime_qualified_from_ticks', 'lifetime_qualified_through_ticks',
                   'lifetime_prefix_crc32', 'lifetime_bytes'}
LIFETIME_FIELDS = 'sequence kind phase invocation parent thread ticks receiver allocation status epoch hazards'.split()
FIELDS = dict(core=(*core_reader.NAMES, 'request', 'birth_fields', 'descriptor', 'pad_class'),
              causal=(*CAUSAL_FIELDS, 'request'),
              scheduler=(*SCHEDULER_FIELDS, 'request', 'native_key', 'discriminator', 'queue'),
              lifetime=tuple(LIFETIME_FIELDS))
KIND_LIMITS = dict(core=17, causal=15, scheduler=12)
MEMBERS = {'session.json', 'geometry.json', *(channel + '.jsonl' for channel in COUNTS)}
STAGES = (1, 2, 5, 3, 10, 7, 9)
UNKNOWN = ('successful claim CAS', 'selected queue route', 'unique pause attribution',
           'uninstrumented winner', 'usual winner', 'population frequency')


def sha(data):
    return hashlib.sha256(data).hexdigest()


def unique(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'Duplicate JSON key')
        result[key] = value
    return result


def decode(data):
    return json.loads(data, object_pairs_hook=unique)


def uint(value, bits=64):
    return type(value) is int and 0 <= value < 2 ** bits


def fixed_hex(value, size):
    require(isinstance(value, str) and len(value) == 2 * size, 'Wrong encoded field width')
    raw = bytes.fromhex(value)
    require(raw.hex() == value, 'Noncanonical encoded field')
    return raw


def rows(data, channel, session):
    with_header, sep, body = data.partition(b'\n')
    require(sep and body.endswith(b'\n'), 'Truncated projected journal')
    require(decode(with_header) == dict(schema=SCHEMA, channel=channel,
            identity_sha256=session['identity_sha256'], fields=list(FIELDS[channel])),
            'Wrong journal domain, process or field layout')
    records = []
    for index, line in enumerate(body.splitlines(), 1):
        values = decode(line)
        require(isinstance(values, list) and len(values) == len(FIELDS[channel]), 'Malformed projected record')
        row = dict(zip(FIELDS[channel], values, strict=True))
        require(type(row['sequence']) is int and row['sequence'] == index, 'Projected sequence gap or reorder')
        special = {'request', 'birth_fields', 'descriptor', 'native_key', 'discriminator', 'queue'}
        if channel == 'lifetime':
            special.update(('kind', 'phase'))
        require(all(uint(v) for k, v in row.items() if k not in special), 'Invalid projected scalar')
        if channel in KIND_LIMITS:
            require(1 <= row['kind'] <= KIND_LIMITS[channel], 'Invalid event kind for channel')
        if 'request' in row:
            q = row['request']
            require(isinstance(q, list) and len(q) == 2 and
                    all(type(v) is int and -(2**31) <= v < 2**31 for v in q), 'Malformed original request')
        if channel == 'scheduler':
            require(all(isinstance(row[k], list) and len(row[k]) == size and
                        all(uint(n, bits) for n in row[k])
                        for k, size, bits in (('native_key', 3, 32), ('discriminator', 3, 32), ('queue', 6, 64))),
                    'Malformed scheduler payload array')
        if channel == 'core':
            raw = bytearray(112)
            birth_fields = row.pop('birth_fields')
            if row['kind'] == 14:
                require(isinstance(birth_fields, list) and len(birth_fields) == len(BIRTH_SLICES),
                        'Incomplete source birth fields')
                for (offset, size), value in zip(BIRTH_SLICES, birth_fields, strict=True):
                    raw[offset:offset+size] = fixed_hex(value, size)
            else:
                require(birth_fields is None, 'Source fields outside birth domain')
            row['source_bytes'] = raw.hex()
            desc = fixed_hex(row['descriptor'], 41)
            pad = row.pop('pad_class')
            require(uint(pad, 24), 'Invalid descriptor equality class')
            row['descriptor'] = (desc[:1] + pad.to_bytes(3, 'little') + desc[1:]).hex()
        records.append(row)
    require(len(records) == COUNTS[channel], 'Incomplete projected journal census')
    return records


def check_session(session):
    require(session['schema'] == SCHEMA and session['identity_sha256'] == IDENTITY and
            session['process'] == PROCESS and session['baseline'] == BUILD, 'Wrong N2 process or baseline')
    t = session['terminal']
    require(set(t) == TERMINAL_FIELDS and all(t[k] is False for k in FALSE) and
            all(type(t[k]) is int and t[k] == 0 for k in ZERO) and
            t['resident_inert'] is True and t['geometry_completed'] == t['geometry_captured'] == 1,
            'Contradictory terminal status')
    require(all(type(t[k]) is int and t[k] == COUNTS[name] for name, keys in CENSUS.items() for k in keys),
            'Terminal channel accounting')


def lifetime_journal(lifetime, session):
    opened, seen = {}, set()
    offsets = dict(HOLDER_RESOURCE_MAP=16, COLLECTION_GEOMETRY=8, COLLECTION_MUTATION=8)
    for row in lifetime:
        k = row['thread'], row['invocation']
        kind, phase = row['kind'], row['phase']
        require(kind in offsets and phase in ('BEGIN', 'END') and all(k) and row['allocation'] and
                row['receiver'] == row['allocation'] + offsets[kind] and row['status'] in (0, 16),
                'Invalid lifetime domain')
        if phase == 'BEGIN':
            require(k not in seen and row['status'] == 0, 'Duplicate or failed lifetime begin')
            seen.add(k)
            opened[k] = row
        else:
            begin = opened.pop(k, None)
            require(begin and begin['ticks'] <= row['ticks'] and
                    all(begin[f] == row[f] for f in ('kind', 'parent', 'receiver', 'allocation')),
                    'Contradictory lifetime pair')
    t = session['terminal']
    first, last = (t['lifetime_qualified_' + k + '_ticks'] for k in ('from', 'through'))
    mark = session['lifetime_mark']
    require(not opened and 0 < first <= last == mark['ticks'] and
            all(row['ticks'] >= first for row in lifetime), 'Incomplete lifetime coverage')
    qualify_mark(mark, lifetime, len(lifetime))
    return dict(events=lifetime, records=len(lifetime), qualified_from_ticks=first,
                qualified_through_ticks=last, raw_prefix_sha256=session['lifetime_original_sha256'])


def construction(core, winner):
    parts = winner['core']
    require([r['kind'] for r in parts] == [2,3,4,5,6,7,8,16,17,9], 'Incomplete or duplicate construction boundaries')
    selected, visited, lookup, descriptor, generating, sample, returned, reserve, store, _ = parts
    entry, birth, pub = (at(core, s) for s in (3924, winner['source_birth'], winner['source_publication']))
    require(entry['kind'] == 1 and entry['sequence'] < selected['sequence'] and
            winner['request'] == [-2, 11] and
            all(r['request'] == entry['request'] and r['thread'] == entry['thread'] and
                r['invocation'] == entry['invocation'] and r['parent'] == entry['parent'] and
                r['proc'] == selected['proc'] and r['epoch'] == selected['epoch'] and
                not (r['status'] or r['hazards']) for r in [entry, *parts]) and
            all(a['ticks'] <= b['ticks'] and a['sequence'] < b['sequence']
                for a, b in zip([entry, *parts], parts)), 'Unqualified constructor invocation or order')
    require(birth['kind'] == 14 and pub['kind'] == 15 and birth['selection'] == 932 and
            birth['holder'] == pub['holder'] and birth['source'] == pub['source'] == selected['source'] and
            birth['thread'] == pub['thread'] and not any(r['status'] or r['hazards'] for r in (birth, pub)),
            'Unqualified constructor birth/publication')
    source.continuity(core, birth['ticks'], store['ticks'], birth['epoch'], store['epoch'], birth['holder'])
    require(visited['a'] == 0 and lookup['a'] == lookup['b'] == 64 and
            lookup['c'] == selected['source'] and lookup['d'] == selected['epoch'] and
            descriptor['d'] == descriptor['holder'] + 0xc8 and
            descriptor['descriptor'] == generating['descriptor'] == sample['descriptor'] == returned['descriptor'] and
            generating['a'] == 0x5e0de and generating['c'] == sample['c'] and
            sample['a'] == 3 and sample['sequence'] == 3962, 'Wrong visited, map, consumed frame or direct sample')
    require(reserve['a'] != 0xffffffff and reserve['a'] < (reserve['c'] & 0xffffffff) <= reserve['c'] >> 32 and
            store['a'] == reserve['d'] + reserve['a'] * 8 and store['sequence'] == 3972 and
            store['b'] == birth['a'] == struct.unpack_from('<Q', bytes.fromhex(birth['source_bytes']), 0x68)[0] and
            store['c'] == birth['d'] == 0, 'Wrong append destination, source token or loss')
    return dict(proc=selected['proc'], invocation=selected['invocation'], selection=selected['selection'],
                request=entry['request'], mask=sample['a'], miss=lookup['sequence'], sample=sample['sequence'],
                store=store['sequence'])


def snapshot_evidence(snapshot, core, journal, winner, chain):
    h, holders = snapshot['header'], snapshot['holders']
    require(snapshot['identity_sha256'] == IDENTITY and h['request'] == h['snapshot'] == 1 and
            h['proc'] == chain['proc'] and h['owner_formid'] == 0x5e0de and
            h['boundary'] == 2 and h['preunlock_seen'] == h['scan_result'] == 1 and
            h['iterator'] == h['scan_capacity'] == h['map_capacity'] and
            h['ticks_begin'] < h['ticks_end'] <= h['completion_ticks'] and
            h['completion_epoch'] == h['epoch'] and
            not any(h[k] for k in ('status', 'loss', 'hazards', 'completion_hazards')) and
            not h['lock_state'] & 0xffc00000 and h['lock_owner'] != h['thread'] and
            all(0x10000 <= h[k] < 0x7fffffffffff for k in ('proc', 'manager', 'consumer')),
            'Wrong or incomplete snapshot boundary')
    require(len(holders) == h['holders'] == 36 <= h['map_capacity'] and
            all(len({p[key] for p in holders}) == len(holders) for key in ('source_pointer', 'holder_pointer')),
            'Incomplete occupied holder census')
    keys, target = set(), None
    for holder in holders:
        identity = source.source_identity(core, holder['source_pointer'], h)
        require(identity['key'] not in keys, 'Geographic source collision at snapshot')
        keys.add(identity['key'])
        if identity['key'] == core_reader.TARGET:
            target = holder, identity
    require(target is not None, 'Target holder absent')
    holder, identity = target
    require(identity['allocation'] == winner['source_allocation'] and
            identity['birth_sequence'] == winner['source_birth'] and
            identity['publication_sequence'] == winner['source_publication'], 'Substituted source birth')
    pointer = holder['holder_pointer']
    generation = source.generation(core, identity, pointer, h)
    require(generation and generation['invocation'] == chain['invocation'] and
            generation['selection'] == chain['selection'], 'Consumed generation/frame mismatch')
    owner = source.owner_context(core, h, 0x5e0de)
    require(owner['generate_sequence'] == 29325, 'Owner context continuity')
    require(all(len(p['counts']) == 3 and all(uint(n) for n in p['counts']) and
                p['counts'][0] <= p['resource_capacity'] for p in holders) and
            [sum(p['counts'][i] for p in holders) for i in range(3)] ==
            [h[k] for k in ('resources', 'regions', 'points')], 'Snapshot census mismatch')
    collections = holder['collections']
    for c in collections:
        require(len(c['regions']) <= c['region_capacity'] and
                all(r['address'] == c['region_data'] + 48 * i and
                    0 <= r['count'] <= r['point_capacity'] and
                    (not r['point_capacity'] or r['point_data'] >= 0x10000)
                    for i, r in enumerate(c['regions'])), 'Target nested allocation shape')
    counts = [len(collections), sum(len(c['regions']) for c in collections),
              sum(r['count'] for c in collections for r in c['regions'])]
    require(counts == holder['counts'] == [3, 78, 180] and
            all(len({c[k] for c in collections}) == 3 for k in ('resource', 'collection_pointer')),
            'Target collection census')
    qualify_snapshot(snapshot, journal)
    source.qualify_construction(dict(generation=generation, header=h, holder_pointer=pointer,
        collection_pointers=[c['collection_pointer'] for c in collections]), journal)
    return dict(source=identity, generation=generation, owner=owner, counts=counts)


def at(events, sequence):
    row = events[sequence - 1]
    require(row['sequence'] == sequence, 'Event-domain selector mismatch')
    return row


def task_histories(scheduler):
    groups, nodes = defaultdict(list), defaultdict(set)
    for row in scheduler:
        require(row['thread'] and (row['kind'] != 3 or row['extra'] < 256), 'Scheduler native field domain')
        if row['allocation']:
            groups[row['node'], row['allocation']].append(row)
            nodes[row['allocation']].add(row['node'])
    result = []
    for (node, allocation), records in groups.items():
        identities = {(r['family'], tuple(r['native_key']), tuple(r['request']), tuple(r['discriminator']))
                      for r in records}
        issues = []
        if not node or len(nodes[allocation]) != 1 or sum(r['kind'] == 1 for r in records) != 1:
            issues.append('AMBIGUOUS_PUBLICATION')
        if len(identities) != 1 or any(r['family'] not in (1, 2) or r['status'] for r in records):
            issues.append('TASK_IDENTITY_OR_STATUS')
        result.append(dict(node=node, allocation=allocation, issues=issues))
    return result


def competition(core, causal, scheduler):
    tasks, births = extract(core, {'events': causal},
                            {'events': scheduler, 'histories': task_histories(scheduler)}, core_reader)
    require([(b['sequence'], b['selection']) for b in births] ==
            [(898,387), (902,388), (906,389), (932,397), (1278,569), (1692,749), (1696,750), (2082,932)],
            'Wrong geographic birth census')
    require(len(tasks) == 392 and all(t['source_allocation'] == 932 for t in tasks), 'Incomplete target cohort')
    require(all(at(core, b['sequence'] + 1)['kind'] == 15 and
                all(at(core, b['sequence'] + 1)[k] == b[k] for k in ('source', 'holder', 'thread', 'epoch'))
                for b in births), 'Unqualified geographic birth publication')
    publications = [r for r in scheduler if r['kind'] == 1 and all(-2 <= q <= 11 for q in r['request'])]
    require(len(publications) == 392 and {(r['node'], r['allocation'], r['family'], tuple(r['request']))
            for r in publications} == {(t['node'], t['task'], t['family'], tuple(t['request'])) for t in tasks},
            'Incomplete coordinate-compatible publication census')
    coords = {(x, y) for x in range(-2, 12) for y in range(-2, 12)}
    require(all({tuple(t['request']) for t in tasks if t['family'] == f} == coords for f in (1, 2)),
            'Incomplete typed coordinate coverage')
    winners = [t for t in tasks if t['outcome'] == 'MISS']
    require(len(winners) == 1 and winners[0]['task'] == 1211, 'Wrong target miss census')
    winner = winners[0]
    stage = {}
    miss, store = (at(core, s) for s in (3959, 3972))
    target_contexts = {(t['thread'], t['invocation'], t['selection'], t['source']) for t in tasks}
    fences = [r for r in core if r['kind'] in (10, 11)]
    birth = births[-1]
    for t in tasks:
        indexed = defaultdict(list)
        for row in t['scheduler']:
            require(row['family'] == t['family'] and row['request'] == t['request'],
                    'Task allocation/family/request mismatch')
            indexed[row['kind']].append(row)
        require(all(len(indexed[k]) == 1 for k in (1, 2, 3, 4, 5, 7, 8, 9)) and indexed[6] and
                0 < len(indexed[10]) == len(indexed[11]) == len(indexed[12]),
                'Missing or ambiguous typed stage')
        stage[t['task']] = {k: min(values, key=lambda r: (r['ticks'], r['sequence'])) for k, values in indexed.items()}
        s = stage[t['task']]
        stamps = [s[k]['ticks'] for k in (*STAGES, 8, 4)]
        require(stamps == sorted(stamps), 'Typed task stages contradict recorded progress order')
        selected = t['core'][0]
        require(s[9]['thread'] == selected['thread'] and s[9]['ticks'] <= selected['ticks'] and
                s[8]['ticks'] >= selected['ticks'] and s[4]['ticks'] >= s[8]['ticks'],
                'Provider/selection/retirement order')
        visited = [r for r in t['core'] if r['kind'] == 3]
        require(len(visited) == 1 and visited[0]['a'] == int(t is not winner) and
                t['outcome'] == ('MISS' if t is winner else 'VISITED_BYPASS'), 'False target bypass')
        require(t is winner or [r['kind'] for r in t['core']] in ([2, 3], [2, 3, 9]),
                'Contrary target bypass history')
        require(all(r['frame'] == t['frame'] and r['proc'] == t['owner'] and r['request'] == t['request'] and
                    r['epoch'] == selected['epoch']
                    for r in t['core']), 'Core task/source domain mismatch')
        require(t is winner or visited[0]['ticks'] > store['ticks'], 'Visited bypass precedes target authority')
        source.continuity(fences, birth['ticks'], visited[0]['ticks'], birth['epoch'], visited[0]['epoch'], birth['holder'])
        if t is not winner:
            require([r['kind'] for r in t['causal']] == [5, 15, 6, 11],
                    'Contrary target exclusive or pending history')
            registered, admitted, released, done = t['causal']
            require(all(r['request'] == t['request'] and r['epoch'] == selected['epoch'] for r in t['causal']) and
                    selected['ticks'] <= registered['ticks'] <= admitted['ticks'] <= released['ticks'] <=
                    visited[0]['ticks'] <= done['ticks'], 'Target bypass lacks ordered shared visit evidence')
    require(all((r['thread'], r['invocation'], r['selection'], r['source']) in target_contexts
                for r in causal if r['source'] == winner['source'] and r['ticks'] > birth['ticks'] and
                r['kind'] in (2, 3, 7, 9, 10)), 'Unjoined contrary target writer history')
    exclusive = [r for t in tasks for r in t['causal'] if r['kind'] in (2, 3, 7, 9, 10)]
    require([r['sequence'] for r in exclusive] == [2948, 2949, 2950, 2951, 2957],
            'Contrary target exclusive or pending history')
    lead = {}
    for kind in STAGES:
        order = sorted((stage[t['task']][kind]['ticks'], t['task'], stage[t['task']][kind]['sequence'])
                       for t in tasks)
        require(order[0][1] == winner['task'] and order[0][0] < order[1][0], 'Wrong winner stage order')
        lead[kind] = [order[0][2], order[1][2], order[1][0] - order[0][0]]
    density = sorted((t for t in tasks if t['family'] == 1), key=lambda t: stage[t['task']][1]['ticks'])
    order = [tuple(t['request']) for t in density]
    _, model = registration()
    require(order == sorted(coords, key=lambda q: (q[0]-q[1], q[0])) == [q for q in model if q in coords] and
            {stage[t['task']][1]['thread'] for t in density} == {34060}, 'Wrong density publication frontier')
    ws = stage[winner['task']]
    layer = next(t for t in tasks if t['family'] == 2 and t['request'] == winner['request'])
    prior_dependencies = [r for r in layer['scheduler'] if r['kind'] == 6 and r['ticks'] < miss['ticks']]
    require(ws[5]['extra'] == ws[3]['serial'] == 970 and ws[3]['rank'] == 0 and ws[3]['extra'] == 1 and
            layer['task'] == 1237 and prior_dependencies and
            max(prior_dependencies, key=lambda r: r['ticks'])['dependencies'] == 7,
            'Decisive readiness/dispatch operands changed')
    peers, partitions = {}, Counter()
    for t in tasks:
        s = stage[t['task']]
        require(s[1]['ticks'] < miss['ticks'] and s[2]['ticks'] < miss['ticks'] and
                (s[5]['ticks'] < miss['ticks']) == (t['family'] == 1) and
                (s[3]['ticks'] < miss['ticks']) == (t['family'] == 1) and
                (t['family'] == 1 or s[9]['ticks'] > miss['ticks']),
                'Task family readiness/service partition at authority')
        if t is winner:
            group = 'constructor'
        elif s[5]['ticks'] > miss['ticks']:
            group = 'ready_after'
        elif s[9]['ticks'] > miss['ticks']:
            group = 'provider_after'
        else:
            group = 'peer'
        partitions[group] += 1
        if group in ('constructor', 'peer'):
            path = [r for r in core if r['kind'] == 2 and (r['thread'], r['invocation']) ==
                    (t['thread'], t['invocation']) and r['sequence'] <= t['core'][0]['sequence']]
            require(len(path) == 4 and all(p['source'] != t['source'] for p in path[:-1]) and
                    path[-1] == t['core'][0] and (group == 'constructor' or path[-1]['ticks'] > store['ticks']),
                    'Peer or winner earlier-source path mismatch')
            require(group == 'constructor' or path[0]['ticks'] < miss['ticks'] < path[1]['ticks'],
                    'Early provider lacks preceding source progress at authority')
            for prior in path[:-1]:
                decisions = [r for r in core if r['kind'] == 3 and
                             all(r[k] == prior[k] for k in ('thread', 'invocation', 'selection', 'source', 'frame'))]
                require(len(decisions) == 1 and decisions[0]['a'] == 1 and
                        not (decisions[0]['status'] or decisions[0]['hazards']) and
                        prior['ticks'] <= decisions[0]['ticks'] < path[-1]['ticks'],
                        'Missing or contrary earlier-source work')
            peers[t['task']] = [p['sequence'] for p in path]
    require(partitions == dict(constructor=1, peer=2, provider_after=193, ready_after=196) and
            set(peers) == {1211, 1283, 1284}, 'Wrong authority-time partitions')
    return winner, stage[winner['task']], dict(lead=lead, peers=peers, partitions=dict(partitions),
                                               target_tasks=len(tasks), bypasses=len(tasks)-1)


def owner_history(core, causal, scheduler, winner):
    lock = winner['owner'] + 0x40
    require(all((r['lock'], r['generation']) == (lock, 1) and r['thread'] and not r['status']
                for r in causal), 'Wrong or uncertain owner generation')
    registers = [r for r in causal if r['kind'] == 1]
    require(len(registers) == 1 and registers[0]['sequence'] == 1 and
            registers[0]['old_state'] == registers[0]['new_state'] == 0, 'Missing zero owner registration')
    transitions = {2:'pending', 3:'acquire', 5:'reader_register', 6:'reader_release', 7:'release'}
    for row in causal:
        if row['kind'] in transitions:
            old, new = row['old_state'], row['new_state']
            require(uint(old, 32) and uint(new, 32) and transition(old, transitions[row['kind']]) == new,
                    'Contradictory owner atomic operands')
    participants = triples(causal)
    counts = Counter(p['type'] for p in participants)
    require(counts == dict(writer=518, reader=23194), 'Incomplete owner participant census')
    selected = {(r['thread'], r['invocation'], r['selection'], r['source']): r for r in core if r['kind'] == 2}
    providers = {(r['thread'], r['core_invocation']): r for r in scheduler if r['kind'] == 9}
    unknown = Counter()
    by_event = {}
    for part in participants:
        events = part['events']
        first = events[0]
        key = tuple(first[k] for k in ('thread', 'invocation', 'selection', 'source'))
        require(all(tuple(r[k] for k in ('thread', 'invocation', 'selection', 'source')) == key for r in events)
                and all(a['ticks'] <= b['ticks'] for a,b in zip(events, events[1:])),
                'Owner triple changed event context')
        if key not in selected:
            unknown[part['type']] += 1
        if key in selected and key[:2] in providers:
            require(first['request'] == providers[key[:2]]['request'], 'Wrong owner/provider request join')
        for event in events:
            by_event[event['sequence']] = part
    require(unknown == dict(writer=473, reader=14473), 'Unknown owner client census')
    chosen = by_event[2949]
    foreign = by_event[2925]
    foreign_start = foreign['events'][0]
    foreign_key = tuple(foreign_start[k] for k in ('thread', 'invocation', 'selection', 'source'))
    require([r['sequence'] for r in chosen['events']] == [2949, 2950, 2957] and
            [r['sequence'] for r in foreign['events']][1:] == [2925, 2932] and
            foreign_key in selected and foreign_key[:2] in providers and
            selected[foreign_key]['proc'] == winner['owner'] and foreign_start['source'] != winner['source'] and
            chosen['events'][0]['source'] == winner['source'] and
            chosen['events'][0]['invocation'] == winner['invocation'], 'Foreign or target writer identity')
    def event(i):
        return at(causal, i)
    # These are same-thread mapped callback bounds. They do not order
    # cross-thread atomic transitions or identify an OS wait interval.
    selection, visit, miss, store, provider_return = (at(core, i) for i in (3942, 3958, 3959, 3972, 3978))
    boundaries = [selection, event(2927), event(2939), event(2942), visit, event(2947), event(2948),
                  event(2949), event(2950), event(2951), miss, store, event(2957), provider_return]
    context = (winner['thread'], winner['invocation'], winner['selection'], winner['source'],
               winner['request'], selection['epoch'])
    require(all(tuple(r[k] for k in ('thread', 'invocation', 'selection', 'source', 'request', 'epoch')) ==
                context for r in boundaries) and
            all(a['ticks'] <= b['ticks'] for a, b in zip(boundaries, boundaries[1:])) and
            [event(i)['site'] - PROCESS['module_base'] for i in (2927, 2939, 2942, 2949, 2950, 2957)] ==
            [0x22cc366, 0x22cc3c3, 0x79fc85, 0x22cc410, 0x22cc48f, 0x2c45c2],
            'Same-thread protected constructor enclosure mismatch')
    require([(event(i)['old_state'], event(i)['new_state']) for i in (2927, 2932, 2942, 2949, 2950)] ==
            [(0x401000,0x401001), (0x401005,5), (1,0), (0,0x1000), (0x1000,0x401000)] and
            by_event[2927] is by_event[2942] and
            [r['sequence'] for r in by_event[2927]['events']] == [2927,2939,2942] and
            [r['sequence'] for r in winner['causal'] if r['kind'] == 11] == [2947] and
            event(2942)['thread'] == event(2949)['thread'] == winner['thread'] and
            event(2942)['ticks'] <= event(2947)['ticks'] <= event(2948)['ticks'] <= event(2949)['ticks'],
            'Target reader, zero-pending or acquire operand mismatch')
    drain = [2935, 2937, 2941, 2940, 2942]
    seqs = [*range(2927, 2933), 2935, 2937, 2940, 2941, 2942, 2949, 2950]
    cohort = [event(i) for i in seqs]
    require(len({id(by_event[i]) for i in range(2927, 2932)}) == 5 and
            {id(by_event[i]) for i in range(2927, 2932)} == {id(by_event[i]) for i in drain} and
            event(2940)['ticks'] == event(2941)['ticks'] and
            exhaustive_operands(cohort, 0x401000) == [[*range(2927, 2933), *drain, 2949, 2950]],
            'Five-reader operand continuation mismatch')
    # Same-owner accounting is conditional on original native coverage and
    # the recorded lifecycle and status bounds in the complete projection.
    index = HistoryIndex(causal, [])
    pairs = Counter(p['interpretation'] for p in index.iter_legacy())
    require(pairs == dict(RELEVANT_LIFECYCLE_OR_CONTEXT_UNCERTAINTY=71118,
                          EARLIER_ACQUISITION_BEFORE_OTHER_HELPER_ENTRY=849,
                          OVERLAPPING_INTERVALS_UNKNOWN=15, PRIOR_PENDING_WRITER_OVERTAKEN=33),
            'Conditional owner-wide pair accounting changed')
    return dict(counts=dict(counts), unscoped=dict(unknown), pairs=dict(pairs), reader_drain=drain,
                target_pending=2949, target_overtakes=0)


def continuations(channels, winner, stages):
    core, causal = channels['core'], channels['causal']
    a, b = at(causal, 2946), at(core, 3967)
    lo, hi = a['ticks'], b['ticks']
    require(a['kind'] == 11 and b['kind'] == 2 and a['thread'] == b['thread'] == 56840 and
            a['invocation'] == b['invocation'] == 1804 and
            lo < at(causal, 2949)['ticks'] < at(causal, 2950)['ticks'] < hi,
            'Wrong peer pause interval or arbitration')
    require(not any(r['thread'] == a['thread'] and lo < r['ticks'] < hi
                    for rows in channels.values() for r in rows), 'Intervening peer stamp')
    alternatives = dict(observer_tail=[lo, lo+1, lo+2, lo+5002, lo+5050, hi],
                        native_continuation=[lo, lo+1, lo+50, lo+51, lo+5051, hi])
    require(all(all(a < b for a, b in zip(ts, ts[1:])) for ts in alternatives.values()), 'Infeasible pause placement')
    claim_return = stages[10]['ticks']
    last = max(r['ticks'] for rows in channels.values() for r in rows
               if r['thread'] == winner['thread'] and r['ticks'] < claim_return)
    start = max(last, stages[3]['ticks'], stages[12]['ticks'])
    first, second = (start + (claim_return-start)*n//3 for n in (1, 2))
    require(start < first < second < claim_return <= stages[7]['ticks'], 'Infeasible internal claim bounds')
    return dict(peer_gap_ticks=hi-lo, pause_models=alternatives, internal_claim_models=[first, second],
                unknown=list(UNKNOWN), basis='Authored models conditional on historically reviewed native and emitter coverage')


def interpret(session, snapshot, channels):
    check_session(session)
    journal = lifetime_journal(channels['lifetime'], session)
    core, causal, scheduler = (channels[k] for k in ('core', 'causal', 'scheduler'))
    winner, stages, race = competition(core, causal, scheduler)
    chain = construction(core, winner)
    return dict(construction=chain, retained=snapshot_evidence(snapshot, core, journal, winner, chain),
                competition=race, owner=owner_history(core, causal, scheduler, winner),
                continuations=continuations(channels, winner, stages))


def parse(members):
    session = decode(members['session.json'])
    check_session(session)
    channels = {k: rows(members[k + '.jsonl'], k, session) for k in COUNTS}
    return session, decode(members['geometry.json']), channels


def read_zip(package, manifest):
    require(manifest['schema'] == SCHEMA and set(manifest['members']) == MEMBERS, 'Unexpected manifest layout')
    pin = manifest['candidate']
    with package.open('rb') as stream:
        require(stream.seek(0, 2) == pin['bytes'], 'ZIP size differs from exact candidate')
        stream.seek(0)
        require(hashlib.file_digest(stream, 'sha256').hexdigest() == pin['sha256'], 'ZIP hash differs from exact candidate')
        stream.seek(0)
        with zipfile.ZipFile(stream) as archive:
            infos = archive.infolist()
            require([i.filename for i in infos] == sorted(MEMBERS), 'ZIP members missing, duplicated or reordered')
            result = {}
            for info in infos:
                expected = manifest['members'][info.filename]
                require(info.file_size == expected['bytes'], 'Projected member extent mismatch')
                data = archive.read(info)
                require(sha(data) == expected['sha256'], 'Projected member hash mismatch')
                result[info.filename] = data
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('candidate', type=Path)
    args = parser.parse_args()
    manifest = decode(MANIFEST.read_bytes())
    summary = interpret(*parse(read_zip(args.candidate, manifest)))
    print(json.dumps(dict(tier='PROJECTED_N2_EVENT_RELATIONSHIPS', candidate=manifest['candidate'],
                          channel_records=COUNTS, **summary), indent=2))


if __name__ == '__main__':
    main()
