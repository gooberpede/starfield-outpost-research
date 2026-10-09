// SPDX-License-Identifier: GPL-3.0-or-later
// Original read-only instruction search. Use -readOnly -noanalysis.
// Reads existing instructions only; writes a fresh local TSV; no target effects.
import ghidra.app.script.GhidraScript;
import ghidra.program.model.listing.*;
import java.nio.file.*;
import java.nio.charset.StandardCharsets;
import java.io.BufferedWriter;
public class OutpostSaveConstants extends GhidraScript {
    public void run() throws Exception {
        String[] args=getScriptArgs();
        if(args.length!=1) throw new IllegalArgumentException("fresh output path required");
        try(BufferedWriter out=Files.newBufferedWriter(Paths.get(args[0]),StandardCharsets.UTF_8,StandardOpenOption.CREATE_NEW)) {
            out.write("SHA256\t"+currentProgram.getExecutableSHA256()+"\n");
            InstructionIterator it=currentProgram.getListing().getInstructions(toAddr("140430000"),true);
            int n=0;
            while(it.hasNext()&&!monitor.isCancelled()) {
                Instruction x=it.next();long va=x.getAddress().getOffset();
                if(va>=0x141900000L)break;
                if(!((va<0x140600000L)||(va>=0x140f00000L&&va<0x140fc0000L)||(va>=0x141340000L&&va<0x141390000L)||(va>=0x141800000L)))continue;
                String s=x.toString();
                if(!s.matches(".*0x2000000(0)?([^0-9a-f].*|$)") &&
                   !(va>=0x141340000L&&va<0x141390000L&&s.matches(".*0x(a[89abcdef][0-9a-f]|b[012][0-9a-f])([^0-9a-f].*|$)")))continue;
                Function f=currentProgram.getFunctionManager().getFunctionContaining(x.getAddress());
                out.write(x.getAddress()+"\t"+s+"\t"+(f==null?"NO_FUNCTION":f.getEntryPoint())+"\n");
                if(++n>=3000){out.write("LIMIT_REACHED\n");break;}
            }
            out.write("CANCELLED\t"+monitor.isCancelled()+"\n");
        }
    }
}
