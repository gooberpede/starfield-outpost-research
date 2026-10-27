// SPDX-License-Identifier: GPL-3.0-or-later
// Bounded D5H initializer dispatch and byte export; adapted from owned
// ReadDispatch.java. Read-only/no-analysis existing Ghidra program only.
// Reads a fixed caller-supplied function/module list; writes CREATE_NEW local TSV.
// Raw module/function bytes remain local. No symbol/type/comment/project writes.
import ghidra.app.script.GhidraScript;
import ghidra.app.decompiler.*;
import ghidra.program.model.listing.*;
import ghidra.program.model.symbol.*;
import ghidra.program.model.address.*;
import java.nio.file.*;
import java.nio.charset.StandardCharsets;
import java.io.*;
import java.util.*;
public class ReadModules extends GhidraScript {
 public void run() throws Exception {
  String[] args=getScriptArgs();
  Set<String> names=new TreeSet<>(); TreeSet<Long> functions=new TreeSet<>();
  for(String line:Files.readAllLines(Paths.get(args[1]),StandardCharsets.UTF_8)) {
   String[] p=line.split("\\t"); if(p.length!=2)throw new Exception("Invalid fixed input row");
   if(p[0].equals("MODULE"))names.add(p[1]+"::vftable");
   else if(p[0].equals("FUNCTION")&&p[1].matches("[0-9a-f]{9}"))functions.add(Long.parseUnsignedLong(p[1],16));
   else throw new Exception("Invalid fixed query");
  }
  ArrayList<Symbol> symbols=new ArrayList<>();
  SymbolIterator si=currentProgram.getSymbolTable().getAllSymbols(true);
  while(si.hasNext()){Symbol s=si.next();if(s.getName(true).endsWith("::vftable_meta_ptr")||names.contains(s.getName(true)))symbols.add(s);}
  symbols.sort((a,b)->a.getAddress().compareTo(b.getAddress()));
  Set<String> found=new TreeSet<>();TreeSet<Long> callbacks=new TreeSet<>();
  DecompInterface di=new DecompInterface();di.openProgram(currentProgram);
  try(BufferedWriter w=Files.newBufferedWriter(Paths.get(args[0]),StandardCharsets.UTF_8,StandardOpenOption.CREATE_NEW)) {
   w.write("SHA256\t"+currentProgram.getExecutableSHA256()+"\nBASE\t"+currentProgram.getImageBase()+"\n");
   for(int i=0;i<symbols.size();i++) {
    Symbol s=symbols.get(i);if(!names.contains(s.getName(true)))continue;
    long span=Long.MAX_VALUE;
    for(int j=i+1;j<symbols.size();j++)if(symbols.get(j).getName(true).endsWith("::vftable_meta_ptr")){span=symbols.get(j).getAddress().subtract(s.getAddress());break;}
    if(span<0x78){w.write("SHORT_TABLE\t"+s.getName(true)+"\t"+s.getAddress()+"\t"+span+"\n");continue;}
    // The distance to the next RTTI label can include strings or unrelated data.
    // Every invoked IModule slot must actually be an executable code pointer.
    boolean module=true;
    for(long slot=0;slot<0x78;slot+=8) {
     long target=currentProgram.getMemory().getLong(s.getAddress().add(slot));
     ghidra.program.model.mem.MemoryBlock b=currentProgram.getMemory().getBlock(toAddr(target));
     if(b==null||!b.isExecute()){w.write("NON_MODULE_TABLE\t"+s.getName(true)+"\t"+s.getAddress()+"\t"+Long.toHexString(slot)+"\t"+Long.toHexString(target)+"\n");module=false;break;}
    }
    if(!module)continue;
    byte[] data=new byte[0x78];currentProgram.getMemory().getBytes(s.getAddress(),data);
    w.write("TABLE\t"+s.getName(true)+"\t"+s.getAddress()+"\t"+HexFormat.of().formatHex(data)+"\n");found.add(s.getName(true));
    for(long slot:new long[]{0x50,0x58,0x68,0x70}) {
     long target=currentProgram.getMemory().getLong(s.getAddress().add(slot));
     w.write("DISPATCH\t"+s.getName(true)+"\t"+s.getAddress()+"\t"+Long.toHexString(slot)+"\t"+Long.toHexString(target)+"\n");
     callbacks.add(target); functions.add(target);
    }
   }
   if(!found.equals(names))throw new Exception("Missing complete module tables: expected "+names+" found "+found);
   w.flush();
   for(long va:functions) {
    Function f=currentProgram.getFunctionManager().getFunctionAt(toAddr(va));
    if(f==null)throw new Exception("Missing exact function "+Long.toHexString(va));
    w.write("FUNCTION\t"+f.getEntryPoint()+"\n");
    AddressRangeIterator ranges=f.getBody().getAddressRanges();
    while(ranges.hasNext()) {
     AddressRange range=ranges.next();byte[] bytes=new byte[Math.toIntExact(range.getLength())];
     currentProgram.getMemory().getBytes(range.getMinAddress(),bytes);
     w.write("RANGE\t"+range.getMinAddress()+"\t"+HexFormat.of().formatHex(bytes)+"\n");
    }
    if(callbacks.contains(va)) {
     InstructionIterator ii=currentProgram.getListing().getInstructions(f.getBody(),true);
     while(ii.hasNext()){Instruction in=ii.next();w.write(in.getAddress()+"\t"+in+"\n");}
     DecompileResults dr=di.decompileFunction(f,120,monitor);
     if(!dr.decompileCompleted())throw new Exception(dr.getErrorMessage());
     w.write("DECOMPILED\n"+dr.getDecompiledFunction().getC()+"\n");
    }
    w.flush();
   }
   w.write("END\n");
  }finally{di.dispose();}
 }
}
