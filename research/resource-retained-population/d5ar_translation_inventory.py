# SPDX-License-Identifier: GPL-3.0-or-later
"""Inventory translation-field roots, raw address literals and initial PE bytes.

Reads pinned original PE plus exact read-only root exports. Writes one exclusive
ignored receipt; never executes native code, opens a DB or accesses a game/save.
Literal/xref coverage is diagnostic and cannot alone exclude computed aliases.
Both caller-available drive floors are checked before and after analysis.
"""
import os
import sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE','') not in ('','0'):
    raise RuntimeError('Use pinned Python -E -B without optimization')

import hashlib
import json
from pathlib import Path
import re
import struct
from d5ar_native_inventory import ROOT, EXE, PIN, disk_floor


def main():
    out=Path(sys.argv[1]).resolve()
    if not out.is_relative_to(ROOT / '.local-work/d5ar') or out.exists():
        raise ValueError('Fresh ignored D5AR output required')
    if any(p.is_symlink() or p.is_junction() for p in (out,*out.parents)):
        raise ValueError('No reparse outputs')
    before=disk_floor()
    data=EXE.read_bytes()
    if hashlib.sha256(data).hexdigest()!=PIN:raise ValueError('Installed PE changed')
    pe=struct.unpack_from('<I',data,0x3c)[0]
    optional=struct.unpack_from('<H',data,pe+20)[0]
    sections=[struct.unpack_from('<IIII',data,pe+24+optional+40*n+8)
              for n in range(struct.unpack_from('<H',data,pe+6)[0])]
    base=struct.unpack_from('<Q',data,pe+48)[0]
    if base!=0x140000000:raise ValueError('Image base mismatch')
    def bytes_at(address,size):
        rva=address-base
        for virtual,start,raw_size,raw in sections:
            if start<=rva and rva+size<=start+max(virtual,raw_size):
                if rva+size<=start+raw_size:return data[raw+rva-start:raw+rva-start+size],'FILE_BACKED'
                if rva>=start+raw_size:return bytes(size),'PE_ZERO_FILL'
                raise ValueError('Mixed raw/zero-fill range')
        raise ValueError('Address not in mapped section')
    def file_va(offset):
        for _,rva,size,raw in sections:
            if raw<=offset<raw+size:return hex(base+rva+offset-raw)
        return None
    roots=[];pins={}
    for label,expected in [('translation-count-writers01','3998f7be033b9ca04583ca39a49398cf0b878596acde49370e34d44b851ca0ad'),
                           ('translation-pointer-writers01','bcf6e6f4aba2ddfe9f8a47a8f987d25b5540f808974c42d23fb8cdb2724fcafd')]:
        path=ROOT / '.local-work/d5ar' / label / 'native.tsv'
        raw=path.read_bytes();digest=hashlib.sha256(raw).hexdigest()
        if digest!=expected or not raw.endswith(b'END\n'):raise ValueError('Root export changed/incomplete')
        pins[str(path.relative_to(ROOT))]=digest
        records=re.findall(r'^ROOT\s+From: ([0-9a-f]+) To: ([0-9a-f]+) Type: ([^ ]+)',raw.decode(),re.M)
        leas=[]
        for address,_,_ in records:
            code,_=bytes_at(int(address,16),8)
            if code[0]==0x8d or (0x40<=code[0]<=0x4f and code[1]==0x8d):leas.append('0x'+address)
        roots.append(dict(export=label,references=len(records),direct_writes=[dict(static_va='0x'+a,target='0x'+b)
            for a,b,kind in records if kind=='WRITE'],native_lea_candidates=leas))
    literal=[]
    for address in range(0x1461fae80,0x1461fae90):
        for name,pattern in [('full_va_u64',struct.pack('<Q',address)),('rva_u32',struct.pack('<I',address-base))]:
            at=0
            while True:
                at=data.find(pattern,at)
                if at<0:break
                literal.append(dict(target=hex(address),encoding=name,file_offset=at,mapped_static_va=file_va(at)))
                at+=1
    initial,origin=bytes_at(0x1461fae80,16)
    value=dict(status='PASS',scope='Bounded direct-root/literal inventory; computed/wider-object aliases not excluded',
        exe_sha256=PIN,root_exports=roots,literal_references=literal,initial_header_hex=initial.hex(),
        initial_header_origin=origin,inputs=pins,method_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        index_zero_immutable_proven=False,floors_before=before,floors_after=disk_floor())
    with out.open('x',encoding='utf8',newline='\n') as stream:stream.write(json.dumps(value,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',roots=[r['references'] for r in roots],literal_references=len(literal),
                         initial_header=initial.hex(),zero_immutable_proven=False)))


if __name__=='__main__':main()
