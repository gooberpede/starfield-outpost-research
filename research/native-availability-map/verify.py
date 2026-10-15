# SPDX-License-Identifier: GPL-3.0-or-later
"""Verify source-linked native contracts; reads only, exclusive local receipt.

No third-party implementation, target execution or analysis-project writes.
See README.md for dependencies, effects, prerequisites and reproduction.
"""
import argparse
import csv
import ctypes
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / '.local-work/native-availability-map'
DOCS = ROOT / 'docs/experiments/native-availability-map'
EXE = Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield/Starfield.exe')
PIN = '7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28'


def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--run', required=True)
    args = parser.parse_args()
    if not args.run.replace('-', '').isalnum():
        raise ValueError('RUN_NAME')
    disk = {}
    for drive in ('C:/', 'D:/'):
        available = ctypes.c_ulonglong()
        if not ctypes.windll.kernel32.GetDiskFreeSpaceExW(drive, ctypes.byref(available), None, None):
            raise OSError('disk query failed')
        disk[drive] = available.value
        if available.value < 40_000_000_000:
            raise RuntimeError('DISK_GUARD')
    assert sha(EXE) == PIN, 'BUILD_PIN'
    sources = list(csv.DictReader((DOCS / 'sources.csv').open(encoding='utf8', newline='')))
    texts = {}
    for row in sources:
        path = ROOT / row['path']
        assert sha(path) == row['sha256'], row['path']
        assert path.stat().st_size == int(row['bytes'])
        texts[row['path']] = path.read_text(encoding='utf8')
    register = list(csv.DictReader((DOCS / 'functions.csv').open(encoding='utf8', newline='')))
    assert len({r['key'] for r in register}) == len(register)
    for row in register:
        assert row['exe_sha256'] == PIN
        assert int(row['static_va'], 16) - 0x140000000 == int(row['rva'], 16)
        assert row['original_name'] == 'FUN_' + row['static_va'][2:]
        text = texts[row['source']]
        assert 'SHA256\t' + PIN in text and 'BASE\t140000000' in text
        # Full function declaration, not just a reference to the address.
        assert 'FUNCTION\t' + row['static_va'][2:] + '\t' + row['original_name'] + '\t' in text, row['key']
        for field in ('inputs', 'outputs', 'prerequisites', 'effects', 'edges', 'limits'):
            assert row[field].strip(), (row['key'], field)
    # Exact instruction pairs: guard against silently converting retained cache
    # state to an empty list, or treating the updater as a region-array API.
    ui = texts['.local-work/recon/resource-availability-ui-15.tsv']
    dependencies = {
        'updater_radius': '1421e07fd\tVMOVAPS XMM6,XMM3',
        'updater_radius2': '1421e0801\tVMOVAPS XMM7,XMM2',
        'internal_manager': '1421e09d4\tMOV RAX,qword ptr [0x145fd9c30]',
        'internal_procgen': '1421e09db\tMOV R15,qword ptr [RAX + 0x130]',
        'procgen_lock': '1421e09ed\tCALL 0x1422cc350',
        'source_callback': '1421e0a46\tCALL 0x1421e0f50',
        'atmo_null_retains': '1421e0c77\tJZ 0x1421e0d65',
        'atmo_same_retains': '1421e0c84\tJZ 0x1421e0d65',
        'biome_null_retains': '1421e0e5b\tJZ 0x1421e0eff',
        'biome_same_retains': '1421e0e68\tJZ 0x1421e0eff',
        'biome_changed_clears': '1421e0e79\tMOV qword ptr [R14 + 0x38],RAX',
        'established_radius': '1421b26b4\tVMOVSS XMM2,dword ptr [RBX + 0x28]',
        'established_height': '1421b26af\tVMOVSS XMM3,dword ptr [RBX + 0x2c]',
        'established_call': '1421b26bc\tCALL 0x1421e07d0',
        'preview_call': '1421b42e3\tCALL 0x1421e07d0',
        'other_call': '1421b6931\tCALL 0x1421e07d0',
    }
    for key, instruction in dependencies.items():
        assert instruction in ui, key
    updater = ui.split('DECOMPILED\ttrue', 1)[0]
    assert 'CALL 0x14079f860' not in updater, 'AREA_PATH_NOT_GENERATOR'
    desc = texts['.local-work/recon/workshop-origin-03.tsv']
    for instruction in (
        '140f4a2ba\tCALL 0x140f38e30',
        '140f4a2bf\tVMOVSS dword ptr [R14 + 0x28],XMM0',
        '140f4a2d5\tVMOVSS dword ptr [R14 + 0x2c],XMM0',
        '140f4a429\tVMOVSS dword ptr [R14 + 0x2c],XMM0',
    ):
        assert instruction in desc
    tests = []
    for pattern in ('test_resource_availability*.py', 'test_resource_spatial.py'):
        command = [sys.executable, '-B', '-m', 'unittest', 'discover', '-s', 'save-analysis/scripts', '-p', pattern]
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
        tests.append(dict(command=command, returncode=result.returncode, stdout=result.stdout, stderr=result.stderr))
    receipt = dict(exe_sha256=PIN, disk=disk, sources=sources, functions=len(register),
                   dependencies=dependencies, tests=tests, native_spatial_equivalence='NOT TESTED',
                   scope='Static instruction assertions and synthetic evaluator regressions; no native calls')
    with (BASE / (args.run + '.json')).open('x', encoding='utf8', newline='\n') as stream:
        json.dump(receipt, stream, indent=2)
        stream.write('\n')
    assert all(t['returncode'] == 0 and 'Ran 0 tests' not in t['stderr'] for t in tests)
    print(json.dumps(dict(functions=len(register), source_pins=len(sources), instruction_contracts=len(dependencies), tests=tests)))


if __name__ == '__main__':
    main()
