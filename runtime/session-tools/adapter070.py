# SPDX-License-Identifier: GPL-3.0-or-later
"""Thin adapter to project-owned 070 operate/decoder; no builds or native edits.
Provenance: runtime/beacon-resource-070/{operate,watch,inspect_resources}.py,
HEAD 0d443482f82c8f1a3750461c6bfec96bd0a6e56e. Semantics remain version-specific.
"""
import importlib.util
from pathlib import Path
import sys
from common import read, sha

SRC = Path(__file__).resolve().parents[1] / 'beacon-resource-070'
sys.path.insert(0, str(SRC))
spec = importlib.util.spec_from_file_location('sor070operate', SRC / 'operate.py')
ops = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ops)


def full(build, pin):
    return ops.manifest(Path(build), pin)


def prelaunch_processes():
    spec = importlib.util.spec_from_file_location('sor050ops', SRC.parent / 'native-oracle-050/operate.py')
    older = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(older)
    return older.processes()


def deployed(m, expected=True):
    ops.audit_deployed(m, expected)
    if expected:
        plugins = ops.GAME / 'Data/SFSE/Plugins'
        names = sorted(p.name for p in plugins.glob('*.dll'))
        conflicts = [n for n in names if n.lower() != 'sornativepositionoracle.dll'
                     and any(x in n.lower() for x in ('sor', 'beaconobserver', 'nativeposition'))]
        if conflicts:
            raise ValueError('competing_observer: ' + repr(conflicts))
        return names


def session(path, m):
    p = ops.session_path(path)
    return p, ops.session_identity(p, m)


def process(s):
    return ops.process_state(s['pid'], s['process_creation_filetime'])


def identity(row, s):
    for k in ('version', 'schema', 'pid', 'process_creation_filetime', 'dll_sha256',
              'game_sha256', 'sfse_sha256', 'module_base'):
        if row.get(k) != s.get(k):
            raise ValueError('worker_identity: ' + k)


def integrity_fields(row):
    if type(row.get('failed')) is not int or row['failed'] < 0 or type(row.get('integrity_failure')) is not bool:
        raise ValueError('missing_or_malformed_worker_integrity_fields')


def health(p, s):
    errors = []
    for name in ('failure.json', 'not-ready.json', 'emergency-status.json'):
        if (p / name).exists():
            row = read(p / name)
            if name != 'emergency-status.json' or row.get('error'):
                errors.append(name)
    last = None
    partial = False
    if (p / 'health.jsonl').exists():
        with (p / 'health.jsonl').open('rb') as f:
            f.seek(0, 2)
            end = f.tell()
            f.seek(max(0, end - 65536))
            lines = f.read().split(b'\n')
        partial = bool(lines[-1])
        # A complete malformed latest line is evidence corruption, not skipped.
        if len(lines) > 1:
            last = __import__('json').loads(lines[-2])
            identity(last, s)
            integrity_fields(last)
            if last.get('integrity_failure') or last.get('failed'):
                errors.append('worker_integrity_failure')
    return dict(errors=errors, last=last, partial_current_line=partial)


def status(p, m, s, request):
    h = health(p, s)
    if h['errors']:
        return dict(status='WORKER_FAILURE', health=h)
    if (p / 'retired.json').exists():
        r = read(p / 'retired.json')
        identity(r, s)
        integrity_fields(r)
        bad = (r.get('failed') or r.get('integrity_failure') or r.get('error') or r.get('active')
               or r.get('captured') is None or r.get('captured') != r.get('last_durable_sequence'))
        return dict(status='RETIREMENT_ERROR' if bad else 'RETIRED', terminal=r, health=h)
    if (p / 'operator-stop.flag').exists() and (p / 'operator-stop.flag').read_bytes() == b'STOP' or (p / 'STOP').exists():
        return dict(status='STOP_PENDING_RETIREMENT', health=h)
    if not (p / 'ready.json').exists():
        return dict(status='WAITING_READY', health=h)
    ready = read(p / 'ready.json')
    identity(ready, s)
    if ready.get('capture_active') is not True or ready.get('group_flush_spool') is not True:
        raise ValueError('ready_contract')
    admission = ops.admission(p, m, s)
    if request is None:
        return dict(status='WAITING_FRESH_ACK', admission=admission, health=h)
    nonce = request['nonce']
    ackpath = p / ('ack-' + nonce + '.json')
    if not ackpath.exists():
        return dict(status='WAITING_ACK', admission=admission, health=h)
    ack = read(ackpath)
    identity(ack, s)
    integrity_fields(ack)
    if ack.get('nonce') != nonce or ack.get('integrity_failure') or ack.get('failed') or ack.get('stopping'):
        raise ValueError('ack_mismatch_or_worker_failure')
    return dict(status='READY_ACK', admission=admission, ack=ack, health=h,
                warning='Nonce proves response to this request, not perpetual freshness; request again at phase boundaries. Compare health serial progress; delay alone is not failure.')


def inspect(p):
    r = ops.inspect(p)
    return {k: v for k, v in r.items() if k not in ('evaluations', 'ui_updates')}
