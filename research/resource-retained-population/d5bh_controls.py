# SPDX-License-Identifier: GPL-3.0-or-later
"""Exercise projected operands from an explicit D5BH candidate in memory.

Standard-library CPython 3.14. Reads only the candidate and imported code.
No output files, source changes, native or game effects.
"""
import argparse
import json
from pathlib import Path

import d5bh_verify as v


def run(path, pin):
    data = v.read_zip(path, pin)
    counts = v.COUNTS['a'][0]
    spine = data['a/events.jsonl'].splitlines()
    ep_a = v.load_episode(data, 'a')
    ep_b = v.load_episode(data, 'b')
    a0, _ = v.geometry(data, 'a0', ep_a)
    a1, _ = v.geometry(data, 'a1', ep_a)
    b0, _ = v.geometry(data, 'b0', ep_b)
    results = {}

    def refuses(label, method, match):
        try:
            method()
        except ValueError as exc:
            v.require(match in str(exc), f'{label} failed at unintended check: {exc}')
            results[label] = str(exc)
        else:
            raise ValueError(f'Negative control accepted: {label}')

    def mutate_member(member, edit):
        changed = dict(data)
        value = v.loads_unique(changed[member])
        edit(value)
        changed[member] = json.dumps(value).encode()
        return changed

    refuses('corrupted-core', lambda: v.event_rows([b'!', *spine[1:]], counts), 'Expecting value')
    refuses('truncated-core', lambda: v.event_rows(spine[:-1], counts), 'record count')
    refuses('reordered-core', lambda: v.event_rows([spine[1], spine[0], *spine[2:]], counts), 'spine gap')
    refuses('duplicate-core', lambda: v.event_rows([spine[0], *spine], counts), 'spine gap')
    refuses('swapped-process', lambda: v.load_episode(dict(data, **{
        'a/identity.json': data['b/identity.json']}), 'a'), 'Wrong native process')
    refuses('wrong-owner', lambda: v.geometry(mutate_member(
        'a0/geometry.json', lambda row: row['header'].update(owner_formid=1)), 'a0', ep_a), 'Consumer owner')

    def changed_frame():
        identity, process, events, journal = ep_a
        rows = [dict(e, descriptor='00' * 44) if e['sequence'] == 8098 else e for e in events]
        v.geometry(data, 'a0', (identity, process, rows, journal))

    refuses('wrong-frame', changed_frame, 'No positively joined')

    def ambiguous():
        identity, process, events, journal = ep_a
        snapshot = v.loads_unique(data['a0/geometry.json'])
        target = a0['proof']['source']
        other = next(holder['source_pointer'] for holder in snapshot['holders']
                     if holder['source_pointer'] != target['source_pointer'])
        target_bytes = next(e['source_bytes'] for e in events if e['sequence'] == target['birth_sequence'])
        rows = [dict(e, source_bytes=target_bytes[:208] + e['source_bytes'][208:])
                if e['kind'] == 14 and e['source'] == other else e for e in events]
        v.geometry(data, 'a0', (identity, process, rows, journal))

    refuses('alternative-target', ambiguous, 'Geographical identity collision')

    def old_survives():
        _, _, events, journal = ep_a
        changed = dict(journal)
        changed['events'] = [dict(row, allocation=row['allocation'] + 0x100000000,
                                  receiver=row['receiver'] + 0x100000000)
                             if row['sequence'] in (6126, 6127) else row
                             for row in journal['events']]
        prior = v.reducer.relation(a0, a1, events, events, changed)['prior_storage']
        v.nested_endings(a0['proof'], a1['proof'], events, changed, prior)

    refuses('old-collection-survives', old_survives, 'Old content survival')

    def change_word(snapshot):
        holder = next(row for row in snapshot['holders'] if row['resources'])
        region = next(region for row in holder['resources'] for region in row['regions'] if region['count'])
        word = bytearray.fromhex(region['points'])
        word[12] ^= 1
        region['points'] = word.hex()

    refuses('semantic-word', lambda: v.geometry(mutate_member(
        'a0/geometry.json', change_word), 'a0', ep_a), 'Complete normalization')
    refuses('wrong-equal-a0', lambda: v.geometry(dict(data, **{
        'a0/geometry.json': data['a1/geometry.json'],
        'a0/original-receipt.json': data['a1/original-receipt.json'],
        'a0/normalized.bin': data['a1/normalized.bin'],
    }), 'a0', ep_a), 'Wrong original capture')
    refuses('altered-prediction', lambda: v.prediction(dict(data, **{
        'prediction.txt': data['prediction.txt'] + b'\n'}), a0, b0, {}), 'Wrong frozen prediction')
    refuses('altered-source-pin', lambda: v.geometry(mutate_member(
        'a0/original-receipt.json', lambda row: row.update(sha256='0' * 64)), 'a0', ep_a),
        'Wrong original capture')
    refuses('wrong-container-pin', lambda: v.read_zip(path, '0' * 64), 'Candidate SHA-256 mismatch')
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('candidate', type=Path)
    parser.add_argument('--sha256', required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.candidate, args.sha256), indent=2))


if __name__ == '__main__':
    main()
