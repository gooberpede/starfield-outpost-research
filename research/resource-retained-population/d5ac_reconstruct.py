# SPDX-License-Identifier: GPL-3.0-or-later
"""Reconstruct preserved B2 events offline, without changing qualification.

Reads the pinned attempt-002 session and owned schema-4 reader/reducer. Writes
exclusive JSON/CSV derivatives below .local-work/d5ac. Requires Python -E -B
and stdlib only. No game, save, configuration, database, network or Git writes.
Frame decoding is independently checked against the existing owned decoder;
CRC and SHA authenticate bytes, not native semantics. SOR-P-0002 lineage:
d5ab_b2_analyze.py and read_capture.py.
"""
import sys
if not __debug__ or sys.flags.optimize:
    raise RuntimeError('Invoke Python with -E -B')
import argparse
from collections import Counter
import csv
import hashlib
import json
from pathlib import Path
import struct
import zlib

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'runtime/construction-winner'))
import read_capture as reader

RAW_SHA = '4a8feb68f667f417967a0cd4a332cefde768658d254ead8d555b3e5f44515218'
DLL_SHA = '9d2f0bab159f3ec23186426fb4833eb645578d2a43612bb2e8def6b1af455dcc'
SESSION = ROOT / '.local-work/d5x/live/session-5ed302aea9da7dc2261163b3dd1816e670a3c2f39891f1ec8d20094afa72b3a1'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def decode_frames(raw):
    if hashlib.sha256(raw).hexdigest() != RAW_SHA:
        raise ValueError('Raw identity mismatch')
    if len(raw) % 328:
        raise ValueError('Partial frame')
    events = []
    # Explicit offsets provide a cross-check of the packaged decoder layout.
    fields = 'sequence kind invocation parent thread ticks epoch hazards status proc source frame holder a b c d selection'.split()
    for offset in range(0, len(raw), 328):
        magic, size, seq, crc = struct.unpack_from('<IIII', raw, offset)
        payload = raw[offset + 16:offset + 328]
        if (magic, size, seq) != (0x31505253, 312, len(events) + 1) or zlib.crc32(payload) != crc:
            raise ValueError(f'Invalid frame at {offset}')
        e = {name: int.from_bytes(payload[i*8:i*8+8], 'little') for i, name in enumerate(fields)}
        e.update(request=[int.from_bytes(payload[x:x+4], 'little', signed=True) for x in (144, 148)],
                 source_bytes=payload[152:264].hex(), descriptor=payload[264:308].hex())
        if e != reader.decode(payload) or e['sequence'] != seq:
            raise ValueError('Decoder disagreement')
        events.append(e)
    return events


def reconstruct(events):
    transitions = []
    # Increment-causing records are fence begin and non-reset fence end.
    # Inherited invocation epochs are deliberately excluded from this accounting.
    previous = 1
    open_calls = {}
    for e in events:
        if e['kind'] in (10, 11):
            key = e['thread'], e['proc'], e['a']
            if e['kind'] == 10:
                assert key not in open_calls and e['hazards']==1 and not e['status']
                open_calls[key]=e
            else:
                begin=open_calls.pop(key)
                assert begin['ticks'] < e['ticks'] and e['hazards']==0 and not e['status']
                if e['a']==0:
                    assert e['epoch']==begin['epoch']
        if e['kind'] == 10 or (e['kind'] == 11 and e['a'] != 0):
            transitions.append(dict(e, before=previous, after=e['epoch'], reason=f"fence-{e['a']}-{'begin' if e['kind']==10 else 'end'}"))
            previous = e['epoch']
    assert not open_calls
    return transitions


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('out', type=Path)
    args = p.parse_args()
    if not args.out.resolve().is_relative_to(ROOT / '.local-work/d5ac'):
        raise ValueError('Output must remain local')
    raw = (SESSION / 'events.bin').read_bytes()
    events = decode_frames(raw)
    result = reader.inspect(SESSION, DLL_SHA)
    historical = json.loads((ROOT / '.local-work/d5ab/B2-APPROVED-002-notes/reader.json').read_bytes())
    assert result == historical and result['complete_session'] and not result['damage']
    assert len(events) == 32141
    transitions = reconstruct(events)
    assert all(e['after'] == e['before'] + 1 for e in transitions)
    assert all(a['ticks'] < b['ticks'] for a,b in zip(transitions,transitions[1:]))
    keys = {(e['invocation'], e['selection']) for e in events if e['sequence'] in (8006, 8020)}
    invocations = {i for i, _ in keys}
    sources = {e['source'] for e in events if e['sequence'] in (8006, 8020)}
    target = [e for e in events if e['invocation'] in invocations or (e['source'] in sources and e['kind'] in (4, 14, 15))]
    resets = [e for e in events if e['kind'] == 12 or (e['kind'] in (10, 11) and e['a'] == 0)]
    # Separate hypothetical native-state oracle, never a schema-4 certificate.
    # Sufficiency depends on the separately audited ordinary native mutator graph.
    anchor, first = events[882], next(e for e in events if e['kind']==1)
    interval = [e for e in events if anchor['ticks'] < e['ticks'] < first['ticks']]
    assert anchor['kind']==11 and anchor['epoch']==113 and first['epoch']==207
    assert first['proc']==anchor['proc']
    assert not any(e['kind'] in (1,4,16,17) for e in interval)
    assert all(e['a']==3 for e in interval if e['kind'] in (10,11))
    assert not any(e['status'] or e['hazards'] for e in events if e['sequence'] in (8006,8020,8091,8106,8339))
    scope = dict(anchor_sequence=883, last_clear_sequence=1731, first_entry_sequence=first['sequence'],
                 proc=first['proc'], intervening_clears=sum(e['kind']==10 for e in interval),
                 no_provider_or_append_observed=True,
                 qualification='Derived empty-state continuity under ordinary native mutator coverage; NOT a production certificate; target has prior eligible decision.')
    malformed = []
    for name, bad in [('truncated', raw[:-1]), ('changed-byte', raw[:100]+bytes([raw[100]^1])+raw[101:]), ('missing-frame',raw[328:])]:
        try:
            decode_frames(bad)
        except ValueError:
            malformed.append(dict(case=name, rejected=True))
        else:
            raise AssertionError(name)
    args.out.mkdir(parents=True, exist_ok=False)
    def write(name, value):
        (args.out / name).write_text(json.dumps(value, indent=2)+'\n', encoding='utf-8', newline='\n')
    write('target.json', target)
    write('resets.json', resets)
    write('transitions.json', transitions)
    write('carried-empty-oracle.json', scope)
    columns = reader.NAMES + ['frame_offset', 'request_x', 'request_y']
    with (args.out / 'events.csv').open('x', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=columns); w.writeheader()
        for e in events:
            w.writerow(dict({k:e[k] for k in reader.NAMES}, frame_offset=(e['sequence']-1)*328,
                            request_x=e['request'][0], request_y=e['request'][1]))
    pins = [SESSION/'identity.json', SESSION/'events.bin', Path(__file__),
            ROOT/'runtime/construction-winner/observer.h', ROOT/'runtime/construction-winner/reduce_v4.py',
            ROOT/'runtime/construction-winner/read_capture.py']
    summary = dict(pins={str(p.relative_to(ROOT)):sha(p) for p in pins}, records=len(events),
                   kinds=dict(Counter(reader.KINDS[e['kind']] for e in events)),
                   increments=len(transitions), final_epoch=transitions[-1]['after'],
                   increment_counts=dict(Counter(e['reason'] for e in transitions)),
                   resets=[e['sequence'] for e in resets], malformed_controls=malformed,
                   admission_qpc_inversions=sum(a['ticks']>b['ticks'] for a,b in zip(events,events[1:])),
                   qualified_chains=len(result['chains']), reader_equal=True)
    write('summary.json', summary)
    print(json.dumps(summary))


if __name__ == '__main__':
    main()
