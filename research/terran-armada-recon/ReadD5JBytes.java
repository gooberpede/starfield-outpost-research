// SPDX-License-Identifier: GPL-3.0-or-later
// Original bounded read-only database-byte export for comparison with installed PE.
// Reads seven explicit existing function bodies; creates one local TSV, no analysis.
import ghidra.app.script.GhidraScript;
import ghidra.program.model.listing.Function;
import ghidra.program.model.address.AddressRangeIterator;
import ghidra.program.model.address.AddressRange;
import java.nio.file.*;
import java.nio.charset.StandardCharsets;
import java.util.HexFormat;
import java.io.BufferedWriter;

public class ReadD5JBytes extends GhidraScript {
    public void run() throws Exception {
        String[] args = getScriptArgs();
        long total = 0;
        try (BufferedWriter w = Files.newBufferedWriter(Paths.get(args[0]),
                StandardCharsets.UTF_8, StandardOpenOption.CREATE_NEW)) {
            w.write("SHA256\t" + currentProgram.getExecutableSHA256() + "\n");
            for (String name : new String[] {"140c5b1d0", "140c49960", "1418af110",
                    "140982210", "140f51350", "140d049b0", "140c9cfb0"}) {
                Function f = currentProgram.getFunctionManager().getFunctionAt(toAddr(name));
                if (f == null) throw new Exception("Missing existing function " + name);
                AddressRangeIterator ranges = f.getBody().getAddressRanges();
                while (ranges.hasNext()) {
                    AddressRange range = ranges.next();
                    int size = Math.toIntExact(range.getLength());
                    total += size;
                    if (total > 262144) throw new Exception("Bounded export size exceeded");
                    byte[] bytes = new byte[size];
                    if (currentProgram.getMemory().getBytes(range.getMinAddress(), bytes) != size)
                        throw new Exception("Short database read");
                    w.write("RANGE\t" + name + "\t" + range.getMinAddress() + "\t"
                            + size + "\t" + HexFormat.of().formatHex(bytes) + "\n");
                }
            }
            w.write("END\n");
        }
    }
}
