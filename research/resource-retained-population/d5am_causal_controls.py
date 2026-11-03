# SPDX-License-Identifier: GPL-3.0-or-later
"""Exercise the causal reader with independent wire and adverse accounting cases.

Creates synthetic, explicitly non-retail session files in one fresh D5AM-local
directory. Reads the exact new reader source, executes its pure file reader and
optimization-refusal CLIs, and writes a qualification receipt. Stdlib only;
no native instruction, game, save, database, deployment, network or Git change.
These fixtures qualify parser/refusal behavior, not the producer, native hook
coverage, actual lock order, owner lifetime or future prediction outcome.
"""
import os
import sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):
    raise RuntimeError('Python optimization is forbidden; invoke with -E -B')

import hashlib
import importlib.util
import json
from pathlib import Path
import re
import struct
import subprocess
import zlib
from d5ad_baseline import guard, sha

ROOT = Path(__file__).resolve().parents[2]
READER = ROOT / 'runtime/construction-winner/d5am_read_causal.py'
DLL = 'a' * 64


def require(value, message):
    if not value:
        raise ValueError(message)


def event(sequence, kind, old=0, new=0, thread=101, ticks=None, **changes):
    row = dict(sequence=sequence, kind=kind, thread=thread, ticks=ticks or sequence * 10,
               lock=0x1000, generation=1, invocation=0, selection=0, source=0,
               epoch=1, hazards=0, old_state=old, new_state=new, status=0, site=0,
               request=[-3, 7])
    row.update(changes)
    return row


def encode(rows, identity):
    header = struct.pack('<4Q', 0x31434c4d41354453, 1, 128, 0)
    header += hashlib.sha256(identity).hexdigest().encode('ascii')
    packets = []
    for row in rows:
        keys = 'sequence kind thread ticks lock generation invocation selection source epoch hazards old_state new_state status site'.split()
        payload = struct.pack('<15Q2i', *(row[k] for k in keys), *row['request'])
        packets.append(struct.pack('<II', 128, zlib.crc32(payload)) + payload)
    return header + b''.join(packets)


def main():
    require(len(sys.argv) == 2 and re.fullmatch('[a-z0-9-]+', sys.argv[1]), 'Fresh bounded label required')
    out = ROOT / '.local-work/d5am' / sys.argv[1]
    require(not any(p.is_symlink() or p.is_junction() for p in (out, *out.parents)), 'Reparse output path')
    initial_free = guard()
    out.mkdir(parents=True, exist_ok=False)
    spec = importlib.util.spec_from_file_location('d5am_causal_under_test', READER)
    reader = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(reader)
    reader_pin = sha(READER)
    identity = dict(schema='sor-d5x/4', causal_schema='sor-d5am-causal/1',
                    causal_bridge_admission_schema='sor-d5am-causal-bridge/1',
                    retail=False, dll_sha256=DLL, nonce='f' * 64, pid=1,
                    creation_filetime=2, qpc_frequency=10_000_000)
    original_rows = [event(1, 1), event(2, 2, 0, 0x1000),
                     event(3, 3, 0x1000, 0x401000), event(4, 7, 0x401000, 0)]
    checks = []

    def fixture(name, rows=None, terminal_change=None, raw_change=None, identity_change=None,
                ack_change=None, terminal_text=None, no_terminal=False):
        folder = out / name
        folder.mkdir()
        ident = dict(identity)
        if identity_change:
            ident.update(identity_change)
        identity_bytes = (json.dumps(ident, separators=(',', ':')) + '\n').encode()
        rows = original_rows if rows is None else rows
        raw = encode(rows, identity_bytes)
        if raw_change:
            raw = raw_change(raw)
        terminal = dict(ident, causal_written=len(rows), causal_enqueued=len(rows),
                        causal_active=0, causal_drops=0, causal_reentrant=0,
                        causal_bridge_active=0, causal_native_counter_faults=0,
                        causal_failed=False, causal_baseline_unknown=0,
                        causal_multiowner=0, causal_uncertain=0, failed=False, output_faults=0,
                        output_fault='none', resident_inert=True)
        if terminal_change:
            terminal_change(terminal)
        ack = {k:v for k,v in terminal.items() if k.startswith('causal_') and k not in ('causal_schema','causal_sites')}
        ack['identity_sha256']=hashlib.sha256(identity_bytes).hexdigest()
        if ack_change:
            ack_change(ack)
        (folder / 'identity.json').write_bytes(identity_bytes)
        (folder / 'causal.bin').write_bytes(raw)
        (folder / 'flush.jsonl').write_text(json.dumps(ack) + '\n', encoding='utf8', newline='\n')
        if not no_terminal:
            (folder / 'terminal.json').write_text(terminal_text or json.dumps(terminal), encoding='utf8', newline='\n')
        return folder

    good = fixture('positive')
    parsed = reader.read(good, DLL)
    require(parsed['sidecar_accounting_complete'] and not parsed['histories'][0]['issues'], 'Positive wire/accounting failed')
    require(parsed['causal_completeness'] == 'INCONCLUSIVE', 'Parser invented full native coverage')
    require(parsed['events'] == original_rows, 'Independent struct wire differs from reader')
    require(parsed['native_bridge_accounting_complete'], 'Declared native admission accounting not checked')
    checks.append('synthetic-wire-all-fields-positive-and-no-native-promotion')

    def refuses(name, **kwargs):
        folder = fixture(name, **kwargs)
        try:
            reader.read(folder, DLL)
        except (ValueError, KeyError, TypeError, json.JSONDecodeError):
            checks.append(name)
        else:
            raise ValueError('Adverse input accepted: ' + name)

    refuses('partial-header', raw_change=lambda raw: raw[:95])
    refuses('partial-frame', raw_change=lambda raw: raw[:-1])
    refuses('wrong-header', raw_change=lambda raw: bytes([raw[0] ^ 1]) + raw[1:])
    refuses('wrong-identity-binding', raw_change=lambda raw: raw[:32] + b'0' * 64 + raw[96:])
    refuses('corrupt-crc', raw_change=lambda raw: raw[:110] + bytes([raw[110] ^ 1]) + raw[111:])
    refuses('sequence-gap', rows=[original_rows[0], event(3, 2, 0, 0x1000)])
    refuses('unknown-kind', rows=[event(1, 16)])
    refuses('unknown-status-bit',rows=[event(1,1,status=16)])
    refuses('unmarked-zero-generation',rows=[event(1,2,0,0x1000,generation=0)])
    crossing=reader.read(fixture('prewatch-crossing-uncertainty',rows=[event(1,2,0,0x1000,generation=0,status=8)],
        terminal_change=lambda t:t.update(causal_uncertain=1)),DLL)
    require(crossing['sidecar_accounting_complete'] and crossing['native_bridge_accounting_complete'] and
            'REGISTRY_GENERATION_UNCERTAINTY' in crossing['coverage_refusals'] and
            crossing['histories'][0]['issues'],'Crossing native operation lost or assigned an invented generation')
    checks.append('prewatch-crossing-uncertainty')
    refuses('wrong-atomic-delta', rows=[event(1, 2, 0, 2)])
    refuses('acquired-with-reader-present', rows=[event(1, 3, 0x1001, 0x401001)])
    refuses('acquired-without-pending-count', rows=[event(1, 3, 0, 0x400000)])
    refuses('recursive-without-exclusive', rows=[event(1, 4, 0, 0x400000)])
    refuses('reader-underflow', rows=[event(1, 6, 0, 0xffffffff)])
    refuses('wrong-final-depth', rows=[event(1, 7, 0x801000, 0x400000)])
    refuses('wrong-recursive-depth', rows=[event(1, 8, 0x401000, 0x1000)])
    refuses('terminal-other-session', terminal_change=lambda t: t.update(nonce='e' * 64))
    refuses('terminal-missing-count', terminal_change=lambda t: t.pop('causal_drops'))
    refuses('terminal-bool-counter', terminal_change=lambda t: t.update(causal_drops=False))
    refuses('terminal-underwritten', terminal_change=lambda t: t.update(causal_written=3))
    refuses('terminal-duplicate-key', terminal_text='{"causal_written":4,"causal_written":4}')
    refuses('terminal-nonfinite-json', terminal_text='{"unsupported":NaN}')
    refuses('ack-other-identity', ack_change=lambda a: a.update(identity_sha256='0' * 64))
    refuses('ack-beyond-file', ack_change=lambda a: a.update(causal_written=5))
    refuses('identity-other-schema', identity_change=dict(causal_schema='sor-d5am-causal/999'))
    refuses('unknown-native-admission-schema', identity_change=dict(causal_bridge_admission_schema='unsupported'))
    for field in ('causal_bridge_active','causal_native_counter_faults'):
        refuses('missing-native-terminal-'+field, terminal_change=lambda t,field=field:t.pop(field))
        refuses('missing-native-ack-'+field, ack_change=lambda a,field=field:a.pop(field))
        refuses('bool-native-'+field, terminal_change=lambda t,field=field:t.update({field:False}))
    refuses('live-native-terminal', terminal_change=lambda t:t.update(causal_bridge_active=1))
    refuses('negative-native-active', ack_change=lambda a:a.update(causal_bridge_active=-1))
    refuses('oversized-native-active', ack_change=lambda a:a.update(causal_bridge_active=2**64))
    refuses('unknown-native-fault', terminal_change=lambda t:t.update(causal_native_counter_faults=4,causal_failed=True))
    refuses('hidden-native-fault', terminal_change=lambda t:t.update(causal_native_counter_faults=1))
    legacy=reader.read(fixture('earlier-no-native-feature',identity_change=dict(causal_bridge_admission_schema=None)),DLL)
    require(legacy['sidecar_accounting_complete'] and not legacy['native_bridge_accounting_complete'], 'Earlier journal promoted to native admission proof')
    checks.append('earlier-byte-accounting-without-native-admission-proof')
    native_failure=reader.read(fixture('declared-native-counter-fault',terminal_change=lambda t:t.update(causal_native_counter_faults=3,causal_failed=True)),DLL)
    require(not native_failure['native_bridge_accounting_complete'] and not native_failure['sidecar_accounting_complete'],'Native fault promoted')
    checks.append('declared-native-counter-fault')
    refuses('terminal-erases-native-fault',ack_change=lambda a:a.update(causal_native_counter_faults=1,causal_failed=True),
            terminal_change=lambda t:t.update(causal_failed=True))
    folder=fixture('ack-native-fault-bits-regress',terminal_change=lambda t:t.update(causal_native_counter_faults=3,causal_failed=True))
    ack=json.loads((folder/'flush.jsonl').read_bytes());first=dict(ack,causal_native_counter_faults=1);second=dict(ack,causal_native_counter_faults=2)
    (folder/'flush.jsonl').write_text(json.dumps(first)+'\n'+json.dumps(second)+'\n',encoding='utf8',newline='\n')
    try:
        reader.read(folder,DLL)
    except ValueError:
        checks.append('ack-native-fault-bits-regress')
    else:
        raise ValueError('Sticky native fault bits regressed without refusal')

    for name, changes, reason in (
        ('declared-loss', dict(causal_drops=1, causal_failed=True), 'RECORDER_LOSS_OR_FAILURE'),
        ('unknown-baseline', dict(causal_baseline_unknown=1), 'UNKNOWN_BASELINE_OR_MULTIOWNER'),
        ('multiple-owner', dict(causal_multiowner=1), 'UNKNOWN_BASELINE_OR_MULTIOWNER'),
        ('registry-uncertainty', dict(causal_uncertain=1), 'REGISTRY_GENERATION_UNCERTAINTY'),
        ('core-output-failure', dict(output_faults=1, output_fault='fixture'), 'CORE_OUTPUT_FAILURE'),
        ('counter-overflow', dict(causal_counter_overflow=True), 'COUNTER_OVERFLOW'),
        ('not-inert', dict(resident_inert=False), 'NOT_OWNED_INERT_STOP')):
        result = reader.read(fixture(name, terminal_change=lambda t, changes=changes: t.update(changes)), DLL)
        if reason in ('UNKNOWN_BASELINE_OR_MULTIOWNER','REGISTRY_GENERATION_UNCERTAINTY'):
            require(result['sidecar_accounting_complete'] and reason in result['coverage_refusals'], name)
        else:
            require(not result['sidecar_accounting_complete'], name)
        require(reason in result['reasons'], name)
        checks.append(name)
    result = reader.read(fixture('no-terminal', no_terminal=True), DLL)
    require(not result['sidecar_accounting_complete'] and 'NO_TERMINAL_ACCOUNTING' in result['reasons'], 'Missing terminal promoted')
    checks.append('no-terminal')

    duplicate_acquisition = original_rows[:3] + [event(4, 3, 0x1000, 0x401000)]
    result = reader.read(fixture('pending-consumed-once', rows=duplicate_acquisition), DLL)
    require('ACQUISITION_WITHOUT_RECORDED_PENDING' in result['histories'][0]['issues'], 'Pending reused across acquisitions')
    checks.append('pending-consumed-once')
    # Register may publish after another thread's probe; it must not be assumed
    # sequence-first. Cross-thread QPC inversions are not native order failures.
    reordered = [event(1, 2, 0, 0x1000, thread=202, ticks=20), event(2, 1, ticks=10),
                 event(3, 3, 0x1000, 0x401000, thread=202, ticks=30)]
    result = reader.read(fixture('cross-thread-publication-inversion', rows=reordered), DLL)
    require(not result['histories'][0]['issues'], 'Cross-thread sequence imposed a false causal order')
    checks.append('cross-thread-publication-inversion')

    # These are deliberately supplied interval schedules, not measured native
    # timing. Same-owner mutual exclusion plus disjoint pre/post bounds are the
    # stated premises; overlapping callbacks must never be guessed into order.
    def windows(name, rows, expected):
        result=reader.read(fixture(name, rows=rows), DLL)
        values=[w['interpretation'] for w in result['histories'][0]['registration_witnesses']]
        require(values==[expected], name + ' interval discrimination')
        checks.append(name)
    windows('pre-helper-delay', [event(1,1,ticks=1),event(2,9,thread=202,ticks=10),
        event(3,2,0,0x1000,thread=202,ticks=11),event(4,3,0x1000,0x401000,thread=202,ticks=12),
        event(5,9,ticks=20),event(6,2,0,0x1000,ticks=21),event(7,3,0x1000,0x401000,ticks=22)],
        'EARLIER_ACQUISITION_BEFORE_OTHER_HELPER_ENTRY')
    windows('prior-pending-overtaken', [event(1,1,ticks=1),event(2,9,ticks=10),event(3,2,0,0x1000,ticks=11),
        event(4,9,thread=202,ticks=20),event(5,2,0x1000,0x2000,thread=202,ticks=21),
        event(6,3,0x2000,0x402000,thread=202,ticks=22),event(7,3,0x1000,0x401000,ticks=30)],
        'PRIOR_PENDING_WRITER_OVERTAKEN')
    windows('overlapping-atomic-brackets', [event(1,1,ticks=1),event(2,9,ticks=10),
        event(3,9,thread=202,ticks=11),event(4,2,0x1000,0x2000,ticks=12),
        event(5,2,0,0x1000,thread=202,ticks=13),event(6,3,0x2000,0x402000,thread=202,ticks=14),
        event(7,3,0x1000,0x401000,ticks=20)],'OVERLAPPING_INTERVALS_UNKNOWN')

    for entry in (READER, Path(__file__), ROOT / 'research/resource-retained-population/d5am_delivery.py',
                  ROOT / 'research/resource-retained-population/d5am_preserve.py',
                  ROOT / 'research/resource-retained-population/d5am_join_causal.py',
                  ROOT / 'research/resource-retained-population/d5am_scheduler_recheck.py'):
        for flags, env in ((['-E', '-B', '-O'], None), (['-E', '-B', '-OO'], None),
                           (['-E', '-B'], dict(os.environ, PYTHONOPTIMIZE='1'))):
            result = subprocess.run([sys.executable, *flags, str(entry), '--help'], env=env, capture_output=True)
            require(result.returncode != 0 and b'optimization' in result.stderr.lower(), 'Optimization not refused by ' + entry.name)
            checks.append(entry.name + ':' + ('inherited-env' if env else flags[-1]))
    require(sha(READER) == reader_pin, 'Reader changed during controls')
    receipt = dict(schema='sor-d5am-causal-controls/1', result='PASS', checks=checks,
                   reader_sha256=reader_pin, method_sha256=sha(__file__),
                   initial_free=initial_free, final_free=guard(),
                   scope='Synthetic byte/parser and declared-uncertainty fixtures only; no native producer or retail observation qualification.')
    with (out / 'qualification.json').open('x', encoding='utf8', newline='\n') as stream:
        json.dump(receipt, stream, indent=2)
        stream.write('\n')
    print(json.dumps(dict(result='PASS', checks=len(checks), out=str(out))))


if __name__ == '__main__':
    main()
