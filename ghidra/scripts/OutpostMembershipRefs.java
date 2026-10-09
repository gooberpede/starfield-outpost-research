// SPDX-License-Identifier: GPL-3.0-or-later
// Original bounded static reader; -readOnly -noanalysis only. Reads existing
// instructions in a bounded image range; writes one exclusive local TSV. No edits.
import ghidra.app.script.GhidraScript;
import ghidra.program.model.listing.*;
import java.nio.file.*;
import java.nio.charset.StandardCharsets;
import java.io.BufferedWriter;
public class OutpostMembershipRefs extends GhidraScript {
 public void run() throws Exception {
  String[] a=getScriptArgs();
  if(a.length!=1) throw new IllegalArgumentException("fresh output required");
  try(BufferedWriter w=Files.newBufferedWriter(Paths.get(a[0]),StandardCharsets.UTF_8,StandardOpenOption.CREATE_NEW)) {
   w.write("SHA256\t"+currentProgram.getExecutableSHA256()+"\n");
   InstructionIterator it=currentProgram.getListing().getInstructions(toAddr("140001000"),true);
   int count=0;
   while(it.hasNext()&&!monitor.isCancelled()) {
    Instruction x=it.next();if(x.getAddress().getOffset()>=0x143400000L)break;
    String s=x.toString();
    if(!s.matches(".*\\[(?!R[SB]P)[^\\]]*0x298\\].*"))continue;
    Function f=currentProgram.getFunctionManager().getFunctionContaining(x.getAddress());
    w.write(x.getAddress()+"\t"+s+"\t"+(f==null?"NO_FUNCTION":f.getEntryPoint())+"\n");
    if(++count>=1000){w.write("LIMIT_REACHED\n");break;}
   }
   w.write("CANCELLED\t"+monitor.isCancelled()+"\n");
  }
 }
}
