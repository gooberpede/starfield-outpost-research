// SPDX-License-Identifier: GPL-3.0-or-later
// Original read-only exporter. No analysis, symbol, type or comment changes.
// Reads currentProgram functions, writes CREATE_NEW local TSV only.
import ghidra.app.script.GhidraScript;
import ghidra.app.decompiler.*;
import ghidra.program.model.listing.*;
import java.nio.file.*;
import java.nio.charset.StandardCharsets;
import java.io.*;
public class ReadWorkshop extends GhidraScript {
 public void run() throws Exception {
  String[] args = getScriptArgs();
  DecompInterface di = new DecompInterface();
  di.openProgram(currentProgram);
  try (BufferedWriter w = Files.newBufferedWriter(Paths.get(args[0]),
       StandardCharsets.UTF_8, StandardOpenOption.CREATE_NEW)) {
   w.write("SHA256\t" + currentProgram.getExecutableSHA256() + "\nBASE\t" + currentProgram.getImageBase() + "\n");
   for (int n=1; n<args.length; n++) {
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
