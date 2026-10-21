// Original E2 offline orchestration only. Requires existing read-only/noanalysis
// Ghidra project and repository-owned Cr1Recon.java. Reads numbered .request
// files (one selector per line), writes exclusive exports and .done receipts in
// the same ignored local directory. No native execution or program mutations.
// A stop file or actual worker failure ends the session. No network/dependencies.
import ghidra.app.script.GhidraScript;
import java.nio.file.*;
import java.nio.charset.StandardCharsets;
import java.util.*;
public class E2ReadSession extends GhidraScript {
 public void run() throws Exception {
  Path root=Paths.get(getScriptArgs()[0]);
  
  while(!monitor.isCancelled()) {
   if(Files.exists(root.resolve("stop"))) break;
   List<Path> jobs=new ArrayList<>();
   try(DirectoryStream<Path> ds=Files.newDirectoryStream(root,"*.request")) { for(Path p:ds) jobs.add(p); }
   Collections.sort(jobs);
   for(Path p:jobs) {
    Path done=root.resolve(p.getFileName().toString()+".done");
    if(Files.exists(done)) continue;
    List<String> args=new ArrayList<>();
    args.add(root.resolve(p.getFileName().toString()+".tsv").toString());
    args.addAll(Files.readAllLines(p,StandardCharsets.UTF_8));
    runScript(args.size()>1 && (args.get(1).startsWith("calls:") || args.get(1).startsWith("float")) ? "TransitCalls.java" : "Cr1Recon.java",args.toArray(new String[0]));
    Files.writeString(done,"reader returned; inspect output and logs\n",StandardOpenOption.CREATE_NEW);
   }
   Thread.sleep(300);
  }
 }
}
