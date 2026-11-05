# SPDX-License-Identifier: GPL-3.0-or-later
"""Verify bounded original GMST reset->definition reload normal-flow closure.
Reads retained original instruction exports and pinned file-audit receipt only;
writes exclusive ignored evidence. CALL exceptions/failed native loads and
unrecorded operators are explicit premises, not invented successful histories.
"""
import os,sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE','') not in ('','0'):raise RuntimeError('Pinned Python -E -B required')
import json,re
from pathlib import Path
from d5ad_baseline import ROOT,guard,sha

def main():
 out=Path(sys.argv[1]).resolve();before=guard()
 if not out.is_relative_to(ROOT/'.local-work/d5ar') or out.exists() or any(p.is_symlink() or p.is_junction() for p in (out,*out.parents)):raise ValueError('Fresh ignored output required')
 path=ROOT/'.local-work/d5ar/reset-parent01/native.tsv';lines=path.read_text(encoding='utf8').splitlines();at=next(i for i,l in enumerate(lines) if l.startswith('FUNCTION\t141896280\t'));rows=[]
 for line in lines[at+1:]:
  if line.startswith(('XREF','DECOMPILE','END_FUNCTION')):break
  match=re.fullmatch(r'([0-9a-f]{9})\t(.+)',line)
  if match:rows.append((int(match[1],16),match[2]))
 seq=[a for a,_ in rows];ops=dict(rows);following={a:seq[i+1] if i+1<len(seq) else None for i,a in enumerate(seq)}
 if len(rows)!=1644 or ops.get(0x141897b19)!='CALL 0x1405994a0' or ops.get(0x1418975c7)!='CALL 0x1428ccfe0':raise ValueError('Original critical flow changed')
 start=0x1418975cc;stop=0x141897b19;seen=set();pending=[start];exits=[]
 while pending:
  address=pending.pop()
  if address==stop or address in seen:continue
  seen.add(address);op=ops[address];mnemonic=op.split()[0]
  if mnemonic=='RET':exits.append((hex(address),op));continue
  if mnemonic.startswith('J'):
   match=re.fullmatch(r'J\w+ 0x([0-9a-f]+)',op)
   if not match:exits.append((hex(address),op));continue
   target=int(match[1],16)
   if target not in ops:exits.append((hex(address),hex(target)))
   else:pending.append(target)
  if mnemonic!='JMP' and following[address]:pending.append(following[address])
 if exits:raise ValueError('Normal exit bypasses definition reload')
 audit=ROOT/'.local-work/d5ar/a0-file-inputs05.json';value=json.loads(audit.read_bytes())
 selected=[r for r in value['records'] if 'InactiveResourceChanceMultExotic'==r['editor_id'].removeprefix('f')]
 if len(selected)!=1 or Path(selected[0]['file']).name.lower()!='starfield.esm' or selected[0]['gmst_data']!=['cdcc4c3d']:raise ValueError('File override alternative remains')
 sources=[path,audit,*[ROOT/'.local-work/d5ar'/name/'native.tsv' for name in ['exotic-root01','effective-setting01','gmst-register01','setting-lookup01','setting-reset01','setting-onchange01','setting-collection-copy01','gmst-data-apply01']]]
 result=dict(status='PASS_SCOPED_NORMAL_FLOW',original_function_instructions=len(rows),nodes_reachable_without_reload=len(seen),normal_exits_without_reload=exits,
  reset_loop='0x141897561 GameSettingCollection getter; registry traversal; 0x1418975c7 reset each registered setting',reload_postdominates_reset=True,reload_call='0x141897b19 -> 0x1405994a0',
  constructor_exotic_bits='0ad7233c',unique_pinned_definition_exotic_bits='cdcc4c3d',
  positive_scope='In the examined ordinary successful file-load path, generic setting reset is followed by definition reload; reset existence alone is not a lasting EXE-default counterexample.',
  not_certified=['Exact A0 dynamic payload at each generation','Complete absence of arbitrary operator/foreign-runtime mutation','Successful DATA application merely from control-flow reachability; native healthy-load prerequisites still apply'],
  inputs={str(p.relative_to(ROOT)):sha(p) for p in sources},method_sha256=sha(__file__),floors_before=before,floors_after=guard())
 with out.open('x',encoding='utf8',newline='\n') as stream:stream.write(json.dumps(result,indent=2)+'\n')
 print(json.dumps(dict(status=result['status'],nodes=len(seen),normal_reload_postdominates=True)))
if __name__=='__main__':main()
