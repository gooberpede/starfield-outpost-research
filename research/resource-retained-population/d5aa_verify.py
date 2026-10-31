# SPDX-License-Identifier: GPL-3.0-or-later
"""Verify D5AA original preservation, static edges and source locators offline.

Reads the fresh D5Y authentication inventory, installed EXE, existing database,
seven read-only native exports and exact protected Save52 originals/copy. Writes
only a fresh .local-work receipt directory and optional authored source CSV.
Stdlib only. Never runs game/native code, mutates a save/database or stages Git.
PE mapping below is original bounded code, not an imported parser.
"""
import csv
import ctypes
import hashlib
import json
from pathlib import Path
import re
import struct
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[2]
EXPORTS=['392bebecef84c96608ba64664307ae9938be77de49e1203c0438357d5adfd7e7','bd0ad17a953ee1de657c3a42c3a23235605cb8284aad912c8efb74bf6531a56c','34db2d9f584ca22f082bdf884182027993b24fe987ca712ceec9446e289635e5','d2f7b8db71540e14c01ab8966043e0b60d9b0bc4a4effb00396086656abbe967','ea5f840af3a5a502941a0cbf76ae70d1955f573f62b3ed1183229830e1733fda','d719d0f5af42c47b5b6a6e9940912c49897c858df66558191556272994cb27c3','e48ea527f32c065652a38b7932fdb37ca285372a90fc553a7cae2efb26ce0614']

def sha(p):
    with Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()

def main(label,source_csv=None):
    assert label.replace('-','').isalnum();out=ROOT/'.local-work/d5aa'/label;assert not out.exists()
    free={}
    for drive in ('C:/','D:/'):
        value=ctypes.c_ulonglong();assert ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(drive),ctypes.byref(value),None,None)
        assert value.value>=40_000_000_000;free[drive]=value.value
    auth=json.loads((ROOT/'.local-work/d5y/d5aa-auth01/analysis.json').read_text(encoding='utf8'))
    inputs=auth['input_hashes'].copy()
    db=json.loads((ROOT/'.local-work/d5x/identity05/identity.json').read_text(encoding='utf8'))['database'];inputs.update(db)
    inputs[str(ROOT/'.local-work/d5x-b1-live/attempt01/capture01.zip')]=auth['archive_sha256']
    policy=json.loads((ROOT/'research/resource-carinae-source-context/save_policy.json').read_text(encoding='utf8'))
    name=next(n for n in policy['designated'] if n.startswith('Save52_'));save=policy['designated'][name]
    for folder in (ROOT/'.local-work/savegames',Path('C:/Users/User/Documents/My Games/Starfield/Saves')):
        p=folder/name;assert p.stat().st_size==save['bytes'];inputs[str(p)]=save['sha256']
    for p,h in inputs.items():assert sha(p)==h,p
    exe=Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield/Starfield.exe')
    image=exe.read_bytes();assert hashlib.sha256(image).hexdigest()=='7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28'
    pe=struct.unpack_from('<I',image,0x3c)[0];assert image[pe:pe+4]==b'PE\0\0'
    count=struct.unpack_from('<H',image,pe+6)[0];opt=struct.unpack_from('<H',image,pe+20)[0]
    sections=[]
    for i in range(count):
        at=pe+24+opt+40*i
        size,rva,rawsize,raw=struct.unpack_from('<4I',image,at+8);sections.append((rva,size,raw,rawsize))
    def offset(va,n=1):
        rva=va-0x140000000
        matches=[raw+rva-base for base,size,raw,rawsize in sections if base<=rva and rva+n<=base+rawsize]
        assert len(matches)==1;return matches[0]
    calls=0;rows=[]
    for i,pin in enumerate(EXPORTS,1):
        p=ROOT/f'.local-work/d5aa/export{i:02}/native.tsv';assert sha(p)==pin
        t=p.read_text(encoding='utf8');assert t.startswith('SHA256\t'+inputs[str(exe)]) and t.endswith('END\n')
        for at,target in re.findall(r'^([0-9a-f]+)\tCALL 0x([0-9a-f]+)\s*$',t,re.M):
            va=int(at,16);off=offset(va,5);assert image[off]==0xe8
            assert va+5+struct.unpack_from('<i',image,off+1)[0]==int(target,16);calls+=1
        seen=set()
        for m in re.finditer(r'^FUNCTION\t([^\t\r\n]+)\t([^\n]+).*?(?=^FUNCTION\t|^END$|\Z)',t,re.M|re.S):
            if m[1] in seen:continue
            seen.add(m[1]);entry=int(m[1],16)
            rows.append(dict(id=f'AA-N{i:02}-{len(seen):02}',kind='READ-ONLY NATIVE EXPORT',path=str(p.relative_to(ROOT)).replace('\\','/'),sha256=pin,domain='PREFERRED STATIC VA; PE FILE OFFSET',locator='0x'+m[1],pe_file_offset=hex(offset(entry)),line_start=t[:m.start()].count('\n')+1,line_end=t[:m.end()].count('\n'),use='Compiled caller, predicate, operand or dispatch proof; see transition map',classification='LOCAL-ONLY'))
    for va,target in ((0x144c943d0,0x1416d3c20),(0x144c84978,0x1415f6520)):
        assert struct.unpack_from('<Q',image,offset(va,8))[0]==target
    source_paths=['.local-work/d5aa/initial.json','.local-work/d5y/d5aa-auth01/analysis.json','.local-work/d5aa/resets01/b1.json','.local-work/d5aa/checks01/checks.json','.local-work/d5aa/checks01/capacity-sensitivity.csv','.local-work/d5x-b1-live/attempt01/archive01.json','.local-work/d5z/b1-02/b1.json','runtime/construction-winner/observer.h','runtime/construction-winner/transport.h','runtime/construction-winner/plugin.cpp','runtime/construction-winner/read_capture.py','research/resource-retained-population/d5y_forensics.py','research/resource-retained-population/d5z_b1.py','research/resource-retained-population/d5z_export.py']
    source_paths += [str(p.relative_to(ROOT)).replace('\\','/') for p in (ROOT/'research/resource-retained-population').glob('d5aa_*.py')]
    source_paths += ['.local-work/d5s/export01/ExploreD5S.java','.local-work/d5s/export01/command.json','.local-work/d5aa/native.py','.local-work/d5aa/render.cjs','.local-work/d5aa/checks02/checks.json','.local-work/d5aa/qa03/quality.json']
    source_paths += ['.local-work/d5aa/checks03/checks.json']
    source_paths += [f'.local-work/d5aa/export{i:02}/{name}' for i in range(1,8) for name in ('ExploreD5S.java','command.json')]
    source_paths += [f'docs/experiments/resource-retained-population/{s}' for s in ('d5q-call-dataflow-map.md','d5r-query-scheduling-map.md','d5s-query-winner-model.md','d5v-lifecycle-consumer-map.md','d5w-normal-path-model.md','d5y-report.md','d5z-report.md','d5z-state-transition-map.md','d5z-state-access.csv','d5z-sources.csv')]
    for name in sorted(set(source_paths)):
        p=ROOT/name;rows.append(dict(id=f'AA-S{len(rows)+1:03}',kind='OWNED METHOD / PRIOR EVIDENCE',path=name,sha256=sha(p),domain='FILE',locator='whole file; claim-specific sections in report',pe_file_offset='',line_start='',line_end='',use='Provenance or inherited scoped mechanism; SOR-P-0002 for owned methods',classification='LOCAL-ONLY' if name.startswith('.local-work') else 'REVIEW-REQUIRED'))
    for tool in (Path(sys.executable),Path('C:/Users/User/AppData/Local/Programs/Eclipse Adoptium/jdk-21.0.12.8-hotspot/bin/java.exe'),Path('D:/tools/ghidra_12.1.2_PUBLIC/Ghidra/Framework/Utility/lib/Utility.jar'),Path('C:/Users/User/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp/package.json')):
        rows.append(dict(id=f'AA-TOOL{len(rows)+1:03}',kind='INSTALLED STANDALONE TOOL',path=str(tool),sha256=sha(tool),domain='FILE',locator='installed tool identity',pe_file_offset='',line_start='',line_end='',use='Existing read-only analysis/rendering tool; no implementation incorporation',classification='LOCAL-ONLY'))
    rows.append(dict(id='AA-RAW',kind='AUTHENTICATED B1 RAW',path='.local-work/d5x/live/session-ceb439b14ddc4db8b734526a124f1e879b64cd457774a87a6a67852fd4489894/events.bin',sha256=auth['raw_sha256'],domain='RAW FILE BYTE OFFSET',locator='328*(sequence-1); payload +16; exact references in d5aa/events.csv',pe_file_offset='',line_start='',line_end='',use='19780 admitted frames; never substitute integrity for semantics',classification='LOCAL-ONLY'))
    out.mkdir()
    if source_csv:
        path=Path(source_csv).resolve();assert path==ROOT/'docs/experiments/resource-retained-population/d5aa-sources.csv'
        with path.open('w',encoding='utf8',newline='') as f:
            w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
    for p,h in inputs.items():assert sha(p)==h,p
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip();index=sha(ROOT/'.git/index')
    assert head==auth['head'] and index==auth['index_sha256']
    receipt=dict(head=head,index_sha256=index,free=free,original_inputs=inputs,database_unchanged=True,protected_save52=save,verified_direct_calls=calls,callback_table_checks=2,exports=EXPORTS,sources=len(rows),limits='Specific Save52 and selected originals only; not a complete active-save audit or live preflight.')
    (out/'verification.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf8',newline='\n');print(json.dumps({k:v for k,v in receipt.items() if k not in ('original_inputs','exports','protected_save52')},indent=2))

if __name__=='__main__':main(*sys.argv[1:])
