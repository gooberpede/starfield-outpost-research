# SPDX-License-Identifier: GPL-3.0-or-later
"""S1 selected saved containers; owned P1 prefix/extra grammar, native-backed
inventory tail subset. Reads hash-pinned HIST-0036 or mature-Save52 originals,
E2 index and S1 census. Writes fresh ignored receipt; decoded scratch cleaned.
Stdlib/project only. Unknown stack extras stop decoding, never imply empty.
No game, native invocation, original/save/database/configuration/Git mutation.
"""
import argparse
import collections
import json
from pathlib import Path
import struct
import sys
from catalog import ROOT, pin
sys.path.insert(0, str(ROOT / 'research/p1-power'))
from saved_instances import extra_view
sys.path.insert(0, str(ROOT / 'save-analysis/scripts'))
from inventory_historical_saves import guard
from stream_save import decoded_save
from extractor_resources import plugin_tables, saved_form
from outpost_membership import token_value
from outpost_record_framing import Reader, iter_records
from validate_mature_outposts import directory
from workshop_inventory import reference_prefix


def inventory(data, r, extra, resolve):
    """Native 1406448b0/140641320/140642a00 wire order; empty stack extras only.
    Item base is queued identity, compact stack count, per-stack extra list then
    signed i32 quantity, item u32 bookkeeping and u8. Unsupported is retained.
    """
    if extra.get('status') != 'COUNT_CLOSED':
        return dict(status='LEADING_EXTRA_GAP')
    c = Reader(data, extra['body_end'], r['end'])
    ri = extra['next_reference_index']
    if not r['flags'] & 0x08000020:
        return dict(status='NO_INVENTORY_CHANGE_BRANCH', tail_bytes=r['end'] - c.p)
    start = c.p
    rows = []
    n = c.count()
    if n > len(r['refs']) - ri:
        raise ValueError('INVENTORY_ITEM_QUEUE_BOUNDS')
    for _ in range(n):
        item = resolve(r['refs'][ri])
        ri += 1
        row = dict(item=item, offset=c.p, stacks=[])
        ns = c.count()
        for _ in range(ns):
            ep = c.p
            ne = c.count()
            if ne:
                return dict(status='UNSUPPORTED_STACK_EXTRAS', start=start,
                            item_count=n, rows=rows, current_item=item,
                            stack_extra_offset=ep, stack_extra_count=ne,
                            next_reference_index=ri)
            count = struct.unpack('<i', c.take(4))[0]
            row['stacks'].append(dict(offset=ep, count=count))
        row['bookkeeping'] = struct.unpack('<I', c.take(4))[0]
        row['byte'] = c.take(1)[0]
        rows.append(row)
    return dict(status='DECODED_EMPTY_STACK_EXTRA_SUBSET', start=start, end=c.p,
                item_count=n, rows=rows, record_end=r['end'],
                next_reference_index=ri, reference_count=len(r['refs']))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--sample', required=True)
    ap.add_argument('--run', required=True)
    a = ap.parse_args()
    assert a.run.isalnum()
    guard()
    base = ROOT / '.local-work/s1-storage'
    out = base / (a.run + '.json')
    assert not out.exists()
    assert a.sample == 'mature-Save52' or (a.sample.startswith('HIST-') and a.sample[5:].isdigit())
    prior = (ROOT / '.local-work/resource-availability/saves01/mature-Save52.json' if a.sample == 'mature-Save52'
             else ROOT / '.local-work/e3-fabricators/saved01' / (a.sample + '.json'))
    old = json.loads(prior.read_text())
    source = Path(old['source']['path'])
    before = pin(source)
    assert before['sha256'] == old['source']['sha256']
    cache = ROOT / '.local-work/e2-organic/inventory02.json'
    by = {r['formid']: r for r in json.loads(cache.read_text())['records']}
    census = ROOT / '.local-work/s1-storage/census02.json'
    candidates = {int(r['formid'], 16): r for r in json.loads(census.read_text())['rows']}
    # Fuel ACTI references are included even without physical TESContainer.
    candidates.update({i: dict(editorid=name) for i, name in
                       [(0x2b063a, 'OutpostPowerFueledGenerator01'),
                        (0x219523, 'OutpostCargoLinkMarker_Fueled'),
                        (0x2a6c3f, 'OutpostCargoLinkMarker')]})
    rows, gaps = [], collections.Counter()
    with decoded_save(source, base / 'scratch') as (data, decoded):
        d = directory(data)
        forms = struct.unpack_from('<' + 'I' * d['reference_count'], data,
                                   d['regions']['reference_u32'][0] + 4)
        plugins = plugin_tables(data)
        def resolve(t):
            return saved_form(token_value(t, forms), plugins)
        for r in iter_records(data, *d['regions']['region_R3'], d['words'][9]):
            if int(r['token'], 16) >> 22 != 2:
                continue
            if r['explicit_type'] is not None and not 0x4a <= r['explicit_type'] <= 0x55:
                continue
            try:
                case = 5 if not r['flags'] & 0x8000 else 6 if r['flags'] & 0x02000008 else 4 if r['flags'] & 6 else 7
                p = reference_prefix(data, r, case)
                bid = resolve(p['base_token']) if p['base_token'] else None
                fid = int(bid.split(':')[1], 16) if bid and bid.startswith('starfield.esm:') else None
                if fid not in candidates:
                    continue
                row = dict(identity=resolve(r['token']), base=bid,
                           editorid=candidates[fid]['editorid'], offset=r['offset'],
                           end=r['end'], flags=r['flags'], prefix=p,
                           resolved_queue=[resolve(t) for t in r['refs']])
                try:
                    extra = extra_view(data, r, p, resolve)
                    row['extra'] = extra
                    row['inventory'] = inventory(data, r, extra, resolve)
                except (ValueError, IndexError) as e:
                    row['gap'] = str(e)
                rows.append(row)
            except (ValueError, IndexError) as e:
                gaps[str(e)] += 1
    assert pin(source) == before
    with out.open('x', encoding='utf8', newline='\n') as f:
        json.dump(dict(sample=a.sample, source=before, prior=pin(prior), tool=pin(Path(__file__)),
                       census=pin(census), cache=pin(cache), decoded=decoded,
                       source_unchanged=True, rows=rows, prefix_gaps=dict(gaps),
                       limits=['Positive inline-base reference subset, not exhaustive Workshop ownership',
                               'Historical saved state, not current loaded stocks',
                               'Nonempty stack extras remain unsupported']), f, indent=2)
        f.write('\n')
    print(a.sample, len(rows), dict(collections.Counter(r.get('inventory', {}).get('status', r.get('gap')) for r in rows)))


if __name__ == '__main__':
    main()
