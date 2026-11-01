# SPDX-License-Identifier: GPL-3.0-or-later
"""Inspect a stopped B2 capture without promoting an unqualified firstness chain.

Reads raw frames, the authenticated reader result and owned schema-4 decoder.
Writes one exclusive local JSON derivative; no target, save, configuration,
network or Git effects. Requires normal Python with -E -B. Reuses owned
read_capture.py/source-identity methods under SOR-P-0002; raw evidence stays local.
"""
import sys
if not __debug__ or sys.flags.optimize:
    raise RuntimeError('Python optimization is forbidden; invoke with -E -B')
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import struct
import zlib

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'runtime/construction-winner'))
import read_capture as reader


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('session', type=Path)
    parser.add_argument('--reader', required=True, type=Path)
    parser.add_argument('--out', required=True, type=Path)
    args = parser.parse_args()
    assert args.out.resolve().is_relative_to(ROOT / '.local-work/d5ab')
    identity = json.loads((args.session / 'identity.json').read_bytes())
    pinned_dll = '9d2f0bab159f3ec23186426fb4833eb645578d2a43612bb2e8def6b1af455dcc'
    result = reader.inspect(args.session, pinned_dll)
    assert result == json.loads(args.reader.read_bytes())
    assert result['complete_session'] and not result['damage']
    raw = (args.session / 'events.bin').read_bytes()
    events = []
    for offset in range(0, len(raw), 328):
        header, payload = raw[offset:offset + 16], raw[offset + 16:offset + 328]
        magic, size, sequence, crc = struct.unpack('<4I', header)
        event = reader.decode(payload)
        assert magic == 0x31505253 and size == 312 and zlib.crc32(payload) == crc
        assert sequence == event['sequence'] == len(events) + 1
        events.append(dict(event, kind_name=reader.KINDS[event['kind']], frame_offset=offset))
    joins = [j for j in result['identities'] if j['source_key'] == reader.TARGET]
    keys = {(j['invocation'], j['selection']) for j in joins if not j['bypass']}
    relevant = [e for e in events if (e['invocation'], e['selection']) in keys]
    samples = []
    for key in sorted(keys):
        parts = [e for e in relevant if (e['invocation'], e['selection']) == key]
        by_kind = {k: [e for e in parts if e['kind'] == k] for k in (2,3,4,5,6,7,8,16,17)}
        if not by_kind[7]:
            continue
        assert all(len(rows) == 1 for rows in by_kind.values())
        ordered = [by_kind[k][0] for k in (2,3,4,5,6,7,8,16,17)]
        assert all(not e['status'] and not e['hazards'] for e in ordered)
        assert len({(e['thread'], e['epoch'], e['proc'], e['source'], e['frame'], e['parent'], tuple(e['request'])) for e in ordered}) == 1
        assert all(a['ticks'] <= b['ticks'] and a['sequence'] < b['sequence'] for a,b in zip(ordered, ordered[1:]))
        selected, visited, lookup, descriptor, generating, sample, generated, reserve, stored = ordered
        joined = next(j for j in joins if (j['invocation'], j['selection']) == key)
        assert not visited['a'] and lookup['a'] == lookup['b']
        assert generating['a'] == 0x5e0de and generating['c'] == sample['c'] and 0 <= sample['a'] <= 15
        assert descriptor['d'] == descriptor['holder'] + 0xc8
        assert reserve['a'] < (reserve['c'] & 0xffffffff) <= (reserve['c'] >> 32)
        assert stored['a'] == reserve['d'] + reserve['a'] * 8 and stored['b'] == joined['token']
        birth = events[joined['birth_sequence'] - 1]
        assert reader.source_key(birth) == reader.TARGET
        samples.append(dict(invocation=key[0], selection=key[1], mask=sample['a'],
            owner_form_id=generating['a'], sample_sequence=sample['sequence'],
            store_sequence=stored['sequence'], allocation=joined['allocation'],
            birth_sequence=joined['birth_sequence'], publication_sequence=joined['publication_sequence'],
            epoch=joined['epoch'], append_destination_verified=True,
            scope='Direct target sample and token-store facts; no cold-first qualification.'))
    epochs = {j['epoch'] for j in joins}
    resets = [e for e in events if e['kind'] == 12 or (e['kind'] in (10,11) and e['a'] == 0)]
    value = dict(method_sha256=sha(__file__), decoder_sha256=sha(reader.__file__),
        raw_sha256=sha(args.session / 'events.bin'), reader_sha256=sha(args.reader),
        identity_sha256=sha(args.session / 'identity.json'), complete_session=result['complete_session'],
        durable_records=result['durable_records'], kind_counts=dict(Counter(e['kind_name'] for e in events)),
        target=reader.TARGET, target_joins=len(joins), target_bypasses=sum(j['bypass'] for j in joins),
        target_epochs=sorted(epochs), target_samples=samples, target_initial_boundaries=relevant,
        reset_boundaries=resets, target_epoch_reset_boundaries=[e for e in resets if e['epoch'] in epochs],
        qualified_chains=result['chains'], firstness_refusals=result['firstness_refusals'],
        semantic_diagnostics=dict(Counter(d['outcome'] for d in result['diagnostics'])),
        conclusion='Direct sample/store observations are separate from absent cold-first certification.',
        address_domain='source/proc/frame/holder/store addresses are runtime pointers; frame_offset is a capture-file byte offset; sequences and FormIDs are separate domains.')
    with args.out.open('x', encoding='utf8', newline='\n') as stream:
        json.dump(value, stream, indent=2);stream.write('\n')
    print(json.dumps(dict(target_joins=len(joins), bypasses=value['target_bypasses'], samples=samples,
                          qualified_chains=len(value['qualified_chains']), target_epoch_reset_boundaries=len(value['target_epoch_reset_boundaries']))))


if __name__ == '__main__':
    main()
