# SPDX-License-Identifier: GPL-3.0-or-later
"""Authenticate copied-analysis instruction bytes and expose lock receiver paths.

Reads one fresh D5AM copied-export receipt/TSV and the pinned installed PE.
Writes a fresh ignored JSON census with exact call/atomic context. No native
execution, project opening, original evidence or game/save/configuration writes.
Receiver classification remains an explicit scientific review, not a text-match
claim that nearby function addresses share a lock.
"""
import os
import sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE','0') not in ('','0'):
    raise RuntimeError('Python optimization is forbidden; invoke with -E -B')
from pathlib import Path
import hashlib
import importlib.util
import json
import re
from d5am_lock_qualify import guard

ROOT=Path(__file__).resolve().parents[2]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def main():
    source=(ROOT/sys.argv[1]).resolve();out=(ROOT/sys.argv[2]).resolve()
    if any(p.is_symlink() or p.is_junction() for path in (source,out) for p in (path,*path.parents)):
        raise ValueError('Reparse path prohibited')
    if not source.is_relative_to(ROOT/'.local-work/d5am') or not out.is_relative_to(ROOT/'.local-work/d5am') or out.exists():
        raise ValueError('Fresh D5AM output required')
    free=guard();receipt=json.loads((source/'result.json').read_bytes());native=source/'native.tsv'
    if not receipt['copy_core_preserved'] or sha(native)!=receipt['native_sha256']:
        raise ValueError('Copied export provenance')
    spec=importlib.util.spec_from_file_location('owned_pe',ROOT/'runtime/retained-population/build.py')
    pe=importlib.util.module_from_spec(spec);spec.loader.exec_module(pe)
    image=(pe.GAME/'Starfield.exe').read_bytes()
    if hashlib.sha256(image).hexdigest()!=pe.GAME_HASH:raise ValueError('Installed PE identity')
    text=native.read_text(encoding='utf8')
    if text.splitlines()[0]!='SHA256\t'+pe.GAME_HASH or not text.endswith('END\n'):raise ValueError('Imported program identity/completeness')
    copied={};byte_count=0
    for addr,raw in re.findall(r'^BYTES\t([0-9a-f]+)\t([0-9a-f]+)$',text,re.M):
        data=bytes.fromhex(raw);rva=int(addr,16)-0x140000000
        if pe.pe_read(image,rva,len(data))!=data:raise ValueError('Analysis byte mismatch '+addr)
        copied[addr]=raw;byte_count+=len(data)
    if not copied:raise ValueError('No exported instruction bytes')
    rows=[];ranges_by_function={}
    for body in re.split(r'^FUNCTION\t',text,flags=re.M)[1:]:
        entry=body.split('\t',1)[0];ranges_by_function[entry]=[(int(a,16),int(b,16)) for a,b in re.findall(r'\[([0-9a-f]{9}),\s*([0-9a-f]{9})\]',body.split('\n',1)[0])];instructions=re.findall(r'^([0-9a-f]{9})\t([^\n]+)$',body.split('\n',1)[1],re.M)
        if any(addr not in copied for addr,_ in instructions):raise ValueError('Unverified instruction')
        contexts=[]
        for index,(addr,op) in enumerate(instructions):
            if any(target in op for target in ('CALL 0x1422cc350','CALL 0x1422cc3d0','CALL 0x1402c45a0')) or '.LOCK' in op or op.startswith('XCHG '):
                contexts.append(dict(site=addr,operation=op,before=instructions[max(0,index-8):index],after=instructions[index+1:index+4]))
        rows.append(dict(entry=entry,instructions=len(instructions),contexts=contexts))
    roots=[int(a,16) for a in re.findall(r'^ROOT\tFrom: ([0-9a-f]+)',text,re.M)]
    direct={entry for entry,ranges in ranges_by_function.items() if any(lo<=a<=hi for a in roots for lo,hi in ranges)}
    interval={entry for entry in ranges_by_function if 0x140787000<=int(entry,16)<0x140790000}
    union=dict(root_references=len(roots),direct_reference_functions=len(direct),manager_interval_functions=len(interval),overlap_functions=len(direct&interval),union_functions=len(direct|interval)) if roots else None
    if roots and len(direct|interval)!=len(rows):raise ValueError('Root/interval union does not explain exported function set')
    result=dict(root_union=union,schema='sor-d5am-owner-census/1',status='PASS',coverage='explicit exported functions; receiver interpretation requires review',
                source_sha256=sha(native),receipt_sha256=sha(source/'result.json'),method_sha256=sha(__file__),exe_sha256=pe.GAME_HASH,
                verified_instructions=len(copied),verified_bytes=byte_count,functions=rows,free_before=free,free_after=guard())
    with out.open('x',encoding='utf8',newline='\n') as stream:stream.write(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',functions=len(rows),verified_instructions=len(copied),verified_bytes=byte_count)))

if __name__=='__main__':
    main()
