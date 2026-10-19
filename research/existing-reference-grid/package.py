"""SPDX-License-Identifier: GPL-3.0-or-later
Local review exporter. Reads Git without optional locks and the working tree;
writes ignored receipts/diffs and disposable plain .local-work/review-patches apply trees only.
No index/ref/staging/network mutation. Stdlib only; C:/D: 40GB guard.
Run --baseline before tracked edits; run without arguments after verification.
"""
import json
import csv
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'.local-work/existing-reference-grid'
sys.path.insert(0,str(ROOT/'save-analysis/scripts'))
from verify_position_v2 import guard,digest


def git(*args,cwd=ROOT):
    r=subprocess.run(['git','-c','core.autocrlf=false',*args],cwd=cwd,
        env=dict(os.environ,GIT_OPTIONAL_LOCKS='0', GIT_CEILING_DIRECTORIES=str(ROOT/'.local-work')),capture_output=True)
    if r.returncode not in (0,1): raise RuntimeError(r.stderr.decode())
    return r


def names(*args):
    return git(*args,'-z').stdout.decode().split('\0')[:-1]


def main():
    space=guard(); OUT.mkdir(exist_ok=True)
    if '--baseline' in sys.argv:
        assert not names('diff','HEAD','--name-only'), 'TRACKED_EDITS_ALREADY_PRESENT'
        files=names('ls-files')
        baseline=dict(head=git('rev-parse','HEAD').stdout.decode().strip(),index=digest(ROOT/'.git/index'),
            status=git('status','--short').stdout.decode(),files={n:digest(ROOT/n) for n in files},
            supplied_brief='docs/implementation-briefs/CODEX_BRIEF_SOR_existing_reference_grid_oracle_integrated.md')
        (OUT/'baseline.json').write_text(json.dumps(baseline,indent=2)+'\n',encoding='utf8',newline='\n')
        return
    base=json.loads((OUT/'baseline.json').read_text())
    assert git('rev-parse','HEAD').stdout.decode().strip()==base['head']
    assert digest(ROOT/'.git/index')==base['index']
    changed=names('diff','HEAD','--name-only'); new=names('ls-files','--others','--exclude-standard')
    allfiles=sorted(changed+new); task=[n for n in allfiles if n!=base['supplied_brief']]
    assert all(digest(ROOT/n)==h for n,h in base['files'].items() if n not in changed)
    links=0
    for n in task:
        b=(ROOT/n).read_bytes(); s=b.decode('utf8')
        assert not b.startswith(b'\xef\xbb\xbf') and b'\r' not in b,n
        assert all(line.rstrip()==line for line in s.splitlines()),n
        if n.endswith('.md'):
            for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',s):
                target=target.split('#')[0].strip('<>')
                if not target or re.match(r'[A-Za-z]+:',target): continue
                assert (ROOT/n).parent.joinpath(target).resolve().exists(),(n,target)
                links+=1
    assert git('diff','HEAD','--check').returncode==0
    patches={}
    for label,files in [('complete',allfiles),('task-only',task)]:
        data=git('diff','HEAD','--',*[n for n in files if n in changed]).stdout if changed else b''
        for n in files:
            if n in new: data+=git('diff','--no-index','--','/dev/null',n).stdout
        path=ROOT/f'.local-work/diffs/existing-reference-grid-{label}.diff';path.write_bytes(data)
        assert sorted(x.decode().rstrip('\r') for x in re.findall(rb'^\+\+\+ b/(.+)$',data,re.M))==files
        review_scratch = ROOT / '.local-work/review-patches'
        review_scratch.mkdir(parents=True, exist_ok=True)
        scratch=Path(tempfile.mkdtemp(prefix='sor-existing-grid-',dir=review_scratch))
        for n in files:
            if n in changed:
                dest=scratch/n;dest.parent.mkdir(parents=True,exist_ok=True)
                dest.write_bytes(git('show',f'HEAD:{n}').stdout)
        # Preserve supplied brief's three existing Markdown hard-break spaces.
        # Task-authored whitespace was checked above; never rewrite the input.
        whitespace='nowarn' if label=='complete' else 'error'
        for args in [('apply','--no-index','--check','--whitespace='+whitespace,str(path)),
                     ('apply','--no-index','--whitespace='+whitespace,str(path))]:
            r=git(*args,cwd=scratch);assert r.returncode==0,r.stderr.decode()
        assert all((scratch/n).read_bytes()==(ROOT/n).read_bytes() for n in files)
        patches[label]=dict(path=str(path),sha256=digest(path),paths=files,scratch=str(scratch),forward_exact=True)
    manifest=[dict(path=n,bytes=(ROOT/n).stat().st_size,sha256=digest(ROOT/n),
        role='supplied brief' if n==base['supplied_brief'] else 'task authored') for n in allfiles]
    receipts=[OUT/'release-lock-05.json', OUT/'qualification-receipt.json']
    exclusions=[dict(path='.local-work/',reason='Ignored raw saves/captures/static exports, receipts and review snapshots; local only'),
        dict(path='D:/ReverseEngineering; D:/tools; .local-work/review-patches',reason='Analysis databases/tool binaries/disposable patch trees excluded'),
        dict(path='game/Vortex/save directories',reason='Protected originals; no live/configuration/save writes')]
    package=dict(head=base['head'],index=base['index'],disk=space,files=manifest,patches=patches,
        exclusions=exclusions,links=links,
        receipts={str(p):digest(p) for p in receipts})
    (OUT/'package.json').write_text(json.dumps(package,indent=2)+'\n',encoding='utf8',newline='\n')
    (OUT/'exclusions.json').write_text(json.dumps(exclusions,indent=2)+'\n',encoding='utf8',newline='\n')
    (OUT/'status.txt').write_bytes(git('status','--short').stdout)
    assert digest(ROOT/'.git/index')==base['index']
    print(json.dumps(dict(package_sha256=digest(OUT/'package.json'),files=len(manifest),links=links,patches=patches)))


if __name__=='__main__': main()
