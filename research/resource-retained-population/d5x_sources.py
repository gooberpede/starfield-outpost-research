# SPDX-License-Identifier: GPL-3.0-or-later
"""Pin D5X input provenance and local-only exclusions, without target execution.

Reads explicitly listed owned sources, installed inputs/tools and local receipts.
Writes the authored source CSV plus a fresh ignored exclusions manifest. Raw
native bytes are never promoted. Stdlib only; no save, database, installed-file,
network or Git mutation.
"""
import csv
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
LOCAL = ROOT / '.local-work/d5x'
DOC = ROOT / 'docs/experiments/resource-retained-population'


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream,'sha256').hexdigest()


def main():
    output = LOCAL / sys.argv[1]
    assert not output.exists()
    rows = []
    head = subprocess.check_output(['git','--no-optional-locks','rev-parse','HEAD'],cwd=ROOT).decode().strip()
    def add(path,kind,claim,origin,eligibility='LOCAL-ONLY'):
        path = Path(path)
        display = str(path.relative_to(ROOT)).replace('\\','/') if path.is_relative_to(ROOT) else str(path)
        rows.append(dict(id=f'D5X-S{len(rows)+1:03}',classification=kind,path=display,bytes=path.stat().st_size,
                         sha256=sha(path),claim=claim,origin=origin,eligibility=eligibility))
    identity = json.loads((LOCAL/'identity04/identity.json').read_text())
    for name in identity['installed']:
        add(name,'INSTALLED INPUT','Fresh exact identity; bytes do not prove semantics','Bethesda/SFSE installed input')
    for name in ('plugin.cpp','observer.h','patch.h','build.py','read_capture.py'):
        add(ROOT/'runtime/retained-population'/name,'OWNED ADAPTATION INPUT','R1 transport/patch/startup method adapted; geometry and Grid validator excluded',head,'REVIEW-REQUIRED')
    for name in ('core.h','win_support.h','third_party/sfse/PluginAPI.h','third_party/sfse/LICENSE.txt'):
        add(ROOT/'runtime/exp0002'/name,'SUPPORT OR APPROVED HEADER','Owned support reused; unchanged SFSE header under explicit D5X MIT extension',head,'REVIEW-REQUIRED')
    sibling=Path('D:/Projects/starfield-reference-handles')
    sibling_head=subprocess.check_output(['git','-c',f'safe.directory={sibling.as_posix()}','--no-optional-locks','rev-parse','HEAD'],cwd=sibling).decode().strip()
    for name in ('plugin.cpp','observer.cpp'):
        add(sibling/'plugin/reference-observer/src'/name,'CONSULTED OWNED SOURCE','Read-only architecture consultation; no CommonLibSF implementation/dependency incorporated',sibling_head)
    for name in ('d5p-r1','d5p-r2','d5p-r2-retail','d5p-r3','d5q','d5r','d5s','d5t','d5u','d5v','d5w'):
        path=DOC/(name+'-sources.csv')
        if path.exists():add(path,'INHERITED SOURCE LEDGER','Prior evidence and failed-run provenance retained unchanged',head,'REVIEW-REQUIRED')
    functions = {'d5q':['140988240-q','140988330-q','140988760-q','140988ab0-q','14078d660-q'],
                 'd5v':['140787830','140788e70','140789850','1407846d0','140784730','140982d90','14079ddf0','140982b70'],
                 'd5w':['14079f860','14079b520','140992ab0','14099fce0','14078c5f0','14096f5c0','140986da0']}
    for task,names in functions.items():
        for name in names:
            add(ROOT/f'.local-work/{task}/functions/{name}.txt','STATIC PRIMARY EXPORT',
                'Original selection/reset/identity/ownership instructions; preferred static VA domain','Existing read-only Ghidra export')
    for name in ('identity02/identity.json','identity03/identity.json','identity04/identity.json','identity05/identity.json','cold-order02.txt','cold-order02.json','cold-order.py','aborted-development-processes.json','toolchain.txt'):
        add(LOCAL/name,'D5X PRIMARY RECEIPT','Fresh identity, cold-order challenge or preserved failed-run disposition','D5X original local method/receipt')
    capstone=Path('C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/Lib/site-packages/capstone')
    for path in (Path(sys.executable),capstone/'__init__.py',capstone/'lib/capstone.dll',Path('C:/Program Files/Microsoft Visual Studio/18/Community/VC/Auxiliary/Build/vcvars64.bat')):
        add(path,'EXISTING STANDALONE TOOL','Execution/decoding only; no implementation incorporation','Installed tool; Capstone 5.0.7 where applicable')
    compiler=Path('C:/Program Files/Microsoft Visual Studio/18/Community/VC/Tools/MSVC/14.51.36231/bin/Hostx64/x64')
    for name in ('cl.exe','link.exe','ml64.exe'):
        add(compiler/name,'EXISTING BUILD TOOL','Actual MSVC/MASM compiler/linker binary pin','Installed Visual Studio toolchain')
    brief=ROOT/'docs/implementation-briefs/CODEX_BRIEF_SOR_RG2_D5X_construction_winner_observer_feasibility_qualification.md'
    add(brief,'FROZEN AUTHORITY','Original unchanged questions and eleven mandatory criteria','Supplied brief','REVIEW-REQUIRED')
    with (DOC/'d5x-sources.csv').open('w',encoding='utf8',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(rows[0]),lineterminator='\n');writer.writeheader();writer.writerows(rows)
    excluded={str(path.relative_to(ROOT)).replace('\\','/'):dict(bytes=path.stat().st_size,sha256=sha(path))
              for path in LOCAL.rglob('*') if path.is_file()}
    output.write_text(json.dumps(dict(schema='sor-d5x-exclusions/1',files=excluded,
        outside_roots=['Installed game/assets/SFSE and protected saves/backups remain in place; never copied into patches',
                       'Existing analysis databases/native exports outside task scratch remain local and unchanged']),indent=2)+'\n',encoding='utf8',newline='\n')
    print(json.dumps(dict(source_rows=len(rows),excluded_files=len(excluded),source_ledger_sha256=sha(DOC/'d5x-sources.csv'))))


if __name__=='__main__':main()
