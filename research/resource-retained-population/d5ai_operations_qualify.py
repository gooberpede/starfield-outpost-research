# SPDX-License-Identifier: GPL-3.0-or-later
"""Challenge postflight capture and preservation failure paths offline.

Uses actual completed native bytes but explicitly substitutes fixture-only
finalization and modeled preservation audits. These controls never count as a
full real preflight, retail authority or save-protection rehearsal. Writes only
fresh ignored copies. No process, game, save, deployment or network operations.
"""
from pathlib import Path
from types import SimpleNamespace
import copy
import json
import shutil
import hashlib
import sys

import d5ai_operations as operations
from d5ai_episode import ROOT


def main():
    source, out = (Path(p).resolve() for p in sys.argv[1:3])
    if not out.is_relative_to(ROOT / '.local-work/d5ai-recorder'):
        raise ValueError('Fresh task-local output required')
    out.mkdir(exist_ok=False)
    identity = json.loads((source / 'identity.json').read_bytes())
    before = dict(protection=dict(fixture_protection=True), remote_protected_sizes=dict(fixture=123), receipt_sha256='a' * 64)
    plan = dict(episode='A', dll_sha256=identity['dll_sha256'], deployed_dll=str(out / 'absent-candidate.dll'), plan_sha256='b' * 64)
    checks = []
    original_verify, original_legacy, original_finalization = operations.verify_plan, operations.legacy, operations.finalization

    def compare(a, b):
        if a != b:
            raise ValueError('Modeled protected bytes changed')

    def full(path):
        return copy.deepcopy(before['protection'])

    module = SimpleNamespace(original_process_gone=lambda identity: 'FIXTURE_PROCESS_ALREADY_ENDED',
                             full=full, compare_protection=compare,
                             remote_sizes=lambda value: copy.deepcopy(before['remote_protected_sizes']))
    operations.verify_plan = lambda plan: None
    operations.legacy = lambda: module
    operations.finalization = lambda *args: dict(fixture_only=True)

    def run(name, prepare=lambda target, terminal: None, expected='PARTIAL_POSTFLIGHT'):
        target = out / name
        shutil.copytree(source, target)
        terminal = json.loads((target / 'terminal.json').read_bytes())
        prepare(target, terminal)
        value = operations.postflight(plan, before, target, {}, out)
        if value['status'] != expected:
            raise AssertionError((name, value['status'], value['capture_errors'], value['protection_errors']))
        checks.append(dict(name=name, expected=expected, passed=True))

    try:
        run('actual-native-capture-with-modeled-preservation', expected='PASS_POSTFLIGHT')
        run('missing-journal', lambda target, terminal: (target / 'lifetimes.bin').unlink())
        run('missing-ledger', lambda target, terminal: (target / 'lifetimes-flush.jsonl').unlink())
        def loss(target, terminal):
            terminal['lifetime_drops'] = 1
            (target / 'terminal.json').write_text(json.dumps(terminal), encoding='utf8')
        run('native-journal-loss', loss)
        def raw_tamper(target, terminal):
            path = target / 'geometry-1.bin'
            data = bytearray(path.read_bytes())
            data[-1] ^= 1
            path.write_bytes(data)
        run('geometry-byte-tamper', raw_tamper)
        Path(plan['deployed_dll']).write_bytes(b'owned unexpected deployed marker')
        run('effective-candidate-still-present')
        Path(plan['deployed_dll']).unlink()
        module.remote_sizes = lambda value: dict(fixture=124)
        run('remote-preservation-change')
        module.remote_sizes = lambda value: copy.deepcopy(before['remote_protected_sizes'])
        module.full = lambda path: dict(fixture_protection=False)
        run('protected-byte-audit-mismatch')
        module.full = full
        def bad_finalization(*args):
            raise ValueError('Modeled missing owned STOP')
        operations.finalization = bad_finalization
        run('owned-finalization-refused')
    finally:
        operations.verify_plan, operations.legacy, operations.finalization = original_verify, original_legacy, original_finalization
    result = dict(schema='sor-d5ai-operations-controls/1', status='PASS', checks=checks, method_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), wrapper_sha256=hashlib.sha256(Path(operations.__file__).read_bytes()).hexdigest(),
                  scope='Actual native file readers plus modeled preservation/finalization failure gates; no real protection/preflight/authority claim')
    (out / 'qualification.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf8', newline='\n')
    print(json.dumps(dict(status='PASS', checks=len(checks))))


if __name__ == '__main__':
    main()
