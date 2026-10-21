# SPDX-License-Identifier: GPL-3.0-or-later
"""B2 bounded documentation checker, original Python stdlib/Git diagnostic.
Run with installed CPython: python -X utf8 docs/audits/publication-readiness-b2/check.py
Reads tracked authored text and current B2 documentation; writes only ignored
.local-work/b2/checks.json. No dependencies, downloads, target/save/database,
index/ref mutation or scientific test. Regex links/tables are candidate checks,
not a complete CommonMark renderer or semantic oracle.
"""
import collections, hashlib, json, os, re, subprocess
from pathlib import Path
from urllib.parse import unquote
R=Path(__file__).resolve().parents[3]; O=R/'.local-work/b2'
def git(*a):return subprocess.check_output(['git',*a],cwd=R,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'))
tracked=git('ls-files','-z').decode().split('\0')[:-1]
new=git('ls-files','--others','--exclude-standard','-z').decode().split('\0')[:-1]
texts={};encoding=[];tables=[];fences=[];links=[]
for p in tracked+[x for x in new if x.startswith('docs/audits/publication-readiness-b2/')]:
 if Path(p).suffix.lower() not in {'.md','.csv','.tsv','.txt','.rst','.adoc'}:continue
 b=(R/p).read_bytes()
 try:t=b.decode('utf8')
 except UnicodeDecodeError:encoding.append([p,'invalid UTF8']);continue
 if b.startswith(b'\xef\xbb\xbf'):encoding.append([p,'BOM'])
 texts[p]=t
def slugs(t):
 out=set();count=collections.Counter();fence=False
 for l in t.splitlines():
  if l.lstrip().startswith(('```','~~~')):fence=not fence;continue
  if fence:continue
  if re.match(r'^#{1,6}\s',l):
   s=re.sub(r'\s+#+\s*$','',re.sub(r'^#+\s+','',l)).lower()
   s=re.sub(r'<[^>]+>','',s);s=re.sub(r'[^\w\- ]','',s).replace(' ','-')
   i=count[s];count[s]+=1;out.add(s+(f'-{i}' if i else ''))
 out.update(re.findall(r'(?:id|name)=["\']([^"\']+)',t));return out
for p,t in texts.items():
 if not p.endswith('.md'):continue
 fence=None;prev=None
 for n,l in enumerate(t.splitlines(),1):
  m=re.match(r'^\s*(`{3,}|~{3,})',l)
  if m:
   if fence is None:fence=(m[1][0],len(m[1]),n)
   elif m[1][0]==fence[0] and len(m[1])>=fence[1]:fence=None
   continue
  if fence:continue
  if l.startswith('|'):
   width=len(re.split(r'(?<!\\)\|',l))
   if prev and width!=prev[0]:tables.append(dict(path=p,line=n,previous=prev,width=width))
   prev=(width,n)
  else:prev=None
  targets=re.findall(r'\[[^\]]*\]\((<[^>]+>|[^\s)]+)(?:\s+"[^"]*")?\)',l)
  targets+=re.findall(r'^\s*\[[^\]]+\]:\s*(\S+)',l)
  targets+=re.findall(r'(?:href|src)=["\']([^"\']+)',l)
  for target in targets:
   target=unquote(target.strip('<>'))
   if re.match(r'^[a-zA-Z][\w+.-]*:',target):continue
   path,_,anchor=target.partition('#');path=path.split('?')[0]
   q=(R/p).parent.joinpath(path).resolve() if path else R/p
   rel=os.path.relpath(q,R).replace('\\','/')
   state='present' if q.exists() else 'missing'
   if '.local-work/' in rel:state='local-only'
   if rel in texts and anchor and anchor not in slugs(texts[rel]):state='anchor-candidate'
   if state!='present':links.append(dict(path=p,line=n,target=target,resolved=rel,state=state))
 if fence:fences.append(dict(path=p,opening=fence))
residual_cases=[
 ('docs/experiments/local-output-links/lifecycle.md','subscribed at145916518 with','subscribed at 145916518 with'),
 ('docs/experiments/crew/current-review.md','Both-drive40GB guards','Both-drive 40GB guards'),
 ('docs/experiments/crew-lifecycle/native.md','check actor3D','check actor 3D'),
 ('docs/experiments/crew-lifecycle/persistence.md','Ordinary actor3D absence','Ordinary actor 3D absence'),
 ('docs/experiments/containers-displays/native.md','ExtraOwnership type1F','ExtraOwnership type 1F')]
residual_controls=[dict(path=p,old_absent=a not in texts[p],new_present=b in texts[p],nonwhitespace_equal=re.sub(r'\s','',a)==re.sub(r'\s','',b)) for p,a,b in residual_cases]
assert all(x['old_absent'] and x['new_present'] and x['nonwhitespace_equal'] for x in residual_controls)
import csv
with (R/'docs/audits/publication-readiness-b2/reader-dependencies.csv').open(encoding='utf8') as f:
 alias_control=[x for x in csv.DictReader(f) if x['path']=='docs/experiments/workshop-population/validation.md' and x['baseline_line']=='24']
assert len(alias_control)==1 and alias_control[0]['source_aliases']=='S1;Save52'
receipt=dict(corpus_files=len(texts),lines=sum(len(t.splitlines()) for t in texts.values()),encoding=encoding,table_transitions=tables,unclosed_fences=fences,link_candidates=links,residual_controls=residual_controls,
 head=git('rev-parse','HEAD').decode().strip(),index_sha256=hashlib.sha256((R/'.git/index').read_bytes()).hexdigest())
O.mkdir(exist_ok=True,parents=True);(O/'checks.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf8',newline='\n')
print(json.dumps({k:v for k,v in receipt.items() if k not in ['link_candidates']},indent=2));print('link candidates',len(links))
