# SPDX-License-Identifier: GPL-3.0-or-later
"""Read-only Cargo census, real restore, consumer replay and retirement proposal.

Reads exact Stage B source/index/archive and authored consumer text. Writes a
fresh ignored receipt tree and disposable restored bytes; no original deletion,
save decoding, installed-content mutation, native execution or policy activation.
Requires installed CPython 3.14, Git, Windows NTFS and owned Stage A/B utilities.
"""
import argparse
import ast
from collections import Counter
import ctypes as c
import datetime
import hashlib
import json
import msvcrt
import os
from pathlib import Path
import struct
import subprocess
import sys
import time

import access as a
import retirement

ALLOCATION_UNITS = {}


def clusters(path, cost=False):
    """Conservative data-allocation projection; resident/MFT recovery counts zero.

    Retrieval pointers are preferred. If this filesystem rejects that read API,
    charge nonresident cluster-aligned FileStandardInfo allocation only for
    streams larger than one cluster. Costs always round upward, never downward.
    """
    kernel = a.e.K
    kernel.DeviceIoControl.argtypes = [a.e.w.HANDLE, a.e.w.DWORD, c.c_void_p,
                                      a.e.w.DWORD, c.c_void_p, a.e.w.DWORD,
                                      c.POINTER(a.e.w.DWORD), c.c_void_p]
    kernel.DeviceIoControl.restype = a.e.w.BOOL
    sectors, per_sector, free, total = (a.e.w.DWORD() for _ in range(4))
    if not kernel.GetDiskFreeSpaceW(str(Path(path).anchor), c.byref(sectors), c.byref(per_sector), c.byref(free), c.byref(total)):
        raise c.WinError(c.get_last_error())
    unit = sectors.value * per_sector.value
    ALLOCATION_UNITS[str(Path(path).anchor)] = unit
    start = c.c_longlong(0)
    buf = c.create_string_buffer(1024 * 1024)
    count = a.e.w.DWORD()
    with a.e.locked(path) as (stream, info):
        ok = kernel.DeviceIoControl(msvcrt.get_osfhandle(stream.fileno()), 0x90073,
                                    c.byref(start), 8, buf, len(buf), c.byref(count), None)
        if not ok:
            error = c.get_last_error()
            if error == 38:  # Resident or empty stream: no nonresident data runs.
                return ((info.length + unit - 1) // unit) * unit if cost else 0
            if error == 50:
                if cost:
                    return max(info.allocation, ((info.length + unit - 1) // unit) * unit)
                attrs = Path(path).stat().st_file_attributes
                if attrs & (0x200 | 0x800 | 0x400 | 0x4000):
                    raise a.Error('Sparse/compressed/reparse allocation requires extent qualification')
                return info.allocation if info.length > unit and info.allocation % unit == 0 else 0
            raise c.WinError(error)
        extents, vcn = struct.unpack_from('<I4xq', buf.raw)
        if count.value != 16 + extents * 16:
            raise a.Error('Unqualified NTFS extent result')
        allocated = 0
        for i in range(extents):
            next_vcn, lcn = struct.unpack_from('<qq', buf.raw, 16 + i * 16)
            if next_vcn < vcn or lcn < -1:
                raise a.Error('Unsupported allocation extent')
            if lcn >= 0:
                allocated += (next_vcn - vcn) * unit
            vcn = next_vcn
        return allocated


def scan(rows):
    """Keep literal citations separate from executable read-site candidates."""
    paths = subprocess.check_output(['git', 'ls-files', '-z'], cwd=a.ROOT).decode().split('\0')[:-1]
    roots = sorted({r['path'].split('/')[1] for r in rows})
    refs = []
    scripts = []
    for name in paths:
        p = a.ROOT / name
        if p.suffix not in ('.py', '.md', '.json', '.csv', '.ps1', '.java'):
            continue
        try:
            text = p.read_text(encoding='utf8')
        except UnicodeError:
            continue
        hits = [dict(line=i, text=line) for i, line in enumerate(text.splitlines(), 1)
                if any(root in line for root in roots)]
        if not hits:
            continue
        kind = ('archive preparation, not a scientific consumer' if 'evidence-archive' in name
                else 'executable path candidate' if p.suffix == '.py' else 'historical citation or navigation')
        refs.append(dict(path=name, sha256=a.e.pin(p), kind=kind, hits=hits))
        if p.suffix == '.py':
            tree = ast.parse(text)
            reads = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr in (
                        'read_text', 'read_bytes', 'open', 'glob', 'rglob'):
                    reads.append(dict(line=node.lineno, expression=ast.get_source_segment(text, node)))
            scripts.append(dict(path=name, sha256=a.e.pin(p), read_sites=reads,
                                disposition='Explicit restored payload workflow' if name in (
                                    'research/c1-cargo/menu_abc.py', 'research/c2-transport/pex.py')
                                else 'Closed acquisition/admission/export method; deliberate restoration and original prerequisites required'))
    return refs, scripts


def main(label):
    if not label.isalnum():
        raise a.Error('Alphanumeric fresh run label required')
    folder = a.LOCAL / label
    if folder.exists():
        raise a.Error('Fresh output required')
    free_before = a.e.space(256 * 1024 * 1024)
    baseline = json.loads((a.LOCAL/'baseline.json').read_text())
    assert subprocess.check_output(['git','rev-parse','HEAD'], cwd=a.ROOT).decode().strip() == baseline['head']
    assert a.e.pin(a.ROOT/'.git/index') == baseline['index_sha256']
    folder.mkdir()
    method_paths = [*sorted(Path(__file__).parent.glob('*.py')),
                    a.ROOT/'research/c1-cargo/menu_abc.py', a.ROOT/'research/c2-transport/pex.py',
                    a.ROOT/'research/evidence-archive-stage-b/engine.py',
                    a.ROOT/'research/evidence-archive-discovery/archive.py']
    method_pins = {str(p): a.e.pin(p) for p in method_paths}
    executed = folder/'executed-methods'
    for p in method_paths:
        target = executed/p.relative_to(a.ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open('xb') as stream:
            stream.write(p.read_bytes())
    a.write(folder/'executed-methods.json', method_pins)
    store = a.Store()
    deep = store.verify()
    with store.authenticated() as (entry, archive, members):
        rows = entry['rows']
        archive_path = archive
    frozen = json.loads((a.e.LOCAL/'freeze02.json').read_text())
    retained = json.loads((a.e.LOCAL/'retain-loose02.json').read_text())['rows']
    old_allow = json.loads((a.e.LOCAL/'deletion-manifest02.json').read_text())['rows']
    assert len(rows) == 1051 and len(frozen) == 1054 and len(retained) == 1017 and len(old_allow) == 37
    assert {r['path'] for r in old_allow}.isdisjoint({r['path'] for r in retained})
    assert {r['path'] for r in frozen} == {r['path'] for r in retained + old_allow}
    start = time.perf_counter()
    before = a.e.inspect(a.ROOT, frozen)
    source_seconds = time.perf_counter() - start
    refs, consumers = scan(rows)
    a.write(folder/'references.json', refs)
    a.write(folder/'consumers.json', consumers)
    ledger = []
    for row in rows:
        p = a.ROOT / row['path']
        suffix = p.suffix.lower()
        role = ('closed experiment method; restoration never executes it' if suffix in ('.py', '.ps1', '.java', '.bat')
                else 'historical report/log/path reference' if suffix in ('.md', '.log', '.txt', '.diff', '.request')
                else 'closed experiment input/output; exact bytes restored on scientific use')
        stat = p.stat()
        ledger.append(dict(path=row['path'], sha256=row['sha256'], bytes=row['bytes'],
                           member=row['path'], owner='cargo-transport-fuel', index_sha256=a.INDEX_SHA,
                           prior='PROPOSED-37' if row['path'] in {r['path'] for r in old_allow} else 'RETAINED-1014',
                           actual_role=role, disposition='PROPOSED-ARCHIVE-ONLY',
                           consumer_refs=[x['path'] for x in refs if row['path'] in '\n'.join(h['text'] for h in x['hits'])],
                           namespace_consumers=[x['path'] for x in consumers if p.parts[-2] in x['path'] or row['path'].split('/')[1] in x['path']],
                           file_id=stat.st_ino, device=stat.st_dev, mtime_ns=stat.st_mtime_ns,
                           data_cluster_bytes=clusters(p)))
    a.write(folder/'dependency-ledger.json', ledger)
    holds = [r for r in frozen if r['path'] not in {x['path'] for x in rows}]
    assert len(holds) == 3 and all(r['historical_version_hold'] for r in holds)
    a.write(folder/'holds.json', dict(rows=holds, reason='Unarchived packager version discrepancy; retained unchanged'))
    restore_start = time.perf_counter()
    restored = store.restore(folder/'restored')
    restore_seconds = time.perf_counter() - restore_start
    a.lease_rows(folder/'restored', restored['lease_sha256'])
    a.write(folder/'recovery.json', dict(state='RESTORED-TESTED', index_sha256=a.INDEX_SHA,
                                       archive_sha256=a.ARCHIVE_SHA, manifest_sha256=a.MANIFEST_SHA,
                                       members=len(rows), restore=restored, seconds=restore_seconds))
    trials = []
    for script, experiment, expected_file in (
            ('research/c1-cargo/menu_abc.py','c1-cargo','menuabc03.json'),
            ('research/c2-transport/pex.py','c2-transport','pex01.json')):
        output = folder/(experiment+'-output')
        cmd = [sys.executable,'-B',script,'--run','replay','--evidence-lease',restored['destination'],
               '--lease-sha256',restored['lease_sha256'],'--output-directory',str(output)]
        result = subprocess.run(cmd, cwd=a.ROOT, capture_output=True, text=True)
        actual = json.loads((output/'replay.json').read_text()) if result.returncode == 0 else None
        expected_path = folder/'restored/.local-work'/experiment/expected_file
        expected = json.loads(expected_path.read_text())
        equal = actual == expected
        trials.append(dict(script=script, command=cmd, returncode=result.returncode, stdout=result.stdout,
                           stderr=result.stderr, equal_historical_output=equal,
                           historical_input_sha256=a.e.pin(expected_path), output_sha256=a.e.pin(output/'replay.json') if actual else None))
        if result.returncode or not equal:
            a.write(folder/'consumer-failure.json', trials)
            raise a.Error('Consumer reproduction failed; preserve trial')
    a.write(folder/'consumer-reproduction.json', trials)
    # Preserve historical failures without rerunning old admission against new HEAD.
    stale = []
    for experiment in ('c1-cargo','c2-transit','c2-transport','c3-fuel'):
        p = folder/'restored/.local-work'/experiment/'baseline.json'
        b = json.loads(p.read_text())
        stale.append(dict(experiment=experiment, baseline_sha256=a.e.pin(p), original_head=b['head'],
                          current_head=baseline['head'], original_index_sha256=b['index']['sha256'],
                          current_index_sha256=baseline['index_sha256'],
                          outcome='Original admission predicates FAIL by identity; no gate skipped or baseline rewritten'))
    a.write(folder/'historical-admission-failures.json', stale)
    plan_rows = [dict(path=r['path'], sha256=r['sha256'], bytes=r['bytes'], member=r['member'], owner=r['owner'],
                      index_sha256=a.INDEX_SHA, file_id=r['file_id'], device=r['device'],
                      disposition=r['disposition']) for r in ledger]
    plan = dict(schema='sor-cargo-retirement/1', authority='DELETION NOT AUTHORIZED',
                index_sha256=a.INDEX_SHA, archive_sha256=a.ARCHIVE_SHA, rows=plan_rows)
    a.write(folder/'deletion-allowlist.json', plan)
    plan_sha = a.e.pin(folder/'deletion-allowlist.json')
    recovery_sha = a.e.pin(folder/'recovery.json')
    prepared = retirement.prepare(store, a.ROOT, folder/'deletion-allowlist.json', plan_sha,
                                 folder/'recovery.json', recovery_sha)
    a.write(folder/'preparation.json', prepared)
    prior = [dict(path=r['path'], bytes=r['bytes'], sha256=r['sha256']) for r in frozen]
    prior_sha = hashlib.sha256(a.e.encode(prior)).hexdigest()
    shadow = a.migrate(prior, [r['path'] for r in rows], store, prior_sha)
    assert a.rollback(shadow, prior_sha) == prior
    # Small Cargo slice only; the old full baseline remains separately bound unchanged.
    a.write(folder/'shadow-baseline.json', shadow)
    global_path = a.ROOT/'.local-work/resource-predictability-contrast/audit-after.json'
    global_pins = json.loads(global_path.read_text())['pins']
    keys = {os.path.normcase(os.path.normpath(n)) for n in global_pins}
    overlap = sum(os.path.normcase(os.path.normpath(str(a.ROOT/r['path']))) in keys for r in rows)
    a.write(folder/'global-baseline-binding.json', dict(path=str(global_path), sha256=a.e.pin(global_path),
            rows=len(global_pins), cargo_overlap=overlap, unchanged=True,
            scope='Cargo shadow replaces Stage B 1054-source boundary, not a claim of savings in the 93334-pin baseline'))
    routine_start = time.perf_counter()
    routine = store.verify(False)
    a.e.inspect(a.ROOT, holds)
    routine['with_three_unarchived_holds_seconds'] = time.perf_counter() - routine_start
    routine['with_holds_objects'] = 5
    routine['with_holds_bytes'] = routine['routine_bytes'] + sum(r['bytes'] for r in holds)
    a.write(folder/'routine-verification.json', routine)
    after = a.e.inspect(a.ROOT, frozen)
    assert before == after
    assert subprocess.check_output(['git','rev-parse','HEAD'], cwd=a.ROOT).decode().strip() == baseline['head']
    assert a.e.pin(a.ROOT/'.git/index') == baseline['index_sha256']
    assert method_pins == {str(p): a.e.pin(p) for p in method_paths}, 'Executed method changed during run'
    a.write(folder/'source-preservation.json', dict(files=1054, unchanged=True,
            before_sha256=hashlib.sha256(a.e.encode(before)).hexdigest(), after_sha256=hashlib.sha256(a.e.encode(after)).hexdigest()))
    # Count only future permanent control artifacts, charge full archive/index cost.
    persistent = sorted(folder.glob('*.json')) + sorted(folder.glob('*-output/*.json')) + sorted(executed.rglob('*.py'))
    costs = [dict(path=str(p), logical_bytes=p.stat().st_size, data_cluster_bytes=clusters(p, cost=True))
             for p in [archive_path, a.INDEX, *persistent]]
    # Reserve covers final measurements/source ledger, final review/seal controls,
    # authored source/docs growth and a future write-ahead journal. It is a cost,
    # not claimed free recovery; final delivery independently checks the bound.
    journal_reserve = 2 * 1024 * 1024
    gross = sum(r['data_cluster_bytes'] for r in ledger)
    net = gross - sum(r['data_cluster_bytes'] for r in costs) - journal_reserve
    a.write(folder/'measurements.json', dict(time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            before_free=free_before, after_free=a.e.space(), archived=1051, proposed=1051, held_unarchived=3,
            source_logical_bytes=sum(r['bytes'] for r in rows), data_cluster_gross=gross,
            persistent_costs=costs, journal_control_reserve=journal_reserve, projected_net_data_cluster_bytes=net,
            cluster_bytes=ALLOCATION_UNITS,
            allocation_method='Retrieval-pointer API unsupported (WinError50). Conservative FileStandardInfo cluster-aligned allocations for uncompressed nonsparse streams larger than one cluster; others zero. Persistent costs round upward; no MFT/directory recovery.',
            before_historical_files=1054, proposed_after_historical_files=3,
            source_seconds=source_seconds, source_hash_calls=1054, source_hash_bytes=sum(r['bytes'] for r in frozen),
            routine=routine, shadow_before=len(prior), shadow_after=len(shadow['after']),
            allowlist_sha256=plan_sha, recovery_sha256=recovery_sha, actual_deleted=0,
            temporary='Full restored tree and disposable synthetic fixtures retained for review, with explicit lease cleanup. Replay outputs and all existing real-run receipts are charged as persistent; no lasting replica planned. Review patch exports are temporary audit costs.'))
    if net <= 0:
        raise a.Error('AC6 net-positive physical-data projection failed')
    a.write(folder/'sources.json', [dict(path=str(p), sha256=a.e.pin(p), bytes=p.stat().st_size) for p in (
        a.INDEX, archive_path, a.e.LOCAL/'freeze02.json', a.e.LOCAL/'retain-loose02.json',
        a.e.LOCAL/'deletion-manifest02.json', a.e.LOCAL/'version-holds02.json',
        a.ROOT/'research/evidence-archive-stage-b/engine.py', a.ROOT/'research/evidence-archive-discovery/archive.py',
        a.ROOT/'research/review_package.py', Path(sys.executable),
        *sorted(Path(__file__).parent.glob('*.py')))])
    print(json.dumps(dict(folder=str(folder), allowlist_sha256=plan_sha,
                          projected_net_data_cluster_bytes=net, consumers_equal=True), indent=2))


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--label', required=True)
    main(ap.parse_args().label)
