# SPDX-License-Identifier: GPL-3.0-or-later
# Adapted owned package helper: HEAD153466e, .local-work/workshop-population-rework/package.py.
"""Original review exporter. Reads HEAD/index and authored UTF8 tree; creates
exclusive ignored patches/manifests and disposable D:/tools apply trees. No
workspace apply, index/ref changes, staging, commit, push or network."""
from pathlib import Path
import subprocess,json,hashlib,os,tempfile,difflib,re,argparse
root=Path.cwd();base=root/'.local-work/continuous-beacon-preview';ap=argparse.ArgumentParser();ap.add_argument('--run',required=True);args=ap.parse_args();assert re.fullmatch('[a-zA-Z0-9-]+',args.run)
seed=json.loads((base/'baseline.json').read_text(encoding='utf8'));env=dict(os.environ,GIT_OPTIONAL_LOCKS='0')
def sha(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def git(*args,cwd=root):
 r=subprocess.run(['git','-c','core.autocrlf=false',*args],cwd=cwd,env=env,capture_output=True)
 if r.returncode:raise RuntimeError((args,r.returncode,r.stderr.decode(errors='replace')))
 return r.stdout
assert git('rev-parse','HEAD').decode().strip()==seed['head'];assert sha(root/'.git/index')==seed['index']['sha256'];assert not git('diff','--cached','--name-only')
changed=git('diff','HEAD','--name-only','-z').decode().split('\0')[:-1];new=git('ls-files','--others','--exclude-standard','-z').decode().split('\0')[:-1];names=sorted(set(changed+new))
before={Path(r['path']).relative_to(root).as_posix():base/'baseline-tree'/Path(r['path']).relative_to(root) for r in seed['files']}
def head(n):
 return git('show','HEAD:'+n) if n in changed else b''
original={n:head(n) for n in names};taskbase={n:before[n].read_bytes() if n in before else original[n] for n in names};current={n:(root/n).read_bytes() for n in names}
task=[n for n in names if current[n]!=taskbase[n]];checks=dict(links=0,existing_link_failures=[],whitespace=True)
for n in names:
 text=current[n].decode('utf8')
 if n in task and n not in before and n in new:
  assert not text.startswith('\ufeff'),n
  assert all(line.rstrip()==line for line in text.splitlines()),n
 if n in task and n.endswith('.md'):
  prior=taskbase[n].decode('utf8')
  for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',text):
   file=target.split('#')[0].strip('<>')
   if file and not re.match(r'[A-Za-z]+:',file):
    if not (root/n).parent.joinpath(file).resolve().exists():
     if target in prior:checks['existing_link_failures'].append([n,target])
     else:raise ValueError(('NEW_LINK_MISSING',n,target))
    checks['links']+=1
git('diff','--check')
def diff(n,old,new):
 if old==new:return b''
 headers='diff --git a/'+n+' b/'+n+'\n'+('new file mode 100644\n' if not old else '')
 lines=difflib.unified_diff(old.decode('utf8').splitlines(keepends=True),new.decode('utf8').splitlines(keepends=True),fromfile='a/'+n if old else '/dev/null',tofile='b/'+n,lineterm='\n')
 parts=[headers]
 for line in lines:
  parts.append(line if line.endswith('\n') else line+'\n\\ No newline at end of file\n')
 return ''.join(parts).encode('utf8')
patches={}
for label,paths,oldset in [('complete',names,original),('task-only',task,taskbase)]:
 data=b''.join(diff(n,oldset[n],current[n]) for n in paths);path=root/('.local-work/diffs/continuous-beacon-preview-'+label+'-'+args.run+'.diff');path.parent.mkdir(exist_ok=True)
 with path.open('xb') as f:f.write(data)
 scratch=Path(tempfile.mkdtemp(prefix='sor-preview-'+label+'-',dir='D:/tools'))
 for n in paths:
  if oldset[n]:
   p=scratch/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(oldset[n])
 git('apply','--no-index','--whitespace=nowarn','--check',str(path),cwd=scratch)
 git('apply','--no-index','--whitespace=nowarn',str(path),cwd=scratch)
 assert all((scratch/n).read_bytes()==current[n] for n in paths)
 git('apply','--no-index','--reverse','--check',str(path),cwd=scratch)
 git('apply','--no-index','--reverse',str(path),cwd=scratch)
 assert all((scratch/n).read_bytes()==oldset[n] if oldset[n] else not (scratch/n).exists() for n in paths)
 patches[label]=dict(path=str(path),sha256=sha(path),bytes=len(data),paths=paths,scratch=str(scratch),forward_check=True,forward_apply_exact=True,reverse_check=True,reverse_apply_exact=True)
local_artifacts=[dict(root=str(base/'builds'),hash_manifest=str(base/'builds/qualification-06/build.json'),contents='DLL/ZIP/OBJ/disposable EXEs/WAL fixtures/test receipts; excluded'),dict(root=str(base/'specialist'),hash_manifest=str(base/'specialist/seal.json'),contents='Private native specialist/DB bracket receipts'),dict(root=str(root/'.local-work/recon'),hash_manifest=str(base/'specialist/seal.json'),contents='Exact six continuous-preview exports/logs; raw native excluded'),dict(root=str(base),hash_manifest=str(base/'baseline.json'),contents='6,847 exact protected original/archive/prior release/frozen input paths and hashes; source/save-menu receipts stay private'),dict(root='D:/ReverseEngineering/Starfield/GhidraProject',hash_manifest=str(base/'specialist/seal.json'),contents='Analysis DB; excluded'),dict(root='D:/tools',hash_manifest='package patches[*].scratch exact paths',contents='Disposable forward/reverse apply trees; authored files only')]
manifest=dict(local_artifacts=local_artifacts,run=args.run,head=seed['head'],index_sha256=seed['index']['sha256'],staged_changes=False,complete_files=[dict(path=n,sha256=sha(root/n)) for n in names],task_files=task,patches=patches,checks=checks,baseline_snapshot=str(base/'baseline.json'),exclusions=['Ignored local raw saves/decoded bytes/native/proprietary evidence excluded','Protected game/Ghidra inputs and D:/tools scratch trees excluded','Supplied unchanged brief excluded from task-only; earlier tracked work retained','No network/publication/integration/staging/commit/push authority'],exporter_sha256=sha(Path(__file__)))
mp=base/('package-'+args.run+'.json');mp.open('x',encoding='utf8').write(json.dumps(manifest,indent=2)+'\n');(base/('status-'+args.run+'.txt')).open('xb').write(git('status','--short'))
assert sha(root/'.git/index')==seed['index']['sha256'];print('PASS complete/task-only forward+reverse exact',len(names),len(task),sha(mp))
