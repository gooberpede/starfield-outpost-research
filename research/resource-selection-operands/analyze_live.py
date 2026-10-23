# SPDX-License-Identifier: GPL-3.0-or-later
"""OFFLINE analysis of closed C1G SRO1/ACK/events and frozen requests.

Reads local receipts, owned decoder/CRC/MT arithmetic and installed-definition
provenance; writes one fresh ignored JSON. No process, save/configuration,
database, network or Git operation. Does not change collector/build05 sources.
All numeric native observations remain separate from derived model checks.
"""
import argparse
import collections
import hashlib
import json
from pathlib import Path
import struct
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'save-analysis/scripts'))
from resource_availability import generation_first_gate
from qualify import independent
from readiness import Tracker


def pin(path):
    with Path(path).open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def raw(row, name):
    g = row[name]
    assert g['status'] == 'COMPLETE' and g['raw'] is not None
    b = bytes.fromhex(g['raw'])
    assert len(b) == g['bytes']
    return b


def u64(row, name):
    return struct.unpack('<Q', raw(row, name))[0]


def fbits(bits):
    return struct.unpack('<f', struct.pack('<I', bits))[0]


def bits(value):
    return struct.unpack('<I', struct.pack('<f', value))[0]


def key(row):
    return row['pid'], row['tid'], row['thread_lifetime'], row['invocation_token']


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--receipts', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    a = ap.parse_args()
    local = ROOT/'.local-work/resource-selection-operands'
    assert a.receipts.resolve().is_relative_to(local) and a.output.resolve().is_relative_to(local)
    assert not a.output.exists()
    events = a.receipts/'events.jsonl'
    rows = [json.loads(l) for l in events.read_text(encoding='utf8').splitlines()]
    session = rows[0]
    assert session['kind'] == 'SESSION' and session['synthetic'] is False
    assert session['exe_sha256'] == '7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28'
    accounting = json.loads((a.receipts/'accounting.json').read_text(encoding='utf8'))
    samples = [r for r in rows if r['kind'] == 'SAMPLE']
    assert accounting['controller_exit'] == 0 and accounting['captures'] == accounting['accepted_acks'] == len(samples)
    assert len(list(a.receipts.glob('capture-*.bin'))) == len(samples)
    assert rows[-1]['kind'] == 'EXIT' and rows[-1]['stopped'] and rows[-1]['open_invocations'] == 0
    assert not any(r['kind'] in ('EXCEPTION', 'LOSS') for r in rows)
    acks = [r for r in rows if r['kind'] == 'ACK_ACCEPTED']
    assert [r['capture'] for r in acks] == list(range(1, len(samples)+1)) and all(r['accepted'] for r in acks)
    assert [r['capture'] for r in rows if r['kind'] == 'RESUME_VERIFIED'] == list(range(1, len(samples)))
    live_threads, sequence = {}, {}
    for r in rows:
        if r['kind'] == 'THREAD_BEGIN':
            assert r['tid'] not in live_threads
            live_threads[r['tid']] = r['lifetime']
        elif r['kind'] == 'THREAD_END':
            assert live_threads.pop(r['tid']) == r['lifetime'] and r['unwitnessed_terminals'] == 0
        elif r['kind'] == 'SAMPLE':
            assert r['pid'] == session['pid'] and live_threads[r['tid']] == r['thread_lifetime']
            k = r['tid'], r['thread_lifetime']
            sequence[k] = sequence.get(k, 0)+1
            assert sequence[k] == r['thread_sequence']
    freeze_path = ROOT/'.local-work/resource-geometry-mature-context/site-feynman-initial02.json'
    assert pin(freeze_path) == '6f40b0d3166796bbdabb31dd8cd4a00dbfc9da144eb13ba3a336367d2f6c539b'
    frozen = json.loads(freeze_path.read_text(encoding='utf8'))
    by_origin = {tuple(s['request']['origin']):s['request'] for s in frozen['sources']}
    provenance = json.loads((local/'provenance01.json').read_text(encoding='utf8'))
    dnam_owners = collections.defaultdict(list)
    for record in provenance['selected_main_records']:
        resource = None
        if record['type'] != 'RSGD':
            continue
        for tag, data in record['fields']:
            if tag == 'RNAM':
                resource = int.from_bytes(bytes.fromhex(data), 'little')
            if tag == 'DNAM':
                dnam_owners[data].append(dict(rsgd=record['formid'], editor_id=record['editor_id'], root_resource=resource))
    active, completed, unbound, selected = {}, [], [], []
    tracker, useful = Tracker(), []
    derived_checks = collections.Counter()
    for i, r in enumerate(samples, 1):
        assert r['capture'] == i and r['synthetic'] is False
        path = a.receipts/f'capture-{i:05d}.bin'
        frames = independent(path)
        ack = json.loads(path.with_suffix('.ack.json').read_text(encoding='utf8'))
        assert ack['synthetic'] is False and ack['status'] == 'DURABLE_READBACK'
        assert frames == [session, r, dict(kind='END', complete=r['required_reads_complete'])]
        slot = ('generation_entry', 'resource_call', 'chance_branch', 'provider_return').index(r['site'])
        assert r['site_rva'] == session['sites'][slot]['rva'] and r['rip'] == session['module_base']+r['site_rva']
        assert r['frame_matches'] and r['entry_bound']
        assert all(g['status'] == 'COMPLETE' for g in r.values() if isinstance(g, dict) and 'address' in g and 'status' in g)
        if tracker.observe(r):
            useful.append(i)
        k = key(r)
        if r['site'] == 'generation_entry':
            assert k not in active and r['unwitnessed_terminals'] == 0
            source = raw(r, 'source')
            origin = struct.unpack('<ii', raw(r, 'origin'))
            active[k] = dict(key=k, entry_capture=i, origin=origin, owner=r['owner_key_u32'],
                             biom=struct.unpack_from('<I', raw(r, 'biom'), 0x28)[0],
                             source_pointer=r['source']['address'], source_frame=list(struct.unpack_from('<8i', source, 0x10)),
                             source_descriptor_bits=raw(r, 'source_descriptor').hex(),
                             historical_epoch=None, calls=[], cells=[], unbound=[])
            assert r['owner_matches_manager'] and r['owner_key_u32'] == 385246
        inv = active[k]
        if r['site'] == 'resource_call':
            assert r['required_reads_complete'] and r['file_provenance']['main_file_identity']
            resource = struct.unpack_from('<I', raw(r, 'ires'), 0x28)[0]
            weight = fbits(r['effective_weight_bits'])
            call = dict(capture=i, resource=resource, weight_bits=r['effective_weight_bits'], weight=weight,
                        rarity=r['rarity_raw'], ordinary_mask=r['mask_register_raw'], mask_branch=r['mask_branch'],
                        mask_basis=r['mask_branch_basis'], chance_bits=r['cell_chance_bits'],
                        chance=fbits(r['cell_chance_bits']), selected_dnam_pointer=r['selected_dnam']['address'],
                        selected_dnam_sha256=hashlib.sha256(raw(r, 'selected_dnam')).hexdigest(),
                        matching_main_definitions=dnam_owners.get(raw(r, 'selected_dnam').hex(), []),
                        rsgd_pointer=u64(r, 'component_selected_rsgd_pointer'),
                        family_root=int.from_bytes(raw(r, 'family_root_formid'), 'little'))
            if 'inactive_setting' in r:
                call['setting_payload_address'] = r['inactive_setting']['address']
                call['setting_payload_bits'] = raw(r, 'inactive_setting').hex()
                assert int.from_bytes(raw(r, 'inactive_setting'), 'little') == r['effective_weight_bits']
            inv['calls'].append(call)
        if r['site'] == 'chance_branch':
            cell = struct.unpack('<ii', raw(r, 'cell_xy_i32'))
            if not r['resource_call_join']:
                assert not r['required_reads_complete']
                assert u64(r, 'resource_return') == session['module_base']+0x79c11c
                # RSI is at byte offset 0xa8 in the captured Windows AMD64 CONTEXT.
                # This identifies a diagnostic pointer; it never repairs raw END.
                resource_pointer = struct.unpack_from('<Q', bytes.fromhex(r['raw_context']), 0xa8)[0]
                unbound.append(dict(capture=i, key=k, caller_return_rva=0x79c11c,
                                    resource_pointer=resource_pointer, cell=cell,
                                    classification='OUTSIDE_ORDINARY_CALL_CONTRACT'))
                inv['unbound'].append(i)
                continue
            assert r['required_reads_complete']
            call = inv['calls'][-1]
            assert u64(r, 'cell_dnam_pointer') == call['selected_dnam_pointer']
            chance = struct.unpack_from('<f', raw(r, 'chance_block'), 28)[0]
            assert bits(chance) == call['chance_bits']
            packed_key = u64(r, 'packed_key_u64')
            derived = generation_first_gate(packed_key, inv['owner'], chance, call['weight'])
            assert bits(derived['draw100']) == r['draw_times_100_bits']
            assert bits(derived['threshold']) == r['threshold_bits']
            assert derived['first_gate_pass'] == (r['chance_edge'] == 'ADMIT')
            derived_checks['first_gate'] += 1
            req = by_origin.get(tuple(inv['origin']))
            if req:
                assert req['packed_keys'][f'{cell[0]},{cell[1]}'] == packed_key
                derived_checks['frozen_key'] += 1
            datum = dict(capture=i, resource=call['resource'], cell=cell, packed_key=packed_key,
                         weight_bits=call['weight_bits'], draw_bits=r['draw_times_100_bits'],
                         threshold_bits=r['threshold_bits'], chance_edge=r['chance_edge'],
                         seed=derived['seed'], seed_basis='DERIVED_CRC_NOT_DIRECT_OBSERVATION')
            inv['cells'].append(datum)
            if cell in ((10, 1), (11, 1), (10, 12), (11, 12)):
                selected.append(dict(datum, invocation=k, origin=inv['origin']))
        if r['site'] == 'provider_return':
            assert r['required_reads_complete']
            inv['terminal_capture'] = i
            inv['modeled_source'] = by_origin.get(tuple(inv['origin']), {}).get('source')
            completed.append(inv)
            del active[k]
    assert not active and useful == [len(samples)]
    out = dict(schema='sor-c1g-phaseb-analysis/1', session=session, events_sha256=pin(events),
               accounting=accounting, samples=len(samples), sites=dict(collections.Counter(r['site'] for r in samples)),
               raw_complete=sum(r['required_reads_complete'] for r in samples),
               raw_incomplete=len(unbound), unbound=unbound, invocations=completed,
               selected_cells=selected, derived_checks=dict(derived_checks), useful_terminals=useful,
               max_read_bytes=max(r['read_bytes'] for r in samples), max_copy_ms=max(r['copy_ms'] for r in samples),
               predecessor_geometry=None, current_accepted_paths=None, historical_c1e_join=None,
               frozen_sha256=pin(freeze_path), provenance_sha256=pin(local/'provenance01.json'),
               analyzer_sha256=pin(Path(__file__)), evidence_class='LOCAL-ONLY')
    with a.output.open('x', encoding='utf8', newline='\n') as f:
        json.dump(out, f, indent=2)
        f.write('\n')
    print(json.dumps(dict(samples=len(samples), raw_complete=out['raw_complete'], unbound=len(unbound),
                          sites=out['sites'], useful=useful, derived_checks=out['derived_checks'],
                          invocations=[dict(entry=x['entry_capture'], terminal=x['terminal_capture'], origin=x['origin'],
                                            biom=x['biom'], resources=[(c['resource'],c['weight']) for c in x['calls']]) for x in completed]), indent=2))


if __name__ == '__main__':
    main()
