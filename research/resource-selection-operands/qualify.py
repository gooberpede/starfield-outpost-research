# SPDX-License-Identifier: GPL-3.0-or-later
"""Run only hash-bound disposable synthetic Windows targets. Reads owned build
pins; writes fresh ignored SRO1/ACK/log receipts. No retail/save/config/database,
network or Git mutation. Installed Python stdlib and MSVC outputs only.
"""
import argparse
import hashlib
import json
from pathlib import Path
import struct
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
LOCAL = ROOT / '.local-work/resource-selection-operands'
sys.path.insert(0, str(ROOT / 'research/resource-oracle-retail'))
from collect import pin, persist, write
from readiness import Tracker


def independent(path):
    """Independent SRO1 parser; exact binary framing/digest, END and ACK."""
    raw = path.read_bytes()
    at, rows = 0, []
    while at < len(raw):
        magic, seq, n, sha = struct.unpack_from('<4sQI32s', raw, at)
        at += 48
        assert magic == b'SRO1' and seq == len(rows)+1 and n <= 1048576
        body = raw[at:at+n]
        at += n
        assert len(body) == n and hashlib.sha256(body).digest() == sha
        rows.append(json.loads(body))
    assert at == len(raw) and [r['kind'] for r in rows] == ['SESSION', 'SAMPLE', 'END']
    ack = json.loads(path.with_suffix('.ack.json').read_text())
    assert ack['sha256'] == pin(path) and ack['bytes'] == len(raw)
    return rows


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--build', required=True, type=Path)
    ap.add_argument('--output', required=True, type=Path)
    a = ap.parse_args()
    build, out = a.build.resolve(), a.output.resolve()
    assert build.is_relative_to(LOCAL) and out.is_relative_to(LOCAL)
    manifest = json.loads((build/'build.json').read_text())
    assert manifest['exit_code'] == 0
    for p, h in manifest['files'].items():
        assert pin(p) == h, p
    out.mkdir(exist_ok=False)
    results = []
    modes = ('inactive', 'active', 'rarity-above-mask', 'inactive-out-of-switch', 'installed-setting', 'paired', 'alternate', 'copper', 'rejected', 'nested', 'threads',
             'wrong-workshop', 'missing-namespace', 'stack-budget', 'injected-context-failure', 'wrong-owner', 'wrong-source', 'partial-descriptor', 'partial-dnam',
             'byte-budget', 'guard-mismatch', 'ackfail', 'no-hit', 'crash-before',
             'crash-after', 'crash-during', 'completion')
    for mode in modes:
        folder = out/mode
        folder.mkdir()
        command = [str(build/'sor-c1g-fixture-controller.exe'), '--synthetic-fixture',
                   pin(build/'sor-c1g-fixture.exe'), mode]
        write(folder/'config.json', dict(command=command, synthetic=True))
        p = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, text=True)
        rows = []
        tracker = Tracker()
        ready = []
        for line in p.stdout:
            row = json.loads(line)
            row['synthetic'] = True
            rows.append(row)
            if row['kind'] != 'SAMPLE':
                tracker.observe(row)
            if row['kind'] == 'SAMPLE':
                path = folder/f'capture-{row["capture"]:05d}.bin'
                persist(path, [rows[0], row, dict(kind='END', complete=row['required_reads_complete'])], synthetic=True)
                assert independent(path)[1] == row
                ack = 'REJECT' if mode == 'ackfail' else f'ACK {row["capture"]}'
                useful = tracker.observe(row)
                ready.append(useful)
                if mode == 'completion' and useful:
                    ack += ' STOP'
                p.stdin.write(ack+'\n')
                p.stdin.flush()
        code = p.wait(timeout=15)
        stderr = p.stderr.read()
        write(folder/'events.json', rows)
        write(folder/'stderr.json', dict(text=stderr))
        errors = []
        def check(ok, why):
            if not ok:
                errors.append(why)
        samples = [r for r in rows if r['kind'] == 'SAMPLE']
        calls = [r for r in samples if r['site'] == 'resource_call']
        cells = [r for r in samples if r['site'] == 'chance_branch']
        check(code == (2 if mode in ('guard-mismatch', 'stack-budget', 'injected-context-failure') else 0), 'exit')
        if mode == 'stack-budget':
            check(len(samples) == 64 and all(r['site'] == 'generation_entry' for r in samples), 'bounded stack refuses 65th')
        elif mode in ('no-hit', 'crash-before', 'guard-mismatch', 'injected-context-failure'):
            check(not samples, 'no pre-evidence samples')
        elif mode == 'ackfail':
            check(len(samples) == 1 and rows[-1]['stopped'], 'reject ACK disposes')
        elif mode == 'crash-during':
            check(len(samples) == 1 and samples[0]['site'] == 'generation_entry', 'entry before crash, no invented terminal')
            check(any(r.get('invalidated_invocations') == 1 for r in rows), 'explicit invocation loss on exception')
        else:
            paired = mode in ('paired', 'completion')
            count = 3 if mode == 'threads' else 2 if mode == 'nested' else 1
            check(len(samples) == (8 if paired else count*5) and len(calls) == (2 if paired else count) and len(cells) == (4 if paired else count*2), 'hit counts')
            bad = mode in ('wrong-owner', 'wrong-source', 'partial-descriptor', 'partial-dnam', 'byte-budget')
            check(all(r['required_reads_complete'] for r in samples) == (not bad), 'qualified/incomplete status')
            if not bad:
                check(all(r['frame_matches'] and r['entry_bound'] for r in samples), 'native frame joins')
                check(all(r['resource_call_join'] for r in cells), 'cell resource joins')
                for c in calls:
                    check(c['file_provenance']['main_file_identity'] == (mode != 'missing-namespace'), 'associated-file identity separate from numeric FormID')
                    check(c['effective_weight_bits'] == (0x3f800000 if mode == 'active' or (mode == 'nested' and c['parent_token']) else 0 if mode == 'inactive-out-of-switch' else 0x3e99999a if mode == 'copper' or (paired and c['observed_resource_call_ordinal'] == 2) else 0x3d4ccccd if mode == 'installed-setting' or paired else 0x3c23d70a), 'actual XMM3 at call')
                    check(c['mask_branch'] == ('ACTIVE' if mode == 'active' or (mode == 'nested' and c['parent_token']) else 'INACTIVE'), 'independent mask predicate')
                for c in cells:
                    expected = 'ADMIT' if mode in ('active', 'copper') or (mode == 'nested' and c['parent_token']) else 'REJECT'
                    xy = struct.unpack('<ii', bytes.fromhex(c['cell_xy_i32']['raw']))
                    if mode == 'installed-setting' or paired:
                        expected = 'ADMIT' if xy[0] == 10 or (paired and c['observed_cell_ordinal'] > 2) else 'REJECT'
                    check(c['chance_edge'] == expected, 'actual compare branch')
                    check(c['seed_before_first_draw'] is None and c['consumer_join'] is None, 'unknowns explicit')
                    xy = struct.unpack('<ii', bytes.fromhex(c['cell_xy_i32']['raw']))
                    check(xy in ((10, 1), (11, 1)), 'signed cell words')
                check(len({r['invocation_token'] for r in samples if r['site'] == 'generation_entry'}) == (1 if mode == 'threads' else count), 'thread-local tokens')
                if mode == 'alternate':
                    e = next(r for r in samples if r['site'] == 'generation_entry')
                    check(struct.unpack_from('<Q', bytes.fromhex(e['source_descriptor']['raw']), 16)[0] == 0xaabbccdd, 'alternate selected descriptor')
            if mode == 'wrong-workshop':
                check(all(r['workshop_binding'].startswith('UNKNOWN') for r in samples), 'source bytes cannot impersonate Workshop')
            if mode == 'threads':
                check(len({r['thread_lifetime'] for r in calls}) == 3, 'thread reuse lifetime separation')
            if mode == 'nested':
                check([r['parent_token'] for r in calls] == [1, 0], 'nested ancestry order')
            if mode == 'completion':
                check(rows[-1]['stopped'] and len(samples) == 8 and sum(ready) == 1, 'durable ACK before same-stop disposal')
        check(sum(r['kind'] == 'ACK_ACCEPTED' for r in rows) == len(samples), 'ACK accounting')
        if mode in ('guard-mismatch', 'stack-budget', 'injected-context-failure'):
            check(any(r['kind'] == 'LOSS' for r in rows), 'durable fatal loss')
        if mode in ('crash-before', 'crash-after', 'crash-during'):
            check(any(r['kind'] == 'EXCEPTION' for r in rows), 'unhandled crash disclosed')
        result = dict(mode=mode, passed=not errors, errors=errors, exit=code,
                      samples=len(samples), stderr=stderr,
                      files={str(f):pin(f) for f in folder.iterdir() if f.is_file()})
        write(folder/'result.json', result)
        results.append(result)
        print(mode, not errors, errors, stderr.strip(), flush=True)
    write(out/'qualification.json', dict(synthetic=True, build_sha256=pin(build/'build.json'), cases=results))
    return 0 if all(r['passed'] for r in results) else 1


if __name__ == '__main__':
    raise SystemExit(main())
