// SPDX-License-Identifier: GPL-3.0-or-later
// Original readOnly/noanalysis existing-instruction reader. Arguments: exclusive
// ignored output, exact callee VA. No disassembly, program/target changes or network.
// Exports at most 1024 existing call xrefs and 20 preceding instructions per xref.
// Context is a locator, not proof of register dataflow across control-flow joins.
import ghidra.app.script.GhidraScript;
import ghidra.program.model.symbol.*;
import ghidra.program.model.listing.*;
import java.nio.file.*;
import java.nio.charset.StandardCharsets;
import java.util.*;
public class XrefContext extends GhidraScript {
 public void run() throws Exception {
  String[] a=getScriptArgs();
  if(a.length!=2) throw new IllegalArgumentException("output calleeVA");
  var refs=currentProgram.getReferenceManager().getReferencesTo(toAddr(a[1]));
  try(var out=Files.newBufferedWriter(Paths.get(a[0]),StandardCharsets.UTF_8,StandardOpenOption.CREATE_NEW)) {
   out.write("SHA256\t"+currentProgram.getExecutableSHA256()+"\nBASE\t"+currentProgram.getImageBase()+"\n");
   int count=0;
   while(refs.hasNext() && !monitor.isCancelled() && count<1024) {
    var ref=refs.next(); var x=currentProgram.getListing().getInstructionAt(ref.getFromAddress());
    if(x==null || !x.getFlowType().isCall()) continue;
    count++; var fn=currentProgram.getFunctionManager().getFunctionContaining(x.getAddress());
    out.write("CALL\t"+x.getAddress()+"\t"+(fn==null?"NO_FUNCTION":fn.getEntryPoint())+"\n");
    var lines=new ArrayList<String>(); lines.add(x.getAddress()+"\t"+x+"\n");
    for(int n=0;n<20;n++) { x=currentProgram.getListing().getInstructionBefore(x.getAddress());
     if(x==null || (fn!=null && !fn.getBody().contains(x.getAddress()))) break;
     lines.add(x.getAddress()+"\t"+x+"\n"); }
    Collections.reverse(lines); for(var line:lines) out.write(line);
   }
   out.write("END\tcount="+count+"\tremaining="+refs.hasNext()+"\tcancelled="+monitor.isCancelled()+"\n");
  }
 }
}
