# SPDX-License-Identifier: GPL-3.0-or-later
"""Match bounded Ghidra module/function bytes against the pinned installed PE.

Reads the task's local ReadModules export and EXE. Writes one exclusive ignored
hash/offset receipt, containing no raw native bytes. Verifies byte identity,
not semantic function completeness, analysis labels, reachability or execution.
Stdlib only; PE mapping adapted from owned native_bytes.py under SOR-P-0002.
No target, save, analysis-project, archive, original-input or Git writes.
"""
import hashlib
from pathlib import Path
import struct
import sys
from audit import ROOT, LOCAL, pin, write
from native_bytes import EXE, EXPECTED


def main():
    source=Path(sys.argv[1]).resolve();output=Path(sys.argv[2]).resolve()
    assert source.is_relative_to(ROOT/'.local-work') and output.is_relative_to(LOCAL) and not output.exists()
    text=source.read_text();assert text.startswith('SHA256\t'+EXPECTED+'\nBASE\t140000000\n') and text.endswith('END\n')
    assert pin(EXE)==EXPECTED
    functions={};tables=[];active=None
    with EXE.open('rb') as f:
        f.seek(0x3c);pe=int.from_bytes(f.read(4),'little');f.seek(pe)
        head=f.read(24);assert head[:4]==b'PE\0\0'
        count=struct.unpack_from('<H',head,6)[0];size=struct.unpack_from('<H',head,20)[0]
        optional=f.read(size);base=struct.unpack_from('<Q',optional,24)[0];assert base==0x140000000
        sections=[f.read(40) for _ in range(count)]
        def compare(va,expected):
            rva=va-base;matches=[]
            for s in sections:
                _,start,raw_size,offset=struct.unpack_from('<IIII',s,8)
                if start<=rva and rva+len(expected)<=start+raw_size:matches.append(offset+rva-start)
            assert len(matches)==1,(hex(va),len(expected))
            f.seek(matches[0]);actual=f.read(len(expected));assert actual==expected,hex(va)
            return dict(va=hex(va),rva=hex(rva),file_offset=matches[0],bytes=len(actual),sha256=hashlib.sha256(actual).hexdigest())
        for line in text.splitlines():
            p=line.split('\t')
            if p[0]=='FUNCTION':
                active=p[1];assert active not in functions;functions[active]=[]
            elif p[0]=='RANGE':
                assert active is not None;functions[active].append(compare(int(p[1],16),bytes.fromhex(p[2])))
            elif p[0]=='TABLE':
                row=compare(int(p[2],16),bytes.fromhex(p[3]));row['name']=p[1];tables.append(row)
    assert functions and tables and all(functions.values())
    # Hash the ordered range identity, lengths and individual content hashes;
    # never present it as the hash of a fictitious contiguous function interval.
    digest=lambda rows:hashlib.sha256(b''.join(struct.pack('<QI',int(r['va'],16),r['bytes'])+bytes.fromhex(r['sha256']) for r in rows)).hexdigest()
    write(output,dict(exe_sha256=EXPECTED,export=str(source.relative_to(ROOT)),export_sha256=pin(source),
        helper_sha256=pin(Path(__file__)),java_sha256=pin(ROOT/'research/resource-query-reachability/ReadModules.java'),
        functions={va:dict(ranges=rows,range_set_sha256=digest(rows)) for va,rows in functions.items()},tables=tables,
        qualification='Exact backing bytes for Ghidra-defined body ranges and selected module tables; not a semantic extent/writer/reachability proof'))
    print('Installed PE byte matches:',len(functions),'function range sets;',len(tables),'module tables')


if __name__=='__main__':main()
