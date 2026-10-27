// SPDX-License-Identifier: GPL-3.0-or-later
// Read existing instructions only; no analysis or project mutation. Fixed bounded
// Terrain subsystem scan for direct focus/frame field writes, not type inference.
// Adapted exporter interfaces from owned ReadSpecialist.java (SOR-P-0002).
import ghidra.app.script.GhidraScript;
import ghidra.program.model.listing.*;
import java.nio.file.*;
import java.nio.charset.StandardCharsets;
import java.io.*;
public class ReadField extends GhidraScript {
 public void run() throws Exception {
  String[] args=getScriptArgs();
  if(args.length!=1) throw new Exception("One fresh output path required");
  try(BufferedWriter w=Files.newBufferedWriter(Paths.get(args[0]),StandardCharsets.UTF_8,StandardOpenOption.CREATE_NEW)) {
   w.write("SHA256\t"+currentProgram.getExecutableSHA256()+"\nBASE\t"+currentProgram.getImageBase()+"\n");
   w.write("SCOPE\t140990000\t1409b0000\tFirst operand memory writes mentioning +0xd8,+0xdc,+0xe0,+0xe8; wider stores/other subsystem writers not excluded\n");
   InstructionIterator it=currentProgram.getListing().getInstructions(toAddr("140990000"),true);
   long count=0,hits=0;
   while(it.hasNext()) {
    monitor.checkCancelled(); Instruction i=it.next();
    if(i.getAddress().compareTo(toAddr("1409b0000"))>=0) break;
    count++; String op=i.getNumOperands()>0?i.getDefaultOperandRepresentation(0).toLowerCase():"";
    String mnemonic=i.getMnemonicString().toUpperCase();
    if(!op.contains("[")||!(mnemonic.startsWith("MOV")||mnemonic.startsWith("VMOV"))) continue;
    if(!(op.contains("+ 0xd8]")||op.contains("+ 0xdc]")||op.contains("+ 0xe0]")||op.contains("+ 0xe8]"))) continue;
    Function f=currentProgram.getFunctionManager().getFunctionContaining(i.getAddress());
    w.write("WRITE\t"+i.getAddress()+"\t"+(f==null?"NONE":f.getEntryPoint())+"\t"+i+"\n"); hits++;
   }
   w.write("COUNTS\t"+count+"\t"+hits+"\nEND\n");
  }
 }
}
