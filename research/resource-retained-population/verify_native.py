# SPDX-License-Identifier: GPL-3.0-or-later
"""Offline PE/site and receipt verification. No process or target mutations.

Reads installed PE, read-only Ghidra site export, built synthetic PE and SRO1
receipts. Writes only the requested task-local verification JSON. Standard
library only; instruction lengths/flows come from the pinned existing analysis.
"""
import json
from pathlib import Path
import struct
import sys
from build import LOCAL,pin
from native_reduce import RETAIL_RVAS,RETAIL_NEXT,EVENTS
from qualify import decoder


class PE:
    def __init__(self,path):
        self.b=Path(path).read_bytes();p=struct.unpack_from('<I',self.b,0x3c)[0]
        assert self.b[p:p+4]==b'PE\0\0' and self.u16(p+4)==0x8664
        n=self.u16(p+6);size=self.u16(p+20);self.opt=p+24
        assert self.u16(self.opt)==0x20b
        self.base=self.u64(self.opt+24);self.sections=[]
        for i in range(n):
            at=self.opt+size+i*40;vs,va,rs,raw=struct.unpack_from('<4I',self.b,at+8)
            self.sections.append((va,vs,rs,raw))
    def u16(self,p):return struct.unpack_from('<H',self.b,p)[0]
    def u32(self,p):return struct.unpack_from('<I',self.b,p)[0]
    def u64(self,p):return struct.unpack_from('<Q',self.b,p)[0]
    def offset(self,rva):
        for va,vs,rs,raw in self.sections:
            if va<=rva<va+max(vs,rs):
                assert rva-va<rs
                return raw+rva-va
        raise ValueError('Unbacked RVA')
    def read(self,rva,n):p=self.offset(rva);return self.b[p:p+n]
    def exported(self,name):
        at=self.offset(self.u32(self.opt+112));count=self.u32(at+24)
        funcs=self.offset(self.u32(at+28));names=self.offset(self.u32(at+32));ords=self.offset(self.u32(at+36))
        for i in range(count):
            p=self.offset(self.u32(names+4*i));end=self.b.index(0,p)
            if self.b[p:end].decode()==name:return self.u32(funcs+4*self.u16(ords+2*i))
        raise ValueError(name)


def sites(build,export):
    retail=PE('C:/Program Files (x86)/Steam/steamapps/common/Starfield/Starfield.exe')
    fixture=PE(build/'sor-d5l-native-fixture.exe');rows=[]
    metadata=[s.split('\t') for s in export.read_text().splitlines() if s.startswith('SITE\t')]
    bodies=[s.split('\t') for s in export.read_text().splitlines() if s.startswith('BODY_BYTES\t')]
    assert bodies
    for _,entry,va,raw in bodies:
        b=bytes.fromhex(raw);assert retail.read(int(va,16)-retail.base,len(b))==b
    assert len(metadata)==len(EVENTS)
    for index,row in enumerate(metadata):
        _,va,n,fall,flows,text,raw=row;rva=int(va,16)-retail.base;n=int(n)
        assert rva==RETAIL_RVAS[index] and retail.read(rva,16)==bytes.fromhex(raw)
        f=fixture.exported(EVENTS[index]);next_f=fixture.exported('after_'+EVENTS[index]);a=retail.read(rva,n);b=fixture.read(f,n)
        # CALL and RIP-relative LEA carry different relocations, same opcode.
        assert (a[:1]==b[:1] if index==2 else a[:3]==b[:3] if index==5 else a==b),(text,a.hex(),b.hex())
        actual_next=int(flows.strip('[]'),16)-retail.base if index in (2,11) else int(fall,16)-retail.base
        assert actual_next==RETAIL_NEXT[index]
        if index==2:assert f+5+struct.unpack('<i',fixture.read(f+1,4))[0]==next_f
        elif index==11:assert f+2+struct.unpack('<b',fixture.read(f+1,1))[0]==next_f
        else:assert f+n==next_f
        rows.append(dict(event=EVENTS[index],rva=rva,next_rva=actual_next,length=n,installed_file_offset=retail.offset(rva),fixture_rva=f,opcode_shape_equal=True))
    return dict(installed_sha256=pin('C:/Program Files (x86)/Steam/steamapps/common/Starfield/Starfield.exe'),export_sha256=pin(export),fixture_sha256=pin(build/'sor-d5l-native-fixture.exe'),sites=rows,backed_functions=len({r[1] for r in bodies}),backed_ranges=len(bodies),backed_bytes=sum(len(r[3])//2 for r in bodies))


def receipts(folder):
    checked=0
    for path in folder.rglob('capture-*.bin'):
        decoder.independent(path);checked+=1
    return checked


if __name__=='__main__':
    build,export,qualification,output=map(lambda x:Path(x).resolve(),sys.argv[1:])
    assert all(p.is_relative_to(LOCAL) for p in (build,export,qualification,output))
    report=sites(build,export);report['independent_receipts']=receipts(qualification)
    output.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report)[:200])
