// SPDX-License-Identifier: GPL-3.0-or-later
// Original read-only exact-short-name symbol query. No DB effects.
import ghidra.app.script.GhidraScript;
import ghidra.program.model.symbol.*;
import java.nio.file.*;
import java.nio.charset.StandardCharsets;
import java.io.*;
public class ReadNamed extends GhidraScript {
 public void run() throws Exception {
  String[] a=getScriptArgs();
  try(BufferedWriter w=Files.newBufferedWriter(Paths.get(a[0]),StandardCharsets.UTF_8,StandardOpenOption.CREATE_NEW)){
   w.write("SHA256\t"+currentProgram.getExecutableSHA256()+"\nBASE\t"+currentProgram.getImageBase()+"\n");
   for(int n=1;n<a.length;n++){
    String[] q=a[n].split(":",2);
    SymbolIterator it=currentProgram.getSymbolTable().getSymbols(q[0]);
    while(it.hasNext()){
     Symbol s=it.next();String name=s.getName(true);
     if(name.contains(q[1]))w.write("SYMBOL\t"+s.getAddress()+"\t"+name+"\n");
    }
   }
   w.write("END\n");
  }
 }
}
