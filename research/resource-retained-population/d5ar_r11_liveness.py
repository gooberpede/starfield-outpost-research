# SPDX-License-Identifier: GPL-3.0-or-later
"""Owned direct-CFG incoming R11 liveness proof from pinned original exports.
Reads existing native instruction exports only; no native or DB execution.
Writes exclusive ignored receipt. CALL preserves neither R11 nor analysis state:
this proof conservatively tracks explicit reads without crediting call clobbers.
"""
import os,sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE','') not in ('','0'):raise RuntimeError('Pinned Python -E -B required')
import json,re
from pathlib import Path
from d5ad_baseline import ROOT,guard,sha

def body(path,start):
    lines=path.read_text().splitlines();at=next(i for i,l in enumerate(lines) if l.startswith('FUNCTION\t'+start+'\t'));rows=[]
    for line in lines[at+1:]:
        if line.startswith(('XREF','DECOMPILE','FUNCTION')):break
        match=re.fullmatch(r'([0-9a-f]{9})\t(.+)',line)
        if match:rows.append((int(match[1],16),match[2]))
    if not rows or rows[0][0]!=int(start,16):raise ValueError('Missing original entry')
    return rows

def inspect(rows):
    if not any('R11' in op for _,op in rows):return dict(instructions=len(rows),incoming_r11_dead=True,uses=[],reason='No R11 operand in complete original body')
    seq=[a for a,_ in rows];pred={a:set() for a in seq}
    for i,(address,op) in enumerate(rows):
        mnemonic=op.split()[0];targets=[]
        if mnemonic.startswith('J'):
            match=re.fullmatch(r'J\w+ 0x([0-9a-f]+)',op)
            if not match:raise ValueError('Indirect jump requires separate closure')
            targets.append(int(match[1],16))
        if mnemonic not in ('JMP','RET','INT3') and i+1<len(seq):targets.append(seq[i+1])
        for target in targets:
            if target not in pred:raise ValueError('Escaping branch')
            pred[target].add(address)
    # Definitely initialized explicit register state, including loop fixed point.
    initialized={a:True for a in seq};initialized[seq[0]]=False
    while True:
        changed=False
        for address,op in rows:
            incoming=False if address==seq[0] else bool(pred[address]) and all(initialized[p] for p in pred[address])
            defines=bool(re.match(r'(?:MOV|LEA|XOR) R11(?:D|W|B)?,',op))
            outgoing=incoming or defines
            if initialized[address]!=outgoing:initialized[address]=outgoing;changed=True
        if not changed:break
    uses=[]
    for address,op in rows:
        if 'R11' not in op:continue
        defines=bool(re.match(r'(?:MOV|LEA) R11(?:D)?,',op))
        if not defines and (address==seq[0] or not pred[address] or not all(initialized[p] for p in pred[address])):raise ValueError('Incoming R11 may be read')
        uses.append(dict(address=hex(address),instruction=op,defines=defines))
    return dict(instructions=len(rows),incoming_r11_dead=True,uses=uses)

def main():
    out=Path(sys.argv[1]).resolve();before=guard()
    if not out.is_relative_to(ROOT/'.local-work/d5ar') or out.exists() or any(p.is_symlink() or p.is_junction() for p in (out,*out.parents)):raise ValueError('Fresh ignored nonreparse receipt')
    groups={'.local-work/d5am/owner-census01/native.tsv':['14079d910'],'.local-work/d5am/owner-census02/native.tsv':['14079df70'],'.local-work/d5am/d5ar-native01/native.tsv':['140788bc0'],'.local-work/d5am/owner-census05/native.tsv':['141881660','140789ce0','140788e70'],'.local-work/d5v/export01/native.tsv':['1421e07d0','1421e0f50'],'.local-work/d5v/export05/native.tsv':['1407affb0'],'.local-work/d5am/d5ar-native02/native.tsv':['1421b2570']}
    result={};pins={}
    for path,starts in groups.items():
        path=ROOT/path;pins[str(path.relative_to(ROOT))]=sha(path)
        for start in starts:result['0x'+start]=inspect(body(path,start))
    value=dict(status='PASS',scope='original ten hook entry incoming R11 liveness only',methods='Direct branch fixed-point definite initialization; no CALL clobber assumed',targets=result,inputs=pins,method_sha256=sha(__file__),floors_before=before,floors_after=guard())
    with out.open('x',encoding='utf8',newline='\n') as stream:stream.write(json.dumps(value,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',targets=len(result))))
if __name__=='__main__':main()
