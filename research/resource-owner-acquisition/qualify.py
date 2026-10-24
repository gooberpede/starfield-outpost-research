# SPDX-License-Identifier: GPL-3.0-or-later
"""Run only pinned disposable Windows fixtures and persist SRO1 receipts.

Reads build/source pins; creates fresh ignored capture/test outputs. Uses owned
transport and independent inherited framing verifier. No retail, save, network,
configuration, analysis database or Git effects. Python stdlib and built MSVC
targets are prerequisites. Negative cases preserve their original failures.
"""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import importlib.util

from build import ROOT, LOCAL, pin

sys.path.insert(0, str(ROOT / 'research/resource-oracle-retail'))
from collect import persist
sys.path.insert(0, str(ROOT / 'research/resource-tungsten-acquisition'))
import importlib.util
spec = importlib.util.spec_from_file_location('d4a_qualifier', ROOT / 'research/resource-tungsten-acquisition/qualify.py')
d4a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(d4a)
independent = d4a.independent
comparison_spec = importlib.util.spec_from_file_location('d4d_comparison', Path(__file__).with_name('compare.py'))
comparison = importlib.util.module_from_spec(comparison_spec)
comparison_spec.loader.exec_module(comparison)
admission_spec = importlib.util.spec_from_file_location('d4d_admission', Path(__file__).with_name('admission.py'))
admission = importlib.util.module_from_spec(admission_spec)
admission_spec.loader.exec_module(admission)


def write(path, value):
    with path.open('x', encoding='utf8', newline='\n') as stream:
        json.dump(value, stream, indent=2)
        stream.write('\n')


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--build', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--modes', nargs='+', default=['map-direct', 'map-exchange', 'map-order',
        'map-null', 'map-duplicate-root', 'map-empty', 'map-malformed', 'map-corrupt',
        'map-nested', 'map-source-reuse', 'map-wrapper-reuse', 'map-unrelated',
        'map-cache', 'map-incomplete', 'map-crash-before', 'map-crash-after',
        'map-wrong-owner', 'map-wrong-type', 'map-out-of-range',
        'map-bound', 'map-bound-wrong-source', 'map-bound-wrong-workshop', 'map-threads', 'map-concurrent', 'map-bypass'])
    a = ap.parse_args()
    build, out = a.build.resolve(), a.output.resolve()
    assert build.is_relative_to(LOCAL) and out.is_relative_to(LOCAL)
    manifest = json.loads((build / 'build.json').read_text())
    assert manifest['exit_code'] == 0
    for p, h in manifest['files'].items():
        assert pin(p) == h, p
    out.mkdir(exist_ok=False)
    results = []
    for mode in a.modes:
        folder = out / mode
        folder.mkdir()
        rows, session, tracker, useful = [], None, admission.Tracker(), []
        command = [str(build / 'sor-d4d-fixture-controller.exe'), '--synthetic-fixture',
                   pin(build / 'sor-d4d-fixture.exe'), mode]
        p = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, text=True)
        for line in p.stdout:
            row = json.loads(line)
            row['synthetic'] = True
            rows.append(row)
            if row['kind'] == 'SESSION':
                session = row
            if row['kind'] == 'SAMPLE':
                path = folder / f'capture-{row["capture"]:05d}.bin'
                persist(path, [session, row, dict(kind='END', complete=row['required_reads_complete'])], synthetic=True)
                assert d4a.independent(path)[1] == row
                stop = tracker.feed(row)
                if stop:
                    useful.append(row['capture'])
                p.stdin.write(f'ACK {row["capture"]}' + (' STOP\n' if stop else '\n'))
                p.stdin.flush()
            else:
                tracker.feed(row)
        code = p.wait(timeout=15)
        stderr = p.stderr.read()
        write(folder / 'events.json', rows)
        write(folder / 'process.json', dict(command=command, exit_code=code, stderr=stderr))
        samples = [r for r in rows if r['kind'] == 'SAMPLE']
        validation = comparison.validate(rows)
        write(folder / 'comparison.json', validation)
        expected_count = 0 if mode in ('map-malformed', 'map-corrupt', 'map-source-reuse',
            'map-cache', 'map-incomplete', 'map-crash-before', 'map-wrong-owner', 'map-wrong-type', 'map-out-of-range') else 3 if mode == 'map-threads' else 2 if mode in ('map-nested', 'map-wrapper-reuse', 'map-concurrent') else 1
        errors = []
        if len(validation['chains']) != expected_count:
            errors.append('complete construction count')
        if code != 0:
            errors.append('controller exit')
        if bool(useful) != (mode == 'map-bound'):
            errors.append('source and Workshop scientific stop')
        if mode == 'map-concurrent':
            entries = [r['capture'] for r in samples if r['site']=='generation_entry']
            returns = [r['capture'] for r in samples if r['site']=='map_return']
            calls = [r['capture'] for r in samples if r['site']=='ordinary_resource_call']
            if len(entries)!=2 or len(returns)!=2 or max(entries)>=min(returns) or not calls or min(calls)<=max(returns):
                errors.append('deterministic overlapping construction phases')
        # These literal histories are an authored oracle separate from both
        # target transition code and D4C reconstruction. No multiset comparison.
        base_slots = [[0x83ec, 0, 0x83ec, 0, 0, 0], [0, 0x57c4, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0x1234]]
        for chain in validation['chains']:
            roots = [0, 0x57d5, 0x99]
            slots = [s.copy() for s in base_slots]
            calls = [0x83ec, 0x83ec, 0x57c4, 0x57d5]
            if mode == 'map-exchange':
                roots, slots = [0, 0x123, 0x123, 0x57d5], [base_slots[0], base_slots[1], [0]*6, [0]*6]
            if mode == 'map-order':
                roots = [0x57d5, 0, 0x99]
                slots[0], slots[1] = slots[1], slots[0]
                calls = [0x57c4, 0x57d5]
            if mode == 'map-null':
                slots = [[0]*6 for _ in roots]
                calls = [0x57d5]
            if mode == 'map-duplicate-root':
                roots[-1], slots[-1], calls = 0x57d5, [0]*6, [0x57d5]
            if mode == 'map-empty':
                roots, slots, calls = [], [], []
            if [c['root'] for c in chain['components']] != roots or [c['slots'] for c in chain['components']] != slots:
                errors.append('exact component oracle')
            if chain['calls'] != calls:
                if mode != 'map-bypass' or chain['calls'] or chain['candidate_call_coverage'] != 'UNKNOWN_SKIPPED_PATH_OR_GAP':
                    errors.append('exact call oracle')
            if mode not in ('map-unrelated', 'map-bound-wrong-source') and chain['source_identity'] != '0:27156:35988:0028be0d':
                errors.append('derived source identity')
            if mode == 'map-unrelated' and chain['source_identity'] == '0:27156:35988:0028be0d':
                errors.append('unrelated same-planet source')
            # Every transition has already been checked against independently
            # copied target before/after snapshots by validate().
            if len(chain['snapshots']) != len(roots)+1:
                errors.append('complete operation boundary count')
        results.append(dict(mode=mode, controller_exit=code, samples=len(samples),
                            frame_checks=[r.get('frame_matches') for r in samples],
                            loss=[r for r in rows if r['kind'] == 'LOSS'],
                            complete_chains=len(validation['chains']), useful=useful, errors=errors))
    write(out / 'summary.json', dict(schema='sor-d4d-qualification/1',
        build_sha256=pin(build / 'build.json'), cases=results,
        passed=all(not r['errors'] for r in results)))
    print(json.dumps(results, indent=2))
    assert all(not r['errors'] for r in results), 'qualification failures preserved'


if __name__ == '__main__':
    main()
