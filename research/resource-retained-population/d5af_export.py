# SPDX-License-Identifier: GPL-3.0-or-later
"""Export explicitly named existing functions from a verified disposable project.

Uses the existing owned D5S Java reader and installed Ghidra/JDK command.
Reads the disposable D5AD copy and its receipt, plus original database hashes
for preservation checks. Writes fresh task-local exports/logs only. Ghidra may
write temporary project files in the disposable copy; the original project is
never passed to Ghidra. No analysis, symbols/types/comments, game, save, network
or Git mutation. SOR-P-0002: D5S exporter and D5AD copy-verification method.
Stop on identity, project-path, output, disk-floor or subprocess failure.
Retain scratch and failed logs; do not clean or restore original inputs.
"""
import json
from pathlib import Path
import subprocess
import sys

from d5ad_baseline import guard, sha

ROOT = Path(__file__).resolve().parents[2]
COPY = Path('D:/tools/sor-d5ad-ghidra-project')


def main():
    if not __debug__ or sys.flags.optimize:
        raise RuntimeError('Use Python -E -B')
    guard()
    out = (ROOT / '.local-work/d5af' / sys.argv[1]).resolve()
    if out.exists() or not out.is_relative_to(ROOT / '.local-work/d5af'):
        raise ValueError('Fresh task-local output required')
    rows = json.loads((COPY / 'copy-receipt.json').read_bytes())['rows']
    pins = {r['copy']: r['sha256'] for r in rows}
    originals = json.loads((ROOT / '.local-work/d5x/identity05/identity.json').read_bytes())['database']
    pins.update(originals)
    for p, expected in pins.items():
        if sha(p) != expected:
            raise ValueError('Database identity mismatch: ' + p)
    old = ROOT / '.local-work/d5s/export01'
    command = json.loads((old / 'command.json').read_bytes())
    original_dir = str(Path('D:/ReverseEngineering/Starfield/GhidraProject'))
    command = [s.replace(str(old), str(out)).replace(original_dir, str(COPY)) for s in command]
    at = command.index('-postScript')
    command = command[:at] + ['-postScript', 'ExploreD5S.java', str(out / 'native.tsv'),
                             *sys.argv[2:], '-log', str(out / 'ghidra.log'),
                             '-scriptlog', str(out / 'script.log')]
    if str(COPY) not in command or any(original_dir in s for s in command):
        raise ValueError('Original project launch prohibited')
    if '-readOnly' not in command or '-noanalysis' not in command:
        raise ValueError('Read-only export flags required')
    out.mkdir(parents=True)
    source = old / 'ExploreD5S.java'
    (out / source.name).write_bytes(source.read_bytes())
    for name in ('ghidra-settings', 'ghidra-cache', 'java-tmp', 'java-home'):
        (out / name).mkdir()
    receipt = dict(command=command, project_pins=pins, reader_sha256=sha(source),
                   method_sha256=sha(__file__), java_sha256=sha(command[0]),
                   ghidra_utility_sha256=sha(command[command.index('-cp')+1]))
    (out / 'command.json').write_text(json.dumps(receipt, indent=2)+'\n',encoding='utf8',newline='\n')
    with (out / 'stdout.log').open('xb') as stdout, (out / 'stderr.log').open('xb') as stderr:
        result = subprocess.run(command, cwd=ROOT, stdout=stdout, stderr=stderr,
                                creationflags=subprocess.CREATE_NO_WINDOW)
    for p, expected in pins.items():
        if sha(p) != expected:
            raise ValueError('Database changed: ' + p)
    if result.returncode or not (out / 'native.tsv').read_text(encoding='utf8').endswith('END\n'):
        raise RuntimeError('Export failed: ' + str(result.returncode))
    receipt.update(exit=result.returncode, native_sha256=sha(out / 'native.tsv'),
                   original_core_preserved=True, copy_core_preserved=True, free=guard())
    (out / 'result.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf8',newline='\n')
    print(json.dumps(dict(output=str(out), sha256=receipt['native_sha256'])))


if __name__ == '__main__':
    main()
