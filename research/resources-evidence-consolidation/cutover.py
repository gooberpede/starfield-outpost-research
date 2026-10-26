# SPDX-License-Identifier: GPL-3.0-or-later
"""Exact proposal, routine verification and separately authorized execution.

Plan reads admitted sources, completed archive/restore receipts and Git identity;
writes inactive controls. Execute requires an external approval file and digest
after maintainer GO. It delegates exact retirement to the qualified transaction.
Never creates an approval for real inputs. No live, network or Git mutations.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
import time
import subprocess
from concurrent.futures import ThreadPoolExecutor

from prepare import ROOT, OUT, OWNER, a, e
import executor as x
DOC = ROOT / 'docs/experiments/resources-evidence-consolidation'
TRUST = DOC / 'selection-proposal.json'
ACTIVE = DOC / 'active-baseline.json'


def save(path, value):
    data = e.encode(value)
    e.space(len(data)*2 + 1024*1024)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    return e.pin(path)


def store():
    build = json.loads((OUT / 'build.json').read_text())
    index = json.loads((OUT / 'proposed-central-index.json').read_text())
    return a.Store(index['path'], index['sha256'], build['archive_sha256'], build['manifest_sha256'], OWNER)


def trusted_configuration(path=TRUST, expected_sha256=None):
    # This reviewed tracked proposal is the external trust root, like Cargo's
    # tracked active selection. It is never learned from candidate local receipts.
    config = (e.authenticate(path, expected_sha256) if expected_sha256 is not None
              else json.loads(Path(path).read_text(encoding='utf8')))
    if config.get('schema') != 'sor-resources-selection-proposal/1' or config.get('authority') != 'NOT AUTHORIZED':
        raise e.Error('Unsupported trusted preparation configuration')
    if hashlib.sha256(e.encode(config['selection'])).hexdigest() != config['selection_sha256']:
        raise e.Error('Reviewed selection content/digest mismatch')
    return config


def transaction(config=None):
    if config is None:
        controls = json.loads((OUT / 'controls.json').read_text())
        selected_store = store()
        source_root, folder = ROOT, OUT / 'real-transaction01'
    else:
        controls = e.authenticate(Path(config['controls']['path']), config['controls']['sha256'])
        roots = config['selection']
        selected_store = a.Store(roots['index']['path'], roots['index']['sha256'],
                                roots['archive_sha256'], roots['manifest_sha256'], OWNER)
        source_root, folder = Path(config['source_root']), Path(config['transaction'])
    return x.Transaction(source_root, selected_store, *sum(([Path(r['path']), r['sha256']] for r in controls['controls']), []),
                         folder, profile=controls['profile'])


def plan():
    st = store()
    namespace = json.loads((OUT / 'namespace.json').read_text())
    namespace_rows = {r['path']: r for r in namespace['rows']}
    admitted = json.loads((OUT / 'admission.json').read_text())['rows']
    membership = json.loads((OUT / 'members.json').read_text())
    originals = {r['path']: r for r in admitted}
    restore = json.loads((OUT / 'restore.json').read_text())
    if restore['files'] != len(membership):
        raise e.Error('Incomplete restoration receipt')
    # Identity recheck after full restoration; source bytes were verified under
    # locked handles during inclusion and are checked again in real preflight.
    def fingerprint(member):
        prior = originals[member['path']]
        p = e.canonical(ROOT / member['path'], ROOT)
        stat = p.stat()
        if stat.st_file_attributes & (0x200 | 0x800):
            raise e.Error('Sparse/compressed source requires separate allocation qualification')
        if (stat.st_ino != prior['file_id'] or stat.st_dev != prior['device'] or stat.st_size != member['bytes'] or
                stat.st_mtime_ns != namespace_rows[member['path']]['mtime_ns']):
            raise e.Error('Post-archive source identity changed')
        return dict(member, member=member['path'], file_id=stat.st_ino,
                         device=stat.st_dev, mtime_ns=stat.st_mtime_ns,
                         allocated_bytes=prior['allocated_bytes'], index_sha256=st.index_sha)
    with ThreadPoolExecutor(max_workers=8) as pool:
        rows = list(pool.map(fingerprint, membership, buffersize=64))
    held = [r for r in admitted if r['disposition'] != 'PROPOSED-ARCHIVE-ONLY']
    before = [{k: r[k] for k in ('path', 'bytes', 'sha256')} for r in admitted]
    shadow = a.migrate(before, [r['path'] for r in rows], st, x.digest(before))
    prefixes = ['.local-work/' + name + '/' for name in
                json.loads((OUT / 'intake.json').read_text())['system_directories']]
    empty = []
    for prefix in prefixes:
        for folder, dirs, files in os.walk(ROOT / prefix, followlinks=False):
            e.canonical(folder, ROOT)
            if not dirs and not files:
                empty.append(Path(folder).relative_to(ROOT).as_posix())
    excluded = [{k: r[k] for k in ('path', 'bytes', 'file_id', 'device', 'mtime_ns')}
                for r in namespace['exclusions']]
    profile = dict(owner=OWNER, prefixes=prefixes, holds=[r['path'] for r in held],
                   empty_directories=sorted(empty), excluded=excluded)
    proposal = dict(schema='sor-cargo-retirement/1', authority='DELETION NOT AUTHORIZED',
                    index_sha256=st.index_sha, archive_sha256=st.archive_sha, rows=rows)
    recovery = dict(state='RESTORED-TESTED', members=len(rows), index_sha256=st.index_sha,
                    archive_sha256=st.archive_sha, manifest_sha256=st.manifest_sha,
                    restoration_receipt_sha256=e.pin(OUT / 'restore.json'),
                    lease_sha256=restore['lease_sha256'])
    controls = []
    for filename, value in (('deletion-allowlist.json', proposal), ('recovery.json', recovery), ('shadow-baseline.json', shadow)):
        path = OUT / filename
        controls.append(dict(path=str(path), sha256=save(path, value), bytes=path.stat().st_size))
    save(OUT / 'controls.json', dict(controls=controls, profile=profile))
    tx = transaction()
    with tx.validated():
        pass
    save(OUT / 'execution-binding.json', dict(authority='NOT AUTHORIZED', binding=tx.binding,
          source_admission_sha256=e.pin(OUT / 'admission.json'),
          protected_exclusions_sha256=hashlib.sha256(e.encode(excluded)).hexdigest()))
    pins = json.loads((ROOT / '.local-work/resource-predictability-contrast/audit-before.json').read_text())['pins']
    normalize = lambda p: os.path.normcase(os.path.normpath(str(p)))
    names = {normalize(ROOT / r['path']) for r in rows}
    removed = {p: h for p, h in pins.items() if normalize(p) in names}
    kept = {p: h for p, h in pins.items() if normalize(p) not in names}
    save(OUT / 'historical-shadow.json', dict(state='PROPOSED-INACTIVE',
          before_sha256='a243c67c0e451aac21cbb5fcb671c9e94ad2b3806406d0fdec1b2626f153ab9b',
          before_count=len(pins), retired_pin_count=len(removed), surviving_pins=kept,
          after_loose_count=len(kept), replacement_payload_objects=2,
          actual_current_reduction=0, candidate_reduction=len(removed)-2))
    print(json.dumps(dict(allowlist_files=len(rows), held_files=len(held), protected_exclusions=len(excluded),
          historical_before=len(pins), proposed_loose_after=len(kept), proposed_payload_objects_after=len(kept)+2)), flush=True)


def expected_completion(tx, shadow, names):
    tail = '0' * 64
    wire = hashlib.sha256()
    ordinal = 0
    binding = x.digest(tx.binding)
    def event(kind, name=None):
        nonlocal tail, ordinal
        item = dict(binding=binding, ordinal=ordinal, previous=tail, event=kind, path=name)
        tail = x.digest(item)
        wire.update(json.dumps(dict(item, hash=tail), sort_keys=True).encode() + b'\n')
        ordinal += 1
    event('PREPARED')
    for name in names:
        event('INTENT', name)
        event('DONE', name)
    event('RETIRED_PENDING_BASELINE')
    baseline = dict(schema='sor-cargo-active/1', binding=tx.binding, before_sha256=shadow['before_sha256'],
                    rows=shadow['after'], retired=len(names), journal_prefix=tail)
    event('COMMITTED')
    return x.digest(baseline), wire.hexdigest()


def freeze():
    tx = transaction()
    plan, _, shadow = tx.read_controls()
    baseline, journal = expected_completion(tx, shadow, [r['path'] for r in plan['rows']])
    selection = dict(schema='sor-resources-active-selection/1', owner=OWNER, state='ACTIVE',
                     baseline_sha256=baseline, journal_sha256=journal,
                     index=dict(path=str(tx.store.index), sha256=tx.store.index_sha),
                     archive_sha256=tx.store.archive_sha, manifest_sha256=tx.store.manifest_sha,
                     controls_sha256=e.pin(OUT / 'controls.json'), retired_members=len(plan['rows']),
                     routine_command=[sys.executable, '-B', str(ROOT / 'research/resources-evidence-consolidation/resources_preservation.py')],
                     resource_only_command=[sys.executable, '-B', str(Path(__file__)), 'verify'])
    config = dict(schema='sor-resources-selection-proposal/1', authority='NOT AUTHORIZED',
                  source_root=str(tx.root), transaction=str(tx.folder),
                  controls=dict(path=str(OUT / 'controls.json'), sha256=e.pin(OUT / 'controls.json')),
                  selection=selection, selection_sha256=x.digest(selection), execution_binding_sha256=x.digest(tx.binding))
    save(OUT / 'execution-binding-final.json', dict(authority='NOT AUTHORIZED', binding=tx.binding,
         binding_sha256=x.digest(tx.binding), allowlist_sha256=tx.controls[0][1],
         controls_sha256=e.pin(OUT / 'controls.json')))
    save(TRUST, config)
    print(json.dumps(dict(trust=str(TRUST), trust_sha256=e.pin(TRUST),
          expected_baseline_sha256=baseline, expected_selection_sha256=x.digest(selection))), flush=True)


def verify_active_selection(path=ACTIVE, config=None, include_members=False):
    config = trusted_configuration() if config is None else config
    selection = e.authenticate(path, config['selection_sha256'])
    if selection != config['selection'] or selection.get('state') != 'ACTIVE' or selection.get('owner') != OWNER:
        raise e.Error('Inactive or wrong system selection')
    tx = transaction(config)
    result = tx.verify(selection['baseline_sha256'], include_members=include_members)
    if e.pin(tx.folder / 'journal.jsonl') != selection['journal_sha256']:
        raise e.Error('Committed journal differs from independently frozen expected bytes')
    return result, tx


def activate(config, tx, fault=lambda event: None, destination=ACTIVE):
    """Publish only the reviewed exact selection after the committed proof.

    A crash before publication leaves readers fail-closed. Repeating this phase
    under the same GO authenticates existing bytes and completes publication.
    """
    expected = config['selection']
    tx.verify(expected['baseline_sha256'])
    if e.pin(tx.folder / 'journal.jsonl') != expected['journal_sha256']:
        raise e.Error('Wrong committed journal before activation')
    target = e.canonical(destination)
    if target != ACTIVE and not target.is_relative_to(OUT):
        raise e.Error('Activation outside exact document or synthetic workspace')
    if target.exists():
        e.authenticate(target, config['selection_sha256'])
        return dict(state='ACTIVE', selection_sha256=config['selection_sha256'])
    target.parent.mkdir(parents=True, exist_ok=True)
    partial = target.with_suffix('.json.writing')
    if partial.exists():
        e.authenticate(partial, config['selection_sha256'])
    else:
        save(partial, expected)
    fault('selection-writing')
    if not e.K.MoveFileExW(str(partial), str(target), 8):
        raise e.c.WinError(e.c.get_last_error())
    fault('selection-published')
    e.authenticate(target, config['selection_sha256'])
    return dict(state='ACTIVE', selection_sha256=config['selection_sha256'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('phase', choices=('plan', 'freeze', 'execute', 'verify'))
    parser.add_argument('--approval', type=Path)
    parser.add_argument('--approval-sha256')
    parser.add_argument('--baseline-sha256')
    parser.add_argument('--configuration-sha256')
    args = parser.parse_args()
    if args.phase == 'plan':
        plan()
    elif args.phase == 'freeze':
        freeze()
    elif args.phase == 'execute':
        if not args.approval or not args.approval_sha256 or not args.configuration_sha256:
            parser.error('Separate maintainer GO, exact approval digest and reviewed configuration digest are required')
        config = trusted_configuration(expected_sha256=args.configuration_sha256)
        tx = transaction(config)
        if x.digest(tx.binding) != config['execution_binding_sha256']:
            raise e.Error('Reviewed execution binding changed')
        tx.approval(args.approval, args.approval_sha256)
        committed = False
        if (tx.folder / 'baseline.json').exists():
            log = x.Journal(tx.folder / 'journal.jsonl', tx.binding, boundary=tx.boundary)
            try:
                committed = log.state == 'COMMITTED'
            finally:
                log.close()
        result = (tx.verify(config['selection']['baseline_sha256']) if committed else
                  tx.execute(args.approval, args.approval_sha256))
        activation = activate(config, tx)
        receipt = OUT / 'execution-result.json'
        if not receipt.exists():
            save(receipt, dict(transaction=result, activation=activation))
        print(json.dumps(dict(transaction=result, activation=activation)), flush=True)
    else:
        result, _ = verify_active_selection()
        print(json.dumps(result), flush=True)
