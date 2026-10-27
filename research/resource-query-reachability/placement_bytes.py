# SPDX-License-Identifier: GPL-3.0-or-later
"""Pin selected concrete placement dispatch slots in the installed PE.

Reads the exact EXE and seven independently located PCMT/PCBN/PCCN slots.
Writes one fresh ignored hash/offset/pointer receipt; stdlib only, no target,
analysis-project, installed-file, original evidence or Git writes. PE mapping
uses owned native_bytes.py method lineage (SOR-P-0002); no source-header code.
"""
from pathlib import Path
import struct
import sys
from native_bytes import EXE, EXPECTED
from audit import LOCAL, pin, write


def main():
    output=Path(sys.argv[1]).resolve()
    assert output.is_relative_to(LOCAL) and not output.exists() and pin(EXE)==EXPECTED
    slots=[('PCMT',0x144b41d80,0x350,0x1407c6080),
           ('PCBN',0x144b41200,0x350,0x1407c1260),
           ('PCBN',0x144b41200,0x358,0x1407c2cb0),
           ('PCBN',0x144b41200,0x370,0x1407c0950),
           ('PCCN',0x144b417d8,0x350,0x1407c3a00),
           ('PCCN',0x144b417d8,0x358,0x1407c3fb0),
           ('PCCN',0x144b417d8,0x370,0x1407c4800)]
    rows=[]
    with EXE.open('rb') as stream:
        stream.seek(0x3c);pe=int.from_bytes(stream.read(4),'little');stream.seek(pe)
        header=stream.read(24);assert header[:4]==b'PE\0\0'
        count,size=struct.unpack_from('<H',header,6)[0],struct.unpack_from('<H',header,20)[0]
        optional=stream.read(size);base=struct.unpack_from('<Q',optional,24)[0]
        assert base==0x140000000
        sections=[stream.read(40) for _ in range(count)]
        for name,table,slot,expected in slots:
            va=table+slot;rva=va-base;offsets=[]
            for section in sections:
                _,start,raw_size,raw=struct.unpack_from('<IIII',section,8)
                if start<=rva and rva+8<=start+raw_size:offsets.append(raw+rva-start)
            assert len(offsets)==1
            stream.seek(offsets[0]);data=stream.read(8)
            actual=struct.unpack('<Q',data)[0];assert actual==expected
            rows.append(dict(form_family=name,table_va=hex(table),slot=hex(slot),
                             pointer_va=hex(va),file_offset=offsets[0],target_va=hex(actual)))
    write(output,dict(exe_sha256=EXPECTED,helper_sha256=pin(Path(__file__)),slots=rows,
        qualification='Exact selected dispatch pointers; runtime form/default identity and graph admission require separate native/data proof'))
    print('Seven concrete placement dispatch pointers match the pinned PE')


if __name__=='__main__':main()
