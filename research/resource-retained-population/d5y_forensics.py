# SPDX-License-Identifier: GPL-3.0-or-later
"""Offline B1 forensics; no observer, reader or transport changes.

Reads pinned retained B1 ZIP/originals, existing native/build receipts and owned
decoders. Writes fresh ignored analysis receipts, plus small REVIEW-REQUIRED
aggregates for the separate figure generator. CPython stdlib; no native execution,
network, save, target, configuration, analysis-database or Git mutation.
Synthetic replay serializes reservations and instantaneous snapshot drains;
it is a sensitivity control, never reconstruction of lost native arrivals.
"""
import argparse
from collections import Counter, defaultdict
import csv
import ctypes
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import subprocess
import zipfile
import zlib

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / '.local-work/d5x-b1-live/attempt01'
SESSION = ROOT / '.local-work/d5x/live/session-ceb439b14ddc4db8b734526a124f1e879b64cd457774a87a6a67852fd4489894'
DOC = ROOT / 'docs/experiments/resource-retained-population'
ARCHIVE = '5f4bf02d5f1994996f1a178cc50986d22bcb91cfc9ff7a8ac41bb90cc3e75ccf'
RAW = 'cd4762095a422fb537844546e923fff667e894a63b082b0205f3107786f49a5c'
TARGET = '0:37536:20928:0029d20e'


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def load(path):
    return json.loads(Path(path).read_text(encoding='utf8'))


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def write(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n', encoding='utf8', newline='\n')


def csv_write(path, rows, fields=None):
    rows = list(rows)
    with path.open('w', encoding='utf8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields or list(rows[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


def replay(events, gap_ms, phase=0):
    """Serial ticket-equivalent capacity test; all drains are instantaneous.

    Only admitted, measured timestamps are inputs. Dropped attempts, reservation
    races, CRC work, guards and real flush placements are absent. Drain snapshots
    cannot starve and the 1024-cell/32-try policy has no contention in this model.
    """
    ticks = sorted(e['ticks'] for e in events)
    period = int(gap_ms * 10000)
    next_drain = ticks[0] + int(period*(phase or 1)) if period else ticks[0]
    used = peak = dropped = 0
    for tick in ticks:
        if not period or tick >= next_drain:
            used = 0
            if period:
                next_drain += ((tick - next_drain) // period + 1) * period
        if used == 1024:
            dropped += 1
        else:
            used += 1
            peak = max(peak, used)
    return dict(gap_ms=gap_ms, phase_fraction=phase, admitted_input_records=len(ticks), simulated_refusals=dropped,
                simulated_peak=peak, actual_dropped_attempts_included=False,
                assumption='serial reservations; instantaneous snapshot drain at periodic ticks')


def pause_replay(events, start, duration_ms):
    """One isolated writer pause; otherwise an ideal drain after every record."""
    end = start + int(duration_ms*10000)
    during = sum(start <= e['ticks'] < end for e in events)
    return dict(start_ticks=start, duration_ms=duration_ms, admitted_inputs_during_pause=during,
                simulated_refusals=max(0, during-1024), initial_backlog=0,
                assumption='one pause; otherwise instantaneous per-record drain; serial reservations')


def contributors(corpus, query):
    """Owned occupancy.py anchor search, without boundary-order assertions.

    Provenance: research/resource-query-reachability/occupancy.py SHA-256
    762a510738a6d08208fcf6ba537ca95c7aef9f107247a7baf8c74d018bcff783.
    Tests installed padded support only; does not establish retail Grid state.
    """
    qx, qy = query
    max_x = max(w-4 for w, h in corpus['source_blocks'].values())
    max_y = max(h-4 for w, h in corpus['source_blocks'].values())
    result = []
    for tx in range((qx-max_x-1)//192, (qx+2)//192+1):
        for ty in range((qy-max_y-1)//192, (qy+2)//192+1):
            tile = corpus['bodies']['0005e0de']['tiles'][f'0:{tx}:{ty}']
            assert tile[1] == 8
            for slot, (block, flags) in enumerate(corpus['patterns'][tile[0]]):
                if not flags & 8:
                    continue
                sx, sy = divmod(slot, 16)
                ax, ay = tx*192+sx*12, ty*192+sy*12
                w, h = (v-4 for v in corpus['source_blocks'][block])
                if -2 <= qx-ax < w+2 and -2 <= qy-ay < h+2:
                    result.append(f'0:{ax}:{ay}:{block}')
    return sorted(result)


def analyse(out):
    free = {}
    for drive in ('C:/', 'D:/'):
        value = ctypes.c_ulonglong()
        if not ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(drive), ctypes.byref(value), None, None):
            raise OSError('free-space query')
        free[drive] = value.value
        assert value.value > 40_000_000_000 + 20_000_000
    out.mkdir(parents=True, exist_ok=False)
    head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT).decode().strip()
    index = sha(ROOT / '.git/index')
    pins = load(BASE / 'pins.json')
    build = load(ROOT / '.local-work/d5x/build24/build.json')
    checks = {}
    for group in (pins['pins'], pins['installed'], build['inputs']):
        for name, expected in group.items():
            actual = sha(name)
            assert actual == expected, name
            checks[name] = actual
    native_pins = {
        '.local-work/d5q/export01/native.tsv': '60cc949338e9e0211b87f56c376e1a057d8b7af2da6f9e34a4ae3e84339f8fcd',
        '.local-work/d5t/export01/native.tsv': '5929be3105198c692f899199b0f4fa4703b34bcd0d58b60ab0c75ca4abf01301',
        '.local-work/d5s/export01/native.tsv': '20e9b5c653d12d4bf20a4f8983656806194525e238ff36c2eb856be4a0ca5ac0',
        '.local-work/d5x/build24/build.json': '593795452f2722606e205bd43b24c1fe1ad13ddfd4bc6e94a9e0465a18911360',
        '.local-work/d5x/qualification05/qualification.json': 'b99c54fe8cd0d97099237c0065c1d7026258cf71ccc038d42df66ce616c22f4c',
        'research/resource-query-reachability/occupancy.py': '762a510738a6d08208fcf6ba537ca95c7aef9f107247a7baf8c74d018bcff783',
        '.local-work/resources-evidence-consolidation/d5r-input-lease01/LEASE.json': '2faa4f392ac9ac8f37de7410836039cc07c07752cea054f8cac5c6fe39a2207a',
        '.local-work/resources-evidence-consolidation/d5r-input-lease01/.local-work/resource-feynman-d5/build04/normalized.json': '97aa50e0eb6bc7a2d5157bffbb311942fd84e7c01e6bd2ef3ea28a4e9bd9e0f9'}
    for name, expected in native_pins.items():
        path = ROOT / name
        assert sha(path) == expected, name
        checks[str(path)] = expected
    for name, expected in load(ROOT/'.local-work/d5x/identity05/identity.json')['database'].items():
        assert sha(name)==expected, name
        checks[name] = expected
    assert sha(pins['staging']['path']) == pins['staging']['sha256']
    assert not Path(pins['deployed']['path']).exists()
    archive = BASE / 'capture01.zip'
    assert sha(archive) == ARCHIVE
    manifest = load(BASE / 'archive01.json')
    assert manifest['sha256'] == ARCHIVE
    with zipfile.ZipFile(archive) as z:
        assert set(z.namelist()) == set(manifest['members'])
        for name, pin in manifest['members'].items():
            with z.open(name) as stream:
                assert hashlib.file_digest(stream, 'sha256').hexdigest() == pin['sha256'], name
            assert sha(pin['original']) == pin['sha256'], pin['original']
            checks[pin['original']] = pin['sha256']
    reader = module('d5y_frozen_reader', ROOT / 'runtime/construction-winner/read_capture.py')
    reporter = module('d5y_unchanged_reporter', ROOT / 'research/resource-retained-population/d5x_b1_report.py')
    raw = (SESSION / 'events.bin').read_bytes()
    assert hashlib.sha256(raw).hexdigest() == RAW
    identity = load(SESSION / 'identity.json')
    ihash = sha(SESSION / 'identity.json')
    assert ihash == '63c77387fa31ef4f0f381e27a0544371f847c13d1003c003909808d2ac3dabf1'
    events, prefixes, rolling = [], {0: 0}, 0
    for pos in range(0, len(raw), 328):
        frame = raw[pos:pos+328]
        magic, length, sequence, crc = struct.unpack_from('<4I', frame)
        e = reader.decode(frame[16:])
        assert magic == 0x31505253 and length == 312 and sequence == e['sequence'] == len(events)+1
        assert zlib.crc32(frame[16:]) == crc and e['kind'] in range(1, 14)
        rolling = zlib.crc32(frame, rolling)
        prefixes[e['sequence']] = rolling
        events.append(e)
    acks = [json.loads(line) for line in (SESSION / 'flush.jsonl').read_text().splitlines()]
    for a in acks:
        assert a['prefix_crc32'] == prefixes[a['records']] and a['identity_sha256'] == ihash
        assert a['bytes'] == a['records']*328
    terminal = load(SESSION / 'terminal.json')
    assert len(events) == terminal['acknowledged'] == terminal['written'] == terminal['enqueued'] == 19780
    assert not terminal['failed'] and terminal['drops'] == 9957
    frequency = identity['qpc_frequency']
    assert frequency == 10000000
    t0 = min(e['ticks'] for e in events)
    buckets = defaultdict(Counter)
    for e in events:
        buckets[(e['ticks']-t0)//frequency][reader.KINDS[e['kind']]] += 1
    chronology = [dict(second=s, **{k: c[k] for k in reader.KINDS[1:]}) for s, c in sorted(buckets.items())]
    csv_write(out / 'chronology.csv', chronology)
    csv_write(out / 'event-strata.csv', (dict(kind=reader.KINDS[k], thread=t, epoch=ep, records=n)
              for (k,t,ep),n in sorted(Counter((e['kind'],e['thread'],e['epoch']) for e in events).items())))
    groups, entries = defaultdict(list), defaultdict(list)
    for e in events:
        if e['kind'] == 1:
            entries[e['invocation']].append(e)
        if e['selection']:
            groups[(e['invocation'], e['selection'])].append(e)
    paths = []
    for (inv, selection), rows in groups.items():
        values = entries.get(inv, [])
        entry = values[0] if values else None
        paths.append(reporter.path_result(entry, len(values), rows, reader))
    # Include provider-only records independently of the selected groups.
    selected_inv = {i for i, _ in groups}
    for inv, values in entries.items():
        if inv not in selected_inv:
            paths.append(reporter.path_result(values[0], len(values), [], reader))
    with (out / 'paths.jsonl').open('x', encoding='utf8', newline='\n') as stream:
        for p in paths:
            stream.write(json.dumps(p)+'\n')
    copied = [e for e in events if any(bytes.fromhex(e['source_bytes']))]
    valid_copies = [e for e in copied if not e['status'] and not e['hazards'] and e['kind'] in (4,5,6,7,8,9)]
    keys = Counter(reader.source_key(e) for e in valid_copies)
    assert TARGET not in keys
    key_rows = []
    pointer_keys = defaultdict(set)
    for e in valid_copies:
        pointer_keys[e['source']].add(reader.source_key(e))
    for key, count in sorted(keys.items()):
        ee = [e for e in valid_copies if reader.source_key(e) == key]
        key_rows.append(dict(source_key=key, records=count, first_sequence=min(e['sequence'] for e in ee),
                             last_sequence=max(e['sequence'] for e in ee),
                             kinds=';'.join(sorted({reader.KINDS[e['kind']] for e in ee})),
                             allocations=len({e['source'] for e in ee})))
    csv_write(out / 'source-depth.csv', key_rows)
    write(out / 'copy-records.json', valid_copies)
    unknown_selections = [e for e in events if e['kind']==2 and e['source'] not in pointer_keys]
    diagnostic_pointer_matches = [e for e in events if e['kind']==2 and e['source'] in pointer_keys]
    pointer_rows, pointer_private = [], []
    selected_pointers = list(dict.fromkeys(e['source'] for e in events if e['kind']==2))
    for ordinal, pointer in enumerate(selected_pointers, 1):
        selected = [e for e in events if e['kind']==2 and e['source']==pointer]
        visits = [e for e in events if e['kind']==3 and e['source']==pointer]
        same_epoch = sum(any(c['kind']==4 and c['source']==pointer and c['epoch']==e['epoch']
                            and c['proc']==e['proc'] for c in valid_copies) for e in selected)
        row = dict(pointer_label=f'P{ordinal:02}', selections=len(selected),
            unique_requests=len({tuple(e['request']) for e in selected}),
            min_x=min(e['request'][0] for e in selected),max_x=max(e['request'][0] for e in selected),
            min_y=min(e['request'][1] for e in selected),max_y=max(e['request'][1] for e in selected),
            first_sequence=min(e['sequence'] for e in selected),last_sequence=max(e['sequence'] for e in selected),
            valid_selections=sum(not e['status'] and not e['hazards'] for e in selected),
            visited_bypasses=sum(bool(e['a']) for e in visits),
            qualified_bypass_pairs=sum(bool(v['a']) and not v['status'] and not v['hazards'] and
                any(s['invocation']==v['invocation'] and s['selection']==v['selection'] and
                    s['epoch']==v['epoch'] and s['proc']==v['proc'] and s['frame']==v['frame'] and
                    s['thread']==v['thread'] and not s['status'] and not s['hazards'] and
                    s['sequence']<v['sequence'] for s in selected) for v in visits),
            within_conditional_target_support=sum(-2<=e['request'][0]<12 and -2<=e['request'][1]<12 for e in selected),
            source_keys=';'.join(sorted(pointer_keys[pointer])),
            selection_same_epoch_lookup_matches=same_epoch,
            epochs=';'.join(map(str,sorted({e['epoch'] for e in selected}))))
        pointer_rows.append(row)
        pointer_private.append(dict(row,pointer=pointer))
    csv_write(out / 'pointer-envelopes.csv', pointer_rows)
    write(out / 'pointer-private.json', pointer_private)
    corpus = load(ROOT / next(n for n in native_pins if n.endswith('normalized.json')))
    if 'payload' in corpus:
        canonical = json.dumps(corpus['payload'], sort_keys=True, separators=(',', ':'), allow_nan=False).encode()
        assert hashlib.sha256(canonical).hexdigest() == corpus['sha256']
        corpus = corpus['payload']
    contributor_cache = {}
    def expected(e):
        q = tuple(e['request'])
        if q not in contributor_cache:
            contributor_cache[q] = contributors(corpus, (37536+q[0],20928+q[1]))
        return contributor_cache[q]
    control_lookups = [e for e in valid_copies if e['kind']==4]
    assert all(reader.source_key(e) in expected(e) for e in control_lookups)
    conditional = []
    for e in events:
        if e['kind']!=2 or e['status'] or e['hazards'] or expected(e)!=[TARGET]:
            continue
        matched = [v for v in groups[(e['invocation'],e['selection'])] if v['kind']==3 and
                   not v['status'] and not v['hazards'] and v['epoch']==e['epoch'] and
                   v['source']==e['source'] and v['frame']==e['frame'] and v['proc']==e['proc'] and
                   v['sequence']>e['sequence']]
        conditional.append(dict(selection_sequence=e['sequence'],visited_sequence=matched[0]['sequence'] if len(matched)==1 else None,
            pointer_label=f'P{selected_pointers.index(e["source"])+1:02}',request_x=e['request'][0],request_y=e['request'][1],
            epoch=e['epoch'],bypass=bool(len(matched)==1 and matched[0]['a']),
            attribution='CONDITIONAL installed frame/content/index; not copied source identity'))
    csv_write(out / 'conditional-target.csv', conditional)
    write(out / 'spatial-controls.json', dict(lookups=len(control_lookups),compatible=24,
        singleton_controls=sum(len(expected(e))==1 for e in control_lookups),
        conditional_singleton_selections=len(conditional),conditional_singleton_bypasses=sum(e['bypass'] for e in conditional),
        first_conditional_selection=min(e['selection_sequence'] for e in conditional),
        last_conditional_selection=max(e['selection_sequence'] for e in conditional),
        target_block_dimensions=corpus['source_blocks']['0029d20e'],
        target_pattern_entry=corpus['patterns']['0023ddf3'][128],
        necessary_unobserved_premises=['same effective descriptor at bypass invocation',
                                      'current ordinary Grid and installed content binding',
                                      'no hidden rebase/retirement/allocation substitution across loss']))
    # Pointer equality is a retrospective diagnostic only, not geographic proof.
    descriptors = []
    for e in events:
        if e['kind'] != 5 or e['status'] or e['hazards']:
            continue
        raw_d = bytes.fromhex(e['descriptor'])
        axis = lambda off: struct.unpack_from('<i', raw_d, off)[0]
        x = axis(4)*192+axis(20)*12+axis(36)
        y = axis(8)*192+axis(24)*12+axis(40)
        descriptors.append(dict(sequence=e['sequence'], chart=raw_d[0], anchor_x=x, anchor_y=y,
                                request_x=e['request'][0], request_y=e['request'][1],
                                face_x=x+e['request'][0], face_y=y+e['request'][1],
                                primary_route=e['d']==e['holder']+0xc8,
                                source_key=reader.source_key(e)))
    write(out / 'descriptors.json', descriptors)
    requests = [e for e in events if e['kind']==1 and not e['status'] and not e['hazards']]
    request_rows = [dict(x=x,y=y,records=n) for (x,y),n in sorted(Counter(tuple(e['request']) for e in requests).items())]
    csv_write(out / 'requests.csv', request_rows)
    progress = []
    previous = 0
    for i,a in enumerate(acks):
        # ACKs have no QPC; endpoint-event ticks are explicitly NOT flush times.
        progress.append(dict(ack_ordinal=i+1, records=a['records'], drops=a['drops'],
            new_reported_drops=a['drops']-previous, enqueued_snapshot=a['enqueued_snapshot'],
            dequeued_snapshot=a['dequeued_snapshot'], queue_high_water_lower_bound=a['queue_high_water_lower_bound'],
            max_flush_ms=a['max_flush_ticks']/frequency*1000,
            max_write_ms=a['max_write_ticks']/frequency*1000,
            endpoint_event_second=(events[a['records']-1]['ticks']-t0)/frequency))
        previous = a['drops']
    csv_write(out / 'writer-progress.csv', progress)
    checkpoints = []
    for name,pin in manifest['members'].items():
        if not name.startswith('checkpoints/') or not name.endswith('.json'):
            continue
        value = load(pin['original'])
        if 'qpc' in value:
            checkpoints.append(dict(name=name, phase=value['phase'], action=value['action'],
                                    second=(value['qpc']-t0)/frequency, utc=value['utc']))
    write(out / 'checkpoints.json', checkpoints)
    replays = [replay(events, gap, phase) for gap in (0,1,5,20,50,100,500,1206.5674)
               for phase in ((0,) if gap==0 else (0,0.25,0.5,0.75))]
    write(out / 'replay.json', replays)
    peak_second = max(buckets, key=lambda s:sum(buckets[s].values()))
    starts = [t0, t0+peak_second*frequency, t0+(peak_second-1)*frequency,
              min(e['ticks'] for e in events if e['sequence']>110)]
    pauses = [pause_replay(events,start,duration) for start in starts for duration in (20,287.5799,1206.5674)]
    write(out / 'isolated-pauses.json', pauses)
    # Independent original-reader output is retained without changing its rules.
    reduced = reader.reduce(events)
    write(out / 'cold-reader.json', reduced)
    result = dict(schema='sor-d5y-forensics/1', classification='REVIEW-REQUIRED aggregates; raw references LOCAL-ONLY',
        head=head,index_sha256=index,free=free,input_hashes=checks,archive_sha256=ARCHIVE,raw_sha256=RAW,
        script_sha256=sha(__file__),identity_sha256=ihash,pid=identity['pid'],creation_filetime=identity['creation_filetime'],
        qpc_frequency=frequency,t0=t0,span_seconds=(max(e['ticks'] for e in events)-t0)/frequency,
        authenticated_records=len(events),flush_prefixes=len(acks),
        kinds=Counter(reader.KINDS[e['kind']] for e in events),
        status_records=[dict(sequence=e['sequence'],kind=reader.KINDS[e['kind']],status=e['status'],epoch=e['epoch']) for e in events if e['status']],
        path_outcomes=Counter(p['outcome'] for p in paths),copied_records=len(copied),valid_copy_records=len(valid_copies),
        source_keys=key_rows,target_positive_records=0,target_first_positive=None,target_last_positive=None,
        target_deepest_stage='NO_AUTHENTICATED_GEOGRAPHIC_IDENTITY',
        selected_records=len([e for e in events if e['kind']==2]),
        selections_with_retrospective_pointer_match=len(diagnostic_pointer_matches),
        selections_without_any_copied_pointer=len(unknown_selections),
        pointer_key_conflicts={str(p):sorted(k) for p,k in pointer_keys.items() if len(k)>1},
        orphan_records=sum(e['invocation']==0 and 2<=e['kind']<=8 for e in events),
        qpc_admission_inversions=sum(a['ticks']>b['ticks'] for a,b in zip(events,events[1:])),
        provider_entries=sum(map(len,entries.values())),
        observed_invocation_tokens=len({e['invocation'] for e in events if e['invocation']}),
        threads=len({e['thread'] for e in events}),
        request_bounds=dict(x=[min(e['request'][0] for e in requests),max(e['request'][0] for e in requests)],
                            y=[min(e['request'][1] for e in requests),max(e['request'][1] for e in requests)]),
        terminal={k:v for k,v in terminal.items() if k not in identity},synthetic_replay=replays,
        isolated_pauses=pauses)
    write(out / 'analysis.json', result)
    # Rehash every read primary to establish preservation across this analysis.
    assert all(sha(name)==digest for name,digest in checks.items())
    assert sha(archive)==ARCHIVE and sha(ROOT/'.git/index')==index
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('label')
    args = parser.parse_args()
    assert args.label.replace('-', '').isalnum()
    result = analyse(ROOT / '.local-work/d5y' / args.label)
    print(json.dumps({k:v for k,v in result.items() if k not in ('input_hashes','status_records','source_keys')}, indent=2))


if __name__ == '__main__':
    main()
