// Original finite read-only C2 transit call-site inventory. Existing instructions
// only, no disassembly/analysis/mutations. Reads one bounded VA interval <=1MiB;
// writes new ignored UTF8 text and reports coverage/cancellation. No invocation.
import ghidra.app.script.GhidraScript;
import ghidra.program.model.listing.*;
import ghidra.program.model.address.Address;
import java.nio.file.*;
import java.nio.charset.StandardCharsets;
import java.io.BufferedWriter;
import java.util.ArrayDeque;
public class TransitCalls extends GhidraScript {
 public void run() throws Exception {
  String[] a=getScriptArgs();
  try(BufferedWriter o=Files.newBufferedWriter(Paths.get(a[0]),StandardCharsets.UTF_8,StandardOpenOption.CREATE_NEW)) {
   o.write("PROGRAM\t"+currentProgram.getName()+"\nSHA256\t"+currentProgram.getExecutableSHA256()+"\nBASE\t"+currentProgram.getImageBase()+"\n");
   for(int q=1;q<a.length;q++) {
    boolean slot720=a[q].equals("slot720"); boolean allLoad=a[q].equals("floatloads")||slot720; boolean allFloat=a[q].equals("floatcalls")||allLoad;
    String[] b=allFloat ? new String[]{"calls",currentProgram.getMinAddress().toString(),currentProgram.getMaxAddress().toString()} : a[q].split(":"); if(b.length!=3||!b[0].equals("calls"))throw new IllegalArgumentException("calls:low:high");
    Address lo=toAddr(b[1]),hi=toAddr(b[2]);if(hi.compareTo(lo)<=0||(!allFloat && hi.subtract(lo)>0x100000))throw new IllegalArgumentException("positive range <=1MiB");
    InstructionIterator it=currentProgram.getListing().getInstructions(lo,true);ArrayDeque<Instruction> prev=new ArrayDeque<>();long count=0,selected=0;
    while(it.hasNext()&&!monitor.isCancelled()) {
     Instruction x=it.next();if(x.getAddress().compareTo(hi)>=0)break;count++;
     String s=x.toString();
     if(((s.startsWith("CALL ") || s.startsWith("JMP ")) && s.contains(slot720 ? " + 0x720]" : " + 0x18]")) || (allLoad && s.startsWith("MOV ") && s.contains("qword ptr [") && s.endsWith(slot720 ? " + 0x720]" : " + 0x18]"))) {
      boolean useful=!allFloat||slot720;
      for(Instruction p:prev)if(p.toString().contains("XMM1")||p.toString().contains(" + 0x240]"))useful=true;
      if(allLoad && !useful){Instruction n=currentProgram.getListing().getInstructionAfter(x.getAddress());for(int z=0;z<16 && n!=null;z++){if(n.toString().contains("XMM1"))useful=true;n=currentProgram.getListing().getInstructionAfter(n.getAddress());}}
      if(!useful){prev.addLast(x);if(prev.size()>16)prev.removeFirst();continue;}
      selected++;Function f=currentProgram.getFunctionManager().getFunctionContaining(x.getAddress());
      o.write("CANDIDATE\t"+x.getAddress()+"\t"+(f==null?"NO_FUNCTION":f.getEntryPoint())+"\n");
      for(Instruction p:prev)o.write(p.getAddress()+"\t"+p+"\n");o.write(x.getAddress()+"\t"+s+"\n");
      if(allLoad){Instruction n=currentProgram.getListing().getInstructionAfter(x.getAddress());for(int z=0;z<16 && n!=null;z++){o.write("AFTER\t"+n.getAddress()+"\t"+n+"\n");n=currentProgram.getListing().getInstructionAfter(n.getAddress());}}
     }
     prev.addLast(x);if(prev.size()>16)prev.removeFirst();
    }
    o.write("END\t"+lo+"\t"+hi+"\texamined="+count+"\tselected="+selected+"\tcancelled="+monitor.isCancelled()+"\n");o.flush();
   }
  }
 }
}
