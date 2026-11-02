# SPDX-License-Identifier: GPL-3.0-or-later
"""Check historical source-birth coverage without inventing geometry or new results.

Reads only the hash-pinned retained B2 retry through the unchanged schema-4 reader.
Writes an exclusive D5AI receipt. Stdlib and owned reader; no process, save,
database, network or Git operations. This is historical feasibility evidence,
not qualification of the new observer or a Phase B observation. Requires -E -B.
"""
import sys
if not __debug__ or sys.flags.optimize:
    raise RuntimeError('Use Python -E -B')

from collections import Counter, defaultdict
import json
from pathlib import Path

from d5ae_baseline import guard, sha

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'runtime/construction-winner'))
import read_capture


def main():
    guard()
    out = (ROOT / '.local-work/d5ai' / sys.argv[1]).resolve()
    if out.exists() or not out.is_relative_to(ROOT / '.local-work/d5ai'):
        raise ValueError('Fresh task-local receipt required')
    session = ROOT / '.local-work/d5x/live/session-5ed302aea9da7dc2261163b3dd1816e670a3c2f39891f1ec8d20094afa72b3a1'
    raw_path = session / 'events.bin'
    if sha(raw_path) != '4a8feb68f667f417967a0cd4a332cefde768658d254ead8d555b3e5f44515218':
        raise ValueError('B2 raw identity changed')
    result = read_capture.inspect(session, '9d2f0bab159f3ec23186426fb4833eb645578d2a43612bb2e8def6b1af455dcc')
    if not result['complete_session'] or result['damage']:
        raise ValueError('Historical B2 authentication failed')
    raw = raw_path.read_bytes()
    events = [read_capture.decode(raw[i + 16:i + 328]) for i in range(0, len(raw), 328)]
    births, rows = defaultdict(list), []
    for event in events:
        if event['kind'] == 14:
            births[event['source']].append(event)
    for generated in (event for event in events if event['kind'] == 6):
        birth = max((b for b in births[generated['source']] if b['ticks'] < generated['ticks']),
                    key=lambda b: b['ticks'], default=None)
        rows.append(dict(generate=generated['sequence'], key=None if birth is None else read_capture.source_key(birth),
                         birth_epoch=None if birth is None else birth['epoch'], generate_epoch=generated['epoch'],
                         birth_sequence=None if birth is None else birth['sequence'],
                         same=birth is not None and birth['epoch'] == generated['epoch']))
    counts = Counter(row['key'] for row in rows)
    receipt = dict(rows=rows, total=len(rows), same_epoch=sum(row['same'] for row in rows),
                   duplicate_generated_geographies={key: n for key, n in counts.items() if n > 1},
                   raw_sha256=sha(raw_path), method_sha256=sha(__file__), reader_sha256=sha(read_capture.__file__),
                   scope='Historical B2 coverage compatibility only; no full geometry, departure/return or new retail result')
    with out.open('x', encoding='utf8', newline='\n') as stream:
        stream.write(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(dict(total=len(rows), same_epoch=receipt['same_epoch'], duplicate_keys=receipt['duplicate_generated_geographies'])))


if __name__ == '__main__':
    main()
