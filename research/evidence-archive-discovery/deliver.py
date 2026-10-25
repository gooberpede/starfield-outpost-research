# SPDX-License-Identifier: GPL-3.0-or-later
"""Prepare source records or export exact mixed-worktree review packages.

Reads initial byte snapshots, current text, receipts and Git only. Writes fresh
ignored records/diffs and new isolated scratch trees. No stage/commit/ref writes,
original payload rehash, save access, source cleanup or archive activation.
Owned diff/Git primitives are reused under SOR-P-0002.
"""
import argparse
import ast
import csv
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

import archive as a
from inventory import ROOT,LOCAL,DOC,write,csvout
sys.path.insert(0,str(ROOT/'runtime/session-tools'))
from export_review import diff,git

SHARED={'CREDITS.md','docs/RESEARCH_STATE.md','docs/SOURCES.md','docs/experiments/README.md','docs/implementation-briefs/README.md'}
BRIEF='docs/implementation-briefs/CODEX_BRIEF_SOR_consolidated_evidence_archival_stage_a.md'


def local_inventory():
    rows=[];stack=[LOCAL];reparse=[]
    while stack:
        folder=stack.pop()
        for entry in os.scandir(folder):
            path=Path(entry.path);s=path.lstat()
            if s.st_file_attributes&0x400:
                reparse.append(path.relative_to(ROOT).as_posix());continue
            if path.is_dir():stack.append(path)
            elif path.is_file():rows.append(dict(path=path.relative_to(ROOT).as_posix(),bytes=s.st_size))
    return rows,reparse


def prepare(label):
    if label and not re.fullmatch("[a-z0-9]+",label):raise ValueError("Fresh alphanumeric preparation label required")
    a.space(1024*1024*1024)
    start=json.loads((LOCAL/'start.json').read_text())
    refs=json.loads((LOCAL/'source-reference-pins03.json').read_text())
    checked=[]
    for row in refs:
        name=row['path'];path=LOCAL/'start-files'/name if name in start['files'] else ROOT/name
        if a.pin(path)!=row['sha256']:raise RuntimeError('Reference version changed: '+name)
        checked.append(row)
    sources=[]
    def add(path,role,basis='Current exact artifact identity'):
        path=Path(path)
        sources.append(dict(id=f'EAD-S{len(sources)+1:03d}',path=path.relative_to(ROOT).as_posix(),sha256=a.pin(path),role=role,basis=basis))
    add(ROOT/BRIEF,'Governing original brief','Initially supplied bytes, preserved')
    add(DOC/'scope-amendment.md','Accepted maintainer scope correction')
    for name in ('AGENTS.md','WORKFLOW.md','THIRD_PARTY_POLICY.md','docs/CHARTER.md','docs/EVIDENCE_STANDARD.md','docs/RESEARCH_EXECUTION_PROTOCOL.md','docs/SAVE_PROTECTION.md','docs/EDITORIAL_STANDARD.md','docs/PERMISSIONS.md','docs/PUBLICATION.md','docs/PROVENANCE.md','docs/templates/completion-contract.md','docs/reviewers/research-completion-reviewer.md'):
        add(ROOT/name,'Existing governing policy; unchanged input')
    for name in ('runtime/session-tools/archive.py','runtime/session-tools/export_review.py','runtime/session-tools/common.py','research/editorial/screen.py','research/preservation-verification/qualify.py'):
        add(ROOT/name,'Owned method consultation/reuse under SOR-P-0002')
    for name in ('start.json','inventory03.sqlite','inventory-summary03.json','source-reference-pins03.json','dependency-mentions03.json','expected-sample-pin-candidates03.json','scope-summary02.json','candidate-owners-scoped02.sqlite','reproduction-proof.json','benchmark01/freeze.json','benchmark01/setup.json','benchmark01/results.json','qualification11/freeze.json','qualification11/results.json','admission-tests.json','planning-model04.json','synthetic-scale04/result.json','cargo-pilot-summary04.json','cargo-pilot-scoped04.json'):
        add(LOCAL/name,'Local primary receipt/metadata; raw content remains LOCAL-ONLY')
    for path in sorted((LOCAL/'benchmark01/methods').glob('*.py')):
        add(path,'Exact executed benchmark method; historical timing binds this version')
    for path in sorted((ROOT/'research/evidence-archive-discovery').glob('*.py')):
        add(path,'Final authored method; later safety/scope changes separately qualified')
    # Actual non-save members were authenticated at intake and after the run.
    freeze=json.loads((LOCAL/'benchmark01/freeze.json').read_text())
    for row in freeze['samples']:
        if row['group']=='protected-save-copy':continue
        sources.append(dict(id=f'EAD-S{len(sources)+1:03d}',path=row['path'],sha256=row['sha256'],role='Actual non-save sample; original payload LOCAL-ONLY',basis='Prior expected identity matched during copy and final original reread; no new package-time payload read'))
    csvout('sources.csv',['id','path','sha256','role','basis'],sources)
    write(LOCAL/('preparation'+(label or '')+'.json'),dict(reference_versions_checked=len(checked),source_ledger_rows=len(sources),
        notes='Reference versions use captured before bytes for inherited modified text. No save payload access.',
        source_ledger_sha256=a.pin(DOC/'sources.csv'),free_bytes=a.space(),
        python=sys.version,python_sha256=a.pin(sys.executable),sqlite=__import__('sqlite3').sqlite_version,
        zstd=__import__('compression.zstd',fromlist=['zstd_version']).zstd_version,
        git=git('--version').decode().strip()))


def package(label):
    a.space(1024*1024*1024)
    start=json.loads((LOCAL/'start.json').read_text())
    assert git('rev-parse','HEAD').decode().strip()==start['head']
    assert a.pin(ROOT/'.git/index')==start['index_sha256']
    assert not git('diff','--cached','--name-only')
    out=LOCAL/label;out.mkdir(exist_ok=False)
    changed=git('diff','HEAD','--name-only','-z').decode().split('\0')[:-1]
    new=git('ls-files','--others','--exclude-standard','-z').decode().split('\0')[:-1]
    names=sorted(set(changed+new));current={n:(ROOT/n).read_bytes() for n in names}
    original={n:git('show','HEAD:'+n) if n in changed else None for n in names}
    before={n:(LOCAL/'start-files'/n).read_bytes() if n in start['files'] else original[n] for n in names}
    task=[n for n in names if current[n]!=before[n]]
    assert all(n in SHARED or n.startswith(('research/evidence-archive-discovery/','docs/experiments/evidence-archive-discovery/')) for n in task)
    for name,row in start['files'].items():
        if name not in SHARED:assert current[name]==before[name],name
    for name in SHARED:
        assert not any(line.startswith('-') and not line.startswith('---') for line in diff(name,before[name],current[name]).decode().splitlines()),('Prior authored text removed',name)
    for n in task:
        text=current[n].decode('utf8');assert '\r' not in text and not text.startswith('\ufeff'),n
        assert all(line.rstrip()==line for line in text.splitlines()),n
        if n.endswith('.py'):ast.parse(text,filename=n)
        if n.endswith('.md'):
            for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',text):
                link=target.split('#')[0].strip('<>')
                if link and not re.match('[A-Za-z]+:',link) and not (ROOT/n).parent.joinpath(link).resolve().exists():
                    assert target in (before[n] or b'').decode('utf8'),(n,target)
    git('diff','--check')
    screen=subprocess.run([sys.executable,'-B','research/editorial/screen.py','--changed'],cwd=ROOT,capture_output=True)
    (out/'editorial-screen.json').write_bytes(screen.stdout)
    (out/'editorial-stderr.txt').write_bytes(screen.stderr)
    if screen.returncode:raise RuntimeError('Editorial suspects; inspect preserved diagnostics')
    scratchroot=ROOT/'.local-work/review-patches';scratchroot.mkdir(exist_ok=True)
    patches={}
    for kind,paths,old in (('complete',names,original),('task-only',task,before)):
        payload=b''.join(diff(n,old[n],current[n]) for n in paths)
        target=ROOT/f'.local-work/diffs/archive-stage-a-{label}-{kind}.diff'
        with target.open('xb') as f:f.write(payload)
        assert re.findall(rb'^diff --git a/(.*?) b/',payload,re.M)==[n.encode() for n in paths]
        with tempfile.TemporaryDirectory(prefix='archive-stage-a-',dir=scratchroot) as temporary:
            tree=Path(temporary).resolve();assert tree.is_relative_to(scratchroot.resolve())
            for n in paths:
                if old[n] is not None:
                    p=tree/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(old[n])
            git('apply','--no-index','--check','--whitespace=nowarn',str(target),cwd=tree)
            git('apply','--no-index','--whitespace=nowarn',str(target),cwd=tree)
            assert all((tree/n).read_bytes()==current[n] for n in paths)
            assert sorted(p.relative_to(tree).as_posix() for p in tree.rglob('*') if p.is_file())==paths
            git('apply','--no-index','--reverse','--check',str(target),cwd=tree)
            git('apply','--no-index','--reverse',str(target),cwd=tree)
            assert all((tree/n).read_bytes()==old[n] if old[n] is not None else not (tree/n).exists() for n in paths)
        git('apply','--reverse','--check','--whitespace=nowarn',str(target))
        patches[kind]=dict(path=str(target),sha256=a.pin(target),bytes=len(payload),paths=paths,forward_reverse_exact=True,actual_tree_reverse=True)
    inventory,reparse=local_inventory()
    write(out/'exclusions.json',dict(task_local=inventory,reparse_test_nodes_not_followed=reparse,
        inherited_inventory='.local-work/evidence-archive-discovery/inventory03.sqlite',
        inherited_inventory_sha256=a.pin(LOCAL/'inventory03.sqlite'),
        reasons='All private/raw/binary/save/container/prototype/index/diagnostic data excluded; metadata/known receipt identities used without rehashing saved payloads',
        additional='Installed content, analysis databases, active saves and unrelated local data remain outside task writes/exports',
        later_records='This snapshot directory and later review/closure outputs are bound by final delivery',publication_clearance=False))
    files=[dict(path=n,bytes=len(current[n]),sha256=hashlib.sha256(current[n]).hexdigest(),scope='Stage A authored/changed' if n in task else 'Prior uncommitted or supplied brief, unchanged by Stage A') for n in names]
    write(out/'changed-files.json',files)
    (out/'git-status-short.txt').write_bytes(git('status','--short','--untracked-files=all'))
    write(out/'snapshot.json',dict(head=start['head'],index_sha256=start['index_sha256'],files=files,task_paths=task,patches=patches,
        task_retained_logical_bytes=sum(r['bytes'] for r in inventory),temporary_peak_bound_bytes=sum(r['bytes'] for r in inventory)+512*1024*1024,
        peak_method='Retained logical total plus bounded transient index/journal margin, not instrumented physical peak',
        free_bytes=a.space(),actual_recovery_bytes=0,no_original_data_move_or_delete=True,
        current_method_sha256={p.name:a.pin(p) for p in (ROOT/'research/evidence-archive-discovery').glob('*.py')}))
    assert a.pin(ROOT/'.git/index')==start['index_sha256']
    assert git('rev-parse','HEAD').decode().strip()==start['head']
    assert all(a.pin(ROOT/n)==hashlib.sha256(data).hexdigest() for n,data in current.items())
    print(json.dumps(dict(snapshot=str(out/'snapshot.json'),snapshot_sha256=a.pin(out/'snapshot.json'),complete_files=len(names),task_files=len(task),patches={k:dict(path=v['path'],sha256=v['sha256']) for k,v in patches.items()}),indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--prepare',action='store_true');parser.add_argument('--label');args=parser.parse_args()
    if args.prepare:prepare(args.label)
    else:
        if not args.label or not re.fullmatch('[a-z0-9]+',args.label):parser.error('Fresh lowercase alphanumeric label required')
        package(args.label)
