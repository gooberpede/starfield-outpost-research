// SPDX-License-Identifier: GPL-3.0-or-later
// Original read-only existing-instruction census; literal offsets are leads only.
import ghidra.app.script.GhidraScript;
import ghidra.program.model.listing.*;
import java.nio.file.*;
import java.nio.charset.StandardCharsets;
import java.io.BufferedWriter;
public class ResourceCellFields extends GhidraScript {
 public void run() throws Exception {
  String[] args=getScriptArgs(); long count=0;
  try(BufferedWriter out=Files.newBufferedWriter(Paths.get(args[0]),StandardCharsets.UTF_8,StandardOpenOption.CREATE_NEW)) {
   out.write("SHA256\t"+currentProgram.getExecutableSHA256()+"\nBASE\t"+currentProgram.getImageBase()+"\n");
   InstructionIterator it=currentProgram.getListing().getInstructions(toAddr("140760000"),true);
   while(it.hasNext()&&!monitor.isCancelled()) {
    Instruction x=it.next(); if(x.getAddress().compareTo(toAddr("1407d0000"))>=0)break; count++;
    String s=x.toString(); if(!(s.contains(" + 0x308]")||s.contains(" + 0x310]")||s.contains(" + 0x130]")))continue;
    if(s.contains("[RSP ")||s.contains("[RBP "))continue;
    Function f=currentProgram.getFunctionManager().getFunctionContaining(x.getAddress());
    out.write(x.getAddress()+"\t"+(f==null?"NO_FUNCTION":f.getEntryPoint())+"\t"+s+"\n");
   }
   out.write("END\texamined="+count+"\tcancelled="+monitor.isCancelled()+"\n");
  }
 }
}
