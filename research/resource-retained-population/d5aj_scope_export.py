# SPDX-License-Identifier: GPL-3.0-or-later
"""Export explicit D5AJ dependencies from a verified disposable Ghidra copy.

Reads the D5AI copy receipt and owned P1 Java export method, rehashes every
copied core, and opens only that existing disposable copy with read-only and
no-analysis flags. Writes a fresh ignored D5AJ directory with settings, native
exports and preservation receipts. No original project opens, symbols, types or
comments change, native code executes, process attaches, save writes or network
operations occur. Stop on pin, path, disk, subprocess or export failure.

SOR-P-0002: adapts d5ai_owner_function_export.py and the P1 owned Java exporter.
The bounded component census now includes source-vector, parent-Grid and copy
operands through the final derived Grid method. Raw native exports stay local.
"""
import sys
if not __debug__ or sys.flags.optimize:
    raise RuntimeError('Use Python -E -B without optimization')
import json
from pathlib import Path
import re
import subprocess
from d5ad_baseline import guard, sha

ROOT = Path(__file__).resolve().parents[2]


def main():
    if len(sys.argv) < 3 or not re.fullmatch('[a-z0-9-]+', sys.argv[1]):
        raise ValueError('Fresh label and explicit export entries required')
    entries = sys.argv[2:]
    if len(entries) > 45 or any(not (re.fullmatch('[0-9a-f]+', value) or
                                       re.fullmatch('@[0-9a-f]+:[0-9]+', value) or
                                       value == '%gridcells') for value in entries):
        raise ValueError('Explicit native addresses/data or bounded Grid census required')
    previous = ROOT / '.local-work/d5ai-ownership/export01'
    prior = json.loads((previous / 'result.json').read_bytes())
    if not prior['copy_core_preserved'] or not prior['original_core_preserved']:
        raise ValueError('Missing original disposable-copy qualification')
    copy = Path('D:/tools/sor-d5ai-ownership-export01')
    out = ROOT / '.local-work/d5aj/native-scope' / sys.argv[1]
    if out.exists():
        raise FileExistsError(out)
    free_before = guard()
    for path, expected in prior['copied'].items():
        if not Path(path).is_relative_to(copy) or sha(path) != expected:
            raise ValueError('Disposable core mismatch: ' + path)
    reader = ROOT / '.local-work/d5ab/p1-specialist-export15/ExploreD5S.java'
    if sha(reader) != 'b9e3b48a2899070b6afec9d07bd7c0432ed4667ddd63bb252242842dee0bf96e':
        raise ValueError('Owned Java reader identity changed')
    java = reader.read_text(encoding='utf8')
    java = java.replace('toAddr("1409871cf")', 'toAddr("14098786f")')
    java = java.replace('if(value.contains(" + 0x20]")||value.contains(" + 0x18]"))',
                        'if(value.contains("0x10")||value.contains("0x18")||value.contains("0x70")||value.contains("CALL")||value.contains("MOVUPS")||value.contains("MOVDQU"))')
    out.mkdir()
    (out / reader.name).write_text(java, encoding='utf8', newline='\n')
    command = [value.replace(str(previous), str(out)) for value in prior['command']]
    at = command.index('-postScript')
    command = command[:at] + ['-postScript', reader.name, str(out / 'native.tsv'),
                             *entries, '-log', str(out / 'ghidra.log'),
                             '-scriptlog', str(out / 'script.log')]
    if str(copy) not in command or any('D:\\ReverseEngineering' in value or
                                       'D:/ReverseEngineering' in value for value in command):
        raise ValueError('Original project opening prohibited')
    if '-readOnly' not in command or '-noanalysis' not in command:
        raise ValueError('Read-only flags required')
    for name in ('ghidra-settings', 'ghidra-cache', 'java-tmp', 'java-home'):
        (out / name).mkdir()
    receipt = dict(command=command, copy_core_before=prior['copied'],
                   prior_receipt_sha256=sha(previous / 'result.json'),
                   method_sha256=sha(__file__), reader_origin=str(reader.relative_to(ROOT)),
                   reader_origin_sha256=sha(reader), java_sha256=sha(out / reader.name),
                   free_before=free_before)
    (out / 'command.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf8', newline='\n')
    with (out / 'stdout.log').open('xb') as stdout, (out / 'stderr.log').open('xb') as stderr:
        result = subprocess.run(command, cwd=ROOT, stdout=stdout, stderr=stderr,
                                creationflags=subprocess.CREATE_NO_WINDOW)
    for path, expected in prior['copied'].items():
        if sha(path) != expected:
            raise ValueError('Disposable core changed: ' + path)
    if result.returncode or not (out / 'native.tsv').read_text(encoding='utf8').endswith('END\n'):
        raise RuntimeError('Export failed: ' + str(result.returncode))
    receipt.update(exit=result.returncode, native_sha256=sha(out / 'native.tsv'),
                   copy_core_preserved=True, free_after=guard())
    (out / 'result.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf8', newline='\n')
    print(out, receipt['native_sha256'])


if __name__ == '__main__':
    main()
