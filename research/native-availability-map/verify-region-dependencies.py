# SPDX-License-Identifier: GPL-3.0-or-later
"""Check focused native lifecycle transcriptions; no native execution.

Reads pinned exports/register and writes one exclusive ignored receipt. Uses
installed Python stdlib only. Run after verify.py for build/register/regressions.
No game, save, database, Git index/ref or network writes. See README.md.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / 'docs/experiments/native-availability-map'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--run', required=True)
    args = parser.parse_args()
    if not args.run.replace('-', '').isalnum():
        raise ValueError('RUN_NAME')
    texts = {}
    pins = list(csv.DictReader((DOC / 'region-sources.csv').open(encoding='utf8', newline='')))
    for row in pins:
        path = ROOT / row['path']
        with path.open('rb') as stream:
            actual = hashlib.file_digest(stream, 'sha256').hexdigest()
        assert actual == row['sha256'], row['path']
        assert path.stat().st_size == int(row['bytes'])
        texts[path.name] = path.read_text(encoding='utf8')
    tests = {
        'provider_actual_callers': ('resource-availability-ui-31.tsv', [
            'XREF\t1407a1a3c\t1407a1940', 'XREF\t1407b526a\t1407b5160']),
        'bounded_index_no_generation': ('resource-region-dependencies-01.tsv', [
            '140985885\tCALL 0x1409870d0',
            '1409858a1\tJGE 0x1409858c0', '1409858a6\tJGE 0x1409858c0',
            '1409858b1\tMOV RAX,qword ptr [RAX + RCX*0x8]', '1409858c5\tXOR EAX,EAX']),
        'neighbor_request': ('resource-region-dependencies-01.tsv', [
            '1407a1050\tCALL 0x1407a1260']),
        'task_wrappers': ('resource-region-dependencies-02.tsv', [
            '1407b585f\tCALL 0x1407b5160', '14076d14f\tCALL 0x14076c560']),
        'current_key_gate': ('resource-region-dependencies-02.tsv', [
            '1407c0745\tCMP EBX,dword ptr [0x145903184]']),
        'entry_wait_not_pure_read': ('resource-region-dependencies-02.tsv', [
            'WaitOnAddress(param_1 + 0x14,local_res8,4,0xffffffff)',
            '*(uint *)(param_1 + 0x14) = uVar5 & 0x7ffffff | 0xa0000000']),
        'broad_reset': ('event-oracle-08.tsv', [
            'FUN_1407aa8a0(param_1 + 0x10',
            '*(undefined8 *)(param_1 + 0x48) = 0', 'FUN_1407b4770']),
        'density_dependencies': ('resource-region-dependencies-04.tsv', [
            'FunctorWithDependenciesNode<BSProcGen::Resources', 'BSProcGen::DensityMapDB']),
    }
    for name, (file, patterns) in tests.items():
        for pattern in patterns:
            assert pattern in texts[file], (name, pattern)
    receipt = dict(source_pins=pins, assertions=tests, result='PASS',
                   coverage='Instruction and complete-decompilation transcription checks only',
                   runtime_sufficiency='NOT TESTED', native_spatial_equivalence='NOT TESTED')
    target = ROOT / '.local-work/resource-region-dependencies' / (args.run + '.json')
    with target.open('x', encoding='utf8', newline='\n') as stream:
        json.dump(receipt, stream, indent=2)
        stream.write('\n')
    print('PASS', len(tests), 'lifecycle assertion groups;', len(pins), 'source pins')


if __name__ == '__main__':
    main()
