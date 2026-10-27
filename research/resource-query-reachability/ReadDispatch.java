// SPDX-License-Identifier: GPL-3.0-or-later
// Read-only bounded D5H dispatch export. Adapted from owned ReadSpecialist.java.
// Requires an existing program, -readOnly -noanalysis and fresh local output.
// Reads seven named modifier vtables and their +0x18 bodies; no project edits.
import ghidra.app.script.GhidraScript;
import ghidra.app.decompiler.*;
import ghidra.program.model.listing.*;
import ghidra.program.model.symbol.*;
import java.nio.file.*;
import java.nio.charset.StandardCharsets;
import java.io.*;
import java.util.*;
public class ReadDispatch extends GhidraScript {
 public void run() throws Exception {
  String[] args=getScriptArgs();
  Set<String> names=new HashSet<>(Arrays.asList("RerangeHeightModifier", "HeightAdjustmentModifier",
    "AlignmentModifier", "ContinentalModifier", "OceanBiomeModifier", "OverlayHeightModifier", "UpdateHeightModifier"));
  TreeSet<Long> targets=new TreeSet<>();
  DecompInterface di=new DecompInterface(); di.openProgram(currentProgram);
  try(BufferedWriter w=Files.newBufferedWriter(Paths.get(args[0]), StandardCharsets.UTF_8, StandardOpenOption.CREATE_NEW)) {
   w.write("SHA256\t"+currentProgram.getExecutableSHA256()+"\nBASE\t"+currentProgram.getImageBase()+"\n");
   SymbolIterator si=currentProgram.getSymbolTable().getAllSymbols(true);
   Set<String> found=new HashSet<>();
   while(si.hasNext()) {
    Symbol s=si.next();
    for(String name:names) if(s.getName(true).equals("BGSTerrainBlock::"+name+"::vftable")) {
     long va=currentProgram.getMemory().getLong(s.getAddress().add(0x18));
     w.write("DISPATCH\t"+s.getName(true)+"\t"+s.getAddress()+"\t18\t"+Long.toHexString(va)+"\n");
     targets.add(va); found.add(name);
    }
   }
   if(!found.equals(names)) throw new Exception("Incomplete concrete modifier census: "+found);
   for(int i=1;i<args.length;i++) targets.add(Long.parseUnsignedLong(args[i],16));
   w.flush();
   for(long va:targets) {
    Function f=currentProgram.getFunctionManager().getFunctionAt(toAddr(va));
    if(f==null) throw new Exception("Missing function "+Long.toHexString(va));
    w.write("FUNCTION\t"+f.getEntryPoint()+"\n");
    InstructionIterator ii=currentProgram.getListing().getInstructions(f.getBody(),true);
    while(ii.hasNext()){Instruction i=ii.next();w.write(i.getAddress()+"\t"+i+"\n");}
    DecompileResults dr=di.decompileFunction(f,120,monitor);
    if(!dr.decompileCompleted())throw new Exception(dr.getErrorMessage());
    w.write("DECOMPILED\n"+dr.getDecompiledFunction().getC()+"\n"); w.flush();
   }
   w.write("END\n");
  } finally {di.dispose();}
 }
}
