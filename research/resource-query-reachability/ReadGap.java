// SPDX-License-Identifier: GPL-3.0-or-later
// Decode a bounded byte window without adding instructions to the database.
// Reads currentProgram bytes via PseudoDisassembler; CREATE_NEW output only.
import ghidra.app.script.GhidraScript;
import ghidra.app.util.PseudoDisassembler;
import ghidra.app.util.PseudoInstruction;
import java.nio.file.*;
import java.nio.charset.StandardCharsets;
import java.io.*;
public class ReadGap extends GhidraScript {
 public void run() throws Exception {
  String[] args=getScriptArgs();
  PseudoDisassembler d=new PseudoDisassembler(currentProgram);
  try(BufferedWriter w=Files.newBufferedWriter(Paths.get(args[0]),StandardCharsets.UTF_8,StandardOpenOption.CREATE_NEW)) {
   w.write("SHA256\t"+currentProgram.getExecutableSHA256()+"\n");
   for(int n=1;n<args.length;n++) {
    String[] parts=args[n].split(":");
    ghidra.program.model.address.Address at=toAddr(parts[0]),end=toAddr(parts[1]);
    while(at.compareTo(end)<0) {
     PseudoInstruction i=d.disassemble(at);
     if(i==null)throw new Exception("Cannot decode "+at);
     w.write(at+"\t"+i+"\n");at=at.add(i.getLength());
    }
    if(!at.equals(end))throw new Exception("Non-boundary end");
   }
   w.write("END\n");
  }
 }
}
