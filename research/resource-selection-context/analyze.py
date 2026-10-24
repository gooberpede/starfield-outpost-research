# SPDX-License-Identifier: GPL-3.0-or-later
"""Decode verified D4 receipts into a new local operand ledger, without fitting.

Reads only the capture directory and explicit profile. Uses the independent
framing parser; writes an exclusive JSON report. No target, geometry mutation,
save/configuration/analysis-project writes, network or additional dependency.
"""
import argparse
import hashlib
import json
from pathlib import Path
import struct
from qualify import independent, transport, LOCAL


def value(row, name, offset=0, fmt='<I'):
    f = row.get(name, {})
    if f.get('status') != 'COMPLETE':
        return None
    return struct.unpack_from(fmt, bytes.fromhex(f['raw']), offset)[0]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--captures', type=Path, required=True)
    ap.add_argument('--case', required=True)
    ap.add_argument('--output', type=Path, required=True)
    a = ap.parse_args()
    assert a.output.resolve().is_relative_to(LOCAL)
    profiles = Path(__file__).with_name('profiles.json')
    profile = json.loads(profiles.read_text())['cases'][a.case]
    rows, ledger = [], {}
    for p in sorted(a.captures.glob('capture-*.bin')):
        session, row, end = independent(p)
        assert row['schema'] == 'sor-d4-operands/1'
        assert session['exe_sha256'] and end['complete'] == row['required_reads_complete']
        rows.append(dict(path=str(p), sha256=transport.pin(p)))
        if 'invocation_token' not in row:
            continue
        key = (row['pid'], row['tid'], row['thread_lifetime'], row['invocation_token'])
        inv = ledger.setdefault(key, dict(identity=key, events=[], calls=[], terminal=False,
                                          workshop_binding='UNKNOWN', consumer_epoch='UNKNOWN'))
        inv['events'].append(row['capture'])
        if row['site'] == 'generation_entry':
            inv.update(source_pointer=row['source']['address'],
                       source_biom=value(row, 'biom', 0x28),
                       owner=row['owner_key_u32'], upstream_join=row['upstream_join'],
                       entry_complete=row['required_reads_complete'],
                       upstream_captures=[row['upstream_biom_capture'],row['upstream_query_capture']])
        if row['site'] == 'resource_call':
            inv['calls'].append(dict(ires=value(row, 'ires', 0x28),
                main_file=row.get('file_provenance', {}).get('main_file_identity'),
                family=value(row, 'family_root_formid'),
                rsgd=value(row, 'rsgd_record_prefix', 0x28),
                dnam_sha256=hashlib.sha256(bytes.fromhex(row['selected_dnam']['raw'])).hexdigest()
                    if row['selected_dnam']['status'] == 'COMPLETE' else None,
                mask=row['mask_register_raw'], weight_bits=row['effective_weight_bits'],
                selection_chain_complete=row['selection_chain_complete']))
        if row['site'] == 'provider_return':
            inv['terminal'] = row['required_reads_complete']
    for inv in ledger.values():
        expected = profile['expected_source_biom']
        inv['first_numeric_difference'] = ('UNKNOWN_INCOMPLETE_ENTRY' if not inv.get('entry_complete') or not inv.get('upstream_join') else 'OWNER' if inv.get('owner') != int(profile['body'], 16)
            else 'SOURCE_BIOM' if expected and inv.get('source_biom') != int(expected, 16)
            else 'NO_UPSTREAM_NUMERIC_DIFFERENCE_DETECTED')
        inv['qualification'] = 'CANDIDATE_SOURCE_ONLY_NOT_WORKSHOP_OR_EPOCH_BINDING'
    transport.write(a.output, dict(schema='sor-d4-analysis/1', case=a.case,
        profile_sha256=transport.pin(profiles), interpretation='NUMERIC_CONTEXT_COMPARISON_ONLY_NOT_A_NATIVE_WINNER_VERDICT', captures=rows, invocations=list(ledger.values()),
        geometry_replay='NOT_PERFORMED', resource_absence='NOT_INFERRED'))


if __name__ == '__main__':
    main()
