# SPDX-License-Identifier: GPL-3.0-or-later
"""Create disposable synthetic stand-ins and execute frozen tests/measurements.

Writes only fresh ignored task directories and aggregate authored CSVs. Reads OS
journal, CPython/Git and free-space state. Uses a temporary read-deny ACL on one
new fixture and removes only that ACL in finally; never handles original saves.
No installation, target operation, policy change, staging, commit or network.
"""
import argparse
import csv
import ctypes
import hashlib
import json
import os
from pathlib import Path
import shutil
import statistics
import struct
import subprocess
import time
import zipfile

import journal
import prototype as p

ROOT = Path(__file__).resolve().parents[2]
LOCAL = ROOT / '.local-work/preservation-verification'
DOC = ROOT / 'docs/experiments/preservation-verification-optimization'


def write(path, value):
    with path.open('x', encoding='utf8', newline='\n') as f:
        json.dump(value, f, indent=2)
        f.write('\n')


def make(root, n=16, performance=False):
    root.mkdir(parents=True, exist_ok=False)
    (root / p.MARKER).write_text('Synthetic only\n', encoding='utf8')
    for kind in ('historical','scientific','critical','outputs'):
        (root / kind).mkdir()
    for i in range(n):
        size = (1024 if i % 64 < 48 else 16384 if i % 64 < 63 else 262144) if performance else 1024
        folder = root / 'historical' / f'{i % 16:02d}'
        folder.mkdir(exist_ok=True)
        (folder / f'{i:05d}.dat').write_bytes(bytes([i % 251]) * size)
    for i in range(16):
        (root / 'scientific' / f'input-{i:02d}.dat').write_bytes(bytes([i])*4096)
    for name in ('manual-save','quicksave','designated-save','backup-manual','backup-quick','backup-designated','installed-exe','installed-esm'):
        original = {'backup-manual':'manual-save','backup-quick':'quicksave','backup-designated':'designated-save'}.get(name,name)
        (root / 'critical' / (name + '.dat')).write_bytes(hashlib.sha256(original.encode()).digest()*8192)
    for backup,original in (('backup-manual','manual-save'),('backup-quick','quicksave'),('backup-designated','designated-save')):
        assert (root / 'critical' / (backup+'.dat')).read_bytes() == (root / 'critical' / (original+'.dat')).read_bytes()
    with zipfile.ZipFile(root / 'scientific/archive.zip','w') as archive:
        archive.writestr('synthetic.txt', 'synthetic archive integrity control')
    return p.baseline(root)


def mutate(root, case):
    leaf = next((root / 'historical').rglob('*.dat'))
    if case in ('alteration','same-size','timestamp-preserved'):
        stamp = leaf.stat()
        data = leaf.read_bytes()
        leaf.write_bytes(bytes([data[0] ^ 1]) + data[1:] + (b'x' if case == 'alteration' else b''))
        if case == 'timestamp-preserved':
            os.utime(leaf, ns=(stamp.st_atime_ns, stamp.st_mtime_ns))
            assert leaf.stat().st_mtime_ns == stamp.st_mtime_ns
    elif case == 'deletion':
        leaf.unlink()
    elif case == 'rename':
        leaf.rename(leaf.with_suffix('.renamed'))
    elif case == 'replacement':
        data = leaf.read_bytes()
        leaf.rename(leaf.with_suffix('.old'))
        leaf.write_bytes(data)
    elif case == 'unexpected-addition':
        (leaf.parent / 'unexpected.dat').write_bytes(b'unexpected')
    elif case == 'manifest-tamper':
        target = root / 'baseline.sqlite'
        data = bytearray(target.read_bytes())
        data[-10] ^= 1
        target.write_bytes(data)
    elif case == 'corrupt-receipt':
        (root / 'baseline.sqlite').write_bytes(b'not a sqlite receipt')
    elif case == 'truncated-archive':
        target = root / 'scientific/archive.zip'
        target.write_bytes(target.read_bytes()[:25])
    elif case == 'protected-original':
        (root / 'critical/manual-save.dat').write_bytes(b'bad')
    elif case == 'changed-exe':
        (root / 'critical/installed-exe.dat').write_bytes(b'bad')
    elif case == 'changed-esm':
        (root / 'critical/installed-esm.dat').write_bytes(b'bad')
    elif case == 'scientific-input':
        (root / 'scientific/input-00.dat').write_bytes(b'bad')
    elif case == 'benign-output':
        (root / 'outputs/authorized-new.md').write_text('New authorized output.\n', encoding='utf8')
    elif case == 'root-replacement':
        (root / 'historical').rename(root / 'historical-old')
        shutil.copytree(root / 'historical-old', root / 'historical')
    elif case == 'hardlink-alias-write':
        alias = root / 'outputs/alias.dat'
        os.link(leaf, alias)
        alias.write_bytes(b'z'*1024)
    elif case not in ('negative-control','wrong-baseline','io-error','permission-denial','interrupted-scan','journal-gap','journal-reset','truncated-journal'):
        raise ValueError(case)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--label', required=True)
    args = ap.parse_args()
    if not args.label.isalnum():
        raise ValueError('Alphanumeric fresh label required')
    out = LOCAL / args.label
    out.mkdir(parents=True, exist_ok=False)
    if min(shutil.disk_usage(d).free for d in ('C:/','D:/')) < 40_000_000_000:
        raise RuntimeError('Both-drive free-space guard')
    cases = ['negative-control','benign-output','alteration','same-size','timestamp-preserved',
        'deletion','rename','replacement','unexpected-addition','manifest-tamper','corrupt-receipt',
        'wrong-baseline','truncated-archive','protected-original','changed-exe','changed-esm','scientific-input',
        'root-replacement','hardlink-alias-write','io-error','permission-denial','interrupted-scan',
        'journal-gap','journal-reset','truncated-journal']
    freeze = dict(schema=1, frozen_before_performance=True, historical_files=4096,
        historical_sizes='48/64 at 1024 bytes, 15/64 at 16384, 1/64 at 262144',
        historical_payload_bytes=64*(48*1024+15*16384+262144), historical_directories=17,
        scientific_files=17, scientific_dat_bytes=65536, critical_files=8, critical_bytes=2097152,
        workflows=dict(W1='D5G-like inherited+union intake (two hash passes), fixed-list post (one); task/critical twice',
                       W2='Before/after full protected stand-ins, fresh scientific inputs, EXE/ESM, namespace and both-drive guards'),
        modes=dict(W1=['legacy','full','journal-conditional'],W2=['full','full']),
        trials=5, order='Alternating legacy/full/journal and reversed on odd trials; W2 paired full/full',
        metrics=['filesystem entries enumerated','logical pin visits','unique historical files read',
                 'payload hash invocations','payload bytes hashed','wall seconds','total verification wall'],
        costs='Include per-call SQLite byte load/digest/deserialize, journal query/read, all input hashes; setup separate and amortized',
        historical_timing='Internal historical operation timer; end-to-end includes critical/scientific and control plane',
        caches='No cache eviction; paired warm runs, fixture creation warms cache. No physical-device I/O claim',
        expected={c: ('ALLOW' if c in ('negative-control','benign-output') else 'DETECT') for c in cases},
        full_journal_fault_expectation='ALLOW: full mode has no journal dependency',
        method_hashes={name:hashlib.sha256((Path(__file__).parent/name).read_bytes()).hexdigest()
                       for name in ('journal.py','prototype.py','qualify.py')},
        threat='Current-byte silent corruption remains required for comparable AC4; conditional mode lacks it',
        setup='One baseline scans/hashes all synthetic leaves, captures file IDs and cursor, hashes baseline. Count cost separately')
    write(out / 'freeze.json', freeze)
    start = time.perf_counter()
    setup = make(out / 'performance',4096,True)
    setup['wall_seconds'] = time.perf_counter()-start
    write(out / 'setup.json', setup)
    measurements = []
    for trial in range(5):
        order = ['legacy','full','journal-conditional']
        if trial % 2:
            order.reverse()
        for mode in order:
            result = p.verify(out / 'performance', setup['anchor'], mode=mode)
            measurements.append(dict(workload='W1',trial=trial,**result))
        for arm in ('baseline','replacement'):
            guard_start = time.perf_counter()
            space_before = {d:shutil.disk_usage(d).free for d in ('C:/','D:/')}
            if min(space_before.values()) < 40_000_000_000:
                raise RuntimeError('W2 before guard')
            result = p.verify(out / 'performance',setup['anchor'], mode='full')
            space_after = {d:shutil.disk_usage(d).free for d in ('C:/','D:/')}
            if min(space_after.values()) < 40_000_000_000:
                raise RuntimeError('W2 after guard')
            result.update(wall_seconds=time.perf_counter()-guard_start,
                          free_before=space_before,free_after=space_after)
            measurements.append(dict(workload='W2',trial=trial,arm=arm,**result))
    write(out / 'measurements.json', measurements)
    sid = subprocess.check_output(['whoami','/user','/fo','csv','/nh'], text=True).strip().split(',')[-1].strip('"')
    tests = []
    for mode in ('full','journal-conditional'):
        for case in cases:
            root = out / 'cases' / (mode + '-' + case)
            setup_case = make(root)
            mutate(root,case)
            original_reader = journal.read_since
            acl = root / 'scientific/input-00.dat'
            acl_set = False
            try:
                anchor = '0'*64 if case == 'wrong-baseline' else setup_case['anchor']
                inject = None
                if case == 'permission-denial':
                    subprocess.run(['icacls',str(acl),'/deny','*'+sid+':(R)'], check=True, capture_output=True)
                    acl_set = True
                if case == 'io-error':
                    def inject(path):
                        raise OSError('Injected read I/O failure')
                if case in ('interrupted-scan','journal-gap','journal-reset','truncated-journal'):
                    def broken(volume, old, case=case):
                        if case == 'interrupted-scan':
                            raise InterruptedError('Injected scan interruption')
                        if case == 'truncated-journal':
                            journal.decode(b'bad')
                        now = dict(old)
                        if case == 'journal-gap':
                            now['first'] = old['next'] + 1
                        else:
                            now['id'] ^= 1
                        journal.validate_cursor(old,now)
                    journal.read_since = broken
                    if mode == 'full':
                        # Full mode does not depend on a journal at all.
                        expected = 'ALLOW'
                    else:
                        expected = 'DETECT'
                else:
                    expected = freeze['expected'][case]
                try:
                    p.verify(root,anchor,mode=mode,inject=inject)
                    observed, detail = 'ALLOW',''
                except (p.IntegrityError,journal.JournalError,OSError,ValueError,zipfile.BadZipFile) as exc:
                    observed, detail = 'DETECT',type(exc).__name__+': '+str(exc)
                tests.append(dict(mode=mode,case=case,expected=expected,observed=observed,
                                  passed=expected==observed,detail=detail))
            finally:
                journal.read_since = original_reader
                if acl_set:
                    subprocess.run(['icacls',str(acl),'/remove:d','*'+sid],check=True,capture_output=True)
    # Model counterexample only: no raw-volume mutation. Withhold mutation events
    # to model storage corruption below the filesystem journal, then compare oracles.
    counter = out / 'counterexample'
    cs = make(counter)
    mutate(counter,'timestamp-preserved')
    original_reader = journal.read_since
    try:
        journal.read_since = lambda volume, old: ([],0,old)
        conditional = p.verify(counter,cs['anchor'],mode='journal-conditional')
    finally:
        journal.read_since = original_reader
    try:
        p.verify(counter,cs['anchor'])
        full_detects = False
    except p.IntegrityError:
        full_detects = True
    write(out / 'counterexample.json', dict(model_only=True,actual_write_was_journaled=True,
        withheld_journal_events=True,conditional_allows=bool(conditional),full_detects=full_detects,
        conclusion='Unjournaled historical corruption is outside conditional coverage, unlike full hashing'))
    write(out / 'tests.json',tests)
    DOC.mkdir(parents=True,exist_ok=True)
    with (out / 'tests.csv').open('x',encoding='utf8',newline='') as f:
        writer = csv.writer(f,lineterminator='\n')
        writer.writerow(['mode','case','expected','observed','passed'])
        writer.writerows([r[k] for k in ('mode','case','expected','observed','passed')] for r in tests)
    with (out / 'measurements.csv').open('x',encoding='utf8',newline='') as f:
        fields = ['workload','trial','mode','arm','wall_seconds','historical_wall_seconds','cpu_seconds','control_bytes_hashed','journal_rows','journal_bytes',
                  'historical_enumerations','historical_logical_pin_visits','historical_unique_files','historical_hash_invocations','historical_bytes_hashed']
        writer = csv.DictWriter(f,fieldnames=fields,lineterminator='\n')
        writer.writeheader()
        for r in measurements:
            row = {k:r.get(k,'') for k in fields if not k.startswith('historical_') or k == 'historical_wall_seconds'}
            row.update({'historical_'+k:v for k,v in r['counts']['historical'].items() if 'historical_'+k in fields})
            writer.writerow(row)
    print(json.dumps(dict(tests=len(tests),failures=[r for r in tests if not r['passed']],setup=setup,
        medians={mode:statistics.median(r['wall_seconds'] for r in measurements if r['workload']=='W1' and r['mode']==mode)
                 for mode in ('legacy','full','journal-conditional')}),indent=2))


if __name__ == '__main__':
    main()
