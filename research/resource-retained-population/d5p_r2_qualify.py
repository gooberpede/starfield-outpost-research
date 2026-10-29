# SPDX-License-Identifier: GPL-3.0-or-later
"""Qualify unchanged R1 DLL and R2 decoder in fresh ignored offline scratch.

Reads installed pins, previous primary receipts, owned sources and the R1 DLL.
Runs only MSVC and disposable native hosts. Writes a new .local-work/d5p-r2
child, logs, a standalone context executable, and task-owned damaged derivatives.
No game, deployment, protected-save copy/mutation, downloads or Git writes.
CPython stdlib and the already installed MSVC/SDK are prerequisites.
"""
import csv
import hashlib
import json
from pathlib import Path
import re
import shutil
import struct
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from d5p_r2_diagnostics import ROOT, DLL, PROFILE, capture, diagnose, ORDER, READS
from build import sha, guard, VC, pe_read, SITES
from read_capture import inspect, decode, SIZE_V2

R1 = ROOT / '.local-work/d5p/r1-build04'


def write(path, value):
    with path.open('x', encoding='utf8', newline='\n') as f:
        json.dump(value, f, indent=2)
        f.write('\n')


def git(*args):
    return subprocess.check_output(['git', '--no-optional-locks', *args], cwd=ROOT).decode().strip()


def main():
    label = sys.argv[1]
    assert re.fullmatch('[a-z0-9-]+', label)
    out = ROOT / '.local-work/d5p-r2' / label
    out.mkdir(parents=True, exist_ok=False)
    build = json.loads((R1 / 'build.json').read_text())
    sources = {p: sha(p) for p in build['sources']}
    assert sources == build['sources']
    assert sha(R1 / 'SorRetainedPopulation.dll') == DLL == build['dll_sha256']
    initial = dict(utc=datetime.now(timezone.utc).isoformat(), head=git('rev-parse', 'HEAD'),
                   branch=git('branch', '--show-current'), index=sha(ROOT / '.git/index'),
                   status=git('status', '--short'), free=guard(), sources=sources)
    write(out / 'initial.json', initial)
    installed = {p: sha(p) for p in build['installed']}
    assert installed == build['installed']
    game = next(Path(p) for p in installed if p.endswith('Starfield.exe'))
    data = game.read_bytes()
    assert all(sha_bytes(pe_read(data, r['rva'], 32)) == r['sha256'] for r in build['sites'])
    del data
    evidence = []
    for ledger in ('d5p-phase-b-sources.csv', 'd5p-r1-sources.csv'):
        for row in csv.DictReader((ROOT / 'docs/experiments/resource-retained-population' / ledger).open(encoding='utf8')):
            if row['path'].startswith('.local-work/'):
                p = ROOT / row['path']
                assert sha(p) == row['sha256'], str(p)
                evidence.append(dict(path=row['path'], sha256=row['sha256']))
    write(out / 'original-evidence.json', evidence)
    # Primary chronology: no event timestamp is fabricated from file mtime.
    live = ROOT / '.local-work/d5p/live/session-3424-98377281'
    raw = (live / 'events.bin').read_bytes()
    events = [decode(raw[i + 16:i + 16 + 1416]) for i in range(0, len(raw), 1432)]
    demands = [e['sequence'] for e in events if e['kind'] == 1]
    chronology = dict(first_invalid_demand=demands[0], last_invalid_demand=demands[-1],
                      count=len(demands), prefix_ready_records=1,
                      terminal=json.loads((live / 'terminal.json').read_text()),
                      files={str(p.relative_to(ROOT)): dict(sha256=sha(p), mtime_ns=p.stat().st_mtime_ns,
                             ctime_ns=p.stat().st_ctime_ns) for p in
                             (live / 'ready.json', live / 'terminal.json',
                              ROOT / '.local-work/d5p-phase-b/arrival-health.json',
                              ROOT / '.local-work/d5p-phase-b/preload-light-guards.json')},
                      limit='No per-event clock or intermediate load/travel milestone ACK; cannot shorten original itinerary')
    assert all(e['status'] & 1 for e in events if e['kind'] == 1)
    write(out / 'chronology.json', chronology)
    host, dll = R1 / 'sor-d5p-fixture.exe', R1 / 'SorRetainedPopulation.dll'
    cases = ('normal', 'context-reasons', 'nested', 'concurrent', 'aba', 'reset',
             'loss-one', 'loss-many', 'retry-one', 'retry-many', 'loss-cross',
             'loss-fence', 'loss-rebuild', 'in-flight-loss', 'hook-stress', 'stress',
             'hook-timing', 'hook-bounds', 'crash-before', 'crash-after',
             'late-disk-fault', 'late-write-fault', 'late-flush-fault', 'late-ack-fault',
             'late-ack-write-fault', 'worker-stop', 'worker-guard')
    def run_case(name):
        guard()
        r = subprocess.run([str(host), str(dll), str(out / name), name], capture_output=True)
        (out / (name + '.log')).write_bytes(r.stdout + r.stderr)
        assert r.returncode == {'crash-before': 71, 'crash-after': 72}.get(name, 0), (name, r.returncode)
        result = inspect(out / name, DLL)
        positive = name in ('normal', 'nested', 'concurrent', 'loss-one', 'loss-many',
                            'retry-one', 'retry-many', 'loss-rebuild', 'hook-stress',
                            'stress', 'hook-timing', 'hook-bounds', 'crash-after', 'worker-stop') or name.startswith('late-')
        assert bool(result['complete_chains']) == positive, name
        if name in ('loss-one', 'retry-one', 'loss-many', 'retry-many'):
            assert result['known_ordinary_drops'] == (1 if name.endswith('one') else 37)
            assert result['loss_diagnostics']['failed'] is False
        if name in ('loss-cross', 'loss-fence', 'in-flight-loss'):
            assert not result['complete_chains']
        if name.startswith('late-'):
            assert result['loss_diagnostics']['failed'] and result['independently_verified_durable_records'] >= 9
        return name, result
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = dict(pool.map(run_case, cases))
    write(out / 'unchanged-native.json', results)
    diagnostic = capture(out / 'context-reasons')
    assert {d.get('reason') for d in diagnostic['diagnostics']} == {0, 5, 7, 8, 12, 14, 15, 16, 19, 21, 22, 23, 24, 26}
    assert diagnostic['authentication']['independently_verified_durable_records'] == 16
    assert sum(d['result'] == 'UNRESOLVED_NONCOMPOSITE_CONTEXT' for d in diagnostic['diagnostics']) == 1
    write(out / 'unchanged-diagnostics.json', diagnostic)
    # Compile a separate host against unchanged observer.h. This is not a new DLL.
    src = Path(__file__).with_name('d5p-r2-context.cpp')
    command = out / 'compile.cmd'
    command.write_text('@echo off\ncall "' + str(VC) + '"\nif errorlevel 1 exit /b 1\n' +
                       f'cl /Bv /nologo /std:c++20 /EHsc /W4 /O2 /MD "{src}" /Fe:context.exe /link /Brepro /INCREMENTAL:NO\n',
                       encoding='utf8', newline='\r\n')
    r = subprocess.run(['cmd', '/d', '/c', str(command)], cwd=out, capture_output=True)
    (out / 'compile.log').write_bytes(r.stdout + r.stderr)
    assert r.returncode == 0, r.stdout.decode(errors='replace')
    r = subprocess.run([str(out / 'context.exe'), str(out / 'context.bin')], capture_output=True)
    assert r.returncode == 0, ('context native oracle', r.returncode)
    stats = json.loads((out / 'context.bin.json').read_text())
    raw = (out / 'context.bin').read_bytes()
    records = [decode(raw[i:i + SIZE_V2]) for i in range(0, len(raw), SIZE_V2)]
    expected = [0, 1, 2, 3, 4, 5, 6, 7, 8, 11, 12, 14, 15, 16, 17, 18, 20, 19, 24, 21, 22, 26, 23, 23, 0]
    assert [e['reason'] for e in records] == expected
    decoded = [diagnose(e, stats['image_base']) for e in records]
    for e, d in zip(records, decoded):
        if d['result'].startswith('UNRESOLVED_'):
            assert e['reason'] == 2 and not e['frame']
            continue
        passed = ORDER if not e['reason'] else ORDER[:ORDER.index(e['reason'])]
        for reason, (field, _) in READS.items():
            assert (d['fields'][field]['validity'] == 'READ_VALID') == (reason in passed)
        if e['reason'] in READS:
            assert d['fields'][READS[e['reason']][0]]['value'] is None
    assert decoded[22]['subcause'] == decoded[23]['subcause']
    write(out / 'context-oracle.json', dict(stats=stats, expected=expected, decoded=decoded,
          composite_not_executed=[9, 10, 13, 25], primitive_only_reasons=[9, 10, 13, 25],
          limits='No exact retail failure reproduction; lifetime final-state subcauses remain unresolved'))
    # Damage copies retain originals. Only acknowledged intact prefix diagnostics count.
    damage = out / 'damage'
    damage.mkdir()
    controls = {}
    for name in ('torn-tail', 'corrupt-first', 'torn-ack', 'wrong-dll'):
        target = damage / 'context-reasons'
        target.mkdir()
        for n in ('events.bin', 'identity.json', 'flush.jsonl'):
            shutil.copyfile(out / 'context-reasons' / n, target / n)
        if name == 'torn-tail':
            with (target / 'events.bin').open('ab') as f:
                f.write(b'abc')
        if name == 'corrupt-first':
            b = bytearray((target / 'events.bin').read_bytes())
            b[100] ^= 1
            (target / 'events.bin').write_bytes(b)
        if name == 'torn-ack':
            p = target / 'flush.jsonl'
            p.write_bytes(p.read_bytes()[:-2])
        if name == 'wrong-dll':
            p = target / 'identity.json'
            p.write_text(p.read_text().replace(DLL, '0' * 64), encoding='utf8')
        try:
            d = capture(target)
            assert d['authentication']['errors']
            assert len(d['diagnostics']) == (16 if name == 'torn-tail' else 0)
            controls[name] = dict(diagnostics=len(d['diagnostics']), authentication=d['authentication']['record_authentication'])
        except ValueError:
            assert name == 'wrong-dll'
            controls[name] = 'REFUSED'
        # All removals are confined to this newly created scratch child.
        assert target.resolve().is_relative_to(out.resolve())
        shutil.rmtree(target)
    write(out / 'damage-oracle.json', controls)
    timings = {name: json.loads((out / name / 'timing.json').read_text()) for name in ('hook-timing', 'hook-bounds')}
    assert {p: sha(p) for p in build['sources']} == sources
    assert {p: sha(p) for p in build['installed']} == installed
    assert sha(dll) == DLL
    assert git('rev-parse', 'HEAD') == initial['head'] and sha(ROOT / '.git/index') == initial['index']
    write(out / 'qualification.json', dict(disposition='OFFLINE_CONTROLS_PASS', profile=PROFILE, dll_sha256=DLL,
          cases=len(cases), timings=timings, initial=initial, final_free=guard(), installed=installed,
          native_sources={str(src.relative_to(ROOT)): sha(src), 'runtime/retained-population/observer.h': sha(ROOT / 'runtime/retained-population/observer.h')},
          receipts={str(p.relative_to(out)): sha(p) for p in out.rglob('*') if p.is_file()}))
    print(json.dumps(dict(out=str(out), cases=len(cases), context_records=len(records), timings=timings)))


def sha_bytes(data):
    return hashlib.sha256(data).hexdigest()


if __name__ == '__main__':
    main()
