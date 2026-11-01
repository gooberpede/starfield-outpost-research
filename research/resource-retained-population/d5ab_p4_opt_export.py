# SPDX-License-Identifier: GPL-3.0-or-later
"""Export exact reopened P4 optimization task/complete patches and verify byte applicability.

Adapted from owned d5ab_p4_export.py; origin SHA-256 d691695b73677e0f92f7568b5baa78a612c8df1f34a6e86b7c394e56b929aa41.
Prior lineage is retained in that source.
Reads HEAD/index, tracked/untracked task text and evidence links. Writes only
ignored diffs/manifests and disposable application trees below .local-work.
No staging, game, network, target, save or analysis-database effects.
"""

import sys

# Safety checks below require assertions, including when imported as a helper.
if not __debug__ or sys.flags.optimize != 0:
    raise RuntimeError('Python optimization is forbidden; invoke with -E -B and no -O/-OO')
import difflib
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

ROOT=Path(__file__).resolve().parents[2]
P3_EXPORT_ORIGIN_SHA256='5554f1d464eabc917c0fb4077a1e0206c49354b995f4d2df7c07f09add10b53d'
BRIEF='docs/implementation-briefs/CODEX_BRIEF_SOR_RG2_D5AB_P4_final_readiness_B2_preparation.md'
ENV=dict(os.environ,GIT_OPTIONAL_LOCKS='0',GIT_CEILING_DIRECTORIES=str(ROOT/'.local-work'))


def sha(data):return hashlib.sha256(data).hexdigest()


def git(*args,cwd=ROOT):
    r=subprocess.run(['git','-c','core.autocrlf=false',*args],cwd=cwd,env=ENV,capture_output=True)
    if r.returncode:raise RuntimeError((args,r.stderr.decode(errors='replace')))
    return r.stdout


def diff(name,old,new):
    parts=['diff --git a/'+name+' b/'+name+'\n']
    if old is None:parts.append('new file mode 100644\n')
    if new is None:parts.append('deleted file mode 100644\n')
    for line in difflib.unified_diff((old or b'').decode('utf8').splitlines(keepends=True),
                                    (new or b'').decode('utf8').splitlines(keepends=True),
                                    fromfile='/dev/null' if old is None else 'a/'+name,
                                    tofile='/dev/null' if new is None else 'b/'+name,lineterm='\n'):
        parts.append(line if line.endswith('\n') else line+'\n\\ No newline at end of file\n')
    return ''.join(parts).encode('utf8')


def main():
    label=sys.argv[1];assert re.fullmatch('[a-z0-9-]+',label)
    out=ROOT/'.local-work/d5ab/p4-opt-delivery'/label;out.mkdir(parents=True,exist_ok=False)
    head=git('rev-parse','HEAD').decode().strip();index=sha((ROOT/'.git/index').read_bytes())
    initial=json.loads((ROOT/'.local-work/d5ab/p4-opt/baseline.json').read_text(encoding='utf8'))
    assert head==initial['head'] and index==initial['index_sha256'], 'External Git baseline change; requalify delivery before export'
    assert not git('diff','--cached','--name-only')
    changed=git('diff','HEAD','--name-only','-z').decode().split('\0')[:-1]
    untracked=git('ls-files','--others','--exclude-standard','-z').decode().split('\0')[:-1]
    names=sorted(set(changed+untracked));task=[n for n in names if n!=BRIEF]
    assert all(n in (BRIEF,'CREDITS.md','docs/SOURCES.md','docs/RESEARCH_STATE.md','docs/implementation-briefs/README.md') or n.startswith('research/resource-retained-population/d5ab_p4_') or n.startswith('docs/experiments/resource-retained-population/d5ab-p4-') or n.startswith('runtime/construction-winner/') or n.startswith('runtime/session-tools/') or n in ('runtime/retained-population/protect.py','research/resource-carinae-source-context/save_policy.py','research/resource-retained-population/prepare_native.py') or n == 'docs/experiments/resource-retained-population/run-card-d5x-b2.md' for n in names)
    before={n:git('show','HEAD:'+n) if n in changed else None for n in names}
    current={n:(ROOT/n).read_bytes() if (ROOT/n).exists() else None for n in names}
    links=[]
    for n in task:
        text=(current[n] or b'').decode('utf8');assert not text.startswith('\ufeff') and '\r' not in text,n
        if n in untracked:assert all(s.rstrip()==s for s in text.splitlines()),n
        if n.endswith('.md'):
            for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',text):
                path=target.split('#')[0].strip('<>')
                if not path or re.match('[A-Za-z]+:',path):continue
                exists=(ROOT/n).parent.joinpath(path).resolve().exists()
                if not exists:assert target in (before[n] or b'').decode('utf8'),(n,target)
                links.append(dict(file=n,target=target,exists=exists))
    git('diff','--check')
    patches={}
    scratch_parent=ROOT/'.local-work/review-patches';scratch_parent.mkdir(exist_ok=True)
    for coverage,paths in (('task-only',task),('complete',names)):
        payload=b''.join(diff(n,before[n],current[n]) for n in paths)
        assert [n.decode() for n in re.findall(rb'^diff --git a/(.*?) b/',payload,re.M)]==paths
        patch=ROOT/'.local-work/diffs'/('d5ab-p4-opt-'+coverage+'.diff');patch.parent.mkdir(exist_ok=True)
        (out/('d5ab-p4-opt-'+coverage+'.diff')).write_bytes(payload)
        with patch.open('wb') as f:f.write(payload)
        with tempfile.TemporaryDirectory(prefix='d5ab-p4-opt-',dir=scratch_parent) as directory:
            scratch=Path(directory)
            for n in paths:
                if before[n] is not None:
                    p=scratch/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(before[n])
            git('apply','--check',str(patch),cwd=scratch);git('apply',str(patch),cwd=scratch)
            assert all(((scratch/n).read_bytes() if (scratch/n).exists() else None)==current[n] for n in paths)
            git('apply','--reverse','--check',str(patch),cwd=scratch);git('apply','--reverse',str(patch),cwd=scratch)
            assert all(((scratch/n).read_bytes() if (scratch/n).exists() else None)==before[n] for n in paths)
        git('apply','--reverse','--check',str(patch))
        patches[coverage]=dict(path=str(patch),sha256=sha(payload),files=len(paths),forward_reverse_bytes='PASS')
    manifest={n:dict(sha256=sha(current[n]) if current[n] is not None else None,
                     bytes=len(current[n]) if current[n] is not None else 0,
                     kind='supplied brief' if n==BRIEF else 'new authored text' if n in untracked else 'modified authored text') for n in names}
    status=git('status','--short').decode();(out/'status.txt').write_text(status,encoding='utf8',newline='\n')
    excluded=[]
    for parent in (ROOT/'.local-work/d5x',ROOT/'.local-work/d5ab',ROOT/'.local-work/d5p'):
        for directory in sorted(list(parent.glob('p4-*'))+list(parent.glob('d5ab-p4-*'))+([parent/'p4'] if (parent/'p4').exists() else [])):
            if directory.name not in ('p4-delivery','p4-opt-delivery'):
                candidates=sorted(directory.rglob('*')) if directory.is_dir() else [directory]
                for path in candidates:
                    if path.is_file():
                        try:data=path.read_bytes()
                        except OSError as error:raise RuntimeError('Excluded artifact is not readable: '+str(path)) from error
                        excluded.append(dict(path=str(path.relative_to(ROOT)),bytes=len(data),sha256=sha(data),classification='LOCAL-ONLY'))
    (out/'exclusions.json').write_text(json.dumps(excluded,indent=2)+'\n',encoding='utf8',newline='\n')
    result=dict(head=head,index_sha256=index,files=manifest,patches=patches,links=links,
                exclusion_manifest=dict(path=str(out/'exclusions.json'),sha256=sha((out/'exclusions.json').read_bytes()),files=len(excluded)),
                exclusions=['Ignored P4 disposable builds, synthetic captures, diagnostic receipts, specialist/reviewer returns and source snapshots under .local-work/d5x/p4-* and .local-work/d5ab/p4-*',
                            'Installed binaries/assets, original saves, static-analysis exports/databases and unrelated historical raw evidence'],
                checks=dict(path_inventory='PASS',new_text_whitespace='PASS',git_diff_check='PASS',internal_paths='PASS'))
    (out/'delivery.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf8',newline='\n')
    assert index==sha((ROOT/'.git/index').read_bytes()) and head==git('rev-parse','HEAD').decode().strip()
    print(json.dumps(dict(out=str(out),files=len(names),patches=patches),indent=2))


if __name__=='__main__':main()
