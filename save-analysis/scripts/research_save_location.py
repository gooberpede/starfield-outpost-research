"""SPDX-License-Identifier: GPL-3.0-or-later
Invoked capacity/location brief: hash-verified manifest inputs, observation only.
Writes exclusive ignored receipts, temporary mapped scratch; stdlib/project code.
No JSON expectations are read. No game/database writes. See experiment report.
"""
from pathlib import Path
import argparse
import json
import struct
import sys
import tracemalloc
from investigate_active_outposts import specs
from inventory_historical_saves import identity, metadata, guard, ROOT
from validate_mature_outposts import directory, pool
from outpost_record_framing import iter_records
from outpost_membership import initial_prefix, token_value
from stream_save import decoded_save


def extract(b):
    d = directory(b)
    a, z = d['regions']['reference_u32']
    # Random table lookup avoids materializing millions of Python integers.
    class Table:
        def __len__(self): return d['reference_count']
        def __getitem__(self, i): return struct.unpack_from('<I', b, a+4+4*i)[0]
    table = Table()
    a3, z3 = d['regions']['region_R3']
    _, strings = pool(b, d)
    candidates, parents, player, count = [], set(), [], 0
    for r in iter_records(b, a3, z3, d['words'][9]):
        count += 1
        if r['token'] == '400014':
            player.append(r)
        if len(r['refs']) < 3 or r['flags'] & 0x8000:
            continue
        try:
            base = token_value(r['refs'][1], table)
        except ValueError:
            continue
        if base != 0x2c60e9:
            continue
        p = initial_prefix(b, r, 5)
        parents.add(p['parent_token'])
        candidates.append(dict(record=r, prefix=p,
            parent_saved_id=token_value(p['parent_token'], table),
            strings=[strings[i]['text'] for i in r['strings'] if i < len(strings)]))
    hits = {}
    for token in parents:
        pattern = bytes.fromhex(token)
        rows = []
        for region, (a, z) in d['regions'].items():
            q = a
            while (q := b.find(pattern, q, z)) >= 0:
                # Narrow raw windows remain ignored/local only.
                rows.append(dict(region=region, offset=q, start=max(a,q-24),
                                 hex=b[max(a,q-24):min(z,q+64)].hex()))
                q += 1
        hits[token] = rows
    return dict(directory=d, framed_records=count, candidates=candidates,
                player_records=player, parent_occurrences=hits)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--run', required=True)
    ap.add_argument('--labels', required=True)
    args = ap.parse_args()
    if not args.run.replace('-', '').isalnum(): raise ValueError('run name')
    out = ROOT / '.local-work/save-capacity-location' / args.run
    out.mkdir(exist_ok=False)
    selected = [s for s in specs() if s['label'] in args.labels.split(',')]
    if {s['label'] for s in selected} != set(args.labels.split(',')):
        raise ValueError('unknown label')
    before = {}
    result = []
    for s in selected:
        guard(out)
        for role in ('source', 'copy'):
            p = Path(s[role]['path'])
            v = identity(p)
            if v['sha256'] != s[role]['sha256']: raise ValueError('INPUT_HASH')
            before[str(p)] = v
        tracemalloc.start()
        with decoded_save(s['copy']['path'], out / 'scratch') as (b, metrics):
            row = dict(label=s['label'], source=s['copy'], metrics=metrics,
                       metadata=metadata(b), extraction=extract(b))
        row['python_peak_bytes'] = tracemalloc.get_traced_memory()[1]
        tracemalloc.stop()
        result.append(row)
        print(s['label'], metrics, 'records', row['extraction']['framed_records'], flush=True)
    after = {p: identity(Path(p)) for p in before}
    if before != after: raise RuntimeError('PRESERVATION_FAILURE')
    for name, data in [('results.json', result), ('preservation.json', dict(before=before,after=after)),
                       ('tools.json', dict(python=sys.version, argv=sys.argv,
                         scripts=[identity(p) for p in Path(__file__).parent.glob('*.py')]))]:
        with (out/name).open('x', encoding='utf-8', newline='\n') as f:
            json.dump(data, f, indent=2); f.write('\n')


if __name__ == '__main__': main()
