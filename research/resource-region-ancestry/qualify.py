# SPDX-License-Identifier: GPL-3.0-or-later
"""Execute only hash-pinned disposable C1E fixtures, never Starfield.

Requires installed Windows MSVC-built fixture/controller and Python stdlib.
Reads build/source pins; creates a fresh ignored receipt directory. No save,
definition, config, Git, database or network writes. No cleanup of prior data.
"""
import argparse
import hashlib
import json
from pathlib import Path
import struct
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
LOCAL = ROOT / '.local-work/resource-region-ancestry'
sys.path.insert(0, str(ROOT / 'research/resource-oracle-retail'))
from collect import pin, persist, write


def independent(path):
    """Separate framing parser; does not call C1B decode or collector readers."""
    raw = path.read_bytes()
    rows = []
    at = 0
    while at < len(raw):
        magic, seq, n, digest = struct.unpack_from('<4sQI32s', raw, at)
        at += 48
        assert magic == b'SRO1' and seq == len(rows)+1 and n <= 1048576
        body = raw[at:at+n]
        at += n
        assert len(body) == n and hashlib.sha256(body).digest() == digest
        rows.append(json.loads(body))
    assert at == len(raw) and [r['kind'] for r in rows] == ['SESSION', 'SAMPLE', 'END']
    ack = json.loads(path.with_suffix('.ack.json').read_text())
    assert ack['sha256'] == hashlib.sha256(raw).hexdigest() and ack['bytes'] == len(raw)
    return rows


def preserve(folder, session, row):
    complete = row['required_reads_complete'] and all(row[k]['status'] == 'COMPLETE' for k in ('geometry', 'selected', 'refresh_payload') if k in row)
    complete &= all(row.get(k,True) for k in ('qb_retained_read','closure_read','descriptor_read'))
    path = folder / f'capture-{row["capture"]:05d}.bin'
    ack = persist(path, [session, row, dict(kind='END', complete=complete)], synthetic=True)
    assert independent(path)[1] == row
    return ack


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--build', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    a = ap.parse_args()
    build, output = a.build.resolve(), a.output.resolve()
    assert build.is_relative_to(LOCAL) and output.is_relative_to(LOCAL)
    manifest = json.loads((build / 'build.json').read_text())
    assert manifest['exit_code'] == 0
    for p, digest in manifest['files'].items():
        assert pin(p) == digest, p
    output.mkdir(exist_ok=False)
    results = []
    modes = ('good', 'copper', 'reject', 'multi', 'maximum', 'multi-reject', 'sources', 'nested', 'threads', 'mixed', 'invalid-procgen',
             'wrong-workshop', 'wrong-source', 'wrong-resource', 'wrong-caller',
             'stale-transfer', 'outside-region', 'empty', 'partial', 'corrupt',
             'oversized', 'byte-budget', 'invalid-source', 'source-budget', 'empty-collection', 'corrupt-collection', 'invalid-collection', 'guard-mismatch', 'ackfail',
             'crash-before', 'crash-after', 'completion')
    for mode in modes:
        folder = output / mode
        folder.mkdir()
        command = [str(build / 'sor-c1e-fixture-controller.exe'), '--synthetic-fixture',
                   pin(build / 'sor-c1e-fixture.exe'), mode]
        write(folder / 'config.json', dict(command=command, synthetic=True, build_sha256=pin(build / 'build.json')))
        p = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        rows = []
        for line in p.stdout:
            row = json.loads(line)
            row['synthetic'] = True
            rows.append(row)
            if row['kind'] == 'SAMPLE':
                preserve(folder, rows[0], row)
                response = 'REJECT' if mode == 'ackfail' else f'ACK {row["capture"]}'
                if mode == 'completion' and row['site'] == 'spatial_transfer_payload':
                    response += ' STOP'
                p.stdin.write(response+'\n')
                p.stdin.flush()
        code = p.wait(timeout=15)
        stderr = p.stderr.read()
        write(folder / 'events.json', rows)
        write(folder / 'stderr.json', dict(text=stderr))
        decisions = [r for r in rows if r.get('decision')]
        transfers = [r for r in rows if 'refresh_payload' in r]
        samples = [r for r in rows if r['kind'] == 'SAMPLE']
        errors = []
        def check(v, why):
            if not v:
                errors.append(why)
        check(code == (2 if mode == 'guard-mismatch' else 0), 'controller exit')
        if mode in ('crash-before', 'guard-mismatch'):
            check(not samples, 'no pre-evidence acquisition')
        elif mode == 'ackfail':
            check(len(samples) == 1 and not decisions and rows[-1]['stopped'], 'abort at first rejected ACK')
        else:
            n = 3 if mode == 'threads' else 2 if mode == 'nested' else 1
            check(len(decisions) == (2 if mode in ('mixed','sources') else n) and len(transfers) == n and len(samples) == (4 if mode in ('mixed','sources') else n*3), 'stop accounting')
            for d in decisions:
                expected_bound = mode not in ('wrong-workshop', 'wrong-source', 'wrong-caller', 'stale-transfer', 'source-budget', 'invalid-procgen')
                check((d['ancestry'] == 'BOUND_CALLBACK') == expected_bound, 'callback stack/source binding')
                expected_selected = mode not in ('wrong-resource', 'outside-region', 'invalid-source', 'empty-collection', 'corrupt-collection', 'invalid-collection')
                check((d['selected']['status'] == 'COMPLETE') == expected_selected, 'selected region lineage')
                geometry_ok = mode not in ('partial', 'corrupt', 'oversized', 'byte-budget')
                # outside-region contains a non-region slice: validity is gated by selected ancestry.
                if mode != 'outside-region':
                    check((d['geometry']['status'] == 'COMPLETE') == geometry_ok, 'bounded geometry')
                if not geometry_ok:
                    check(d['geometry']['ordered_xyzw'] is None, 'failed read is not empty')
                if geometry_ok and mode not in ('outside-region',):
                    pts = bytes.fromhex(d['geometry']['ordered_xyzw'])
                    count = struct.unpack_from('<I', bytes.fromhex(d['geometry']['raw_region']), 24)[0]
                    check(len(pts) == count*16, 'point byte count')
                    check(count == (4096 if mode == 'maximum' else 3 if mode in ('multi','multi-reject') else 0 if mode == 'empty' else 1), 'fixture native count')
                    if count and mode not in ('threads', 'maximum', 'multi-reject'):
                        check(struct.unpack_from('<4f', pts) == (10,20,0,3), 'independent coordinate words')
                if d['ancestry'] == 'BOUND_CALLBACK':
                    matches = [t for t in transfers if (t['tid'],t['thread_lifetime'],t['updater_token']) ==
                               (d['tid'],d['thread_lifetime'],d['updater_token'])]
                    check(len(matches) == 1 and matches[0]['updater_bp'] == d['updater_bp'], 'entry-to-transfer token')
                    if d['decision'] == 'ACCEPT':
                        check(any(m['pointer'] == d['resource_pointer'] for m in matches[0]['refresh_payload']['members']), 'actual accepted pointer transfer')
                    elif mode != 'mixed':
                        check(not matches[0]['refresh_payload']['members'], 'rejected region adds no resource')
                check(not d['census_complete'] and d['generation_inputs'] is None and d['population_epoch'] is None, 'no invented epochs/census')
            if mode == 'sources':
                check([d['source_ordinal'] for d in decisions] == [0,1] and len({d['selected']['source_wrapper'] for d in decisions}) == 2 and len(transfers[0]['refresh_payload']['members']) == 2, 'distinct accepted sources')
            if mode in ('multi','multi-reject','reject','empty'):
                check(decisions[0]['decision'] == ('ACCEPT' if mode == 'multi' else 'REJECT'), 'geometry-derived terminal')
            if mode == 'invalid-procgen':
                check(decisions[0]['loss'] == 'stack-source-read' and not decisions[0]['required_reads_complete'], 'durable failed-read LOSS')
                path=folder/f'capture-{decisions[0]["capture"]:05d}.bin'
                check(not independent(path)[-1]['complete'], 'LOSS is incomplete terminal')
            if mode == 'mixed':
                check([d['decision'] for d in decisions] == ['REJECT','ACCEPT'] and [d['selected']['ordinal'] for d in decisions] == [0,1] and len(transfers[0]['refresh_payload']['members']) == 1, 'real temporary accepted-set reduction')
            if mode == 'nested':
                check(decisions[0]['parent_token'] != 0 and decisions[1]['parent_token'] == 0, 'nested parent')
                check(decisions[0]['updater_token'] != decisions[1]['updater_token'], 'distinct nested tokens')
            if mode == 'threads':
                check(len({d['thread_lifetime'] for d in decisions}) == 3, 'thread lifetimes')
                xs = [struct.unpack_from('<f', bytes.fromhex(d['geometry']['ordered_xyzw']))[0] for d in decisions]
                check(xs == [10,100,101], 'changed memory across thread lifetimes')
            if mode in ('good','copper') and decisions:
                check(decisions[0]['file_provenance']['main_file_identity'], 'resource file identity')
            if mode == 'completion':
                check(rows[-1]['stopped'] and sum(r['kind']=='ACK_ACCEPTED' and r['accepted'] for r in rows)==3, 'durable same-stop completion')
        if mode == 'guard-mismatch':
            check(any(r['kind']=='LOSS' for r in rows), 'durable fatal LOSS record')
        check(sum(r['kind']=='ACK_ACCEPTED' for r in rows) == len(samples), 'one acknowledgement per capture')
        result = dict(mode=mode, passed=not errors, errors=errors, exit=code, stderr=stderr,
                      samples=len(samples), files={f.name:pin(f) for f in folder.iterdir() if f.is_file()})
        write(folder / 'result.json', result)
        results.append(result)
        print(mode, not errors, errors, stderr.strip(), flush=True)
    write(output / 'qualification.json', dict(synthetic=True, cases=results, build_sha256=pin(build / 'build.json')))
    return 0 if all(r['passed'] for r in results) else 1


if __name__ == '__main__':
    raise SystemExit(main())
