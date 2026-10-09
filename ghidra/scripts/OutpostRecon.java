// SPDX-License-Identifier: GPL-3.0-or-later
// Original bounded reader. Invoke only with -readOnly -noanalysis.
// Reads existing defined strings/xrefs/functions; writes one new UTF-8 report.
// No analysis, symbols, types, comments, bytes, or target-process changes.
// Args: output-file then optional exact static function addresses.
import ghidra.app.script.GhidraScript;
import ghidra.app.decompiler.DecompInterface;
import ghidra.app.decompiler.DecompileResults;
import ghidra.program.model.listing.*;
import ghidra.program.model.symbol.*;
import ghidra.program.model.address.Address;
import java.nio.file.*;
import java.nio.charset.StandardCharsets;
import java.io.BufferedWriter;
import java.util.Locale;

public class OutpostRecon extends GhidraScript {
    public void run() throws Exception {
        String[] args = getScriptArgs();
        if (args.length < 1 || args.length > 13) throw new IllegalArgumentException("output plus at most 12 functions");
        try (BufferedWriter out = Files.newBufferedWriter(Paths.get(args[0]), StandardCharsets.UTF_8, StandardOpenOption.CREATE_NEW)) {
            out.write("PROGRAM\t" + currentProgram.getName() + "\nSHA256\t" + currentProgram.getExecutableSHA256()
                + "\nBASE\t" + currentProgram.getImageBase() + "\nLANG\t" + currentProgram.getLanguageID()
                + "\nCOMPILER\t" + currentProgram.getCompilerSpec().getCompilerSpecID() + "\n");
            if (args.length == 1 || (args.length == 2 && (args[1].equals("interfaces") || args[1].equals("exp0002") || args[1].equals("saves")))) {
                boolean exp0002 = args.length == 2 && args[1].equals("exp0002");
                boolean saves = args.length == 2 && args[1].equals("saves");
                DataIterator it = currentProgram.getListing().getDefinedData(true);
                int count = 0;
                while (it.hasNext() && !monitor.isCancelled()) {
                    Data d = it.next();
                    if (!d.hasStringValue()) continue;
                    String s = String.valueOf(d.getValue());
                    String lower = s.toLowerCase(Locale.ROOT);
                    if (saves) {
                        if (!(lower.contains("savegame") || lower.contains("saveload") || lower.contains("manualsave") || lower.contains("quicksave") || lower.contains("deletesave") || lower.contains("save game") || lower.contains("saving game") || lower.contains("savecomplete"))) continue;
                    } else if (exp0002) {
                        if (!java.util.Arrays.asList("getplayer", "getpositionx", "getpositiony", "getpositionz", "getanglex", "getangley", "getanglez", "getparentcell", "getworldspace", "getcurrentlocation", "getbaseobject", "getformid", "is3dloaded", "getworkshop", "getrefs").contains(lower)) continue;
                    } else {
                        if (!(lower.contains("workshop") || lower.contains("outpost") || lower.contains("cargolink") || lower.contains("unfilledcontainers"))) continue;
                        if (args.length == 2 && !(lower.startsWith(".?a") || lower.equals("getworkshop") || lower.equals("getworkshopownedobjects") || lower.equals("getworkshopresourceobjects") || lower.equals("movecontainercontenttounfilledcontainers") || lower.contains("workshop::") || lower.contains("extraworkshop") || (lower.contains("workshop") && (lower.contains("savegame") || lower.contains("loadgame"))))) continue;
                    }
                    if (++count > 350) { out.write("STRING_LIMIT_REACHED\n"); break; }
                    out.write("STRING\t" + d.getAddress() + "\t" + s.replace('\n',' ').replace('\r',' ') + "\n");
                    ReferenceIterator refs = currentProgram.getReferenceManager().getReferencesTo(d.getAddress());
                    int n=0;
                    while (refs.hasNext() && n++ < 8) {
                        Reference r=refs.next();
                        Function f=currentProgram.getFunctionManager().getFunctionContaining(r.getFromAddress());
                        out.write("XREF\t" + r.getFromAddress() + "\t" + r.getReferenceType() + "\t" + (f==null ? "NO_FUNCTION" : f.getEntryPoint()+"\t"+f.getName()) + "\n");
                    }
                    if(refs.hasNext()) out.write("XREF_LIMIT_REACHED\n");
                }
                out.write("SCAN_END\tcancelled=" + monitor.isCancelled() + "\n");
            } else {
                DecompInterface dc = new DecompInterface();
                try {
                    if (!dc.openProgram(currentProgram)) throw new IllegalStateException("decompiler open failed");
                    for (int i=1; i<args.length; i++) {
                        if(args[i].startsWith("win:")) {
                            Address center=toAddr(args[i].substring(4));
                            Instruction x=currentProgram.getListing().getInstructionAt(center);
                            if(x==null) throw new IllegalArgumentException("Window center not an existing instruction");
                            for(int j=0;j<12 && x.getPrevious()!=null;j++) x=x.getPrevious();
                            out.write("WINDOW\t"+center+"\n");
                            for(int j=0;j<45 && x!=null;j++,x=x.getNext()) out.write(x.getAddress()+"\t"+x+"\n");
                            continue;
                        }
                        if(args[i].startsWith("ref:")) {
                            Address target=toAddr(args[i].substring(4));
                            out.write("REFERENCE_TARGET\t"+target+"\n");
                            ReferenceIterator ri=currentProgram.getReferenceManager().getReferencesTo(target);
                            int n=0;
                            while(ri.hasNext() && n++<24) {
                                Reference r=ri.next();
                                Function owner=currentProgram.getFunctionManager().getFunctionContaining(r.getFromAddress());
                                out.write("XREF\t"+r.getFromAddress()+"\t"+(owner==null?"NO_FUNCTION":owner.getEntryPoint()+"\t"+owner.getName())+"\n");
                            }
                            if(ri.hasNext()) out.write("XREF_LIMIT_REACHED\n");
                            continue;
                        }
                        boolean full=args[i].startsWith("full:");
                        Address a=toAddr(full?args[i].substring(5):args[i]);
                        Function f=currentProgram.getFunctionManager().getFunctionAt(a);
                        if(f==null) {
                            out.write("NO_FUNCTION_AT\t"+a+"\n");
                            Instruction x=currentProgram.getListing().getInstructionAt(a);
                            for(int n=0; x!=null && n<40; n++) {
                                out.write(x.getAddress()+"\t"+x+"\n");
                                if(x.getFlowType().isTerminal() || x.getFlowType().isJump()) break;
                                x=x.getNext();
                            }
                            continue;
                        }
                        out.write("FUNCTION\t"+f.getEntryPoint()+"\t"+f.getName()+"\t"+f.getBody()+"\n");
                        InstructionIterator ins=currentProgram.getListing().getInstructions(f.getBody(),true);
                        int n=0;
                        while(ins.hasNext() && n++<600) {Instruction x=ins.next(); out.write(x.getAddress()+"\t"+x+"\n");}
                        if(ins.hasNext()) out.write("INSTRUCTION_LIMIT_REACHED\n");
                        DecompileResults result=dc.decompileFunction(f,30,monitor);
                        out.write("DECOMPILED\t"+result.decompileCompleted()+"\t"+result.getErrorMessage()+"\n");
                        if(result.decompileCompleted()) {
                            String c=result.getDecompiledFunction().getC();
                            int limit=full?250000:50000;
                            out.write(c.substring(0,Math.min(c.length(),limit)));
                            if(c.length()>limit) out.write("\nDECOMPILATION_LIMIT_REACHED\n");
                        }
                    }
                } finally {dc.dispose();}
            }
        }
    }
}
