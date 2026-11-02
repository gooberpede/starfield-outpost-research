# SPDX-License-Identifier: GPL-3.0-or-later
"""Audit the preserved B2 Lodge checkpoint against native event boundaries.

Reads historical B1/B2 events and identities, the identity-bound Lodge ACK and
observation, B1 ACK, and owned D5AC/read_capture methods. Writes a fresh ignored
local receipt.
Stdlib only, under the D5AD offline brief; no target, save, DB or Git writes.
SOR-P-0002: conceptually reuses D5AC fixed-offset decoding and inspector.
Checks a partial order; never invents unrecorded initialization events.
"""
import collections
import hashlib
import json
from pathlib import Path
import struct
import sys
import zlib

import d5ac_reconstruct as ac
from d5ad_baseline import guard, sha

ROOT = Path(__file__).resolve().parents[2]
NOTES = ROOT / '.local-work/d5ab/B2-APPROVED-002-notes'


def validate_resets(resets):
    if len(resets) != 6:
        raise ValueError('Missing reset triad')
    for offset in (0, 3):
        begin, cold, end = resets[offset:offset + 3]
        if ([e['kind'] for e in (begin, cold, end)] != [10, 12, 11] or
                any(e['status'] for e in (begin, cold, end)) or
                [e['hazards'] for e in (begin, cold, end)] != [1, 1, 0] or
                len({e['proc'] for e in (begin, cold, end)}) != 1 or
                len({e['epoch'] for e in (begin, cold, end)}) != 1 or
                len({e['thread'] for e in (begin, cold, end)}) != 1 or
                cold['a'] or cold['b'] or
                not begin['ticks'] < cold['ticks'] < end['ticks']):
            raise ValueError('Unqualified matched reset triad')


def audit(events, ack):
    n = ack['ack']['acknowledged']
    if ack['state'] != 'HEALTHY_ACK' or n != 876:
        raise ValueError('Wrong Lodge checkpoint')
    if ack['ack']['loss_generation'] or ack['ack']['output_faults']:
        raise ValueError('Unhealthy checkpoint')
    prefix = events[:n]
    if any(e['kind'] in (1, 2, 4, 16, 17) for e in prefix):
        raise ValueError('Unexpected provider/append in checkpoint prefix')
    births, pairs = {}, []
    for e in prefix:
        if e['kind'] not in (14, 15):
            continue
        key = e['source'], e['holder']
        if e['status'] or e['hazards']:
            raise ValueError('Unqualified source metadata event')
        if e['kind'] == 14:
            if key in births:
                raise ValueError('Overlapping source birth')
            births[key] = e
        else:
            birth = births.pop(key, None)
            if not birth or birth['thread'] != e['thread'] or birth['ticks'] > e['ticks']:
                raise ValueError('Unmatched source publication')
            pairs.append([birth['sequence'], e['sequence']])
    if births or len(pairs) != 383:
        raise ValueError('Incomplete source publication pairs')
    resets = [e for e in events if e['kind'] == 12 or (e['kind'] in (10, 11) and e['a'] == 0)]
    validate_resets(resets)
    if [e['sequence'] for e in resets] != [2, 3, 4, 881, 882, 883]:
        raise ValueError('Reset boundary mismatch')
    if max(e['ticks'] for e in prefix) >= resets[3]['ticks']:
        raise ValueError('Recorded QPC does not order the second reset after prefix')
    prefix_clears = [e for e in prefix[4:] if e['kind'] == 10]
    if len(prefix_clears) != 53 or any(e['a'] != 3 for e in prefix_clears):
        raise ValueError('Unexpected precheckpoint invalidation')
    if len({resets[0]['proc'], resets[3]['proc']}) != 1:
        raise ValueError('ProcGen identity changed between resets')
    first = next(e for e in events if e['kind'] == 1)
    if first['sequence'] != 2470 or first['ticks'] <= resets[-1]['ticks']:
        raise ValueError('First provider boundary mismatch')
    if any(e['kind'] in (1, 4, 16, 17) for e in events[n:first['sequence'] - 1]):
        raise ValueError('Unexpected intervening mutation')
    return dict(checkpoint=n, prefix_kinds=dict(collections.Counter(ac.reader.KINDS[e['kind']] for e in prefix)),
                resets=[dict(sequence=e['sequence'], kind=e['kind'], ticks=e['ticks'], epoch=e['epoch']) for e in resets],
                prefix_max_qpc=max(e['ticks'] for e in prefix),
                first_provider=dict(sequence=first['sequence'], ticks=first['ticks'], epoch=first['epoch']),
                first_source_birth=next(e['sequence'] for e in events if e['kind'] == 14),
                first_publication=next(e['sequence'] for e in events if e['kind'] == 15),
                checkpoint_empty_anchor=dict(reset_end=4, grid_clears=53,
                    scope='Derived under ordinary mutation coverage: metadata creation and removal-only Grid clears preserve empty population/visited state; not a direct ACK-time memory snapshot'),
                source_publication_pairs=pairs,
                prefix_sources=[dict(sequence=e['sequence'], key=ac.reader.source_key(e),
                                     loss_generation=e['d'], grid=e['holder'],
                                     source=e['source'], allocation=e['selection'],
                                     status=e['status'], hazards=e['hazards'])
                                for e in prefix if e['kind'] == 14],
                qualification='Recorded boundary order, not reset caller identity or a native visual-load timestamp')


def main():
    if not __debug__ or sys.flags.optimize:
        raise RuntimeError('Invoke Python with -E -B')
    guard()
    out = Path(sys.argv[1]).resolve()
    if out.exists() or not out.is_relative_to(ROOT / '.local-work/d5ad'):
        raise ValueError('Fresh local output required')
    raw = (ac.SESSION / 'events.bin').read_bytes()
    events = ac.decode_frames(raw)
    inspected = ac.reader.inspect(ac.SESSION, ac.DLL_SHA)
    if not inspected['complete_session'] or inspected['damage']:
        raise ValueError('Historical capture failed authentication')
    ackpath = NOTES / 'loaded-Lodge-poll-dc1fcbfa1c5f4c3f8940b051900df7d3.json'
    ack = json.loads(ackpath.read_bytes())
    if ack['identity_sha256'] != sha(ac.SESSION / 'identity.json'):
        raise ValueError('ACK identity mismatch')
    result = audit(events, ack)
    controls = []
    for name in ('wrong-checkpoint', 'loss', 'prefix-provider', 'second-reset-clock',
                 'unmatched-publication', 'cold-status', 'cold-hazard', 'end-proc', 'end-epoch'):
        changed_ack = json.loads(json.dumps(ack))
        changed_events = [dict(e) for e in events]
        if name == 'wrong-checkpoint':
            changed_ack['ack']['acknowledged'] = 875
        elif name == 'loss':
            changed_ack['ack']['loss_generation'] = 1
        elif name == 'prefix-provider':
            changed_events[5]['kind'] = 1
        elif name == 'second-reset-clock':
            changed_events[880]['ticks'] = result['prefix_max_qpc']
        elif name == 'unmatched-publication':
            changed_events[5]['source'] ^= 8
        elif name == 'cold-status':
            changed_events[2]['status'] = 1
        elif name == 'cold-hazard':
            changed_events[2]['hazards'] = 0
        elif name == 'end-proc':
            changed_events[3]['proc'] = 123
        else:
            changed_events[3]['epoch'] = 999
        try:
            audit(changed_events, changed_ack)
        except ValueError:
            controls.append(dict(name=name, rejected=True))
        else:
            raise AssertionError('Control accepted: ' + name)
    paths = [Path(__file__), Path(ac.__file__), ackpath, ac.SESSION / 'events.bin',
             ac.SESSION / 'identity.json', NOTES / 'loaded-Lodge-observation.json',
             ROOT / 'runtime/construction-winner/read_capture.py']
    result.update(controls=controls, records=len(events), reader_complete=True,
                  pins={p.relative_to(ROOT).as_posix(): sha(p) for p in paths},
                  observation=json.loads((NOTES / 'loaded-Lodge-observation.json').read_bytes()),
                  boundary_limit='ACK prefix is a durable admission watermark, not a barrier stopping concurrent producers; omitted hook classes remain unobserved.')
    b1 = ROOT / '.local-work/d5x/live/session-ceb439b14ddc4db8b734526a124f1e879b64cd457774a87a6a67852fd4489894'
    if sha(b1 / 'events.bin') != 'cd4762095a422fb537844546e923fff667e894a63b082b0205f3107786f49a5c':
        raise ValueError('B1 raw pin')
    b1result = ac.reader.inspect(b1, '20160e2ccdf183c84baddae0214c0438eb471b3eb0ec34dee0632bb5880ddaeb')
    data = (b1 / 'events.bin').read_bytes()
    b1events = []
    for offset in range(0, len(data), 328):
        magic, size, sequence, crc = struct.unpack_from('<4I', data, offset)
        payload = data[offset + 16:offset + 328]
        if (magic, size, sequence) != (0x31505253, 312, len(b1events) + 1) or zlib.crc32(payload) != crc:
            raise ValueError('B1 frame integrity')
        e = ac.reader.decode(payload)
        if e['sequence'] != sequence:
            raise ValueError('B1 payload sequence')
        b1events.append(e)
    b1ackpath = b1 / 'ack-8d85d0bf7dcbd78c5ca21407d2195151.json'
    if sha(b1ackpath) != '1fc15ba246845ad0ebbae536948ab3dc7c60daaea5711cf0923f17778f8029b0':
        raise ValueError('B1 ACK pin')
    b1ack = json.loads(b1ackpath.read_bytes())
    if b1ack['acknowledged'] != 110 or b1ack['drops'] or not b1result['complete_session']:
        raise ValueError('B1 checkpoint authentication')
    b1reset_rows = [e for e in b1events if e['kind'] == 12 or (e['kind'] in (10, 11) and e['a'] == 0)]
    validate_resets(b1reset_rows)
    b1resets = [e['sequence'] for e in b1reset_rows]
    if b1resets != [2, 3, 4, 115, 116, 117]:
        raise ValueError('B1 reset mismatch')
    result['b1'] = dict(records=len(b1events), schema=json.loads((b1 / 'identity.json').read_bytes())['schema'],
                        checkpoint=110, prefix_kinds=dict(collections.Counter(ac.reader.KINDS[e['kind']] for e in b1events[:110])),
                        reset_sequences=b1resets, terminal_drops=b1result['terminal']['drops'],
                        scope='Current unchanged reader supports historical schema 2; no reproduction claim for superseded D5Y reader pins')
    result['pins'].update({p.relative_to(ROOT).as_posix(): sha(p) for p in (b1 / 'events.bin', b1 / 'identity.json', b1ackpath)})
    out.mkdir(parents=True)
    (out / 'chronology.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8', newline='\n')
    print(json.dumps({k: result[k] for k in ('checkpoint', 'prefix_kinds', 'first_source_birth', 'first_provider', 'controls')}))


if __name__ == '__main__':
    main()
