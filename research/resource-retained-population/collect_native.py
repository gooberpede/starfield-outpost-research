# SPDX-License-Identifier: GPL-3.0-or-later
"""D5L future attachment transport; NOT authorized by Phase A.

Adapted from the maintainer-owned D5E collect.py (SOR-P-0002).

Requires a separately approved run card/GO and hash-bound admission receipt.
Reads that receipt, build/source pins and target PID. Runs the native controller,
persists SRO1 snapshots/ACKs plus a flushed event journal in a fresh ignored
directory. STOP may terminate the target under the future crash-tolerant policy.
No game launch, save/configuration/database writes, network or Git operations.
"""
import argparse
import json
import os
from pathlib import Path
import queue
import shutil
import subprocess
import threading
import importlib.util
from build import ROOT, LOCAL, pin
from prepare_native import SOURCE
from preservation_native import verify_build_files, PREFLIGHT_SCHEMA


def admission_checks(gate):
    assert gate['status']=='GO' and gate['phase']=='B' and gate['source']==SOURCE
    assert gate['approval_reference'].strip() and gate['cloud_confirmed'] is True
    assert set(gate['allowed_interventions'])=={'software_int3_14','all_stop_and_peer_suspend','owned_rip_tf_rearm','termination_teardown'}
    for field in ('run_card','preflight','build_manifest'):
        assert pin(gate[field]['path'])==gate[field]['sha256']
    pre=json.loads(Path(gate['preflight']['path']).read_text())
    assert pre['schema']==PREFLIGHT_SCHEMA and pre['status']=='OFFLINE_CHECKED_NOT_AUTHORIZED' and pre['source']==SOURCE and pre['run_card']==gate['run_card'] and pre['build_manifest']==gate['build_manifest']
    assert all(pin(f)==h for f,h in pre['code_pins'].items())
    import sys
    sys.path.insert(0,str(ROOT/'research/resource-carinae-source-context'))
    from save_policy import load_policy,policy_hash,sizes,partition
    policy=load_policy();assert policy_hash(policy)==pre['save_policy_sha256']
    def light(folder,expected):
        parts=partition(sizes(Path(folder),policy),policy);assert not parts['unclassified']
        assert {n:r['bytes'] for n,r in parts['protected'].items()}=={n:r['bytes'] for n,r in partition(expected,policy)['protected'].items()}
    light(pre['live_path'],pre['protected_live'])
    def unchanged(f,r):
        st=Path(f).stat();return st.st_size==r['bytes'] and st.st_mtime_ns==r['mtime_ns']
    assert all(unchanged(f,r) for f,r in pre['archive_guard'].items())
    for candidates in pre['backups'].values():
        assert any(r['kind']=='AUTHENTICATED_ARCHIVE_MEMBER' or (Path(r['path']).is_file() and unchanged(r['path'],r['metadata'])) for r in candidates)
    remote=Path(pre['sync']['remote_path']);light(remote/'Saves',pre['sync']['remote'])
    other={p.relative_to(remote).as_posix():dict(bytes=p.stat().st_size,sha256=pin(p)) for p in remote.rglob('*') if p.is_file() and not p.is_relative_to(remote/'Saves')}
    assert other==pre['sync']['other']
    for f,r in pre['installed'].items():
        st=Path(f).stat();assert st.st_size==r['bytes'] and st.st_mtime_ns==r['mtime_ns']
    for f,r in pre['file_guards'].items():
        st=Path(f).stat();assert st.st_size==r['bytes'] and st.st_mtime_ns==r['mtime_ns']
    assert gate['creation_filetime_100ns']>pre['created_filetime_100ns'] and gate['used'] is False
    return pre


def load(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


transport = load('d5e_pump_transport', 'research/resource-oracle-retail/collect.py')
verifier = load('d5e_pump_decoder', 'research/resource-tungsten-acquisition/qualify.py')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--retail-pilot', action='store_true', required=True)
    parser.add_argument('--admission', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    admission, output = args.admission.resolve(), args.output.resolve()
    assert admission.is_relative_to(LOCAL) and output.is_relative_to(LOCAL)
    gate = json.loads(admission.read_text())
    pre = admission_checks(gate)
    # This gate records an already explicit human GO; it never supplies authority.
    manifest = json.loads(Path(gate['build_manifest']['path']).read_text())
    assert manifest['exit_code'] == 0
    assert verify_build_files(manifest)==pre['operational_sources']
    controller = Path(gate['build_manifest']['path']).parent / 'sor-d5l-native-controller.exe'
    assert pin(controller) == manifest['files'][str(controller)]
    assert min(shutil.disk_usage(d).free for d in ('C:/', 'D:/')) >= 40_000_000_000
    transport.write(admission.with_suffix('.consumed.json'),dict(admission_sha256=pin(admission),pid=gate['pid'],creation_filetime_100ns=gate['creation_filetime_100ns'],output=str(output)))
    return pump([str(controller), '--retail-pilot', str(gate['pid']),str(gate['creation_filetime_100ns'])], output, gate, pin(admission), False)


def pump(command, output, gate, admission_hash, synthetic, test_failure=None):
    """Shared bounded external transport, also exercised by disposable fixtures."""
    output.mkdir(exist_ok=False)
    transport.write(output / 'admission.json', gate)
    assert test_failure is None or synthetic
    if test_failure == 'pre-arm-stop':
        (output / 'STOP').write_bytes(b'fixture cancellation\n')
    stderr = (output / 'stderr.txt').open('xb')
    process = subprocess.Popen(command,
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=stderr, text=True)
    try:
        return _events(process, output, admission_hash, synthetic, test_failure)
    except BaseException as error:
        try:
            transport.write(output / 'transport-failure.json', dict(reason=type(error).__name__,
                detail=str(error), coverage='GAP', controller_pid=process.pid))
        except OSError:
            pass
        raise
    finally:
        # The controller owns kill-on-debugger-exit. Retiring it after transport
        # failure intentionally disposes the research target under the card.
        if process.poll() is None:
            process.terminate()
        process.wait(timeout=15)
        process.stdin.close()
        process.stdout.close()
        stderr.close()


def _events(process, output, admission_hash, synthetic, test_failure):
    incoming = queue.Queue(maxsize=32)
    def reader():
        for line in process.stdout:
            incoming.put(line)
        incoming.put(None)
    threading.Thread(target=reader, daemon=True).start()
    session, number, stopping = None, 0, False
    with (output / 'events.jsonl').open('x', encoding='utf8', newline='\n') as journal:
        while True:
            try:
                line = incoming.get(timeout=1)
            except queue.Empty:
                if test_failure == 'idle-collector-loss':
                    raise RuntimeError('synthetic idle collector failure')
                if test_failure == 'idle-pipe-loss':
                    process.stdin.close()
                    test_failure = None
                # An idle STOP is an intentional abort and may precede a queued
                # sample; that race yields a declared GAP, never a forged ACK.
                if not stopping and ((output / 'STOP').exists() or min(shutil.disk_usage(d).free for d in ('C:/', 'D:/')) < 40_000_000_000):
                    process.stdin.write('STOP\n');process.stdin.flush();stopping=True
                continue
            if line is None:
                break
            row = json.loads(line)
            journal.write(json.dumps(row) + '\n');journal.flush();os.fsync(journal.fileno())
            if row['kind'] == 'SESSION':
                assert session is None and row['synthetic'] is synthetic
                session = row
            if row['kind'] in ('SAMPLE', 'ARM_BARRIER'):
                assert session
                number += 1
                envelope = [dict(session, admission_sha256=admission_hash),
                    dict(kind='SAMPLE', event=row), dict(kind='END', complete=row.get('read_complete', True))]
                path = output / f'capture-{number:06d}.bin'
                transport.persist(path, envelope, synthetic=synthetic)
                assert verifier.independent(path) == envelope
                if stopping:
                    continue
                if row['kind'] == 'ARM_BARRIER':
                    if (output / 'STOP').exists():
                        answer = 'STOP'
                        stopping = True
                    else:
                        answer = 'ARM_ACK'
                        transport.write(output / 'READY.json', dict(admission_sha256=admission_hash,
                            barrier_sha256=pin(path), session=session, state='ARMED_BEFORE_OPERATOR_LOAD'))
                else:
                    suffix = ' STOP' if (output / 'STOP').exists() or not row.get('read_complete',False) or (row.get('frame_valid') is False) else ''
                    answer = f'ACK {row["capture"]}{suffix}'
                    stopping = bool(suffix)
                process.stdin.write(answer + '\n');process.stdin.flush()
    code = process.wait(timeout=15)
    transport.write(output / 'controller-exit.json', dict(exit_code=code, requested_stop=stopping))
    return code


if __name__ == '__main__':
    raise SystemExit(main())
