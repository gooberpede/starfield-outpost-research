# SPDX-License-Identifier: GPL-3.0-or-later
"""Read the sealed C19 archive and write a bounded callback derivative and custody receipt.

CPython 3.14+ standard library and the existing project-owned 070 offline decoder.
No archive extraction, target access, database, save or source changes.
"""

import argparse
from collections import Counter
from compression.zstd import ZstdFile
import csv
import hashlib
import json
import os
from pathlib import Path
import struct
import sys
import tarfile


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'runtime/beacon-resource-070'))
from inspect_resources import SIZE, decode, field, resource


ARCHIVE_BYTES = 351425006
ARCHIVE_SHA = '2df3244872961232c87067ca60e2c59e54ab66d7c2c858031db2649cc86ed8a5'
MANIFEST = 'ARCHIVE-MEMBERS.json'
MANIFEST_SHA = 'de8b2aa5f2fe89878ef8d8a1f4708952302250f955cdddfab1b4e7eaf1c8d8d1'
EXE_SHA = '7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28'
ESM_SHA = '1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7'
PREFIX = '.local-work/continuous-beacon-preview/'
SESSION = PREFIX + 'live/session-24552-88395531/'
RUN = PREFIX + 'run-20261014T233433728771Z/'
LEDGER = ROOT / 'docs/experiments/continuous-beacon-preview/live-sources.csv'
DECODER = ROOT / 'runtime/beacon-resource-070/inspect_resources.py'
DECODER_SHA = 'f8d04369ded0ccc24cceba08443d6c9487cd93e9ebdc98a9f52cde78b7af5ce9'
RAW_COUNT = 611926
EVENTS = SESSION + 'events.bin'
JOURNAL = SESSION + 'records.jsonl'
SELECTED_RECEIPTS = {
    SESSION + name for name in ('session.json', 'retired.json')
} | {
    RUN + name for name in ('seal.json', 'phase-analysis01.json', 'preview-reference-definitions01.json',
                            'additional-resource-definitions01.json')
}
RESOURCE_NAMES = {0x57C1: 'Lead', 0x57C7: 'Iron', 0x57C9: 'Alkanes', 0x57F5: 'Helium-3'}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def json_bytes(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':')) + '\n').encode('utf-8')


def file_identity(path):
    with path.open('rb') as source:
        return dict(bytes=os.fstat(source.fileno()).st_size,
                    sha256=hashlib.file_digest(source, 'sha256').hexdigest())


def member_identity(data):
    return dict(bytes=len(data), sha256=hashlib.sha256(data).hexdigest())


def model_range(event):
    return field(event['output'], 0x38, '<Q'), field(event['output'], 0x40, '<Q')


class Capture:
    def __init__(self):
        self.active = {}
        self.invocations = set()
        self.tokens = {}
        self.models = {}
        self.callbacks = []
        self.evaluations = []

    def token(self, pointer):
        return self.tokens.setdefault(pointer, len(self.tokens) + 1) if pointer else 0

    def identity(self, pointer, form, form_type):
        if not pointer:
            require(form is None and form_type is None, 'null identity fields')
            return [0, None]
        require(form is not None and form_type == 0x9F, f'unresolved IRES operand form={form} type={form_type}')
        return [self.token(pointer), f'{form:08x}']

    def operand(self, event):
        value = resource(event)
        return self.identity(value['pointer'], value['form_id'], value['form_type'])

    def population(self, scope, phase, index):
        header, members = scope['pops'][phase, index]
        begin, end = header['args'][1:3]
        require(end - begin == len(members) * 8, 'population header/member length')
        return header['sequence'], members

    def consume(self, raw, sequence):
        require(struct.unpack_from('<Q', raw)[0] == sequence, 'raw sequence')
        event = decode(raw)
        kind, phase, invocation = event['kind'], event['phase'], event['invocation']
        require(event['status'] == 0, f'record {sequence} nonzero status')
        if kind == 108:
            require(phase in (1, 2), 'invalid population phase')
            scope = self.active.setdefault(invocation, {'pops': {}, 'children': [], 'census': []})
            key = (phase, event['args'][0])
            require(key not in scope['pops'], 'duplicate population header')
            scope['pops'][key] = event, []
        elif kind == 109:
            header, members = self.active[invocation]['pops'][phase, event['args'][0]]
            require(event['args'][1:3] == header['args'][1:3], 'member range differs from header')
            require(event['args'][3] == len(members), 'population member order')
            require(field(event['operand'], 0, '<Q') == event['reference'], 'member pointer copy')
            members.append([sequence, *self.operand(event)])
        elif kind == 110:
            census = self.active[invocation]['census']
            require(phase == 2 and event['operand']['ok'] and event['operand']['length'] == 0x170
                    and event['args'][3] == len(census), 'model row census order/read')
            census.append((sequence, event['operand']['address']))
        else:
            self.scope(event, kind, phase, invocation)

    def scope(self, event, kind, phase, invocation):
        require(kind in range(101, 108), 'unexpected observer kind')
        if phase == 1:
            require(invocation not in self.invocations, 'duplicate invocation entry')
            self.invocations.add(invocation)
            self.active.setdefault(invocation, {'pops': {}, 'children': [], 'census': []})['entry'] = event
            return
        scope = self.active.pop(invocation)
        entry = scope['entry']
        require(phase == 2 and all(event[key] == entry[key] for key in ('kind', 'site', 'parent', 'thread')),
                'unpaired, incomplete or changed invocation')
        require(entry['qpc'] <= event['qpc'], 'reversed native interval')
        parent = event['parent']
        if parent:
            self.active[parent]['children'].append((entry, event, scope))
        if kind == 101:
            signature = [[member[2] for member in self.population(scope, 2, index)[1]] for index in range(3)]
            self.evaluations.append((entry['qpc'], event['qpc'], invocation, event['site'], signature))
        elif kind == 102:
            self.callback(entry, event, scope)

    def callback(self, entry, exit_event, scope):
        children = sorted(scope['children'], key=lambda child: child[0]['sequence'])
        common = [(before, after, child) for before, after, child in children if before['kind'] in (103, 104)]
        require([(before['kind'], before['site']) for before, _, _ in common]
                == [(103, 0x15785C9), (104, 0x15785E8)], 'UI common-consumer call order')
        result = {'invocation': entry['invocation'], 'entry': entry['sequence'], 'exit': exit_event['sequence'],
                  'model': self.models.setdefault(entry['args'][1], len(self.models) + 1),
                  'qpc': [entry['qpc'], exit_event['qpc']], 'append': [], 'rows': []}
        for index, name in enumerate(('spatial', 'atmosphere')):
            before, after, child = common[index]
            header, members = self.population(child, 1, index)
            result[name] = dict(call=before['invocation'], entry=before['sequence'], exit=after['sequence'],
                                header=header, members=members)
        header, members = self.population(scope, 1, 2)
        result['biome'] = dict(header=header, members=members)
        pointer = field(entry['operand'], 0, '<Q')
        require(pointer is not None, 'water selector unreadable')
        result['selector'] = self.identity(pointer, field(entry['cell'], 0x28, '<I'),
                                           field(entry['cell'], 0x2E, '<B'))
        for before, after, _ in children:
            if before['kind'] == 105:
                require(before['site'] == 0x157862E, 'unexpected append site')
                pointer = field(before['operand'], 0, '<Q')
                require(pointer, 'selected append without readable resource pointer')
                identity = self.identity(pointer, field(before['base'], 0x28, '<I'),
                                         field(before['base'], 0x2E, '<B'))
                result['append'].append([before['invocation'], before['sequence'], after['sequence'], *identity])
        begin, end = model_range(exit_event)
        rows = [child for child in children if child[0]['kind'] == 106]
        require(begin is not None and end - begin == len(rows) * 0x170 and len(rows) == len(scope['census']),
                'UI final row census length')
        for ordinal, ((before, after, _), (census_seq, address)) in enumerate(zip(rows, scope['census'], strict=True)):
            require(before['site'] in (0x15787E9, 0x15787FC) and before['command'] == ordinal
                    and after['operand']['ok'] and after['operand']['length'] == 0x170
                    and address == begin + ordinal * 0x170, 'constructor/census ordinal association')
            result['rows'].append([ordinal, before['invocation'], before['sequence'], after['sequence'],
                                   census_seq, *self.operand(before)])
        self.callbacks.append(result)


def read_events(reader, size):
    require(size == RAW_COUNT * SIZE, 'WAL member byte count')
    digest = hashlib.sha256()
    hashes = bytearray()
    capture = Capture()
    sequence = 0
    while block := reader.read(SIZE * 256):
        digest.update(block)
        require(len(block) % SIZE == 0, 'partial raw record')
        view = memoryview(block)
        for offset in range(0, len(view), SIZE):
            raw = view[offset:offset + SIZE]
            sequence += 1
            hashes.extend(hashlib.sha256(raw).digest())
            capture.consume(raw, sequence)
    require(sequence == RAW_COUNT and not capture.active, 'incomplete capture census')
    return dict(bytes=size, sha256=digest.hexdigest()), hashes, capture


def read_journal(reader, size, hashes):
    digest = hashlib.sha256()
    total = 0
    count = 0
    for count, line in enumerate(reader, 1):
        digest.update(line)
        total += len(line)
        row = json.loads(line)
        start = (count - 1) * 32
        require(line.endswith(b'\n') and row['sequence'] == count and row['length'] == SIZE
                and row['offset'] == (count - 1) * SIZE
                and hashes[start:start + 32].hex() == row['sha256'], f'WAL journal record {count}')
    require(count == RAW_COUNT and total == size, 'journal final census or length')
    return dict(bytes=total, sha256=digest.hexdigest())


def read_archive(archive):
    ledger = {}
    with LEDGER.open(encoding='utf-8', newline='') as source:
        for row in csv.DictReader(source):
            member = RUN + Path(row['local_path'].replace('\\', '/')).name
            ledger[member] = (row['source_id'], row['sha256'])

    found, receipts = {}, {}
    journal_hashes = capture = manifest = None
    with archive.open('rb') as source:
        start = os.fstat(source.fileno())
        digest = hashlib.file_digest(source, 'sha256').hexdigest()
        require((start.st_size, digest) == (ARCHIVE_BYTES, ARCHIVE_SHA), 'compressed archive identity')
        source.seek(0)
        with ZstdFile(source, 'rb') as decoded, tarfile.open(fileobj=decoded, mode='r:', stream=True) as tar:
            for member in tar:
                name = member.name
                if not (name in ledger or name.startswith(SESSION) or name == MANIFEST):
                    continue
                require(member.isreg() and not member.sparse and name not in found, 'duplicate or nonregular archive member')
                with tar.extractfile(member) as reader:
                    if name == EVENTS:
                        found[name], journal_hashes, capture = read_events(reader, member.size)
                    elif name == JOURNAL:
                        require(journal_hashes is not None, 'journal encountered before raw member')
                        found[name] = read_journal(reader, member.size, journal_hashes)
                    elif (name in SELECTED_RECEIPTS or name == MANIFEST
                          or (name.startswith(SESSION + 'operator-') and name.endswith('.json'))):
                        data = reader.read()
                        found[name] = member_identity(data)
                        if name == MANIFEST:
                            require(found[name]['sha256'] == MANIFEST_SHA, 'embedded inventory hash')
                            manifest = json.loads(data)
                        else:
                            receipts[name] = json.loads(data)
                    else:
                        found[name] = dict(bytes=member.size, sha256=hashlib.file_digest(reader, 'sha256').hexdigest())
                    require(found[name]['bytes'] == member.size, 'archive member size mismatch')
        source.seek(0)
        require(hashlib.file_digest(source, 'sha256').hexdigest() == digest, 'archive changed during acquisition')
        after = os.fstat(source.fileno())
        current = archive.stat()
        for stat in (after, current):
            require((stat.st_dev, stat.st_ino, stat.st_size, stat.st_mtime_ns)
                    == (start.st_dev, start.st_ino, start.st_size, start.st_mtime_ns), 'archive identity changed')

    require(manifest is not None and len(manifest) == 134131, 'archive inventory census')
    members = {r['path']: {'bytes': r['bytes'], 'sha256': r['sha256']} for r in manifest
               if r['path'].startswith(SESSION) or r['path'] in ledger}
    require({name: row for name, row in found.items() if name != MANIFEST} == members, 'embedded source inventory comparison')
    require(len(ledger) == 25 and all(found[name]['sha256'] == pin for name, (_, pin) in ledger.items()),
            'tracked C19 live-source digest comparison')
    seal = receipts[RUN + 'seal.json']
    require(seal['status'] == 'SEALED_INVENTORY', 'original seal status')
    session = {name.removeprefix(SESSION): {'length': r['bytes'], 'sha256': r['sha256']}
               for name, r in found.items() if name.startswith(SESSION)}
    require(session == seal['files'], 'original session seal member comparison')
    terminal = receipts[SESSION + 'retired.json']
    original_session = receipts[SESSION + 'session.json']
    require(all(r['game_sha256'] == EXE_SHA and r['schema'] == 7 and r['event_size'] == SIZE
                and r['qpc_frequency'] == 10000000 and r['version'] == '0.7.0' for r in (original_session, terminal)),
            'capture baseline/schema')
    require(terminal['attempted'] == terminal['captured'] == terminal['last_durable_sequence'] == RAW_COUNT
            and terminal['offset'] == found[EVENTS]['bytes'] and terminal['failed'] == terminal['active'] == 0
            and not terminal['error'] and not terminal['integrity_failure'], 'capture retirement integrity')

    inventory = [{'member': name, **row, 'source_id': ledger.get(name, (None,))[0]}
                 for name, row in sorted(found.items())]
    return capture, receipts, inventory


def make_derivative(capture, receipts):
    preview_site = 0x21B42E3
    counts = Counter(site for _, _, _, site, _ in capture.evaluations)
    require(counts == {preview_site: 35573, 0x21B26BC: 1}, f'evaluation site census {counts}')
    runs = []
    for start, end, invocation, site, populations in sorted(capture.evaluations):
        if site != preview_site:
            continue
        if not runs or runs[-1]['populations'] != populations:
            runs.append(dict(run=len(runs) + 1, first_invocation=invocation, start=start,
                             evaluations=0, populations=populations, phase=None, operator_labels=None))
        run = runs[-1]
        run.update(end=end, last_invocation=invocation, evaluations=run['evaluations'] + 1)

    phase_source = receipts[RUN + 'phase-analysis01.json']
    initialization, = [invocation for _, _, invocation, site, _ in capture.evaluations if site != preview_site]
    original_runs = [segment for segment in phase_source['segments']
                     if not segment['first_inv'] == segment['last_inv'] == initialization]
    require(len(runs) == len(original_runs) == 6, f'stable preview run census {len(runs)}/{len(original_runs)}')
    for run, original in zip(runs, original_runs, strict=True):
        require([run['start'], run['end']] == original['qpc']
                and run['first_invocation'] == original['first_inv'] and run['last_invocation'] == original['last_inv']
                and run['evaluations'] == original['count']
                and [[int(form, 16) for form in pop] for pop in run['populations']] == original['population_signature'],
                'historical preview-run boundary comparison')
    for name, marker in receipts.items():
        if not name.startswith(SESSION + 'operator-') or not marker['phase'].endswith('_PREVIEW_VISIBLE'):
            continue
        receipt_qpc = marker['receipt_monotonic_ns'] // 100
        selected, = [run for run in runs if run['start'] <= receipt_qpc <= run['end']]
        selected.update(phase=marker['phase'][0], operator_labels=marker['reported_labels'])

    callbacks = sorted(capture.callbacks, key=lambda c: c['entry'])
    counts = Counter()
    for callback in callbacks:
        start, end = callback.pop('qpc')
        run, = [run for run in runs if run['start'] <= start and end <= run['end']]
        callback['run'] = run['run']
        counts[run['run']] += 1
    for run, original in zip(runs, original_runs, strict=True):
        require(counts[run['run']] == original['ui_updates'], 'historical preview-run callback count comparison')
        del run['start'], run['end']

    definitions = {}
    for name in ('preview-reference-definitions01.json', 'additional-resource-definitions01.json'):
        receipt = receipts[RUN + name]
        require(len(receipt['sources']) == 1 and receipt['sources'][0]['sha256'] == ESM_SHA, 'definition receipt ESM pin')
        for records in receipt['records'].values():
            record, = records
            if record['record_type'] == 'IRES':
                form = record['formid']
                definitions[f'{form:08x}'] = dict(label=RESOURCE_NAMES[form], editor_id=record['editor_id'],
                                                definition=f"{record['plugin']}:{form:06x}")
    require(len(definitions) == 4, 'resource definition census')
    return dict(schema='sor-d5be-c19-callbacks/1', capture='SOR-EV-0043', exe_sha256=EXE_SHA,
                definition_esm_sha256=ESM_SHA, records=RAW_COUNT, initialization_evaluations=1,
                preview_evaluations=35573, definitions=definitions, runs=runs, callbacks=callbacks)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive', type=Path)
    parser.add_argument('output_directory', type=Path)
    args = parser.parse_args()
    try:
        require(file_identity(DECODER)['sha256'] == DECODER_SHA, 'original offline decoder hash')
        output = args.output_directory.resolve()
        require(output.is_relative_to(ROOT / '.local-work/d5be/c19'), 'output must be inside the ignored C19 workspace')
        derivative = output / 'c19-callbacks-v1.json'
        receipt = output / 'custody.json'
        require(not derivative.exists() and not receipt.exists(), 'refuse to replace previous output')
        capture, receipts, inventory = read_archive(args.archive)
        payload = json_bytes(make_derivative(capture, receipts))
        custody = dict(schema='sor-d5be-c19-custody/1', archive=dict(bytes=ARCHIVE_BYTES, sha256=ARCHIVE_SHA),
                       members=inventory, wal_records=RAW_COUNT, decoder=file_identity(DECODER),
                       source_ledger=file_identity(LEDGER), producer=file_identity(Path(__file__)),
                       derivative=member_identity(payload))
        output.mkdir(parents=True, exist_ok=True)
        for path, data in ((derivative, payload), (receipt, json_bytes(custody))):
            with path.open('xb') as target:
                target.write(data)
        print(json.dumps(dict(custody['derivative'], members=len(inventory), records=RAW_COUNT), sort_keys=True))
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.exit(1, f'C19 build: {error}\n')


if __name__ == '__main__':
    main()
