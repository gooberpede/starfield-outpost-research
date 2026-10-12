# SPDX-License-Identifier: GPL-3.0-or-later
"""Read-only schema4 fallback provenance audit; stdout JSON only.

Reads explicit archived session and frozen predictions via project readers.
No process/native execution, save/database access, original writes or network.
Redirect stdout to a NEW ignored derivative. Stdlib/project dependencies only.
Native arithmetic expectations are observations, never generated fixtures.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import struct

from live02_analysis import diagnostic_lifetimes, r, ROOT, guard


def unique(events, kind):
    rows = [e for e in events if e['kind'] == kind]
    if len(rows) != 1:
        raise ValueError('unique_kind:' + str(kind))
    return rows[0]


def args(e, count):
    return list(struct.unpack('<' + 'Q' * count, r.raw(e, 'input_hierarchy', count * 8)[:count * 8]))


def audit(events, module_base):
    lifetime = diagnostic_lifetimes(events)
    reconciled = r.reconcile(events, module_base)
    if len(reconciled['routes']) != 1:
        raise ValueError('one_route_required')
    route = reconciled['routes'][0]
    # The inherited field qualifies a generic component only. Use an explicit
    # name here; never expose it as completed Workshop/model science.
    route['generic_component_qualified'] = route.pop('scientific_complete')
    if route['defects'] or route['path'] != 'FALLBACK_REFERENCE':
        raise ValueError('qualified_fallback_required')
    if len(route['grid']) != 1 or route['grid'][0]['classification'] != 'IDENTITY_BOUND_GENERIC_COMPONENT_REPLAY':
        raise ValueError('qualified_grid_required')
    boundary = {k: unique(events, k) for k in (22, 23, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34)}
    order = [22, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 23]
    if [boundary[k]['sequence'] for k in order] != sorted(boundary[k]['sequence'] for k in order):
        raise ValueError('route_order')
    start, fb, grid = boundary[22], boundary[30], boundary[33]
    ref = r.raw(grid, 'ref', 0xd0)
    if ref != r.raw(fb, 'ref', 0xd0):
        raise ValueError('fallback_reference_changed')
    grid_args = args(grid, 3)
    source_args = args(boundary[31], 3)
    if source_args[2] != args(boundary[29], 5)[1]:
        raise ValueError('source_angles_not_fallback_buffer')
    chosen = r.u64(grid, 'context_raw', 0x18)
    if chosen != r.u64(fb, 'result'):
        raise ValueError('chosen_reference_changed')
    nested_q = [e for e in events if e['kind'] == 7 and boundary[29]['sequence'] < e['sequence'] < fb['sequence']]
    if len(nested_q) != lifetime['Q_normal']:
        raise ValueError('Q_outside_fallback_window')
    cell = r.raw(grid, 'cell', 0x118)
    base = r.raw(grid, 'base', 0x30)
    read32 = lambda b, at: struct.unpack_from('<I', b, at)[0]
    f3 = lambda e, n: list(struct.unpack('<3f', r.raw(e, n, 12)[:12]))
    return dict(
        lifetime=lifetime, kind_counts=dict(sorted(Counter(e['kind'] for e in events).items())),
        route=route, boundaries=[dict(kind=k, sequence=boundary[k]['sequence'], invocation=boundary[k]['invocation'], parent=boundary[k]['parent'], thread=boundary[k]['thread'], args=[hex(v) for v in args(boundary[k], 7 if k in (22, 23) else 6)]) for k in order],
        identity=dict(reference_pointer=hex(chosen), runtime_reference_formid=f'{read32(ref, 0x28):08X}', base_formid=f'{read32(base, 0x28):08X}', runtime_cell_formid=f'{read32(cell, 0x28):08X}', parent_world_pointer=hex(grid['blobs']['center']['address']), runtime_parent_world_formid=f'{read32(r.raw(grid, "center", 0x30), 0x28):08X}', native_handle='NOT_CAPTURED', persistent_save_join='NOT_ESTABLISHED'),
        request_angles_hex=r.raw(start, 'source', 16)[:16].hex(),
        fallback_input_angles_hex=r.raw(boundary[29], 'candidate', 16)[:16].hex(),
        fallback_output_angles_hex=r.raw(fb, 'candidate', 16)[:16].hex(),
        final_angles_hex=r.raw(boundary[23], 'center', 16)[:16].hex(),
        fallback_local_xyz=f3(fb, 'center'), route_residual_xyz=f3(grid, 'translation'),
        sampled_reference_xyz=list(struct.unpack_from('<3f', ref, 0x8c)),
        route_source_null=args(start, 7)[3] == 0, route_known_null=args(start, 7)[4] == 0,
        adjust_low_byte=args(start, 7)[6] & 255,
        grid_pointer=hex(grid_args[1]), source_pointer=hex(source_args[1]),
        descriptor_before=r.raw(grid, 'candidate', 44).hex(), descriptor_after=r.raw(boundary[34], 'candidate', 44).hex(),
        generic_native_observations=len(route['grid']), native_nonzero_observations=sum(g['native_floor'] != [0, 0] for g in route['grid']),
        frozen_workshop_comparison='NOT_TESTED; generic component has no compensated-workshop identity')


def main(session):
    guard()
    files = [p for p in sorted(session.iterdir()) if p.is_file()]
    hashes = lambda: {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    before = hashes()
    original = r.inspect(session)
    events, integrity = r.records(session)
    ready = json.loads((session / 'ready.json').read_text())
    result = audit(events, int(ready['module_base'], 16))
    predictions = ROOT / 'docs/experiments/engine-oracle/predictions.json'
    prediction_bytes = predictions.read_bytes()
    if len(json.loads(prediction_bytes)) != 23 or hashlib.sha256(prediction_bytes).hexdigest() != r.PREDICTION_HASH:
        raise ValueError('frozen_predictions_changed')
    if before != hashes():
        raise ValueError('input_changed')
    inventory = []
    for folder in sorted(session.parent.glob('session-*')):
        if not (folder / 'ready.json').exists():
            continue
        metadata = json.loads((folder / 'ready.json').read_text())
        if metadata.get('event_size') != r.SIZE or metadata.get('schema') not in (1, 2, 3, 4):
            inventory.append(dict(session=folder.name, version=metadata.get('version'),
                status='NOT_DECODED_UNQUALIFIED_SCHEMA', ready_sha256=hashlib.sha256((folder / 'ready.json').read_bytes()).hexdigest()))
            continue
        rows, check = r.records(folder)
        # Only common raw/header transport is decoded here; this is no claim
        # that the schema4 scientific reconciler validates earlier versions.
        inventory.append(dict(session=folder.name, version=metadata['version'],
            integrity=check, kinds=dict(sorted(Counter(e['kind'] for e in rows).items())),
            raw_sha256=hashlib.sha256((folder / 'events.bin').read_bytes()).hexdigest()))
    print(json.dumps(dict(result=result, integrity=integrity, original_capture_complete=original['capture_complete'], worker_complete=original['worker_complete'], retirement_complete=original['retirement_complete'], inputs_sha256=before, predictions_sha256=r.PREDICTION_HASH, retained_session_inventory=inventory), indent=2))


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('session', type=Path)
    main(p.parse_args().session)
