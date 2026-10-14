// SPDX-License-Identifier: GPL-3.0-or-later
// Original read-only exporter. No analysis, symbol, type or comment changes.
// Reads currentProgram functions, writes CREATE_NEW local TSV only.
import ghidra.app.script.GhidraScript;
import ghidra.app.decompiler.*;
import ghidra.program.model.listing.*;
import java.nio.file.*;
import java.nio.charset.StandardCharsets;
import java.io.*;
public class ReadSpecialist extends GhidraScript {
 public void run() throws Exception {
  String[] args = getScriptArgs();
  DecompInterface di = new DecompInterface();
  di.openProgram(currentProgram);
  try (BufferedWriter w = Files.newBufferedWriter(Paths.get(args[0]),
       StandardCharsets.UTF_8, StandardOpenOption.CREATE_NEW)) {
   w.write("SHA256\t" + currentProgram.getExecutableSHA256() + "\nBASE\t" + currentProgram.getImageBase() + "\n");
   for (int n=1; n<args.length; n++) {
    if (args[n].startsWith("vloads:")) {
 java.util.ArrayList<ghidra.program.model.symbol.Symbol> ss=new java.util.ArrayList<>();
 ghidra.program.model.symbol.SymbolIterator sit=currentProgram.getSymbolTable().getAllSymbols(true);
 while(sit.hasNext()){ghidra.program.model.symbol.Symbol sy=sit.next();String nm=sy.getName(true);if((nm.contains("Activity")&&nm.endsWith("::vftable"))||nm.endsWith("::vftable_meta_ptr"))ss.add(sy);}
 ss.sort((x,y)->x.getAddress().compareTo(y.getAddress()));
 java.util.TreeSet<Long> fs=new java.util.TreeSet<>();
 for(int k=0;k<ss.size();k++){ghidra.program.model.symbol.Symbol sy=ss.get(k);String nm=sy.getName(true);boolean wantFactories=args[n].endsWith("48");if(!nm.endsWith("::vftable")||(wantFactories?(!nm.startsWith("BGS")||nm.contains("Runtime")||nm.contains("<")||!nm.endsWith("Activity::vftable")):!nm.contains("Runtime")))continue;long delta=Long.MAX_VALUE;for(int j=k+1;j<ss.size();j++){if(ss.get(j).getName(true).endsWith("::vftable_meta_ptr")){delta=ss.get(j).getAddress().subtract(sy.getAddress());break;}}
 long slot=args[n].endsWith("48")?0x48:args[n].endsWith("90")?0x90:0x70; if(delta<slot+8){w.write("SHORT_VTABLE\t"+sy.getAddress()+"\t"+delta+"\t"+nm+"\n");continue;}
 long v=currentProgram.getMemory().getLong(sy.getAddress().add(slot));w.write("LOAD_SLOT\t"+sy.getAddress()+"\t"+nm+"\t"+Long.toHexString(v)+"\t"+delta+"\n");fs.add(v);}
 for(long va:fs){Function f=currentProgram.getFunctionManager().getFunctionAt(toAddr(va));if(f==null){w.write("NO_FUNCTION\t"+Long.toHexString(va)+"\n");continue;}w.write("FUNCTION\t"+f.getEntryPoint()+"\n");DecompileResults dr=di.decompileFunction(f,120,monitor);if(!dr.decompileCompleted())throw new Exception(dr.getErrorMessage());w.write("DECOMPILED\n"+dr.getDecompiledFunction().getC()+"\n");}continue;
}
    if (args[n].startsWith("sym:")) { String z=args[n].substring(4).toLowerCase(); ghidra.program.model.symbol.SymbolIterator it=currentProgram.getSymbolTable().getAllSymbols(true);while(it.hasNext()){ghidra.program.model.symbol.Symbol sy=it.next();if(sy.getName(true).toLowerCase().contains(z))w.write("SYMBOL\t"+sy.getAddress()+"\t"+sy.getName(true)+"\n");}continue;}
    if (args[n].startsWith("ins:")) { String[] z=args[n].split(":"); InstructionIterator it=currentProgram.getListing().getInstructions(toAddr(z[1]),true); while(it.hasNext()){Instruction i=it.next();if(i.getAddress().compareTo(toAddr(z[2]))>=0)break;w.write(i.getAddress()+"\t"+i+"\n");}continue; }
    if (args[n].startsWith("data:")) {
     String[] spec=args[n].split(":");
     ghidra.program.model.address.Address a=toAddr(spec[1]);
     for(int q=0;q<Integer.parseInt(spec[2]);q++) {
      long v=currentProgram.getMemory().getLong(a.add(q*8));
      w.write("DATA\t"+a.add(q*8)+"\t"+Long.toHexString(v)+"\t"+currentProgram.getSymbolTable().getPrimarySymbol(toAddr(v))+"\n");
     }
     continue;
    }
    if (args[n].startsWith("range:")) {
     String[] range=args[n].split(":");
     FunctionIterator functions=currentProgram.getFunctionManager().getFunctions(toAddr(range[1]),true);
     while(functions.hasNext()) {
      Function f=functions.next();
      if(f.getEntryPoint().compareTo(toAddr(range[2]))>=0) break;
      w.write("FUNCTION\t"+f.getEntryPoint()+"\n");
      DecompileResults result=di.decompileFunction(f,120,monitor);
      if(!result.decompileCompleted()) throw new Exception(result.getErrorMessage());
      w.write("DECOMPILED\n"+result.getDecompiledFunction().getC()+"\n");
     }
     continue;
    }
    if (args[n].startsWith("ref:")) {
     ghidra.program.model.symbol.ReferenceIterator refs=currentProgram.getReferenceManager().getReferencesTo(toAddr(args[n].substring(4)));
     while(refs.hasNext()) {
      ghidra.program.model.symbol.Reference r=refs.next();
      Function f=currentProgram.getFunctionManager().getFunctionContaining(r.getFromAddress());
      w.write("XREF\t"+r.getFromAddress()+"\t"+r.getReferenceType()+"\t"+(f==null?"NONE":f.getEntryPoint())+"\n");
     }
     continue;
    }
    Function f=args[n].startsWith("at:")
      ? currentProgram.getFunctionManager().getFunctionContaining(toAddr(args[n].substring(3)))
      : currentProgram.getFunctionManager().getFunctionAt(toAddr(args[n]));
    if (f==null) throw new Exception("MISSING_FUNCTION " + args[n]);
    w.write("FUNCTION\t" + f.getEntryPoint() + "\n");
    InstructionIterator ii=currentProgram.getListing().getInstructions(f.getBody(),true);
    while(ii.hasNext()) { Instruction i=ii.next(); w.write(i.getAddress()+"\t"+i+"\n"); }
    DecompileResults result=di.decompileFunction(f, 120, monitor);
    if (!result.decompileCompleted()) throw new Exception(result.getErrorMessage());
    w.write("DECOMPILED\n" + result.getDecompiledFunction().getC() + "\n");
   }
   w.write("END\n");
  } finally { di.dispose(); }
 }
}





