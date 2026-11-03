# SPDX-License-Identifier: GPL-3.0-or-later
"""Authenticate three retained recordings and derive bounded D5AM chronology.

Reads immutable local seals, ZIPs, original recordings and owned readers. Writes
exclusive new files below a caller-supplied local output directory. No process,
save, deployment, network or analysis-project contact. Stdlib only. SOR-P-0002
covers source-informed reuse of this repository's core/geometry/lifetime readers;
the output records exact source hashes. Missing historical stages stay unknown.
"""
import sys
import os
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):
    raise RuntimeError('Python optimization is forbidden; invoke with -E -B')
import argparse
from collections import Counter
import ctypes
import csv
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import zipfile
import zlib

ROOT = Path(__file__).resolve().parents[2]
TARGET = '0:37536:20928:0029d20e'
CASES = (
    ('B2', '.local-work/d5ab/B2-APPROVED-002-archive', 'capture.zip',
     'f472f69b85e37a4715c1d713e91387e80d20d3518fc66a5b42b9709e0e733d88'),
    ('A', '.local-work/d5ak/a-live01-archive', 'episode-a.zip',
     'fe4bdbcfda8b0689e39444afbef5e9094cd78739787cc4fe2dfc7fd777bd9509'),
    ('B', '.local-work/d5al/b-live01-archive', 'episode-b.zip',
     '7ada51002e4311c6db49001f49e8c34b59aea6698eabbcb37473c67719ac19e5'))
NAMES = 'sequence kind invocation parent thread ticks epoch hazards status proc source frame holder a b c d selection'.split()
KINDS = 'unused entry selected visited lookup descriptor generating sample generated returned fence_begin fence_end cold ready birth published reserve stored'.split()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


def dump(path, value):
    guard()
    with path.open('x', encoding='utf8', newline='\n') as stream:
        json.dump(value, stream, indent=2)
        stream.write('\n')


def frames(data):
    require(len(data) % 328 == 0, 'Torn core frame')
    rows = []
    for offset in range(0, len(data), 328):
        magic, size, low, crc = struct.unpack_from('<4I', data, offset)
        raw = data[offset + 16:offset + 328]
        e = dict(zip(NAMES, struct.unpack_from('<18Q', raw)))
        require((magic, size, low, e['sequence'], zlib.crc32(raw)) ==
                (0x31505253, 312, len(rows) + 1, len(rows) + 1, crc), 'Core frame integrity')
        require(1 <= e['kind'] <= 17, 'Unknown event kind')
        e.update(request=list(struct.unpack_from('<2i', raw, 144)),
                 source_bytes=raw[152:264].hex(), descriptor=raw[264:308].hex())
        rows.append(e)
    return rows


def source_key(e):
    raw = bytes.fromhex(e['source_bytes'])
    x = sum(struct.unpack_from('<i', raw, o)[0] * m for o, m in ((0x3c, 192), (0x4c, 12), (0x5c, 1)))
    y = sum(struct.unpack_from('<i', raw, o)[0] * m for o, m in ((0x40, 192), (0x50, 12), (0x60, 1)))
    return f'{raw[0x38]}:{x}:{y}:{struct.unpack_from("<I", raw)[0]:08x}'


def authenticate(folder, archive_name, expected_zip):
    seal_bytes = (folder / 'seal.json').read_bytes()
    seal = json.loads(seal_bytes)
    archive = folder / archive_name
    require(sha(archive.read_bytes()) == expected_zip, 'Archived ZIP pin mismatch')
    verified = {}
    with zipfile.ZipFile(archive) as zipped:
        names = zipped.namelist()
        require(len(names) == len(set(names)) and set(names) == set(seal['files']) | {'SOR-MANIFEST.json'},
                'Archive census mismatch')
        require(json.loads(zipped.read('SOR-MANIFEST.json')) == seal, 'Embedded manifest mismatch')
        for name, pin in seal['files'].items():
            alias, relative = name.split('/', 1)
            path = Path(seal['roots'][alias]['path']) / relative
            raw = path.read_bytes()
            require(len(raw) == pin['size'] and sha(raw) == pin['sha256'], 'Original pin mismatch: ' + name)
            require(zipped.read(name) == raw, 'Archive/original byte difference: ' + name)
            verified[str(path)] = dict(size=len(raw), sha256=sha(raw))
    return seal, verified, dict(seal_sha256=sha(seal_bytes), archive_sha256=expected_zip,
                               payload_files=len(verified), payload_bytes=sum(p['size'] for p in verified.values()))


def table(path, rows):
    if not rows:
        return
    guard()
    with path.open('x', encoding='utf8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


def guard():
    """SOR-P-0002: retain d5ae_baseline.guard's caller-available disk floors."""
    result = {}
    for drive in ('C:/', 'D:/'):
        free = ctypes.c_ulonglong()
        if not ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(drive), ctypes.byref(free), None, None):
            raise OSError('Free-space query failed')
        if free.value < 40_000_000_000:
            raise RuntimeError('Free-space floor violated')
        result[drive] = free.value
    return result


def owner_context(events, proc, left, right):
    """Conservatively include whole observed provider intervals at both edges.

    QPC sampling precedes recorder reservation. Use the union of QPC and
    reservation overlap, including ties and incomplete/contradictory endpoints.
    These are provider callback intervals, never measured lock occupancy.
    """
    groups = {}
    for event in events:
        if event['invocation']:
            groups.setdefault(event['invocation'], []).append(event)
    low, high = sorted((left['sequence'], right['sequence']))
    early, late = sorted((left['ticks'], right['ticks']))
    participants, context = [], []
    for invocation, rows in groups.items():
        if not any(e['proc'] == proc for e in rows):
            continue
        entry = [e for e in rows if e['kind'] == 1]
        returned = [e for e in rows if e['kind'] == 9]
        known = (len(entry) == len(returned) == 1 and entry[0]['sequence'] < returned[0]['sequence'] and
                 entry[0]['ticks'] <= returned[0]['ticks'])
        sequence_overlap = known and entry[0]['sequence'] <= high and returned[0]['sequence'] >= low
        qpc_overlap = known and entry[0]['ticks'] <= late and returned[0]['ticks'] >= early
        if not (not known or sequence_overlap or qpc_overlap):
            continue
        a, b = (entry[0], returned[0]) if known else (None, None)
        participants.append(dict(invocation=invocation, thread=rows[0]['thread'],
            entry=a['sequence'] if a else 'UNKNOWN', returned=b['sequence'] if b else 'UNKNOWN',
            entry_ticks=a['ticks'] if a else 'UNKNOWN', returned_ticks=b['ticks'] if b else 'UNKNOWN',
            sequence_overlap=bool(sequence_overlap), qpc_overlap=bool(qpc_overlap), endpoints='KNOWN_CALLBACKS' if known else 'UNKNOWN',
            left_sequence_crossing=bool(known and a['sequence'] < low <= b['sequence']),
            right_sequence_crossing=bool(known and a['sequence'] <= high < b['sequence']),
            left_qpc_crossing=bool(known and a['ticks'] < early <= b['ticks']),
            right_qpc_crossing=bool(known and a['ticks'] <= late < b['ticks']),
            context_records=len(rows)))
        context.extend(rows)
    # Preserve orphan observations in either window without inventing a caller.
    context.extend(e for e in events if not e['invocation'] and e['proc'] == proc and
                   (low <= e['sequence'] <= high or early <= e['ticks'] <= late))
    return sorted(context, key=lambda e: e['sequence']), participants


def safe_owner_event(label, event, target_source):
    return dict(episode=label, sequence=event['sequence'], kind=KINDS[event['kind']], invocation=event['invocation'],
        selection=event['selection'], thread=event['thread'], ticks=event['ticks'], target=event['source'] == target_source,
        source_allocation=event['source_allocation'], geographic_source=event['geographic_source'],
        request_x=event['request'][0], request_y=event['request'][1], status=event['status'], hazards=event['hazards'])


def review_tables(out, target_events, contenders, coverage, owner_events, context_events, participants, windows):
    """Emit reproducible safe review CSVs; never copy raw pointers or payloads."""
    out.mkdir(exist_ok=False)
    active = [row for row in contenders if row['outcome'] != 'visited_bypass']
    keys = {(row['episode'], row['invocation']) for row in active}
    selected = [{key: value for key, value in row.items() if key != 'descriptor_words'} for row in target_events
                if (row['episode'], row['invocation']) in keys or row['kind'] in ('birth', 'published')]
    census = []
    for window in windows:
        label = window['label']
        current = [row for row in owner_events if row['episode'] == label]
        interval = [row for row in current if window['left'] <= row['sequence'] <= window['right']]
        scoped = [row for row in participants if row['episode'] == label]
        census.append(dict(episode=label, all_target_contenders=sum(r['episode'] == label for r in contenders),
            unvisited_contenders=sum(r['episode'] == label for r in active),
            visited_bypasses=sum(r['episode'] == label and r['outcome'] == 'visited_bypass' for r in contenders),
            owner_recorded_activity=len(current), contested_begin=window['left'], contested_end=window['right'],
            contested_owner_records=len(interval), contested_invocations=len({r['invocation'] for r in interval}),
            contested_sources=len({r['source_allocation'] for r in interval if r['source_allocation'] != 'UNKNOWN'}),
            whole_context_invocations=len(scoped), whole_context_records=sum(r['context_records'] for r in scoped),
            left_sequence_crossings=sum(r['left_sequence_crossing'] for r in scoped),
            right_sequence_crossings=sum(r['right_sequence_crossing'] for r in scoped),
            left_qpc_crossings=sum(r['left_qpc_crossing'] for r in scoped),
            right_qpc_crossings=sum(r['right_qpc_crossing'] for r in scoped),
            unknown_endpoints=sum(r['endpoints'] == 'UNKNOWN' for r in scoped)))
    table(out / 'd5am-retail-contenders.csv', active)
    table(out / 'd5am-retail-events.csv', selected)
    table(out / 'd5am-retail-coverage.csv', [dict(row, event_kinds=row['event_kinds'].replace(';', ' | ')) for row in coverage])
    table(out / 'd5am-retail-owner-events.csv', context_events)
    table(out / 'd5am-retail-owner-participants.csv', participants)
    table(out / 'd5am-retail-census.csv', census)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    args.out = args.out.absolute()
    require(args.out.resolve().is_relative_to(ROOT / '.local-work/d5am'), 'Fresh D5AM-local output required')
    require(not any(p.is_symlink() or p.is_junction() for p in (args.out, *args.out.parents)), 'Reparse output path')
    free_before = guard()
    args.out.mkdir(parents=True, exist_ok=False)
    sys.path.insert(0, str(ROOT / 'runtime/construction-winner'))
    core = module('d5am_core_reader', ROOT / 'runtime/construction-winner/read_capture.py')
    geo = module('d5am_geometry_reader', ROOT / 'runtime/construction-winner/d5ai_read_geometry.py')
    life = module('d5am_lifetime_reader', ROOT / 'runtime/construction-winner/d5ai_read_lifetime.py')
    results, allpins, public_events, contenders, coverage, owner_events = [], {}, [], [], [], []
    context_events, participants, windows = [], [], []
    for case, relative, archive_name, zip_pin in CASES:
        seal, pins, auth = authenticate(ROOT / relative, archive_name, zip_pin)
        allpins.update(pins)
        session = Path(seal['roots']['raw']['path'])
        identity = json.loads((session / 'identity.json').read_bytes())
        terminal = json.loads((session / 'terminal.json').read_bytes())
        checked = core.inspect(session, identity['dll_sha256'])
        require(checked['complete_session'] and not checked['damage'] and not terminal['drops'], 'Incomplete core')
        events = frames((session / 'events.bin').read_bytes())
        births, selections, by_invocation = {}, {}, {}
        target_sources = {}
        for e in events:
            by_invocation.setdefault(e['invocation'], []).append(e)
            if e['kind'] == 14:
                births[e['source']] = e
                if source_key(e) == TARGET:
                    target_sources[e['selection']] = e
            origin = births.get(e['source'])
            e['source_allocation'] = origin['selection'] if origin else 'UNKNOWN'
            e['geographic_source'] = source_key(origin) if origin else 'UNKNOWN'
        generations = []
        for alloc, birth in target_sources.items():
            # Candidate events are bounded by the next birth at the same address.
            later = [e['sequence'] for e in events if e['kind'] == 14 and e['source'] == birth['source'] and e['sequence'] > birth['sequence']]
            upper = min(later, default=len(events) + 1)
            target = [e for e in events if birth['sequence'] <= e['sequence'] < upper and e['source'] == birth['source']]
            generated = [e for e in target if e['kind'] == 6]
            for generator in generated:
                label = 'B2' if case == 'B2' else ('A0' if len(generations) == 0 else 'A1') if case == 'A' else 'B0'
                generations.append(dict(label=label, allocation=alloc, birth=birth['sequence'],
                                        published=[e['sequence'] for e in target if e['kind'] == 15],
                                        generation=generator['sequence'], invocation=generator['invocation'],
                                        owner_formid=f"0x{generator['a']:08x}", epoch=generator['epoch']))
                invocations = sorted({e['invocation'] for e in target if e['kind'] == 2 and e['invocation']})
                proc = generator['proc']
                for invocation in invocations:
                    rows = [e for e in target if e['invocation'] == invocation]
                    entry = next((e for e in by_invocation[invocation] if e['kind'] == 1), None)
                    visited = [e for e in rows if e['kind'] == 3]
                    lookups = [e for e in rows if e['kind'] == 4]
                    outcome = 'constructed' if any(e['kind'] == 6 for e in rows) else 'map_hit' if lookups else 'visited_bypass' if visited and all(e['a'] for e in visited) else 'unknown'
                    contenders.append(dict(episode=label, allocation=alloc, invocation=invocation,
                        thread=rows[0]['thread'], request_x=entry['request'][0] if entry else 'UNKNOWN',
                        request_y=entry['request'][1] if entry else 'UNKNOWN',
                        entry=entry['sequence'] if entry else 'UNKNOWN', entry_ticks=entry['ticks'] if entry else 'UNKNOWN',
                        returned=';'.join(str(e['sequence']) for e in by_invocation[invocation] if e['kind'] == 9),
                        selected=';'.join(str(e['sequence']) for e in rows if e['kind'] == 2),
                        visited=';'.join(str(e['sequence']) for e in visited), lookup=';'.join(str(e['sequence']) for e in lookups), outcome=outcome))
                for e in target:
                    if e['kind'] in (14, 15) or e['invocation'] in invocations:
                        public_events.append(dict(episode=label, allocation=alloc, sequence=e['sequence'], kind=KINDS[e['kind']],
                            invocation=e['invocation'], selection=e['selection'], parent=e['parent'], thread=e['thread'],
                            ticks=e['ticks'], epoch=e['epoch'], status=e['status'], hazards=e['hazards'],
                            request_x=e['request'][0], request_y=e['request'][1],
                            result=e['a'] if e['kind'] in (3, 4, 7, 16) else '',
                            capacity=e['b'] if e['kind'] == 4 else '',
                            descriptor_words=';'.join(str(v) for v in struct.unpack_from('<10i', bytes.fromhex(e['descriptor']), 4)) if e['kind'] == 5 else ''))
                # Every recorded same-ProcGen event through this source generation's
                # observed activity, including unrelated source selections. These
                # are possible participants, never a complete lock-holder census.
                first = min(e['sequence'] for invocation in invocations for e in by_invocation[invocation] if e['kind'] == 1)
                last = max(e['sequence'] for e in target if e['kind'] in (3, 4, 17))
                owner_rows = [e for e in events if e['proc'] == proc and first <= e['sequence'] <= last and e['kind'] not in (10, 11)]
                for e in owner_rows:
                    owner_events.append(safe_owner_event(label, e, birth['source']))
                active_invocations = {e['invocation'] for e in target if e['kind'] == 3 and not e['a']}
                starts = [e for invocation in active_invocations for e in by_invocation[invocation] if e['kind'] == 1]
                finishes = [e for e in target if e['kind'] == 4 and e['invocation'] in active_invocations]
                # The reservation endpoints and QPC envelope are independently
                # bounded; a cross-thread inversion must not shrink either one.
                left = dict(min(starts, key=lambda e: e['sequence']), ticks=min(e['ticks'] for e in starts))
                right = dict(max(finishes, key=lambda e: e['sequence']), ticks=max(e['ticks'] for e in finishes))
                context, scoped = owner_context(events, proc, left, right)
                context_events.extend(safe_owner_event(label, e, birth['source']) for e in context)
                participants.extend(dict(episode=label, **row) for row in scoped)
                windows.append(dict(label=label, left=left['sequence'], right=right['sequence'],
                                    left_ticks=left['ticks'], right_ticks=right['ticks']))
                for stage, state, kinds in (
                    ('registration/eligibility/readiness/dispatch/worker_claim', 'NOT INSTRUMENTED', ''),
                    ('provider_entry/return', 'OBSERVED CALLBACK; return event precedes wrapper return', 'entry;returned'),
                    ('source_selection/visited_decision', 'OBSERVED CALLBACK; shared unlock timing UNKNOWN', 'selected;visited'),
                    ('visited_callback_return/shared_release', 'NOT INSTRUMENTED', ''),
                    ('exclusive_pending/acquired/released', 'NOT INSTRUMENTED; lookup inside held interval only', ''),
                    ('protected_lookup/generation/sample/store', 'OBSERVED; insertion native-implied', 'lookup;descriptor;generating;sample;generated;reserve;stored'),
                    ('owner-wide_readers/writers', 'PARTIAL provider boundary coverage only; other lock calls UNKNOWN', ''),
                    ('complete_geometry', 'NOT INSTRUMENTED' if case == 'B2' else 'AUTHENTICATED Raw2; frame/lifetime qualification separate', '')):
                    coverage.append(dict(episode=label, stage=stage, availability=state, event_kinds=kinds))
        geometry_summary, lifetime_summary = [], None
        if case != 'B2':
            geometry = geo.read_session(session)
            require(not geometry['errors'], 'Geometry reader errors')
            journal = life.read_prefix(session, terminal)
            require(journal['records'] == terminal['lifetime_written'] and not journal['open_intervals'], 'Lifetime census')
            for snapshot in geometry['snapshots']:
                qualification = life.qualify_snapshot(snapshot, journal)
                header = snapshot['header']
                geometry_summary.append(dict(snapshot=header['snapshot'], request=header['request'], raw_sha256=snapshot['sha256'],
                    holders=header['holders'], resources=header['resources'], regions=header['regions'], points=header['points'],
                    complete=snapshot['complete_representation'], header=header, lifetime=qualification))
            lifetime_summary = {k: journal[k] for k in ('records', 'prefix_bytes', 'raw_prefix_sha256', 'qualified_from_ticks', 'qualified_through_ticks', 'unlogged_cutoff_ticks')}
            dump(args.out / (case + '-lifetimes.json'), journal)
        dump(args.out / (case + '-events.json'), events)
        results.append(dict(case=case, session=str(session), identity_sha256=checked['identity_sha256'],
            pid=identity['pid'], creation_filetime=identity['creation_filetime'], dll_sha256=identity['dll_sha256'],
            host_sha256=identity['host_sha256'], qpc_frequency=identity['qpc_frequency'], raw_sha256=checked['raw_sha256'],
            complete_session=checked['complete_session'], records=len(events), kinds=dict(Counter(KINDS[e['kind']] for e in events)),
            archive=auth, identity=identity, terminal=terminal, generations=generations,
            geometry=geometry_summary, lifetime=lifetime_summary))
    # Verify all original bytes again after every decoding pass.
    for path, pin in allpins.items():
        raw = Path(path).read_bytes()
        require(len(raw) == pin['size'] and sha(raw) == pin['sha256'], 'Original changed during analysis')
    source_paths = [Path(__file__), ROOT / 'runtime/construction-winner/read_capture.py',
                    ROOT / 'runtime/construction-winner/d5ai_read_geometry.py', ROOT / 'runtime/construction-winner/d5ai_read_lifetime.py',
                    ROOT / 'runtime/construction-winner/reduce_v3.py', ROOT / 'runtime/construction-winner/reduce_v4.py']
    dump(args.out / 'summary.json', dict(schema='sor-d5am-chronology/1', sessions=results,
        originals_verified_before_after=len(allpins), free_before=free_before, free_after=guard(),
        sources={str(p):sha(p.read_bytes()) for p in source_paths},
        missing='Native task, lock admission and callback-return stages were never captured; no decode can recover them.'))
    dump(args.out / 'protected-inventory.json', allpins)
    table(args.out / 'target-events.csv', public_events)
    table(args.out / 'contenders.csv', contenders)
    table(args.out / 'coverage.csv', coverage)
    table(args.out / 'owner-events.csv', owner_events)
    table(args.out / 'owner-context-events.csv', context_events)
    table(args.out / 'owner-participants.csv', participants)
    dump(args.out / 'owner-windows.json', windows)
    review_tables(args.out / 'review-tables', public_events, contenders, coverage, owner_events, context_events, participants, windows)
    print(json.dumps(dict(sessions=[dict(case=r['case'], records=r['records'], generations=r['generations']) for r in results],
                          protected_files=len(allpins), target_events=len(public_events), contenders=len(contenders), owner_events=len(owner_events))))


if __name__ == '__main__':
    main()
