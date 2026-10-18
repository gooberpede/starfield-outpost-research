// SPDX-License-Identifier: GPL-3.0-or-later
// R1 bounded lead selector, adapted owned Cr1Recon.java field method.
// Existing instructions only; -readOnly -noanalysis required. Writes one new
// local TSV, no native invocation or database mutation. Literals are leads.
import ghidra.app.script.GhidraScript;
import ghidra.program.model.listing.*;
import java.nio.file.*;
import java.io.*;
import java.nio.charset.StandardCharsets;
public class RobotFields extends GhidraScript {
 public void run() throws Exception {
  try(BufferedWriter out=Files.newBufferedWriter(Paths.get(getScriptArgs()[0]),StandardCharsets.UTF_8,StandardOpenOption.CREATE_NEW)) {
   out.write("SHA256\t"+currentProgram.getExecutableSHA256()+"\nBASE\t"+currentProgram.getImageBase()+"\n");
   boolean scripts=getScriptArgs().length>2&&getScriptArgs()[2].startsWith("scripts");
   boolean binding=scripts&&getScriptArgs()[2].equals("scripts-binding");
   String[][] ranges=scripts?(binding?new String[][]{{"1405d0000","1405e0000"},{"140cd0000","140ce3000"},{"141f40000","141fa0000"}}:new String[][]{{"1405d0000","1405e0000"},{"140cd0000","140ce3000"}}):new String[][]{{"140f20000","140fa0000"},{"141710000","141730000"},{"142190000","142200000"}};
   for(String[] range:ranges) {
    InstructionIterator ii=currentProgram.getListing().getInstructions(toAddr(range[0]),true);long count=0,selected=0;
    while(ii.hasNext() && !monitor.isCancelled()) {
     Instruction x=ii.next();if(x.getAddress().compareTo(toAddr(range[1]))>=0) break;count++;
     String s=x.toString();if(s.contains("[RSP ")||s.contains("[RBP "))continue;
     String[] fields=getScriptArgs().length>2&&!scripts?getScriptArgs()[2].split(","):new String[]{"170","150","178"};boolean match=scripts&&(s.contains("0x200")||s.equals("MOV EDX,0x9")||(binding&&(s.contains(" + 0xff]")||s.contains(" + 0xfe]")||s.equals("SHR EAX,0x9"))));
     if(!scripts)for(String field:fields){if(!field.matches("[a-f0-9]{1,4}"))throw new IllegalArgumentException("hex field required");if(s.contains(" + 0x"+field+"]"))match=true;}
     if(!match)continue;
     Function f=currentProgram.getFunctionManager().getFunctionContaining(x.getAddress());
     out.write("FIELD_LEAD\t"+x.getAddress()+"\t"+(f==null?"UNKNOWN":f.getEntryPoint())+"\t"+s+"\n");selected++;
    }
    out.write("RANGE_END\t"+range[0]+"\t"+range[1]+"\texamined="+count+"\tselected="+selected+"\tcancelled="+monitor.isCancelled()+"\n");
   }
  }
 }
}
