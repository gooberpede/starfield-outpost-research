// SPDX-License-Identifier: GPL-3.0-or-later
// Original bounded reader. Invoke only with -readOnly -noanalysis.
// Reads existing defined strings/xrefs/functions; writes one new UTF-8 report.
// No analysis, symbols, types, comments, bytes, or target-process changes.
// Args: NEW output-file then up to12 selectors. Exact VA / full:VA use existing
// function entries only (interior addresses are not silently normalized).
// refall:VA inventories up to4096 existing xrefs; data:VA reads24 qwords around
// a bounded window; sym:substring searches existing symbols (cap256).
// functions:startVA:endVA lists existing entries in a positive <=1MiB range.
// field:HEX / rebase-fields scan existing instructions for literal non-stack
// offsets, not typed alias proofs. terrain-fields/factory-dispatch use explicit
// address ranges below. Every census reports cancellation/coverage; callers
// must check script errors as well as process exit. No new analysis is created.
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

public class Cr1Recon extends GhidraScript {
    public void run() throws Exception {
        String[] args = getScriptArgs();
        if (args.length < 1 || args.length > 13) throw new IllegalArgumentException("output plus at most 12 functions");
        try (BufferedWriter out = Files.newBufferedWriter(Paths.get(args[0]), StandardCharsets.UTF_8, StandardOpenOption.CREATE_NEW)) {
            out.write("PROGRAM\t" + currentProgram.getName() + "\nSHA256\t" + currentProgram.getExecutableSHA256()
                + "\nBASE\t" + currentProgram.getImageBase() + "\nLANG\t" + currentProgram.getLanguageID()
                + "\nCOMPILER\t" + currentProgram.getCompilerSpec().getCompilerSpecID() + "\n");
            if (args.length == 1 || (args.length == 2 && (args[1].equals("interfaces") || args[1].equals("exp0002") || args[1].equals("saves") || args[1].equals("surface")))) {
                boolean exp0002 = args.length == 2 && args[1].equals("exp0002");
                boolean saves = args.length == 2 && args[1].equals("saves");
                boolean surface = args.length == 2 && args[1].equals("surface");
                DataIterator it = currentProgram.getListing().getDefinedData(true);
                int count = 0;
                while (it.hasNext() && !monitor.isCancelled()) {
                    Data d = it.next();
                    if (!d.hasStringValue()) continue;
                    String s = String.valueOf(d.getValue());
                    String lower = s.toLowerCase(Locale.ROOT);
                    if (surface) {
                        if (!(lower.contains("latitude") || lower.contains("longitude") || lower.contains("landing") || lower.contains("planetary") || lower.contains("worldspaceoverlay") || lower.contains("uniquePatternPlacement".toLowerCase(Locale.ROOT)))) continue;
                    } else if (saves) {
                        if (!(lower.contains("savegame") || lower.contains("saveload") || lower.contains("manualsave") || lower.contains("quicksave") || lower.contains("deletesave") || lower.contains("save game") || lower.contains("saving game") || lower.contains("savecomplete"))) continue;
                    } else if (exp0002) {
                        if (!java.util.Arrays.asList("getplayer", "getpositionx", "getpositiony", "getpositionz", "getanglex", "getangley", "getanglez", "getparentcell", "getworldspace", "getcurrentlocation", "getbaseobject", "getformid", "is3dloaded", "getworkshop", "getrefs").contains(lower)) continue;
                    } else {
                        if (!(lower.contains("robot") || lower.contains("buildlimit") || lower.contains("buildcount") || lower.contains("build limit") || lower.contains("itemcount") || lower.contains("objectcount"))) continue;
                        if (args.length == 2 && !(lower.startsWith(".?a") || lower.equals("getworkshop") || lower.equals("getworkshopownedobjects") || lower.equals("getworkshopresourceobjects") || lower.equals("movecontainercontenttounfilledcontainers") || lower.contains("workshop::") || lower.contains("extraworkshop") || (lower.contains("workshop") && (lower.contains("savegame") || lower.contains("loadgame"))))) continue;
                    }
                    if (++count > 1500) { out.write("STRING_LIMIT_REACHED\n"); break; }
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
                        if(args[i].startsWith("functions:")) {
                            String[] bounds=args[i].split(":");
                            if(bounds.length!=3 || !bounds[1].matches("[0-9a-fA-F]{9}") || !bounds[2].matches("[0-9a-fA-F]{9}"))
                                throw new IllegalArgumentException("functions:startVA:endVA");
                            Address start=toAddr(bounds[1]),end=toAddr(bounds[2]);
                            if(end.compareTo(start)<=0 || end.subtract(start)>0x100000)
                                throw new IllegalArgumentException("function inventory range must be positive and <=1MiB");
                            FunctionIterator fi=currentProgram.getFunctionManager().getFunctions(start,true);
                            long selected=0;
                            while(fi.hasNext() && !monitor.isCancelled()) {
                                Function f=fi.next();
                                if(f.getEntryPoint().compareTo(end)>=0) break;
                                out.write("FUNCTION_INVENTORY\t"+f.getEntryPoint()+"\t"+f.getName()+"\t"+f.getBody()+"\n");
                                selected++;
                            }
                            out.write("FUNCTION_INVENTORY_END\t"+start+"\t"+end+"\tselected="+selected+"\tcancelled="+monitor.isCancelled()+"\n");
                            continue;
                        }
                        if(args[i].equals("factory-dispatch")) {
                            Address end=toAddr("142430000");
                            InstructionIterator ii=currentProgram.getListing().getInstructions(toAddr("142400000"),true);
                            long examined=0,selected=0;
                            while(ii.hasNext() && !monitor.isCancelled()) {
                                Instruction x=ii.next();
                                if(x.getAddress().compareTo(end)>=0) break;
                                examined++;
                                String s=x.toString();
                                if(!s.matches("CALL .* \\+ 0x(8|10|18|20|28|30)\\].*")) continue;
                                Function f=currentProgram.getFunctionManager().getFunctionContaining(x.getAddress());
                                out.write("FACTORY_CALL_CANDIDATE\t"+x.getAddress()+"\t"+(f==null?"NO_FUNCTION":f.getEntryPoint())+"\t"+s+"\n");
                                selected++;
                            }
                            out.write("FACTORY_SCAN_END\texamined="+examined+"\tselected="+selected+"\tcancelled="+monitor.isCancelled()+"\n");
                            continue;
                        }
                        if(args[i].equals("rebase-fields") || args[i].equals("terrain-fields") || args[i].startsWith("field:")) {
                            boolean terrain=args[i].equals("terrain-fields");
                            String exact=args[i].startsWith("field:")?args[i].substring(6):null;
                            if(exact!=null && !exact.matches("[0-9a-f]{1,4}")) throw new IllegalArgumentException("field hex offset");
                            InstructionIterator ii=currentProgram.getListing().getInstructions(toAddr("140f20000"),true);
                            long examined=0,selected=0;
                            while(ii.hasNext() && !monitor.isCancelled()) {
                                Instruction x=ii.next(); examined++;
                                if(x.getAddress().compareTo(toAddr("142200000"))>=0) break;
                                String s=x.toString();
                                if(terrain) {
                                    if(x.getAddress().compareTo(toAddr("140780000"))<0 || x.getAddress().compareTo(toAddr("140790000"))>=0) continue;
                                    if(!s.matches(".* \\+ 0x1[def][048c]\\].*")) continue;
                                } else if(exact!=null) {
                                    String va=x.getAddress().toString();
                                    if(!(va.compareTo("140f20000")>=0 && va.compareTo("140fa0000")<0) && !(va.compareTo("142190000")>=0 && va.compareTo("142200000")<0) && !(va.compareTo("141710000")>=0 && va.compareTo("141730000")<0)) continue;
                                    if(!s.contains(" + 0x"+exact+"]")) continue;
                                } else if(!(s.contains(" + 0x1ec]") || s.contains(" + 0x1f0]"))) continue;
                                if(s.contains("[RSP ") || s.contains("[RBP ")) continue;
                                Function f=currentProgram.getFunctionManager().getFunctionContaining(x.getAddress());
                                out.write("FIELD_CANDIDATE\t"+x.getAddress()+"\t"+(f==null?"NO_FUNCTION":f.getEntryPoint())+"\t"+s+"\n");
                                selected++;
                            }
                            out.write("FIELD_SCAN_END\texamined="+examined+"\tselected="+selected+"\tcancelled="+monitor.isCancelled()+"\n");
                            continue;
                        }
                        if(args[i].startsWith("data:")) {
                            Address a=toAddr(args[i].substring(5));
                            out.write("DATA_WINDOW\t"+a+"\n");
                            for(int j=-8;j<16;j++) {
                                Address p=a.add(j*8);
                                long v=currentProgram.getMemory().getLong(p);
                                out.write(p+"\t"+Long.toHexString(v)+"\t"+currentProgram.getSymbolTable().getPrimarySymbol(toAddr(v))+"\n");
                            }
                            continue;
                        }
                        if(args[i].startsWith("sym:")) {
                            String needle=args[i].substring(4);
                            SymbolIterator si=currentProgram.getSymbolTable().getAllSymbols(true);
                            int n=0;
                            while(si.hasNext() && !monitor.isCancelled()) {
                                Symbol s=si.next();
                                if(!s.getName(true).contains(needle)) continue;
                                out.write("SYMBOL\t"+s.getAddress()+"\t"+s.getName(true)+"\n");
                                if(++n>=256) {out.write("SYMBOL_LIMIT_REACHED\n");break;}
                            }
                            continue;
                        }
                        if(args[i].startsWith("win:")) {
                            Address center=toAddr(args[i].substring(4));
                            Instruction x=currentProgram.getListing().getInstructionAt(center);
                            if(x==null) throw new IllegalArgumentException("Window center not an existing instruction");
                            for(int j=0;j<12 && x.getPrevious()!=null;j++) x=x.getPrevious();
                            out.write("WINDOW\t"+center+"\n");
                            for(int j=0;j<45 && x!=null;j++,x=x.getNext()) out.write(x.getAddress()+"\t"+x+"\n");
                            continue;
                        }
                        if(args[i].startsWith("ref:") || args[i].startsWith("refall:")) {
                            boolean all=args[i].startsWith("refall:");
                            int cap=all?4096:24;
                            Address target=toAddr(args[i].substring(all?7:4));
                            out.write("REFERENCE_TARGET\t"+target+"\n");
                            ReferenceIterator ri=currentProgram.getReferenceManager().getReferencesTo(target);
                            int n=0;
                            while(ri.hasNext() && n++<cap) {
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
