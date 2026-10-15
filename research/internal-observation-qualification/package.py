"""Owned predecessor document/patch checker adapted for this qualification. Reads HEAD, worktree and selected pins;
writes ignored receipts/patches and temporary text apply trees. No target execution,
network, dependencies, index/ref mutation or protected-input writes."""
import csv,difflib,hashlib,json,os,pathlib,re,subprocess,tempfile
R=pathlib.Path(__file__).resolve().parents[2]; O=R/'.local-work/internal-observation-qualification'
ENV=dict(os.environ,GIT_OPTIONAL_LOCKS='0')
def git(*a,cwd=R):
 p=subprocess.run(['git','-c','core.autocrlf=false',*a],cwd=cwd,env=ENV,capture_output=True)
 if p.returncode:raise RuntimeError((a,p.stderr.decode(errors='replace')))
 return p.stdout
def sha(b):return hashlib.sha256(b).hexdigest()
def filehash(p):
 d=hashlib.sha256()
 with pathlib.Path(p).open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):d.update(b)
 return d.hexdigest()
def write(name,obj): (O/name).write_text(json.dumps(obj,indent=2)+'\n',encoding='utf-8',newline='\n')
before=json.loads((O/'preservation-before.json').read_text())
assert git('rev-parse','HEAD').decode().strip()==before['head']
rows=[dict(x,actual=filehash(x['path'])) for x in before['pins']]
assert all(x['actual']==x['sha256'] for x in rows)
write('preservation-after.json',{'head':before['head'],'pins_checked':len(rows),'all_equal':True,'pins':rows,'scope':before['scope']})
changed=git('diff','HEAD','--name-only','-z').decode().split('\0')[:-1]
new=git('ls-files','--others','--exclude-standard','-z').decode().split('\0')[:-1]
names=sorted(set(changed+new)); brief='docs/implementation-briefs/CODEX_BRIEF_SOR_experiment_A_internal_observation_offline_qualification.md'
task=[n for n in names if n!=brief]
assert task and brief in names
cur={n:(R/n).read_bytes() if (R/n).exists() else None for n in names}
old={n:git('show','HEAD:'+n) if n in changed else None for n in names}
link_count=0;prose=[]
for n in task:
 t=cur[n].decode('utf-8'); assert '\r' not in t and not t.startswith('\ufeff'),n
 # Whole new documents, added lines only in existing indexes.
 checked=t if n in new else '\n'.join(x[1:] for x in git('diff','--',n).decode().splitlines() if x.startswith('+') and not x.startswith('+++'))
 assert all(x.rstrip()==x for x in checked.splitlines()),n
 for line in checked.splitlines():
  if re.search(r'\w`|`[A-Za-z]|\b(?:0x[0-9a-f]+|0\.[78]\.0)[A-Za-z]',line,re.I):prose.append({'path':n,'line':line})
 if not n.endswith('.md'):continue
 for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',checked):
  p=target.split('#')[0].strip('<>')
  if not p or re.match(r'^[A-Za-z]+:',p):continue
  assert (R/n).parent.joinpath(p).resolve().exists(),(n,target)
  link_count+=1
# Exact source hash pins from prior manifests.
pins=[]
for manifest in ['docs/experiments/native-availability-map/sources.csv','docs/experiments/resource-availability-milestone-b/native-sources.csv']:
 for row in csv.DictReader((R/manifest).open(encoding='utf-8-sig')):
  if row['path'] in [str(pathlib.Path(x['path']).relative_to(R)).replace('\\','/') for x in before['pins'] if pathlib.Path(x['path']).is_relative_to(R)]:
   assert filehash(R/row['path'])==row['sha256'];pins.append(row['path'])
P16=(R/'.local-work/recon/resource-availability-ui-16.tsv').read_text();P17=(R/'.local-work/recon/resource-availability-ui-17.tsv').read_text()
facts=['1421e1140\tJA 0x1421e174e','1421e114c\tJZ 0x1421e1772','1421e1154\tJZ 0x1421e174e','1421e174e\tADD RBX,0x30','1421e1772\tMOV RBX,qword ptr [RSI + 0x8]','1421e18f2\tMOV EAX,0x1','1421e1091\tMOV R9,qword ptr [RSI]','1421e1393\tMOV RDX,qword ptr [RSI]','1421e146b\tMOV EAX,dword ptr [RDX + 0xc]']
assert all(x in P16 for x in facts)
assert '140f4ac54\tMOV EAX,dword ptr [RDX + 0xc]' in P17
assert '140f4acef\tAND AL,CL' in P17
exe=next(x for x in rows if x['path'].endswith('Starfield.exe'))
assert exe['actual']=='7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28'
git('diff','--check')
def diff(n,a,b):
 out=['diff --git a/'+n+' b/'+n+'\n']
 if a is None:out.append('new file mode 100644\n')
 if b is None:out.append('deleted file mode 100644\n')
 for line in difflib.unified_diff((a or b'').decode().splitlines(keepends=True),(b or b'').decode().splitlines(keepends=True),fromfile='/dev/null' if a is None else 'a/'+n,tofile='/dev/null' if b is None else 'b/'+n,lineterm='\n'):
  out.append(line if line.endswith('\n') else line+'\n\\ No newline at end of file\n')
 return ''.join(out).encode()
patches={}
for kind,paths in [('task-only',task),('complete',names)]:
 data=b''.join(diff(n,old[n],cur[n]) for n in paths)
 out=R/('.local-work/diffs/internal-observation-qualification-'+kind+'.diff');out.parent.mkdir(exist_ok=True);out.write_bytes(data)
 inventory=re.findall(r'^diff --git a/(.*?) b/.*$',data.decode(),re.M);assert inventory==paths
 with tempfile.TemporaryDirectory(prefix='sor-spatial-review-') as td:
  d=pathlib.Path(td)
  for n in paths:
   if old[n] is not None:(d/n).parent.mkdir(parents=True,exist_ok=True);(d/n).write_bytes(old[n])
  git('apply','--check',str(out),cwd=d);git('apply',str(out),cwd=d)
  assert all((d/n).read_bytes()==cur[n] for n in paths)
  git('apply','--check','--reverse',str(out),cwd=d);git('apply','--reverse',str(out),cwd=d)
  assert all(((d/n).read_bytes()==old[n]) if old[n] is not None else not (d/n).exists() for n in paths)
 patches[kind]={'path':str(out),'sha256':sha(data),'bytes':len(data),'paths':paths,'forward_reverse_exact':True}
def inventory(paths):return [{'path':n,'sha256':sha(cur[n]),'bytes':len(cur[n]),'kind':'new text' if n in new else 'modified text'} for n in paths]
write('changed-files.json',inventory(task));write('complete-files.json',inventory(names))
write('exclusions.json',{'text_patch_scope':'Nonignored uncommitted text only','ignored_local':['.local-work/internal-observation-qualification/ disposable runs and receipts','.local-work/diffs/ patches','.local-work/recon/ unchanged native exports','Existing raw saves/captures/build artifacts/databases remain outside patches'],'binary_changed_files':[],'supplied_brief_in_complete_only':brief,'external_protected_roots':'No writes or full inventory audit'})
(O/'git-status-short.txt').write_bytes(git('status','--short'))
write('verification.json',{'source_manifest_pin_checks':len(pins),'unique_source_pins':len(set(pins)),'instruction_assertions':len(facts)+2,'exe_pin_equal':True,'selected_preservation_pins':len(rows),'links_checked':link_count,'git_diff_check':'PASS','new_file_whitespace':'PASS','prose_pattern_candidates':prose,'patch_inventory_and_exact_forward_reverse':'PASS','native_pairs':0,'native_equivalence':'NOT TESTED','synthetic_native_tests':'native-11', 'decoder_receipt':'native-11/decode.json'})
evidence={str(p.relative_to(O)):dict(sha256=filehash(p),bytes=p.stat().st_size) for p in O.rglob('*') if p.is_file() and (p.parts[-2].startswith('native') or p.name in ('static-contract.json','preservation-before.json'))}
write('evidence-files.json',evidence)
write('package.json',{'head':before['head'],'index_sha256':filehash(R/'.git/index'),'script_sha256':filehash(__file__),'evidence_manifest_sha256':filehash(O/'evidence-files.json'),'task_files':inventory(task),'complete_files':inventory(names),'patches':patches})
(O/'package.sha256').write_text(filehash(O/'package.json')+'  package.json\n',encoding='utf-8')
print(json.dumps({'task_files':len(task),'complete_files':len(names),'source_pins':len(set(pins)),'instruction_assertions':len(facts)+2,'links':link_count,'prose_candidates':len(prose),'preserved':len(rows),'patches':patches},indent=2))
