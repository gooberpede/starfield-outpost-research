# SPDX-License-Identifier: GPL-3.0-or-later
"""Export exact unstaged review text and audit selected preservation pins.

Project-owned predecessor package.py informs the patch/check method. Reads
HEAD/index/worktree, preservation-before.json and task evidence; writes ignored
JSON/status/diffs and disposable temporary apply trees. No native execution,
network, staging, ref mutation, target or protected-input writes.
"""
import difflib
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'.local-work/x87-preservation'
BRIEF='docs/implementation-briefs/CODEX_BRIEF_SOR_experiment_A_x87_state_preservation.md'


def git(*args,cwd=ROOT):
    result=subprocess.run(['git','-c','core.autocrlf=false',*args],cwd=cwd,
                          env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'),capture_output=True)
    if result.returncode: raise RuntimeError((args,result.stderr.decode(errors='replace')))
    return result.stdout


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream,'sha256').hexdigest()


def write(name,value):
    (OUT/name).write_text(json.dumps(value,indent=2)+'\n',encoding='utf8',newline='\n')


def patch(path,old,new):
    result=['diff --git a/'+path+' b/'+path+'\n']
    if old is None:result.append('new file mode 100644\n')
    if new is None:result.append('deleted file mode 100644\n')
    for line in difflib.unified_diff((old or b'').decode().splitlines(keepends=True),
                                    (new or b'').decode().splitlines(keepends=True),
                                    fromfile='/dev/null' if old is None else 'a/'+path,
                                    tofile='/dev/null' if new is None else 'b/'+path,lineterm='\n'):
        result.append(line if line.endswith('\n') else line+'\n\\ No newline at end of file\n')
    return ''.join(result).encode()


def main():
    baseline=json.loads((OUT/'preservation-before.json').read_text())
    assert git('rev-parse','HEAD').decode().strip()==baseline['head']
    disks={d:shutil.disk_usage(d).free for d in ('C:/','D:/')}
    assert all(n>=40_000_000_000 for n in disks.values())
    rows=[dict(row,actual=sha(row['path'])) for row in baseline['pins']]
    assert all(row['actual']==row['sha256'] for row in rows), 'PROTECTED_INPUT_MISMATCH'
    write('preservation-after.json',dict(head=baseline['head'],pins=rows,all_equal=True,
                                         scope=baseline['scope'],disk=disks))
    changed=git('diff','HEAD','--name-only','-z').decode().split('\0')[:-1]
    new=git('ls-files','--others','--exclude-standard','-z').decode().split('\0')[:-1]
    names=sorted(set(changed+new)); assert BRIEF in new
    task=[n for n in names if n!=BRIEF]
    current={n:(ROOT/n).read_bytes() if (ROOT/n).exists() else None for n in names}
    old={n:git('show','HEAD:'+n) if n in changed else None for n in names}
    links=0
    for name in task:
        text=current[name].decode('utf8')
        assert not text.startswith('\ufeff') and '\r' not in text,name
        added=text if name in new else '\n'.join(line[1:] for line in git('diff','--',name).decode().splitlines()
                                                  if line.startswith('+') and not line.startswith('+++'))
        assert all(line==line.rstrip() for line in added.splitlines()),name
        if name.endswith('.md'):
            for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',added):
                path=target.split('#')[0].strip('<>')
                if not path or re.match(r'^[A-Za-z]+:',path):continue
                assert (ROOT/name).parent.joinpath(path).resolve().exists(),(name,target)
                links+=1
    git('diff','--check')
    patches={}
    for kind,paths in [('task-only',task),('complete',names)]:
        target=ROOT/f'.local-work/diffs/x87-preservation-{kind}.diff'
        target.parent.mkdir(exist_ok=True)
        data=b''.join(patch(n,old[n],current[n]) for n in paths)
        target.write_bytes(data)
        assert re.findall(r'^diff --git a/(.*?) b/.*$',data.decode(),re.M)==paths
        with tempfile.TemporaryDirectory(prefix='sor-x87-review-') as directory:
            tree=Path(directory)
            for name in paths:
                if old[name] is not None:
                    (tree/name).parent.mkdir(parents=True,exist_ok=True)
                    (tree/name).write_bytes(old[name])
            git('apply','--check',str(target),cwd=tree)
            git('apply',str(target),cwd=tree)
            assert all((tree/n).read_bytes()==current[n] for n in paths)
            git('apply','--check','--reverse',str(target),cwd=tree)
            git('apply','--reverse',str(target),cwd=tree)
            assert all((tree/n).read_bytes()==old[n] if old[n] is not None else not (tree/n).exists() for n in paths)
        patches[kind]=dict(path=str(target),sha256=sha(target),bytes=len(data),paths=paths,exact_forward_reverse=True)
    def inventory(paths):
        return [dict(path=n,sha256=sha(ROOT/n),bytes=len(current[n]),kind='new text' if n in new else 'modified text') for n in paths]
    write('changed-files.json',inventory(task))
    write('complete-files.json',inventory(names))
    write('exclusions.json',dict(scope='All nonignored changed text included; ignored local evidence excluded',
          supplied_brief_complete_only=BRIEF,binary_changed_files=[],
          excluded=['.local-work/x87-preservation/ raw synthetic states, geometry, generated sources, binaries and receipts',
                    '.local-work/diffs/ review patches','All pre-existing protected local-only material']))
    (OUT/'git-status-short.txt').write_bytes(git('status','--short'))
    evidence={str(p.relative_to(OUT)):dict(sha256=sha(p),bytes=p.stat().st_size) for p in OUT.rglob('*')
              if p.is_file() and (p.relative_to(OUT).parts[0].startswith(('diagnostic-','corrected-'))
                                 or p.name in ('preservation-before.json','regression.json'))}
    write('evidence-files.json',evidence)
    write('verification.json',dict(selected_pins=len(rows),all_equal=True,links_checked=links,
          whitespace='PASS',utf8_lf='PASS',patch_inventory_and_content='PASS',
          exact_forward_reverse='PASS',prose='Manual implementer and independent reviewer inspection required',
          native_spatial_equivalence='NOT TESTED',retail_safety='NOT TESTED'))
    write('package.json',dict(head=baseline['head'],index_sha256=sha(ROOT/'.git/index'),
          task_files=inventory(task),complete_files=inventory(names),patches=patches,
          evidence_manifest_sha256=sha(OUT/'evidence-files.json'),
          verification_sha256=sha(OUT/'verification.json'),preservation_sha256=sha(OUT/'preservation-after.json')))
    (OUT/'package.sha256').write_text(sha(OUT/'package.json')+'  package.json\n',encoding='utf8',newline='\n')
    print(json.dumps(dict(task_files=len(task),complete_files=len(names),pins=len(rows),links=links,
                          package_sha256=sha(OUT/'package.json'))))


if __name__=='__main__':main()
