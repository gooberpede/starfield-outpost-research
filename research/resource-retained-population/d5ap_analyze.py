# SPDX-License-Identifier: GPL-3.0-or-later
"""Authenticate sealed N2 inputs and extract complete recorded competition.

SOR-P-0002 source-informed reuse of owned D5AO/D5AM readers. Reads retained
seal and archive, source lock and closed raw session. Writes a fresh derivative
under .local-work/d5ap. Stdlib and existing project readers; no process, save,
deployment, analysis database or network operations. No native observer edits.
The original raw readers keep their validation; pure witness enrichment becomes
a separately queryable index. All output remains local pending review.
"""
import os
import sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):
    raise RuntimeError('Use pinned Python -E -B without optimization')

import argparse
from collections import Counter, defaultdict, deque
import csv
import ctypes
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import time
import zipfile

ROOT = Path(__file__).resolve().parents[2]
OLD = ROOT / '.local-work/d5ao/n2-live01'
SEAL = '99360972df120f7ba331bd56593b930fc881f78b6c6938230b20a3956986a3b5'
ARCHIVE = 'd7d48edf884b796865ed56ef5d5e467f381ce51ac6e6229e980a3e267cbc78af'


def require(value, message):
    if not value:
        raise ValueError(message)


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def write(path, value):
    with Path(path).open('x', encoding='utf8', newline='\n') as stream:
        json.dump(value, stream, indent=2)
        stream.write('\n')


def guard():
    floors = {}
    for drive in ('C:/', 'D:/'):
        available = ctypes.c_ulonglong()
        require(ctypes.windll.kernel32.GetDiskFreeSpaceExW(
            ctypes.c_wchar_p(drive), ctypes.byref(available), None, None), 'Disk query failed')
        require(available.value >= 40_000_000_000, 'Caller-available disk floor')
        floors[drive] = available.value
    return floors


def authenticate():
    require(sha(OLD / 'seal01.json') == SEAL, 'Seal identity changed')
    require(sha(OLD / 'N2-evidence01.zip') == ARCHIVE, 'Archive identity changed')
    seal = json.loads((OLD / 'seal01.json').read_bytes())
    def member(item):
        name, pin = item
        prefix, relative = name.split('/', 1)
        path = Path(seal['roots'][prefix]['path']) / relative
        require(path.stat().st_size == pin['size'] and sha(path) == pin['sha256'], 'Sealed member changed: ' + name)
        return name, str(path)
    with ThreadPoolExecutor(max_workers=4) as pool:
        locators = dict(pool.map(member, seal['files'].items()))
    with zipfile.ZipFile(OLD / 'N2-evidence01.zip') as archive:
        # Every evidence payload is streamed independently; no restoration writes.
        for name, pin in seal['files'].items():
            with archive.open(name) as stream:
                require(hashlib.file_digest(stream, 'sha256').hexdigest() == pin['sha256'], 'Archive member changed: ' + name)
    lock_path = OLD / 'reviewed01/d5ao-n2-source-lock.json'
    plan = json.loads((OLD / 'reviewed01/n2-plan.json').read_bytes())
    require(sha(lock_path) == plan['d5ao_n2_source_lock_sha256'], 'Source-lock binding')
    lock = json.loads(lock_path.read_bytes())
    with ThreadPoolExecutor(max_workers=4) as pool:
        actual = list(pool.map(sha, lock['sources']))
    require(all(h == expected for h, expected in zip(actual, lock['sources'].values())), 'Original source pin changed')
    require(sha(sys.executable) == lock['interpreter_sha256'], 'Pinned interpreter mismatch')
    return seal, locators, plan, dict(seal_sha256=SEAL, archive_sha256=ARCHIVE,
        sealed_members=len(locators), source_pins=len(actual), source_lock_sha256=sha(lock_path),
        interpreter=sys.executable, interpreter_sha256=sha(sys.executable), python=sys.version)


def triples(rows):
    """Pair per-thread reader/writer lifetimes without cross-thread total order."""
    pending = defaultdict(deque)
    readers = defaultdict(deque)
    held = defaultdict(list)
    result = []
    for row in rows:
        key = (row['lock'], row['generation'], row['thread'])
        kind = row['kind']
        if kind == 2:
            pending[key].append(row)
        elif kind == 3:
            require(bool(pending[key]), 'Acquisition missing pending')
            held[key].append([pending[key].popleft(), row])
        elif kind == 7:
            require(bool(held[key]), 'Final release missing acquisition')
            parts = held[key].pop()
            result.append(dict(type='writer', events=parts + [row]))
        elif kind == 5:
            readers[key].append([row])
        elif kind == 15:
            candidate = next((p for p in reversed(readers[key]) if len(p) == 1), None)
            require(candidate is not None, 'Admitted reader missing registration')
            candidate.append(row)
        elif kind == 6:
            require(bool(readers[key]), 'Reader release missing registration')
            parts = readers[key].pop()
            require(len(parts) == 2, 'Reader release missing admitted boundary')
            result.append(dict(type='reader', events=parts + [row]))
        elif kind in (4, 8):
            raise ValueError('N2 ordinary census unexpectedly contains recursive ownership')
    require(not any(pending.values()) and not any(held.values()) and not any(readers.values()), 'Open participant lifetime')
    return result


def extract(core, causal, scheduler, core_reader):
    births, publications, source_rows = {}, {}, defaultdict(list)
    contexts, entries = defaultdict(list), {}
    for row in core:
        if row['kind'] == 14:
            births[row['source']] = row
        origin = births.get(row['source'])
        if row['kind'] == 15 and origin:
            publications[(row['source'], origin['selection'])] = row
        if origin:
            source_rows[(row['source'], origin['selection'])].append(row)
        if row['kind'] == 1:
            entries[(row['thread'], row['invocation'])] = row
        if row['selection'] and row['kind'] not in (14, 15):
            contexts[(row['thread'], row['invocation'], row['selection'], row['source'])].append(row)
    target_births = [r for r in core if r['kind'] == 14 and core_reader.source_key(r) == core_reader.TARGET]
    target_rows = []
    for birth in target_births:
        rows = source_rows[(birth['source'], birth['selection'])]
        target_rows.extend((birth, row) for row in rows if row['kind'] == 2)
    providers = defaultdict(list)
    tasks = defaultdict(list)
    for row in scheduler['events']:
        tasks[(row['node'], row['allocation'])].append(row)
        if row['kind'] == 9:
            providers[(row['thread'], row['core_invocation'])].append(row)
    causal_contexts = defaultdict(list)
    for row in causal['events']:
        causal_contexts[(row['thread'], row['invocation'], row['selection'], row['source'])].append(row)
    task_histories = {(h['node'], h['allocation']): h for h in scheduler['histories']}
    contenders = []
    for birth, selected in target_rows:
        key = (selected['thread'], selected['invocation'], selected['selection'], selected['source'])
        origin = entries[key[:2]]
        matches = providers[key[:2]]
        require(len(matches) == 1, 'Missing or duplicate typed provider')
        provider = matches[0]
        task_key = (provider['node'], provider['allocation'])
        stages = tasks[task_key]
        require(not task_histories[task_key]['issues'], 'Unqualified task history')
        require(all(not r['status'] and not r['hazards'] for r in stages), 'Task uncertainty')
        require({r['kind'] for r in stages} >= set(range(1, 13)), 'Missing task stages')
        require(provider['request'] == origin['request'], 'Original task/provider request mismatch')
        path, locks = contexts[key], causal_contexts[key]
        require(all(not r['status'] and not r['hazards'] for r in path + locks), 'Core/lock uncertainty')
        visited = [r for r in path if r['kind'] == 3]
        require(len(visited) == 1, 'Missing/duplicate target visited decision')
        pub = publications[(birth['source'], birth['selection'])]
        require(birth['sequence'] < pub['sequence'] < selected['sequence'], 'Source publication join')
        require(birth['thread'] == pub['thread'], 'Source constructor/publication mismatch')
        lookups = [r for r in path if r['kind'] == 4]
        outcome = ('MISS' if lookups[0]['a'] == lookups[0]['b'] else 'HIT') if lookups else 'VISITED_BYPASS'
        contenders.append(dict(task=provider['allocation'], node=provider['node'], family=provider['family'],
            invocation=selected['invocation'], selection=selected['selection'], thread=selected['thread'],
            request=origin['request'], source=selected['source'], source_allocation=birth['selection'],
            source_birth=birth['sequence'], source_publication=pub['sequence'], owner=selected['proc'],
            frame=selected['frame'], outcome=outcome, scheduler=stages, core=path, causal=locks))
    require(len({r['task'] for r in contenders}) == len(contenders), 'Target task ABA/duplicate selection')
    return contenders, target_births


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    floors = guard()
    out = args.out.absolute()
    require(out.resolve().is_relative_to(ROOT / '.local-work/d5ap'), 'Fresh D5AP-local output required')
    require(not any(p.is_symlink() or p.is_junction() for p in (out, *out.parents)), 'No reparse output')
    out.mkdir(parents=True, exist_ok=False)
    start = time.perf_counter()
    snapshots = out / 'sources'
    snapshots.mkdir()
    for path in Path(__file__).parent.glob('d5ap_*.py'):
        with (snapshots / path.name).open('xb') as stream:
            stream.write(path.read_bytes())
    seal, locators, plan, auth = authenticate()
    write(out / 'authentication.json', dict(**auth, floors=floors, locators=locators))
    session = Path(seal['roots']['raw']['path'])
    sys.path.insert(0, str(ROOT / 'runtime/construction-winner'))
    import read_capture as core_reader
    import d5an_read_causal as causal_reader
    import d5am_read_scheduler as scheduler_reader
    import d5ai_read_lifetime as lifetime_reader
    import d5ai_read_geometry as geometry_reader
    import d5an_read_counter as counter_reader
    from d5ap_windows import HistoryIndex
    # Replace only the pure enrichment seam. Original validators run unaltered.
    indexes = []
    def indexed(rows, issues):
        index = HistoryIndex(rows, issues)
        indexes.append(index)
        return index.export()
    causal_reader.registration_windows = indexed
    scientific = core_reader.inspect(session, plan['dll_sha256'])
    require(scientific['complete_session'] and not scientific['damage'], 'Core incomplete or damaged')
    causal = causal_reader.read(session, plan['dll_sha256'])
    scheduler = scheduler_reader.read(session, plan['dll_sha256'])
    require(causal['sidecar_accounting_complete'] and causal['native_bridge_accounting_complete'], 'Causal accounting')
    require(scheduler['byte_accounting_complete'] and scheduler['native_bridge_accounting_complete'], 'Scheduler accounting')
    require(not causal['reasons'] and all(not h['issues'] for h in causal['histories']), 'Owner history qualification')
    lifetime = lifetime_reader.read_prefix(session, scientific['terminal'])
    geometry = geometry_reader.read_session(session)
    counter = counter_reader.read(session, plan['dll_sha256'], plan['dll'])
    require(lifetime['complete'] and not lifetime['loss'] and not geometry['errors'] and counter['complete'], 'Content/counter qualification')
    import d5aj_reduce
    source_proof = d5aj_reduce.inspect(session, plan['dll_sha256'], core_reader.TARGET, 0x5e0de)
    require(len(source_proof['observations']) == 1 and not source_proof['refused'], 'Source/frame/lifetime attribution')
    write(out / 'source-proof.json', source_proof)
    raw = (session / 'events.bin').read_bytes()
    core = [core_reader.decode(raw[i + 16:i + 328]) for i in range(0, len(raw), 328)]
    contenders, births = extract(core, causal, scheduler, core_reader)
    winners = [r for r in contenders if r['outcome'] == 'MISS']
    require(len(winners) == 1, 'Single target construction assumption')
    winner = winners[0]
    participants = triples(causal['events'])
    write(out / 'contenders.json', contenders)
    write(out / 'participants.json', participants)
    write(out / 'core.json', core)
    write(out / 'causal.json', causal)
    write(out / 'scheduler.json', scheduler)
    write(out / 'content.json', dict(lifetime=lifetime, geometry=geometry, counter=counter, scientific=scientific))
    stage_ranks = {}
    for kind in (1, 2, 5, 3, 10, 7, 9):
        w = next(e for e in winner['scheduler'] if e['kind'] == kind)
        stage_ranks[scheduler_reader.KINDS[kind]] = dict(sequence=w['sequence'], ticks=w['ticks'],
            strictly_earlier=sum(min(e['ticks'] for e in c['scheduler'] if e['kind'] == kind) < w['ticks'] for c in contenders),
            equal=sum(min(e['ticks'] for e in c['scheduler'] if e['kind'] == kind) == w['ticks'] for c in contenders))
    fields = ['task', 'family', 'request', 'invocation', 'selection', 'thread', 'source_allocation', 'outcome']
    stage_names = [(1, 'publication'), (2, 'activation'), (5, 'ready_approach'), (3, 'dispatch'),
                   (11, 'queue_before'), (12, 'queue_return'), (10, 'claim_return'), (7, 'callback'),
                   (9, 'provider'), (8, 'callback_end'), (4, 'retirement')]
    with (out / 'contenders.csv').open('x', encoding='utf8', newline='') as stream:
        labels = fields + [n + suffix for _, n in stage_names for suffix in ('_witness', '_ticks')] + ['core_witnesses', 'causal_witnesses']
        writer = csv.DictWriter(stream, fieldnames=labels, lineterminator='\n')
        writer.writeheader()
        for contender in contenders:
            row = {k: contender[k] for k in fields}
            for kind, name in stage_names:
                values = [r for r in contender['scheduler'] if r['kind'] == kind]
                row[name + '_witness'] = ' '.join(str(r['sequence']) for r in values)
                row[name + '_ticks'] = ' '.join(str(r['ticks']) for r in values)
            row['core_witnesses'] = ' '.join(str(r['sequence']) for r in contender['core'])
            row['causal_witnesses'] = ' '.join(str(r['sequence']) for r in contender['causal'])
            writer.writerow(row)
    query_start = time.perf_counter()
    counts = Counter()
    for index in indexes:
        for relationship in index.iter_legacy():
            counts[relationship['interpretation']] += 1
    write(out / 'summary.json', dict(schema='sor-d5ap-analysis/1', authentication=auth,
        source_sha256=sha(__file__), windows_sha256=sha(Path(__file__).with_name('d5ap_windows.py')),
        target_births=[dict(sequence=r['sequence'], allocation=r['selection'], source=r['source']) for r in births],
        contender_count=len(contenders), outcomes=dict(Counter(c['outcome'] for c in contenders)),
        family_counts=dict(Counter(c['family'] for c in contenders)), winner_task=winner['task'],
        winner_invocation=winner['invocation'], stage_ranks=stage_ranks,
        participants=dict(Counter(p['type'] for p in participants)),
        core_records=len(core), causal_records=len(causal['events']), scheduler_records=len(scheduler['events']),
        lifetime_records=lifetime['records'], pair_classes=dict(counts),
        all_writer_query_seconds=time.perf_counter()-query_start, total_seconds=time.perf_counter()-start,
        outputs={p.name: sha(p) for p in out.iterdir() if p.is_file()}))
    print(json.dumps(json.loads((out / 'summary.json').read_bytes()), indent=2))


if __name__ == '__main__':
    main()
