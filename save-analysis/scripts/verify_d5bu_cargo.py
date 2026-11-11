# SPDX-License-Identifier: GPL-3.0-or-later
"""Read the finite D5BU cargo selections from one pinned Save52 original."""
import argparse
from collections import Counter
import json
from pathlib import Path
import struct
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from d5bt_reader import ROOT, disk_guard, pin, require
from extractor_resources import plugin_tables, saved_form
from outpost_membership import token_value
from outpost_record_framing import iter_records, Reader
from research_resource_availability import audit
from validate_mature_outposts import directory, envelopes
from verify_d5bu_controls import decode_member, member_pins
from workshop_inventory import reference_prefix

sys.path.insert(0, str(ROOT / 'research/s1-storage'))
from saved import inventory, extra_view

C3_CONTEXT = (3598255, '557f6148a357cc0a354336637a939ae1c3736a63f7a5f7cea27c189cd5095920')


def ship_instance_tail(data, r, x, resolve):
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


def upstream_ids(resolve, markers, edges):
    upstream = {resolve(token) for token in markers}
    while True:
        additional = {source for source, target in edges if target in upstream} - upstream
        if not additional:
            return upstream
        upstream.update(additional)


def c3_selection(resolve, by_token, markers, edges):
    upstream = upstream_ids(resolve, markers, edges)
    return {token for token in by_token if resolve(token) in upstream}


def cargo_producers(data, resolve, markers, edges):
    upstream = upstream_ids(resolve, markers, edges)
    return [dict(owner=beacon['identity'], resource=group['resource_identity'], row=row)
            for beacon in audit(data)['beacons']
            for group in beacon.get('workshop', {}).get('resource_rows', [])
            for row in group['rows'] if row['reference_identities'][0] in upstream]


def parse(data, mode):
    rows = {}
    d = directory(data)
    forms = struct.unpack_from('<' + 'I' * d['reference_count'], data,
                               d['regions']['reference_u32'][0] + 4)
    plugins = plugin_tables(data)
    def resolve(t):
        return saved_form(token_value(t, forms), plugins)
    records = list(iter_records(data, *d['regions']['region_R3'], d['words'][9]))
    envelope = [e for e in envelopes(data, d) if e['qualifies']]
    assert len(envelope) == 1 and 'parsed' in envelope[0]
    edges = [(resolve(s), resolve(g['key'])) for g in envelope[0]['parsed']['groups']
             for s in g['refs']]
    by_token = {r['token']: r for r in records}
    markers = {r['token'] for r in records if '6a6c3f' in r['refs'] or '619523' in r['refs']}
    selected = set(markers)
    for t in markers:
        selected.update(x for x in by_token[t]['refs'] if x in by_token and resolve(x).startswith('DYNAMIC:'))
    ships = {t for t in selected if any(x in by_token[t]['refs'] for x in ('655cc6','619042'))}
    for t in ships:
        selected.update(x for x in by_token[t]['refs'] if x in by_token and resolve(x).startswith('DYNAMIC:'))
    if mode == 'c3':
        selected.update(c3_selection(resolve, by_token, markers, edges))
    producer_rows = cargo_producers(data, resolve, markers, edges) if mode == 'c3' else []
    downstream = {}
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
                if t in ships:

                    try: x = ship_instance_tail(data, r, x, resolve)
                    except (ValueError, AssertionError) as exc: row['ship_extension_gap'] = repr(exc)
                row['extra'] = x
                row['inventory'] = inventory(data, r, x, resolve)
                break
            except (ValueError, KeyError, IndexError, struct.error) as exc:
                row['prefix_error'] = str(exc)
        rows[t] = row
    return dict(producer_rows=producer_rows, records=len(records), rows=rows,
                edge_envelope=envelope[0], edges=edges, downstream=downstream,
                markers=sorted(markers), ships=sorted(ships))


def ship_subset(c2):
    rows = c2['rows']
    actual_markers = [rows[token] for token in c2['markers']
                      if rows[token].get('base') in {'starfield.esm:2a6c3f', 'starfield.esm:219523'}]
    require((len(rows), len(actual_markers), len(c2['ships'])) == (929, 61, 24), 'C2_SELECTED_COUNTS')
    ships = [rows[token] for token in c2['ships']]
    stocks = Counter()
    for ship in ships:
        stock = ship.get('inventory', {})
        if stock['status'] == 'DECODED_EMPTY_STACK_EXTRA_SUBSET':
            stocks['stocked' if stock['item_count'] else 'empty'] += 1
        else:
            gap = ship.get('ship_extension_gap', '')
            for tag in ('30', 'd9'):
                if f'C1_SHIP_TAIL_EXTRA_0x{tag}' in gap:
                    stocks[tag] += 1
                    break
            else:
                raise ValueError('C2_UNCLASSIFIED_STOCK_GAP')
    require(stocks == {'stocked': 11, 'empty': 8, '30': 4, 'd9': 1}, f'C2_STOCK_SCOPE:{stocks}')
    return dict(stocks=stocks, selected=len(rows), markers=len(actual_markers), ships=len(ships))


def verify_selected(c2, c3):
    def by_id(result):
        return {row['identity'].split(':')[-1]: row for row in result['rows'].values()}

    def links(row):
        extra, = [e for e in row['extra']['extras'] if e['type'] == '4c']
        return extra['offset'], {e['keyword'].split(':')[-1]: e['target'].split(':')[-1]
                                 for e in extra['entries']}

    def items(row):
        return [(entry['item'].split(':')[-1], stack['count'], stack['offset'])
                for entry in row['inventory']['rows'] for stack in entry['stacks']]

    def av(row, key):
        require(row['extra']['status'] == 'COUNT_CLOSED', 'CARGO_AV_CONTEXT')
        return [(field['value'], field['offset']) for extra in row['extra']['extras']
                if extra['type'] == 'bf' for section in extra['sections']
                for field in section['values'] if field['av'] == 'starfield.esm:' + key]

    transport, fuel = by_id(c2), by_id(c3)
    for marker, peer, offset, extra_offset in (
        ('ff02c3c4', 'ff03444c', 3810829, 3810958),
        ('ff03444c', 'ff02c3c4', 4505842, 4505971),
    ):
        row = transport[marker]
        at, graph = links(row)
        require((row['offset'], at, graph['255cc8'], graph['255cc7']) ==
                (offset, extra_offset, peer, 'ff02dc37'), 'C2_PRINCIPAL_MARKER')
    hold = transport['ff02dc37']
    at, graph = links(hold)
    require((hold['offset'], at) == (2344136, 2344486)
            and {k: graph[k] for k in ('255ccc', '255cca', '255ccb', '255cc9', '255cce', '255ccd', '255cc3')} ==
            dict(zip(('255ccc', '255cca', '255ccb', '255cc9', '255cce', '255ccd', '255cc3'),
                     ('ff02c3ef', 'ff02c3f0', 'ff034474', 'ff034475', 'ff02c3c3', 'ff03444b', 'ff03444b'))),
            'C2_PRINCIPAL_HOLD')
    stock = hold['inventory']
    require((stock['start'], stock['end'], stock['item_count']) == (2344497, 2344498, 0),
            'C2_PRINCIPAL_STOCK')
    require(av(hold, '2457af') == [(1.0, 2344468)]
            and av(transport['ff047b8b'], '2457af') == [(1.0, 2436339)]
            and av(transport['ff01c5b7'], '2457af') == [], 'C2_DIRECTION_AV')
    for identity, target, expected in (
        ('ff019341', 'ff01ca83', [('00558e', 558), ('005579', 3)]),
        ('ff01c5b7', 'ff0217b4', [('00557a', 7)]),
        ('ff047b8b', 'ff02b86a', [('00557f', 3)]),
    ):
        require(links(transport[identity])[1]['255cc3'] == target
                and [x[:2] for x in items(transport[identity])] == expected, 'C2_FREIGHT_DIRECTION')
    for identity, item, quantity, offset in (
        ('ff04fb23', '00558e', 1, 5801989), ('ff050483', '00558e', 150, 5873692),
        ('ff036b0f', '00558e', 15, 4567639), ('ff036b11', '00558e', 15, 4568153),
        ('ff0428f5', '005576', 499, 5094135),
    ):
        require((item, quantity, offset) in items(fuel[identity]), 'C3_SOURCE_STOCK')
    destinations = {target for _, target in c3['edges']}
    for identity in ('ff0217b5', 'ff020ce1'):
        require('DYNAMIC:' + identity not in destinations, 'C3_PAD01_SCOPED_ABSENCE')
        require(av(fuel[identity], '000338') == [], 'C3_OMITTED_FUEL_OVERRIDE')
    require(av(fuel['ff04fad9'], '000338') == [(1.0, 5783442)]
            and av(fuel['ff02b86b'], '000338') == [(2.0, 3732273)], 'C3_EXPLICIT_FUEL_OVERRIDES')
    require(items(fuel['ff04fb23'])[0][1] < 5, 'C3_BELOW_ONE_CYCLE')
    for identity, offset, cached in (
        ('ff0217b5', 5811894, 0), ('ff04fad9', 4440860, 1),
        ('ff020ce1', 3760441, 0), ('ff02b86b', 3616939, 0),
    ):
        row, = [r['row'] for r in c3['producer_rows'] if r['resource'] == 'starfield.esm:21e6ff'
                and r['row']['reference_identities'][0] == 'DYNAMIC:' + identity]
        require(row['offset'] == offset and struct.unpack('<iiBff', bytes.fromhex(row['payload_hex'])) ==
                (0, 1, cached, 30.271221160888672, 102.5999984741211), 'C3_PAD_PRODUCER')
        require(fuel[identity]['inventory']['status'] == 'NO_INVENTORY_CHANGE_BRANCH', 'C3_PAD_STOCK_SCOPE')


def refuse_ship_extensions():
    record = dict(end=4, refs=['one', 'two'])
    view = dict(status='UNSUPPORTED_EXTRA', extras=[dict(type='33', offset=0)],
                next_reference_index=0, count=1)
    for payload in (b'\x33\x03\x08\0', b'\x33\x02\x04\0', b'\x33\x02\x08\x01'):
        try:
            ship_instance_tail(payload, record, view, str)
        except (AssertionError, ValueError):
            continue
        raise ValueError('CARGO_UNSUPPORTED_EXTRA33_ACCEPTED')
    return ['unsupported flags', 'unsupported count', 'unsupported mask']


def verify_wire(data, c2):
    records = {row['identity']: row for row in c2['rows'].values()}
    for identity, offset in (('ff02c3ef', 3826329), ('ff02c3f0', 3826450),
                             ('ff034474', 4521282), ('ff034475', 4521403)):
        require(records['DYNAMIC:' + identity]['offset'] == offset, 'C2_BAY_RECORD_OFFSET')
    for offset, count in ((5801989, 1), (5873692, 150), (4567639, 15),
                          (4568153, 15), (5094135, 499)):
        require(data[offset] == 0 and struct.unpack_from('<i', data, offset+1)[0] == count,
                'C3_INDEPENDENT_STOCK_BYTES')
    for offset, value in ((5783442, 1.0), (3732273, 2.0), (2344468, 1.0), (2436339, 1.0)):
        require(struct.unpack_from('<f', data, offset)[0] == value, 'CARGO_INDEPENDENT_AV_BYTES')
    require(data[2344497] == 0, 'C2_INDEPENDENT_EMPTY_HOLD')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--save52', required=True, type=Path)
    parser.add_argument('--c3-context', required=True, type=Path)
    parser.add_argument('--receipt', required=True, type=Path)
    args = parser.parse_args()
    require(sys.flags.isolated and sys.dont_write_bytecode and __debug__, 'USE_PYTHON_I_B')
    disk_guard(args.receipt.parent)
    require(pin(args.c3_context) == C3_CONTEXT, 'C3_CONTEXT_IDENTITY')
    prior = json.loads(args.c3_context.read_bytes())
    with args.receipt.open('x', encoding='utf8', newline='\n') as stream:
        try:
            with decode_member(40, args.save52, args.receipt.parent, member_pins()) as (data, metrics):
                c2, c3 = parse(data, 'c2'), parse(data, 'c3')
                verify_wire(data, c2)
            summary = ship_subset(c2)
            require(all(json.loads(json.dumps(c3[key])) == prior[key] for key in c3), 'C3_RECEIPT_COMPARISON')
            require(pin(args.c3_context) == C3_CONTEXT, 'C3_CONTEXT_CHANGED')
            require(len(c3['edges']) == 246 and len(c3['rows']) == 944, 'C3_SELECTION')
            require(c2['edges'] == c3['edges'], 'C2_C3_EDGE_CORRESPONDENCE')
            verify_selected(c2, c3)
            disk_guard(args.receipt.parent)
            json.dump(dict(decoded=metrics['decoded_sha256'], c2=summary, c3_receipt_match=True,
                           controls=refuse_ship_extensions(), c2_rows=c2['rows']), stream, indent=2)
            stream.write('\n')
        except Exception as error:
            json.dump(dict(error=type(error).__name__, detail=str(error)), stream)
            raise


if __name__ == '__main__':
    main()
