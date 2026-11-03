# SPDX-License-Identifier: GPL-3.0-or-later
"""Export byte-exact D5AL live Episode B review packages without staging.

SOR-P-0002: owned runtime/retained-population/export_review.py diff/apply method.
Reads baseline, Git HEAD/index, changed text and ignored evidence. Writes fresh
ignored patches/manifests and retained standalone apply trees. No game, save,
database, network, index/ref or unrelated source mutation. Stdlib and Git only.
Refuse scope drift, nontext patch inputs, byte mismatch or protected-state drift.
"""
import sys
import os
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):
    raise RuntimeError('Use pinned Python -E -B')

import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

from d5ad_baseline import guard, sha

ROOT = Path(__file__).resolve().parents[2]
ENV = dict(os.environ,GIT_OPTIONAL_LOCKS='0',GIT_CEILING_DIRECTORIES=str(ROOT/'.local-work'))
SPEC = importlib.util.spec_from_file_location('owned_review_diff',ROOT/'runtime/retained-population/export_review.py')
DIFF = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(DIFF)


def git(*args,cwd=ROOT):
    result=subprocess.run(['git','-c','core.autocrlf=false',*args],cwd=cwd,env=ENV,capture_output=True)
    if result.returncode:
        raise RuntimeError((args,result.stderr.decode(errors='replace')))
    return result.stdout


def main():
    if not __debug__ or sys.flags.optimize:
        raise RuntimeError('Use Python -E -B')
    label=sys.argv[1]
    if not re.fullmatch('[a-z0-9-]+',label):
        raise ValueError('Bounded label required')
    guard()
    out=ROOT/'.local-work/d5al/b-live01-finalization'/label
    out.parent.mkdir(exist_ok=True)
    out.mkdir(exist_ok=False)
    baseline=json.loads((ROOT/'.local-work/d5al/b-live01/baseline.json').read_bytes())
    if git('rev-parse','HEAD').decode().strip()!=baseline['head'] or sha(ROOT/'.git/index')!=baseline['index_sha256']:
        raise ValueError('HEAD/index changed')
    changed=git('diff','HEAD','--name-only','-z').decode().split('\0')[:-1]
    untracked=git('ls-files','--others','--exclude-standard','-z').decode().split('\0')[:-1]
    names=sorted(set(changed+untracked))
    current={n:(ROOT/n).read_bytes() if (ROOT/n).is_file() else None for n in names}
    before={n:git('show','HEAD:'+n) if n in changed else None for n in names}
    start={n:((ROOT/'.local-work/d5al/b-live01/baseline-tree'/n).read_bytes()
              if not baseline['files'][n].get('deleted') else None)
           if n in baseline['files'] else before[n] for n in names}
    task=sorted(n for n in names if current[n]!=start[n])
    allowed={'CREDITS.md','docs/SOURCES.md','docs/RESEARCH_STATE.md',
             'docs/implementation-briefs/README.md',
             'docs/implementation-briefs/CODEX_AMENDMENT_SOR_D5AL_EPISODE_B_live_2026-11-03.md',
             'docs/experiments/resource-retained-population/resource-generation-gameplay-checklist.md'}
    for n in task:
        if n not in allowed and not n.startswith(('docs/experiments/resource-retained-population/d5al-b-',
                         'docs/experiments/resource-retained-population/run-card-d5al-',
                         'research/resource-retained-population/d5al_b_')):
            raise ValueError('Unattributable change: '+n)
    links=[]
    for n in names:
        text=(current[n] or b'').decode('utf8')
        if n in task:
            if text.startswith('\ufeff') or '\r' in text:
                raise ValueError('Authored encoding: '+n)
            if any(line.rstrip()!=line for line in text.splitlines()):
                raise ValueError('Task whitespace: '+n)
        if n.endswith('.md'):
            for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',text):
                path=target.split('#')[0].strip('<>')
                if not path or re.match('[A-Za-z]+:',path):
                    continue
                exists=(ROOT/n).parent.joinpath(path).resolve().exists()
                if not exists and n in task and target not in (start[n] or b'').decode('utf8'):
                    raise ValueError('New broken local link: '+n+' '+target)
                links.append(dict(file=n,target=target,exists=exists))
    git('diff','--check')
    patchdir=ROOT/'.local-work/diffs';patchdir.mkdir(exist_ok=True)
    parent=ROOT/'.local-work/review-patches';parent.mkdir(exist_ok=True)
    patches={}
    for coverage,paths,old in [('task-only',task,start),('complete',names,before)]:
        payload=b''.join(DIFF.diff(n,old[n],current[n]) for n in paths)
        if [n.decode() for n in re.findall(rb'^diff --git a/(.*?) b/',payload,re.M)]!=paths:
            raise ValueError('Patch path coverage')
        patch=patchdir/f'd5al-b-{label}-{coverage}.diff'
        with patch.open('xb') as stream:
            stream.write(payload)
        scratch=Path(tempfile.mkdtemp(prefix='d5al-b-'+coverage+'-',dir=parent)).resolve()
        if not scratch.is_relative_to(parent.resolve()):
            raise ValueError('Scratch root')
        for n in paths:
            if old[n] is not None:
                p=scratch/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(old[n])
        git('apply','--check',str(patch),cwd=scratch)
        git('apply',str(patch),cwd=scratch)
        if any(((scratch/n).read_bytes() if (scratch/n).exists() else None)!=current[n] for n in paths):
            raise ValueError('Forward patch bytes')
        git('apply','--reverse','--check',str(patch),cwd=scratch)
        git('apply','--reverse',str(patch),cwd=scratch)
        if any(((scratch/n).read_bytes() if (scratch/n).exists() else None)!=old[n] for n in paths):
            raise ValueError('Reverse patch bytes')
        patches[coverage]=dict(path=str(patch),sha256=sha(patch),paths=paths,
                               forward_reverse_exact_bytes=True,scratch=str(scratch))
    manifest={n:dict(sha256=sha(ROOT/n) if current[n] is not None else None,
                     bytes=len(current[n] or b''),task_authored=n in task,
                     prior_uncommitted=n in baseline['files'],
                     supplied_brief=bool(baseline['files'].get(n, {}).get('supplied_brief', False))) for n in names}
    exclusions=[]
    # Baseline copies duplicate repository bytes; their full inventory is in
    # baseline.json. All other task-local raw/export/control files are pinned.
    local_files = [p for folder in ('b-live01', 'b-live01-archive', 'b-live01-finalization')
                   for p in (ROOT/'.local-work/d5al'/folder).rglob('*')]
    for p in sorted(local_files):
        if not p.is_file() or 'baseline-tree' in p.parts or out in p.parents:
            continue
        exclusions.append(dict(path=p.relative_to(ROOT).as_posix(),bytes=p.stat().st_size,
                               sha256=sha(p),classification='LOCAL-ONLY; excluded from patches'))
    status=git('status','--short','--untracked-files=all').decode()
    (out/'status.txt').write_text(status,encoding='utf8',newline='\n')
    result=dict(head=baseline['head'],index_sha256=baseline['index_sha256'],files=manifest,
                patches=patches,links=links,exclusions=exclusions,baseline_copies='.local-work/d5al/b-live01/baseline.json',
                other_exclusions='Original D5AI/D5AJ/D5AK/D5AL history, saves, installed proprietary inputs and databases remain local and unchanged. The stopped B raw session and all 107 payloads are pinned by .local-work/d5al/b-live01-archive/seal.json; immutable A0 is pinned by original D5AL baseline01 manifest. All new B private companions, archive and finalization receipts are individually excluded and hashed. Fresh export directory is excluded to avoid recursion; only authored eligible text appears in patches.',
                checks=dict(git_diff_check='PASS',inventory='PASS',forward_reverse_exact_bytes='PASS',
                            task_encoding_whitespace='PASS',new_local_links='PASS'),method_sha256=sha(__file__))
    (out/'delivery.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf8',newline='\n')
    if git('rev-parse','HEAD').decode().strip()!=baseline['head'] or sha(ROOT/'.git/index')!=baseline['index_sha256']:
        raise ValueError('HEAD/index drift during export')
    print(json.dumps(dict(directory=str(out),task_files=len(task),complete_files=len(names),patches=patches)))


if __name__=='__main__':
    main()
