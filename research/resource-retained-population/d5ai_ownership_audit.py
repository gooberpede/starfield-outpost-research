# SPDX-License-Identifier: GPL-3.0-or-later
"""Authenticate bounded ownership windows and classify their native references.

Reads pinned retained exports, the disposable export receipt and installed PE.
Writes fresh ignored static-audit JSON and a requested authored CSV source ledger.
No instructions execute, no database opens, and no protected inputs change.
The PE exception-directory parser is owned analysis; it identifies embedded
chained RUNTIME_FUNCTION records rather than guessing that data xrefs are calls.
"""
import sys
if not __debug__ or sys.flags.optimize:
    raise RuntimeError('Use Python -E -B without -O/-OO')
from pathlib import Path
import csv
import ctypes
import hashlib
import json
import re
import struct

ROOT=Path(__file__).resolve().parents[2]
PIN='7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28'
sha=lambda b:hashlib.sha256(b).hexdigest()
out=(ROOT/sys.argv[1]).resolve()
if not out.is_relative_to(ROOT/'.local-work/d5ai-ownership') or out.exists():
    raise ValueError('Fresh ignored output required')
free={}
for drive in ('C:/','D:/'):
    n=ctypes.c_ulonglong()
    if not ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(drive),ctypes.byref(n),None,None):
        raise OSError('Disk query failed')
    if n.value<40_000_000_000: raise RuntimeError('Disk floor')
    free[drive]=n.value
data=Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield/Starfield.exe').read_bytes()
if sha(data)!=PIN: raise ValueError('Executable mismatch')
pe=struct.unpack_from('<I',data,0x3c)[0]; opt=pe+24
sections=[]
for i in range(struct.unpack_from('<H',data,pe+6)[0]):
    at=opt+struct.unpack_from('<H',data,pe+20)[0]+40*i
    sections.append((data[at:at+8].rstrip(b'\0').decode(),*struct.unpack_from('<IIII',data,at+8)))
def offset(rva):
    for name,size,va,rawsize,raw in sections:
        if va<=rva<va+rawsize:return raw+rva-va
    raise ValueError(hex(rva))
def section(rva):
    return next(name for name,size,va,rawsize,raw in sections if va<=rva<va+rawsize)
directory,size=struct.unpack_from('<II',data,opt+112+24)
chains={}
for at in range(directory,directory+size,12):
    begin,end,unwind=struct.unpack_from('<III',data,offset(at))
    flags=data[offset(unwind)]>>3
    if flags&4:
        count=data[offset(unwind)+2]
        chain=unwind+((4+count*2+3)&~3)
        target=struct.unpack_from('<III',data,offset(chain))
        chains[chain]=(begin,end,unwind,target)
fresh=json.loads((ROOT/'.local-work/d5ai-ownership/export01/result.json').read_bytes())
if not fresh['original_core_preserved'] or not fresh['copy_core_preserved'] or fresh['exit']:
    raise ValueError('Disposable project preservation')
sources=[
('.local-work/d5s/export04/native.tsv','4cffd7d5b30f102d6080b241aad0fefce609a03957ee71897d5fb68b400c50f8',
 ('14079a330','1407ac2f0','1407ac0d0','14079b520')),
('.local-work/d5s/export08/native.tsv','fd0cbc75eaf2575de30acb5068087da0dcfbb0b8fdc5b9fcf60c7287fe42b081',
 ('1407ac260','1407a97c0','1407aa9b0')),
('.local-work/d5s/export11/native.tsv','83c14430825400628dccd5ecfe9357f266b3e1a258897b51ec23a86294cd3ed9',('14079c470',)),
('.local-work/d5q/export01/native.tsv','60cc949338e9e0211b87f56c376e1a057d8b7af2da6f9e34a4ae3e84339f8fcd',('14079f860',)),
('.local-work/d5v/export01/native.tsv','10b853e420d4aa5e97935bb5591bc16a23d15cfa1db2a692fee0ca00754f66e3',
 ('1421e07d0','1421e0f50','14079ddf0','140982b70','1409829b0')),
('.local-work/d5v/export02/native.tsv','fba0aef8b33cdee01cce3d8c8f53e7527d50fc71bd60d749c1da5767dcad9234',('140982d90',)),
('.local-work/d5v/export04/native.tsv','c2e4216835dbd41e6dc16a3a1b3c911b773ab63a70299e4045b864698b31510e',('14079df70',)),
('.local-work/d5v/export05/native.tsv','449f6e9f8678d93870bd7825f590af31632b8a128971ba9ed8611b76c4d43658',('1407affb0',)),
('.local-work/d5af/prelock-export01/native.tsv','bad793664b90b987bd5dc4d91fb70936a2d9590029b17dc2eb7e7d1e2c807b47',('1422cc350','1422cc3d0','1402c45a0')),
('.local-work/d5ah-extractor/export02/native.tsv','647a07d95df2f3301e0596dda4fecad148f3063ea35178f1610094fa79fc3911',('140975030','1407aa8a0','1407aab10')),
('.local-work/d5ai-ownership/export01/native.tsv',fresh['native_sha256'],('1407ab730','1407abc90','1407aabd0','1407ab8c0','1407a9650','1407ab510','14079d910')),
('.local-work/d5s/export55/native.tsv','c1326c505bd28a4ab75343ecc5141d5bec6e203636773c17ecc5506c2d5006e3',('14078d660',))]
rows=[]; references=[]
for path,pin,entries in sources:
    raw=(ROOT/path).read_bytes()
    if sha(raw)!=pin:raise ValueError(path)
    lines=raw.decode('utf8').splitlines()
    for entry in entries:
        start=next(i for i,s in enumerate(lines) if s.startswith('FUNCTION\t'+entry+'\t'))
        end=next(i for i in range(start,len(lines)) if lines[i]=='END_FUNCTION')
        rows.append(dict(id=f'D5AI-OWN-{len(rows)+1:02}',path=path,sha256=pin,static_va='0x'+entry,
                         first_line=start+1,last_line=end+1,eligibility='LOCAL-ONLY',
                         lineage='Bethesda primary native; retained export' if 'd5ai-ownership' not in path else 'Bethesda primary native; verified disposable export'))
        for line in lines[start:end]:
            m=re.match(r'XREF\tFrom: ([0-9a-f]+) To: ([0-9a-f]+) Type: (\S+)',line)
            if not m:continue
            address,target,kind=m.groups(); rva=int(address,16)-0x140000000
            disposition='code-reference' if section(rva)=='.text' else 'unclassified-data'
            if section(rva)=='.pdata':disposition='exception-directory'
            if rva in chains and chains[rva][3][0]==int(entry,16)-0x140000000:
                disposition='chained-runtime-function'
            references.append(dict(target='0x'+target,source='0x'+address,type=kind,section=section(rva),disposition=disposition))
# Every data reference in the core construction/copy chain must be metadata,
# not an unexamined virtual or asynchronous caller.
core={'0x'+s for s in ('14079a330','1407ac2f0','1407ac0d0','14079b520','14079c470','1407a97c0','1407aa9b0','1407aabd0','1407abc90')}
unknown=[r for r in references if r['target'] in core and r['disposition']=='unclassified-data']
if unknown:raise ValueError(unknown)
out.parent.mkdir(parents=True,exist_ok=True)
result=dict(scope='Bounded native graph, direct cross-references and chained-unwind metadata; no universal indirect-call census',
            executable_sha256=PIN,method_sha256=sha(Path(__file__).read_bytes()),sources=rows,references=references,
            unclassified_core_data_references=unknown,free=free,disposable_export_sha256=sha((ROOT/'.local-work/d5ai-ownership/export01/result.json').read_bytes()))
out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf8',newline='\n')
if len(sys.argv)>2:
    destination=(ROOT/sys.argv[2]).resolve()
    if destination!=ROOT/'docs/experiments/resource-retained-population/d5ai-ownership-sources.csv':raise ValueError('Only task source CSV')
    with destination.open('w',encoding='utf8',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(rows[0]),lineterminator='\n');writer.writeheader();writer.writerows(rows)
print('PASS',len(rows),'windows',len(references),'references',out)
