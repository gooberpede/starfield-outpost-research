// SPDX-License-Identifier: GPL-3.0-or-later
// Owned D5AM derivative of retained ExploreD5S.java under SOR-P-0002.
// Reads explicit existing functions, bytes and references from a verified copy;
// writes only a fresh local export. No analysis or symbol/type/comment writes.
import ghidra.app.script.GhidraScript;
import ghidra.app.decompiler.*;
import ghidra.program.model.listing.*;
import ghidra.program.model.symbol.*;
import java.nio.file.*;
import java.nio.charset.StandardCharsets;
import java.io.BufferedWriter;
import java.util.*;
public class D5AMOwnerCensus extends GhidraScript {
    public void run() throws Exception {
        String[] args=getScriptArgs();Set<String> entries=new LinkedHashSet<>();
        boolean rootsMode=args.length==2&&args[1].equals("145fd9c30");
        ArrayList<String> roots=new ArrayList<>();
        DecompInterface d=new DecompInterface();d.openProgram(currentProgram);
        try(BufferedWriter w=Files.newBufferedWriter(Paths.get(args[0]),StandardCharsets.UTF_8,StandardOpenOption.CREATE_NEW)){
            w.write("SHA256\t"+currentProgram.getExecutableSHA256()+"\n");
            if(rootsMode){
                w.write("SCOPE\tManager method interval140787000..140790000 plus every existing direct manager singleton reference receiver\n");
                FunctionIterator fit=currentProgram.getFunctionManager().getFunctions(toAddr("140787000"),true);
                while(fit.hasNext()){Function f=fit.next();if(f.getEntryPoint().getOffset()>=0x140790000L)break;entries.add(f.getEntryPoint().toString());}
                ReferenceIterator rr=currentProgram.getReferenceManager().getReferencesTo(toAddr("145fd9c30"));
                while(rr.hasNext()){Reference r=rr.next();roots.add(r.toString());Function f=currentProgram.getFunctionManager().getFunctionContaining(r.getFromAddress());if(f!=null)entries.add(f.getEntryPoint().toString());}
                for(String r:roots)w.write("ROOT\t"+r+"\n");
            }else for(int n=1;n<args.length;n++)entries.add(args[n]);
            if(entries.size()>(rootsMode?500:45))throw new Exception("Explicit function bound");
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
                    byte[] raw=i.getBytes();StringBuilder hex=new StringBuilder();
                    for(byte b:raw)hex.append(String.format("%02x",b&255));
                    w.write("BYTES\t"+i.getAddress()+"\t"+hex+"\n");
                }
                ReferenceIterator refs=currentProgram.getReferenceManager().getReferencesTo(f.getEntryPoint());
                while(refs.hasNext()){
                    Reference ref=refs.next();w.write("XREF\t"+ref+"\n");
                    Function caller=currentProgram.getFunctionManager().getFunctionContaining(ref.getFromAddress());
                    if(caller!=null)w.write("XREF_FUNCTION\t"+ref.getFromAddress()+"\t"+caller.getEntryPoint()+"\t"+caller.getBody()+"\n");
                }
                if(!rootsMode){DecompileResults result=d.decompileFunction(f,60,monitor);
                if(!result.decompileCompleted())throw new Exception("Decompiler "+at);
                w.write("DECOMPILE\n"+result.getDecompiledFunction().getC()+"\n");}
                w.write("END_FUNCTION\n");
            }w.write("COUNT\t"+entries.size()+"\nEND\n");
        }finally{d.dispose();}
    }
}
