# SPDX-License-Identifier: GPL-3.0-or-later
"""Read pinned PE and exports, write local instruction receipts (hashes, no bytes).

No executable loading, disassembly execution, project writes, or target calls.
"""
import hashlib
import json
from pathlib import Path
import struct

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'.local-work/internal-observation-qualification'
GAME=Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield/Starfield.exe')


def main():
    data=GAME.read_bytes()
    assert hashlib.sha256(data).hexdigest()=='7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28'
    pe=struct.unpack_from('<I',data,0x3c)[0]
    assert data[pe:pe+4]==b'PE\0\0'
    count=struct.unpack_from('<H',data,pe+6)[0]; size=struct.unpack_from('<H',data,pe+20)[0]
    assert struct.unpack_from('<Q',data,pe+24+24)[0]==0x140000000
    sections=[]
    for i in range(count):
        off=pe+24+size+40*i
        virtual_size,rva,raw_size,raw=struct.unpack_from('<4I',data,off+8)
        sections.append((rva,raw_size,raw))
    sites=[]
    for rva,length in [(0x21e1060,3),(0x21e174e,4),(0x21e1772,4)]:
        matches=[raw+rva-start for start,n,raw in sections if start<=rva and rva+length<=start+n]
        assert len(matches)==1
        file_offset=matches[0]
        sites.append(dict(rva=hex(rva),continuation_rva=hex(rva+length),
                          file_offset=file_offset,length=length,
                          sha256=hashlib.sha256(data[file_offset:file_offset+length]).hexdigest()))
    source=ROOT/'.local-work/recon/resource-availability-ui-16.tsv'; text=source.read_text()
    assert [s['sha256'] for s in sites]==[
        '846d5300049dd03272bc0f077d31504adeaa436fbc57f91634e530d90eb0506b',
        '2bd578ff1687c5184959c9d184d7a67e04031beed898aade6b1ab79e673d3f2e',
        'cc8d19354ef1ca3315dccb0616ed49ed068c05d54bc612497396d2ffe691c04b']
    assert hashlib.sha256(source.read_bytes()).hexdigest()=='3e29f0c813e9a49aa9c53eada6dee052056dfd659979aeea89868fe7c8447aca'
    facts=['1421e1060\tMOV R8B,0x1','1421e1119\tVSUBPS XMM3,XMM2,XMM0',
           '1421e1140\tJA 0x1421e174e','1421e114c\tJZ 0x1421e1772',
           '1421e1154\tJZ 0x1421e174e','1421e145c\tMOV AL,0x1',
           '1421e1460\tJNZ 0x1421e1761','1421e16d4\tJBE 0x1421e1761',
           '1421e1714\tJBE 0x1421e1761','1421e174e\tADD RBX,0x30',
           '1421e1772\tMOV RBX,qword ptr [RSI + 0x8]','1421e18f2\tMOV EAX,0x1']
    assert all(x in text for x in facts)
    report=dict(build='1.16.244.0',image_base='0x140000000',sites=sites,
                export_instruction_assertions=len(facts),scope='Read-only bytes/exports; not patch admission')
    (OUT/'static-contract.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report))


if __name__=='__main__': main()
