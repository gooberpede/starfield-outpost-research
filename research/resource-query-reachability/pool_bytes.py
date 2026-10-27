# SPDX-License-Identifier: GPL-3.0-or-later
"""Read two exact pool-worker dispatch tables from the pinned installed PE.

Stdlib; owned D5H PE-mapping lineage. Writes a fresh ignored pointer/hash receipt.
No target, installed-file, analysis-project, original-evidence or Git writes.
Receiver/capture/consumer semantics require the separate native proof.
"""
import hashlib
from pathlib import Path
import struct
import sys
from audit import LOCAL, pin, write
from native_bytes import EXE, EXPECTED


def main():
    output=Path(sys.argv[1]).resolve()
    assert output.is_relative_to(LOCAL) and not output.exists() and pin(EXE)==EXPECTED
    rows=[]
    with EXE.open('rb') as stream:
        stream.seek(0x3c);pe=int.from_bytes(stream.read(4),'little');stream.seek(pe)
        header=stream.read(24);assert header[:4]==b'PE\0\0'
        optional=stream.read(struct.unpack_from('<H',header,20)[0])
        base=struct.unpack_from('<Q',optional,24)[0];assert base==0x140000000
        sections=[stream.read(40) for _ in range(struct.unpack_from('<H',header,6)[0])]
        for name,va in [('worker capture',0x144da7d08),('GroupThread',0x144da7d58)]:
            rva=va-base;offsets=[]
            for section in sections:
                _,start,size,raw=struct.unpack_from('<IIII',section,8)
                if start<=rva and rva+24<=start+size:offsets.append(raw+rva-start)
            assert len(offsets)==1
            stream.seek(offsets[0]);data=stream.read(24)
            slots={hex(i*8):hex(value) for i,value in enumerate(struct.unpack('<3Q',data))}
            if name=='worker capture':assert slots['0x10']=='0x1428d79b0'
            rows.append(dict(name=name,va=hex(va),file_offset=offsets[0],
                             bytes=24,sha256=hashlib.sha256(data).hexdigest(),slots=slots))
    write(output,dict(exe_sha256=EXPECTED,helper_sha256=pin(Path(__file__)),tables=rows,
        qualification='Exact selected PE dispatch bytes only; no runtime execution or receiver-lifetime claim'))
    print({row['name']:row['slots'] for row in rows})


if __name__=='__main__':main()
