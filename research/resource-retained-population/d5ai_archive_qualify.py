# SPDX-License-Identifier: GPL-3.0-or-later
"""Qualify unchanged archival on one actual completed offline native session.

Allowed: query original PID/creation/exit through query-only handles; authenticate
core, Raw2, lifetime and owned STOP files; seal and ZIP/Deflate stream-verify the
quiescent original tree plus an explicitly fixture-only companion. Writes only
fresh ignored contract, companion, roots, seal, ZIP and verification receipts.
Risk: source drift, insufficient caller-available disk or incorrect inventory.
STOP on any pin, process, reader, reparse, inventory, disk or archive failure.
Both C:/ and D:/ retain 40,000,000,000 caller-available bytes. Cleanup preserves
the original tree and every new artifact, including failed receipts; no deletion.
No game, save, deployment, process intervention, retail approval or network use.
"""
from pathlib import Path
import hashlib
import importlib.util
import json
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'runtime/session-tools'))
sys.path.insert(0, str(ROOT / 'runtime/construction-winner'))
from common import fresh, guard, inventory, regular, sha
from read_capture import inspect
from d5ai_read_geometry import read_session
from d5ai_read_lifetime import read_prefix, qualify_snapshot
from d5ai_operations import worker_json, legacy

ARCHIVE_PATH = ROOT / 'runtime/session-tools/archive.py'
spec = importlib.util.spec_from_file_location('d5ai_unchanged_archive', ARCHIVE_PATH)
archive = importlib.util.module_from_spec(spec)
spec.loader.exec_module(archive)


def module_pins():
    paths = {Path(__file__).resolve(), ARCHIVE_PATH, ROOT/'research/resource-retained-population/d5ab_p4_operations.py', Path(sys.executable).resolve()}
    for module in list(sys.modules.values()):
        path = getattr(module, '__file__', None)
        if path and Path(path).is_file():
            paths.add(Path(path).resolve())
    return {str(path): sha(path) for path in sorted(paths)}


def main():
    session, out = (regular(p).resolve() for p in sys.argv[1:3])
    expected = ROOT / '.local-work/d5ai-recorder/native-controller03/session'
    if session != expected or not out.is_relative_to(ROOT / '.local-work/d5ai-recorder'):
        raise ValueError('Exact completed owned fixture and fresh task-local output required')
    if out.is_relative_to(session) or session.is_relative_to(out):
        raise ValueError('Archive output must remain outside the original source tree')
    initial_free = guard()
    out.mkdir(exist_ok=False)
    fresh(out / 'contract.json', dict(
        schema='sor-d5ai-archive-contract/1', session=str(session),
        question='Can unchanged offline archival preserve and verify every actual Raw2/lifetime session byte?',
        allowed_actions=['Read files', 'Query PID creation and exit only', 'Authenticate actual completed fixture',
                         'Create fresh companion and partial seal', 'ZIP/Deflate and stream every member to SHA256'],
        outputs=str(out), risks=['Source drift', 'Disk exhaustion', 'Inventory or archive mismatch'],
        stop=['Any source pin or process/reader/STOP/inventory/guard failure', 'Caller-available C/D bytes below 40 GB floor'],
        cleanup='Preserve original session, ZIP and all receipts; no deletion or extraction',
        authority='OFFLINE FIXTURE ONLY; no retail episode, GO, full protection audit or publication claim',
        initial_free=initial_free))
    try:
        source_before = inventory(session)
        identity = json.loads((session / 'identity.json').read_bytes())
        if identity['retail'] is not False:
            raise ValueError('Disposable fixture required')
        process_module = legacy()
        deps = module_pins()
        process_state = process_module.original_process_gone(identity)
        if process_state not in ('GONE', 'EXITED', 'ORIGINAL_GONE_PID_REUSED'):
            raise ValueError('Original fixture process not established gone')
        terminal = worker_json(session / 'terminal.json')
        core = inspect(session, identity['dll_sha256'])
        geometry = read_session(session)
        lifetime = read_prefix(session, terminal)
        if not core['complete_session'] or geometry['errors'] or len(geometry['snapshots']) != 2:
            raise ValueError('Actual completed core/Raw2 fixture required')
        for snapshot in geometry['snapshots']:
            if not snapshot['complete_representation']:
                raise ValueError('Incomplete actual geometry checkpoint')
            qualify_snapshot(snapshot, lifetime)
        state = json.loads((session / 'p4-state.json').read_bytes())
        stop = state['stop']
        identity_hash = sha(session / 'identity.json')
        if (state['identity_sha256'] != identity_hash or stop['identity_sha256'] != identity_hash or
                stop['owner'] != state['owner'] or len(state['owner']) != 32 or len(stop['stop_nonce']) != 32 or
                (session / 'STOP').read_bytes() != (json.dumps(stop, sort_keys=True) + '\n').encode() or
                state['telemetry_fault'] or not terminal['resident_inert']):
            raise ValueError('Owned native STOP evidence mismatch')
        controller_receipt = json.loads((session.parent / 'qualification.json').read_bytes())
        if controller_receipt['status'] != 'PASS' or controller_receipt['stop']['stop'] != stop:
            raise ValueError('Actual controller receipt mismatch')
        companion = out / 'companion'
        companion.mkdir()
        fresh(companion / 'core-authentication.json', core)
        fresh(companion / 'geometry-authentication.json', geometry)
        fresh(companion / 'lifetime-authentication.json', lifetime)
        fresh(companion / 'owned-stop.json', stop)
        fresh(companion / 'actual-controller-receipt.json', controller_receipt)
        fresh(companion / 'module-dependencies.json', dict(pins=deps, python_version=sys.version))
        postflight = companion / 'fixture-postflight.json'
        fresh(postflight, dict(schema='sor-d5ai-fixture-postflight/1', action='postflight',
                               process_state=process_state, session=str(session), status='PARTIAL_POSTFLIGHT',
                               scope='OFFLINE FIXTURE; actual capture/STOP authentication only',
                               no_full_protection_audit=True, no_retail_approval=True,
                               identity_sha256=identity_hash, source_inventory=source_before))
        roots = dict(capture=dict(path=str(session), kind='raw-capture'),
                     companion=dict(path=str(companion), kind='private-receipt'))
        for name in ('roots.json','seal.json','create.json','verify.json','qualification.json','native-raw2-lifetime.zip'):
            archive.outside(out/name,roots)
        fresh(out / 'roots.json', roots)
        partial_reason = 'owned offline fixture, no retail episode'
        seal = archive.seal(roots, postflight, sha(postflight), partial_reason)
        if seal['status'] != 'PARTIAL' or seal['partial_reason'] != partial_reason:
            raise ValueError('Fixture seal cannot imply completed retail postflight')
        exact = {'capture/' + name: row for name, row in source_before.items()}
        exact.update({'companion/' + name: row for name, row in inventory(companion).items()})
        if exact != seal['files']:
            raise ValueError('Exact raw/companion inventory mismatch')
        required = {'capture/lifetimes.bin', 'capture/lifetimes-flush.jsonl',
                    'capture/geometry-1.bin', 'capture/geometry-2.bin', 'capture/events.bin', 'capture/STOP'}
        if not required.issubset(seal['files']):
            raise ValueError('New sidecars omitted from archive inventory')
        fresh(out / 'seal.json', seal)
        destination = out / 'native-raw2-lifetime.zip'
        created = archive.create(out / 'seal.json', sha(out / 'seal.json'), destination)
        fresh(out / 'create.json', created)
        verified = archive.verify(destination, seal, sha(destination))
        fresh(out / 'verify.json', verified)
        safeguards = []
        def refuses(name, action):
            try:
                action()
            except ValueError:
                safeguards.append(name)
            else:
                raise AssertionError('Archive safeguard accepted: ' + name)
        refuses('partial-reason-required', lambda: archive.seal(roots, postflight, sha(postflight)))
        refuses('output-inside-source', lambda: archive.outside(session / 'forbidden.zip', roots))
        refuses('companion-required', lambda: archive.seal(dict(capture=roots['capture']), postflight, sha(postflight), partial_reason))
        refuses('wrong-archive-pin', lambda: archive.verify(destination, seal, '0' * 64))
        refuses('unsafe-member-name', lambda: archive.safe_name('../geometry-1.bin'))
        refuses('casefold-duplicate', lambda: archive.validate_names(['capture/a', 'CAPTURE/A']))
        if inventory(session) != source_before or archive.collect(roots) != seal['files']:
            raise ValueError('Original or companion tree changed')
        if not all(sha(path) == digest for path, digest in deps.items()):
            raise ValueError('Module source changed during qualification')
        result = dict(schema='sor-d5ai-actual-archive/1', status='PASS', process_state=process_state,
                      scope='Actual offline fixture archive integrity; not a retail episode or full protection audit',
                      source_session=str(session), source_files=len(source_before), members=len(seal['files']),
                      roots_sha256=sha(out / 'roots.json'), seal_sha256=sha(out / 'seal.json'),
                      archive_sha256=sha(destination), create_sha256=sha(out / 'create.json'),
                      verify_sha256=sha(out / 'verify.json'), module_pins=deps, safeguards=safeguards,
                      original_tree='PRESERVED', archive='PRESERVED', final_free=guard())
        fresh(out / 'qualification.json', result)
        print(json.dumps({k: v for k, v in result.items() if k != 'module_pins'}))
    except BaseException as error:
        fresh(out / 'failure.json', dict(status='FAIL', error=repr(error), originals='PRESERVED'))
        raise


if __name__ == '__main__':
    main()
