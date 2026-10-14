// SPDX-License-Identifier: GPL-3.0-or-later
// Original read-only bounded existing-instruction selector; textual offsets are leads only.
import ghidra.app.script.GhidraScript;
import ghidra.program.model.listing.*;
import java.nio.file.*;
import java.nio.charset.StandardCharsets;
import java.io.BufferedWriter;
public class ResourceFields extends GhidraScript {
 public void run() throws Exception {
  String[] args=getScriptArgs(); long count=0;
  try(BufferedWriter out=Files.newBufferedWriter(Paths.get(args[0]),StandardCharsets.UTF_8,StandardOpenOption.CREATE_NEW)) {
   out.write("SHA256\t"+currentProgram.getExecutableSHA256()+"\nBASE\t"+currentProgram.getImageBase()+"\n");
   InstructionIterator it=currentProgram.getListing().getInstructions(toAddr("1421a0000"),true);
   while(it.hasNext()&&!monitor.isCancelled()) {
    Instruction x=it.next(); if(x.getAddress().compareTo(toAddr("142200000"))>=0)break; count++;
    String s=x.toString(); if(!(s.contains(" + 0x520]")||s.contains(" + 0x538]")||s.contains(" + 0x550]")||s.contains(" + 0x528]")||s.contains(" + 0x540]")||s.contains(" + 0x558]")))continue;
    Function f=currentProgram.getFunctionManager().getFunctionContaining(x.getAddress());
    out.write(x.getAddress()+"\t"+(f==null?"NO_FUNCTION":f.getEntryPoint())+"\t"+s+"\n");
   }
   out.write("END\texamined="+count+"\tcancelled="+monitor.isCancelled()+"\n");
  }
 }
}
