# SPDX-License-Identifier: GPL-3.0-or-later
"""Export original command/lifetime root references from the verified D5AM copy.

Adapts the project-owned D5AM exporter and Java method under SOR-P-0002. Reads
the recorded 15-file copy roster and installed Ghidra/JDK, verifies copy bytes
before and after, and writes only a fresh ignored output namespace. Opens only
the disposable copy with -readOnly -noanalysis. No original database, native
target, save, network, installed configuration or Git content is written.
"""
import os
import sys
if sys.flags.optimize or not __debug__ or os.environ.get('PYTHONOPTIMIZE', '0') not in ('', '0'):
    raise RuntimeError('Optimization forbidden; invoke pinned Python -E -B')

import hashlib
import json
from pathlib import Path
import subprocess
from d5ar_native_inventory import ROOT, disk_floor


def sha(path):
    with Path(path).open('rb') as source:
        return hashlib.file_digest(source, 'sha256').hexdigest()


def main():
    label, root = sys.argv[1:]
    if not label or any(c not in 'abcdefghijklmnopqrstuvwxyz0123456789-' for c in label):
        raise ValueError('Simple label required')
    if not root or any(c not in '0123456789abcdef' for c in root):
        raise ValueError('Explicit static root address required')
    previous = ROOT / '.local-work/d5am/owner-census01'
    prior = json.loads((previous / 'result.json').read_bytes())
    copy = Path('D:/tools/sor-d5am-owner-census01')
    output = ROOT / '.local-work/d5ar' / label
    if output.exists() or any(p.is_symlink() or p.is_junction() for p in (output, *output.parents)):
        raise ValueError('Fresh non-reparse output required')
    if not prior['copy_core_preserved'] or not prior['original_core_preserved']:
        raise ValueError('Missing original copy preservation proof')
    for path, expected in prior['copied'].items():
        if not Path(path).is_relative_to(copy) or sha(path) != expected:
            raise ValueError('Disposable copy mismatch')
    before = disk_floor()
    output.mkdir(parents=True)
    java_source = ROOT / 'research/resource-retained-population/D5AMOwnerCensus.java'
    original = java_source.read_text(encoding='utf8')
    old = 'boolean rootsMode=args.length==2&&args[1].equals("145fd9c30");'
    new = 'boolean rootsMode=args.length==2;'
    if original.count(old) != 1:
        raise ValueError('Owned Java source anchor changed')
    generated = original.replace(old, new)
    first = generated.index('                FunctionIterator fit=')
    last = generated.index('                ReferenceIterator rr=', first)
    generated = generated[:first] + generated[last:]
    generated = generated.replace('toAddr("145fd9c30")', 'toAddr(args[1])')
    generated = generated.replace('Manager method interval140787000..140790000 plus every existing direct manager singleton reference receiver',
                                  'D5AR explicit data-root references and their existing containing functions')
    (output / java_source.name).write_text(generated, encoding='utf8', newline='\n')
    command = [s.replace(str(previous), str(output)) for s in prior['command']]
    at = command.index('-postScript')
    command = command[:at] + ['-postScript', java_source.name, str(output / 'native.tsv'), root,
                            '-log', str(output / 'ghidra.log'), '-scriptlog', str(output / 'script.log')]
    if str(copy) not in command or '-readOnly' not in command or '-noanalysis' not in command:
        raise ValueError('Disposable read-only command required')
    for name in ('ghidra-settings', 'ghidra-cache', 'java-tmp', 'java-home'):
        (output / name).mkdir()
    receipt = dict(command=command, source_sha256=sha(__file__), owned_java_input_sha256=sha(java_source),
                   generated_java_sha256=sha(output / java_source.name), copy_before=prior['copied'],
                   prior_receipt_sha256=sha(previous / 'result.json'), free_before=before,
                   interpreter_sha256=sha(sys.executable), java_sha256=sha(command[0]),
                   ghidra_utility_sha256=sha(command[command.index('-cp') + 1]))
    (output / 'command.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf8', newline='\n')
    with (output / 'stdout.log').open('xb') as stdout, (output / 'stderr.log').open('xb') as stderr:
        result = subprocess.run(command, cwd=ROOT, stdout=stdout, stderr=stderr, creationflags=subprocess.CREATE_NO_WINDOW)
    for path, expected in prior['copied'].items():
        if sha(path) != expected:
            raise ValueError('Disposable copy changed')
    if result.returncode or not (output / 'native.tsv').read_text(encoding='utf8').endswith('END\n'):
        raise RuntimeError('Read-only export failed')
    receipt.update(exit=result.returncode, copy_preserved=True, native_sha256=sha(output / 'native.tsv'), free_after=disk_floor())
    (output / 'result.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf8', newline='\n')
    print(output)


if __name__ == '__main__':
    main()
