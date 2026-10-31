# SPDX-License-Identifier: GPL-3.0-or-later
"""Read-only Ghidra exports using the repository-owned D5S reader.

Adapted from `.local-work/d5aa/native.py`.
Origin SHA-256: `2e09a065f3161c7e87b1faef88de71187a7ea91b33a94e9cf647e8b06a63c5d9`
The owned D5S Java reader and command remain local prerequisites; the native
export keeps proprietary bytes local. This script documents every launch argument.


Reads existing project and pinned command; writes fresh isolated local output.
No analysis, symbol changes, executable invocation or database mutation.
"""
from pathlib import Path
import hashlib,json,subprocess,sys,ctypes
R=Path(__file__).resolve().parents[2]; O=R/'.local-work/d5aa'
def sha(p):
    with Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
pins=json.loads((R/'.local-work/d5x/identity05/identity.json').read_text(encoding='utf8'))['database']
assert all(sha(p)==h for p,h in pins.items())
for drive in ('C:/','D:/'):
    free=ctypes.c_ulonglong()
    assert ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(drive),ctypes.byref(free),None,None)
    assert free.value>40_000_000_000
assert sys.argv[1].replace('-', '').isalnum()
out=O/sys.argv[1];out.mkdir(exist_ok=False)
old=R/'.local-work/d5s/export01'
src=(old/'ExploreD5S.java').read_text(encoding='utf8')
src=src.replace('Function f=currentProgram','''if(at.startsWith("@")){
String[] parts=at.substring(1).split(":");ghidra.program.model.address.Address base=toAddr(parts[0]);int length=Integer.parseInt(parts[1]);
if(length>4096)throw new Exception("Data bound");
for(int off=0;off<length;off+=8){ghidra.program.model.address.Address address=base.add(off);w.write("DATA\\t"+address+"\\t"+Long.toUnsignedString(currentProgram.getMemory().getLong(address),16)+"\\n");
ReferenceIterator rr=currentProgram.getReferenceManager().getReferencesTo(address);while(rr.hasNext())w.write("DXREF\\t"+rr.next()+"\\n");}continue;}
if(at.startsWith("?")){String needle=at.substring(1);
SymbolIterator si=currentProgram.getSymbolTable().getAllSymbols(true);int matches=0;
while(si.hasNext()){Symbol sy=si.next();String fullname=sy.getName(true);if(fullname.toLowerCase().contains(needle.toLowerCase())){
if(++matches>20000)throw new Exception("Symbol output bound");
w.write("SYMBOL\\t"+sy.getAddress()+"\\t"+fullname+"\\n");}}continue;}
Function f=currentProgram''')
(out/'ExploreD5S.java').write_text(src,encoding='utf8',newline='\n')
cmd=[s.replace(str(old),str(out)) for s in json.loads((old/'command.json').read_text(encoding='utf8'))]
at=cmd.index('-postScript');cmd=cmd[:at]+['-postScript','ExploreD5S.java',str(out/'native.tsv'),*sys.argv[2:],'-log',str(out/'ghidra.log'),'-scriptlog',str(out/'script.log')]
for n in ('ghidra-settings','ghidra-cache','java-tmp','java-home'):(out/n).mkdir()
assert '-readOnly' in cmd and '-noanalysis' in cmd
(out/'command.json').write_text(json.dumps(cmd,indent=2)+'\n',encoding='utf8',newline='\n')
with (out/'stdout.log').open('wb') as a,(out/'stderr.log').open('wb') as b:
    result=subprocess.run(cmd,cwd=R,stdout=a,stderr=b,creationflags=subprocess.CREATE_NO_WINDOW)
assert all(sha(p)==h for p,h in pins.items())
assert result.returncode==0
assert (out/'native.tsv').read_text(encoding='utf8').endswith('END\n')
print(out,sha(out/'native.tsv'))
