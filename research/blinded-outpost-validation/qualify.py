# SPDX-License-Identifier: GPL-3.0-or-later
"""Offline synthetic qualification driver with real Windows boundary attacks.

Reads task code, installed CPython and names of existing protected sources.
Writes exclusive ignored receipts, synthetic custodian sentinels, provisioned
runtime copies and disposable junction fixtures. Runs only task-owned Python/
PowerShell/C# fixtures. Never opens a real save successfully in the predictor;
parent records existing path identity, and the child must receive ACCESS_DENIED.
No network, game operations, source ACL edits or account changes. AppContainer
profiles are temporary. Requires host execution outside the Codex sandbox.
"""
import argparse
import ctypes
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

import gate
from test_toolchain import location, comparable, truth, bundle

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).parent
LOCAL = ROOT/'.local-work/blinded-outpost-validation'


def write(path, value):
    path.write_bytes(gate.canonical(value))


def pin(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--label', required=True)
    args = parser.parse_args()
    if not args.label.isalnum():
        raise ValueError('LABEL')
    if min(shutil.disk_usage(d).free for d in ('C:/', 'D:/')) < 40000000000:
        raise ValueError('DISK_FLOOR')
    out = LOCAL/args.label
    out.mkdir()
    source_before = {p.name: pin(p) for p in HERE.iterdir() if p.is_file()}
    write(out/'source-before.json', source_before)
    commands = []

    def run(label, command, expected=0):
        result = subprocess.run(command, cwd=ROOT, capture_output=True)
        (out/(label+'-stdout.txt')).write_bytes(result.stdout)
        (out/(label+'-stderr.txt')).write_bytes(result.stderr)
        commands.append(dict(label=label, command=command, exit_code=result.returncode,
            stdout_sha256=pin(out/(label+'-stdout.txt')), stderr_sha256=pin(out/(label+'-stderr.txt'))))
        if expected == 0 and result.returncode or expected != 0 and result.returncode == 0:
            raise AssertionError(label + ': unexpected exit; inspect preserved logs')
        return result

    run('tests', [sys.executable, '-B', str(HERE/'test_toolchain.py')])
    custodian = out/'custodian'; custodian.mkdir()
    for name in ('raw.sfs', 'extractors.json', 'native.bin', '.hidden.json', 'revelation.json'):
        (custodian/name).write_bytes(b'SYNTHETIC CONFIDENTIAL RESOURCE 00000002\n')
    assert ctypes.windll.kernel32.SetFileAttributesW(str(custodian/'.hidden.json'), 2)
    save_dir = Path('C:/Users/User/Documents/My Games/Starfield/Saves')
    actual_save = next(save_dir.glob('Save*.sfs'))
    original_pin = pin(actual_save)
    probe_input = out/'probe-input'; probe_input.mkdir()
    probes = [dict(operation='read', path=str(custodian/n), purpose=n) for n in
        ('raw.sfs', 'extractors.json', 'native.bin', '.hidden.json', 'revelation.json')]
    probes += [dict(operation='list', path=str(custodian), purpose='custodian-enumeration'),
        dict(operation='read', path=str(actual_save), purpose='real-protected-save'),
        dict(operation='list', path=str(save_dir), purpose='real-save-enumeration'),
        dict(operation='list', path=str(ROOT/'.local-work/resource-combined-acquisition'), purpose='native-capture-enumeration'),
        dict(operation='read', path=str(custodian/'../custodian/raw.sfs'), purpose='path-traversal'),
        dict(operation='write', path='../input/probes.json', purpose='read-only-input'),
        dict(operation='symlink', path=str(custodian/'raw.sfs'), purpose='symlink-escape-attempt')]
    write(probe_input/'probes.json', probes)
    probe_manifest = out/'probe-manifest.json'
    write(probe_manifest, {'probes.json': pin(probe_input/'probes.json')})
    powershell = shutil.which('pwsh') or shutil.which('powershell')
    def boundary(label, worker, inputs, manifest, expected=0):
        dest = LOCAL/(args.label+'-'+label)
        run(label, [powershell, '-NoProfile', '-File', str(HERE/'boundary.ps1'),
            '-Destination', str(dest), '-Worker', str(worker), '-Inputs', str(inputs),
            '-InputManifest', str(manifest), '-WorkerSha256', pin(worker)], expected)
        return dest
    dest = boundary('probes', HERE/'probe.py', probe_input, probe_manifest)
    evidence = json.loads((dest/'output/probe.json').read_bytes())
    assert len(evidence['rows']) == len(probes)
    assert all((row['result'] == 'DENIED' and (row['winerror'] == 5 or row.get('errno') == 13)) or
        (row['operation'] == 'symlink' and row['result'] == 'DENIED_CREATION_PRIVILEGE') for row in evidence['rows']), evidence
    launch = json.loads((dest/'boundary.json').read_bytes())
    assert launch['token_verified'] and not launch['capabilities'] and launch['cleanup'] == 'PROFILE_DELETED_OR_NOT_CREATED'
    assert pin(actual_save) == original_pin
    # Hidden or unexpected extra files are rejected before launching anything.
    (probe_input/'sidecar.json').write_bytes(b'{}')
    assert ctypes.windll.kernel32.SetFileAttributesW(str(probe_input/'sidecar.json'), 2)
    boundary('sidecar-refused', HERE/'probe.py', probe_input, probe_manifest, 1)
    # The junction is deliberately outside an allowed flat input inventory.
    junction = out/'junction'
    junction_script = out/'junction.ps1'
    junction_script.write_bytes(b'param([string]$Link,[string]$Target)\nNew-Item -ItemType Junction -Path $Link -Target $Target | Out-Null\n')
    run('junction-create', [powershell, '-NoProfile', '-File', str(junction_script), '-Link', str(junction), '-Target', str(custodian)])
    boundary('junction-refused', HERE/'probe.py', junction, probe_manifest, 1)
    (custodian/'worker.py').write_bytes(b'raise RuntimeError("Untrusted worker")\n')
    refused = boundary('worker-ancestor-refused', junction/'worker.py', probe_input, probe_manifest, 1)
    assert not refused.exists()
    assert b'Reparse ancestor' in (out/'worker-ancestor-refused-stderr.txt').read_bytes()
    outputs = []
    for body in ('Kreet', 'Vectera', 'Jemison'):
        inputs = out/(body+'-input'); inputs.mkdir()
        for name in ('bridge.py',):
            (inputs/name).write_bytes((HERE/name).read_bytes())
        write(inputs/'location.json', location(body))
        manifest = out/(body+'-manifest.json')
        write(manifest, {p.name: pin(p) for p in inputs.iterdir()})
        for repeat in range(2):
            destination = boundary(body+str(repeat), HERE/'predict.py', inputs, manifest)
            outputs.append(dict(body=body, repeat=repeat, path=str(destination/'output/prediction.json'),
                sha256=pin(destination/'output/prediction.json')))
        assert outputs[-1]['sha256'] == outputs[-2]['sha256']
    # Durable gate examples are explicitly synthetic; all rules and tools freeze
    # before this driver writes revelation, with independent expected digests.
    examples = []
    for ordinal, mode in enumerate(('mismatch', 'different-alternative'), 1):
        trial = f'{ordinal:032x}'; p = comparable(); p['trial'] = trial
        registry = out/(mode+'-registry'); registry.mkdir()
        work = out/(mode+'-bundle'); inventory = bundle(work, p)
        frozen = gate.freeze(registry, work, trial,
            ['location_custodian', 'prediction_runner', 'revelation_custodian', 'independent_gate', 'comparator'], inventory)
        t = truth(p, 1 if mode == 'different-alternative' else 0)
        if mode == 'mismatch':
            t['sources'][0]['regions'][0]['points_le'] = '00008841' + t['sources'][0]['regions'][0]['points_le'][8:]
        truthpath = out/(mode+'-truth.json'); write(truthpath, t)
        result = gate.reveal(registry, work, trial, frozen, truthpath, pin(truthpath))
        assert result['comparison']['protocol'] == 'COMPARABLE'
        examples.append(dict(mode=mode, freeze_sha256=frozen, comparison=result['comparison']))
    assert source_before == {p.name: pin(p) for p in HERE.iterdir() if p.is_file()}, 'Qualification source changed during execution'
    write(out/'summary.json', dict(schema='sor-blind-qualification/1', synthetic_only=True,
        commands=commands, denied_probes=evidence, token=launch['sid'], actual_save_unchanged=True,
        deterministic_predictions=outputs, examples=examples, accuracy_acceptance=False,
        installed_python_sha256=pin(Path(sys.executable)), source={p.name: pin(p) for p in HERE.iterdir() if p.is_file()}))
    print('Synthetic tests, Windows token/access attacks, two replays per candidate, and freeze/reveal examples PASS')


if __name__ == '__main__':
    main()
