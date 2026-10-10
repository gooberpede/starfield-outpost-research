"""SPDX-License-Identifier: GPL-3.0-or-later
Read-only SOR-EXP-0017 PE constants/vtable and installed ESM settings probe.
Explicit local inputs, exclusive ignored JSON output, stdlib/project reader.
No executable/ESM/database/save/network/Git writes. Hashes inputs pre/post;
40-billion-byte available-space floor. Raw definitions remain local.
"""
import argparse
import json
from pathlib import Path
import struct
from inventory_historical_saves import identity, guard
from inspect_outpost_definitions import esm_records


def pe_read(path, va, size):
    with path.open('rb') as f:
        h=f.read(64)
        if h[:2]!=b'MZ': raise ValueError('DOS header')
        nt=struct.unpack_from('<I',h,60)[0]
        f.seek(nt); h=f.read(24)
        if h[:4]!=b'PE\0\0': raise ValueError('PE header')
        n=struct.unpack_from('<H',h,6)[0]; opt=struct.unpack_from('<H',h,20)[0]
        optional=f.read(opt)
        if struct.unpack_from('<H',optional)[0]!=0x20b: raise ValueError('PE64')
        base=struct.unpack_from('<Q',optional,24)[0]
        rva=va-base
        for _ in range(n):
            s=f.read(40)
            vs,rv,rs,off=struct.unpack_from('<4I',s,8)
            if rv<=rva and rva+size<=rv+rs:
                physical=off+rva-rv
                f.seek(physical); b=f.read(size)
                if len(b)!=size: raise ValueError('truncated PE read')
                return dict(va=hex(va),rva=hex(rva),file_offset=physical,hex=b.hex())
    raise ValueError('unbacked PE range')


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('exe',type=Path); ap.add_argument('esm',type=Path); ap.add_argument('output',type=Path)
    a=ap.parse_args(); guard(a.output.parent)
    before=[identity(p) for p in (a.exe,a.esm)]
    constants=[]
    for v,n in [(0x144ae80f0,12),(0x144c24e60,0x58),
        (0x145f0b318,24),(0x145f0b9e0,0x60),(0x144f03f5c,4),(0x144f044e8,4),(0x144f04c5c,4)]:
        try: constants.append(pe_read(a.exe,v,n))
        except ValueError as e: constants.append(dict(va=hex(v),error=str(e)))
    for r in constants:
        raw=bytes.fromhex(r.get('hex',''))
        if len(raw)==4: r['float32']=struct.unpack('<f',raw)[0]
    definitions=[]
    for r,fields in esm_records(a.esm,{b'GMST',b'AVIF',b'KYWD',b'DFOB',b'GLOB',b'ACTI'}):
        edid=fields.get(b'EDID',b'').rstrip(b'\0').decode('utf8','backslashreplace')
        if r['formid'] in (0x63fc5,0x2c60e9) or ('workshop' in edid.lower() and any(s in edid.lower() for s in ('radius','border','buildarea'))):
            r.update(edid=edid,fields={k.decode():v.hex() for k,v in fields.items() if len(v)<=256})
            definitions.append(r)
    after=[identity(p) for p in (a.exe,a.esm)]
    if before!=after: raise ValueError('input changed')
    with a.output.open('x',encoding='utf8',newline='\n') as f:
        json.dump(dict(before=before,after=after,constants=constants,definitions=definitions),f,indent=2);f.write('\n')
    print(json.dumps(dict(constants=constants,definitions=definitions)))


if __name__=='__main__': main()
