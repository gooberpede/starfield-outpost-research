# SPDX-License-Identifier: GPL-3.0-or-later
"""Export named owner helpers from the independently reverified disposable copy.

Reads prior D5AM copy pins and the owned D5S-derived D5AM exporter. Opens only that copy in
read-only/no-analysis Ghidra, with fresh ignored output/settings. Rehashes every
copied core before and after. No original project opening, target or save writes.
SOR-P-0002: adapted owned d5ai_owner_function_export.py; copied-core namespace
and early optimization guard differ. Original fifteen-file proof is inherited
from the pinned first fresh D5AM receipt; only the copy is opened.
"""
import os
import sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE','0') not in ('','0'):
    raise RuntimeError('Python optimization is forbidden; invoke with -E -B')
from pathlib import Path
import json
import subprocess
from d5ad_baseline import guard,sha

ROOT=Path(__file__).resolve().parents[2]
def main():
    label=sys.argv[1]
    if not label or any(c not in 'abcdefghijklmnopqrstuvwxyz0123456789-' for c in label):raise ValueError('Simple label')
    if len(sys.argv)<3 or any(not value or any(c not in '0123456789abcdef' for c in value) for value in sys.argv[2:]):raise ValueError('Explicit static function addresses')
    previous=ROOT/'.local-work/d5am/owner-census01'
    prior=json.loads((previous/'result.json').read_bytes())
    if not prior['copy_core_preserved'] or not prior['original_core_preserved']:raise ValueError('Prior copy proof')
    copy=Path('D:/tools/sor-d5am-owner-census01')
    out=ROOT/'.local-work/d5am'/label
    if any(p.is_symlink() or p.is_junction() for p in (out,*out.parents)) or out.exists():raise FileExistsError(out)
    for path,expected in prior['copied'].items():
        if not Path(path).is_relative_to(copy) or sha(path)!=expected:raise ValueError('Disposable core mismatch')
    guard();out.mkdir()
    script=Path(__file__).with_name('D5AMOwnerCensus.java')
    (out/script.name).write_bytes(script.read_bytes())
    command=[s.replace(str(previous),str(out)) for s in prior['command']]
    at=command.index('-postScript')
    command=command[:at]+['-postScript',script.name,str(out/'native.tsv'),*sys.argv[2:],'-log',str(out/'ghidra.log'),'-scriptlog',str(out/'script.log')]
    if str(copy) not in command or any('D:\\ReverseEngineering' in s or 'D:/ReverseEngineering' in s for s in command):raise ValueError('Original project prohibited')
    if '-readOnly' not in command or '-noanalysis' not in command:raise ValueError('Read-only flags')
    for name in ('ghidra-settings','ghidra-cache','java-tmp','java-home'):(out/name).mkdir()
    receipt=dict(command=command,interpreter_sha256=sha(sys.executable),java_executable_sha256=sha(command[0]),
                 ghidra_utility_sha256=sha(command[command.index('-cp')+1]),copy_core_before=prior['copied'],prior_receipt_sha256=sha(previous/'result.json'),
                 method_sha256=sha(__file__),java_sha256=sha(script),free_before=guard())
    (out/'command.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf8',newline='\n')
    with (out/'stdout.log').open('xb') as stdout,(out/'stderr.log').open('xb') as stderr:
        completed=subprocess.run(command,cwd=ROOT,stdout=stdout,stderr=stderr,creationflags=subprocess.CREATE_NO_WINDOW)
    for path,expected in prior['copied'].items():
        if sha(path)!=expected:raise ValueError('Disposable core changed')
    if completed.returncode or not (out/'native.tsv').read_text(encoding='utf8').endswith('END\n'):raise RuntimeError('Export failed')
    receipt.update(exit=completed.returncode,native_sha256=sha(out/'native.tsv'),copy_core_preserved=True,free_after=guard())
    (out/'result.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf8',newline='\n')
    print(out,receipt['native_sha256'])

if __name__=='__main__':
    main()
