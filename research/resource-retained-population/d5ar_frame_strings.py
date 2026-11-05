# SPDX-License-Identifier: GPL-3.0-or-later
"""Read-only pinned-PE exact frame/origin registration-name candidate search.

Writes bounded offsets/VAs, exact matched search terms and selected bounded ASCII
label context to ignored receipt; does not dump bulk strings, execute code, disassemble, open
analysis databases or contact a network. Names nominate original native xrefs;
they do not prove semantics or writer presence/absence. Both-drive floors apply.
"""
import os
import sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE','') not in ('','0'):
    raise RuntimeError('Use pinned Python -E -B without optimization')

import hashlib
import json
from pathlib import Path
import struct
from d5ar_native_inventory import ROOT,EXE,PIN,disk_floor


def main():
    out=Path(sys.argv[1]).resolve()
    if not out.is_relative_to(ROOT/'.local-work/d5ar') or out.exists():raise ValueError('Fresh ignored output required')
    if any(p.is_symlink() or p.is_junction() for p in (out,*out.parents)):raise ValueError('No reparse outputs')
    before=disk_floor();data=EXE.read_bytes()
    if hashlib.sha256(data).hexdigest()!=PIN:raise ValueError('Installed PE changed')
    pe=struct.unpack_from('<I',data,0x3c)[0];optional=struct.unpack_from('<H',data,pe+20)[0]
    sections=[struct.unpack_from('<IIII',data,pe+24+optional+40*n+8)
        for n in range(struct.unpack_from('<H',data,pe+6)[0])]
    def va(offset):
        for _,rva,size,raw in sections:
            if raw<=offset<raw+size:return hex(0x140000000+rva+offset-raw)
        return None
    terms=['BSPosition','WorldOrigin','OriginShift','ShiftOrigin','SetOrigin','Rebase','FloatingOrigin',
           'OriginOffset','FrameIndex','PositionIndex','RegisterPosition','TranslateWorld']
    rows=[]
    for term in terms:
        for encoding in ['ascii','utf-16-le']:
            pattern=term.encode(encoding);at=0
            while True:
                hit=data.find(pattern,at)
                if hit<0:break
                at=hit+1;row=dict(term=term,encoding=encoding,file_offset=hit,static_va=va(hit))
                if encoding=='ascii' and term in ('BSPosition','WorldOrigin','OriginShift','OriginOffset'):
                    start=data.rfind(b'\0',max(0,hit-192),hit)+1
                    end=data.find(b'\0',hit,min(len(data),hit+192))
                    if end>=0 and end-start<=256:
                        row.update(label_start=va(start),local_label=data[start:end].decode('ascii',errors='backslashreplace'))
                rows.append(row)
                if len(rows)>300:raise ValueError('Bounded registration-candidate count exceeded')
    result=dict(status='PASS',scope='Exact-name nominations only; no native semantic absence claim',
        exe_sha256=PIN,method_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        terms=terms,matches=rows,floors_before=before,floors_after=disk_floor())
    with out.open('x',encoding='utf8',newline='\n') as stream:stream.write(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',matches=len(rows),selected_labels=[r for r in rows if 'local_label' in r])))


if __name__=='__main__':main()
