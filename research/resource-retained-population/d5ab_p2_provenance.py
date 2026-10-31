# SPDX-License-Identifier: GPL-3.0-or-later
"""Verify final P2 component receipts and emit a selected synthetic summary.

Reads explicit local native/controller/queue/consumer receipts, current source,
Git HEAD/index and preserved historical evidence. Writes a fresh ignored provenance
receipt and an authored summary JSON under docs. Uses CPython stdlib only. No build,
game, network, deployment, save/database mutation, staging, commit or push.
"""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding='utf8'))


def main():
    build, controller, queue, reader, sharing, legacy, out = [Path(value).resolve() for value in sys.argv[1:]]
    assert all(p.is_relative_to(ROOT / '.local-work') for p in (build, controller, queue, reader, sharing, legacy, out))
    free = {drive: shutil.disk_usage(drive).free for drive in ('C:/', 'D:/')}
    assert min(free.values()) >= 40_000_000_000
    out.mkdir(exist_ok=False)
    native = read(build / 'build.json')
    control = read(controller / 'receipt.json')
    stress = read(queue / 'receipt.json')
    consume = read(reader / 'receipt.json')
    shared = read(sharing / 'receipt.json')
    regression = read(legacy / 'receipt.json')
    assert regression['passed'] and regression['tests'] == 54 and regression['build'] == str(build)
    assert all(sha(name) == digest for name, digest in regression['inputs'].items())
    assert shared['passed'] and shared['source_unchanged'] and shared['old_policy_open_error'] == 32
    assert shared['build'] == str(build) and shared['final_state'] == 'STOPPED_LOSS'
    assert all(sha(ROOT / name) == digest for name, digest in shared['inputs'].items())
    assert native['source_unchanged'] and native['compilation']['pass_exit']
    assert len(native['cases']) == 61 and all(r['pass_exit'] for r in native['cases'])
    assert all(sha(path) == digest for path, digest in native['inputs'].items())
    assert control['passed'] and len(control['results']) == 26
    controller_cases = []
    for item in control['results']:
        assert item['exit'] == 0 and sha(item['receipt']) == item['receipt_sha256']
        case = read(item['receipt'])
        assert case['passed'] and case['source_unchanged'] and case['build'] == str(build)
        assert all(sha(ROOT / path) == digest for path, digest in case['inputs'].items())
        controller_cases.extend({k: row[k] for k in ('case', 'pass_test', 'states', 'readback')} for row in case['results'])
    assert stress['source_unchanged'] and len(stress['results']) == 9
    assert all(sha(path) == digest for path, digest in stress['inputs'].items())
    assert all(row['passed'] and row['lossless_losses'] == 0 for row in stress['results'])
    assert consume['passed'] and consume['final_build_consumer_match'] and not consume['development_only']
    assert consume['build_sha256'] == sha(build / 'build.json')
    assert all(sha(path) == digest for path, digest in consume['inputs'].items())
    package = build / 'package-runtime'
    assert consume['dll_sha256'] == sha(package / 'SorConstructionWinner.dll')
    for name in ('read_capture.py', 'reduce_v3.py', 'worker_health.py', 'controller.py'):
        assert sha(package / name) == sha(ROOT / 'runtime/construction-winner' / name)
    unchanged = {}
    for name in ('observer.h', 'bridges.asm', 'fixture.asm', 'patch.h', 'plugin.cpp'):
        relative = 'runtime/construction-winner/' + name
        old = subprocess.check_output(['git', 'show', 'HEAD:' + relative], cwd=ROOT)
        assert hashlib.sha256(old).hexdigest() == sha(ROOT / relative)
        unchanged[relative] = sha(ROOT / relative)
    preservation = []
    for item in read(ROOT / '.local-work/d5ab-c2/preservation-before.json'):
        path = ROOT / item['path']
        if not item['path'].startswith('.local-work/'):
            continue
        if item['exists']:
            assert path.is_file() and path.stat().st_size == item['bytes'] and sha(path) == item['sha256'], item['path']
        else:
            assert not path.exists(), item['path']
        preservation.append(item)
    representative = read(build / 'representative/terminal.json')
    representative_host = read(build / 'representative/fixture.json')
    assert representative['drops'] == 0 and representative['enqueued'] == representative['acknowledged']
    receipt_paths = [build / 'build.json', controller / 'receipt.json', queue / 'receipt.json', reader / 'receipt.json', sharing / 'receipt.json', legacy / 'receipt.json']
    prior_build = ROOT / '.local-work/d5x/p2-repro01'
    repeated = read(prior_build / 'build.json')
    assert repeated['source_unchanged'] and repeated['compilation']['pass_exit']
    assert len(repeated['cases']) == 2 and all(item['pass_exit'] for item in repeated['cases'])
    assert repeated['inputs'] == native['inputs']
    repeated_dll = sha(prior_build / 'SorConstructionWinner.dll') == consume['dll_sha256']
    assert repeated_dll
    summary = dict(schema='sor-d5ab-p2-qualified-components/1',
                   scope='Offline engineering only; source lifetime unqualified; B2 NOT AUTHORIZED',
                   receipts={str(p.relative_to(ROOT)): sha(p) for p in receipt_paths},
                   components={str(Path(p).relative_to(ROOT)): digest for p, digest in native['inputs'].items()},
                   dll_sha256=consume['dll_sha256'], unchanged_native_boundaries=unchanged,
                   repeated_dll_build=dict(prior=str(prior_build.relative_to(ROOT)), identical_sha256=repeated_dll,
                       build_receipt_sha256=sha(prior_build / 'build.json'), control_cases=2,
                       limit='Identical final inputs and DLL bytes in a separate build; two reproduction controls do not replace the full 61-case suite.'),
                   native_cases=61, consumer_checks=consume['tests'], controller_cases=controller_cases,
                   legacy_semantic_regressions=regression['tests'],
                   file_sharing_control=dict(passed=True, old_policy_open_error=32, final_state=shared['final_state']),
                   queue_runs=stress['results'], representative={key: representative[key] for key in (
                       'enqueued', 'written', 'flushed', 'acknowledged', 'drops', 'cell_bytes', 'capacity',
                       'queue_high_water_lower_bound', 'output_faults', 'max_flush_ticks', 'qpc_frequency', 'worker_timing_ticks')},
                   representative_host=representative_host,
                   preserved_historical_files=len(preservation))
    summary['initial_free'] = free
    summary['final_free'] = {drive: shutil.disk_usage(drive).free for drive in free}
    assert min(summary['final_free'].values()) >= 40_000_000_000
    (out / 'preservation.json').write_text(json.dumps(preservation, indent=2) + '\n', encoding='utf8', newline='\n')
    (out / 'receipt.json').write_text(json.dumps(summary, indent=2) + '\n', encoding='utf8', newline='\n')
    (ROOT / 'docs/experiments/resource-retained-population/d5ab-p2-test-results.json').write_text(
        json.dumps(summary, indent=2) + '\n', encoding='utf8', newline='\n')
    print(json.dumps(dict(native=61, controller=len(controller_cases), consumer=consume['tests'], queue=9,
                          historical_preserved=len(preservation), out=str(out))))


if __name__ == '__main__':
    main()
