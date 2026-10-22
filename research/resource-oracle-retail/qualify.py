# SPDX-License-Identifier: GPL-3.0-or-later
"""Runs only the separately compiled synthetic variant and owned layout fixture.

Exercises the same four-slot Windows debug/controller path and retail decoder.
Writes exact commands, raw synthetic memory and readback receipts to fresh ignored
output. No game launch/attachment, saves, config, dependencies or Git mutation.
"""
import argparse
import json
from pathlib import Path
import subprocess
from collect import LOCAL, pin, preserve_sample, receipt, write


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--build', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    a = ap.parse_args()
    build, output = a.build.resolve(), a.output.resolve()
    assert build.is_relative_to(LOCAL) and output.is_relative_to(LOCAL)
    manifest = json.loads((build / 'build.json').read_text())
    assert manifest['exit_code'] == 0
    for p, digest in manifest['files'].items():
        assert pin(p) == digest, p
    output.mkdir(exist_ok=False)
    unit = subprocess.run([str(build / 'sor-c1d-tests.exe')], capture_output=True, text=True)
    write(output / 'unit.json', dict(exit_code=unit.returncode, stdout=unit.stdout, stderr=unit.stderr))
    assert unit.returncode == 0
    results = []
    for mode in ('good', 'threads', 'wrong-workshop', 'wrong-return', 'stale-transfer',
                 'invalid', 'guard-mismatch', 'ackfail', 'crash-before', 'crash-after', 'partial-prelude', 'unrelated-partial', 'completion'):
        folder = output / mode
        folder.mkdir()
        command = [str(build / 'sor-c1d-fixture-controller.exe'), '--synthetic-fixture',
                   pin(build / 'sor-c1d-fixture.exe'), mode]
        write(folder / 'config.json', dict(command=command, synthetic=True, build_sha256=pin(build / 'build.json')))
        p = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        rows, acks = [], []
        for line in p.stdout:
            row = json.loads(line)
            row['synthetic'] = True
            rows.append(row)
            if row['kind'] == 'SAMPLE':
                ack, useful = preserve_sample(folder, rows[0], row, synthetic=True)
                acks.append(ack)
                response = 'REJECT\n' if mode == 'ackfail' else f'ACK {row["capture"]}\n'
                if mode == 'completion' and row['site'] == 'spatial_transfer_payload':
                    response = f'ACK {row["capture"]} STOP\n'
                p.stdin.write(response)
                p.stdin.flush()
        code = p.wait(timeout=15)
        stderr = p.stderr.read()
        write(folder / 'events.json', rows)
        samples = [r for r in rows if r['kind'] == 'SAMPLE']
        transfers = [r for r in samples if r['site'] == 'spatial_transfer_payload']
        selectors = [r for r in samples if r['site'] == 'catalogue_selected_population']
        returns = [r for r in samples if r['site'] == 'catalogue_grid_return']
        passed = False
        if mode in ('good', 'threads', 'crash-after', 'partial-prelude', 'unrelated-partial'):
            count = 3 if mode == 'threads' else 1
            passed = code == 0 and len(samples) == 4*count and len(transfers) == count and len(returns) == count
            passed &= all(r['identity'] == 'BOUND' and r['refresh_payload_site_ancestry'] == 'BOUND_TRANSFER'
                          and [m['runtime_formid'] for m in r['refresh_payload']['members']] == [0x57d4, 0x57cf] for r in transfers)
            passed &= all(r['matched_selected_input'] and r['actual_filter_al'] == 1 for r in returns)
            passed &= all(r['selected_population'] == 'spatial' and r['grid_caller'] for r in selectors)
            passed &= all(len(r['payload_file_provenance'])==2 and all(v['provenance']['main_file_identity'] for v in r['payload_file_provenance']) for r in transfers)
            passed &= all(r['shared_population_site_ancestry'] == 'UNKNOWN' for r in samples)
            if mode in ('partial-prelude', 'unrelated-partial'):
                passed &= all(r['populations']['atmosphere']['status'] == 'INCOMPLETE' for r in samples)
                passed &= not receipt.decode((folder / 'capture-00001.bin').read_bytes())[-1]['complete']
        elif mode == 'wrong-workshop':
            passed = code == 0 and len(samples) == 4 and all(r['identity'] == 'UNKNOWN' for r in samples)
        elif mode == 'wrong-return':
            passed = code == 0 and len(selectors) == 1 and not selectors[0]['grid_caller'] and not returns
        elif mode == 'stale-transfer':
            passed = code == 0 and len(transfers) == 1 and transfers[0]['identity'] == 'UNKNOWN'
        elif mode == 'invalid':
            passed = code == 0 and len(transfers) == 1 and transfers[0]['refresh_payload']['status'] == 'INCOMPLETE'
        elif mode == 'guard-mismatch':
            passed = code == 2 and not samples and 'hit instruction guard' in stderr
        elif mode == 'ackfail':
            passed = code == 0 and len(samples) == 1 and any(r['kind'] == 'EXIT' and r['stopped'] for r in rows)
        elif mode == 'crash-before':
            passed = code == 0 and not samples and any(r['kind'] == 'EXIT' for r in rows)
        elif mode == 'completion':
            passed = code == 0 and len(samples) == 2 and len(transfers) == 1 and not selectors and not returns
            passed &= any(r['kind'] == 'EXIT' and r['stopped'] for r in rows)
            passed &= sum(r['kind'] == 'ACK_ACCEPTED' and r['accepted'] for r in rows) == 2
        result = dict(mode=mode, passed=bool(passed), controller_exit=code, stderr=stderr,
                      samples=len(samples), acks=len(acks), files={p.name: pin(p) for p in folder.iterdir() if p.is_file()})
        write(folder / 'result.json', result)
        results.append(result)
        print(mode, passed, len(samples), stderr.strip(), flush=True)
    write(output / 'qualification.json', dict(synthetic=True, unit=unit.returncode == 0, cases=results))
    return 0 if all(r['passed'] for r in results) else 1


if __name__ == '__main__':
    raise SystemExit(main())
