// SPDX-License-Identifier: GPL-3.0-or-later
// Original read-only instruction locator. Requires -readOnly -noanalysis.
// Args: NEW local output, preferred VA start/end (positive <= 1 MiB), hex offset.
// Reads existing instructions/functions; writes one exclusive local TSV. No
// analysis, symbols/types/comments/bytes, program or target-process mutations.
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.*;
import java.nio.file.*;
import java.nio.charset.StandardCharsets;
import java.io.BufferedWriter;

public class ScopedFieldUses extends GhidraScript {
    public void run() throws Exception {
        String[] a = getScriptArgs();
        if (a.length != 4 || !a[3].matches("[0-9a-f]{1,4}"))
            throw new IllegalArgumentException("output start end hex-offset");
        Address start = toAddr(a[1]), end = toAddr(a[2]);
        if (end.compareTo(start) <= 0 || end.subtract(start) > 0x100000)
            throw new IllegalArgumentException("range must be positive <= 1 MiB");
        try (BufferedWriter w = Files.newBufferedWriter(Paths.get(a[0]), StandardCharsets.UTF_8, StandardOpenOption.CREATE_NEW)) {
            w.write("SHA256\t" + currentProgram.getExecutableSHA256() + "\nBASE\t" + currentProgram.getImageBase() + "\n");
            InstructionIterator it = currentProgram.getListing().getInstructions(start, true);
            long examined = 0, selected = 0;
            while (it.hasNext() && !monitor.isCancelled()) {
                Instruction x = it.next();
                if (x.getAddress().compareTo(end) >= 0) break;
                examined++;
                String s = x.toString();
                if (!s.contains(" + 0x" + a[3] + "]") || s.contains("[RSP ") || s.contains("[RBP ")) continue;
                Function f = currentProgram.getFunctionManager().getFunctionContaining(x.getAddress());
                w.write("FIELD\t" + x.getAddress() + "\t" + (f == null ? "NO_FUNCTION" : f.getEntryPoint()) + "\t" + s + "\n");
                selected++;
            }
            w.write("END\texamined=" + examined + "\tselected=" + selected + "\tcancelled=" + monitor.isCancelled() + "\n");
        }
    }
}
