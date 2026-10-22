# SPDX-License-Identifier: GPL-3.0-or-later
"""Offline independent receipt/accounting and scoped native interpretation.

Reads closed retail receipts, ACKs, pinned static sources and installed witness
metadata. Writes one new ignored JSON derivative; never edits raw evidence,
saves, game state, analysis database or Git metadata. Stdlib/owned C1B decoder.
"""
import argparse
import collections
import json
from pathlib import Path
import struct
from collect import LOCAL, ROOT, pin, receipt, write


def qword(context, offset):
    # Windows x64 CONTEXT layout, as serialized by the compiled controller.
    return struct.unpack_from('<Q', bytes.fromhex(context), offset)[0]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--attempt', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    a = ap.parse_args()
    folder, out = a.attempt.resolve(), a.output.resolve()
    assert folder.is_relative_to(LOCAL) and out.is_relative_to(LOCAL) and not out.exists()
    result = json.loads((folder / 'result.json').read_text(encoding='utf8'))
    rows = [json.loads(line) for line in (folder / 'events.jsonl').read_text(encoding='utf8').splitlines()]
    session = next(r for r in rows if r['kind'] == 'SESSION')
    base = session['module_base']
    samples = [r for r in rows if r['kind'] == 'SAMPLE']
    assert result['captures'] == result['acknowledgements'] == len(samples)
    acks, source_qualified, gates = [], [], []
    live, sequence, pending = {}, {}, {}
    for row in rows:
        kind = row['kind']
        if kind == 'THREAD_BEGIN':
            assert row['tid'] not in live
            live[row['tid']] = row['lifetime']
        elif kind == 'THREAD_END':
            assert row['tid'] in live
            del live[row['tid']]
        elif kind == 'SAMPLE':
            n = row['capture']
            assert n == len(acks)+1 and row['pid'] == session['pid']
            assert live[row['tid']] == row['thread_lifetime']
            t = row['thread_lifetime']
            sequence[t] = sequence.get(t, 0)+1
            assert row['thread_sequence'] == sequence[t]
            path = folder / f'capture-{n:05d}.bin'
            ack = json.loads(path.with_suffix('.ack.json').read_text(encoding='utf8'))
            raw = path.read_bytes()
            decoded = receipt.decode(raw)
            assert ack['synthetic'] is False and ack['bytes'] == len(raw) and ack['sha256'] == pin(path)
            assert decoded[0] == session and decoded[1] == row
            assert qword(row['raw_context'], 0xf8) == row['rip'] == base+row['site_rva']
            acks.append(dict(capture=n, bytes=len(raw), sha256=pin(path), complete=decoded[-1]['complete']))
            if row['site'] == 'spatial_transfer_payload':
                extra = bytes.fromhex(row['raw_binding_extra'])
                ref = bytes.fromhex(row['raw_binding_reference'])
                definition = bytes.fromhex(row['raw_binding_base'])
                caller = row['caller_return']-base
                bound = (caller in (0x21b26c1, 0x21b6936) and row['saved_caller_r14'] == row['binding_reference']
                         and qword(row['raw_context'], 0xe0) == base+0x5f5d618
                         and qword(row['raw_context'], 0xe8) == base+0x5f5d800
                         and ref[0x2e] == 0x4a and definition[0x2e] == 0x1e
                         and struct.unpack_from('<I', definition, 0x28)[0] == 0x2c60e9
                         and struct.unpack_from('<Q', extra)[0] == base+0x4c24e60
                         and extra[0x12] == 0xbc and extra[0x98:0xa0].hex() == 'c3a5866f4cfcf585')
                payload = row['refresh_payload']
                identities = []
                for p in row.get('payload_file_provenance', []):
                    matches = [m for m in payload['members'] or [] if m['pointer'] == p['resource_pointer']]
                    assert len(matches) == 1
                    member = matches[0]
                    assert member['runtime_formid'] == p['runtime_formid']
                    header = bytes.fromhex(member['raw'])
                    assert struct.unpack_from('<I', header, 0x28)[0] == member['runtime_formid']
                    assert header[0x2e] == member['type'] == 0x9f
                    proof = p['provenance']
                    qualified = proof['status'] == 'COMPLETE' and proof['count'] == 1 and len(proof['files']) == 1
                    if qualified:
                        f = proof['files'][0]
                        prefix = bytes.fromhex(f['raw_prefix'])
                        name = prefix[0x38:0x13c].split(b'\0', 1)[0].decode('ascii')
                        flags = struct.unpack_from('<I', prefix, 0x1b8)[0]
                        qualified = (name == f['name'] == 'Starfield.esm' and prefix[0x218] == f['full_index'] == 0
                                     and not flags & 0x700 and p['runtime_formid'] >> 24 == 0
                                     and struct.unpack_from('<Q', prefix)[0] in (base+0x4b29a70, base+0x4b29b80))
                    if qualified:
                        assert proof['main_file_identity']
                        identities.append(f'Starfield.esm:{p["runtime_formid"]:06x}')
                source_qualified.append(dict(capture=n, original_identity=row['identity'], caller_rva=hex(caller),
                    source_qualified_P3=bool(bound), source='spatial_refresh_transfer_input_before_install',
                    payload_status=payload['status'], runtime_ids=[m['runtime_formid'] for m in payload['members'] or []],
                    plugin_qualified_resources=identities, generation_age='UNKNOWN', shared_cache_ancestry='UNKNOWN'))
            elif row['site'] == 'catalogue_selected_population':
                pending[t] = row
            elif row['site'] == 'catalogue_grid_return' and row['matched_selected_input']:
                selected = pending[t]
                assert selected['grid_caller'] and selected['node_pointer'] == row['node_pointer']
                assert qword(selected['raw_context'], 0xa0)+0x67 == qword(row['raw_context'], 0x98)
                tag = selected['selected_population']
                if tag != 'UNKNOWN' and selected['produced']['status'] == selected['populations'][tag]['status'] == 'COMPLETE':
                    wanted = {m['pointer'] for m in selected['produced']['members']}
                    available = {m['pointer'] for m in selected['populations'][tag]['members']}
                    assert bool(wanted & available) == bool(row['actual_filter_al'])
                gates.append(dict(input_capture=selected['capture'], return_capture=n, source=tag,
                    produced_runtime_ids=[m['runtime_formid'] for m in selected['produced']['members'] or []],
                    actual_filter_al=row['actual_filter_al'], P3_identity='UNKNOWN'))
    accepted = [r for r in rows if r['kind'] == 'ACK_ACCEPTED' and r['accepted']]
    exits = [r for r in rows if r['kind'] == 'EXIT']
    assert len(accepted) == len(samples) and len(exits) == 1 and exits[0]['captures'] == len(samples)
    sources = [ROOT / '.local-work/recon/resource-availability-ui-15.tsv',
               ROOT / 'docs/experiments/resource-geometry-observation/cases.md']
    for p in (LOCAL / 'native').glob('*.tsv'):
        sources.append(p)
    write(out, dict(schema='sor-c1d-retail-analysis/1', status='VERIFIED_SCOPED', synthetic=False,
        raw_receipt_directory=str(folder), raw_files={p.name: pin(p) for p in folder.iterdir() if p.is_file()},
        session=session, census=dict(collections.Counter(r['site'] for r in samples)), acknowledgements=acks,
        source_qualified_transfers=source_qualified, diagnostic_catalogue_pairs=gates, exit=exits[0],
        source_pins={str(p): pin(p) for p in sources}, analyzer_sha256=pin(__file__),
        limits='No raw reclassification or edits. Shared vectors at transfer are pre-install. '
               'No region coordinates, generation age, defining/winning-file semantics, full load map, '
               'P3-bound catalogue outcome, placement or production claim.'))
    print(out, 'verified samples', len(samples), 'transfers', source_qualified, 'diagnostic gate pairs', len(gates))


if __name__ == '__main__':
    main()
