# SPDX-License-Identifier: GPL-3.0-or-later
"""Pin the retained native original-query to direct-sample dataflow evidence.

Reads one immutable LOCAL-ONLY D5Q export, validates its identity and exact
instruction facts, and writes a fresh ignored static-evidence receipt. No new
disassembly, native execution, target/save/database/network or Git mutation.
Uses owned retained D5Q evidence under SOR-P-0002. A fact census is not a runtime
observation; the authored report explains the def-use and ABI interpretation.
"""
import hashlib
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[2]


def main():
    out=(ROOT/sys.argv[1]).resolve()
    assert out.is_relative_to(ROOT/'.local-work/d5ab')
    out.mkdir(parents=True,exist_ok=False)
    source=ROOT/'.local-work/d5q/export01/native.tsv'
    digest=hashlib.sha256(source.read_bytes()).hexdigest()
    assert digest=='60cc949338e9e0211b87f56c376e1a057d8b7af2da6f9e34a4ae3e84339f8fcd'
    lines=source.read_text(encoding='utf8').splitlines()
    # Retain line digests rather than proprietary instruction text in Git.
    facts={
        '14079f867':'8b20bbff0fffcbb5d3879ba10f5640e39a44e74970b10a38970cd4683678052e',
        '14079f87b':'e71fb16f9bbed2b89f7953190c14d7195730c47fa206f3879c135a8d6d1a37fe',
        '14079fe9e':'87e8ba0580db33a01dbf9809e25cdfbd069d98f4c3df0c577d9559b805d31cec',
        '14079fea1':'b757b0e41ec705e2f2712c574397848f104b5e4728cc91132911c412f7152461',
        '14079fea8':'c8c0273d04ace7086f3775705af3cacd5ae2c8796a00cd624e6f391ce9f935e4',
        '14079feaf':'454ecc8be5828a1afada527e075d4e7a3cb263d7ad011aa54f8977a7a8c95191',
        '14078d6dc':'8cb7b0e5be25d05622a884610adf1d3607e5ef47468e471837f575fb218e63a6',
        '14078d6e5':'0a1e0fa1e07e74e963e66b7e5c37495687ddac045e2327248cb63b5eb955bdf9',
        '14078d6e8':'9ac80a57f12847679452c67270f80f452e5045740e3d8b81d0c6e99971a45d02',
        '14078d6ec':'54725e22923f9cc7c87488ee1482ad4b2fe536e472803707fdcdf22ff4ab87f1',
        '14078d6f0':'efd14f8b6bbc5934d4533f5f5707df474b9e8861da26e8da09acfa71c728134c',
        '14078d6f4':'8f75b25499d873d753446da759b021dd9053542ec97bc463d8c0fc9452dd09c1',
        '14079feb4':'2b5355f9102ccbd872c4cf068eb33d5fea9a1e4c04d7f37a494bb2566ca5f019',
        '14079feb7':'8a8b877e96e820c6094c52b6a0e15f086ea55378a54b102f8d29c3382dab082b',
        '14079febe':'b96055c4eae479bde5b1dc2068481ded0b0663b61900740d7e30aa3742b4385a',
        '14079ff08':'f522f482d91a9c0b90386e88cd1f658d1870a9603c7b2844a5e3c85a7d204573',
        '14079ff0f':'7b681b70345cd4aa4e2320f747e7c1ac17e090ab43f5e8da6134f4b56b0873ef',
        '14079ff13':'a88f9944184702483409bcc4f83ed43b1b84dcd07ef1ae8d1599c246de26ad62',
        '14079ff18':'bc713d69ca21cf118537aea769b708f743074ba5de175c0e34573a94bdceffb4',
        '14079b527':'f511278d7b280b78bd0a214caa22902a0b754cf1678f717439ccf83170fcf041',
        '14079b53e':'fd6f71500b42523f6aac4f8692590beff4c17d97f554c6023684f7c0b8a91520',
        '14079b8dd':'1fce6cb6201328d0547de576402bb14fdc2caced6a9f28ad09fd9b36ffe1d566',
        '14079b8e8':'c8da5f60a3aeac5c1e0ffccf9c61dd9a23600092f3fa19cf095105b4762fe5be',
    }
    rows=[]
    for va,line_hash in facts.items():
        matches=[i for i,line in enumerate(lines) if line.startswith(va+'\t')]
        assert len(matches)==1,va
        index=matches[0]
        assert hashlib.sha256(lines[index].encode()).hexdigest()==line_hash,va
        rows.append(dict(preferred_static_va='0x'+va,line=index+1))
    # Seven pushed nonvolatile registers plus 0x2a0 local allocation move the
    # generator stack by 0x2d8. The saved R8 at entry+0x18 is thus RSP+0x2f0.
    assert 7*8+0x2a0+0x18==0x2f0
    assert -0x2c8+0x2d8==0x10
    result=dict(schema='sor-d5ab-p3-native-query-dataflow/1',passed=True,
                source=str(source),source_sha256=digest,
                image_base='0x140000000',executable_sha256=lines[0].split('\t')[1],
                facts=rows,scope='STATIC direct argument dataflow; no historical or retail occurrence claim.',
                distinction='Original Int2, source-origin Int2 and projected geographic query are separate values/addresses.',
                method_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    (out/'receipt.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf8',newline='\n')
    print(json.dumps(dict(passed=True,facts=len(rows),out=str(out))))


if __name__=='__main__':
    main()
