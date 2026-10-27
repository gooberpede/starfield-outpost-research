// SPDX-License-Identifier: GPL-3.0-or-later
// Read existing instruction lengths/flow/bytes and erase body. No analysis edits.
import ghidra.app.script.GhidraScript;
import ghidra.app.decompiler.*;
import ghidra.program.model.listing.*;
import ghidra.program.model.symbol.*;
import ghidra.program.model.address.*;
import java.nio.file.*;
import java.nio.charset.StandardCharsets;
import java.io.BufferedWriter;
import java.util.HexFormat;
import java.util.LinkedHashSet;
public class ExportD5LSites extends GhidraScript {
    public void run() throws Exception {
        try(BufferedWriter w=Files.newBufferedWriter(Paths.get(getScriptArgs()[0]),StandardCharsets.UTF_8,StandardOpenOption.CREATE_NEW)){
            w.write("SHA256\t"+currentProgram.getExecutableSHA256()+"\n");
            LinkedHashSet<Function> bodies=new LinkedHashSet<>();
            for(String at:new String[]{"14079fca3","14079fcd0","14079feaf","14079b8ed","14079acf2","14079ff1d","14079d8b2","14079de92","14079d910","140975030","1409829b0","140983140","1409828d5","140982b70"}){
                Instruction i=currentProgram.getListing().getInstructionAt(toAddr(at));
                if(i==null)throw new Exception("No existing instruction "+at);
                bodies.add(currentProgram.getFunctionManager().getFunctionContaining(i.getAddress()));
                byte[] b=new byte[16];currentProgram.getMemory().getBytes(i.getAddress(),b);
                w.write("SITE\t"+at+"\t"+i.getLength()+"\t"+i.getFallThrough()+"\t"+java.util.Arrays.toString(i.getFlows())+"\t"+i+"\t"+HexFormat.of().formatHex(b)+"\n");
            }
            for(String at:new String[]{"1407ac2f0","1407ac0d0"})bodies.add(currentProgram.getFunctionManager().getFunctionAt(toAddr(at)));
            for(Function body:bodies){
                if(body==null)throw new Exception("Missing support body");
                AddressRangeIterator ranges=body.getBody().getAddressRanges(true);
                while(ranges.hasNext()){
                    AddressRange range=ranges.next();long n=range.getLength();if(n>131072)throw new Exception("Body range bound");
                    byte[] bytes=new byte[(int)n];currentProgram.getMemory().getBytes(range.getMinAddress(),bytes);
                    w.write("BODY_BYTES\t"+body.getEntryPoint()+"\t"+range.getMinAddress()+"\t"+HexFormat.of().formatHex(bytes)+"\n");
                }
            }
            Function f=currentProgram.getFunctionManager().getFunctionAt(toAddr("140975030"));
            w.write("FUNCTION\t"+f.getEntryPoint()+"\t"+f.getBody()+"\n");
            InstructionIterator it=currentProgram.getListing().getInstructions(f.getBody(),true);
            while(it.hasNext()){Instruction i=it.next();w.write(i.getAddress()+"\t"+i+"\n");}
            ReferenceIterator refs=currentProgram.getReferenceManager().getReferencesTo(f.getEntryPoint());
            while(refs.hasNext())w.write("XREF\t"+refs.next()+"\n");
            DecompInterface d=new DecompInterface();d.openProgram(currentProgram);
            try{DecompileResults result=d.decompileFunction(f,60,monitor);if(!result.decompileCompleted())throw new Exception("Decompile");w.write("DECOMPILE\n"+result.getDecompiledFunction().getC()+"\n");}finally{d.dispose();}
            w.write("END\n");
        }
    }
}
