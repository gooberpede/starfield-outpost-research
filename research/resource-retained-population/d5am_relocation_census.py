# SPDX-License-Identifier: GPL-3.0-or-later
"""Read pinned PE relocation entries for all candidate guard domains.

Reads installed pinned PE, retained identity and one completed/generated candidate
identity. Writes one fresh ignored JSON receipt. Executes no native code, opens
no analysis project and changes no source, game, save, configuration or Git state.
"""
import os
import sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE','0') not in ('','0'):
    raise RuntimeError('Python optimization is forbidden; invoke with -E -B')
import hashlib
import importlib.util
import json
import re
import struct
from pathlib import Path

from d5am_lock_qualify import guard

def main():
    ROOT=Path(__file__).resolve().parents[2]
    spec=importlib.util.spec_from_file_location('owned_pe',ROOT/'runtime/retained-population/build.py')
    pe=importlib.util.module_from_spec(spec);spec.loader.exec_module(pe)
    candidate=(ROOT/sys.argv[1]).resolve();out=(ROOT/sys.argv[2]).resolve()
    if not candidate.is_relative_to(ROOT/'.local-work/d5am') or not out.is_relative_to(ROOT/'.local-work/d5am') or out.exists():
        raise ValueError('Fresh D5AM output and candidate required')
    if any(p.is_symlink() or p.is_junction() for path in (candidate,out) for p in (path,*path.parents)):
        raise ValueError('Reparse paths prohibited')
    free_before=guard()
    image=(pe.GAME/'Starfield.exe').read_bytes()
    if hashlib.sha256(image).hexdigest()!=pe.GAME_HASH:raise ValueError('Pinned PE mismatch')
    optional=struct.unpack_from('<I',image,0x3c)[0]+24
    rr,rs=struct.unpack_from('<II',image,optional+112+5*8);raw=pe.pe_read(image,rr,rs)
    rel={};pos=0
    while pos<len(raw):
        page,size=struct.unpack_from('<II',raw,pos)
        if size<8 or size%2 or pos+size>len(raw):raise ValueError('Relocation block')
        for entry in struct.unpack_from('<'+'H'*((size-8)//2),raw,pos+8):
            if entry>>12:rel[page+(entry&4095)]=entry>>12
        pos+=size
    identity=candidate/'identity.generated.h';text=identity.read_text(encoding='utf8')
    retained=[int(x) for x in re.findall(r'\{(\d+),(?:\d+,)?"[0-9a-f]{64}"\}',text)]
    known=[0x21e09ed,0x21e0aa5,0x21e0a7e,0x789ce0,0x788e70,0x7aab10,0x7ac260,0x7ac2f0]
    for name in ('causal_rvas','scheduler_rvas'):
        values=re.search(name+r'\[\]=\{([^}]+)\}',text)
        if not values:raise ValueError('Missing generated source array')
        known.extend(int(x,0) for x in values[1].split(','))
    for r in list(known):
        call=pe.pe_read(image,r,5)
        if call[0]==0xe8:known.append(r+5+int.from_bytes(call[1:],'little',signed=True))
    known.append(0x27ec2e0)
    ranges=sorted(set((r,32) for r in retained+known))
    ranges+= [(0x22cc350,126),(0x22cc3d0,216),(0x2c45a0,81)]
    rows=[dict(rva=hex(r),bytes=n,relocations=[dict(rva=hex(a),type=t) for a,t in rel.items() if r<=a<r+n]) for r,n in ranges]
    vt=[dict(rva=hex(r+8*i),type=rel.get(r+8*i)) for r in (0x4b3d0e8,0x4b3d138,0x4b406b8) for i in range(4)]
    ok=all(not r['relocations'] for r in rows) and all(r['type']==10 for r in vt)
    receipt=dict(schema='sor-d5am-pe-relocation-census/1',exe_sha256=pe.GAME_HASH,
                 identity_sha256=hashlib.sha256(identity.read_bytes()).hexdigest(),
                 method_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                 code_ranges=rows,vtable_slots=vt,status='PASS' if ok else 'FAIL')
    receipt.update(free_before=free_before,free_after=guard())
    with out.open('x',encoding='utf8',newline='\n') as stream:stream.write(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(dict(status=receipt['status'],code_ranges=len(rows),dir64_slots=len(vt))))
    if not ok:raise RuntimeError('Relocation domain requires review')

if __name__=='__main__':
    main()
