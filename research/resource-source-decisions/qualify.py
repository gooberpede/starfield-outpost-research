# SPDX-License-Identifier: GPL-3.0-or-later
"""Exercise actual disposable Windows targets through four fixed hardware probes.

Reads a hash-bound build. Writes fresh ignored raw events, SRO1 receipts, durable
ACKs, reductions and expected/observed results. Reuses owned C1 transport and D4
independent decoder. Executes only the pinned sibling fixture/controller. STOP
and intentional crash cases dispose synthetic processes; never retail or saves.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import subprocess
import ctypes
from build import ROOT, LOCAL, pin
from reduce import reduce


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


transport = load('d5e_transport', 'research/resource-oracle-retail/collect.py')
verifier = load('d5e_verifier', 'research/resource-tungsten-acquisition/qualify.py')


def write(path, value):
    transport.write(path, value)


def target_absent(pid):
    kernel = ctypes.WinDLL('kernel32', use_last_error=True)
    kernel.OpenProcess.restype = ctypes.c_void_p
    kernel.OpenProcess.argtypes = [ctypes.c_ulong, ctypes.c_int, ctypes.c_ulong]
    kernel.GetExitCodeProcess.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_ulong)]
    kernel.CloseHandle.argtypes = [ctypes.c_void_p]
    handle = kernel.OpenProcess(0x1000, False, pid)
    if not handle:
        return ctypes.get_last_error() == 87
    code = ctypes.c_ulong()
    gone = bool(kernel.GetExitCodeProcess(handle, ctypes.byref(code)) and code.value != 259)
    kernel.CloseHandle(handle)
    return gone


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--modes', nargs='+')
    args = parser.parse_args()
    build, out = args.build.resolve(), args.output.resolve()
    assert build.is_relative_to(LOCAL) and out.is_relative_to(LOCAL)
    manifest = json.loads((build / 'build.json').read_text())
    assert manifest['exit_code'] == 0
    for path, digest in manifest['files'].items():
        assert pin(path) == digest, path
    out.mkdir(exist_ok=False)
    modes = ('basic', 'reuse', 'reset', 'replacement', 'interleave', 'threads', 'nested', 'partial', 'failed-insert',
             'stale', 'misleading', 'invalid', 'crash', 'bypass-incomplete', 'hit-unknown',
             'stop', 'bad-ack', 'lost-sequence', 'corruption', 'slot-pressure', 'lost-slot', 'interrupted-teardown')
    if args.modes:
        assert all(mode in modes for mode in args.modes)
        modes = tuple(args.modes)
    results = []
    for mode in modes:
        dest = out / mode
        dest.mkdir()
        command = [str(build / 'sor-d5e-controller.exe'), '--synthetic-fixture',
                   pin(build / 'sor-d5e-fixture.exe'), mode]
        rows, captures = [], []
        pid, session = None, None
        with (dest / 'stderr.txt').open('xb') as stderr:
            process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                stderr=stderr, text=True)
            for line in process.stdout:
                row = json.loads(line)
                rows.append(row)
                if row['kind'] == 'SESSION':
                    pid = row['pid']
                    session = row
                if row['kind'] in ('ARM_BARRIER', 'SAMPLE'):
                    path = dest / f'capture-{len(captures):05d}.bin'
                    envelope = [dict(session, acquisition=str(dest)),
                                dict(kind='SAMPLE', event=row), dict(kind='END', complete=True)]
                    ack = transport.persist(path, envelope, synthetic=True)
                    assert verifier.independent(path) == envelope
                    captures.append(dict(path=str(path), **ack))
                    if row['kind'] == 'ARM_BARRIER':
                        answer = 'ARM_ACK'
                    else:
                        answer = f'ACK {row["capture"]}'
                        if mode == 'stop' and row['capture'] == 4:
                            answer += ' STOP'
                        if mode == 'bad-ack':
                            answer = 'REJECT'
                        if mode == 'interrupted-teardown' and row['capture'] == 1:
                            kernel = ctypes.WinDLL('kernel32', use_last_error=True)
                            kernel.OpenProcess.restype = ctypes.c_void_p
                            kernel.OpenProcess.argtypes = [ctypes.c_ulong, ctypes.c_int, ctypes.c_ulong]
                            kernel.TerminateProcess.argtypes = [ctypes.c_void_p, ctypes.c_uint]
                            kernel.CloseHandle.argtypes = [ctypes.c_void_p]
                            handle = kernel.OpenProcess(1, False, pid)
                            assert handle and kernel.TerminateProcess(handle, 0xd5e1)
                            kernel.CloseHandle(handle)
                    process.stdin.write(answer + '\n')
                    process.stdin.flush()
            code = process.wait(timeout=15)
        result = reduce(rows)
        write(dest / 'events.json', rows)
        write(dest / 'receipts.json', captures)
        write(dest / 'reduction.json', result)
        errors = []
        tiers = [d['tier'] for d in result['decisions']]
        branches = [d['decision'] for d in result['decisions']]
        failures = ('bad-ack', 'slot-pressure', 'lost-slot', 'interrupted-teardown')
        if mode not in (*failures, 'stop') and (tiers[:3] != ['A', 'B', 'B'] or branches[:3] != ['MAP_MISS', 'MAP_HIT', 'VISITED_BYPASS']):
            errors.append('initial independent branch oracle')
        if mode in ('reuse', 'reset', 'replacement'):
            if [d['mask'] for d in result['decisions'] if d['tier'] == 'A'] != [0, 3]:
                errors.append('contradictory masks conflated')
            if len(result['decisions']) < 4 or result['decisions'][0]['lifetime'] == result['decisions'][-1]['lifetime']:
                errors.append('lifetime reuse conflated')
        if mode in ('interleave', 'threads'):
            # Four workers each issue ten hits on the same selected pointer,
            # plus the final hit and initial three; unrelated misses also nest.
            expected = 4 + 4 * 10
            if len(result['decisions']) != expected:
                errors.append(f'interleaved selected decisions: expected {expected}, observed {len(result["decisions"])}')
        if mode in ('partial', 'stale', 'failed-insert') and (not tiers or tiers[-1] != 'C'):
            errors.append('incomplete/stale promotion')
        if mode == 'invalid' and not result['rejected']:
            errors.append('invalid read accepted')
        if mode == 'misleading' and len(result['decisions']) != 3:
            errors.append('unrelated identity promoted')
        if mode in ('bypass-incomplete', 'hit-unknown') and (not tiers or tiers[-1] != 'B'):
            errors.append('reuse requires invented historical construction')
        if result['first_ever'] != 'UNKNOWN':
            errors.append('first-observed promoted to first-ever')
        if mode == 'lost-sequence':
            mutated = [dict(r) for r in rows]
            next(r for r in mutated if r['kind'] == 'SAMPLE')['capture'] += 1
            if any(d['tier'] in ('A', 'B') for d in reduce(mutated)['decisions']):
                errors.append('sequence loss did not close coverage')
        if mode == 'corruption':
            raw = bytearray(Path(captures[0]['path']).read_bytes())
            raw[len(raw)//2] ^= 1
            corrupt = dest / 'corrupt.bin'
            corrupt.write_bytes(raw)
            try:
                verifier.independent(corrupt)
                errors.append('transport corruption accepted')
            except (ValueError, AssertionError, RuntimeError, UnicodeError):
                pass
        if code not in ((0, 2) if mode == 'interrupted-teardown' else (2,) if mode in failures else (0,)):
            errors.append(f'controller exit {code}')
        if mode in failures and not any(r['kind'] in ('GAP', 'FAILURE_CLEANUP') for r in rows):
            errors.append('failure without coverage-loss record')
        stopped = next((i for i, r in enumerate(rows) if r['kind'] == 'STOP_COMMITTED'), None)
        if mode == 'stop' and (stopped is None or not any(r['kind'] == 'SAMPLE' and r['capture'] == 4 for r in rows)
                or not any(r['kind'] == 'EXIT' and r['code'] == 0xd5e0 for r in rows)):
            errors.append('requested durable stop/disposal boundary not witnessed')
        if stopped is not None and any(r['kind'] in ('SAMPLE', 'THREAD_ARMED', 'ARM_BARRIER') for r in rows[stopped+1:]):
            errors.append('post-stop sampling or rearming')
        kernel = ctypes.WinDLL('kernel32', use_last_error=True)
        kernel.OpenProcess.restype = ctypes.c_void_p
        kernel.OpenProcess.argtypes = [ctypes.c_ulong, ctypes.c_int, ctypes.c_ulong]
        kernel.GetExitCodeProcess.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_ulong)]
        kernel.CloseHandle.argtypes = [ctypes.c_void_p]
        handle = kernel.OpenProcess(0x1000, False, pid)
        if handle:
            exit_code = ctypes.c_ulong()
            absent = bool(kernel.GetExitCodeProcess(handle, ctypes.byref(exit_code)) and exit_code.value != 259)
            kernel.CloseHandle(handle)
        else:
            absent = ctypes.get_last_error() == 87
        if not absent:
            errors.append('disposable target still active or absence unverified')
        write(dest / 'process.json', dict(command=command, controller_exit=code))
        record = dict(mode=mode, pass_=not errors, errors=errors, decisions=len(tiers),
            captures=len(captures), tiers=tiers, target_absent=absent, build_sha256=pin(build / 'build.json'))
        results.append(record)
        print(mode, 'PASS' if not errors else errors, flush=True)
    write(out / 'matrix.json', results)
    pump = load('d5e_collect_test', 'research/resource-source-decisions/collect.py')
    pump_out = out / 'shared-pump'
    command = [str(build / 'sor-d5e-controller.exe'), '--synthetic-fixture', pin(build / 'sor-d5e-fixture.exe'), 'basic']
    pump_code = pump.pump(command, pump_out, dict(synthetic=True), pin(build / 'build.json'), True)
    pump_rows = [json.loads(line) for line in (pump_out / 'events.jsonl').read_text().splitlines()]
    pump_result = reduce(pump_rows)
    pump_pass = pump_code == 0 and [d['tier'] for d in pump_result['decisions']] == ['A', 'B', 'B'] and (pump_out / 'READY.json').is_file()
    write(out / 'shared-pump.json', dict(pass_=pump_pass, controller_exit=pump_code, reduction=pump_result))
    assert pump_pass
    failures = []
    for fault in ('pre-arm-stop', 'idle-collector-loss', 'idle-pipe-loss'):
        folder = out / fault
        command[-1] = 'idle'
        try:
            fault_code = pump.pump(command, folder, dict(synthetic=True), pin(build / 'build.json'), True, fault)
        except RuntimeError:
            assert fault == 'idle-collector-loss'
            fault_code = None
        fault_rows = [json.loads(line) for line in (folder / 'events.jsonl').read_text().splitlines()]
        pid = next(r['pid'] for r in fault_rows if r['kind'] == 'SESSION')
        gone = target_absent(pid)
        success = gone and not any(r['kind'] == 'SAMPLE' for r in fault_rows)
        if fault == 'pre-arm-stop':
            success &= not (folder / 'READY.json').exists() and fault_code == 2
            success &= any(r['kind'] == 'STOP_COMMITTED' for r in fault_rows)
        elif fault == 'idle-collector-loss':
            success &= (folder / 'transport-failure.json').is_file()
        else:
            success &= fault_code == 2 and any(r['kind'] == 'FAILURE_CLEANUP' for r in fault_rows)
        failures.append(dict(case=fault, pass_=bool(success), target_absent=gone, controller_exit=fault_code))
    write(out / 'pump-failures.json', failures)
    assert all(r['pass_'] for r in failures), failures
    return int(any(not r['pass_'] for r in results))


if __name__ == '__main__':
    raise SystemExit(main())
