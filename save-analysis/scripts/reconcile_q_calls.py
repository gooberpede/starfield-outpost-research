"""SPDX-License-Identifier: GPL-3.0-or-later
Offline Q ledger, original project analysis of schema2 and pinned native code.
Reads a retained session, original journal/health, monitor, ESM catalog and pins.
Writes an exclusive NEW ignored directory after 40GB C:/D: guards; stdout summary.
No process/native calls, game/save/config/database edits, installs or network.
Raw pointers/bytes stay LOCAL-ONLY. Source: docs/experiments/q-to-e-control-flow.md.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import struct
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'runtime/native-oracle-020'))
from inspect_events import inspect, raw
from verify_position_v2 import guard, digest
from position_quantizer_diagnostic import diagnose


def packed_key(data):
    """Exact bit extraction; NOT the landscape-dependent96FB40 result."""
    if len(data) != 8:
        raise ValueError('PACKED_KEY_LENGTH')
    k = int.from_bytes(data, 'little')
    return dict(hex=data.hex(), system_id=(k >> 41) & 0x3ffff,
                body_index=(k >> 35) & 0x3f, tag=(k >> 32) & 7,
                packed_xy=[k & 0xffff, (k >> 16) & 0xffff])


def separation(bounds, delta, shift):
    """AD0B1C..56: signed32 rectangle disjointness, not a containment test."""
    if len(bounds) != 4 or len(delta) != 2 or len(shift) != 4:
        raise ValueError('RECTANGLE_ARITY')
    signed = lambda v: ((v + 2**31) % 2**32) - 2**31
    left, right = (signed(shift[i] + delta[0]) for i in (0, 1))
    bottom, top = (signed(shift[i] + delta[1]) for i in (2, 3))
    return bounds[0] > right or left > bounds[1] or bounds[2] > top or bottom > bounds[3]


def saved_token_for_candidate(key):
    """Proposed tagged numeric correspondence, not a proven runtime remapping."""
    if not 0 <= key <= 0xffffffff or key>>24 not in (0,0xff):
        raise ValueError('UNSUPPORTED_CANDIDATE_ID_DOMAIN')
    return ((key&0x3fffff)|(0x800000 if key>>24==0xff else 0x400000)).to_bytes(3,'little').hex()


def event_row(begin, end, journal):
    c, w, candidate = (raw(begin, n) for n in ('context_raw', 'world', 'candidate'))
    args = struct.unpack('<3Q', raw(begin, 'input_hierarchy'))
    if args != (begin['reference'], begin['context'], 0):
        raise ValueError('ARGUMENT_SNAPSHOT_MISMATCH')
    fields = struct.unpack('<5Q', c)
    lon, lat, fid, tail = struct.unpack('<ddII', candidate)
    result = raw(end, 'result')
    output_before, output_after = raw(begin, 'center'), raw(end, 'center')
    mutations = [n for n in ('context_raw', 'candidate', 'world', 'translation', 'center')
                 if raw(begin, n) != raw(end, n)]
    diagnostic=diagnose(lon,lat)
    diagnostic['boundary_mxcsr_hex']=f'{begin["mxcsr"]:08x}'
    diagnostic['boundary_rounding_mode']=(begin['mxcsr']>>13)&3
    diagnostic['boundary_ftz']=bool(begin['mxcsr']&0x8000)
    diagnostic['boundary_daz']=bool(begin['mxcsr']&0x40)
    for item in [diagnostic,*diagnostic['dispatch_candidates'].values()]:
        item['unknowns']=[u if u!='MXCSR environment' else
            'within-helper environment preservation and scalar provider equivalence'
            for u in item['unknowns']]
    return dict(invocation=begin['invocation'], thread=begin['thread'], parent=begin['parent'],
        begin_sequence=begin['sequence'], end_sequence=end['sequence'],
        begin_qpc=begin['qpc'], end_qpc=end['qpc'], mxcsr=begin['mxcsr'],
        arguments_hex=[f'{v:016x}' for v in args], context_fields_hex=[f'{v:016x}' for v in fields],
        journal=[journal[begin['sequence']], journal[end['sequence']]],
        snapshots={label: {n: e['blobs'][n] for n in ('context_raw', 'candidate', 'world',
            'translation', 'center', 'source', 'input_hierarchy', 'result')}
            for label, e in [('begin', begin), ('end', end)]},
        candidate_hex=candidate.hex(), angle_hex=[candidate[:8].hex(), candidate[8:16].hex()],
        longitude=lon, latitude=lat, candidate_form=f'{fid:08X}', tail_hex=candidate[20:].hex(),
        output_before_hex=output_before.hex(), output_after_hex=output_after.hex(),
        return_hex=result.hex(), uint32_return=int.from_bytes(result, 'little'),
        observed_mutated_blobs=mutations, source_key=packed_key(w[0x310:0x318]),
        query_world_form=f'{struct.unpack_from("<I",w,0x28)[0]:08X}', query_world_type=w[0x2e],
        bounds=list(struct.unpack('<4i', raw(begin, 'translation'))),
        # Both angular modes are predictions only. Never use this to assert a live branch.
        angular_diagnostic=diagnostic,
        predicates=dict(output_nonzero_at_entry=output_before != b'\0',
            output_nonzero_at_exit=output_after != b'\0',
            candidate_id_nonzero=fid != 0, descriptor_tail_zero=tail == 0,
            resolver_result='UNKNOWN', overlay_result='UNKNOWN', active_landscape='UNKNOWN',
            hierarchy_equality='UNKNOWN', overlay_bit0='UNKNOWN', rectangle_separation='UNKNOWN'),
        path='UNRESOLVED: early unchanged-latch return OR hierarchy/flag skip plus disjoint rectangle',
        association='No E/C/center/grid child in qualified invocation; no proximity join')


def reconcile(session, output):
    space = guard()
    if output.exists():
        raise FileExistsError(output)
    # Before any derivative: hash every original session file plus original pins.
    manifest = ROOT/'.local-work/native-oracle-020/operations/continuation-live-evidence-manifest-01.json'
    prior = json.loads(manifest.read_text())
    paths = set(p for p in session.iterdir() if p.is_file()) | {manifest}
    paths |= {ROOT/r['path'] for r in prior['files']}
    post = json.loads((ROOT/'.local-work/native-oracle-020/operations/continuation-live-postflight-01.json').read_text())
    paths |= {Path(r['path']) for r in post['checks'] if 'path' in r}
    supplement = ROOT/'.local-work/native-oracle-020/operations/continuation-live-postflight-supplement-01.json'
    checkpoint_pins=json.loads(supplement.read_text())['new_checkpoint_pins']
    paths |= {supplement} | {Path(r['path']) for r in checkpoint_pins}
    catalog = ROOT/'.local-work/save-capacity-location/esm-index-verified.json'
    cat = json.loads(catalog.read_text())
    paths |= {catalog, Path(cat['source']['path'])}
    # N1 saves are originals, never overwritten or used as model expectations.
    paths |= set(Path('C:/Users/User/Documents/My Games/Starfield/Saves').glob('Save2[78]_*.sfs'))
    paths |= set((ROOT/'runtime/native-oracle-020').glob('*.*'))
    paths |= {ROOT/'docs/experiments/engine-oracle/predictions.json'}
    before = {str(p): digest(p) for p in sorted(paths)}
    for r in prior['files']:
        if before[str(ROOT/r['path'])] != r['sha256']:
            raise ValueError('PRIOR_EVIDENCE_PIN')
    for r in post['checks']:
        if 'path' in r and before[str(Path(r['path']))] != r['expected']:
            raise ValueError('PROTECTED_PIN')
    for r in checkpoint_pins:
        if before[str(Path(r['path']))] != r['sha256']:
            raise ValueError('N1_SAVE_PIN')
    if before[str(Path(cat['source']['path']))] != cat['source']['sha256']:
        raise ValueError('ESM_PIN')
    result = inspect(session)
    if not result['diagnostics']['worker_evidence_qualified']:
        raise ValueError('UNQUALIFIED_CAPTURE')
    events = result['raw_events']
    journal = {r['sequence']:r for r in map(json.loads, (session/'records.jsonl').read_text().splitlines())}
    rows = []
    for scope in result['diagnostics']['scope_rows']:
        items = [e for e in events if e['invocation'] == scope['invocation']]
        if not scope['normal_complete'] or [e['kind'] for e in items] != [7, 8]:
            raise ValueError('EXPECTED_Q_PAIR')
        row = event_row(*items, journal)
        matching = [v for v in cat['records'] if f'{v["formid"]:08X}' == row['candidate_form']]
        row['static_candidate_lookup'] = [dict(type=v['type'], edid=v['edid'],
            esm_file_offset=v['offset']) for v in matching]
        rows.append(row)
    monitor = ROOT/'.local-work/native-oracle-020/operations/continuation-live-monitor-01.jsonl'
    from datetime import datetime
    mon = [json.loads(s) for s in monitor.read_text().splitlines()]
    # Operator/phase observations remain separate from native invocation identity.
    checkpoints = {}
    for p in sorted((ROOT/'.local-work/native-oracle-020/operations').glob('continuation-*.json')):
        v = json.loads(p.read_text())
        if 'health' in v and 'latest' in v['health']:
            h=v['health']['latest']
            checkpoints[p.name]=dict(utc=v['utc'],operator=v.get('operator_report'),
                health_pass=v['health']['pass_check'],entered=h['entered'],qpc=h['qpc'],
                health_sequence=h['health_sequence'],flushed_events=h['flushed_events'])
    monitor_max_gap=max((datetime.fromisoformat(b['utc'])-datetime.fromisoformat(a['utc'])).total_seconds()
                        for a,b in zip(mon,mon[1:]))
    health=[json.loads(s) for s in (session/'health.jsonl').read_text().splitlines()]
    health_max_gap=max((b['qpc']-a['qpc'])/result['provenance']['qpc_frequency']
                       for a,b in zip(health,health[1:]))
    summary = dict(schema='sor-q-ledger/1', classification='LOCAL-ONLY', disk=space,
        events=len(events), invocations=len(rows), distinct_descriptors=len({r['candidate_hex'] for r in rows}),
        diagnostics=result['diagnostics'], qpc_frequency=result['provenance']['qpc_frequency'],
        native_grid_comparisons=len(result['comparisons']), monitor_rows=len(mon),
        monitor_max_utc_gap_seconds=monitor_max_gap, strict_one_second_cadence='FAIL',
        health_rows=len(health), health_max_qpc_gap_seconds=health_max_gap,
        checkpoint_receipts=checkpoints, before=before,
        limitations=['No helper return/landscape/overlay snapshot; exact path unavailable',
                    'world+310 is packed key, optional source-pointer read is semantically invalid',
                    'Angular diagnostic uses surrogate cos and unobserved dispatch; not a native output'])
    after = {str(p): digest(p) for p in sorted(paths)}
    if before != after:
        raise ValueError('INPUT_CHANGED')
    guard()
    output.mkdir(parents=True)
    for name, value in [('ledger.json',rows), ('receipt.json',summary), ('after.json',after)]:
        with (output/name).open('x',encoding='utf8',newline='\n') as f:
            json.dump(value,f,indent=2,allow_nan=False);f.write('\n')
    columns = ['invocation','thread','parent','begin_sequence','end_sequence','candidate_form',
               'candidate_hex','longitude','latitude','return_hex','uint32_return',
               'output_before_hex','output_after_hex','bounds','observed_mutated_blobs','path','association']
    with (output/'ledger.csv').open('x',encoding='utf8',newline='') as f:
        writer=csv.DictWriter(f,columns,lineterminator='\n');writer.writeheader()
        writer.writerows({k:r[k] for k in columns} for r in rows)
    print(json.dumps(dict(events=len(events),invocations=len(rows),pins=len(before),output=str(output))))


if __name__ == '__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--session',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args();reconcile(args.session,args.output)
