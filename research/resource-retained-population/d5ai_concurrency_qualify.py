# SPDX-License-Identifier: GPL-3.0-or-later
"""Qualify simultaneous lifetime/core/geometry service by the exact shared worker.

Reads retained build16 objects/headers and approved local compiler tools; writes fresh
ignored source copies, contract, executables, native sessions and receipts. Runs
only owned hosts. Four producer threads use unique operation allocations and an
independent forwarding/admission oracle. Geometry uses actual owned CALL bridges
over an immutable supplied population and logical native reader, not game data.
Core guard windows/direct Event producers are supplied; eighteen engine entry
hooks are not claimed. No game, save, deployment, network or foreign intervention.
Stop on pin/compile/native/oracle/guard failure; retain every artifact. Both
drives retain the 40 GB caller-available floor plus declared reserve. No deletion.
"""
from pathlib import Path
import hashlib
import json
import re
import struct
import subprocess
import sys
import zlib

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'runtime/session-tools'))
sys.path.insert(0, str(ROOT / 'runtime/construction-winner'))
from common import guard, fresh, sha
from d5ai_read_geometry import decode as decode_geometry, loads_unique
from d5ai_read_lifetime import read_prefix, qualify_snapshot, EVENT
from read_capture import decode as decode_core
from d5ai_operations import worker_json

VC = Path('C:/Program Files/Microsoft Visual Studio/18/Community/VC/Auxiliary/Build/vcvars64.bat')


def verify_case(case, accept_intra_call_ties=False):
    oracle = json.loads((case / 'oracle.json').read_bytes())
    session = case / 'session'
    identity = loads_unique((session / 'identity.json').read_bytes())
    terminal = worker_json(session / 'terminal.json')
    assert identity['dll_sha256'] == identity['host_sha256'] == sha(case.parent/'d5ai-concurrency.exe')
    mode = oracle['mode']
    overloaded = mode == 'overload'
    ops = {op['allocation']: op for op in oracle['operations']}
    assert len(ops) == 4 * oracle['calls_per_thread']
    assert all(op['callback_count'] == 1 for op in ops.values())
    assert oracle['peak_original_callbacks'] >= 4 and oracle['geometry_during_four_callbacks']
    assert oracle['core_cell_bytes'] == 320 and oracle['lifetime_cell_bytes'] == 104
    assert oracle['core_queue_bytes'] == 320 * 32768 and oracle['lifetime_queue_bytes'] == 104 * 32768
    core_bytes = (session / 'events.bin').read_bytes()
    assert len(core_bytes) % 328 == 0
    expected = {(op['allocation'], sub) for op in ops.values() for sub, yes in enumerate(op['core_accepted']) if yes}
    admitted, order = set(), {}
    for offset in range(0, len(core_bytes), 328):
        magic, size, low, crc = struct.unpack_from('<4I', core_bytes, offset)
        payload = core_bytes[offset + 16:offset + 328]
        event = decode_core(payload)
        sequence = offset // 328 + 1
        assert (magic, size, low, crc) == (0x31505253, 312, sequence & 0xffffffff, zlib.crc32(payload))
        assert event['sequence'] == sequence and event['kind'] == 13
        if sequence == 1:
            assert event['a'] == 0
            continue
        op = ops[event['c']]
        key = (event['c'], event['d'])
        assert key in expected and key not in admitted
        assert event['a'] == op['thread_index'] + 1 and event['b'] == op['ordinal'] and event['thread'] == op['thread']
        admitted.add(key)
        order.setdefault(event['thread'], []).append((op['ordinal'], event['d']))
    assert admitted == expected and all(values == sorted(values) for values in order.values())
    assert len(core_bytes) // 328 == terminal['enqueued'] == terminal['written'] == terminal['flushed'] == terminal['acknowledged']
    assert oracle['core_offers'] == terminal['enqueued'] + terminal['drops']
    assert terminal['drops'] == terminal['queue_full'] + terminal['contention_exhausted'] + terminal['reentrant_losses']
    raw_life = (session / 'lifetimes.bin').read_bytes()
    assert len(raw_life) == 96 + 112 * terminal['lifetime_enqueued']
    pairs, previous, invocations, lifetime_order = {}, {}, {}, {}
    for offset in range(96, len(raw_life), 112):
        magic, size, low, crc = struct.unpack_from('<4I', raw_life, offset)
        payload = raw_life[offset + 16:offset + 112]
        values = EVENT.unpack(payload)
        seq, kind, phase, invocation, parent, thread, ticks, receiver, allocation, status, epoch, hazards = values
        assert (magic, size, low, crc) == (0x314a4c53, 96, seq & 0xffffffff, zlib.crc32(payload))
        assert seq == (offset - 96) // 112 + 1
        op = ops[allocation]
        assert kind == op['kind'] and phase in (0, 1) and thread == op['thread'] and not parent and not status
        assert receiver == allocation + (16 if kind == 1 else 8)
        assert ticks >= previous.get(thread, 0)
        previous[thread] = ticks
        lifetime_order.setdefault(thread, []).append((op['ordinal'], phase))
        row = pairs.setdefault(allocation, {})
        assert phase not in row
        row[phase] = dict(sequence=seq, ticks=ticks, invocation=invocation)
        if invocation in invocations:
            assert invocations[invocation] == allocation
        invocations[invocation] = allocation
    assert all(values == sorted(values) for values in lifetime_order.values())
    ties = 0
    for allocation, phases in pairs.items():
        if 0 in phases and 1 in phases:
            assert phases[0]['sequence'] < phases[1]['sequence'] and phases[0]['invocation'] == phases[1]['invocation']
            assert phases[0]['ticks'] <= phases[1]['ticks']
            ties += phases[0]['ticks'] == phases[1]['ticks']
        elif not overloaded:
            raise AssertionError('Zero-loss journal lost a phase')
    assert oracle['lifetime_offers'] == terminal['lifetime_enqueued'] + terminal['lifetime_drops']
    assert terminal['lifetime_enqueued'] == terminal['lifetime_written'] == terminal['lifetime_flushed'] == terminal['lifetime_acknowledged']
    geometry = []
    flush_ticks = []
    for path in sorted(session.glob('geometry-*.bin'), key=lambda p: int(p.stem.split('-')[1])):
        snapshot = decode_geometry(path.read_bytes())
        receipt = loads_unique(path.with_suffix('.json').read_bytes())
        assert receipt['sha256'] == sha(path) and receipt['identity_sha256'] == sha(session / 'identity.json') and receipt['flushed'] is True
        assert receipt['bytes'] == path.stat().st_size
        geometry.append(snapshot)
        flush_ticks.append(receipt['worker_flushed_ticks'] - snapshot['header']['completion_ticks'])
    coverage = 'INCONCLUSIVE'
    if overloaded:
        assert terminal['failed'] and terminal['lifetime_failed'] and terminal['drops'] > 0 and terminal['lifetime_drops'] > 0
        assert not geometry and terminal['geometry_completed'] == 0 and 0 < terminal['geometry_captured'] <= 4
        try:
            read_prefix(session, terminal)
        except ValueError:
            pass
        else:
            raise AssertionError('Overload became qualified history')
    else:
        assert not terminal['failed'] and not terminal['lifetime_failed'] and terminal['drops'] == terminal['lifetime_drops'] == 0
        assert len(pairs) == len(ops) and len(geometry) == terminal['geometry_completed'] == 33
        assert terminal['geometry_no_slot'] == 0 and terminal['geometry_busy_skips'] == 0
        if mode == 'held':
            assert oracle['core_pending_before_release'] == oracle['core_offers'] - 1
            assert oracle['lifetime_pending_before_release'] == oracle['lifetime_offers']
        try:
            journal = read_prefix(session, terminal)
        except ValueError:
            if not (mode == 'short' and ties and not accept_intra_call_ties):
                raise
        else:
            assert not ties or accept_intra_call_ties
            try:
                qualify_snapshot(geometry[0], journal)
            except ValueError:
                pass
            else:
                raise AssertionError('Capture during four active callbacks became qualified')
            qualify_snapshot(geometry[-1], journal)
            coverage = 'POST_PRODUCER_CAPTURE_QUALIFIED'
        ack = worker_json(session / ('ack-' + 'd' * 32 + '.json'))
        assert ack['lifetime_acknowledged'] == terminal['lifetime_enqueued'] and ack['acknowledged'] == terminal['enqueued']
    frequency = identity['qpc_frequency']
    result = dict(mode=mode, operations=len(ops), forwarded_originals=len(ops), core_records=terminal['enqueued'],
                  core_drops=terminal['drops'], lifetime_records=terminal['lifetime_enqueued'], lifetime_drops=terminal['lifetime_drops'],
                  intra_call_QPC_ties=ties, coverage=coverage, lifetime_per_thread_order_verified=True,
                  lifetime_complete_pairs=sum(len(phases)==2 for phases in pairs.values()),
                  lifetime_partial_pairs=sum(len(phases)==1 for phases in pairs.values()),
                  lifetime_unobserved_operations=len(ops)-len(pairs), overlapping_original_callbacks=oracle['peak_original_callbacks'],
                  geometry_captured=terminal['geometry_captured'], geometry_persisted=terminal['geometry_completed'],
                  core_cell_bytes=oracle['core_cell_bytes'], core_queue_bytes=oracle['core_queue_bytes'],
                  lifetime_cell_bytes=oracle['lifetime_cell_bytes'], lifetime_queue_bytes=oracle['lifetime_queue_bytes'],
                  worker_cpu_seconds=oracle['worker_cpu_100ns'] / 10000000,
                  producer_interval_seconds=(oracle['producers_done_ticks'] - oracle['started_ticks']) / frequency,
                  worker_write_calls=terminal['write_calls'], worker_flush_calls=terminal['flush_calls'],
                  maximum_worker_write_seconds=terminal['max_write_ticks'] / frequency,
                  maximum_worker_flush_seconds=terminal['max_flush_ticks'] / frequency,
                  shared_worker_timing_ticks=terminal['worker_timing_ticks'])
    if oracle['all_durable_ack_observed_ticks']:
        result['last_producer_to_durable_ACK_observed_seconds'] = (oracle['all_durable_ack_observed_ticks'] - oracle['producers_done_ticks']) / frequency
        result['geometry_completion_to_raw_flush_sample_seconds'] = dict(min=min(flush_ticks) / frequency, max=max(flush_ticks) / frequency)
    return result


def main():
    build, out = (Path(p).resolve() for p in sys.argv[1:3])
    if not out.is_relative_to(ROOT / '.local-work/d5ai-recorder'):
        raise ValueError('Fresh task-local output required')
    guard({'D:/': 128 * 1024 * 1024})
    out.mkdir(exist_ok=False)
    fresh(out / 'contract.json', dict(schema='sor-d5ai-integrated-concurrency-contract/1',
        allowed='Compile/link exact retained build16 objects and execute only four owned disposable hosts; read/verify files',
        inputs='Pinned retained objects/headers, approved installed compiler and authored driver',
        outputs=str(out), risks=['Driver/ABI/guard fault', 'Unexpected loss or ordering', 'Disk exhaustion'],
        stop='Any source/guard/compile/native/oracle failure; preserve all attempts', cleanup='Retain originals, new binaries and every receipt; no deletion',
        modes=dict(normal='4x512 operations; explicit 1 ms owned callback work; zero-loss envelope',
                   short='4x512 unpaced short callbacks; zero-loss transport, intra-call ties require exact typed phase/sequence proof in the pinned receiver; boundary ties remain refused',
                   held='4x128 operations with shared worker queues held; explicit 1 ms callback work; zero loss then drain',
                   overload='4x5000 unpaced operations with queues held; loss expected and exactly accounted, no balanced-success claim'),
        geometry='Actual owned 3 CALL bridges, immutable supplied population/shared reader; first capture while 4 callbacks held, post-producer capture 33 where loss-free',
        core='Direct owned Event producers and supplied guard windows; not 18 native engine entry hooks',
        reserve_bytes=128 * 1024 * 1024, floor_bytes_per_drive=40000000000, no_live_authority=True))
    source = Path(__file__).with_name('d5ai-concurrency-driver.cpp')
    objects = ['transport.obj', 'bridges.obj', 'd5ai-bridge.obj', 'd5ai-context-fixture.obj']
    candidate = next((build / 'sources').rglob('d5ai_geometry.h')).parent
    include = out / 'runtime/construction-winner'
    include.mkdir(parents=True)
    names = ['transport.h', 'observer.h', 'patch.h', 'd5ai_geometry.h', 'd5ai_lifetime.h']
    pins = {str(p): sha(p) for p in [source, Path(__file__), VC, *[build / p for p in objects], *[candidate / p for p in names]]}
    for name in names:
        (include / name).write_bytes((candidate / name).read_bytes())
    support = out / 'runtime/exp0002'
    support.mkdir()
    for name in ('win_support.h', 'core.h'):
        path = build / 'sources/runtime/exp0002' / name
        pins[str(path)] = sha(path)
        (support / name).write_bytes(path.read_bytes())
    (out / source.name).write_bytes(source.read_bytes())
    (out / Path(__file__).name).write_bytes(Path(__file__).read_bytes())
    for name in ('d5ai_read_geometry.py','d5ai_read_lifetime.py','read_capture.py'):
        pins[str(ROOT/'runtime/construction-winner'/name)]=sha(ROOT/'runtime/construction-winner'/name)
    for name in ('d5ai_operations.py','d5ai_episode.py'):
        pins[str(Path(__file__).with_name(name))]=sha(Path(__file__).with_name(name))
    command = '@echo off\ncall "' + str(VC) + '"\nif errorlevel 1 exit /b 1\ncl /Bv /nologo /std:c++20 /EHsc /W4 /O2 /MD /DSOR_QUEUE_CAPACITY=32768 /I"' + str(include) + '" ' + source.name + ' ' + ' '.join('"' + str(build / obj) + '"' for obj in objects) + ' /Fe:d5ai-concurrency.exe /link /Brepro /INCREMENTAL:NO /MAP:d5ai-concurrency.map bcrypt.lib\n'
    (out / 'build.cmd').write_text(command, encoding='utf8', newline='\r\n')
    compiled = subprocess.run(['cmd', '/d', '/c', str(out / 'build.cmd')], cwd=out, capture_output=True)
    (out / 'build.log').write_bytes(compiled.stdout + compiled.stderr)
    result = dict(schema='sor-d5ai-integrated-concurrency-qualification/2', inputs=pins, compilation=compiled.returncode, cases=[], actual_observer_kind='Standalone EXE; source-matched native producer plus retained shared-worker integration; not executed DLL16', source_matched_to_candidate16_sha256=sha(build/'SorConstructionWinner.dll'), inline_scope='Driver recompiles retained header templates/direct core emit callers; no claim of identical DLL machine code for those paths')
    if compiled.returncode == 0:
        for mode in ('normal', 'short', 'held', 'overload'):
            guard()
            process = subprocess.run([str(out / 'd5ai-concurrency.exe'), str(out / mode), mode], cwd=out, capture_output=True)
            (out / (mode + '.stdout')).write_bytes(process.stdout)
            (out / (mode + '.stderr')).write_bytes(process.stderr)
            row = dict(mode=mode, exit=process.returncode)
            result['cases'].append(row)
            if process.returncode:
                break
            try:
                row['verification'] = verify_case(out / mode, accept_intra_call_ties=True)
            except Exception as error:
                row['verification_error'] = repr(error)
                break
        map_text=(out/'d5ai-concurrency.map').read_text(encoding='utf8')
        base=int(re.search(r'Preferred load address is ([0-9a-fA-F]+)',map_text)[1],16)
        symbols={}
        for line in map_text.splitlines():
            parts=line.split()
            if len(parts)>=4 and re.fullmatch('[0-9a-fA-F]{4}:[0-9a-fA-F]{8}',parts[0]) and re.fullmatch('[0-9a-fA-F]{16}',parts[2]):
                symbols.setdefault(int(parts[2],16)-base,[]).append(dict(symbol=parts[1],object=parts[-1]))
        first=json.loads((out/'normal/oracle.json').read_bytes()) if (out/'normal/oracle.json').exists() else dict(function_rvas={})
        result['code_origins']={name:dict(rva=rva,map_rows=symbols.get(rva,[])) for name,rva in first['function_rvas'].items()}
        result['origin_rows_complete']=len(result['code_origins'])==11 and all(row['map_rows'] for row in result['code_origins'].values())
        result['driver_object_sha256']=sha(out/'d5ai-concurrency-driver.obj')
        result['link_map_sha256']=sha(out/'d5ai-concurrency.map')
        result['executable_sha256'] = sha(out / 'd5ai-concurrency.exe')
    result['inputs_unchanged'] = all(sha(path) == digest for path, digest in pins.items())
    result['status'] = 'PASS' if compiled.returncode == 0 and len(result['cases']) == 4 and all(row['exit'] == 0 and 'verification' in row for row in result['cases']) and result['inputs_unchanged'] and result.get('origin_rows_complete') else 'FAIL'
    result['final_free'] = guard()
    fresh(out / 'qualification.json', result)
    print(json.dumps(result))
    return 0 if result['status'] == 'PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())
