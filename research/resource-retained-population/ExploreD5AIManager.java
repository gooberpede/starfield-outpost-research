// SPDX-License-Identifier: GPL-3.0-or-later
// Read-only owner-continuity census. Reads existing listing/functions/references;
// writes a fresh ignored export. No analysis or symbols/types/comments change.
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.*;
import ghidra.program.model.listing.*;
import ghidra.program.model.symbol.*;
import java.nio.file.*;
import java.nio.charset.StandardCharsets;
import java.io.BufferedWriter;
import java.util.*;

public class ExploreD5AIManager extends GhidraScript {
    public void run() throws Exception {
        String[] args=getScriptArgs();
        TreeMap<Long,Function> functions=new TreeMap<>();
        FunctionIterator fit=currentProgram.getFunctionManager().getFunctions(toAddr("140787000"),true);
        while(fit.hasNext()) {
            Function f=fit.next();long entry=f.getEntryPoint().getOffset();
            if(entry>=0x140790000L)break;
            functions.put(entry,f);
        }
        ArrayList<String> roots=new ArrayList<>();
        ReferenceIterator refs=currentProgram.getReferenceManager().getReferencesTo(toAddr("145fd9c30"));
        while(refs.hasNext()) {
            Reference r=refs.next();roots.add(r.toString());
            Function f=currentProgram.getFunctionManager().getFunctionContaining(r.getFromAddress());
            if(f!=null)functions.put(f.getEntryPoint().getOffset(),f);
        }
        try(BufferedWriter w=Files.newBufferedWriter(Paths.get(args[0]),StandardCharsets.UTF_8,StandardOpenOption.CREATE_NEW)) {
            w.write("SHA256\t"+currentProgram.getExecutableSHA256()+"\n");
            w.write("SCOPE\tManager method interval 0x140787000..0x140790000 plus every existing direct singleton reference receiver\n");
            for(String root:roots)w.write("ROOT\t"+root+"\n");
            for(Function f:functions.values()) {
                w.write("FUNCTION\t"+f.getEntryPoint()+"\t"+f.getBody()+"\n");
                ReferenceIterator callers=currentProgram.getReferenceManager().getReferencesTo(f.getEntryPoint());
                while(callers.hasNext())w.write("XREF\t"+callers.next()+"\n");
                InstructionIterator it=currentProgram.getListing().getInstructions(f.getBody(),true);
                while(it.hasNext()) {
                    Instruction instruction=it.next();
                    w.write(instruction.getAddress()+"\t"+instruction+"\n");
                }
                w.write("END_FUNCTION\n");
            }
            w.write("COUNT\t"+functions.size()+"\nEND\n");
        }
    }
}
