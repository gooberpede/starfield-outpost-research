// SPDX-License-Identifier: GPL-3.0-or-later
// Original read-only reader. No analysis or database edits.
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Function;
import ghidra.program.model.symbol.Reference;
import ghidra.program.model.symbol.ReferenceIterator;
import java.nio.file.*;
import java.nio.charset.StandardCharsets;
import java.io.BufferedWriter;
public class ResourceGlobalRefs extends GhidraScript {
 public void run() throws Exception {
  String[] args=getScriptArgs();
  try(BufferedWriter out=Files.newBufferedWriter(Paths.get(args[0]),StandardCharsets.UTF_8,StandardOpenOption.CREATE_NEW)) {
   out.write("SHA256\t"+currentProgram.getExecutableSHA256()+"\nBASE\t"+currentProgram.getImageBase()+"\n");
   Address start=toAddr(args[1]); Address end=toAddr(args[2]);
   for(Address a=start;a.compareTo(end)<0&&!monitor.isCancelled();a=a.add(1)) {
    ReferenceIterator refs=currentProgram.getReferenceManager().getReferencesTo(a);
    while(refs.hasNext()) {
     Reference r=refs.next(); Function f=currentProgram.getFunctionManager().getFunctionContaining(r.getFromAddress());
     out.write(a+"\t"+r.getFromAddress()+"\t"+(f==null?"NO_FUNCTION":f.getEntryPoint())+"\t"+r.getReferenceType()+"\n");
    }
   }
   out.write("END\tcancelled="+monitor.isCancelled()+"\n");
  }
 }
}
