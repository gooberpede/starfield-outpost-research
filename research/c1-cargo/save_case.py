# SPDX-License-Identifier: GPL-3.0-or-later
"""C1 finite Save52 reread. CPython -B, stdlib and owned S1/P1 readers.

Reads pinned Save52 copy, prior S1 receipt and installed-definition cache.
Writes exclusive ignored JSON and temporary decoded scratch (cleaned by reader).
No original/save/game/database/config/Git/network mutation. Both-drive 40GB guard.
Selected records include the two known marker tokens and their explicit linked
references; unsupported prefixes/extras remain gaps, never empty inventories.
"""
import argparse
import json
from pathlib import Path
import struct
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'research/s1-storage'))
from catalog import pin
from saved import inventory, extra_view
from inventory_historical_saves import guard
from stream_save import decoded_save
from extractor_resources import plugin_tables, saved_form
from outpost_membership import token_value
from outpost_record_framing import iter_records, Reader
from validate_mature_outposts import directory, envelopes
from workshop_inventory import reference_prefix

guard()
ap = argparse.ArgumentParser()
ap.add_argument('--run', required=True)
args = ap.parse_args()
assert args.run.isalnum()
base = ROOT / '.local-work/c1-cargo'
prior = ROOT / '.local-work/s1-storage/saved06.json'
old = json.loads(prior.read_text(encoding='utf8'))
source = Path(old['source']['path'])
before = pin(source)
assert before == old['source']
cache = ROOT / '.local-work/e2-organic/inventory02.json'
definitions = {r['formid']: r for r in json.loads(cache.read_text())['records']}
rows = {}
with decoded_save(source, base / 'scratch') as (data, decoded):
    d = directory(data)
    forms = struct.unpack_from('<' + 'I' * d['reference_count'], data,
                               d['regions']['reference_u32'][0] + 4)
    plugins = plugin_tables(data)
    def resolve(t):
        return saved_form(token_value(t, forms), plugins)
    def ship_instance_tail(r, x):
        """Only the observed flag02/two-mod/zero-bitmask Extra33 case.
        Native 140404a10 + 140406e80: form queue then optional flag bytes.
        Preserve all other cases as explicit gaps, not a general mod decoder.
        """
        if not (x['status'] == 'UNSUPPORTED_EXTRA' and
                x['extras'][-1]['type'] == '33'):
            return x
        rows = x['extras'][:-1]
        c = Reader(data, x['extras'][-1]['offset'], r['end'])
        ri = x['next_reference_index']
        def refs(n):
            nonlocal ri
            assert n <= len(r['refs']) - ri
            values = [resolve(t) for t in r['refs'][ri:ri+n]]
            ri += n
            return values
        assert c.take(1) == b'\x33'
        flags, n = c.take(1)[0], c.count()
        assert flags == 2 and n == 2
        mask = c.take((n*3+7)//8)
        assert mask == b'\0'
        rows.append(dict(type='33', offset=c.p-4, flags=flags, mod_count=n,
                         mask=mask.hex(), mods=refs(n), end=c.p,
                         scope='Only flag02 count2 mask00; no optional mod bytes'))
        for _ in range(x['count'] - len(rows)):
            start, tag = c.p, c.take(1)[0]
            row = dict(type=f'{tag:02x}', offset=start)
            if tag == 0x84:
                n = c.count()
                row['references'] = refs(n)
                row['bytes'] = c.take(n).hex()
            elif tag == 0x4c:
                row['entries'] = []
                for _ in range(c.count()):
                    key, off = refs(1)[0], c.p
                    mode = c.take(1)[0]
                    row['entries'].append(dict(keyword=key, target=refs(1)[0],
                                               mode=mode, offset=off))
            else:
                raise ValueError('C1_SHIP_TAIL_EXTRA_' + hex(tag))
            row['end'] = c.p
            rows.append(row)
        assert len(rows) == x['count']
        return dict(status='COUNT_CLOSED', count=x['count'], extras=rows,
                    body_end=c.p, next_reference_index=ri, record_end=r['end'],
                    queue_count=len(r['refs']), extension='C1 bounded Extra33')
    records = list(iter_records(data, *d['regions']['region_R3'], d['words'][9]))
    envelope = [e for e in envelopes(data, d) if e['qualifies']]
    assert len(envelope) == 1 and 'parsed' in envelope[0]
    edges = [(resolve(s), resolve(g['key'])) for g in envelope[0]['parsed']['groups']
             for s in g['refs']]
    by_token = {r['token']: r for r in records}
    selected = {'82c3c4', '83444c', '825f95', '830a80'}
    # One hop through each marker's queued dynamic references covers explicit
    # compartment/ship/terminal associations without broad inventory extraction.
    for token in ('82c3c4', '83444c'):
        selected.update(t for t in by_token[token]['refs']
                        if t in by_token and resolve(t).startswith('DYNAMIC:'))
    for token in ('82c3c3', '83444b'):
        selected.update(t for t in by_token[token]['refs']
                        if t in by_token and resolve(t).startswith('DYNAMIC:'))
    downstream = {}
    for token in ('82c3f0', '834475'):
        visited, todo = set(), [resolve(token)]
        while todo:
            current = todo.pop()
            if current in visited:
                continue
            visited.add(current)
            todo.extend(t for s, t in edges if s == current and t)
        downstream[token] = sorted(visited)
    selected.update(t for t in by_token
                    if resolve(t) in set(sum(downstream.values(), [])))
    for r in records:
        if ('6508aa' in r['refs'] and
                any(t in r['refs'] for t in ('82c3c4', '83444c'))):
            selected.add(r['token'])
    for t in sorted(selected):
        r = by_token[t]
        row = dict(token=t, identity=resolve(t), offset=r['offset'], end=r['end'],
                   flags=r['flags'], resolved_queue=[resolve(x) for x in r['refs']])
        case = (5 if not r['flags'] & 0x8000 else
                6 if r['flags'] & 0x02000008 else
                4 if r['flags'] & 6 else 7)
        for case in (case,):
            try:
                p = reference_prefix(data, r, case)
                if p.get('self_token') != t:
                    continue
                row['prefix'] = p
                row['base'] = resolve(p['base_token']) if p.get('base_token') else None
                x = extra_view(data, r, p, resolve)
                if t == '82dc37':
                    x = ship_instance_tail(r, x)
                row['extra'] = x
                row['inventory'] = inventory(data, r, x, resolve)
                break
            except (ValueError, KeyError, IndexError, struct.error) as exc:
                row['prefix_error'] = str(exc)
        rows[t] = row
assert pin(source) == before
result = dict(source=before, prior=pin(prior), cache=pin(cache), tool=pin(__file__),
              decoded=decoded, records=len(records), rows=rows, source_unchanged=True,
              edge_envelope=envelope[0], edges=edges, downstream=downstream)
with (base / (args.run + '.json')).open('x', encoding='utf8', newline='\n') as f:
    json.dump(result, f, indent=2)
    f.write('\n')
guard()
print('PASS', len(rows), 'selected records;', len(records), 'framed records')
