# Read/export existing native analysis

`ReadWorkshop.java` is original project source-informed research tooling.
Prerequisites: existing pinned Starfield.exe Ghidra project/program and installed
Ghidra 12.1.2/JDK 21; approved offline brief. It reads existing instructions,
function boundaries, xrefs, strings/data as requested and existing decompiler
state. It writes one exclusively new local TSV with program SHA256/base header.
No analysis, symbols/types/comments or target operations are performed.

Run as an installed Ghidra headless post-script with `-readOnly -noanalysis`,
`-process Starfield.exe`, script path this directory, followed by output path
and explicit **quoted** preferred-image VAs. `ref:VA` exports xrefs; `at:VA`
selects a containing function; `range:START:END` walks existing functions.
Exact invocation and installed JVM arguments are retained locally in
`.local-work/workshop-inventory/export.ps1` and per-export logs. The direct JVM
route uses repository-local ignored settings/cache after the ordinary launcher
failed trying to write a protected Java-home settings location.

The installed decompiler's120-second per-function tool timeout is not a
scientific population/output quota. A missing function or incomplete export is
an explicit failed/partial artifact; retain its log and completed prior functions.
No `END` marker is inferred for a partial file. Review decompiler prototypes
against instructions. Do not transfer VAs/layouts to another build.

All full native TSVs/logs remain LOCAL-ONLY and ignored; no executable imports
or databases belong in Git. [Report/dependency map](../../docs/experiments/workshop-membership/dependencies.md)
and source ledger retain authored contracts and hashes. The validator checks
the original database/executable pins after exports. No new tool/dependency
download, live execution or database mutation follows from this script existing.
