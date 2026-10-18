// SPDX-License-Identifier: GPL-3.0-or-later
// Original static locator. ReadOnly/noanalysis only. Reads existing instructions
// in the supplied positive interval; writes exclusive local TSV. No disassembly,
// state changes, target operations or network. Args: output startVA endVA literal.
import ghidra.app.script.GhidraScript;
import java.nio.file.*;
import java.nio.charset.StandardCharsets;
public class LiteralUses extends GhidraScript {
 public void run() throws Exception {
  var a=getScriptArgs(); if(a.length!=4) throw new IllegalArgumentException("output start end literal");
  var start=toAddr(a[1]); var end=toAddr(a[2]);
  if(end.compareTo(start)<=0) throw new IllegalArgumentException("positive range");
  var it=currentProgram.getListing().getInstructions(start,true);
  try(var out=Files.newBufferedWriter(Paths.get(a[0]),StandardCharsets.UTF_8,StandardOpenOption.CREATE_NEW)) {
   out.write("SHA256\t"+currentProgram.getExecutableSHA256()+"\nBASE\t"+currentProgram.getImageBase()+"\n");
   long examined=0,selected=0;
   while(it.hasNext()&&!monitor.isCancelled()) {
    var x=it.next(); if(x.getAddress().compareTo(end)>=0) break; examined++;
    if(!x.toString().contains(a[3])) continue;
    var fn=currentProgram.getFunctionManager().getFunctionContaining(x.getAddress());
    out.write("MATCH\t"+x.getAddress()+"\t"+(fn==null?"NO_FUNCTION":fn.getEntryPoint())+"\t"+x+"\n"); selected++;
   }
   out.write("END\texamined="+examined+"\tselected="+selected+"\tcancelled="+monitor.isCancelled()+"\n");
  }
 }
}
