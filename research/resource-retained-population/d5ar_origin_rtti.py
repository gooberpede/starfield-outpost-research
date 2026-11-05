# SPDX-License-Identifier: GPL-3.0-or-later
"""Locate bounded original world-origin event RTTI/vtable candidates in pinned PE.

Owned decoder hypothesis for MSVC image-relative RTTI: validates COL signature,
self RVA, file-backed type/hierarchy bounds and base arrays. Matches nominate
native vtables/functions for existing-analysis verification, not event semantics.
Reads PE only; writes exclusive ignored offsets/metadata, no native execution,
DB mutation, save/target access, installs or network. Both-drive floors checked.
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
    if any(p.is_symlink() or p.is_junction() for p in (out,*out.parents)):raise ValueError('No reparse output')
    before=disk_floor();data=EXE.read_bytes()
    if hashlib.sha256(data).hexdigest()!=PIN:raise ValueError('Installed PE changed')
    pe=struct.unpack_from('<I',data,0x3c)[0];optional=struct.unpack_from('<H',data,pe+20)[0]
    sections=[struct.unpack_from('<IIII',data,pe+24+optional+40*n+8)
        for n in range(struct.unpack_from('<H',data,pe+6)[0])]
    def offset(rva,size=1):
        for _,start,raw_size,raw in sections:
            if start<=rva and rva+size<=start+raw_size:return raw+rva-start
        raise ValueError('Not wholly file-backed')
    def rva_at(at):
        for _,rva,size,raw in sections:
            if raw<=at<raw+size:return rva+at-raw
        raise ValueError('Unmapped file offset')
    def words(rva,n):return struct.unpack_from('<'+'I'*n,data,offset(rva,4*n))
    def name(rva):
        at=offset(rva+16);end=data.find(b'\0',at,min(len(data),at+256))
        if end<0:raise ValueError('Unbounded type name')
        return data[at:end].decode('ascii')
    wanted={0x5a0b570,0x5a0b5c0,0x5a0ba80,0x5a0bac0};rows=[];at=0;valid=0
    while True:
        at=data.find(b'\x01\0\0\0',at)
        if at<0:break
        candidate=at;at+=1
        try:
            rva=rva_at(candidate)
            signature,vt_offset,constructor,td,hierarchy,self_rva=words(rva,6)
            if signature!=1 or self_rva!=rva or vt_offset>0x10000:continue
            signature_h,attributes,count,array=words(hierarchy,4)
            if signature_h!=0 or not 1<=count<=128:continue
            base_records=words(array,count)
            types=[words(base,1)[0] for base in base_records]
            own=name(td)
            if not own.startswith('.?A'):continue
            valid+=1
            if not wanted.intersection(types) and td not in wanted:continue
            locations=[];search=0;pattern=struct.pack('<Q',0x140000000+rva)
            while True:
                hit=data.find(pattern,search)
                if hit<0:break
                search=hit+1
                try:
                    vrva=rva_at(hit);functions=struct.unpack_from('<8Q',data,offset(vrva+8,64))
                    locations.append(dict(vtable_static_va=hex(0x140000000+vrva+8),
                        first_eight_words=[hex(value) for value in functions]))
                except (ValueError,struct.error):continue
            rows.append(dict(col_static_va=hex(0x140000000+rva),vtable_object_offset=vt_offset,
                type_static_va=hex(0x140000000+td),type_name=own,hierarchy_static_va=hex(0x140000000+hierarchy),
                base_types=[dict(type_static_va=hex(0x140000000+base),name=name(base),
                    descriptor_static_va=hex(0x140000000+record),member_displacement=words(record,3)[2],
                    pdisp_word=words(record,4)[3],vdisp_word=words(record,5)[4]) for base,record in zip(types,base_records)],vtables=locations))
            if len(rows)>64:raise RuntimeError('Bounded event-family COL count exceeded')
        except (ValueError,UnicodeDecodeError,struct.error):continue
    result=dict(status='PASS',scope='Validated-layout RTTI candidate decoder; native event semantics require original function verification',
        exe_sha256=PIN,method_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        plausible_col_count=valid,event_family=rows,floors_before=before,floors_after=disk_floor())
    with out.open('x',encoding='utf8',newline='\n') as stream:stream.write(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',plausible_cols=valid,event_family=len(rows))))


if __name__=='__main__':main()
