// SPDX-License-Identifier: GPL-3.0-or-later
// Original read-only instruction inventory, not a semantic/type classifier.
// Requires -readOnly -noanalysis. Reads existing disassembly only; writes one
// exclusive local UTF-8 TSV. No bytes/symbol/type/comment/database mutation.
// Args: output, start static address, exclusive end static address.
import ghidra.app.script.GhidraScript;
import ghidra.program.model.listing.*;
import ghidra.program.model.address.Address;
import java.nio.file.*;
import java.nio.charset.StandardCharsets;
import java.io.BufferedWriter;

public class WorkshopOriginRefs extends GhidraScript {
    public void run() throws Exception {
        String[] args = getScriptArgs();
        if (args.length != 3) throw new IllegalArgumentException("output/start/end");
        Address start=toAddr(args[1]), end=toAddr(args[2]);
        try (BufferedWriter out=Files.newBufferedWriter(Paths.get(args[0]), StandardCharsets.UTF_8, StandardOpenOption.CREATE_NEW)) {
            out.write("PROGRAM\t"+currentProgram.getName()+"\nSHA256\t"+currentProgram.getExecutableSHA256()+"\nBASE\t"+currentProgram.getImageBase()+"\n");
            InstructionIterator it=currentProgram.getListing().getInstructions(start,true);
            long examined=0, selected=0;
            while(it.hasNext() && !monitor.isCancelled()) {
                Instruction x=it.next();
                if(x.getAddress().compareTo(end)>=0) break;
                examined++;
                String s=x.toString();
                if(!(s.contains(" + 0x60]") || s.contains(" + 0x68]"))) continue;
                if(s.contains("[RSP ") || s.contains("[RBP ")) continue;
                Function f=currentProgram.getFunctionManager().getFunctionContaining(x.getAddress());
                out.write(x.getAddress()+"\t"+(f==null?"NO_FUNCTION":f.getEntryPoint())+"\t"+s+"\n");
                selected++;
            }
            out.write("END\texamined="+examined+"\tselected="+selected+"\tcancelled="+monitor.isCancelled()+"\n");
        }
    }
}
