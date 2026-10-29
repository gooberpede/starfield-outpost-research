# SPDX-License-Identifier: GPL-3.0-or-later
"""Pin consulted methods, installed inputs and final receipts; no experiment.

Reads the enumerated local sources/build and writes the authored D5P CSV ledger.
No raw bytes, game, configuration, dependency installation or Git mutation.
"""
import csv
import json
from pathlib import Path
import subprocess
import sys
from build import ROOT,SRC,LOCAL,GAME,sha


def main():
    build=Path(sys.argv[1]).resolve();assert build.is_relative_to(LOCAL)
    manifest=json.loads((build/'build.json').read_text())
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    sibling=Path('D:/Projects/starfield-reference-handles')
    sibling_head=subprocess.check_output(['git','-c','safe.directory='+str(sibling),'-C',str(sibling),'rev-parse','HEAD'],text=True).strip()
    rows=[]
    def add(path,kind,use,revision):
        p=Path(path);assert p.is_file(),p
        name=p.relative_to(ROOT).as_posix() if p.is_relative_to(ROOT) else str(p)
        rows.append(dict(id='D5P-S'+str(len(rows)+1).zfill(3),path=name,sha256=sha(p),kind=kind,use=use,origin_revision=revision))
    for name in ('README.md','WORKFLOW.md','THIRD_PARTY_POLICY.md','docs/EVIDENCE_STANDARD.md','docs/SAVE_PROTECTION.md','docs/EDITORIAL_STANDARD.md'):
        add(ROOT/name,'REVIEW-REQUIRED policy','Governing constraint; no amendment by D5P',head)
    for directory,names in (
        ('resource-population-lifecycle',('native.md','report.md')),
        ('resource-source-enumeration',('native.md','report.md')),
        ('resource-query-reachability',('feasibility.md',)),
        ('resource-query-variability',('proofs.md',)),
        ('resource-retained-population',('native.md','phase-b-postmortem.md','d5m-phase-b-postmortem.md','d5n-phase-b.md','d5o-report.md','d5o-phase-b.md','d5o-phase-b-review.md'))):
        for name in names:add(ROOT/'docs/experiments'/directory/name,'REVIEW-REQUIRED prior research','Native ownership/copy/variability or failed acquisition boundary',head)
    for name in ('native-full.tsv','native-sites04.tsv','native-owner-copy04.tsv'):
        add(ROOT/'.local-work/resource-retained-population'/name,'LOCAL-ONLY native export','Read-only primary instruction/ABI/field evidence',head)
    for name in ('plugin.cpp','build.py'):
        add(ROOT/'runtime/beacon-resource-070'/name,'Maintainer-owned method','Conceptually adapted load/identity/build pattern under SOR-P-0002',head)
    for name in ('history.h','patch.h'):
        add(ROOT/'runtime/native-oracle-060'/name,'Maintainer-owned method','Inspected spool/relay/sole-thread/inert-wrapper designs; new implementation',head)
    for name in ('core.h','win_support.h'):
        add(ROOT/'runtime/exp0002'/name,'Maintainer-owned implementation','Reused unchanged Win32 hashing/file support and included core definitions',head)
    add(ROOT/'runtime/session-tools/export_review.py','Maintainer-owned method','Adapted exact byte patch-export method',head)
    add(ROOT/'research/resource-retained-population/prepare_native.py','Maintainer-owned implementation','Reused full_preservation offline method through protect.py',head)
    for name in ('src/plugin.cpp','src/event_buffer.h','src/population_lifecycle.cpp','build.ps1','dependency-pins.json','README.md'):
        add(sibling/'plugin/reference-observer'/name,'Maintainer-owned consultation','Inspected initialization/lifetime/buffering/build; CommonLib dependencies rejected',sibling_head)
    add(sibling/'docs/experiments/evidence/sfse-passive-reference-handle-observer/plugin-load-validation.json','Prior live receipt','Loader-only successful load; ordinary launch did not load SFSE',sibling_head)
    add(ROOT/'runtime/exp0002/third_party/sfse/PluginAPI.h','Approved MIT header','Unchanged interface compiled with explicit D5P extension','48535cc4306ab345252bf740c20a1c6194929b0e')
    add(ROOT/'runtime/exp0002/third_party/sfse/LICENSE.txt','MIT notice','Retained with deployment package','48535cc4306ab345252bf740c20a1c6194929b0e')
    for name in manifest['installed']:add(Path(name),'LOCAL-ONLY installed input','Fresh exact identity before/after native build','Installed; hash is identity')
    for name in ('sfse_loader.exe','sfse_1_16_244.dll'):
        add(GAME/name,'LOCAL-ONLY installed prerequisite','Read-only Phase B loader/runtime identity','Installed; hash is identity')
    add(Path(sys.executable),'Installed tool','CPython stdlib execution; not source incorporation','Installed; hash is identity')
    for line in (build/'compile.log').read_text(errors='replace').splitlines():
        p=Path(line.strip())
        if p.name.lower() in ('cl.exe','ml64.exe','link.exe') and p.is_file():
            add(p,'Installed tool','MSVC/MASM native build; versions in compile.log','Installed; hash is identity')
    for name in ('build.json','qualification.json','package.json','compile.log','reader-qualification.log','identity.generated.h'):
        if (build/name).exists():add(build/name,'LOCAL-ONLY final receipt','Exact build/qualification/deployment evidence','D5P final candidate')
    for p in sorted(SRC.iterdir()):
        if p.is_file():add(p,'Original task method','D5P source/build/reader/operations; held for independent review','Current uncommitted D5P')
    for label in ('protection-before','protection-after'):
        for name in ('protection.json','remaining-inputs.json'):
            p=LOCAL/label/name
            if p.exists():add(p,'LOCAL-ONLY protection receipt','Active archive-backed preservation and protected namespaces','D5P Phase A')
    target=ROOT/'docs/experiments/resource-retained-population/d5p-sources.csv'
    with target.open('w',encoding='utf8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=('id','path','sha256','kind','use','origin_revision'),lineterminator='\n');w.writeheader();w.writerows(rows)
    print('Pinned',len(rows),'D5P sources/receipts')


if __name__=='__main__':main()
