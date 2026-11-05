# SPDX-License-Identifier: GPL-3.0-or-later
"""Read pinned PE for wider translation-neighborhood address literals.

No execution/disassembly/database change. Candidates are byte encodings, never
asserted instruction boundaries or pointer aliases. Records mapped sections and
all matching full-VA/RVA values in a bounded 8 KiB neighborhood; writes one
exclusive ignored receipt with input/method pins and both-drive floors.
"""
import os
import sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE','') not in ('','0'):
    raise RuntimeError('Use pinned Python -E -B without optimization')

import hashlib
import json
from pathlib import Path
import struct
from d5ar_native_inventory import ROOT, EXE, PIN, disk_floor


def main():
    out=Path(sys.argv[1]).resolve()
    if not out.is_relative_to(ROOT/'.local-work/d5ar') or out.exists():raise ValueError('Fresh ignored output required')
    if any(p.is_symlink() or p.is_junction() for p in (out,*out.parents)):raise ValueError('No reparse output')
    before=disk_floor();data=EXE.read_bytes()
    if hashlib.sha256(data).hexdigest()!=PIN:raise ValueError('Installed PE changed')
    pe=struct.unpack_from('<I',data,0x3c)[0];optional=struct.unpack_from('<H',data,pe+20)[0]
    sections=[]
    for n in range(struct.unpack_from('<H',data,pe+6)[0]):
        at=pe+24+optional+40*n
        virtual,rva,size,raw=struct.unpack_from('<IIII',data,at+8)
        sections.append((data[at:at+8].rstrip(b'\0').decode('ascii'),rva,size,raw,struct.unpack_from('<I',data,at+36)[0]))
    def location(offset):
        for name,rva,size,raw,flags in sections:
            if raw<=offset<raw+size:return dict(section=name,static_va=hex(0x140000000+rva+offset-raw),executable=bool(flags&0x20000000))
        return dict(section=None,static_va=None,executable=False)
    hits=[]
    for name,upper,size,base in [('full_va_u64',b'\x1f\x46\x01\0\0\0',8,0),('rva_u32',b'\x1f\x06',4,0x140000000)]:
        at=0
        while True:
            match=data.find(upper,at)
            if match<0:break
            at=match+1;start=match-2
            if start<0 or start+size>len(data):continue
            value=int.from_bytes(data[start:start+size],'little')+base
            if 0x1461f9e80<=value<0x1461fbe80:
                hits.append(dict(encoding=name,file_offset=start,target=hex(value),location=location(start),
                    surrounding_start=max(0,start-16),surrounding_hex=data[max(0,start-16):start+size+16].hex()))
    result=dict(status='PASS',scope='Raw encoded candidates; no instruction-boundary or semantic alias claim',
        exe_sha256=PIN,method_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        neighborhood=['0x1461f9e80','0x1461fbe80'],candidates=hits,floors_before=before,floors_after=disk_floor())
    with out.open('x',encoding='utf8',newline='\n') as stream:stream.write(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',candidates=len(hits))))


if __name__=='__main__':main()
