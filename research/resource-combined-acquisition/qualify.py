# SPDX-License-Identifier: GPL-3.0-or-later
"""Run real disposable Windows debugger fixtures; never attach to retail.

Reads pinned build and source files. Creates fresh ignored SRO1 receipts,
independent readback results, events and process diagnostics. Stdlib plus the
installed MSVC-built fixture/controller are required. STOP intentionally disposes
only the fixture process; no game, save, configuration, network or Git writes.
"""
import ctypes
from ctypes import wintypes
import argparse
import json
from pathlib import Path
import subprocess
import sys

from build import ROOT, LOCAL, pin
from reduce import Tracker, load
transport = load('d5b_transport', 'research/resource-oracle-retail/collect.py')
verifier = load('d5b_framing', 'research/resource-tungsten-acquisition/qualify.py')


from d5b_contract import MODES
independent = verifier.independent

def target_absent(pid):
    """Query only the disposable fixture PID after controller exit."""
    kernel = ctypes.WinDLL('kernel32', use_last_error=True)
    kernel.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
    kernel.OpenProcess.restype = wintypes.HANDLE
    kernel.GetExitCodeProcess.argtypes = [wintypes.HANDLE, ctypes.POINTER(wintypes.DWORD)]
    kernel.CloseHandle.argtypes = [wintypes.HANDLE]
    handle = kernel.OpenProcess(0x1000, False, pid)
    if not handle:
        return ctypes.get_last_error() == 87
    try:
        code = wintypes.DWORD()
        assert kernel.GetExitCodeProcess(handle, ctypes.byref(code))
        return code.value != 259
    finally:
        kernel.CloseHandle(handle)


def write(path, value):
    with path.open('x', encoding='utf8', newline='\n') as stream:
        json.dump(value, stream, indent=2, allow_nan=False)
        stream.write('\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--modes', nargs='+', default=MODES)
    args = parser.parse_args()
    build, out = args.build.resolve(), args.output.resolve()
    assert build.is_relative_to(LOCAL) and out.is_relative_to(LOCAL)
    manifest = json.loads((build / 'build.json').read_text(encoding='utf8'))
    assert manifest['exit_code'] == 0
    for path, expected in manifest['files'].items():
        assert pin(path) == expected, path
    out.mkdir(exist_ok=False)
    results = []
    for mode in args.modes:
        dest = out / mode
        dest.mkdir()
        command = [str(build / 'sor-d5b-fixture-controller.exe'), '--synthetic-fixture',
                   pin(build / 'sor-d5b-fixture.exe'), mode]
        proof = dict(fixture_sha256=pin(build / 'sor-d5b-fixture.exe'), build_sha256=pin(build / 'build.json'),
                     producer_sha256=pin(Path(__file__).with_name('producer.cpp')),
                     consumer_sha256=pin(Path(__file__).with_name('consumer.cpp')))
        tracker, rows, verified, session = Tracker(proof), [], [], None
        with (dest / 'stderr.txt').open('xb') as stderr:
            process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                       stderr=stderr, text=True)
            for line in process.stdout:
                row = json.loads(line)
                row['synthetic'] = True
                rows.append(row)
                if row['kind'] == 'SESSION':
                    session = row
                if row['kind'] != 'SAMPLE':
                    tracker.feed(row)
                    continue
                path = dest / f'capture-{row["capture"]:05d}.bin'
                transport.persist(path, [session, row, dict(kind='END', complete=row['required_reads_complete'])], synthetic=True)
                assert verifier.independent(path)[1] == row
                verified.append(dict(path=str(path), sha256=pin(path), independent_decode=True))
                useful = tracker.feed(row)
                suffix = ' CONSUMER' if useful == 'CONSTRUCTION' and mode in ('combined','linked','linked-reuse','linked-reset') else ' STOP' if useful == 'CONSUMPTION' and mode == 'cache-stop-many' else ' PRODUCER' if row['site'] == 'spatial_transfer_payload' and row['active_updaters'] == 0 else ''
                if mode == 'kill-before-ack' and row['capture'] == 1:
                    kernel = ctypes.WinDLL('kernel32', use_last_error=True)
                    kernel.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
                    kernel.OpenProcess.restype = wintypes.HANDLE
                    kernel.TerminateProcess.argtypes = [wintypes.HANDLE, wintypes.UINT]
                    kernel.CloseHandle.argtypes = [wintypes.HANDLE]
                    handle = kernel.OpenProcess(1, False, row['pid'])
                    assert handle and kernel.TerminateProcess(handle, 0xe0d5b001)
                    kernel.CloseHandle(handle)
                if mode == 'dropped-ack':
                    process.stdin.close()
                else:
                    answer = 'REJECT' if mode == 'ackfail' or mode == 'ackfail-return' and useful == 'CONSTRUCTION' else f'ACK {row["capture"]}{suffix}'
                    process.stdin.write(answer + '\n')
                    process.stdin.flush()
            code = process.wait(timeout=15)
        write(dest / 'events.json', rows)
        write(dest / 'verified.json', verified)
        reduction = tracker.result()
        write(dest / 'reduction.json', reduction)
        write(dest / 'process.json', dict(command=command, controller_exit=code))
        errors = []
        expected = {'empty-generation': (1, 0), 'mask0': (1, 0), 'mask3': (1, 0), 'conflict': (2, 0),
                    'combined': (1, 1), 'linked': (1, 1), 'linked-reuse': (1, 1), 'linked-reset': (1, 1), 'cache-multi': (0, 1), 'cache-stop-many': (0, 1)}
        if mode in expected and (len(tracker.constructions), len(tracker.consumptions)) != expected[mode]:
            errors.append('positive observation count')
        if mode in ('wrong-key', 'wrong-owner', 'wrong-query', 'partial-dnam') and tracker.constructions:
            errors.append('invalid construction promoted')
        if mode.startswith('cache-wrong') or mode in ('cache-unrelated-source', 'cache-stale-transfer', 'cache-pointer-reuse', 'cache-partial-page', 'cache-corrupt', 'cache-nonfinite'):
            if tracker.consumptions:
                errors.append('invalid consumption promoted')
        for construction in tracker.constructions:
            assert isinstance(construction['provider_token'], int) and construction['provider_token'] > 0
            entry = next(r for r in rows if r['kind']=='SAMPLE' and r.get('site')=='generation_entry' and [r['pid'],r['tid'],r['thread_lifetime'],r['invocation_token']]==construction['context'])
            assert construction['provider_token']==entry['provider_token']==entry['upstream_provider_token']
        if mode == 'conflict' and [r['mask'] for r in tracker.constructions] != [0, 3]:
            errors.append('conflicting masks lost')
        if mode == 'empty-generation' and tracker.constructions and tracker.constructions[0]['calls']:
            errors.append('zero calls replaced by invented candidates')
        if mode == 'cache-empty-transfer' and not tracker.empty_transfers:
            errors.append('observed empty transfer lost')
        if bool(tracker.links) != (mode == 'linked'):
            errors.append('synthetic lifetime linkage oracle')
        if any(r.get('producer_consumer_link') for r in [reduction]):
            errors.append('invented epoch')
        stop = next((i for i, r in enumerate(rows) if r['kind'] == 'STOP_COMMITTED'), None)
        if stop is not None and any(r['kind'] in ('SAMPLE', 'PHASE', 'THREAD_BEGIN', 'STARTUP_ARMED', 'RESUME_VERIFIED') for r in rows[stop+1:]):
            errors.append('post-STOP observation or rearming')
        expected_codes = {0, 2} if mode == 'kill-before-ack' else {2} if mode == 'injected-context-failure' else {0}
        if code not in expected_codes:
            errors.append('controller exit')
        if mode == 'ackfail-return' and reduction['constructions']:
            errors.append('unacknowledged construction promoted')
        if mode == 'kill-before-ack' and (tracker.constructions or tracker.consumptions or not any(r['kind']=='EXIT' and r['code']==0xe0d5b001 for r in rows)):
            errors.append('pre-ACK target failure oracle')
        assert target_absent(session['pid']), 'synthetic PID survived'
        for item in verified:
            assert pin(item['path']) == item['sha256']
            verifier.independent(Path(item['path']))
        results.append(dict(mode=mode, controller_exit=code, samples=len(verified),
                            constructions=len(tracker.constructions), consumptions=len(tracker.consumptions),
                            status=reduction['status'], errors=errors))
        print(mode, code, results[-1]['status'], errors, flush=True)
    if 'mask0' in args.modes and 'mask3' in args.modes:
        pair = [json.loads((out/m/'reduction.json').read_text(encoding='utf8'))['constructions'][0] for m in ('mask0','mask3')]
        assert [r['mask'] for r in pair] == [0,3]
        assert pair[0]['first_query_xy_i32_le'] != pair[1]['first_query_xy_i32_le']
        assert pair[0]['geographic_operand']['raw'] != pair[1]['geographic_operand']['raw']
    write(out / 'summary.json' , dict(schema='sor-d5b-qualification/1',
        build_sha256=pin(build / 'build.json'), cases=results, passed=all(not r['errors'] for r in results)))
    assert all(not r['errors'] for r in results), 'failures preserved'


if __name__ == '__main__':
    main()
