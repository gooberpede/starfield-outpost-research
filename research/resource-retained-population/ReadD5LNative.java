// SPDX-License-Identifier: GPL-3.0-or-later
// Adapted from project-owned ReadD5JBytes; read-only existing analysis export.
// Writes one exclusive local file. No analysis, symbols, types or comments change.
import ghidra.app.script.GhidraScript;
import ghidra.app.decompiler.*;
import ghidra.program.model.listing.*;
import ghidra.program.model.symbol.*;
import java.nio.file.*;
import java.nio.charset.StandardCharsets;
import java.io.BufferedWriter;
public class ReadD5LNative extends GhidraScript {
    public void run() throws Exception {
        DecompInterface d = new DecompInterface();d.openProgram(currentProgram);
        try (BufferedWriter w = Files.newBufferedWriter(Paths.get(getScriptArgs()[0]), StandardCharsets.UTF_8, StandardOpenOption.CREATE_NEW)) {
            w.write("SHA256\t"+currentProgram.getExecutableSHA256()+"\nBASE\t"+currentProgram.getImageBase()+"\n");
            for(String at:new String[]{"14079a330","14079b520","14079c470","140982d90","1409832e0","140985900","140985c50","14079d660","14079d910","14079ddf0"}){
                Function f=currentProgram.getFunctionManager().getFunctionAt(toAddr(at));
                if(f==null)throw new Exception("Missing existing function "+at);
                w.write("FUNCTION\t"+at+"\t"+f.getBody()+"\n");
                InstructionIterator it=currentProgram.getListing().getInstructions(f.getBody(),true);
                while(it.hasNext()){Instruction i=it.next();w.write(i.getAddress()+"\t"+i+"\n");}
                ReferenceIterator refs=currentProgram.getReferenceManager().getReferencesTo(f.getEntryPoint());
                while(refs.hasNext())w.write("XREF\t"+refs.next()+"\n");
                DecompileResults r=d.decompileFunction(f,60,monitor);
                if(!r.decompileCompleted())throw new Exception("Decompiler failed: "+at);
                w.write("DECOMPILE\n"+r.getDecompiledFunction().getC()+"\nEND_FUNCTION\n");
            }
            w.write("END\n");
        }finally{d.dispose();}
    }
}
