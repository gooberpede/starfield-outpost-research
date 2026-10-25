# SPDX-License-Identifier: GPL-3.0-or-later
"""Conservative D5E fixture reducer; never treats fixture epochs as native fields.

Reads an explicit events JSON file and writes a new JSON result. Standard library
only. No target, save, database, configuration, network or Git operations.
"""
import argparse
import json
import struct

PACKET = struct.Struct('<11Q2i6I')
FIELDS = ('magic manager source manager_epoch source_epoch invocation parent visited_key '
          'wrapper lookup capacity query_x query_y mask branch inserted complete geo ready').split()


def reduce(rows):
    session = None
    armed = False
    last = 0
    open_calls = {}
    decisions = []
    rejected = []
    coverage = []

    def incomplete(call, reason):
        decisions.append(dict(call, tier='C', missing=[reason], first_ever=False))

    for order, row in enumerate(rows):
        kind = row['kind']
        if kind == 'SESSION':
            if session is not None:
                raise ValueError('multiple sessions require separate reduction')
            if row.get('synthetic') is not True:
                raise ValueError('fixture lifetime oracle required; use native_reduce for retail')
            session = row
        elif kind == 'ARM_BARRIER':
            armed = bool(session and row.get('readback') and row.get('all_threads', 0) > 0 and row.get('slots') == 4)
            coverage.append(dict(order=order, state='ARMED' if armed else 'GAP'))
        elif kind in ('GAP', 'STOP_COMMITTED', 'EXIT'):
            coverage.append(dict(order=order, state='CLOSED' if kind == 'EXIT' else 'GAP', reason=kind))
            if kind == 'GAP':
                for call in open_calls.values():
                    incomplete(call, 'coverage_gap')
                open_calls.clear()
            armed = False
        elif kind == 'SAMPLE':
            capture = row['capture']
            if capture != last + 1:
                armed = False
                coverage.append(dict(order=order, state='GAP', reason='capture_sequence'))
            last = capture
            if not armed or not row.get('native_read_complete'):
                rejected.append(dict(capture=capture, reason='coverage_or_native_read'))
                continue
            raw = bytes.fromhex(row['raw_packet'])
            if len(raw) != PACKET.size:
                rejected.append(dict(capture=capture, reason='packet_size'))
                continue
            p = dict(zip(FIELDS, PACKET.unpack(raw)))
            if p['magic'] != 0x4435455041434b31 or p['geo'] != 1:
                rejected.append(dict(capture=capture, reason='magic_or_unrelated_source'))
                continue
            key = (row['tid'], row['thread_lifetime'], p['invocation'])
            identity = [p[k] for k in ('manager', 'manager_epoch', 'source', 'source_epoch')]
            if row['site'] == 0:
                if key in open_calls:
                    incomplete(open_calls.pop(key), 'replaced_invocation')
                call = dict(session_pid=session['pid'], context=list(key), parent=p['parent'],
                    lifetime=identity, lifetime_basis='SYNTHETIC_ORACLE_ONLY',
                    source_geography='0:37536:20928:0029d20e', visited_key=p['visited_key'],
                    query=[p['query_x'], p['query_y']], first_observed_capture=capture,
                    first_ever=False, samples=[capture], decision='PENDING', mask=None,
                    insertion=False, population_complete=False, raw_complete=bool(p['complete']))
                if not all(identity):
                    incomplete(call, 'lifetime_witness')
                elif p['branch'] == 2:
                    decisions.append(dict(call, decision='VISITED_BYPASS', tier='B', missing=[]))
                else:
                    open_calls[key] = call
                continue
            call = open_calls.get(key)
            if call is None:
                rejected.append(dict(capture=capture, reason='missing_invocation'))
                continue
            call['samples'].append(capture)
            if call['lifetime'] != identity or call['query'] != [p['query_x'], p['query_y']]:
                incomplete(open_calls.pop(key), 'identity_or_original_query_changed')
                continue
            call['raw_complete'] &= bool(p['complete'])
            if row['site'] == 1:
                if call['decision'] != 'PENDING' or p['lookup'] > p['capacity']:
                    incomplete(open_calls.pop(key), 'lookup_order_or_bounds')
                else:
                    call['decision'] = 'MAP_MISS' if p['lookup'] == p['capacity'] else 'MAP_HIT'
                    call['lookup'] = p['lookup']
                    call['capacity'] = p['capacity']
                    call['wrapper_at_lookup'] = p['wrapper']
            elif row['site'] == 2:
                if call['decision'] != 'MAP_MISS' or not 0 <= p['mask'] <= 15 or call['mask'] is not None:
                    incomplete(open_calls.pop(key), 'mask_order_or_range')
                else:
                    call['mask'] = p['mask']
            elif row['site'] == 3:
                open_calls.pop(key)
                call['insertion'] = bool(p['inserted'] and p['wrapper'])
                call['population_complete'] = bool(p['ready'])
                if not call['raw_complete']:
                    incomplete(call, 'native_operands')
                elif call['decision'] == 'MAP_HIT' and call.get('wrapper_at_lookup'):
                    decisions.append(dict(call, tier='B', missing=[]))
                elif call['decision'] == 'MAP_MISS' and call['mask'] is not None and call['insertion'] and call['population_complete']:
                    decisions.append(dict(call, tier='A', missing=[]))
                else:
                    incomplete(call, 'mask_or_construction_or_insertion')
    for call in open_calls.values():
        incomplete(call, 'terminal_event')
    decisions.sort(key=lambda d: d['first_observed_capture'])
    return dict(schema='sor-d5e-reduction/1', synthetic=True, decisions=decisions,
        first_observed=decisions[0] if decisions else None, first_ever='UNKNOWN',
        coverage=coverage, rejected=rejected, tier='D' if not decisions else None,
        mask_comparison=[dict(capture=d['first_observed_capture'], mask=d['mask'],
            frozen_alternative=d['mask'] if d['mask'] in (0, 3) else 'NEITHER')
            for d in decisions if d['mask'] is not None],
        native_epoch='UNKNOWN', retail_result='NOT_TESTED')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('events')
    parser.add_argument('output')
    args = parser.parse_args()
    with open(args.events, encoding='utf8') as stream:
        result = reduce(json.load(stream))
    with open(args.output, 'x', encoding='utf8', newline='\n') as stream:
        json.dump(result, stream, indent=2, allow_nan=False)
        stream.write('\n')


if __name__ == '__main__':
    main()
