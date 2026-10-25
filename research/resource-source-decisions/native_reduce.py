# SPDX-License-Identifier: GPL-3.0-or-later
"""Reduce native stopped snapshots conservatively to tier C or no-decision D.

Reads JSON rows supplied by a future explicitly authorized native acquisition.
Writes an exclusive offline report. No process, save, database, network or Git
effects. Synthetic epoch packets are rejected rather than accepted as retail.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import struct

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('owned_d5b_reduce', ROOT / 'research/resource-combined-acquisition/reduce.py')
owned = importlib.util.module_from_spec(spec)
spec.loader.exec_module(owned)


def raw(row, field, length):
    value = row.get(field)
    if not isinstance(value, dict) or not value.get('complete'):
        raise ValueError(field + ':incomplete_read')
    try:
        data = bytes.fromhex(value['raw'])
    except (KeyError, TypeError, ValueError):
        raise ValueError(field + ':invalid_hex') from None
    if len(data) != length:
        raise ValueError(field + ':wrong_length')
    return data


def reduce(rows):
    result, rejected, coverage = [], [], []
    session = None
    armed = False
    last = 0
    for order, row in enumerate(rows):
        kind = row['kind']
        if kind == 'SESSION':
            if session is not None:
                raise ValueError('multiple_native_sessions')
            if not (row.get('synthetic') is False and row.get('schema') == 'sor-d5e/1'
                    and row.get('image_sha256') == '7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28'
                    and isinstance(row.get('pid'), int) and row['pid'] > 0
                    and isinstance(row.get('module_base'), int) and row['module_base'] >= 0x10000):
                raise ValueError('unpinned_native_session')
            session = dict(row)
        elif kind == 'ARM_BARRIER':
            armed = bool(session and row.get('readback') and row.get('slots') == 4 and row.get('all_threads', 0))
            coverage.append(dict(order=order, state='ARMED' if armed else 'GAP', reason='arm_barrier'))
        elif kind in ('GAP', 'EXIT', 'STOP_COMMITTED'):
            armed = False
            coverage.append(dict(order=order, state='CLOSED' if kind == 'EXIT' else 'GAP', reason=kind))
        elif kind == 'SAMPLE':
            try:
                if row['capture'] != last + 1:
                    armed = False
                    coverage.append(dict(order=order, state='GAP', reason='capture_sequence'))
                    raise ValueError('capture_sequence')
                last = row['capture']
                if not (session and armed and row.get('native') and row.get('frame_valid')):
                    raise ValueError('session_coverage_or_native_frame')
                if row['site'] not in range(4) or row.get('rip') != session['module_base'] + (0x79fca3, 0x79fcd0, 0x79b8ed, 0x79feaf)[row['site']]:
                    raise ValueError('native_site_address')
                source = raw(row, 'source', 0x70)
                manager = raw(row, 'manager', 0x200)
                if source != raw(row, 'source_again', 0x70):
                    raise ValueError('source_changed_at_stop')
                if manager != raw(row, 'manager_again', 0x200):
                    raise ValueError('manager_changed_at_stop')
                if raw(row, 'manager_pointer', 8) != raw(row, 'manager_pointer_again', 8):
                    raise ValueError('manager_replaced_at_stop')
                missing = ['native_lifetime_fence', 'associated_definition_file_identity', 'completed_construction_event']
                missing += [name + ':incomplete_read' for name, value in row.items()
                            if isinstance(value, dict) and value.get('complete') is False]
                query = None
                try:
                    query = raw(row, 'original_query', 8)
                    if query != raw(row, 'original_query_again', 8):
                        raise ValueError('original_query_changed_at_stop')
                except ValueError as error:
                    missing.append(str(error))
                    query = None
                offset = 0x1c0 if manager[0x20] == 3 else 0xc8
                key = owned.source_key(source, manager[offset:offset+0x2c])
                if key != owned.SOURCE:
                    raise ValueError('unrelated_or_unsupported_source_geography')
                if struct.unpack_from('<I', manager, 0x80)[0] != owned.BODY:
                    raise ValueError('unrelated_owner')
                site = row['site']
                operand = row['decision_operand']
                if site == 0:
                    if operand not in (0, 1) or row.get('visited_key_operand') != struct.unpack_from('<Q', source, 0x68)[0]:
                        raise ValueError('visited_operand_or_key')
                    decision = 'VISITED_BYPASS' if operand else 'VISITED_NOT_FOUND'
                elif site == 1:
                    capacity = struct.unpack('<Q', raw(row, 'capacity', 8))[0]
                    if not 0 <= operand <= capacity:
                        raise ValueError('lookup_capacity_bounds')
                    decision = 'MAP_MISS' if operand == capacity else 'MAP_HIT'
                    if operand < capacity:
                        slot = raw(row, 'lookup_slot', 24)
                        if slot[:8] != raw(row, 'source_pointer', 8) or struct.unpack_from('<I', slot, 16)[0] == 0xffffffff:
                            raise ValueError('lookup_slot_identity_or_occupancy')
                        if struct.unpack_from('<Q', slot, 8)[0] == 0:
                            missing.append('retained_wrapper_null')
                elif site == 2:
                    if not 0 <= operand <= 15:
                        raise ValueError('sampled_mask_range')
                    try:
                        raw(row, 'geographic_query', 0x18)
                    except ValueError as error:
                        missing.append(str(error))
                    decision = 'SAMPLED_MASK'
                else:
                    try:
                        if query is None or query != raw(row, 'conversion_original_query', 8):
                            raise ValueError('conversion_query_mismatch_or_missing')
                        raw(row, 'conversion_descriptor', 0x2c)
                    except ValueError as error:
                        missing.append(str(error))
                    decision = 'ORIGINAL_QUERY_AT_CONVERSION'
                result.append(dict(order=order, capture=row['capture'], decision=decision,
                    tier='C' if site in (0, 1) else 'D', original_query=list(struct.unpack('<2i', query)) if query else None,
                    mask=operand if site == 2 else None, source_geography=key,
                    association_validation='INTERIOR_FRAME_AND_OWNER_ONLY',
                    context=[row['tid'], row['thread_lifetime'], row['provider_working_rsp']],
                    manager_lifetime=None, source_lifetime=None, first_ever=False,
                    missing=missing, session=dict(session), native_read_complete=row.get('native_read_complete', False),
                    ancestry='UNJOINED_STOPS'))
            except (KeyError, ValueError, struct.error) as error:
                rejected.append(dict(order=order, capture=row.get('capture'), site=row.get('site'),
                    context=[row.get('tid'), row.get('thread_lifetime'), row.get('provider_working_rsp')],
                    reason=str(error), session=session))
                if row['capture'] != last:
                    armed = False
                    last = row['capture']
    decisions = [r for r in result if r['tier'] == 'C']
    return dict(schema='sor-d5e-native-reduction/1', synthetic=False, session=session, observations=result,
        rejected=rejected, coverage=coverage, first_observed=decisions[0] if decisions else None,
        first_ever='UNKNOWN', tier='C' if decisions else 'D',
        frozen_comparison=[dict(capture=r['capture'], mask=r['mask'],
            alternative=r['mask'] if r['mask'] in (0, 3) else 'NEITHER')
            for r in result if r['mask'] is not None])


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
