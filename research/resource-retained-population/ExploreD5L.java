// SPDX-License-Identifier: GPL-3.0-or-later
// Read-only, explicitly bounded follow-up for D5L owner and copy outcomes.
// Reads existing functions and two specified vtables; writes a fresh local export.
import ghidra.app.script.GhidraScript;
import ghidra.app.decompiler.*;
import ghidra.program.model.listing.*;
import ghidra.program.model.symbol.*;
import java.nio.file.*;
import java.nio.charset.StandardCharsets;
import java.io.BufferedWriter;
import java.util.*;
public class ExploreD5L extends GhidraScript {
    public void run() throws Exception {
        String[] args=getScriptArgs();Set<String> entries=new LinkedHashSet<>();
        DecompInterface d=new DecompInterface();d.openProgram(currentProgram);
        try(BufferedWriter w=Files.newBufferedWriter(Paths.get(args[0]),StandardCharsets.UTF_8,StandardOpenOption.CREATE_NEW)){
            w.write("SHA256\t"+currentProgram.getExecutableSHA256()+"\n");
            for(String table:new String[]{"144b67f48","144b3e0b8"}){
                for(int off=0;off<(table.equals("144b67f48")?0x48:0x90);off+=8){
                    long ptr=currentProgram.getMemory().getLong(toAddr(table).add(off));
                    Function f=currentProgram.getFunctionManager().getFunctionAt(toAddr(ptr));
                    w.write("VTABLE\t"+table+"\t"+Integer.toHexString(off)+"\t"+Long.toHexString(ptr)+"\n");
                    if(f!=null)entries.add(f.getEntryPoint().toString());
                }
            }
            for(int n=1;n<args.length;n++)entries.add(args[n]);
            if(entries.size()>45)throw new Exception("Explicit function bound");
            for(String at:entries){
                Function f=currentProgram.getFunctionManager().getFunctionAt(toAddr(at));
                if(f==null)f=currentProgram.getFunctionManager().getFunctionContaining(toAddr(at));
                if(f==null)throw new Exception("Missing function "+at);
                w.write("FUNCTION\t"+f.getEntryPoint()+"\t"+f.getBody()+"\n");
                InstructionIterator it=currentProgram.getListing().getInstructions(f.getBody(),true);
                int count=0;
                while(it.hasNext()){
                    if(++count>15000)throw new Exception("Instruction bound "+at);
                    Instruction i=it.next();w.write(i.getAddress()+"\t"+i+"\n");
                }
                ReferenceIterator refs=currentProgram.getReferenceManager().getReferencesTo(f.getEntryPoint());
                while(refs.hasNext())w.write("XREF\t"+refs.next()+"\n");
                DecompileResults result=d.decompileFunction(f,60,monitor);
                if(!result.decompileCompleted())throw new Exception("Decompiler "+at);
                w.write("DECOMPILE\n"+result.getDecompiledFunction().getC()+"\nEND_FUNCTION\n");
            }w.write("END\n");
        }finally{d.dispose();}
    }
}
