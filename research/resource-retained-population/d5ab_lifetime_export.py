# SPDX-License-Identifier: GPL-3.0-or-later
"""Read-only source-lifetime census using the owned D5S/D5AA exporter.

Reads existing project and pinned command; writes fresh isolated local output.
No analysis, symbol/type/comment edits, game execution or database mutation.
Requires installed Ghidra/JDK and existing project/identity pins. Writes only a
fresh .local-work/d5ab pass: scripts, caches, commands, native exports and hashes.
The %1a0 pass inventories exact allocation/free size operands, not source types;
receiver and pointer-flow analysis must distinguish unrelated same-size objects.
"""
from pathlib import Path
import hashlib,json,subprocess,sys,ctypes
R=Path('D:/Projects/starfield-outpost-research'); O=R/'.local-work/d5ab'
def sha(p):
    with Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
pins=json.loads((R/'.local-work/d5x/identity05/identity.json').read_text())['database']
assert all(sha(p)==h for p,h in pins.items())
for drive in ('C:/','D:/'):
    free=ctypes.c_ulonglong()
    assert ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(drive),ctypes.byref(free),None,None)
    assert free.value>40_000_000_000
out=O/sys.argv[1];out.mkdir(exist_ok=False)
old=R/'.local-work/d5s/export01'
src=(old/'ExploreD5S.java').read_text()
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
src=src.replace('Function f=currentProgram', '\n'.join([
'if(at.equals("%1a0")){',
'InstructionIterator scan=currentProgram.getListing().getInstructions(true);long scanned=0,candidates=0;',
'while(scan.hasNext()){Instruction i=scan.next();scanned++;String text=i.toString();',
'if(text.equals("MOV ECX,0x1a0")||text.equals("MOV EDX,0x1a0")){',
'Function owner=currentProgram.getFunctionManager().getFunctionContaining(i.getAddress());',
'w.write("CANDIDATE\\t"+(owner==null?"UNKNOWN":owner.getEntryPoint())+"\\t"+i.getAddress()+"\\t"+text+"\\n");candidates++;',
'Instruction next=i;for(int k=0;k<12&&next!=null;k++,next=currentProgram.getListing().getInstructionAfter(next.getAddress()))w.write("CONTEXT\\t"+next.getAddress()+"\\t"+next+"\\n");',
'} }w.write("CENSUS\\t"+scanned+"\\t"+candidates+"\\n");continue;}',
'Function f=currentProgram']))
src=src.replace('Function f=currentProgram', '\n'.join([
'if(at.startsWith("!")){',
'String[] range=at.substring(1).split(":");ghidra.program.model.address.Address lo=toAddr(range[0]),hi=toAddr(range[1]);',
'ghidra.app.util.PseudoDisassembler decoder=new ghidra.app.util.PseudoDisassembler(currentProgram);int count=0;',
'w.write("PSEUDO\\t"+lo+"\\t"+hi+"\\n");',
'while(lo.compareTo(hi)<0){if(++count>64)throw new Exception("Explicit decode bound");',
'ghidra.app.util.PseudoInstruction ins=decoder.disassemble(lo);if(ins==null)throw new Exception("Decode "+lo);',
'w.write(lo+"\\t"+ins+"\\n");lo=lo.add(ins.getLength());if(ins.getMnemonicString().equals("RET"))break;}continue;}',
'Function f=currentProgram']))
(out/'ExploreD5S.java').write_text(src,encoding='utf8',newline='\n')
cmd=[s.replace(str(old),str(out)) for s in json.loads((old/'command.json').read_text())]
at=cmd.index('-postScript');cmd=cmd[:at]+['-postScript','ExploreD5S.java',str(out/'native.tsv'),*sys.argv[2:],'-log',str(out/'ghidra.log'),'-scriptlog',str(out/'script.log')]
for n in ('ghidra-settings','ghidra-cache','java-tmp','java-home'):(out/n).mkdir()
assert '-readOnly' in cmd and '-noanalysis' in cmd
(out/'command.json').write_text(json.dumps(cmd,indent=2)+'\n',encoding='utf8',newline='\n')
with (out/'stdout.log').open('wb') as a,(out/'stderr.log').open('wb') as b:
    result=subprocess.run(cmd,cwd=R,stdout=a,stderr=b,creationflags=subprocess.CREATE_NO_WINDOW)
assert all(sha(p)==h for p,h in pins.items())
assert result.returncode==0
assert (out/'native.tsv').read_text().endswith('END\n')
(out/'preservation.json').write_text(json.dumps(dict(database=pins,database_unchanged=True,sha256=sha(out/'native.tsv'),exporter_sha256=sha(__file__),java_sha256=sha(cmd[0]),java_script_sha256=sha(out/'ExploreD5S.java'),reader_origin_sha256=sha(old/'ExploreD5S.java')),indent=2)+'\n',encoding='utf8',newline='\n')
print(out,sha(out/'native.tsv'))
